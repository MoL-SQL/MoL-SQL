"""Generate reproducible MoL-Cube composition and selection statistics."""

from __future__ import annotations

import csv
import shutil
import subprocess
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from mol_sql.contracts.hashing import sha256_file, sha256_json
from mol_sql.contracts.io import load_json, load_jsonl, write_json
from mol_sql.dataset.cube.models import (
    CUBE_CONFIGURATIONS,
    CubeCandidateProfile,
    CubeMembership,
    CubeRealization,
    CubeReleaseManifest,
)

from .models import CubeStatisticsManifest

CUBE_STATISTICS_CONFIG = {
    "version": "cube-report-v0.1",
    "selection_comparison": "selected-vs-unselected-candidate-universe",
    "completeness_contract": list(CUBE_CONFIGURATIONS),
}


@dataclass(frozen=True)
class CubeStatisticsOptions:
    repo_root: Path
    cube_release_dir: Path
    full_statistics_dir: Path
    output_dir: Path | None = None
    allow_engineering: bool = False
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


def _composition(
    profiles: list[CubeCandidateProfile],
    memberships: list[CubeMembership],
    realizations: list[CubeRealization],
) -> dict[str, Any]:
    selected_ids = {row.logical_id for row in memberships if row.selected}
    selected = [row for row in profiles if row.logical_id in selected_ids]
    databases: dict[str, set[str]] = defaultdict(set)
    tiers: dict[str, Counter[str]] = defaultdict(Counter)
    for row in selected:
        databases[row.source_family].add(row.database_id)
        tiers[row.source_family][str(row.difficulty["composite_tier"])] += 1
    source_counts = Counter(row.source_family for row in selected)
    realization_sources = Counter(row.source_family for row in realizations)
    return {
        "candidate_logical_instances": len(profiles),
        "selected_logical_instances": len(selected),
        "realizations": len(realizations),
        "configurations": dict(sorted(Counter(row.configuration for row in realizations).items())),
        "sources": {
            source: {
                "logical_instances": source_counts[source],
                "realizations": realization_sources[source],
                "databases": len(databases[source]),
                "composite_tiers": dict(sorted(tiers[source].items())),
            }
            for source in sorted(source_counts)
        },
    }


def _completeness(realizations: list[CubeRealization]) -> dict[str, Any]:
    grouped: dict[str, list[CubeRealization]] = defaultdict(list)
    for row in realizations:
        grouped[row.logical_id].append(row)
    expected = set(CUBE_CONFIGURATIONS)
    incomplete = []
    duplicate_cells = []
    for logical_id, rows in sorted(grouped.items()):
        counts = Counter(row.configuration for row in rows)
        missing = sorted(expected - set(counts))
        duplicates = sorted(name for name, count in counts.items() if count != 1)
        if missing:
            incomplete.append({"logical_id": logical_id, "missing": missing})
        if duplicates:
            duplicate_cells.append({"logical_id": logical_id, "configurations": duplicates})
    return {
        "expected_cells_per_logical_instance": 8,
        "logical_instances": len(grouped),
        "complete_logical_instances": len(grouped) - len(incomplete) - len(duplicate_cells),
        "configuration_counts": dict(sorted(Counter(row.configuration for row in realizations).items())),
        "incomplete": incomplete,
        "duplicate_cells": duplicate_cells,
        "contract_satisfied": not incomplete and not duplicate_cells,
    }


def _treatment_and_barriers(profiles: list[CubeCandidateProfile], selected_ids: set[str]) -> dict[str, Any]:
    selected = [row for row in profiles if row.logical_id in selected_ids]
    support_fields = (
        "q_treatment_present",
        "s_treatment_present",
        "v_treatment_present",
    )
    support = Counter()
    controls = Counter()
    barriers = Counter()
    pending = Counter()
    by_source: dict[str, Counter[str]] = defaultdict(Counter)
    for row in selected:
        for field in support_fields:
            if row.treatment_support.get(field):
                support[field] += 1
                by_source[row.source_family][field] += 1
        for field, value in row.controls.items():
            if value is True:
                controls[field] += 1
        barriers.update(row.barrier_opportunities)
        pending.update(row.pending_human_annotations)
    denominator = len(selected)
    return {
        "logical_instances": denominator,
        "treatment_support": {
            field: {
                "count": support[field],
                "fraction": round(support[field] / denominator, 6) if denominator else 0.0,
            }
            for field in support_fields
        },
        "controls": dict(sorted(controls.items())),
        "barrier_opportunities": dict(sorted(barriers.items())),
        "pending_human_annotations": dict(sorted(pending.items())),
        "by_source": {source: dict(sorted(counts.items())) for source, counts in sorted(by_source.items())},
    }


