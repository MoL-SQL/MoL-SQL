"""Automatic MoL-Full alignment, SQL, and database gates."""

from __future__ import annotations

import sqlite3
import time
import unicodedata
from collections import Counter
from pathlib import Path
from typing import Any

import sqlglot
from sqlglot import exp

from mol_sql.contracts.ids import stable_id
from mol_sql.contracts.io import load_json
from mol_sql.contracts.models import AuditRecord
from mol_sql.dataset.adapters.base import AdaptedSource, FULL_CONFIGURATIONS


def _source_audit(
    source_family: str,
    gate: str,
    *,
    passed: int,
    total: int,
    error_codes: list[str] | None = None,
    details: dict | None = None,
) -> AuditRecord:
    errors = error_codes or []
    return AuditRecord(
        audit_id=stable_id("audit", source_family, gate),
        subject_type="source",
        subject_id=source_family,
        gate=gate,
        status="pass" if passed == total and not errors else "fail",
        error_codes=sorted(set(errors)),
        details={"passed": passed, "total": total, **(details or {})},
    )


def _sqlite_integrity(path: Path) -> tuple[bool, str | None]:
    try:
        uri = f"file:{path.resolve()}?mode=ro"
        with sqlite3.connect(uri, uri=True) as connection:
            row = connection.execute("PRAGMA integrity_check").fetchone()
        result = None if row is None else str(row[0])
        return result == "ok", None if result == "ok" else f"integrity:{result}"
    except sqlite3.Error as exc:
        return False, f"sqlite:{type(exc).__name__}:{exc}"


def _read_only(sql: str) -> None:
    statements = sqlglot.parse(sql, read="sqlite")
    allowed = (exp.Select, exp.Union, exp.Intersect, exp.Except)
    if len(statements) != 1 or not isinstance(statements[0], allowed):
        raise ValueError("not_read_only")
    if any(
        statements[0].find(node) is not None
        for node in (exp.Insert, exp.Update, exp.Delete, exp.Create, exp.Drop)
    ):
        raise ValueError("not_read_only")


def _execute(path: Path, sql: str, timeout_seconds: float) -> list[tuple[Any, ...]]:
    _read_only(sql)
    deadline = time.monotonic() + timeout_seconds
    uri = f"file:{path.resolve()}?mode=ro"
    with sqlite3.connect(uri, uri=True) as connection:
        def decode_text(value: bytes) -> str:
            try:
                return value.decode("utf-8")
            except UnicodeDecodeError:
                return value.decode("latin-1")

        connection.text_factory = decode_text
        connection.set_progress_handler(
            lambda: 1 if time.monotonic() >= deadline else 0,
            1000,
        )
        return connection.execute(sql).fetchall()


def _value_canonicalizer(adapted: AdaptedSource) -> dict[str, dict[str, str]]:
    """Map replacement-pair endpoints to one deterministic representative."""

    path_value = adapted.spec.replacement_map
    if path_value is None:
        return {}
    path = adapted.repo_root / path_value
    if not path.is_file():
        return {}
    raw = load_json(path)
    result: dict[str, dict[str, str]] = {}
    for database_id, replacements in raw.items():
        parent: dict[str, str] = {}

        def find(item: str) -> str:
            parent.setdefault(item, item)
            if parent[item] != item:
                parent[item] = find(parent[item])
            return parent[item]

        def union(left: str, right: str) -> None:
            left_root, right_root = find(left), find(right)
            if left_root != right_root:
                smaller, larger = sorted((left_root, right_root))
                parent[larger] = smaller

        for row in replacements.get("values", []):
            if len(row) >= 4:
                union(str(row[-2]), str(row[-1]))
        groups: dict[str, list[str]] = {}
        for item in parent:
            groups.setdefault(find(item), []).append(item)
        mapping = {}
        for members in groups.values():
            representative = min(members)
            mapping.update({member: representative for member in members})
        result[str(database_id)] = mapping
    return result


