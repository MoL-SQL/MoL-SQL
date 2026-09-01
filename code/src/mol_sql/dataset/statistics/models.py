"""Versioned records for MoL-Full dataset statistics."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

FULL_STATISTICS_VERSION = "mol-full-statistics-v0.1"
CUBE_STATISTICS_VERSION = "mol-cube-statistics-v0.1"


class StatisticsModel(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_assignment=True)
    statistics_version: Literal["mol-full-statistics-v0.1"] = FULL_STATISTICS_VERSION


class FullLogicalProfile(StatisticsModel):
    logical_id: str
    source_family: str
    database_id: str
    split: str
    source_sample_key: str
    legacy_index: int = Field(ge=0)
    source_difficulty: str | None
    answer_semantics: Literal["ordered", "multiset"]
    phenomena: list[str]
    sql_features: dict[str, Any]
    schema_features: dict[str, Any]
    value_features: dict[str, Any]
    treatment_support: dict[str, Any]
    controls: dict[str, Any]
    difficulty: dict[str, Any]
    quality_status: Literal["retained"] = "retained"


class FullStatisticsManifest(StatisticsModel):
    release_id: str
    release_status: Literal["draft", "frozen"]
    release_manifest_hash: str
    canonical_artifact_hashes: dict[str, str]
    provisional: bool
    blockers: list[str]
    generated_at_utc: str
    code_commit: str | None
    code_dirty: bool | None
    config_hash: str
    logical_instances: int = Field(ge=0)
    files: dict[str, str]


class CubeStatisticsManifest(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_assignment=True)
    statistics_version: Literal["mol-cube-statistics-v0.1"] = CUBE_STATISTICS_VERSION
    release_id: str
    release_status: Literal["engineering-draft", "frozen", "stale"]
    release_manifest_hash: str
    upstream_full_statistics_manifest_hash: str
    canonical_artifact_hashes: dict[str, str]
    provisional: bool
    non_claim_bearing: bool
    blockers: list[str]
    generated_at_utc: str
    code_commit: str | None
    code_dirty: bool | None
    config_hash: str
    logical_instances: int = Field(ge=0)
    realizations: int = Field(ge=0)
    candidates: int = Field(ge=0)
    files: dict[str, str]
