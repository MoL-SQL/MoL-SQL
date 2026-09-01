"""Build a deterministic reference-based MoL-Full release from legacy seeds."""

from __future__ import annotations

import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path

import sqlglot

from mol_sql.contracts.hashing import sha256_file, sha256_json
from mol_sql.contracts.ids import stable_id
from mol_sql.contracts.io import write_json, write_jsonl
from mol_sql.contracts.models import (
    LogicalInstance,
    Realization,
    ReleaseManifest,
    SourceRecord,
)
from mol_sql.dataset.adapters import adapter_for, load_source_specs
from mol_sql.dataset.adapters.base import AdaptedSource, FULL_CONFIGURATIONS
from mol_sql.dataset.audit import (
    audit_source,
    build_human_audit_queue,
    summarize_human_audit,
)


@dataclass(frozen=True)
class BuildOptions:
    repo_root: Path
    source_config: Path
    output_dir: Path
    release_id: str
    check_database_integrity: bool = True
    execute_equivalence: bool = False
    execution_timeout_seconds: float = 30.0
    human_audit_per_source: int = 20
    requested_status: str = "draft"
    source_families: tuple[str, ...] | None = None


def _relative(repo_root: Path, path: Path) -> str:
    absolute = path.absolute()
    try:
        return absolute.relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        return path.resolve().as_posix()


def _answer_semantics(sql: str) -> str:
    try:
        tree = sqlglot.parse_one(sql, read="sqlite")
        return "ordered" if tree.args.get("order") is not None else "multiset"
    except Exception:
        return "ordered" if re.search(r"\border\s+by\b", sql, re.I) else "multiset"


def _phenomena(sql: str) -> list[str]:
    lowered = sql.lower()
    labels = []
    for label, pattern in (
        ("join", r"\bjoin\b"),
        ("nested", r"\(\s*select\b"),
        ("aggregation", r"\b(count|sum|avg|min|max)\s*\("),
        ("group_by", r"\bgroup\s+by\b"),
        ("order_by", r"\border\s+by\b"),
        ("set_operation", r"\b(union|intersect|except)\b"),
        ("literal", r"('[^']*'|\"[^\"]*\")"),
    ):
        if re.search(pattern, lowered):
            labels.append(label)
    return labels


def _provenance_blockers(adapted: AdaptedSource) -> list[str]:
    spec = adapted.spec
    missing = []
    for name in (
        "upstream_version",
        "source_url",
        "snapshot_date",
        "license_spdx",
        "license_evidence_url",
    ):
        if not getattr(spec, name):
            missing.append(f"{spec.source_family}:missing_provenance:{name}")
    if spec.replacement_map and not (adapted.input_hashes.get("replacement_map")):
        missing.append(f"{spec.source_family}:missing_replacement_map")
    if spec.fixed_points and not (adapted.input_hashes.get("fixed_points")):
        missing.append(f"{spec.source_family}:missing_fixed_points")
    for artifact in (
        "replacement_proposals",
        "execution_repairs",
        "execution_adjudications",
    ):
        if getattr(spec, artifact) and not adapted.input_hashes.get(artifact):
            missing.append(f"{spec.source_family}:missing_{artifact}")
    if spec.redistribution_policy == "unresolved":
        missing.append(f"{spec.source_family}:redistribution_unresolved")
    return missing


def _source_record(adapted: AdaptedSource, repo_root: Path) -> SourceRecord:
    blockers = _provenance_blockers(adapted)
    return SourceRecord(
        source_family=adapted.spec.source_family,
        release_role=adapted.spec.release_role,
        upstream_version=adapted.spec.upstream_version,
        source_url=adapted.spec.source_url,
        snapshot_date=adapted.spec.snapshot_date,
        license_spdx=adapted.spec.license_spdx,
        license_evidence_url=adapted.spec.license_evidence_url,
        redistribution_policy=adapted.spec.redistribution_policy,
        license_notes=adapted.spec.license_notes,
        native_language=adapted.spec.native_language,
        split=adapted.spec.split,
        seed_root=_relative(repo_root, repo_root / adapted.spec.root),
        replacement_proposals=adapted.spec.replacement_proposals,
        replacement_map=adapted.spec.replacement_map,
        fixed_points=adapted.spec.fixed_points,
        execution_repairs=adapted.spec.execution_repairs,
        execution_adjudications=adapted.spec.execution_adjudications,
        input_hashes=adapted.input_hashes,
        provenance_complete=not blockers,
        blockers=blockers,
    )