def _normalized_rows(
    rows: list[tuple[Any, ...]], mapping: dict[str, str]
) -> list[tuple[Any, ...]]:
    def normalize(value: Any) -> Any:
        if isinstance(value, str):
            value = unicodedata.normalize("NFC", value)
            return mapping.get(value, value)
        if isinstance(value, float):
            return round(value, 6)
        return value

    return [
        tuple(normalize(value) for value in row)
        for row in rows
    ]


def _execution_equivalence(
    adapted: AdaptedSource,
    *,
    timeout_seconds: float,
) -> tuple[AuditRecord, list[str]]:
    source = adapted.spec.source_family
    mappings = _value_canonicalizer(adapted)
    passed = 0
    attempted = 0
    skipped_missing = 0
    failures: Counter[str] = Counter()
    failure_samples: list[dict[str, Any]] = []
    for sample in adapted.samples:
        en_path = adapted.database_paths[("en", sample.database_id)]
        zh_path = adapted.database_paths[("zh", sample.database_id)]
        if en_path is None or zh_path is None:
            skipped_missing += 1
            continue
        attempted += 1
        try:
            en_sql = adapted.execution_sql(
                _sql(adapted, sample.rows["Q_en--S_en--V_en"])
            )
            zh_sql = adapted.execution_sql(
                _sql(adapted, sample.rows["Q_en--S_zh--V_zh"])
            )
            en_rows = _execute(
                en_path,
                en_sql,
                timeout_seconds,
            )
            zh_rows = _execute(
                zh_path,
                zh_sql,
                timeout_seconds,
            )
            mapping = mappings.get(sample.database_id, {})
            left, right = _normalized_rows(en_rows, mapping), _normalized_rows(
                zh_rows, mapping
            )
            ordered = bool(
                sqlglot.parse_one(
                    en_sql,
                    read="sqlite",
                ).args.get("order")
            )
            equal = left == right if ordered else Counter(left) == Counter(right)
            if equal:
                passed += 1
            else:
                failures["result_mismatch"] += 1
                failure_samples.append(
                    {
                        "source_sample_key": sample.source_sample_key,
                        "legacy_index": sample.legacy_index,
                        "database_id": sample.database_id,
                        "error_code": "result_mismatch",
                    }
                )
        except sqlite3.OperationalError as exc:
            code = "timeout" if "interrupted" in str(exc).lower() else "sqlite_error"
            failures[code] += 1
            failure_samples.append(
                {
                    "source_sample_key": sample.source_sample_key,
                    "legacy_index": sample.legacy_index,
                    "database_id": sample.database_id,
                    "error_code": code,
                    "error": str(exc),
                }
            )
        except Exception as exc:
            code = type(exc).__name__
            failures[code] += 1
            failure_samples.append(
                {
                    "source_sample_key": sample.source_sample_key,
                    "legacy_index": sample.legacy_index,
                    "database_id": sample.database_id,
                    "error_code": code,
                    "error": str(exc),
                }
            )
    status = "not_run" if attempted == 0 else ("pass" if passed == attempted else "fail")
    error_codes = sorted(failures)
    if skipped_missing:
        error_codes.append("missing_database_artifact")
    record = AuditRecord(
        audit_id=stable_id("audit", source, "execution_equivalence"),
        subject_type="source",
        subject_id=source,
        gate="execution_equivalence",
        status=status,
        error_codes=sorted(set(error_codes)),
        details={
            "passed": passed,
            "attempted": attempted,
            "skipped_missing_database": skipped_missing,
            "failures": dict(failures),
            "failure_samples": failure_samples,
            "timeout_seconds": timeout_seconds,
        },
    )
    blockers = []
    if attempted == 0:
        blockers.append(f"{source}:execution_equivalence_not_run")
    if failures:
        blockers.append(f"{source}:execution_equivalence_failed:{dict(failures)}")
    if skipped_missing:
        blockers.append(f"{source}:execution_equivalence_incomplete")
    return record, blockers


