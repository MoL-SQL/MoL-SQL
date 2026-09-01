"""Export and validate source-separated BIRD-compatible MoL-Cube packages."""

from __future__ import annotations

import shutil
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

from mol_sql.contracts.hashing import sha256_file
from mol_sql.contracts.io import load_json, load_jsonl, write_json
from mol_sql.dataset.full.bird_export import (
    BIRD_SCHEMA_FIELDS,
    _FileHasher,
    _check_sqlite_readable,
    _materialize_database,
)

from .models import CubeCandidateProfile, CubeRealization, CubeReleaseManifest

CUBE_BIRD_FORMAT_VERSION = "mol-cube-bird-format-v0.1"
DatabaseMode = Literal["copy", "hardlink", "symlink"]
DistributionMode = Literal["local", "public"]


@dataclass(frozen=True)
class CubeBirdExportOptions:
    repo_root: Path
    release_dir: Path
    output_dir: Path | None = None
    database_mode: DatabaseMode = "symlink"
    distribution: DistributionMode = "local"
    overwrite: bool = False


def _resolve(repo_root: Path, path: str | Path) -> Path:
    candidate = Path(path)
    return candidate if candidate.is_absolute() else repo_root / candidate


def _package_rows(
    realizations: list[CubeRealization],
    profiles: dict[str, CubeCandidateProfile],
) -> list[dict[str, Any]]:
    rows = []
    for question_id, realization in enumerate(realizations):
        sql = realization.gold_sql.strip()
        if any(character in sql for character in ("\n", "\r", "\t")):
            raise ValueError(f"{realization.realization_id}: SQL is not single-line")
        profile = profiles[realization.logical_id]
        rows.append(
            {
                "question_id": question_id,
                "db_id": realization.database_id,
                "question": realization.question,
                "SQL": sql,
                "evidence": "",
                "difficulty": profile.difficulty["composite_tier"],
                "logical_id": realization.logical_id,
                "realization_id": realization.realization_id,
                "source_family": realization.source_family,
                "source_sample_key": realization.source_sample_key,
                "configuration": realization.configuration,
                "question_language": realization.question_language,
                "schema_language": realization.schema_language,
                "value_language": realization.value_language,
            }
        )
    return rows


def _package_tables(repo_root: Path, realizations: list[CubeRealization]) -> list[dict[str, Any]]:
    table_paths = {row.tables_path for row in realizations}
    if len(table_paths) != 1:
        raise ValueError(f"package has multiple tables inputs: {sorted(table_paths)}")
    tables_path = _resolve(repo_root, next(iter(table_paths))).resolve()
    tables = load_json(tables_path)
    if not isinstance(tables, list) or not all(isinstance(row, dict) for row in tables):
        raise ValueError(f"{tables_path}: tables.json must be a list")
    by_database: dict[str, dict[str, Any]] = {}
    for row in tables:
        database_id = row.get("db_id")
        if not isinstance(database_id, str) or not database_id:
            raise ValueError(f"{tables_path}: schema entry has no db_id")
        missing = sorted(BIRD_SCHEMA_FIELDS - set(row))
        if missing:
            raise ValueError(f"{tables_path}:{database_id}: missing fields {missing}")
        if database_id in by_database:
            raise ValueError(f"{tables_path}: duplicate db_id {database_id}")
        by_database[database_id] = row
    requested = sorted({row.database_id for row in realizations})
    missing = [database_id for database_id in requested if database_id not in by_database]
    if missing:
        raise ValueError(f"{tables_path}: missing schemas for {missing}")
    return [by_database[database_id] for database_id in requested]


def _package_databases(
    repo_root: Path,
    package_dir: Path,
    realizations: list[CubeRealization],
    mode: DatabaseMode,
    hasher: _FileHasher,
) -> dict[str, str]:
    paths: dict[str, Path] = {}
    hashes: dict[str, str] = {}
    for row in realizations:
        source = _resolve(repo_root, row.database_path).resolve()
        if paths.setdefault(row.database_id, source) != source:
            raise ValueError(f"{row.realization_id}: multiple database paths")
        if hashes.setdefault(row.database_id, row.database_hash) != row.database_hash:
            raise ValueError(f"{row.realization_id}: inconsistent database hashes")
    packaged = {}
    for database_id, source in sorted(paths.items()):
        actual_hash = hasher.hash(source)
        if actual_hash != hashes[database_id]:
            raise ValueError(f"{source}: hash changed since Cube construction")
        relative = Path("database") / database_id / f"{database_id}.sqlite"
        _materialize_database(source, package_dir / relative, mode)
        packaged[relative.as_posix()] = actual_hash
    return packaged


