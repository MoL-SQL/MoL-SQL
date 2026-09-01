"""Generate reproducible MoL-Full profiles and aggregate statistics."""

from __future__ import annotations

import csv
import json
import math
import shutil
import subprocess
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import sqlglot
from sqlglot import exp

from mol_sql.contracts.hashing import sha256_file, sha256_json
from mol_sql.contracts.io import load_json, load_jsonl, write_json, write_jsonl
from mol_sql.contracts.models import (
    LogicalInstance,
    Realization,
    ReleaseManifest,
    SourceRecord,
)

from .models import FullLogicalProfile, FullStatisticsManifest

FULL_CONFIGURATIONS = (
    "Q_en--S_en--V_en",
    "Q_zh--S_en--V_en",
    "Q_en--S_zh--V_zh",
    "Q_zh--S_zh--V_zh",
)
FEATURE_CONFIG = {
    "version": "full-logical-profile-v0.1.1",
    "sql_dialect": "sqlite",
    "double_quoted_value_policy": "quoted-unknown-column",
    "composite_method": "mean-source-internal-dimension-percentiles",
    "composite_weights": {"sql": 1.0, "schema": 1.0, "value": 1.0},
    "source_internal_tiers": {"easy_max_percentile": 1 / 3, "medium_max_percentile": 2 / 3},
}


@dataclass(frozen=True)
class FullStatisticsOptions:
    repo_root: Path
    release_dir: Path
    output_dir: Path | None = None
    allow_draft: bool = False
    overwrite: bool = False


def _resolve(repo_root: Path, path: Path | str) -> Path:
    candidate = Path(path)
    return candidate if candidate.is_absolute() else repo_root / candidate


def _git_state(repo_root: Path) -> tuple[str | None, bool | None]:
    try:
        commit = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=repo_root,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        dirty = bool(
            subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=repo_root,
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()
        )
        return commit, dirty
    except (OSError, subprocess.CalledProcessError):
        return None, None


def _ast_depth(node: exp.Expression) -> int:
    children = [child for child in node.iter_expressions()]
    return 1 + max((_ast_depth(child) for child in children), default=0)


def _sql_features(
    sql: str,
    known_columns: set[str] | None = None,
) -> tuple[dict[str, Any], exp.Expression]:
    tree = sqlglot.parse_one(sql, read="sqlite")
    nodes = list(tree.walk())
    tables = [node.name for node in tree.find_all(exp.Table)]
    known_column_names = {name.casefold() for name in known_columns or set()}
    quoted_values = [
        node
        for node in tree.find_all(exp.Column)
        if isinstance(node.this, exp.Identifier)
        and bool(node.this.args.get("quoted"))
        and node.name.casefold() not in known_column_names
    ]
    quoted_value_ids = {id(node) for node in quoted_values}
    columns = [
        node.name
        for node in tree.find_all(exp.Column)
        if id(node) not in quoted_value_ids
    ]
    string_literals = [
        str(node.this) for node in tree.find_all(exp.Literal) if node.is_string
    ] + [node.name for node in quoted_values]
    numeric_literals = [
        str(node.this) for node in tree.find_all(exp.Literal) if not node.is_string
    ]
    comparisons = sum(
        1
        for node in nodes
        if isinstance(
            node,
            (exp.EQ, exp.NEQ, exp.GT, exp.GTE, exp.LT, exp.LTE, exp.Like, exp.In, exp.Between),
        )
    )
    arithmetic = sum(
        1
        for node in nodes
        if isinstance(node, (exp.Add, exp.Sub, exp.Mul, exp.Div, exp.Mod))
    )
    aggregates = sum(
        1
        for node in nodes
        if isinstance(node, (exp.Count, exp.Sum, exp.Avg, exp.Min, exp.Max))
    )
    set_operations = sum(
        1 for node in nodes if isinstance(node, (exp.Union, exp.Intersect, exp.Except))
    )
    select_count = sum(1 for node in nodes if isinstance(node, exp.Select))
    condition_count = comparisons + sum(
        1 for node in nodes if isinstance(node, (exp.And, exp.Or, exp.Not))
    )
    features = {
        "ast_nodes": len(nodes),
        "ast_depth": _ast_depth(tree),
        "select_count": select_count,
        "nested_query_count": max(0, select_count - 1),
        "table_reference_count": len(tables),
        "unique_table_count": len({name.casefold() for name in tables}),
        "column_reference_count": len(columns),
        "unique_column_count": len({name.casefold() for name in columns}),
        "join_count": sum(1 for node in nodes if isinstance(node, exp.Join)),
        "condition_count": condition_count,
        "comparison_count": comparisons,
        "negation_count": sum(1 for node in nodes if isinstance(node, exp.Not)),
        "aggregation_count": aggregates,
        "group_by": any(isinstance(node, exp.Group) for node in nodes),
        "having": any(isinstance(node, exp.Having) for node in nodes),
        "order_by": any(isinstance(node, exp.Order) for node in nodes),
        "limit": any(isinstance(node, exp.Limit) for node in nodes),
        "set_operation_count": set_operations,
        "arithmetic_count": arithmetic,
        "string_literal_count": len(string_literals),
        "numeric_literal_count": len(numeric_literals),
        "string_literals": string_literals,
        "numeric_literals": numeric_literals,
        "referenced_tables": sorted({name for name in tables}, key=str.casefold),
        "referenced_columns": sorted({name for name in columns}, key=str.casefold),
    }
    features["score"] = round(
        features["join_count"]
        + 2 * features["nested_query_count"]
        + 2 * features["set_operation_count"]
        + features["aggregation_count"]
        + int(features["group_by"])
        + int(features["having"])
        + int(features["order_by"])
        + int(features["limit"])
        + 0.5 * features["condition_count"]
        + 0.5 * features["arithmetic_count"]
        + 0.1 * features["ast_depth"],
        4,
    )
    return features, tree