def _schemas(adapted: AdaptedSource) -> dict[str, dict[str, set[str]]]:
    result: dict[str, dict[str, set[str]]] = {}
    for configuration, path in adapted.tables_paths.items():
        by_database: dict[str, set[str]] = {}
        for row in load_json(path):
            database_id = str(row.get("db_id"))
            by_database[database_id] = {
                str(name).casefold()
                for name in row.get("table_names_original", [])
            }
        result[configuration] = by_database
    return result


def _replacement_map_audit(adapted: AdaptedSource) -> AuditRecord:
    source = adapted.spec.source_family
    configured = adapted.spec.replacement_map
    if configured is None:
        return AuditRecord(
            audit_id=stable_id("audit", source, "replacement_map_consistency"),
            subject_type="source",
            subject_id=source,
            gate="replacement_map_consistency",
            status="fail",
            error_codes=["replacement_map_not_configured"],
        )
    path = adapted.repo_root / configured
    if not path.is_file():
        return AuditRecord(
            audit_id=stable_id("audit", source, "replacement_map_consistency"),
            subject_type="source",
            subject_id=source,
            gate="replacement_map_consistency",
            status="fail",
            error_codes=["replacement_map_missing"],
            artifact_refs=[configured],
        )
    raw = load_json(path)
    release_database_ids = {sample.database_id for sample in adapted.samples}
    fixed_columns: set[tuple[str, str, str]] = set()
    fixed_value_columns: set[tuple[str, str, str]] = set()
    fixed_point_ref = adapted.spec.fixed_points
    if fixed_point_ref:
        fixed_point_path = adapted.repo_root / fixed_point_ref
        if not fixed_point_path.is_file():
            return AuditRecord(
                audit_id=stable_id("audit", source, "replacement_map_consistency"),
                subject_type="source",
                subject_id=source,
                gate="replacement_map_consistency",
                status="fail",
                error_codes=["fixed_points_missing"],
                artifact_refs=[configured, fixed_point_ref],
            )
        policy = load_json(fixed_point_path)
        if policy.get("source_family") != source:
            return AuditRecord(
                audit_id=stable_id("audit", source, "replacement_map_consistency"),
                subject_type="source",
                subject_id=source,
                gate="replacement_map_consistency",
                status="fail",
                error_codes=["fixed_points_source_mismatch"],
                artifact_refs=[configured, fixed_point_ref],
            )
        fixed_columns = {
            (str(row["database_id"]), str(row["table"]), str(row["column"]))
            for row in policy.get("columns", [])
        }
        fixed_value_columns = {
            (str(row["database_id"]), str(row["table"]), str(row["column"]))
            for row in policy.get("value_columns", [])
        }
    errors: Counter[str] = Counter()
    counts: Counter[str] = Counter()
    fixed_points: Counter[str] = Counter()
    out_of_scope_databases: list[str] = []
    for database_id, mapping in raw.items():
        database_id = str(database_id)
        if database_id not in release_database_ids:
            out_of_scope_databases.append(database_id)
            continue
        if not isinstance(mapping, dict):
            errors["invalid_database_mapping"] += 1
            continue
        table_sources: dict[str, str] = {}
        table_targets: dict[str, str] = {}
        for row in mapping.get("tables", []):
            if not isinstance(row, list) or len(row) != 2:
                errors["invalid_table_entry"] += 1
                continue
            source_name, target_name = map(str, row)
            counts["tables"] += 1
            if source_name == target_name:
                fixed_points["tables"] += 1
            if (
                source_name in table_sources
                and table_sources[source_name] != target_name
            ):
                errors["inconsistent_table_source"] += 1
            if (
                target_name in table_targets
                and table_targets[target_name] != source_name
            ):
                errors["table_target_collision"] += 1
            table_sources[source_name] = target_name
            table_targets[target_name] = source_name

        column_sources: dict[tuple[str, str], str] = {}
        column_targets: dict[tuple[str, str], str] = {}
        for row in mapping.get("columns", []):
            if not isinstance(row, list) or len(row) != 3:
                errors["invalid_column_entry"] += 1
                continue
            table, source_name, target_name = map(str, row)
            counts["columns"] += 1
            if (database_id, table, source_name) in fixed_columns:
                errors["fixed_column_replaced"] += 1
            if source_name == target_name:
                fixed_points["columns"] += 1
            source_key, target_key = (table, source_name), (table, target_name)
            if (
                source_key in column_sources
                and column_sources[source_key] != target_name
            ):
                errors["inconsistent_column_source"] += 1
            if (
                target_key in column_targets
                and column_targets[target_key] != source_name
            ):
                errors["column_target_collision"] += 1
            column_sources[source_key] = target_name
            column_targets[target_key] = source_name

        value_sources: dict[tuple[str, str, str], str] = {}
        for row in mapping.get("values", []):
            if not isinstance(row, list) or len(row) != 4:
                errors["invalid_value_entry"] += 1
                continue
            table, column, source_value, target_value = map(str, row)
            counts["values"] += 1
            if (database_id, table, column) in fixed_value_columns:
                errors["fixed_value_column_replaced"] += 1
            if source_value == target_value:
                fixed_points["values"] += 1
            key = (table, column, source_value)
            if key in value_sources and value_sources[key] != target_value:
                errors["inconsistent_value_source"] += 1
            value_sources[key] = target_value
        counts["databases"] += 1
        if not database_id:
            errors["empty_database_id"] += 1
    return AuditRecord(
        audit_id=stable_id("audit", source, "replacement_map_consistency"),
        subject_type="source",
        subject_id=source,
        gate="replacement_map_consistency",
        status="pass" if not errors else "fail",
        error_codes=sorted(errors),
        details={
            "counts": dict(counts),
            "fixed_points": dict(fixed_points),
            "errors": dict(errors),
            "release_database_count": len(release_database_ids),
            "out_of_scope_database_count": len(out_of_scope_databases),
            "out_of_scope_databases": sorted(out_of_scope_databases),
        },
        artifact_refs=[
            ref
            for ref in (configured, fixed_point_ref, adapted.spec.replacement_proposals)
            if ref
        ],
    )


