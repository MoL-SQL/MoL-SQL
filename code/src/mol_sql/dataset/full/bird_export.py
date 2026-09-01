"""Export and validate source-separated BIRD-compatible MoL-Full packages."""

from __future__ import annotations

import os
import shutil
import sqlite3
from errno import EXDEV
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

from mol_sql.contracts.hashing import sha256_file
from mol_sql.contracts.io import load_json, load_jsonl, write_json
from mol_sql.contracts.models import (
    LogicalInstance,
    Realization,
    ReleaseManifest,
    SourceRecord,
)

BIRD_FORMAT_VERSION = "mol-full-bird-format-v0.1"
BIRD_SCHEMA_FIELDS = {
    "db_id",
    "table_names",
    "table_names_original",
    "column_names",
    "column_names_original",
    "column_types",
    "primary_keys",
    "foreign_keys",
}
DatabaseMode = Literal["copy", "hardlink", "symlink"]
DistributionMode = Literal["local", "public"]


@dataclass(frozen=True)
class BirdExportOptions:
    repo_root: Path
    release_dir: Path
    output_dir: Path | None = None
    database_mode: DatabaseMode = "hardlink"
    distribution: DistributionMode = "local"
    overwrite: bool = False


class _FileHasher:
    def __init__(self) -> None:
        self._cache: dict[tuple[int, int, int, int], str] = {}

    def hash(self, path: Path) -> str:
        stat = path.stat()
        key = (stat.st_dev, stat.st_ino, stat.st_size, stat.st_mtime_ns)
        if key not in self._cache:
            self._cache[key] = sha256_file(path)
        return self._cache[key]


def _resolve(repo_root: Path, path: str | Path) -> Path:
    candidate = Path(path)
    return candidate if candidate.is_absolute() else repo_root / candidate


def _load_source_row(
    repo_root: Path,
    realization: Realization,
    logical: LogicalInstance,
    cache: dict[Path, list[dict[str, Any]]],
) -> dict[str, Any]:
    dataset_path = _resolve(repo_root, realization.dataset_path).resolve()
    if dataset_path not in cache:
        rows = load_json(dataset_path)
        if not isinstance(rows, list) or not all(isinstance(row, dict) for row in rows):
            raise ValueError(f"{dataset_path}: dev.json must be a list of objects")
        cache[dataset_path] = rows
    rows = cache[dataset_path]
    if logical.legacy_index >= len(rows):
        raise ValueError(
            f"{realization.realization_id}: legacy index {logical.legacy_index} "
            f"is outside {dataset_path}"
        )
    return rows[logical.legacy_index]


def _single_line_sql(realization: Realization) -> str:
    sql = realization.gold_sql.strip()
    if any(character in sql for character in ("\n", "\r", "\t")):
        raise ValueError(
            f"{realization.realization_id}: gold SQL contains a line break or tab"
        )
    return sql


def _distribution_scope(source: SourceRecord) -> str:
    if source.redistribution_policy == "redistributable_with_attribution":
        return "redistributable_with_attribution"
    if source.redistribution_policy == "upstream_download_only":
        return "upstream_required"
    return "local_only"


def _materialize_database(source: Path, target: Path, mode: DatabaseMode) -> None:
    source = source.resolve()
    if not source.is_file():
        raise FileNotFoundError(source)
    target.parent.mkdir(parents=True, exist_ok=True)
    if mode == "copy":
        shutil.copy2(source, target)
    elif mode == "hardlink":
        try:
            os.link(source, target)
        except OSError as exc:
            if exc.errno == EXDEV:
                raise ValueError(
                    f"cannot hardlink {source} across filesystems; "
                    "use database mode 'copy' or 'symlink'"
                ) from exc
            raise
    elif mode == "symlink":
        target.symlink_to(os.path.relpath(source, start=target.parent))
    else:
        raise ValueError(f"unsupported database mode: {mode}")


def _package_rows(
    repo_root: Path,
    realizations: list[Realization],
    logical_by_id: dict[str, LogicalInstance],
) -> list[dict[str, Any]]:
    dataset_cache: dict[Path, list[dict[str, Any]]] = {}
    rows: list[dict[str, Any]] = []
    for question_id, realization in enumerate(realizations):
        logical = logical_by_id[realization.logical_id]
        source_row = _load_source_row(
            repo_root,
            realization,
            logical,
            dataset_cache,
        )
        rows.append(
            {
                "question_id": question_id,
                "db_id": realization.database_id,
                "question": realization.question,
                "SQL": _single_line_sql(realization),
                "evidence": source_row.get("evidence") or "",
                "difficulty": (
                    logical.difficulty or source_row.get("difficulty") or "unknown"
                ),
                "logical_id": realization.logical_id,
                "realization_id": realization.realization_id,
                "source_family": realization.source_family,
                "source_sample_key": realization.source_sample_key,
            }
        )
    return rows


