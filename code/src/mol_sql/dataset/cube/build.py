"""Deterministic engineering build for the MoL-Cube eight-cell panel."""

from __future__ import annotations

import math
import shutil
import sqlite3
import time
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from mol_sql.contracts.hashing import sha256_file, sha256_json
from mol_sql.contracts.ids import stable_id
from mol_sql.contracts.io import load_json, load_jsonl, write_json, write_jsonl
from mol_sql.contracts.models import (
    LogicalInstance,
    Realization,
    ReleaseManifest,
    SourceRecord,
)
from mol_sql.dataset.full.rewrite import (
    rewrite_sql_components,
    transplant_sql_values,
)
from mol_sql.dataset.statistics.models import (
    FullLogicalProfile,
    FullStatisticsManifest,
)

from .models import (
    CUBE_CONFIGURATIONS,
    CubeCandidateProfile,
    CubeMembership,
    CubeRealization,
    CubeReleaseManifest,
)


@dataclass(frozen=True)
class CubeBuildOptions:
    repo_root: Path
    full_release_dir: Path
    full_statistics_dir: Path
    sampler_config: Path
    output_dir: Path
    allow_draft: bool = False
    overwrite: bool = False
    resume: bool = False
    execute_equivalence: bool = True
    execution_timeout_seconds: float = 30.0


def _resolve(repo_root: Path, path: Path | str) -> Path:
    candidate = Path(path)
    return candidate if candidate.is_absolute() else repo_root / candidate


