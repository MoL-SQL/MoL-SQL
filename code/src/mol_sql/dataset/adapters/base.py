"""Common adapter implementation for aligned legacy four-cell workloads."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Literal

import yaml
from pydantic import BaseModel, ConfigDict, Field

from mol_sql.contracts.hashing import sha256_file
from mol_sql.contracts.io import load_json

FULL_CONFIGURATIONS = (
    "Q_en--S_en--V_en",
    "Q_zh--S_en--V_en",
    "Q_en--S_zh--V_zh",
    "Q_zh--S_zh--V_zh",
)


class VariantSpec(BaseModel):
    model_config = ConfigDict(extra="forbid")
    directory: str
    question_language: Literal["en", "zh"]
    schema_language: Literal["en", "zh"]
    value_language: Literal["en", "zh"]


class SourceSpec(BaseModel):
    model_config = ConfigDict(extra="forbid")
    source_family: str
    release_role: Literal["core", "extension"] = "core"
    root: str
    native_language: Literal["en", "zh"]
    split: str
    id_field: str | None = None
    sql_fields: list[str] = Field(default_factory=lambda: ["query", "SQL", "sql_query"])
    difficulty_field: str | None = "difficulty"
    upstream_version: str | None = None
    source_url: str | None = None
    snapshot_date: str | None = None
    license_spdx: str | None = None
    license_evidence_url: str | None = None
    redistribution_policy: Literal[
        "redistributable_with_attribution",
        "upstream_download_only",
        "unresolved",
    ] = "unresolved"
    license_notes: str | None = None
    replacement_proposals: str | None = None
    replacement_map: str | None = None
    fixed_points: str | None = None
    execution_repairs: str | None = None
    execution_adjudications: str | None = None
    database_roots: dict[Literal["en", "zh"], str | None]
    variants: dict[str, VariantSpec]


@dataclass(frozen=True)
class AdaptedSample:
    source_sample_key: str
    legacy_index: int
    database_id: str
    difficulty: str | None
    rows: dict[str, dict[str, Any]]


@dataclass(frozen=True)
class AdaptedSource:
    repo_root: Path
    spec: SourceSpec
    samples: list[AdaptedSample]
    dev_paths: dict[str, Path]
    tables_paths: dict[str, Path]
    database_paths: dict[tuple[str, str], Path | None]
    input_hashes: dict[str, str]
    dropped_samples: list[dict[str, Any]]
    execution_sql: Callable[[str], str]


def load_source_specs(path: Path) -> list[SourceSpec]:
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict) or not isinstance(raw.get("sources"), list):
        raise ValueError(f"{path}: expected a top-level sources list")
    specs = [SourceSpec.model_validate(item) for item in raw["sources"]]
    names = [spec.source_family for spec in specs]
    if len(names) != len(set(names)):
        raise ValueError(f"{path}: duplicate source_family")
    return specs


class SourceAdapter:
    """Normalize one source family while preserving all original rows."""

    source_family: str

    def __init__(self, repo_root: Path, spec: SourceSpec):
        if spec.source_family != self.source_family:
            raise ValueError(
                f"{type(self).__name__} cannot load {spec.source_family!r}"
            )
        self.repo_root = repo_root.resolve()
        self.spec = spec
        self.source_root = self.repo_root / spec.root

    def _sql(self, row: dict[str, Any]) -> str:
        for field in self.spec.sql_fields:
            value = row.get(field)
            if isinstance(value, str) and value.strip():
                return value.strip()
        raise ValueError(
            f"{self.source_family}: no SQL in fields {self.spec.sql_fields}"
        )

    def sql(self, row: dict[str, Any]) -> str:
        return self._sql(row)

    @classmethod
    def execution_sql(cls, sql: str) -> str:
        """Apply source-official deterministic SQL evaluation preprocessing."""

        return sql

    def question(self, row: dict[str, Any]) -> str:
        value = row.get("question")
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{self.source_family}: empty question")
        return value.strip()

    def sample_key(self, row: dict[str, Any], index: int) -> str:
        if self.spec.id_field is None:
            return f"index:{index}"
        value = row.get(self.spec.id_field)
        if value is None or str(value).strip() == "":
            raise ValueError(
                f"{self.source_family}:{index}: missing {self.spec.id_field}"
            )
        return str(value)

    def database_id(self, row: dict[str, Any]) -> str:
        value = row.get("db_id", row.get("db_name"))
        if value is None or str(value).strip() == "":
            raise ValueError(f"{self.source_family}: missing database ID")
        return str(value)

    def _database_path(self, language: str, database_id: str) -> Path | None:
        configured = self.spec.database_roots.get(language)
        if configured is None:
            return None
        root = self.repo_root / configured
        candidates = [
            root / database_id / f"{database_id}.sqlite",
            root / database_id / f"{database_id}.db",
            root / f"{database_id}.sqlite",
            root / f"{database_id}.db",
        ]
        for candidate in candidates:
            if candidate.is_file():
                return candidate
        db_dir = root / database_id
        if db_dir.is_dir():
            found = sorted((*db_dir.glob("*.sqlite"), *db_dir.glob("*.db")))
            if len(found) == 1:
                return found[0]
        return None

    def load(self) -> AdaptedSource:
        if set(self.spec.variants) != set(FULL_CONFIGURATIONS):
            raise ValueError(
                f"{self.source_family}: expected exactly {FULL_CONFIGURATIONS}"
            )
        rows_by_configuration: dict[str, list[dict[str, Any]]] = {}
        dev_paths: dict[str, Path] = {}
        tables_paths: dict[str, Path] = {}
        input_hashes: dict[str, str] = {}
        for configuration in FULL_CONFIGURATIONS:
            variant = self.spec.variants[configuration]
            directory = self.source_root / variant.directory
            dev_path, tables_path = directory / "dev.json", directory / "tables.json"
            if not dev_path.is_file() or not tables_path.is_file():
                raise FileNotFoundError(
                    f"{self.source_family}/{configuration}: missing dev.json or tables.json"
                )
            rows = load_json(dev_path)
            tables = load_json(tables_path)
            if not isinstance(rows, list) or not isinstance(tables, list):
                raise ValueError(f"{directory}: dev.json and tables.json must be lists")
            rows_by_configuration[configuration] = rows
            dev_paths[configuration], tables_paths[configuration] = dev_path, tables_path
            input_hashes[f"{configuration}:dev.json"] = sha256_file(dev_path)
            input_hashes[f"{configuration}:tables.json"] = sha256_file(tables_path)

        counts = {name: len(rows) for name, rows in rows_by_configuration.items()}
        if len(set(counts.values())) != 1:
            raise ValueError(f"{self.source_family}: unaligned counts: {counts}")

        samples: list[AdaptedSample] = []
        database_ids: set[str] = set()
        for index in range(next(iter(counts.values()))):
            rows = {
                configuration: rows_by_configuration[configuration][index]
                for configuration in FULL_CONFIGURATIONS
            }
            keys = {
                self.sample_key(row, index)
                for row in rows.values()
            }
            if len(keys) != 1:
                raise ValueError(
                    f"{self.source_family}:{index}: source IDs differ: {sorted(keys)}"
                )
            db_ids = {self.database_id(row) for row in rows.values()}
            if len(db_ids) != 1:
                raise ValueError(
                    f"{self.source_family}:{index}: database IDs differ: {sorted(db_ids)}"
                )
            database_id = next(iter(db_ids))
            database_ids.add(database_id)
            difficulty = None
            if self.spec.difficulty_field:
                raw_difficulty = rows[FULL_CONFIGURATIONS[0]].get(
                    self.spec.difficulty_field
                )
                difficulty = (
                    str(raw_difficulty) if raw_difficulty is not None else None
                )
            samples.append(
                AdaptedSample(
                    source_sample_key=next(iter(keys)),
                    legacy_index=index,
                    database_id=database_id,
                    difficulty=difficulty,
                    rows=rows,
                )
            )

        dropped_samples: list[dict[str, Any]] = []
        if self.spec.execution_adjudications:
            adjudication_path = (
                self.repo_root / self.spec.execution_adjudications
            )
            if not adjudication_path.is_file():
                raise FileNotFoundError(adjudication_path)
            decisions = load_json(adjudication_path).get("decisions", [])
            drops = {
                int(row["legacy_index"]): row
                for row in decisions
                if row.get("source_family") == self.source_family
                and row.get("decision") == "drop"
            }
            for index, decision in drops.items():
                if index >= len(samples):
                    raise ValueError(
                        f"{self.source_family}: invalid dropped legacy index {index}"
                    )
                sample = samples[index]
                if (
                    sample.source_sample_key != str(decision["source_sample_key"])
                    or sample.database_id != str(decision["database_id"])
                ):
                    raise ValueError(
                        f"{self.source_family}:{index}: adjudication identity mismatch"
                    )
                dropped_samples.append(dict(decision))
            samples = [
                sample
                for sample in samples
                if sample.legacy_index not in drops
            ]
            database_ids = {sample.database_id for sample in samples}

        database_paths = {
            (language, database_id): self._database_path(language, database_id)
            for language in ("en", "zh")
            for database_id in sorted(database_ids)
        }
        for path in sorted(
            {path for path in database_paths.values() if path is not None}
        ):
            relative = path.relative_to(self.repo_root).as_posix()
            input_hashes[f"database:{relative}"] = sha256_file(path)

        for name in (
            "replacement_proposals",
            "replacement_map",
            "fixed_points",
            "execution_repairs",
            "execution_adjudications",
        ):
            configured = getattr(self.spec, name)
            if configured:
                artifact = self.repo_root / configured
                if artifact.is_file():
                    input_hashes[name] = sha256_file(artifact)

        return AdaptedSource(
            repo_root=self.repo_root,
            spec=self.spec,
            samples=samples,
            dev_paths=dev_paths,
            tables_paths=tables_paths,
            database_paths=database_paths,
            input_hashes=input_hashes,
            dropped_samples=dropped_samples,
            execution_sql=self.execution_sql,
        )