def _schema_features(
    schema: dict[str, Any],
    sql_features: dict[str, Any],
) -> dict[str, Any]:
    table_names = schema.get("table_names_original") or schema.get("table_names") or []
    columns = schema.get("column_names_original") or schema.get("column_names") or []
    column_names = [str(item[1]) for item in columns if isinstance(item, list) and item[0] != -1]
    referenced_tables = {name.casefold() for name in sql_features["referenced_tables"]}
    referenced_columns = {name.casefold() for name in sql_features["referenced_columns"]}
    matched_tables = {name for name in table_names if str(name).casefold() in referenced_tables}
    matched_columns = {name for name in column_names if str(name).casefold() in referenced_columns}
    table_count = len(table_names)
    column_count = len(column_names)
    referenced_table_count = len(matched_tables)
    referenced_column_count = len(matched_columns)
    features = {
        "table_count": table_count,
        "column_count": column_count,
        "primary_key_count": len(schema.get("primary_keys") or []),
        "foreign_key_count": len(schema.get("foreign_keys") or []),
        "schema_serialization_chars": len(
            json.dumps(schema, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        ),
        "gold_referenced_table_count": referenced_table_count,
        "gold_referenced_column_count": referenced_column_count,
        "distractor_table_count": max(0, table_count - referenced_table_count),
        "distractor_column_count": max(0, column_count - referenced_column_count),
        "gold_table_ratio": round(referenced_table_count / table_count, 6) if table_count else 0.0,
        "gold_column_ratio": round(referenced_column_count / column_count, 6) if column_count else 0.0,
        "requires_join": sql_features["join_count"] > 0,
        "requires_bridge_table": None,
    }
    features["score"] = round(
        math.log1p(table_count)
        + math.log1p(column_count)
        + 0.5 * features["distractor_table_count"]
        + 0.05 * features["distractor_column_count"]
        + sql_features["join_count"],
        4,
    )
    return features


def _known_columns(schema: dict[str, Any], replacements: dict[str, Any]) -> set[str]:
    names = {
        str(item[1])
        for key in ("column_names_original", "column_names")
        for item in schema.get(key, [])
        if isinstance(item, list) and len(item) > 1 and item[0] != -1
    }
    for row in replacements.get("columns", []):
        if len(row) >= 3:
            names.update((str(row[1]), str(row[2])))
    return names


def _load_optional_json(repo_root: Path, path: str | None, cache: dict[Path, Any]) -> Any:
    if path is None:
        return None
    resolved = _resolve(repo_root, path).resolve()
    if resolved not in cache:
        cache[resolved] = load_json(resolved)
    return cache[resolved]


def _replacement_entry(replacements: Any, database_id: str) -> dict[str, Any]:
    if isinstance(replacements, dict):
        entry = replacements.get(database_id)
        if isinstance(entry, dict):
            return entry
    return {"tables": [], "columns": [], "values": []}


def _fixed_point_entry(fixed_points: Any, database_id: str) -> tuple[list[dict], list[dict]]:
    if not isinstance(fixed_points, dict):
        return [], []
    columns = [row for row in fixed_points.get("columns", []) if row.get("database_id") == database_id]
    values = [row for row in fixed_points.get("value_columns", []) if row.get("database_id") == database_id]
    return columns, values


def _treatment_features(
    realizations: dict[str, Realization],
    sql_features: dict[str, Any],
    replacements: dict[str, Any],
    fixed_columns: list[dict],
    fixed_values: list[dict],
    known_columns: set[str],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    table_sources = {str(row[0]).casefold() for row in replacements.get("tables", [])}
    column_sources = {str(row[1]).casefold() for row in replacements.get("columns", [])}
    value_rows = replacements.get("values", [])
    value_terms = {
        str(term)
        for row in value_rows
        for term in row[2:4]
        if len(row) >= 4 and str(row[2]) != str(row[3])
    }
    referenced_tables = [name.casefold() for name in sql_features["referenced_tables"]]
    referenced_columns = [name.casefold() for name in sql_features["referenced_columns"]]
    active_fixed_values = [
        row
        for row in fixed_values
        if str(row.get("column", "")).casefold() in referenced_columns
    ]
    mapped_schema_references = sum(name in table_sources for name in referenced_tables) + sum(
        name in column_sources for name in referenced_columns
    )
    total_schema_references = len(referenced_tables) + len(referenced_columns)
    literals = sql_features["string_literals"]
    mapped_literal_occurrences = sum(literal in value_terms for literal in literals)
    mapped_literal_unique = len({literal for literal in literals if literal in value_terms})
    canonical_question = realizations["Q_en--S_en--V_en"].question
    recurring_entities = {
        literal
        for literal in literals
        if literal in value_terms
        and (canonical_question.casefold().count(literal.casefold()) + literals.count(literal) > 1)
    }
    en_questions = {
        realizations["Q_en--S_en--V_en"].question,
        realizations["Q_en--S_zh--V_zh"].question,
    }
    zh_questions = {
        realizations["Q_zh--S_en--V_en"].question,
        realizations["Q_zh--S_zh--V_zh"].question,
    }
    sql_en = realizations["Q_en--S_en--V_en"].gold_sql
    sql_zh = realizations["Q_en--S_zh--V_zh"].gold_sql
    sql_en_features = sql_features
    sql_zh_features, _ = _sql_features(sql_zh, known_columns)
    en_identifiers = Counter(
        name.casefold()
        for name in (
            sql_en_features["referenced_tables"]
            + sql_en_features["referenced_columns"]
        )
    )
    zh_identifiers = Counter(
        name.casefold()
        for name in (
            sql_zh_features["referenced_tables"]
            + sql_zh_features["referenced_columns"]
        )
    )
    actual_identifier_changes = sum((en_identifiers - zh_identifiers).values())
    en_literals = Counter(sql_en_features["string_literals"])
    zh_literals = Counter(sql_zh_features["string_literals"])
    actual_literal_changes = sum((en_literals - zh_literals).values())
    support = {
        "q_treatment_present": all(
            left != right
            for left, right in (
                (
                    realizations["Q_en--S_en--V_en"].question,
                    realizations["Q_zh--S_en--V_en"].question,
                ),
                (
                    realizations["Q_en--S_zh--V_zh"].question,
                    realizations["Q_zh--S_zh--V_zh"].question,
                ),
            )
        ),
        "q_unique_en_realizations": len(en_questions),
        "q_unique_zh_realizations": len(zh_questions),
        "q_length_chars_en": len(realizations["Q_en--S_en--V_en"].question),
        "q_length_chars_zh": len(realizations["Q_zh--S_en--V_en"].question),
        "s_treatment_present": actual_identifier_changes > 0,
        "s_actual_identifier_change_count": actual_identifier_changes,
        "s_mapped_reference_count": mapped_schema_references,
        "s_reference_count": total_schema_references,
        "s_treatment_intensity": round(mapped_schema_references / total_schema_references, 6)
        if total_schema_references
        else 0.0,
        "v_treatment_present": actual_literal_changes > 0,
        "v_actual_literal_change_count": actual_literal_changes,
        "v_mapped_literal_count": mapped_literal_occurrences,
        "v_mapped_unique_literal_count": mapped_literal_unique,
        "v_treatment_intensity": round(mapped_literal_occurrences / len(literals), 6)
        if literals
        else 0.0,
        "combined_sql_changed": sql_en != sql_zh,
    }
    value = {
        "string_literal_count": len(literals),
        "mapped_literal_count": mapped_literal_occurrences,
        "mapped_unique_literal_count": mapped_literal_unique,
        "replacement_value_entries_in_database": len(value_rows),
        "recurring_entity_count": len(recurring_entities),
        "recurring_entities": sorted(recurring_entities),
        "fixed_value_column_count": len(active_fixed_values),
    }
    value["score"] = round(
        len(literals)
        + mapped_literal_occurrences
        + 2 * len(recurring_entities)
        + len(active_fixed_values),
        4,
    )
    fixed_column_names = {str(row.get("column", "")).casefold() for row in fixed_columns}
    controls = {
        "literal_free": len(literals) == 0,
        "value_bearing": len(literals) > 0,
        "mapped_value_bearing": mapped_literal_occurrences > 0,
        "recurring_entity": bool(recurring_entities),
        "schema_fixed_point": any(name in fixed_column_names for name in referenced_columns),
        "value_fixed_point": bool(active_fixed_values),
        "low_schema_lexical_load": mapped_schema_references <= 1,
    }
    return support, value, controls


def _rank_percentiles(profiles: list[FullLogicalProfile], score_key: str) -> dict[str, float]:
    by_source: dict[str, list[FullLogicalProfile]] = defaultdict(list)
    for profile in profiles:
        by_source[profile.source_family].append(profile)
    result: dict[str, float] = {}
    for source_profiles in by_source.values():
        ordered = sorted(
            source_profiles,
            key=lambda profile: (profile.difficulty[score_key], profile.logical_id),
        )
        denominator = max(1, len(ordered) - 1)
        start = 0
        while start < len(ordered):
            end = start + 1
            score = ordered[start].difficulty[score_key]
            while end < len(ordered) and ordered[end].difficulty[score_key] == score:
                end += 1
            percentile = ((start + end - 1) / 2) / denominator
            for profile in ordered[start:end]:
                result[profile.logical_id] = percentile
            start = end
    return result


def _assign_difficulty(profiles: list[FullLogicalProfile]) -> list[FullLogicalProfile]:
    for profile in profiles:
        profile.difficulty["sql_score"] = profile.sql_features["score"]
        profile.difficulty["schema_score"] = profile.schema_features["score"]
        profile.difficulty["value_score"] = profile.value_features["score"]
    for score_key, percentile_key in (
        ("sql_score", "sql_percentile_in_source"),
        ("schema_score", "schema_percentile_in_source"),
        ("value_score", "value_percentile_in_source"),
    ):
        percentiles = _rank_percentiles(profiles, score_key)
        for profile in profiles:
            profile.difficulty[percentile_key] = round(percentiles[profile.logical_id], 6)
    for profile in profiles:
        profile.difficulty["composite_score"] = round(
            (
                profile.difficulty["sql_percentile_in_source"]
                + profile.difficulty["schema_percentile_in_source"]
                + profile.difficulty["value_percentile_in_source"]
            )
            / 3,
            6,
        )
    composite_percentiles = _rank_percentiles(profiles, "composite_score")
    for profile in profiles:
        profile.difficulty["composite_percentile_in_source"] = round(
            composite_percentiles[profile.logical_id], 6
        )
    for profile in profiles:
        percentile = profile.difficulty["composite_percentile_in_source"]
        profile.difficulty["composite_tier"] = (
            "easy" if percentile <= 1 / 3 else "medium" if percentile <= 2 / 3 else "hard"
        )
    return profiles


def _summary(values: list[float]) -> dict[str, float | int | None]:
    if not values:
        return {"count": 0, "min": None, "max": None, "mean": None, "median": None}
    ordered = sorted(values)
    middle = len(ordered) // 2
    median = (
        ordered[middle]
        if len(ordered) % 2
        else (ordered[middle - 1] + ordered[middle]) / 2
    )
    return {
        "count": len(values),
        "min": min(values),
        "max": max(values),
        "mean": round(sum(values) / len(values), 6),
        "median": round(median, 6),
    }


def _composition(profiles: list[FullLogicalProfile], realizations: list[Realization]) -> dict[str, Any]:
    by_source = Counter(profile.source_family for profile in profiles)
    databases_by_source: dict[str, set[str]] = defaultdict(set)
    source_difficulty: dict[str, Counter[str]] = defaultdict(Counter)
    phenomena: dict[str, Counter[str]] = defaultdict(Counter)
    tiers: dict[str, Counter[str]] = defaultdict(Counter)
    for profile in profiles:
        databases_by_source[profile.source_family].add(profile.database_id)
        source_difficulty[profile.source_family][profile.source_difficulty or "missing"] += 1
        phenomena[profile.source_family].update(profile.phenomena)
        tiers[profile.source_family][profile.difficulty["composite_tier"]] += 1
    return {
        "logical_instances": len(profiles),
        "realizations": len(realizations),
        "configurations": dict(sorted(Counter(row.configuration for row in realizations).items())),
        "sources": {
            source: {
                "logical_instances": by_source[source],
                "realizations": sum(row.source_family == source for row in realizations),
                "databases": len(databases_by_source[source]),
                "source_difficulty": dict(sorted(source_difficulty[source].items())),
                "sql_phenomena": dict(sorted(phenomena[source].items())),
                "composite_tiers": dict(sorted(tiers[source].items())),
            }
            for source in sorted(by_source)
        },
    }


def _difficulty_summary(profiles: list[FullLogicalProfile]) -> dict[str, Any]:
    metrics = ("sql_score", "schema_score", "value_score", "composite_score")
    by_source: dict[str, list[FullLogicalProfile]] = defaultdict(list)
    for profile in profiles:
        by_source[profile.source_family].append(profile)
    return {
        "overall": {
            metric: _summary([float(profile.difficulty[metric]) for profile in profiles])
            for metric in metrics
        },
        "by_source": {
            source: {
                metric: _summary([float(profile.difficulty[metric]) for profile in rows])
                for metric in metrics
            }
            for source, rows in sorted(by_source.items())
        },
    }


def _treatment_summary(profiles: list[FullLogicalProfile]) -> dict[str, Any]:
    fields = (
        "q_treatment_present",
        "s_treatment_present",
        "v_treatment_present",
    )
    controls = (
        "literal_free",
        "value_bearing",
        "mapped_value_bearing",
        "recurring_entity",
        "schema_fixed_point",
        "value_fixed_point",
        "low_schema_lexical_load",
    )
    by_source: dict[str, list[FullLogicalProfile]] = defaultdict(list)
    for profile in profiles:
        by_source[profile.source_family].append(profile)

    def summarize(rows: list[FullLogicalProfile]) -> dict[str, Any]:
        return {
            "samples": len(rows),
            "treatment_presence": {
                field: sum(bool(row.treatment_support[field]) for row in rows)
                for field in fields
            },
            "controls": {
                field: sum(bool(row.controls[field]) for row in rows) for field in controls
            },
            "intensity": {
                "schema": _summary(
                    [float(row.treatment_support["s_treatment_intensity"]) for row in rows]
                ),
                "value": _summary(
                    [float(row.treatment_support["v_treatment_intensity"]) for row in rows]
                ),
            },
        }

    return {
        "overall": summarize(profiles),
        "by_source": {source: summarize(rows) for source, rows in sorted(by_source.items())},
    }


def _quality_summary(
    repo_root: Path,
    release_dir: Path,
    manifest: ReleaseManifest,
) -> dict[str, Any]:
    drops_path = release_dir / "execution_adjudications.jsonl"
    with drops_path.open(encoding="utf-8") as handle:
        drops = [json.loads(line) for line in handle if line.strip()]
    drop_reasons = Counter(row.get("reason_code", "unknown") for row in drops)
    drops_by_source = Counter(row.get("source_family", "unknown") for row in drops)
    human = load_json(release_dir / "human_audit_summary.json")
    bird = None
    if manifest.bird_format_manifest:
        bird_path = release_dir / manifest.bird_format_manifest
        if bird_path.is_file():
            bird = load_json(bird_path).get("totals")
    repair_count = 0
    repair_paths = {
        row.execution_repairs
        for row in load_jsonl(release_dir / "source_records.jsonl", SourceRecord)
        if row.execution_repairs
    }
    for relative in repair_paths:
        repair_file = _resolve(repo_root, relative)
        if repair_file.is_file():
            repair_count += len(load_json(repair_file).get("sql_repairs", []))
    return {
        "eligible_before_execution_adjudication": manifest.logical_instances + len(drops),
        "retained_logical_instances": manifest.logical_instances,
        "dropped_logical_instances": len(drops),
        "drop_reasons": dict(sorted(drop_reasons.items())),
        "drops_by_source": dict(sorted(drops_by_source.items())),
        "versioned_sql_repairs": repair_count,
        "audit_summary": manifest.audit_summary,
        "blockers": manifest.blockers,
        "human_audit": human,
        "bird_format": bird,
    }
def _write_database_csv(path: Path, profiles: list[FullLogicalProfile]) -> None:
    counts = Counter((profile.source_family, profile.database_id) for profile in profiles)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["source_family", "database_id", "logical_instances"])
        for (source, database_id), count in sorted(counts.items()):
            writer.writerow([source, database_id, count])


def _profiles(
    repo_root: Path,
    logical_rows: list[LogicalInstance],
    realization_rows: list[Realization],
) -> list[FullLogicalProfile]:
    realization_groups: dict[str, dict[str, Realization]] = defaultdict(dict)
    for realization in realization_rows:
        realization_groups[realization.logical_id][realization.configuration] = realization
    json_cache: dict[Path, Any] = {}
    schema_cache: dict[Path, dict[str, dict[str, Any]]] = {}
    profiles: list[FullLogicalProfile] = []
    for logical in logical_rows:
        realizations = realization_groups[logical.logical_id]
        if set(realizations) != set(FULL_CONFIGURATIONS):
            raise ValueError(f"{logical.logical_id}: incomplete Full configurations")
        canonical = realizations["Q_en--S_en--V_en"]
        tables_path = _resolve(repo_root, canonical.tables_path).resolve()
        if tables_path not in schema_cache:
            schemas = load_json(tables_path)
            schema_cache[tables_path] = {row["db_id"]: row for row in schemas}
        schema = schema_cache[tables_path].get(logical.database_id)
        if schema is None:
            raise ValueError(f"{tables_path}: missing {logical.database_id}")
        replacement_map = _load_optional_json(
            repo_root, canonical.replacement_map, json_cache
        )
        replacements = _replacement_entry(replacement_map, logical.database_id)
        known_columns = _known_columns(schema, replacements)
        sql_features, _ = _sql_features(logical.canonical_sql, known_columns)
        schema_features = _schema_features(schema, sql_features)
        fixed_points = _load_optional_json(repo_root, canonical.fixed_points, json_cache)
        fixed_columns, fixed_values = _fixed_point_entry(
            fixed_points, logical.database_id
        )
        support, value_features, controls = _treatment_features(
            realizations,
            sql_features,
            replacements,
            fixed_columns,
            fixed_values,
            known_columns,
        )
        profiles.append(
            FullLogicalProfile(
                logical_id=logical.logical_id,
                source_family=logical.source_family,
                database_id=logical.database_id,
                split=logical.split,
                source_sample_key=logical.source_sample_key,
                legacy_index=logical.legacy_index,
                source_difficulty=logical.difficulty,
                answer_semantics=logical.answer_semantics,
                phenomena=logical.phenomena,
                sql_features=sql_features,
                schema_features=schema_features,
                value_features=value_features,
                treatment_support=support,
                controls=controls,
                difficulty={},
            )
        )
    return _assign_difficulty(profiles)


def generate_full_statistics(options: FullStatisticsOptions) -> FullStatisticsManifest:
    repo_root = options.repo_root.resolve()
    release_dir = _resolve(repo_root, options.release_dir).resolve()
    release_manifest_path = release_dir / "release_manifest.json"
    release_manifest = ReleaseManifest.model_validate(load_json(release_manifest_path))
    provisional = release_manifest.status != "frozen"
    if provisional and not options.allow_draft:
        raise ValueError("draft Full statistics require allow_draft=True")
    output_dir = (
        _resolve(repo_root, options.output_dir).resolve()
        if options.output_dir is not None
        else repo_root
        / "artifacts"
        / "paper_stats"
        / "dataset"
        / ("provisional" if provisional else "frozen")
        / release_manifest.release_id
    )
    if output_dir.exists() and not options.overwrite:
        raise FileExistsError(f"{output_dir} already exists; pass overwrite=True")
    temporary_dir = output_dir.with_name(f".{output_dir.name}.tmp")
    if temporary_dir.exists():
        shutil.rmtree(temporary_dir)
    temporary_dir.mkdir(parents=True)
    try:
        logical_rows = load_jsonl(
            release_dir / "logical_instances.jsonl", LogicalInstance
        )
        realization_rows = load_jsonl(
            release_dir / "realizations.jsonl", Realization
        )
        profiles = _profiles(repo_root, logical_rows, realization_rows)
        write_jsonl(temporary_dir / "logical_profiles.jsonl", profiles)
        write_json(
            temporary_dir / "composition.json",
            _composition(profiles, realization_rows),
        )
        write_json(
            temporary_dir / "difficulty.json",
            _difficulty_summary(profiles),
        )
        write_json(
            temporary_dir / "treatment_support.json",
            _treatment_summary(profiles),
        )
        write_json(
            temporary_dir / "quality_funnel.json",
            _quality_summary(repo_root, release_dir, release_manifest),
        )
        _write_database_csv(temporary_dir / "composition_by_database.csv", profiles)
        output_files = [
            "logical_profiles.jsonl",
            "composition.json",
            "difficulty.json",
            "treatment_support.json",
            "quality_funnel.json",
            "composition_by_database.csv",
        ]
        code_commit, code_dirty = _git_state(repo_root)
        statistics_manifest = FullStatisticsManifest(
            release_id=release_manifest.release_id,
            release_status=release_manifest.status,
            release_manifest_hash=sha256_file(release_manifest_path),
            canonical_artifact_hashes={
                name: release_manifest.file_hashes[name]
                for name in (
                    "logical_instances.jsonl",
                    "realizations.jsonl",
                    "source_records.jsonl",
                    "audit_records.jsonl",
                )
            },
            provisional=provisional,
            blockers=release_manifest.blockers,
            generated_at_utc=datetime.now(timezone.utc).isoformat(),
            code_commit=code_commit,
            code_dirty=code_dirty,
            config_hash=sha256_json(FEATURE_CONFIG),
            logical_instances=len(profiles),
            files={
                name: sha256_file(temporary_dir / name) for name in output_files
            },
        )
        write_json(
            temporary_dir / "report_manifest.json",
            statistics_manifest.model_dump(mode="json"),
        )
        if output_dir.exists():
            shutil.rmtree(output_dir)
        output_dir.parent.mkdir(parents=True, exist_ok=True)
        temporary_dir.replace(output_dir)
        return statistics_manifest
    except Exception:
        if temporary_dir.exists():
            shutil.rmtree(temporary_dir)
        raise