def _quote_identifier(identifier: str) -> str:
    return '"' + identifier.replace('"', '""') + '"'


def _fixed_point_data_audit(adapted: AdaptedSource) -> AuditRecord:
    source = adapted.spec.source_family
    configured = adapted.spec.fixed_points
    gate = "fixed_point_data_consistency"
    if configured is None:
        return AuditRecord(
            audit_id=stable_id("audit", source, gate),
            subject_type="source",
            subject_id=source,
            gate=gate,
            status="not_applicable",
        )
    policy_path = adapted.repo_root / configured
    map_path = (
        adapted.repo_root / adapted.spec.replacement_map
        if adapted.spec.replacement_map
        else None
    )
    if not policy_path.is_file() or map_path is None or not map_path.is_file():
        return AuditRecord(
            audit_id=stable_id("audit", source, gate),
            subject_type="source",
            subject_id=source,
            gate=gate,
            status="fail",
            error_codes=["fixed_point_artifact_missing"],
            artifact_refs=[
                ref
                for ref in (configured, adapted.spec.replacement_map)
                if ref
            ],
        )
    policy = load_json(policy_path)
    replacements = load_json(map_path)
    failures: list[dict[str, Any]] = []
    checked = 0

    def translated_names(
        database_id: str, table: str, column: str
    ) -> tuple[str, str]:
        mapping = replacements.get(database_id, {})
        target_table = next(
            (
                str(row[1])
                for row in mapping.get("tables", [])
                if len(row) == 2 and str(row[0]) == table
            ),
            table,
        )
        target_column = next(
            (
                str(row[2])
                for row in mapping.get("columns", [])
                if len(row) == 3
                and str(row[0]) == table
                and str(row[1]) == column
            ),
            column,
        )
        return target_table, target_column

    for row in policy.get("columns", []):
        database_id = str(row["database_id"])
        if database_id not in {sample.database_id for sample in adapted.samples}:
            continue
        table, column = str(row["table"]), str(row["column"])
        target_table, target_column = translated_names(database_id, table, column)
        en_path = adapted.database_paths.get(("en", database_id))
        zh_path = adapted.database_paths.get(("zh", database_id))
        checked += 1
        if en_path is None or zh_path is None:
            failures.append(
                {"database_id": database_id, "error_code": "missing_database_artifact"}
            )
            continue
        try:
            with sqlite3.connect(f"file:{en_path.resolve()}?mode=ro", uri=True) as en_db:
                en_columns = {
                    str(item[1])
                    for item in en_db.execute(
                        f"PRAGMA table_info({_quote_identifier(table)})"
                    )
                }
            with sqlite3.connect(f"file:{zh_path.resolve()}?mode=ro", uri=True) as zh_db:
                zh_columns = {
                    str(item[1])
                    for item in zh_db.execute(
                        f"PRAGMA table_info({_quote_identifier(target_table)})"
                    )
                }
            if column not in en_columns or target_column not in zh_columns:
                failures.append(
                    {
                        "database_id": database_id,
                        "table": table,
                        "column": column,
                        "error_code": "fixed_column_missing",
                    }
                )
        except sqlite3.Error as exc:
            failures.append(
                {
                    "database_id": database_id,
                    "error_code": "fixed_point_sqlite_error",
                    "error": str(exc),
                }
            )

    for row in policy.get("value_columns", []):
        database_id = str(row["database_id"])
        if database_id not in {sample.database_id for sample in adapted.samples}:
            continue
        table, column = str(row["table"]), str(row["column"])
        key_column = row.get("key_column")
        target_table, target_column = translated_names(database_id, table, column)
        target_key = (
            translated_names(database_id, table, str(key_column))[1]
            if key_column
            else None
        )
        en_path = adapted.database_paths.get(("en", database_id))
        zh_path = adapted.database_paths.get(("zh", database_id))
        checked += 1
        if en_path is None or zh_path is None:
            failures.append(
                {"database_id": database_id, "error_code": "missing_database_artifact"}
            )
            continue
        try:
            if key_column:
                en_sql = (
                    f"SELECT {_quote_identifier(str(key_column))}, "
                    f"{_quote_identifier(column)} FROM {_quote_identifier(table)}"
                )
                zh_sql = (
                    f"SELECT {_quote_identifier(str(target_key))}, "
                    f"{_quote_identifier(target_column)} "
                    f"FROM {_quote_identifier(target_table)}"
                )
            else:
                en_sql = (
                    f"SELECT {_quote_identifier(column)} "
                    f"FROM {_quote_identifier(table)}"
                )
                zh_sql = (
                    f"SELECT {_quote_identifier(target_column)} "
                    f"FROM {_quote_identifier(target_table)}"
                )
            with sqlite3.connect(f"file:{en_path.resolve()}?mode=ro", uri=True) as en_db:
                en_rows = en_db.execute(en_sql).fetchall()
            with sqlite3.connect(f"file:{zh_path.resolve()}?mode=ro", uri=True) as zh_db:
                zh_rows = zh_db.execute(zh_sql).fetchall()
            equal = (
                dict(en_rows) == dict(zh_rows)
                if key_column
                else Counter(en_rows) == Counter(zh_rows)
            )
            if not equal:
                failures.append(
                    {
                        "database_id": database_id,
                        "table": table,
                        "column": column,
                        "error_code": "fixed_value_data_mismatch",
                        "source_rows": len(en_rows),
                        "target_rows": len(zh_rows),
                    }
                )
        except sqlite3.Error as exc:
            failures.append(
                {
                    "database_id": database_id,
                    "error_code": "fixed_point_sqlite_error",
                    "error": str(exc),
                }
            )
    return AuditRecord(
        audit_id=stable_id("audit", source, gate),
        subject_type="source",
        subject_id=source,
        gate=gate,
        status="pass" if not failures else "fail",
        error_codes=sorted({row["error_code"] for row in failures}),
        details={
            "checked": checked,
            "passed": checked - len(failures),
            "failure_samples": failures,
        },
        artifact_refs=[configured, adapted.spec.replacement_map],
    )