def _distribution_scope(manifest: CubeReleaseManifest) -> str:
    blockers = "\n".join(manifest.blockers).lower()
    return (
        "local_only"
        if "redistribution" in blockers or "license" in blockers
        else "redistributable_with_attribution"
    )


def _update_release_metadata(
    release_dir: Path,
    manifest: CubeReleaseManifest,
    bird_manifest_path: Path,
    database_mode: DatabaseMode,
    distribution_scope: str,
) -> CubeReleaseManifest:
    relative = bird_manifest_path.relative_to(release_dir).as_posix()
    bird_hash = sha256_file(bird_manifest_path)
    updated = manifest.model_copy(
        update={
            "bird_format_version": CUBE_BIRD_FORMAT_VERSION,
            "bird_format_manifest": relative,
            "bird_format_manifest_hash": bird_hash,
            "bird_format_packaging_mode": database_mode,
            "bird_format_distribution_scope": distribution_scope,
        }
    )
    write_json(release_dir / "release_manifest.json", updated.model_dump(mode="json"))
    sums_path = release_dir / "SHA256SUMS.json"
    sums = load_json(sums_path) if sums_path.is_file() else {}
    sums[relative] = bird_hash
    sums["release_manifest.json"] = sha256_file(release_dir / "release_manifest.json")
    write_json(sums_path, sums)
    return updated