def _package_tables(
    repo_root: Path,
    realizations: list[Realization],
) -> list[dict[str, Any]]:
    table_paths = {realization.tables_path for realization in realizations}
    if len(table_paths) != 1:
        raise ValueError(f"package has multiple tables.json inputs: {sorted(table_paths)}")
    tables_path = _resolve(repo_root, next(iter(table_paths))).resolve()
    tables = load_json(tables_path)
    if not isinstance(tables, list) or not all(isinstance(row, dict) for row in tables):
        raise ValueError(f"{tables_path}: tables.json must be a list of objects")
    by_database: dict[str, dict[str, Any]] = {}
    for table in tables:
        database_id = table.get("db_id")
        if not isinstance(database_id, str) or not database_id:
            raise ValueError(f"{tables_path}: schema entry has no db_id")
        if database_id in by_database:
            raise ValueError(f"{tables_path}: duplicate db_id {database_id}")
        missing_fields = sorted(BIRD_SCHEMA_FIELDS - set(table))
        if missing_fields:
            raise ValueError(
                f"{tables_path}:{database_id}: missing BIRD schema fields "
                f"{missing_fields}"
            )
        by_database[database_id] = table
    requested = sorted({realization.database_id for realization in realizations})
    missing = [database_id for database_id in requested if database_id not in by_database]
    if missing:
        raise ValueError(f"{tables_path}: missing schemas for {missing}")
    return [by_database[database_id] for database_id in requested]