def _database_profile(path: Path) -> list[tuple[int, int, int, int, int]]:
    uri = f"file:{path.resolve()}?mode=ro"
    profiles: list[tuple[int, int, int, int, int]] = []
    with sqlite3.connect(uri, uri=True) as connection:
        tables = [
            str(row[0])
            for row in connection.execute(
                "SELECT name FROM sqlite_master "
                "WHERE type = 'table' AND name NOT LIKE 'sqlite_%' ORDER BY name"
            )
        ]
        for table in tables:
            escaped = table.replace('"', '""')
            columns = connection.execute(
                f'PRAGMA table_info("{escaped}")'
            ).fetchall()
            foreign_keys = connection.execute(
                f'PRAGMA foreign_key_list("{escaped}")'
            ).fetchall()
            indices = connection.execute(
                f'PRAGMA index_list("{escaped}")'
            ).fetchall()
            row_count = int(
                connection.execute(
                    f'SELECT COUNT(*) FROM "{escaped}"'
                ).fetchone()[0]
            )
            profiles.append(
                (
                    len(columns),
                    sum(int(column[5]) > 0 for column in columns),
                    len(foreign_keys),
                    sum(bool(index[2]) for index in indices),
                    row_count,
                )
            )
    return sorted(profiles)


def _structural_equivalence_audit(adapted: AdaptedSource) -> AuditRecord:
    source = adapted.spec.source_family
    database_ids = sorted({sample.database_id for sample in adapted.samples})
    passed = 0
    skipped = 0
    failure_databases: list[dict[str, Any]] = []
    for database_id in database_ids:
        en_path = adapted.database_paths[("en", database_id)]
        zh_path = adapted.database_paths[("zh", database_id)]
        if en_path is None or zh_path is None:
            skipped += 1
            continue
        try:
            en_profile, zh_profile = _database_profile(en_path), _database_profile(
                zh_path
            )
            if en_profile == zh_profile:
                passed += 1
            else:
                failure_databases.append(
                    {
                        "database_id": database_id,
                        "error_code": "structural_profile_mismatch",
                        "en_tables": len(en_profile),
                        "zh_tables": len(zh_profile),
                    }
                )
        except sqlite3.Error as exc:
            failure_databases.append(
                {
                    "database_id": database_id,
                    "error_code": "structural_profile_error",
                    "error": str(exc),
                }
            )
    attempted = passed + len(failure_databases)
    if failure_databases:
        status = "fail"
    elif skipped:
        status = "warning"
    else:
        status = "pass"
    return AuditRecord(
        audit_id=stable_id("audit", source, "database_structural_equivalence"),
        subject_type="source",
        subject_id=source,
        gate="database_structural_equivalence",
        status=status,
        error_codes=sorted(
            {
                item["error_code"] for item in failure_databases
            }
            | ({"missing_database_artifact"} if skipped else set())
        ),
        details={
            "passed": passed,
            "attempted": attempted,
            "skipped_missing_database": skipped,
            "profile": "multiset(columns, primary_keys, foreign_keys, unique_indices, rows)",
            "failure_databases": failure_databases,
        },
    )


