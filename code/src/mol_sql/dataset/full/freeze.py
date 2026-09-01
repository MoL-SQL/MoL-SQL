"""Validate and freeze an existing MoL-Full release directory."""

from __future__ import annotations

from collections import Counter, defaultdict
from pathlib import Path

from mol_sql.contracts.hashing import sha256_file
from mol_sql.contracts.io import load_json, load_jsonl, write_json
from mol_sql.contracts.models import (
    AuditRecord,
    HumanAuditItem,
    LogicalInstance,
    Realization,
    ReleaseManifest,
    SourceRecord,
)
from mol_sql.dataset.audit.human_audit import summarize_human_audit
from mol_sql.dataset.full.bird_export import validate_bird_full


def _repo_root_for(release_dir: Path) -> Path:
    for candidate in (release_dir, *release_dir.parents):
        if (candidate / "code" / "pyproject.toml").is_file():
            return candidate
    raise ValueError(f"cannot locate repository root from {release_dir}")


def freeze_mol_full(release_dir: Path) -> ReleaseManifest:
    release_dir = release_dir.resolve()
    manifest = ReleaseManifest.model_validate(
        load_json(release_dir / "release_manifest.json")
    )
    sources = load_jsonl(release_dir / "source_records.jsonl", SourceRecord)
    logical = load_jsonl(release_dir / "logical_instances.jsonl", LogicalInstance)
    realizations = load_jsonl(release_dir / "realizations.jsonl", Realization)
    audits = load_jsonl(release_dir / "audit_records.jsonl", AuditRecord)
    human = load_jsonl(release_dir / "human_audit_queue.jsonl", HumanAuditItem)

    blockers: list[str] = []
    for source in sources:
        if not source.provenance_complete or source.blockers:
            blockers.extend(source.blockers or [f"{source.source_family}:provenance"])
    for audit in audits:
        if audit.status not in {"pass", "not_applicable"}:
            blockers.append(
                f"{audit.subject_id}:gate:{audit.gate}:{audit.status}"
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

    realized_by_logical: Counter[str] = Counter(
        realization.logical_id for realization in realizations
    )
    logical_ids = {item.logical_id for item in logical}
    if set(realized_by_logical) != logical_ids:
        blockers.append("alignment:logical_id_set_mismatch")
    if any(count != 4 for count in realized_by_logical.values()):
        blockers.append("alignment:not_exactly_four_realizations")
    realization_ids = [item.realization_id for item in realizations]
    if len(realization_ids) != len(set(realization_ids)):
        blockers.append("alignment:duplicate_realization_id")

    if manifest.bird_format_manifest is None:
        blockers.append("bird_format:missing")
    else:
        try:
            validate_bird_full(_repo_root_for(release_dir), release_dir)
        except (FileNotFoundError, ValueError, KeyError) as exc:
            blockers.append(f"bird_format:invalid:{exc}")

    tracked = [
        "source_records.jsonl",
        "logical_instances.jsonl",
        "realizations.jsonl",
        "legacy_id_map.jsonl",
        "audit_records.jsonl",
        "human_audit_queue.jsonl",
        "human_audit_summary.json",
        "audit_summary.json",
        "failures.jsonl",
        "execution_adjudications.jsonl",
    ]
    file_hashes = {name: sha256_file(release_dir / name) for name in tracked}
    for name, expected in manifest.file_hashes.items():
        if name in {"human_audit_queue.jsonl", "human_audit_summary.json"}:
            continue
        actual = file_hashes.get(name)
        if actual != expected:
            blockers.append(f"artifact_hash_mismatch:{name}")

    if blockers:
        raise ValueError(
            "MoL-Full release is not freeze-ready:\n- " + "\n- ".join(sorted(set(blockers)))
        )

    source_counts = Counter(item.source_family for item in logical)
    audit_summary: dict[str, Counter[str]] = defaultdict(Counter)
    for audit in audits:
        audit_summary[audit.gate][audit.status] += 1
    frozen = manifest.model_copy(
        update={
            "status": "frozen",
            "logical_instances": len(logical),
            "realizations": len(realizations),
            "source_counts": dict(sorted(source_counts.items())),
            "file_hashes": file_hashes,
            "audit_summary": {
                gate: dict(sorted(counts.items()))
                for gate, counts in sorted(audit_summary.items())
            },
            "blockers": [],
        }
    )
    write_json(release_dir / "release_manifest.json", frozen.model_dump(mode="json"))
    sums = {
        **file_hashes,
        "release_manifest.json": sha256_file(release_dir / "release_manifest.json"),
    }
    if frozen.bird_format_manifest and frozen.bird_format_manifest_hash:
        sums[frozen.bird_format_manifest] = frozen.bird_format_manifest_hash
    write_json(release_dir / "SHA256SUMS.json", sums)
    return frozen