def export_bird_cube(options: CubeBirdExportOptions) -> dict[str, Any]:
    repo_root = options.repo_root.resolve()
    release_dir = _resolve(repo_root, options.release_dir).resolve()
    output_dir = (
        _resolve(repo_root, options.output_dir).resolve()
        if options.output_dir is not None
        else release_dir / "bird_format"
    )
    if output_dir == release_dir or release_dir not in output_dir.parents:
        raise ValueError("BIRD export output must be inside the Cube release directory")
    if output_dir.exists() and not options.overwrite:
        raise FileExistsError(f"{output_dir} already exists; pass overwrite=True")
    if options.distribution == "public" and options.database_mode != "copy":
        raise ValueError("public BIRD export requires database mode 'copy'")
    manifest = CubeReleaseManifest.model_validate(load_json(release_dir / "release_manifest.json"))
    scope = _distribution_scope(manifest)
    if options.distribution == "public" and scope != "redistributable_with_attribution":
        raise ValueError("public BIRD export is blocked by unresolved licensing or redistribution")
    realizations = load_jsonl(release_dir / "realizations.jsonl", CubeRealization)
    profiles = {
        row.logical_id: row
        for row in load_jsonl(release_dir / "candidate_profiles.jsonl", CubeCandidateProfile)
    }
    grouped: dict[tuple[str, str], list[CubeRealization]] = defaultdict(list)
    for row in realizations:
        grouped[(row.source_family, row.configuration)].append(row)
    expected = {
        (source, configuration)
        for source in manifest.source_families
        for configuration in manifest.configurations
    }
    if set(grouped) != expected:
        raise ValueError(f"incomplete source/configuration groups: missing={sorted(expected-set(grouped))}")

    temporary_dir = output_dir.with_name(f".{output_dir.name}.tmp")
    if temporary_dir.exists():
        shutil.rmtree(temporary_dir)
    temporary_dir.mkdir(parents=True)
    hasher = _FileHasher()
    packages = []
    try:
        for source, configuration in sorted(grouped):
            group = sorted(
                grouped[(source, configuration)],
                key=lambda row: (profiles[row.logical_id].legacy_index, row.realization_id),
            )
            package_dir = temporary_dir / source / configuration
            package_dir.mkdir(parents=True)
            rows = _package_rows(group, profiles)
            write_json(package_dir / "dev.json", rows)
            write_json(package_dir / "tables.json", _package_tables(repo_root, group))
            (package_dir / "dev_gold.sql").write_text(
                "".join(f"{row['SQL']}\t{row['db_id']}\n" for row in rows),
                encoding="utf-8",
                newline="\n",
            )
            database_hashes = _package_databases(
                repo_root, package_dir, group, options.database_mode, hasher
            )
            file_hashes = {
                "dev.json": hasher.hash(package_dir / "dev.json"),
                "dev_gold.sql": hasher.hash(package_dir / "dev_gold.sql"),
                "tables.json": hasher.hash(package_dir / "tables.json"),
                **database_hashes,
            }
            package_manifest = {
                "schema_version": CUBE_BIRD_FORMAT_VERSION,
                "release_id": manifest.release_id,
                "source_family": source,
                "configuration": configuration,
                "packaging_mode": options.database_mode,
                "distribution_scope": scope,
                "samples": len(rows),
                "databases": len(database_hashes),
                "logical_ids": [row["logical_id"] for row in rows],
                "realization_ids": [row["realization_id"] for row in rows],
                "file_hashes": dict(sorted(file_hashes.items())),
                "canonical_artifact_hashes": {
                    name: manifest.file_hashes[name]
                    for name in ("candidate_profiles.jsonl", "membership.jsonl", "realizations.jsonl")
                },
            }
            write_json(package_dir / "package_manifest.json", package_manifest)
            packages.append(
                {
                    "source_family": source,
                    "configuration": configuration,
                    "path": f"{source}/{configuration}",
                    "samples": len(rows),
                    "databases": len(database_hashes),
                    "distribution_scope": scope,
                    "package_manifest_hash": hasher.hash(package_dir / "package_manifest.json"),
                }
            )
        write_json(
            temporary_dir / "manifest.json",
            {
                "schema_version": CUBE_BIRD_FORMAT_VERSION,
                "release_id": manifest.release_id,
                "packaging_mode": options.database_mode,
                "requested_distribution": options.distribution,
                "distribution_scope": scope,
                "source_packages": packages,
                "totals": {
                    "packages": len(packages),
                    "samples": sum(row["samples"] for row in packages),
                    "databases_across_packages": sum(row["databases"] for row in packages),
                },
                "canonical_artifact_hashes": {
                    name: manifest.file_hashes[name]
                    for name in ("candidate_profiles.jsonl", "membership.jsonl", "realizations.jsonl")
                },
            },
        )
        if output_dir.exists():
            shutil.rmtree(output_dir)
        temporary_dir.replace(output_dir)
    except Exception:
        if temporary_dir.exists():
            shutil.rmtree(temporary_dir)
        raise

    updated = _update_release_metadata(
        release_dir, manifest, output_dir / "manifest.json", options.database_mode, scope
    )
    return {
        "release_id": updated.release_id,
        "output_dir": output_dir.as_posix(),
        **validate_bird_cube(repo_root, release_dir, output_dir),
    }