def _scope_reference_audit(adapted: AdaptedSource) -> AuditRecord:
    """Conservatively validate physical tables and qualified aliases."""

    schemas = _schemas(adapted)
    passed = 0
    total = len(adapted.samples) * len(FULL_CONFIGURATIONS)
    failure_samples: list[dict[str, Any]] = []
    for sample in adapted.samples:
        for configuration in FULL_CONFIGURATIONS:
            try:
                tree = sqlglot.parse_one(
                    _sql(adapted, sample.rows[configuration]),
                    read="sqlite",
                )
                cte_names = {
                    cte.alias_or_name.casefold() for cte in tree.find_all(exp.CTE)
                }
                physical_tables = []
                qualifiers = set(cte_names)
                qualifiers.update(
                    subquery.alias.casefold()
                    for subquery in tree.find_all(exp.Subquery)
                    if subquery.alias
                )
                for table in tree.find_all(exp.Table):
                    name = table.name.casefold()
                    qualifiers.add(name)
                    if table.alias:
                        qualifiers.add(table.alias.casefold())
                    if name not in cte_names:
                        physical_tables.append(name)
                expected = schemas[configuration].get(sample.database_id, set())
                missing_tables = sorted(set(physical_tables) - expected)
                unknown_qualifiers = sorted(
                    {
                        column.table.casefold()
                        for column in tree.find_all(exp.Column)
                        if column.table and column.table.casefold() not in qualifiers
                    }
                )
                if missing_tables or unknown_qualifiers:
                    failure_samples.append(
                        {
                            "source_sample_key": sample.source_sample_key,
                            "legacy_index": sample.legacy_index,
                            "database_id": sample.database_id,
                            "configuration": configuration,
                            "error_code": "scope_reference_failure",
                            "missing_tables": missing_tables,
                            "unknown_qualifiers": unknown_qualifiers,
                        }
                    )
                else:
                    passed += 1
            except Exception as exc:
                failure_samples.append(
                    {
                        "source_sample_key": sample.source_sample_key,
                        "legacy_index": sample.legacy_index,
                        "database_id": sample.database_id,
                        "configuration": configuration,
                        "error_code": "scope_reference_exception",
                        "error": f"{type(exc).__name__}:{exc}",
                    }
                )
    return AuditRecord(
        audit_id=stable_id(
            "audit", adapted.spec.source_family, "sql_scope_reference"
        ),
        subject_type="source",
        subject_id=adapted.spec.source_family,
        gate="sql_scope_reference",
        status="pass" if passed == total else "fail",
        error_codes=(
            [] if passed == total else ["sql_scope_reference_failure"]
        ),
        details={
            "passed": passed,
            "total": total,
            "validation_level": "physical_tables_and_qualified_aliases",
            "failure_samples": failure_samples,
        },
    )