def _difficulty(profiles: list[CubeCandidateProfile], selected_ids: set[str]) -> dict[str, Any]:
    selected = [row for row in profiles if row.logical_id in selected_ids]
    by_source: dict[str, list[CubeCandidateProfile]] = defaultdict(list)
    for row in selected:
        by_source[row.source_family].append(row)
    metrics = ("sql_score", "schema_score", "value_score", "composite_score")

    def values(rows: list[CubeCandidateProfile], metric: str) -> list[float]:
        return [
            float(row.difficulty[metric])
            for row in rows
            if row.difficulty.get(metric) is not None
        ]

    return {
        "overall": {
            "tiers": dict(sorted(Counter(str(row.difficulty["composite_tier"]) for row in selected).items())),
            **{
                metric: _summary(values(selected, metric))
                for metric in metrics
            },
        },
        "by_source": {
            source: {
                "tiers": dict(sorted(Counter(str(row.difficulty["composite_tier"]) for row in rows).items())),
                **{
                    metric: _summary(values(rows, metric))
                    for metric in metrics
                },
            }
            for source, rows in sorted(by_source.items())
        },
    }


def _cohort_summary(rows: list[CubeCandidateProfile]) -> dict[str, Any]:
    count = len(rows)
    support_fields = ("q_treatment_present", "s_treatment_present", "v_treatment_present")
    return {
        "logical_instances": count,
        "sources": dict(sorted(Counter(row.source_family for row in rows).items())),
        "tiers": dict(sorted(Counter(str(row.difficulty["composite_tier"]) for row in rows).items())),
        "composite_score": _summary([float(row.difficulty["composite_score"]) for row in rows]),
        "support_rates": {
            field: round(sum(bool(row.treatment_support.get(field)) for row in rows) / count, 6)
            if count else 0.0
            for field in support_fields
        },
        "barrier_opportunities": dict(sorted(Counter(label for row in rows for label in row.barrier_opportunities).items())),
    }


def _selection_comparison(profiles: list[CubeCandidateProfile], selected_ids: set[str]) -> dict[str, Any]:
    selected = [row for row in profiles if row.logical_id in selected_ids]
    unselected = [row for row in profiles if row.logical_id not in selected_ids]
    return {
        "candidate_universe": _cohort_summary(profiles),
        "selected": _cohort_summary(selected),
        "unselected": _cohort_summary(unselected),
        "selection_fraction": round(len(selected) / len(profiles), 6) if profiles else 0.0,
    }


def _quality(manifest: CubeReleaseManifest, release_dir: Path) -> dict[str, Any]:
    failures_path = release_dir / "failures.jsonl"
    with failures_path.open(encoding="utf-8") as handle:
        failure_rows = sum(1 for line in handle if line.strip())
    return {
        "status": manifest.status,
        "non_claim_bearing": manifest.non_claim_bearing,
        "blockers": manifest.blockers,
        "inherited_blockers": manifest.inherited_blockers,
        "audit_summary": manifest.audit_summary,
        "build_failure_rows": failure_rows,
        "quota_shortfalls": manifest.quota_shortfalls,
    }


def _write_database_csv(path: Path, profiles: list[CubeCandidateProfile], selected_ids: set[str]) -> None:
    counts: Counter[tuple[str, str]] = Counter(
        (row.source_family, row.database_id)
        for row in profiles
        if row.logical_id in selected_ids
    )
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["source_family", "database_id", "logical_instances"])
        for (source, database_id), count in sorted(counts.items()):
            writer.writerow([source, database_id, count])