def validate_bird_cube(
    repo_root: Path,
    release_dir: Path,
    output_dir: Path | None = None,
) -> dict[str, Any]:
    repo_root = repo_root.resolve()
    release_dir = _resolve(repo_root, release_dir).resolve()
    manifest = CubeReleaseManifest.model_validate(load_json(release_dir / "release_manifest.json"))
    if output_dir is None:
        if manifest.bird_format_manifest is None:
            raise ValueError("Cube release manifest does not reference a BIRD export")
        root_manifest_path = _resolve(release_dir, manifest.bird_format_manifest).resolve()
        output_dir = root_manifest_path.parent
    else:
        output_dir = _resolve(repo_root, output_dir).resolve()
        root_manifest_path = output_dir / "manifest.json"
    if sha256_file(root_manifest_path) != manifest.bird_format_manifest_hash:
        raise ValueError("BIRD manifest hash does not match Cube release manifest")
    root = load_json(root_manifest_path)
    if root.get("schema_version") != CUBE_BIRD_FORMAT_VERSION:
        raise ValueError("unsupported Cube BIRD format version")
    if root.get("release_id") != manifest.release_id:
        raise ValueError("Cube BIRD release_id mismatch")
    for name, expected_hash in root["canonical_artifact_hashes"].items():
        if manifest.file_hashes.get(name) != expected_hash:
            raise ValueError(f"canonical Cube artifact changed after export: {name}")

    realizations = load_jsonl(release_dir / "realizations.jsonl", CubeRealization)
    expected_by_id = {row.realization_id: row for row in realizations}
    expected_packages = {
        (source, configuration)
        for source in manifest.source_families
        for configuration in manifest.configurations
    }
    records = root.get("source_packages")
    if not isinstance(records, list):
        raise ValueError("Cube BIRD source_packages must be a list")
    if {(row.get("source_family"), row.get("configuration")) for row in records} != expected_packages:
        raise ValueError("Cube BIRD export does not contain every source/configuration package")

    seen: set[str] = set()
    configuration_counts: Counter[str] = Counter()
    source_counts: Counter[str] = Counter()
    hasher = _FileHasher()
    for record in records:
        source, configuration = record["source_family"], record["configuration"]
        package_dir = output_dir / record["path"]
        package_path = package_dir / "package_manifest.json"
        if hasher.hash(package_path) != record["package_manifest_hash"]:
            raise ValueError(f"{package_dir}: package manifest hash mismatch")
        package = load_json(package_path)
        if package["source_family"] != source or package["configuration"] != configuration:
            raise ValueError(f"{package_dir}: package identity mismatch")
        for relative, expected_hash in package["file_hashes"].items():
            path = package_dir / relative
            if hasher.hash(path) != expected_hash:
                raise ValueError(f"{path}: hash mismatch")
            if relative.startswith("database/"):
                _check_sqlite_readable(path)
        dev = load_json(package_dir / "dev.json")
        tables = load_json(package_dir / "tables.json")
        gold = (package_dir / "dev_gold.sql").read_text(encoding="utf-8").splitlines()
        if len(dev) != package["samples"] or len(gold) != len(dev):
            raise ValueError(f"{package_dir}: sample count mismatch")
        if [row["realization_id"] for row in dev] != package["realization_ids"]:
            raise ValueError(f"{package_dir}: realization order mismatch")
        if [row["logical_id"] for row in dev] != package["logical_ids"]:
            raise ValueError(f"{package_dir}: logical order mismatch")
        table_ids = [row.get("db_id") for row in tables]
        if len(table_ids) != len(set(table_ids)) or set(table_ids) != {row["db_id"] for row in dev}:
            raise ValueError(f"{package_dir}: tables.json database coverage mismatch")
        for index, (row, gold_line) in enumerate(zip(dev, gold, strict=True)):
            if row["question_id"] != index:
                raise ValueError(f"{package_dir}: non-sequential question_id")
            realization_id = row["realization_id"]
            expected = expected_by_id.get(realization_id)
            if expected is None or realization_id in seen:
                raise ValueError(f"unknown or duplicate Cube realization: {realization_id}")
            seen.add(realization_id)
            if expected.source_family != source or expected.configuration != configuration:
                raise ValueError(f"{realization_id}: package placement mismatch")
            if row["logical_id"] != expected.logical_id or row["question"] != expected.question:
                raise ValueError(f"{realization_id}: identity or question mismatch")
            if row["db_id"] != expected.database_id or row["SQL"] != expected.gold_sql.strip():
                raise ValueError(f"{realization_id}: database or SQL mismatch")
            if gold_line != f"{row['SQL']}\t{row['db_id']}":
                raise ValueError(f"{realization_id}: dev_gold.sql mismatch")
            configuration_counts[configuration] += 1
            source_counts[source] += 1
    if seen != set(expected_by_id):
        raise ValueError(f"Cube BIRD export is missing {len(set(expected_by_id)-seen)} realizations")
    if any(
        configuration_counts[configuration] != manifest.logical_instances
        for configuration in manifest.configurations
    ):
        raise ValueError("Cube BIRD configuration counts are not balanced")
    return {
        "valid": True,
        "schema_version": CUBE_BIRD_FORMAT_VERSION,
        "packages": len(records),
        "samples": len(seen),
        "configuration_sample_counts": dict(sorted(configuration_counts.items())),
        "source_sample_counts": dict(sorted(source_counts.items())),
        "packaging_mode": root["packaging_mode"],
        "distribution_scope": root["distribution_scope"],
    }