def audit_source(
    adapted: AdaptedSource,
    *,
    check_database_integrity: bool,
    execute_equivalence: bool,
    execution_timeout_seconds: float,
) -> tuple[list[AuditRecord], list[str]]:
    """Return aggregate audit records and release blockers for one source."""

    source = adapted.spec.source_family
    records: list[AuditRecord] = []
    blockers: list[str] = []

    sql_total = len(adapted.samples) * len(FULL_CONFIGURATIONS)
    sql_passed = 0
    sql_errors: Counter[str] = Counter()
    question_passed = 0
    question_total = sql_total
    coupled_sql_passed = 0
    coupled_sql_total = len(adapted.samples) * 2
    database_id_passed = 0

    for sample in adapted.samples:
        if (
            len(
                {
                    str(
                        sample.rows[configuration].get(
                            "db_id", sample.rows[configuration].get("db_name")
                        )
                    )
                    for configuration in FULL_CONFIGURATIONS
                }
            )
            == 1
        ):
            database_id_passed += 1
        for configuration in FULL_CONFIGURATIONS:
            row = sample.rows[configuration]
            question = row.get("question")
            if isinstance(question, str) and question.strip():
                question_passed += 1
            try:
                sqlglot.parse_one(
                    _sql(adapted, row),
                    read="sqlite",
                    error_level="raise",
                )
                sql_passed += 1
            except Exception as exc:
                sql_errors[f"{type(exc).__name__}"] += 1

        if _sql(adapted, sample.rows[FULL_CONFIGURATIONS[0]]) == _sql(
            adapted, sample.rows[FULL_CONFIGURATIONS[1]]
        ):
            coupled_sql_passed += 1
        if _sql(adapted, sample.rows[FULL_CONFIGURATIONS[2]]) == _sql(
            adapted, sample.rows[FULL_CONFIGURATIONS[3]]
        ):
            coupled_sql_passed += 1

    records.append(
        _source_audit(
            source,
            "four_cell_alignment",
            passed=database_id_passed,
            total=len(adapted.samples),
        )
    )
    records.append(_replacement_map_audit(adapted))
    records.append(_fixed_point_data_audit(adapted))
    records.append(_scope_reference_audit(adapted))
    records.append(
        _source_audit(
            source,
            "question_nonempty",
            passed=question_passed,
            total=question_total,
        )
    )
    records.append(
        _source_audit(
            source,
            "sql_parse",
            passed=sql_passed,
            total=sql_total,
            error_codes=list(sql_errors),
            details={"errors": dict(sql_errors)},
        )
    )
    records.append(
        _source_audit(
            source,
            "question_only_sql_invariance",
            passed=coupled_sql_passed,
            total=coupled_sql_total,
        )
    )

    expected_databases = len(adapted.database_paths)
    present_databases = sum(path is not None for path in adapted.database_paths.values())
    missing = [
        f"{language}:{database_id}"
        for (language, database_id), path in sorted(adapted.database_paths.items())
        if path is None
    ]
    db_status = "pass" if not missing else "fail"
    records.append(
        AuditRecord(
            audit_id=stable_id("audit", source, "database_presence"),
            subject_type="source",
            subject_id=source,
            gate="database_presence",
            status=db_status,
            error_codes=["missing_database_artifact"] if missing else [],
            details={
                "passed": present_databases,
                "total": expected_databases,
                "missing": missing,
            },
        )
    )
    blockers.extend(f"{source}:missing_database:{item}" for item in missing)
    records.append(_structural_equivalence_audit(adapted))

    unique_paths = sorted(
        {path for path in adapted.database_paths.values() if path is not None}
    )
    if not check_database_integrity:
        records.append(
            AuditRecord(
                audit_id=stable_id("audit", source, "database_integrity"),
                subject_type="source",
                subject_id=source,
                gate="database_integrity",
                status="not_run",
                error_codes=["database_integrity_not_run"],
                details={"available_databases": len(unique_paths)},
            )
        )
        blockers.append(f"{source}:database_integrity_not_run")
    else:
        failures: list[str] = []
        passed = 0
        for path in unique_paths:
            ok, error = _sqlite_integrity(path)
            if ok:
                passed += 1
            else:
                failures.append(f"{path.name}:{error}")
        records.append(
            _source_audit(
                source,
                "database_integrity",
                passed=passed,
                total=len(unique_paths),
                error_codes=["database_integrity_failure"] if failures else [],
                details={"failures": failures},
            )
        )
        blockers.extend(f"{source}:database_integrity:{item}" for item in failures)

    if execute_equivalence:
        execution_record, execution_blockers = _execution_equivalence(
            adapted,
            timeout_seconds=execution_timeout_seconds,
        )
        records.append(execution_record)
        blockers.extend(execution_blockers)
    else:
        records.append(
            AuditRecord(
                audit_id=stable_id("audit", source, "execution_equivalence"),
                subject_type="source",
                subject_id=source,
                gate="execution_equivalence",
                status="not_run",
                error_codes=["execution_equivalence_not_run"],
                details={"logical_instances": len(adapted.samples)},
            )
        )
        blockers.append(f"{source}:execution_equivalence_not_run")

    for record in records:
        if record.status in {"fail", "warning"} and record.gate not in {
            "database_presence"
        }:
            blockers.append(f"{source}:automatic_gate_failed:{record.gate}")
    return records, sorted(set(blockers))


def _sql(adapted: AdaptedSource, row: dict) -> str:
    for field in adapted.spec.sql_fields:
        value = row.get(field)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""
