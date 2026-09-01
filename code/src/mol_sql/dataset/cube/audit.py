"""Post-build execution audit for a materialized MoL-Cube release."""

from __future__ import annotations

import json
import sqlite3
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from mol_sql.contracts.hashing import sha256_file
from mol_sql.contracts.io import load_json, load_jsonl, write_json, write_jsonl
from mol_sql.contracts.models import LogicalInstance, SourceRecord
from mol_sql.dataset.adapters import execution_sql_for

from .build import _english_to_chinese_replacements, _execute, _resolve
from .models import CubeRealization, CubeReleaseManifest


@dataclass(frozen=True)
class CubeAuditOptions:
    repo_root: Path
    cube_release_dir: Path
    full_release_dir: Path
    output_dir: Path | None = None
    timeout_seconds: float = 5.0
    workers: int = 4
    logical_ids: set[str] | None = None


def _audit_one(
    repo_root: Path,
    rows: list[CubeRealization],
    answer_semantics: str,
    replacements: dict[str, Any],
    timeout_seconds: float,
) -> dict[str, Any]:
    logical_id = rows[0].logical_id
    normalization = {
        str(target): str(source)
        for _, _, source, target in replacements.get("values", [])
    }
    unique_queries = {(row.database_path, row.gold_sql): row for row in rows}
    try:
        results = [
            _execute(
                _resolve(repo_root, row.database_path),
                execution_sql_for(row.source_family, row.gold_sql),
                answer_semantics == "ordered",
                normalization,
                timeout_seconds,
            )
            for row in unique_queries.values()
        ]
        status = "pass" if all(result == results[0] for result in results[1:]) else "mismatch"
        return {
            "logical_id": logical_id,
            "source_family": rows[0].source_family,
            "database_id": rows[0].database_id,
            "status": status,
            "unique_queries": len(unique_queries),
        }
    except sqlite3.Error as exc:
        return {
            "logical_id": logical_id,
            "source_family": rows[0].source_family,
            "database_id": rows[0].database_id,
            "status": "timeout" if str(exc) == "interrupted" else "error",
            "details": str(exc),
            "unique_queries": len(unique_queries),
        }


def audit_mol_cube(options: CubeAuditOptions) -> dict[str, Any]:
    repo_root = options.repo_root.resolve()
    cube_release_dir = _resolve(repo_root, options.cube_release_dir)
    full_release_dir = _resolve(repo_root, options.full_release_dir)
    output_dir = options.output_dir or cube_release_dir / "audits"
    output_dir = _resolve(repo_root, output_dir)

    grouped: dict[str, list[CubeRealization]] = defaultdict(list)
    for row in load_jsonl(cube_release_dir / "realizations.jsonl", CubeRealization):
        if options.logical_ids is None or row.logical_id in options.logical_ids:
            grouped[row.logical_id].append(row)
    incomplete = [logical_id for logical_id, rows in grouped.items() if len(rows) != 8]
    if incomplete:
        raise ValueError(f"audit input contains incomplete eight-cell groups: {incomplete[:5]}")

    semantics = {
        row.logical_id: row.answer_semantics
        for row in load_jsonl(
            full_release_dir / "logical_instances.jsonl", LogicalInstance
        )
    }
    native_languages = {
        row.source_family: row.native_language
        for row in load_jsonl(full_release_dir / "source_records.jsonl", SourceRecord)
    }
    replacement_files = {
        path: load_json(_resolve(repo_root, path))
        for path in {
            rows[0].replacement_map
            for rows in grouped.values()
            if rows[0].replacement_map
        }
    }

    def task(rows: list[CubeRealization]) -> dict[str, Any]:
        first = rows[0]
        replacements: dict[str, Any] = {"tables": [], "columns": [], "values": []}
        if first.replacement_map:
            replacements = _english_to_chinese_replacements(
                replacement_files[first.replacement_map].get(
                    first.database_id, replacements
                ),
                native_languages[first.source_family],
            )
        return _audit_one(
            repo_root,
            rows,
            semantics[first.logical_id],
            replacements,
            options.timeout_seconds,
        )

    ordered_groups = [grouped[key] for key in sorted(grouped)]
    with ThreadPoolExecutor(max_workers=options.workers) as executor:
        records = list(executor.map(task, ordered_groups))
    counts = Counter(record["status"] for record in records)
    summary = {
        "audited_logical_instances": len(records),
        "timeout_seconds": options.timeout_seconds,
        "workers": options.workers,
        "status_counts": dict(sorted(counts.items())),
    }
    write_jsonl(output_dir / "execution_audit.jsonl", records)
    write_json(output_dir / "execution_audit_summary.json", summary)
    if options.logical_ids is None:
        manifest_path = cube_release_dir / "release_manifest.json"
        manifest = CubeReleaseManifest.model_validate(load_json(manifest_path))
        blockers = [
            blocker
            for blocker in manifest.blockers
            if not blocker.startswith("cube_execution_equivalence:")
        ]
        for status in ("mismatch", "timeout", "error"):
            count = counts.get(status, 0)
            if count:
                blockers.append(f"cube_execution_equivalence:{status}:{count}")
        audit_summary = dict(manifest.audit_summary)
        audit_summary["eight_cell_execution_equivalence"] = dict(sorted(counts.items()))
        file_hashes = dict(manifest.file_hashes)
        try:
            audit_prefix = output_dir.relative_to(cube_release_dir).as_posix()
        except ValueError:
            audit_prefix = None
        if audit_prefix is not None:
            for name in ("execution_audit.jsonl", "execution_audit_summary.json"):
                relative = f"{audit_prefix}/{name}"
                file_hashes[relative] = sha256_file(output_dir / name)
        manifest = manifest.model_copy(
            update={
                "blockers": sorted(set(blockers)),
                "audit_summary": audit_summary,
                "file_hashes": file_hashes,
            }
        )
        write_json(manifest_path, manifest.model_dump(mode="json"))
        sums_path = cube_release_dir / "SHA256SUMS.json"
        sums = load_json(sums_path)
        sums.update(file_hashes)
        sums["release_manifest.json"] = sha256_file(manifest_path)
        write_json(sums_path, sums)
    return summary


def load_logical_ids(path: Path) -> set[str]:
    logical_ids = set()
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            value = json.loads(line)
            logical_ids.add(str(value["logical_id"]))
    return logical_ids