def _write_gold(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text(
        "".join(f"{row['SQL']}\t{row['db_id']}\n" for row in rows),
        encoding="utf-8",
        newline="\n",
    )


def _package_databases(
    repo_root: Path,
    package_dir: Path,
    realizations: list[Realization],
    database_mode: DatabaseMode,
    hasher: _FileHasher,
) -> dict[str, str]:
    database_paths: dict[str, Path] = {}
    expected_hashes: dict[str, str] = {}
    for realization in realizations:
        if realization.database_path is None:
            raise ValueError(f"{realization.realization_id}: database_path is missing")
        source = _resolve(repo_root, realization.database_path).resolve()
        previous = database_paths.setdefault(realization.database_id, source)
        if previous != source:
            raise ValueError(
                f"{realization.source_family}/{realization.configuration}/"
                f"{realization.database_id}: multiple database paths"
            )
        expected = realization.input_hashes.get("database")
        if expected is None:
            raise ValueError(f"{realization.realization_id}: database hash is missing")
        previous_hash = expected_hashes.setdefault(realization.database_id, expected)
        if previous_hash != expected:
            raise ValueError(
                f"{realization.source_family}/{realization.configuration}/"
                f"{realization.database_id}: inconsistent database hashes"
            )

    hashes: dict[str, str] = {}
    for database_id, source in sorted(database_paths.items()):
        actual_hash = hasher.hash(source)
        if actual_hash != expected_hashes[database_id]:
            raise ValueError(
                f"{source}: hash changed since canonical realization was built"
            )
        relative = Path("database") / database_id / f"{database_id}.sqlite"
        target = package_dir / relative
        _materialize_database(source, target, database_mode)
        hashes[relative.as_posix()] = actual_hash
    return hashes


def _update_release_metadata(
    release_dir: Path,
    manifest: ReleaseManifest,
    bird_manifest_path: Path,
    bird_manifest_hash: str,
    database_mode: DatabaseMode,
    distribution_scope: str,
) -> ReleaseManifest:
    relative_manifest = bird_manifest_path.relative_to(release_dir).as_posix()
    blockers = [
        blocker
        for blocker in manifest.blockers
        if not blocker.startswith("bird_format:")
    ]
    updated = manifest.model_copy(
        update={
            "status": "draft" if manifest.status == "frozen" else manifest.status,
            "blockers": blockers,
            "bird_format_version": BIRD_FORMAT_VERSION,
            "bird_format_manifest": relative_manifest,
            "bird_format_manifest_hash": bird_manifest_hash,
            "bird_format_packaging_mode": database_mode,
            "bird_format_distribution_scope": distribution_scope,
        }
    )
    write_json(release_dir / "release_manifest.json", updated.model_dump(mode="json"))
    sums_path = release_dir / "SHA256SUMS.json"
    sums = load_json(sums_path) if sums_path.is_file() else {}
    sums[relative_manifest] = bird_manifest_hash
    sums["release_manifest.json"] = sha256_file(release_dir / "release_manifest.json")
    write_json(sums_path, sums)
    return updated


def export_bird_full(options: BirdExportOptions) -> dict[str, Any]:
    repo_root = options.repo_root.resolve()
    release_dir = _resolve(repo_root, options.release_dir).resolve()
    output_dir = (
        _resolve(repo_root, options.output_dir).resolve()
        if options.output_dir is not None
        else release_dir / "bird_format"
    )
    if output_dir == release_dir or release_dir not in output_dir.parents:
        raise ValueError("BIRD export output must be inside the release directory")
    if output_dir.exists() and not options.overwrite:
        raise FileExistsError(f"{output_dir} already exists; pass overwrite=True")
    if options.distribution == "public" and options.database_mode != "copy":
        raise ValueError("public BIRD export requires database mode 'copy'")

    release_manifest = ReleaseManifest.model_validate(
        load_json(release_dir / "release_manifest.json")
    )
    logical = load_jsonl(release_dir / "logical_instances.jsonl", LogicalInstance)
    realizations = load_jsonl(release_dir / "realizations.jsonl", Realization)
    sources = load_jsonl(release_dir / "source_records.jsonl", SourceRecord)
    logical_by_id = {item.logical_id: item for item in logical}
    source_by_family = {item.source_family: item for item in sources}

    if options.distribution == "public":
        blocked = [
            source.source_family
            for source in sources
            if source.redistribution_policy != "redistributable_with_attribution"
        ]
        if blocked:
            raise ValueError(
                "public BIRD export is blocked by source redistribution policy: "
                + ", ".join(sorted(blocked))
            )

    grouped: dict[tuple[str, str], list[Realization]] = defaultdict(list)
    for realization in realizations:
        grouped[(realization.source_family, realization.configuration)].append(
            realization
        )
    expected_keys = {
        (source_family, configuration)
        for source_family in release_manifest.source_families
        for configuration in release_manifest.configurations
    }
    if set(grouped) != expected_keys:
        missing = sorted(expected_keys - set(grouped))
        extra = sorted(set(grouped) - expected_keys)
        raise ValueError(f"incomplete source/configuration groups: missing={missing}, extra={extra}")

    temporary_dir = output_dir.with_name(f".{output_dir.name}.tmp")
    if temporary_dir.exists():
        shutil.rmtree(temporary_dir)
    temporary_dir.mkdir(parents=True)
    hasher = _FileHasher()
    package_records: list[dict[str, Any]] = []
    try:
        for source_family, configuration in sorted(grouped):
            group = sorted(
                grouped[(source_family, configuration)],
                key=lambda item: (
                    logical_by_id[item.logical_id].legacy_index,
                    item.realization_id,
                ),
            )
            package_dir = temporary_dir / source_family / configuration
            package_dir.mkdir(parents=True)
            rows = _package_rows(repo_root, group, logical_by_id)
            tables = _package_tables(repo_root, group)
            write_json(package_dir / "dev.json", rows)
            write_json(package_dir / "tables.json", tables)
            _write_gold(package_dir / "dev_gold.sql", rows)
            database_hashes = _package_databases(
                repo_root,
                package_dir,
                group,
                options.database_mode,
                hasher,
            )
            file_hashes = {
                "dev.json": hasher.hash(package_dir / "dev.json"),
                "dev_gold.sql": hasher.hash(package_dir / "dev_gold.sql"),
                "tables.json": hasher.hash(package_dir / "tables.json"),
                **database_hashes,
            }
            source_record = source_by_family[source_family]
            package_manifest = {
                "schema_version": BIRD_FORMAT_VERSION,
                "release_id": release_manifest.release_id,
                "source_family": source_family,
                "configuration": configuration,
                "packaging_mode": options.database_mode,
                "distribution_scope": _distribution_scope(source_record),
                "samples": len(rows),
                "databases": len(database_hashes),
                "realization_ids": [row["realization_id"] for row in rows],
                "file_hashes": dict(sorted(file_hashes.items())),
                "canonical_artifact_hashes": {
                    name: release_manifest.file_hashes[name]
                    for name in (
                        "logical_instances.jsonl",
                        "realizations.jsonl",
                        "source_records.jsonl",
                    )
                },
            }
            write_json(package_dir / "package_manifest.json", package_manifest)
            package_records.append(
                {
                    "source_family": source_family,
                    "configuration": configuration,
                    "path": f"{source_family}/{configuration}",
                    "samples": len(rows),
                    "databases": len(database_hashes),
                    "distribution_scope": _distribution_scope(source_record),
                    "package_manifest_hash": hasher.hash(
                        package_dir / "package_manifest.json"
                    ),
                }
            )

        scopes = {record["distribution_scope"] for record in package_records}
        overall_scope = (
            "local_only"
            if "local_only" in scopes
            else "upstream_required"
            if "upstream_required" in scopes
            else "redistributable_with_attribution"
        )
        bird_manifest = {
            "schema_version": BIRD_FORMAT_VERSION,
            "release_id": release_manifest.release_id,
            "packaging_mode": options.database_mode,
            "requested_distribution": options.distribution,
            "distribution_scope": overall_scope,
            "source_packages": package_records,
            "totals": {
                "packages": len(package_records),
                "samples": sum(record["samples"] for record in package_records),
                "databases_across_packages": sum(
                    record["databases"] for record in package_records
                ),
            },
            "canonical_artifact_hashes": {
                name: release_manifest.file_hashes[name]
                for name in (
                    "logical_instances.jsonl",
                    "realizations.jsonl",
                    "source_records.jsonl",
                )
            },
        }
        write_json(temporary_dir / "manifest.json", bird_manifest)
        if output_dir.exists():
            shutil.rmtree(output_dir)
        temporary_dir.replace(output_dir)
    except Exception:
        if temporary_dir.exists():
            shutil.rmtree(temporary_dir)
        raise

    bird_manifest_path = output_dir / "manifest.json"
    bird_manifest_hash = sha256_file(bird_manifest_path)
    updated_release = _update_release_metadata(
        release_dir,
        release_manifest,
        bird_manifest_path,
        bird_manifest_hash,
        options.database_mode,
        load_json(bird_manifest_path)["distribution_scope"],
    )
    validation = validate_bird_full(repo_root, release_dir, output_dir)
    return {
        "release_id": updated_release.release_id,
        "output_dir": output_dir.as_posix(),
        "manifest": bird_manifest_path.as_posix(),
        **validation,
    }


def _check_sqlite_readable(path: Path) -> None:
    try:
        with sqlite3.connect(f"file:{path}?mode=ro", uri=True) as connection:
            connection.execute("PRAGMA schema_version").fetchone()
    except sqlite3.DatabaseError as exc:
        raise ValueError(f"{path}: unreadable SQLite database: {exc}") from exc


def validate_bird_full(
    repo_root: Path,
    release_dir: Path,
    output_dir: Path | None = None,
) -> dict[str, Any]:
    repo_root = repo_root.resolve()
    release_dir = _resolve(repo_root, release_dir).resolve()
    release_manifest = ReleaseManifest.model_validate(
        load_json(release_dir / "release_manifest.json")
    )
    if output_dir is None:
        if release_manifest.bird_format_manifest is None:
            raise ValueError("release manifest does not reference a BIRD export")
        root_manifest_path = _resolve(
            release_dir,
            release_manifest.bird_format_manifest,
        ).resolve()
        output_dir = root_manifest_path.parent
    else:
        output_dir = _resolve(repo_root, output_dir).resolve()
        root_manifest_path = output_dir / "manifest.json"
    if not root_manifest_path.is_file():
        raise FileNotFoundError(root_manifest_path)
    root_hash = sha256_file(root_manifest_path)
    if release_manifest.bird_format_manifest_hash != root_hash:
        raise ValueError("BIRD manifest hash does not match release manifest")
    root = load_json(root_manifest_path)
    if root.get("schema_version") != BIRD_FORMAT_VERSION:
        raise ValueError("unsupported BIRD export schema version")
    if root.get("release_id") != release_manifest.release_id:
        raise ValueError("BIRD export release_id mismatch")
    for name, expected in root["canonical_artifact_hashes"].items():
        if release_manifest.file_hashes.get(name) != expected:
            raise ValueError(f"canonical artifact changed after BIRD export: {name}")

    realizations = load_jsonl(release_dir / "realizations.jsonl", Realization)
    expected_by_id = {item.realization_id: item for item in realizations}
    seen_realizations: set[str] = set()
    hasher = _FileHasher()
    sample_counts: Counter[str] = Counter()

    expected_packages = {
        (source_family, configuration)
        for source_family in release_manifest.source_families
        for configuration in release_manifest.configurations
    }
    records = root.get("source_packages")
    if not isinstance(records, list):
        raise ValueError("BIRD manifest source_packages must be a list")
    actual_packages = {
        (record.get("source_family"), record.get("configuration"))
        for record in records
    }
    if actual_packages != expected_packages:
        raise ValueError("BIRD export does not contain every source/configuration package")

    for record in records:
        source_family = record["source_family"]
        configuration = record["configuration"]
        package_dir = output_dir / record["path"]
        package_manifest_path = package_dir / "package_manifest.json"
        if hasher.hash(package_manifest_path) != record["package_manifest_hash"]:
            raise ValueError(f"{package_dir}: package manifest hash mismatch")
        package = load_json(package_manifest_path)
        if package["source_family"] != source_family:
            raise ValueError(f"{package_dir}: source_family mismatch")
        if package["configuration"] != configuration:
            raise ValueError(f"{package_dir}: configuration mismatch")
        for relative, expected_hash in package["file_hashes"].items():
            path = package_dir / relative
            if hasher.hash(path) != expected_hash:
                raise ValueError(f"{path}: hash mismatch")
            if relative.startswith("database/"):
                _check_sqlite_readable(path)

        dev = load_json(package_dir / "dev.json")
        tables = load_json(package_dir / "tables.json")
        gold_lines = (package_dir / "dev_gold.sql").read_text(
            encoding="utf-8"
        ).splitlines()
        if not isinstance(dev, list) or not isinstance(tables, list):
            raise ValueError(f"{package_dir}: dev.json and tables.json must be lists")
        if len(dev) != package["samples"] or len(gold_lines) != len(dev):
            raise ValueError(f"{package_dir}: sample count mismatch")
        if [row["realization_id"] for row in dev] != package["realization_ids"]:
            raise ValueError(f"{package_dir}: realization order mismatch")
        table_ids = [row.get("db_id") for row in tables]
        if len(table_ids) != len(set(table_ids)):
            raise ValueError(f"{package_dir}: duplicate tables.json db_id")
        dev_database_ids = {row["db_id"] for row in dev}
        if set(table_ids) != dev_database_ids:
            raise ValueError(f"{package_dir}: tables.json database coverage mismatch")

        for index, (row, gold_line) in enumerate(zip(dev, gold_lines, strict=True)):
            if row["question_id"] != index:
                raise ValueError(f"{package_dir}: non-sequential question_id")
            realization_id = row["realization_id"]
            if realization_id in seen_realizations:
                raise ValueError(f"duplicate realization in BIRD export: {realization_id}")
            seen_realizations.add(realization_id)
            realization = expected_by_id.get(realization_id)
            if realization is None:
                raise ValueError(f"unknown realization in BIRD export: {realization_id}")
            if realization.source_family != source_family:
                raise ValueError(f"{realization_id}: source_family mismatch")
            if realization.configuration != configuration:
                raise ValueError(f"{realization_id}: configuration mismatch")
            if row["logical_id"] != realization.logical_id:
                raise ValueError(f"{realization_id}: logical_id mismatch")
            if row["question"] != realization.question:
                raise ValueError(f"{realization_id}: question mismatch")
            if row["db_id"] != realization.database_id:
                raise ValueError(f"{realization_id}: db_id mismatch")
            if row["SQL"] != realization.gold_sql.strip():
                raise ValueError(f"{realization_id}: SQL mismatch")
            if gold_line != f"{row['SQL']}\t{row['db_id']}":
                raise ValueError(f"{realization_id}: dev_gold.sql mismatch")
            sample_counts[source_family] += 1

    if seen_realizations != set(expected_by_id):
        missing = sorted(set(expected_by_id) - seen_realizations)
        raise ValueError(f"BIRD export is missing realizations: {missing[:10]}")
    return {
        "valid": True,
        "schema_version": BIRD_FORMAT_VERSION,
        "packages": len(records),
        "samples": len(seen_realizations),
        "source_sample_counts": dict(sorted(sample_counts.items())),
        "packaging_mode": root["packaging_mode"],
        "distribution_scope": root["distribution_scope"],
    }