def _relative(repo_root: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        return str(path.resolve())


def _load_yaml(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        value = yaml.safe_load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a YAML mapping")
    return value


def _barriers(profile: FullLogicalProfile) -> tuple[list[str], dict[str, Any], list[str]]:
    sql = profile.sql_features
    schema = profile.schema_features
    support = profile.treatment_support
    controls = profile.controls
    barriers: list[str] = []
    evidence: dict[str, Any] = {}

    compositional = any(
        (
            sql.get("condition_count", 0) >= 2,
            sql.get("nested_query_count", 0) > 0,
            sql.get("set_operation_count", 0) > 0,
            sql.get("group_by", False),
            sql.get("having", False),
        )
    )
    if compositional:
        barriers.append("Q-COMP")
        evidence["Q-COMP"] = {
            key: sql.get(key)
            for key in (
                "condition_count",
                "nested_query_count",
                "set_operation_count",
                "group_by",
                "having",
            )
        }
    if schema.get("distractor_table_count", 0) > 0 or schema.get(
        "distractor_column_count", 0
    ) >= 5:
        barriers.append("S-SELECT")
        evidence["S-SELECT"] = {
            "distractor_table_count": schema.get("distractor_table_count", 0),
            "distractor_column_count": schema.get("distractor_column_count", 0),
        }
    if schema.get("requires_join", False):
        barriers.append("S-JOIN")
        evidence["S-JOIN"] = {
            "join_count": sql.get("join_count", 0),
            "requires_bridge_table": schema.get("requires_bridge_table"),
        }
    if support.get("s_treatment_present", False):
        barriers.append("S-LEX")
        evidence["S-LEX"] = {
            "mapped_reference_count": support.get("s_mapped_reference_count", 0),
            "treatment_intensity": support.get("s_treatment_intensity", 0.0),
        }
    if support.get("v_treatment_present", False):
        barriers.append("V-EXACT")
        evidence["V-EXACT"] = {
            "mapped_literal_count": support.get("v_mapped_literal_count", 0),
            "treatment_intensity": support.get("v_treatment_intensity", 0.0),
        }
    if controls.get("recurring_entity", False):
        barriers.append("V-RECUR")
        evidence["V-RECUR"] = {
            "recurring_entity_count": profile.value_features.get(
                "recurring_entity_count", 0
            )
        }

    q_support = bool(support.get("q_treatment_present", False))
    s_support = bool(support.get("s_treatment_present", False))
    v_support = bool(support.get("v_treatment_present", False))
    for label, present in (
        ("I-QS", q_support and s_support),
        ("I-QV", q_support and v_support),
        ("I-SV", s_support and v_support),
        ("I-QSV", q_support and s_support and v_support and compositional),
    ):
        if present:
            barriers.append(label)
            evidence[label] = {
                "q_support": q_support,
                "s_support": s_support,
                "v_support": v_support,
                "q_compositional": compositional,
            }

    pending = ["Q-LEX", "Q-REF"] if q_support else []
    return barriers, evidence, pending


def _english_to_chinese_replacements(
    replacements: dict[str, Any],
    native_language: str,
) -> dict[str, Any]:
    if native_language == "en":
        return replacements
    table_map = {
        str(source): str(target)
        for source, target in replacements.get("tables", [])
    }
    column_map = {
        (str(table), str(source)): str(target)
        for table, source, target in replacements.get("columns", [])
    }
    return {
        "tables": [
            [str(target), str(source)]
            for source, target in replacements.get("tables", [])
        ],
        "columns": [
            [
                table_map.get(str(table), str(table)),
                str(target_column),
                str(source_column),
            ]
            for table, source_column, target_column in replacements.get("columns", [])
        ],
        "values": [
            [
                table_map.get(str(table), str(table)),
                column_map.get((str(table), str(source_column)), str(source_column)),
                target_value,
                source_value,
            ]
            for table, source_column, source_value, target_value in replacements.get(
                "values", []
            )
        ],
    }


def _schema_replacements_from_metadata(
    english_tables: list[dict[str, Any]],
    chinese_tables: list[dict[str, Any]],
    database_id: str,
) -> dict[str, list[list[Any]]]:
    english = next(
        (row for row in english_tables if str(row.get("db_id")) == database_id),
        None,
    )
    chinese = next(
        (row for row in chinese_tables if str(row.get("db_id")) == database_id),
        None,
    )
    if english is None or chinese is None:
        raise ValueError(f"missing paired schema metadata for {database_id}")

    english_table_names = english.get("table_names_original", [])
    chinese_table_names = chinese.get("table_names_original", [])
    if len(english_table_names) != len(chinese_table_names):
        raise ValueError(f"paired table count mismatch for {database_id}")
    tables = [
        [str(source), str(target)]
        for source, target in zip(english_table_names, chinese_table_names, strict=True)
    ]

    english_columns = english.get("column_names_original", [])
    chinese_columns = chinese.get("column_names_original", [])
    if len(english_columns) != len(chinese_columns):
        raise ValueError(f"paired column count mismatch for {database_id}")
    columns: list[list[Any]] = []
    for english_column, chinese_column in zip(
        english_columns, chinese_columns, strict=True
    ):
        english_table_index, english_name = english_column
        chinese_table_index, chinese_name = chinese_column
        if english_table_index != chinese_table_index:
            raise ValueError(f"paired column table mismatch for {database_id}")
        if int(english_table_index) < 0:
            continue
        columns.append(
            [
                str(english_table_names[int(english_table_index)]),
                str(english_name),
                str(chinese_name),
            ]
        )
    return {"tables": tables, "columns": columns}


def build_candidate_profiles(
    profiles: list[FullLogicalProfile],
) -> list[CubeCandidateProfile]:
    candidates = []
    for profile in profiles:
        barriers, evidence, pending = _barriers(profile)
        candidates.append(
            CubeCandidateProfile(
                logical_id=profile.logical_id,
                source_family=profile.source_family,
                database_id=profile.database_id,
                split=profile.split,
                source_sample_key=profile.source_sample_key,
                legacy_index=profile.legacy_index,
                treatment_support=profile.treatment_support,
                controls=profile.controls,
                difficulty=profile.difficulty,
                barrier_opportunities=barriers,
                barrier_evidence=evidence,
                pending_human_annotations=pending,
            )
        )
    return sorted(candidates, key=lambda row: row.logical_id)


def _stable_tie(seed: int, logical_id: str) -> str:
    return stable_id("cube-rank", str(seed), logical_id)


def _target_tiers(target: int, proportions: dict[str, float]) -> dict[str, int]:
    raw = {tier: target * float(proportions.get(tier, 0.0)) for tier in proportions}
    counts = {tier: math.floor(value) for tier, value in raw.items()}
    remainder = target - sum(counts.values())
    for tier in sorted(raw, key=lambda key: (raw[key] - counts[key], key), reverse=True):
        if remainder <= 0:
            break
        counts[tier] += 1
        remainder -= 1
    return counts


def sample_cube_membership(
    candidates: list[CubeCandidateProfile],
    config: dict[str, Any],
) -> tuple[list[CubeMembership], list[dict[str, Any]]]:
    seed = int(config["seed"])
    target_per_source = int(config["target_per_source"])
    database_fraction = float(config.get("database_max_fraction", 1.0))
    difficulty_proportions = dict(config.get("difficulty_proportions", {}))
    minimums = dict(config.get("minimums_per_source", {}))
    by_source: dict[str, list[CubeCandidateProfile]] = defaultdict(list)
    for candidate in candidates:
        by_source[candidate.source_family].append(candidate)

    selected_ids: set[str] = set()
    reasons: dict[str, list[str]] = defaultdict(list)
    shortfalls: list[dict[str, Any]] = []
    rank = 0
    ranks: dict[str, int] = {}

    for source, pool in sorted(by_source.items()):
        target = min(target_per_source, len(pool))
        tier_targets = _target_tiers(target, difficulty_proportions)
        configured_database_cap = max(1, math.ceil(target * database_fraction))
        database_total = max(1, len({candidate.database_id for candidate in pool}))
        feasible_database_cap = math.ceil(target / database_total)
        database_cap = max(configured_database_cap, feasible_database_cap)
        if feasible_database_cap > configured_database_cap:
            shortfalls.append(
                {
                    "source_family": source,
                    "quota": "database_max_fraction_infeasible",
                    "required_max": configured_database_cap,
                    "minimum_feasible_max": feasible_database_cap,
                    "database_count": database_total,
                }
            )
        selected: list[CubeCandidateProfile] = []
        database_counts: Counter[str] = Counter()
        tier_counts: Counter[str] = Counter()
        feature_counts: Counter[str] = Counter()

        def feature(candidate: CubeCandidateProfile, name: str) -> bool:
            if name == "v_support":
                return bool(candidate.treatment_support.get("v_treatment_present"))
            if name in {"literal_free", "recurring_entity"}:
                return bool(candidate.controls.get(name))
            return name in candidate.barrier_opportunities

        remaining = list(pool)
        while remaining and len(selected) < target:
            scored = []
            for candidate in remaining:
                tier = str(candidate.difficulty.get("composite_tier", "medium"))
                unmet_features = sum(
                    max(0, int(required) - feature_counts[name])
                    for name, required in minimums.items()
                    if feature(candidate, name)
                )
                tier_need = max(0, tier_targets.get(tier, 0) - tier_counts[tier])
                barrier_gain = sum(
                    1 for label in candidate.barrier_opportunities if feature_counts[label] == 0
                )
                treatment_gain = sum(
                    bool(candidate.treatment_support.get(key))
                    for key in (
                        "q_treatment_present",
                        "s_treatment_present",
                        "v_treatment_present",
                    )
                )
                over_database_cap = database_counts[candidate.database_id] >= database_cap
                scored.append(
                    (
                        over_database_cap,
                        -unmet_features,
                        -tier_need,
                        -barrier_gain,
                        -treatment_gain,
                        database_counts[candidate.database_id],
                        _stable_tie(seed, candidate.logical_id),
                        candidate,
                    )
                )
            scored.sort(key=lambda row: row[:-1])
            chosen = scored[0][-1]
            remaining.remove(chosen)
            selected.append(chosen)
            database_counts[chosen.database_id] += 1
            tier = str(chosen.difficulty.get("composite_tier", "medium"))
            tier_counts[tier] += 1
            for label in chosen.barrier_opportunities:
                feature_counts[label] += 1
            for name in minimums:
                if feature(chosen, name):
                    feature_counts[name] += 1
            selected_ids.add(chosen.logical_id)
            rank += 1
            ranks[chosen.logical_id] = rank
            reasons[chosen.logical_id] = [
                f"source_target:{source}",
                f"difficulty:{tier}",
                *[f"barrier:{label}" for label in chosen.barrier_opportunities],
            ]

        for tier, required in sorted(tier_targets.items()):
            if tier_counts[tier] < required:
                shortfalls.append(
                    {
                        "source_family": source,
                        "quota": f"difficulty:{tier}",
                        "required": required,
                        "observed": tier_counts[tier],
                    }
                )
        for name, required_value in sorted(minimums.items()):
            required = min(int(required_value), target)
            if feature_counts[name] < required:
                shortfalls.append(
                    {
                        "source_family": source,
                        "quota": name,
                        "required": required,
                        "observed": feature_counts[name],
                    }
                )
        for database_id, observed in sorted(database_counts.items()):
            if observed > database_cap:
                shortfalls.append(
                    {
                        "source_family": source,
                        "quota": "database_max_fraction",
                        "database_id": database_id,
                        "required_max": database_cap,
                        "observed": observed,
                    }
                )

    memberships = [
        CubeMembership(
            logical_id=candidate.logical_id,
            source_family=candidate.source_family,
            database_id=candidate.database_id,
            selected=candidate.logical_id in selected_ids,
            selection_rank=ranks.get(candidate.logical_id),
            selection_reasons=reasons.get(candidate.logical_id, []),
        )
        for candidate in candidates
    ]
    return memberships, shortfalls


def _quote_identifier(value: str) -> str:
    return '"' + value.replace('"', '""') + '"'


def _case_name(names: set[str], wanted: str) -> str | None:
    if wanted in names:
        return wanted
    matches = [name for name in names if name.casefold() == wanted.casefold()]
    return matches[0] if len(matches) == 1 else None


def _materialize_database(
    source: Path,
    target: Path,
    replacements: dict[str, Any],
    *,
    schema_language: str,
    value_language: str,
    reuse_existing: bool,
) -> list[str]:
    if reuse_existing and target.is_file() and not Path(f"{target}-journal").exists():
        return []
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
    errors: list[str] = []
    with sqlite3.connect(target) as connection:
        connection.execute("PRAGMA foreign_keys=OFF")
        try:
            connection.execute("PRAGMA ignore_check_constraints=ON")
        except sqlite3.Error:
            pass
        table_rows = connection.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        ).fetchall()
        tables = {str(row[0]) for row in table_rows if not str(row[0]).startswith("sqlite_")}

        if value_language == "zh":
            for table, column, source_value, target_value in replacements.get("values", []):
                actual_table = _case_name(tables, str(table))
                if actual_table is None:
                    errors.append(f"missing_table:{table}")
                    continue
                columns = {
                    str(row[1])
                    for row in connection.execute(
                        f"PRAGMA table_info({_quote_identifier(actual_table)})"
                    ).fetchall()
                }
                actual_column = _case_name(columns, str(column))
                if actual_column is None:
                    errors.append(f"missing_column:{table}.{column}")
                    continue
                try:
                    connection.execute(
                        f"UPDATE {_quote_identifier(actual_table)} "
                        f"SET {_quote_identifier(actual_column)}=? "
                        f"WHERE {_quote_identifier(actual_column)}=?",
                        (target_value, source_value),
                    )
                except sqlite3.Error as exc:
                    errors.append(f"value_update:{table}.{column}:{exc}")

        if schema_language == "zh":
            duplicate_targets = Counter(
                (str(table).casefold(), str(target).casefold())
                for table, _, target in replacements.get("columns", [])
            )
            for table, source_column, target_column in replacements.get("columns", []):
                actual_table = _case_name(tables, str(table))
                if actual_table is None or source_column == target_column:
                    continue
                if duplicate_targets[(str(table).casefold(), str(target_column).casefold())] > 1:
                    errors.append(f"duplicate_column_target:{table}.{target_column}")
                    continue
                columns = {
                    str(row[1])
                    for row in connection.execute(
                        f"PRAGMA table_info({_quote_identifier(actual_table)})"
                    ).fetchall()
                }
                actual_column = _case_name(columns, str(source_column))
                if actual_column is None:
                    errors.append(f"missing_column:{table}.{source_column}")
                    continue
                try:
                    connection.execute(
                        f"ALTER TABLE {_quote_identifier(actual_table)} "
                        f"RENAME COLUMN {_quote_identifier(actual_column)} "
                        f"TO {_quote_identifier(str(target_column))}"
                    )
                except sqlite3.Error as exc:
                    errors.append(f"column_rename:{table}.{source_column}:{exc}")
            for source_table, target_table in replacements.get("tables", []):
                actual_table = _case_name(tables, str(source_table))
                if actual_table is None or source_table == target_table:
                    continue
                try:
                    connection.execute(
                        f"ALTER TABLE {_quote_identifier(actual_table)} "
                        f"RENAME TO {_quote_identifier(str(target_table))}"
                    )
                    tables.remove(actual_table)
                    tables.add(str(target_table))
                except sqlite3.Error as exc:
                    errors.append(f"table_rename:{source_table}:{exc}")
        connection.commit()
    return errors


def _canonical_rows(
    rows: list[tuple[Any, ...]],
    ordered: bool,
    value_normalization: dict[str, str],
) -> list[tuple[str, ...]]:
    normalized = [
        tuple(
            repr(value_normalization.get(value, value))
            if isinstance(value, str)
            else repr(value)
            for value in row
        )
        for row in rows
    ]
    return normalized if ordered else sorted(normalized)


def _execute(
    database: Path,
    sql: str,
    ordered: bool,
    value_normalization: dict[str, str],
    timeout_seconds: float,
) -> list[tuple[str, ...]]:
    started = time.monotonic()
    with sqlite3.connect(database) as connection:
        def decode_text(value: bytes) -> str:
            try:
                return value.decode("utf-8")
            except UnicodeDecodeError:
                return value.decode("latin-1")

        connection.text_factory = decode_text
        connection.set_progress_handler(
            lambda: int(time.monotonic() - started > timeout_seconds),
            10_000,
        )
        rows = connection.execute(sql).fetchall()
    return _canonical_rows(rows, ordered, value_normalization)


def _question_donor(q_language: str, v_language: str) -> str:
    return f"Q_{q_language}--S_{v_language}--V_{v_language}"


def _full_configuration(q_language: str, database_language: str) -> str:
    return f"Q_{q_language}--S_{database_language}--V_{database_language}"


def build_mol_cube(options: CubeBuildOptions) -> CubeReleaseManifest:
    repo_root = options.repo_root.resolve()
    full_release_dir = _resolve(repo_root, options.full_release_dir)
    full_statistics_dir = _resolve(repo_root, options.full_statistics_dir)
    sampler_config_path = _resolve(repo_root, options.sampler_config)
    output_dir = _resolve(repo_root, options.output_dir)
    if output_dir.exists():
        if options.resume:
            pass
        elif not options.overwrite:
            raise FileExistsError(f"{output_dir} exists; pass overwrite=True")
        else:
            shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=options.resume)

    full_manifest_path = full_release_dir / "release_manifest.json"
    statistics_manifest_path = full_statistics_dir / "report_manifest.json"
    full_manifest_hash = sha256_file(full_manifest_path)
    statistics_manifest_hash = sha256_file(statistics_manifest_path)
    full_manifest = ReleaseManifest.model_validate(load_json(full_manifest_path))
    statistics_manifest = FullStatisticsManifest.model_validate(
        load_json(statistics_manifest_path)
    )
    if full_manifest.status != "frozen" and not options.allow_draft:
        raise ValueError("draft Full release requires allow_draft=True")
    if statistics_manifest.release_manifest_hash != full_manifest_hash:
        raise ValueError("Full statistics are stale relative to the Full release manifest")
    if statistics_manifest.logical_instances != full_manifest.logical_instances:
        raise ValueError("Full statistics logical count does not match the Full release")

    sampler_config = _load_yaml(sampler_config_path)
    profiles = load_jsonl(
        full_statistics_dir / "logical_profiles.jsonl", FullLogicalProfile
    )
    candidates = build_candidate_profiles(profiles)
    candidates_by_id = {candidate.logical_id: candidate for candidate in candidates}
    memberships, quota_shortfalls = sample_cube_membership(candidates, sampler_config)
    selected_ids = {row.logical_id for row in memberships if row.selected}
    logical_instances = {
        row.logical_id: row
        for row in load_jsonl(
            full_release_dir / "logical_instances.jsonl", LogicalInstance
        )
        if row.logical_id in selected_ids
    }
    full_realizations = load_jsonl(
        full_release_dir / "realizations.jsonl", Realization
    )
    source_records_path = full_release_dir / "source_records.jsonl"
    native_languages = (
        {
            source.source_family: source.native_language
            for source in load_jsonl(source_records_path, SourceRecord)
        }
        if source_records_path.is_file()
        else {row.source_family: "en" for row in full_realizations}
    )
    by_logical = defaultdict(dict)
    for realization in full_realizations:
        if realization.logical_id in selected_ids:
            by_logical[realization.logical_id][realization.configuration] = realization

    replacement_cache: dict[str, dict[str, Any]] = {}
    tables_metadata_cache: dict[str, list[dict[str, Any]]] = {}
    schema_replacement_cache: dict[
        tuple[str, str, str], dict[str, list[list[Any]]]
    ] = {}
    database_cache: dict[tuple[str, str, str], tuple[Path, str, list[str]]] = {}
    tables_cache: dict[tuple[str, str, str], str] = {}
    realizations: list[CubeRealization] = []
    failures: list[dict[str, Any]] = []
    audit_counts: Counter[str] = Counter()

    for logical_id in sorted(selected_ids):
        source_rows = by_logical.get(logical_id, {})
        if set(source_rows) != set(full_manifest.configurations):
            failures.append({"logical_id": logical_id, "error": "missing_full_cells"})
            continue
        en_base = source_rows["Q_en--S_en--V_en"]
        replacement_path = en_base.replacement_map
        replacements: dict[str, Any] = {"tables": [], "columns": [], "values": []}
        if replacement_path:
            if replacement_path not in replacement_cache:
                replacement_cache[replacement_path] = load_json(
                    _resolve(repo_root, replacement_path)
                )
            replacements = _english_to_chinese_replacements(
                replacement_cache[replacement_path].get(
                    en_base.database_id, replacements
                ),
                native_languages[en_base.source_family],
            )
        if en_base.source_family == "bull" and (
            not replacements.get("tables") or not replacements.get("columns")
        ):
            chinese_base = source_rows["Q_en--S_zh--V_zh"]
            schema_key = (
                en_base.tables_path,
                chinese_base.tables_path,
                en_base.database_id,
            )
            if schema_key not in schema_replacement_cache:
                for tables_path in schema_key[:2]:
                    if tables_path not in tables_metadata_cache:
                        tables_metadata_cache[tables_path] = load_json(
                            _resolve(repo_root, tables_path)
                        )
                schema_replacement_cache[schema_key] = (
                    _schema_replacements_from_metadata(
                        tables_metadata_cache[en_base.tables_path],
                        tables_metadata_cache[chinese_base.tables_path],
                        en_base.database_id,
                    )
                )
            derived_schema = schema_replacement_cache[schema_key]
            replacements = {
                **replacements,
                "tables": replacements.get("tables") or derived_schema["tables"],
                "columns": replacements.get("columns") or derived_schema["columns"],
            }

        logical_rows: list[CubeRealization] = []
        logical_failed = False
        for configuration in CUBE_CONFIGURATIONS:
            q_language = configuration[2:4]
            s_language = configuration[8:10]
            v_language = configuration[14:16]
            coupled = s_language == v_language
            schema_donor = source_rows[_full_configuration(q_language, s_language)]
            question_donor = source_rows[_question_donor(q_language, v_language)]
            if coupled:
                if schema_donor.database_path is None:
                    database_path = output_dir / "missing.sqlite"
                    database_errors = ["missing_coupled_database"]
                else:
                    database_path = _resolve(repo_root, schema_donor.database_path)
                    database_errors = []
                database_hash = schema_donor.input_hashes.get("database", "")
                if not database_hash and database_path.is_file():
                    database_hash = sha256_file(database_path)
                gold_sql = schema_donor.gold_sql
                construction = "reuse-full"
                upstream_ids = [schema_donor.realization_id]
            else:
                cache_key = (en_base.source_family, en_base.database_id, configuration[5:])
                if cache_key not in database_cache:
                    if en_base.database_path is None:
                        database_errors = ["missing_english_database"]
                        database_path = output_dir / "missing.sqlite"
                    else:
                        database_path = (
                            output_dir
                            / "databases"
                            / f"S_{s_language}--V_{v_language}"
                            / en_base.source_family
                            / en_base.database_id
                            / f"{en_base.database_id}.sqlite"
                        )
                        database_errors = _materialize_database(
                            _resolve(repo_root, en_base.database_path),
                            database_path,
                            replacements,
                            schema_language=s_language,
                            value_language=v_language,
                            reuse_existing=options.resume
                            and native_languages[en_base.source_family] == "en",
                        )
                    database_hash = (
                        sha256_file(database_path) if database_path.is_file() else ""
                    )
                    database_cache[cache_key] = (
                        database_path,
                        database_hash,
                        database_errors,
                    )
                database_path, database_hash, database_errors = database_cache[cache_key]
                rewrite = rewrite_sql_components(
                    en_base.gold_sql,
                    replacements,
                    rewrite_schema=s_language == "zh",
                    rewrite_values=False,
                )
                if rewrite.status == "pass" and rewrite.sql and v_language == "zh":
                    transplanted = transplant_sql_values(
                        rewrite.sql,
                        source_rows["Q_en--S_zh--V_zh"].gold_sql,
                        en_base.gold_sql,
                    )
                    rewrite = (
                        transplanted
                        if transplanted.status == "pass"
                        else rewrite_sql_components(
                            en_base.gold_sql,
                            replacements,
                            rewrite_schema=s_language == "zh",
                            rewrite_values=True,
                        )
                    )
                if rewrite.status != "pass" or rewrite.sql is None:
                    database_errors = [
                        *database_errors,
                        f"sql_rewrite:{rewrite.error_code}",
                    ]
                    gold_sql = en_base.gold_sql
                else:
                    gold_sql = rewrite.sql
                construction = "mixed-value-materialization"
                upstream_ids = [
                    en_base.realization_id,
                    schema_donor.realization_id,
                    question_donor.realization_id,
                ]
            if database_errors:
                failures.append(
                    {
                        "logical_id": logical_id,
                        "configuration": configuration,
                        "errors": sorted(set(database_errors)),
                    }
                )
                logical_failed = True
                break

            table_key = (
                schema_donor.source_family,
                schema_donor.tables_path,
                s_language,
            )
            if table_key not in tables_cache:
                target_tables = (
                    output_dir
                    / "metadata"
                    / schema_donor.source_family
                    / f"S_{s_language}"
                    / Path(schema_donor.tables_path).name
                )
                target_tables.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(_resolve(repo_root, schema_donor.tables_path), target_tables)
                tables_cache[table_key] = _relative(repo_root, target_tables)

            logical_rows.append(
                CubeRealization(
                    realization_id=stable_id("cube-realization", logical_id, configuration),
                    logical_id=logical_id,
                    source_family=en_base.source_family,
                    source_sample_key=en_base.source_sample_key,
                    configuration=configuration,
                    question_language=q_language,
                    schema_language=s_language,
                    value_language=v_language,
                    database_id=en_base.database_id,
                    split=en_base.split,
                    question=question_donor.question,
                    gold_sql=gold_sql,
                    tables_path=tables_cache[table_key],
                    database_path=_relative(repo_root, database_path),
                    database_hash=database_hash,
                    construction=construction,
                    treatment_presence={
                        "q": q_language == "zh"
                        and bool(
                            candidates_by_id[logical_id].treatment_support.get(
                                "q_treatment_present"
                            )
                        ),
                        "s": s_language == "zh"
                        and bool(
                            candidates_by_id[logical_id].treatment_support.get(
                                "s_treatment_present"
                            )
                        ),
                        "v": v_language == "zh"
                        and bool(
                            candidates_by_id[logical_id].treatment_support.get(
                                "v_treatment_present"
                            )
                        ),
                    },
                    upstream_realization_ids=sorted(set(upstream_ids)),
                    replacement_map=replacement_path,
                    input_hashes={
                        "full_release_manifest": full_manifest_hash,
                        "full_statistics_manifest": statistics_manifest_hash,
                        "database": database_hash,
                    },
                )
            )

        if logical_failed:
            continue
        if options.execute_equivalence:
            ordered = logical_instances[logical_id].answer_semantics == "ordered"
            value_normalization = {
                str(target): str(source)
                for _, _, source, target in replacements.get("values", [])
            }
            try:
                unique_queries = {
                    (row.database_path, row.gold_sql): row for row in logical_rows
                }
                results = [
                    _execute(
                        _resolve(repo_root, row.database_path),
                        row.gold_sql,
                        ordered,
                        value_normalization,
                        options.execution_timeout_seconds,
                    )
                    for row in unique_queries.values()
                ]
                if any(result != results[0] for result in results[1:]):
                    failures.append(
                        {"logical_id": logical_id, "error": "execution_mismatch"}
                    )
                    audit_counts["fail"] += 1
                    continue
                audit_counts["pass"] += 1
            except sqlite3.Error as exc:
                failures.append(
                    {
                        "logical_id": logical_id,
                        "error": "execution_error",
                        "details": str(exc),
                    }
                )
                audit_counts["fail"] += 1
                continue
        else:
            audit_counts["not_run"] += 1
        realizations.extend(logical_rows)

    retained_ids = {row.logical_id for row in realizations}
    for membership in memberships:
        if membership.selected and membership.logical_id not in retained_ids:
            membership.selected = False
            membership.selection_rank = None
            membership.selection_reasons = [*membership.selection_reasons, "build_failed"]

    write_jsonl(output_dir / "candidate_profiles.jsonl", candidates)
    write_jsonl(output_dir / "membership.jsonl", memberships)
    write_jsonl(output_dir / "realizations.jsonl", realizations)
    write_jsonl(output_dir / "failures.jsonl", failures)
    write_json(output_dir / "quota_shortfalls.json", quota_shortfalls)

    retained_counts = Counter(
        candidate.source_family
        for candidate in candidates
        if candidate.logical_id in retained_ids
    )
    database_counts = Counter(
        candidate.database_id
        for candidate in candidates
        if candidate.logical_id in retained_ids
    )
    tracked = [
        "candidate_profiles.jsonl",
        "membership.jsonl",
        "realizations.jsonl",
        "failures.jsonl",
        "quota_shortfalls.json",
    ]
    file_hashes = {name: sha256_file(output_dir / name) for name in tracked}
    blockers = [*full_manifest.blockers]
    if failures:
        blockers.append(f"cube_build_failures:{len(failures)}")
    if not options.execute_equivalence:
        blockers.append("cube_execution_equivalence:not_run")
    blockers.append("cube_human_annotations:incomplete")
    status = "engineering-draft"
    manifest = CubeReleaseManifest(
        release_id=str(sampler_config["release_id"]),
        status=status,
        non_claim_bearing=status != "frozen",
        upstream_full_release_id=full_manifest.release_id,
        upstream_full_status=full_manifest.status,
        upstream_full_manifest_hash=full_manifest_hash,
        upstream_full_statistics_manifest_hash=statistics_manifest_hash,
        upstream_full_logical_profiles_hash=sha256_file(
            full_statistics_dir / "logical_profiles.jsonl"
        ),
        inherited_blockers=full_manifest.blockers,
        blockers=sorted(set(blockers)),
        source_families=sorted(retained_counts),
        logical_instances=len(retained_ids),
        realizations=len(realizations),
        configurations=list(CUBE_CONFIGURATIONS),
        source_counts=dict(sorted(retained_counts.items())),
        database_counts=dict(sorted(database_counts.items())),
        sampler_config_hash=sha256_json(sampler_config),
        sampler_seed=int(sampler_config["seed"]),
        database_packaging_mode="copy",
        audit_summary={"eight_cell_execution_equivalence": dict(audit_counts)},
        quota_shortfalls=quota_shortfalls,
        file_hashes=file_hashes,
    )
    write_json(output_dir / "release_manifest.json", manifest.model_dump(mode="json"))
    write_json(
        output_dir / "SHA256SUMS.json",
        {
            **file_hashes,
            "release_manifest.json": sha256_file(output_dir / "release_manifest.json"),
        },
    )
    return manifest