def generate_cube_statistics(options: CubeStatisticsOptions) -> CubeStatisticsManifest:
    repo_root = options.repo_root.resolve()
    release_dir = _resolve(repo_root, options.cube_release_dir).resolve()
    full_statistics_dir = _resolve(repo_root, options.full_statistics_dir).resolve()
    release_manifest_path = release_dir / "release_manifest.json"
    manifest = CubeReleaseManifest.model_validate(load_json(release_manifest_path))
    provisional = manifest.status != "frozen"
    if provisional and not options.allow_engineering:
        raise ValueError("engineering Cube statistics require allow_engineering=True")
    full_manifest_path = full_statistics_dir / "report_manifest.json"
    if sha256_file(full_manifest_path) != manifest.upstream_full_statistics_manifest_hash:
        raise ValueError("upstream Full statistics manifest hash mismatch")
    output_dir = (
        _resolve(repo_root, options.output_dir).resolve()
        if options.output_dir is not None
        else repo_root / "artifacts" / "paper_stats" / "dataset"
        / ("provisional" if provisional else "frozen") / manifest.release_id
    )
    if output_dir.exists() and not options.overwrite:
        raise FileExistsError(f"{output_dir} already exists; pass overwrite=True")
    temporary_dir = output_dir.with_name(f".{output_dir.name}.tmp")
    if temporary_dir.exists():
        shutil.rmtree(temporary_dir)
    temporary_dir.mkdir(parents=True)
    try:
        profiles = load_jsonl(release_dir / "candidate_profiles.jsonl", CubeCandidateProfile)
        memberships = load_jsonl(release_dir / "membership.jsonl", CubeMembership)
        realizations = load_jsonl(release_dir / "realizations.jsonl", CubeRealization)
        if {row.logical_id for row in profiles} != {row.logical_id for row in memberships}:
            raise ValueError("candidate profiles and membership logical IDs differ")
        selected_ids = {row.logical_id for row in memberships if row.selected}
        if selected_ids != {row.logical_id for row in realizations}:
            raise ValueError("selected membership and realization logical IDs differ")
        outputs = {
            "composition.json": _composition(profiles, memberships, realizations),
            "cube_completeness.json": _completeness(realizations),
            "treatment_barrier_support.json": _treatment_and_barriers(profiles, selected_ids),
            "difficulty.json": _difficulty(profiles, selected_ids),
            "full_cube_comparison.json": _selection_comparison(profiles, selected_ids),
            "quality_funnel.json": _quality(manifest, release_dir),
            "quota_shortfalls.json": manifest.quota_shortfalls,
        }
        for name, value in outputs.items():
            write_json(temporary_dir / name, value)
        _write_database_csv(temporary_dir / "composition_by_database.csv", profiles, selected_ids)
        output_files = [*outputs, "composition_by_database.csv"]
        code_commit, code_dirty = _git_state(repo_root)
        report = CubeStatisticsManifest(
            release_id=manifest.release_id,
            release_status=manifest.status,
            release_manifest_hash=sha256_file(release_manifest_path),
            upstream_full_statistics_manifest_hash=sha256_file(full_manifest_path),
            canonical_artifact_hashes={
                name: manifest.file_hashes[name]
                for name in ("candidate_profiles.jsonl", "membership.jsonl", "realizations.jsonl")
            },
            provisional=provisional,
            non_claim_bearing=manifest.non_claim_bearing,
            blockers=manifest.blockers,
            generated_at_utc=datetime.now(timezone.utc).isoformat(),
            code_commit=code_commit,
            code_dirty=code_dirty,
            config_hash=sha256_json(CUBE_STATISTICS_CONFIG),
            logical_instances=len(selected_ids),
            realizations=len(realizations),
            candidates=len(profiles),
            files={name: sha256_file(temporary_dir / name) for name in output_files},
        )
        write_json(temporary_dir / "report_manifest.json", report.model_dump(mode="json"))
        if output_dir.exists():
            shutil.rmtree(output_dir)
        output_dir.parent.mkdir(parents=True, exist_ok=True)
        temporary_dir.replace(output_dir)
        return report
    except Exception:
        if temporary_dir.exists():
            shutil.rmtree(temporary_dir)
        raise