def _records_for_source(
    adapted: AdaptedSource,
    repo_root: Path,
) -> tuple[list[LogicalInstance], list[Realization], list[dict]]:
    logical_instances: list[LogicalInstance] = []
    realizations: list[Realization] = []
    legacy_map: list[dict] = []
    spec = adapted.spec
    canonical_configuration = FULL_CONFIGURATIONS[0]
    for sample in adapted.samples:
        canonical_row = sample.rows[canonical_configuration]
        canonical_question = _question(canonical_row)
        canonical_sql = _sql(adapted, canonical_row)
        logical_id = stable_id(
            "logical",
            spec.source_family,
            spec.upstream_version or "unfrozen",
            spec.split,
            sample.database_id,
            sample.source_sample_key,
        )
        logical_hashes = {
            "canonical_dev": adapted.input_hashes[
                f"{canonical_configuration}:dev.json"
            ]
        }
        for artifact in (
            "replacement_proposals",
            "replacement_map",
            "fixed_points",
            "execution_repairs",
            "execution_adjudications",
        ):
            if artifact in adapted.input_hashes:
                logical_hashes[artifact] = adapted.input_hashes[artifact]
        logical_instances.append(
            LogicalInstance(
                logical_id=logical_id,
                source_family=spec.source_family,
                source_sample_key=sample.source_sample_key,
                legacy_index=sample.legacy_index,
                database_id=sample.database_id,
                split=spec.split,
                canonical_question=canonical_question,
                canonical_sql=canonical_sql,
                answer_semantics=_answer_semantics(canonical_sql),
                difficulty=sample.difficulty,
                phenomena=_phenomena(canonical_sql),
                provenance_refs=[f"source:{spec.source_family}"],
                input_hashes=logical_hashes,
            )
        )
        legacy_map.append(
            {
                "source_family": spec.source_family,
                "legacy_index": sample.legacy_index,
                "source_sample_key": sample.source_sample_key,
                "logical_id": logical_id,
            }
        )
        for configuration in FULL_CONFIGURATIONS:
            variant = spec.variants[configuration]
            row = sample.rows[configuration]
            database_path = adapted.database_paths[
                (variant.schema_language, sample.database_id)
            ]
            dev_path = adapted.dev_paths[configuration]
            tables_path = adapted.tables_paths[configuration]
            hashes = {
                "dev_json": adapted.input_hashes[f"{configuration}:dev.json"],
                "tables_json": adapted.input_hashes[f"{configuration}:tables.json"],
            }
            if database_path is not None:
                hashes["database"] = adapted.input_hashes[
                    f"database:{_relative(repo_root, database_path)}"
                ]
            if "replacement_map" in adapted.input_hashes:
                hashes["replacement_map"] = adapted.input_hashes["replacement_map"]
            if "replacement_proposals" in adapted.input_hashes:
                hashes["replacement_proposals"] = adapted.input_hashes[
                    "replacement_proposals"
                ]
            if "fixed_points" in adapted.input_hashes:
                hashes["fixed_points"] = adapted.input_hashes["fixed_points"]
            if "execution_repairs" in adapted.input_hashes:
                hashes["execution_repairs"] = adapted.input_hashes[
                    "execution_repairs"
                ]
            if "execution_adjudications" in adapted.input_hashes:
                hashes["execution_adjudications"] = adapted.input_hashes[
                    "execution_adjudications"
                ]
            realizations.append(
                Realization(
                    realization_id=stable_id("realization", logical_id, configuration),
                    logical_id=logical_id,
                    source_family=spec.source_family,
                    source_sample_key=sample.source_sample_key,
                    configuration=configuration,
                    question_language=variant.question_language,
                    schema_language=variant.schema_language,
                    value_language=variant.value_language,
                    database_id=sample.database_id,
                    split=spec.split,
                    question=_question(row),
                    gold_sql=_sql(adapted, row),
                    dataset_path=_relative(repo_root, dev_path),
                    tables_path=_relative(repo_root, tables_path),
                    database_path=(
                        _relative(repo_root, database_path)
                        if database_path is not None
                        else None
                    ),
                    replacement_proposals=spec.replacement_proposals,
                    replacement_map=spec.replacement_map,
                    fixed_points=spec.fixed_points,
                    execution_repairs=spec.execution_repairs,
                    execution_adjudications=spec.execution_adjudications,
                    input_hashes=hashes,
                )
            )
    return logical_instances, realizations, legacy_map


def _audit_summary(records) -> dict[str, dict[str, int]]:
    summary: dict[str, Counter[str]] = defaultdict(Counter)
    for record in records:
        summary[record.gate][record.status] += 1
    return {
        gate: dict(sorted(counts.items()))
        for gate, counts in sorted(summary.items())
    }


