"""Rerun automatic gates for an existing MoL-Full draft release."""

from __future__ import annotations

from collections import Counter, defaultdict
from pathlib import Path

from mol_sql.contracts.hashing import sha256_file
from mol_sql.contracts.ids import stable_id
from mol_sql.contracts.io import load_json, load_jsonl, write_json, write_jsonl
from mol_sql.contracts.models import (
    HumanAuditItem,
    ReleaseManifest,
    SourceRecord,
)
from mol_sql.dataset.adapters import adapter_for, load_source_specs
from mol_sql.dataset.audit import (
    audit_source,
    summarize_human_audit,
)
from mol_sql.dataset.full.bird_export import validate_bird_full


def audit_mol_full(
    *,
    repo_root: Path,
    source_config: Path,
    release_dir: Path,
    check_database_integrity: bool,
    execute_equivalence: bool,
    execution_timeout_seconds: float,
) -> ReleaseManifest:
    repo_root = repo_root.resolve()
    source_config = (
        source_config
        if source_config.is_absolute()
        else repo_root / source_config
    )
    release_dir = (
        release_dir if release_dir.is_absolute() else repo_root / release_dir
    )
    old_manifest = ReleaseManifest.model_validate(
        load_json(release_dir / "release_manifest.json")
    )
    specs = load_source_specs(source_config)
    if [spec.source_family for spec in specs] != old_manifest.source_families:
        raise ValueError(
            "source config families/order do not match the release manifest"
        )
    adapted_sources = [
        adapter_for(spec.source_family, repo_root, spec).load() for spec in specs
    ]
    audits = []
    blockers: list[str] = []
    for source in adapted_sources:
        rows, source_blockers = audit_source(
            source,
            check_database_integrity=check_database_integrity,
            execute_equivalence=execute_equivalence,
            execution_timeout_seconds=execution_timeout_seconds,
        )
        audits.extend(rows)
        blockers.extend(source_blockers)
    write_jsonl(release_dir / "audit_records.jsonl", audits)

    summary: dict[str, Counter[str]] = defaultdict(Counter)
    for audit in audits:
        summary[audit.gate][audit.status] += 1
    audit_summary = {
        gate: dict(sorted(counts.items()))
        for gate, counts in sorted(summary.items())
    }
    write_json(release_dir / "audit_summary.json", audit_summary)

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
    write_jsonl(release_dir / "failures.jsonl", failure_rows)

    sources = load_jsonl(release_dir / "source_records.jsonl", SourceRecord)
    for source in sources:
        blockers.extend(source.blockers)
    human = load_jsonl(
        release_dir / "human_audit_queue.jsonl",
        HumanAuditItem,
    )
    human_summary = summarize_human_audit(human)
    write_json(release_dir / "human_audit_summary.json", human_summary)
    if not human_summary["ready"]:
        blockers.append("human_audit:incomplete")
    elif not human_summary["ready_for_freeze"]:
        blockers.append(
            f"human_audit:adjudicated_failures:"
            f"{human_summary['failed_after_adjudication']}"
        )

    if old_manifest.bird_format_manifest is None:
        blockers.append("bird_format:missing")
    else:
        try:
            validate_bird_full(repo_root, release_dir)
        except (FileNotFoundError, ValueError, KeyError) as exc:
            blockers.append(f"bird_format:invalid:{exc}")

    tracked = [
        "source_records.jsonl",
        "logical_instances.jsonl",
        "realizations.jsonl",
        "legacy_id_map.jsonl",
        "audit_records.jsonl",
        "audit_summary.json",
        "failures.jsonl",
        "human_audit_queue.jsonl",
        "human_audit_summary.json",
        "execution_adjudications.jsonl",
    ]
    file_hashes = {name: sha256_file(release_dir / name) for name in tracked}
    manifest = old_manifest.model_copy(
        update={
            "status": "draft",
            "file_hashes": file_hashes,
            "audit_summary": audit_summary,
            "blockers": sorted(set(blockers)),
        }
    )
    write_json(release_dir / "release_manifest.json", manifest.model_dump(mode="json"))
    sums = {
        **file_hashes,
        "release_manifest.json": sha256_file(release_dir / "release_manifest.json"),
    }
    if manifest.bird_format_manifest and manifest.bird_format_manifest_hash:
        sums[manifest.bird_format_manifest] = manifest.bird_format_manifest_hash
    write_json(release_dir / "SHA256SUMS.json", sums)
    return manifest