def build_mol_full(options: BuildOptions) -> ReleaseManifest:
    repo_root = options.repo_root.resolve()
    source_config = (
        options.source_config
        if options.source_config.is_absolute()
        else repo_root / options.source_config
    )
    output_dir = (
        options.output_dir
        if options.output_dir.is_absolute()
        else repo_root / options.output_dir
    )
    specs = load_source_specs(source_config)
    if options.source_families:
        requested = set(options.source_families)
        specs = [spec for spec in specs if spec.source_family in requested]
        missing = requested - {spec.source_family for spec in specs}
        if missing:
            raise ValueError(f"unknown source families: {sorted(missing)}")
    adapted_sources = [
        adapter_for(spec.source_family, repo_root, spec).load() for spec in specs
    ]

    source_records = [_source_record(source, repo_root) for source in adapted_sources]
    logical_instances: list[LogicalInstance] = []
    realizations: list[Realization] = []
    legacy_map: list[dict] = []
    audits = []
    blockers: list[str] = []
    for source in adapted_sources:
        logical, realized, mapped = _records_for_source(source, repo_root)
        logical_instances.extend(logical)
        realizations.extend(realized)
        legacy_map.extend(mapped)
        source_audits, source_blockers = audit_source(
            source,
            check_database_integrity=options.check_database_integrity,
            execute_equivalence=options.execute_equivalence,
            execution_timeout_seconds=options.execution_timeout_seconds,
        )
        audits.extend(source_audits)
        blockers.extend(source_blockers)
    for source_record in source_records:
        blockers.extend(source_record.blockers)

    human_queue = build_human_audit_queue(
        adapted_sources,
        per_source=options.human_audit_per_source,
    )
    human_summary = summarize_human_audit(human_queue)
    if not human_summary["ready"]:
        blockers.append("human_audit:incomplete")
    elif not human_summary["ready_for_freeze"]:
        blockers.append(
            f"human_audit:adjudicated_failures:"
            f"{human_summary['failed_after_adjudication']}"
        )

    output_dir.mkdir(parents=True, exist_ok=True)
    paths = {
        "source_records.jsonl": source_records,
        "logical_instances.jsonl": logical_instances,
        "realizations.jsonl": realizations,
        "legacy_id_map.jsonl": legacy_map,
        "audit_records.jsonl": audits,
        "human_audit_queue.jsonl": human_queue,
        "execution_adjudications.jsonl": [
            {
                "drop_id": stable_id(
                    "drop",
                    source.spec.source_family,
                    row["source_sample_key"],
                    row["reason_code"],
                ),
                **row,
            }
            for source in adapted_sources
            for row in source.dropped_samples
        ],
    }
    for filename, rows in paths.items():
        write_jsonl(output_dir / filename, rows)
    write_json(output_dir / "human_audit_summary.json", human_summary)
    audit_summary = _audit_summary(audits)
    write_json(output_dir / "audit_summary.json", audit_summary)
    failure_rows = [
        {
            "failure_id": stable_id(
                "failure",
                audit.subject_id,
                audit.gate,
                sample.get("source_sample_key", "aggregate"),
                sample.get("error_code", audit.status),
            ),
            "source_family": audit.subject_id,
            "gate": audit.gate,
            **sample,
        }
        for audit in audits
        for sample in (
            audit.details.get("failure_samples")
            or (
                [
                    {
                        "error_code": ",".join(audit.error_codes) or audit.status,
                        "details": audit.details,
                    }
                ]
                if audit.status in {"fail", "not_run", "warning"}
                else []
            )
        )
    ]
    write_jsonl(output_dir / "failures.jsonl", failure_rows)

    file_hashes = {
        filename: sha256_file(output_dir / filename)
        for filename in sorted(
            [
                *paths,
                "human_audit_summary.json",
                "audit_summary.json",
                "failures.jsonl",
            ]
        )
    }
    source_counts = Counter(item.source_family for item in logical_instances)
    blockers = sorted(set(blockers))
    blockers.append("bird_format:missing")
    blockers = sorted(set(blockers))
    requested_frozen = options.requested_status == "frozen"
    status = "frozen" if requested_frozen and not blockers else "draft"
    manifest = ReleaseManifest(
        release_id=options.release_id,
        release_kind="mol-full",
        status=status,
        source_families=[spec.source_family for spec in specs],
        logical_instances=len(logical_instances),
        realizations=len(realizations),
        configurations=list(FULL_CONFIGURATIONS),
        source_counts=dict(sorted(source_counts.items())),
        file_hashes=file_hashes,
        audit_summary=audit_summary,
        blockers=blockers,
        build_config_hash=sha256_json(
            {
                "source_config_sha256": sha256_file(source_config),
                "release_id": options.release_id,
                "check_database_integrity": options.check_database_integrity,
                "execute_equivalence": options.execute_equivalence,
                "execution_timeout_seconds": options.execution_timeout_seconds,
                "human_audit_per_source": options.human_audit_per_source,
                "source_families": options.source_families,
            }
        ),
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


def _question(row: dict) -> str:
    value = row.get("question")
    if not isinstance(value, str) or not value.strip():
        raise ValueError("empty question")
    return value.strip()


def _sql(adapted: AdaptedSource, row: dict) -> str:
    for field in adapted.spec.sql_fields:
        value = row.get(field)
        if isinstance(value, str) and value.strip():
            return value.strip()
    raise ValueError(f"{adapted.spec.source_family}: missing SQL")
