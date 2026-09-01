"""Versioned records for MoL-Cube construction and audit."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

CUBE_CONTRACT_VERSION = "mol-cube-contract-v0.1"
CUBE_CONFIGURATIONS = (
    "Q_en--S_en--V_en",
    "Q_en--S_en--V_zh",
    "Q_en--S_zh--V_en",
    "Q_en--S_zh--V_zh",
    "Q_zh--S_en--V_en",
    "Q_zh--S_en--V_zh",
    "Q_zh--S_zh--V_en",
    "Q_zh--S_zh--V_zh",
)
CubeConfiguration = Literal[
    "Q_en--S_en--V_en",
    "Q_en--S_en--V_zh",
    "Q_en--S_zh--V_en",
    "Q_en--S_zh--V_zh",
    "Q_zh--S_en--V_en",
    "Q_zh--S_en--V_zh",
    "Q_zh--S_zh--V_en",
    "Q_zh--S_zh--V_zh",
]


class CubeModel(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_assignment=True)
    cube_contract_version: Literal["mol-cube-contract-v0.1"] = CUBE_CONTRACT_VERSION


class CubeCandidateProfile(CubeModel):
    logical_id: str
    source_family: str
    database_id: str
    split: str
    source_sample_key: str
    legacy_index: int = Field(ge=0)
    treatment_support: dict[str, Any]
    controls: dict[str, Any]
    difficulty: dict[str, Any]
    barrier_opportunities: list[str]
    barrier_evidence: dict[str, Any]
    pending_human_annotations: list[str] = Field(default_factory=list)
    quality_status: Literal["retained"] = "retained"


class CubeMembership(CubeModel):
    logical_id: str
    source_family: str
    database_id: str
    selected: bool
    selection_rank: int | None = Field(default=None, ge=1)
    selection_reasons: list[str] = Field(default_factory=list)
    full_to_cube_weight: float | None = Field(default=None, gt=0)


class CubeRealization(CubeModel):
    realization_id: str
    logical_id: str
    source_family: str
    source_sample_key: str
    configuration: CubeConfiguration
    question_language: Literal["en", "zh"]
    schema_language: Literal["en", "zh"]
    value_language: Literal["en", "zh"]
    database_id: str
    split: str
    question: str
    gold_sql: str
    tables_path: str
    database_path: str
    database_hash: str
    construction: Literal["reuse-full", "mixed-value-materialization"]
    treatment_presence: dict[str, bool]
    upstream_realization_ids: list[str]
    replacement_map: str | None = None
    input_hashes: dict[str, str]

    @model_validator(mode="after")
    def configuration_matches_languages(self) -> "CubeRealization":
        expected = (
            f"Q_{self.question_language}--S_{self.schema_language}"
            f"--V_{self.value_language}"
        )
        if self.configuration != expected:
            raise ValueError(
                f"configuration {self.configuration!r} does not match {expected!r}"
            )
        return self


class CubeReleaseManifest(CubeModel):
    release_id: str
    release_kind: Literal["mol-cube"] = "mol-cube"
    status: Literal["engineering-draft", "frozen", "stale"]
    non_claim_bearing: bool
    upstream_full_release_id: str
    upstream_full_status: Literal["draft", "frozen"]
    upstream_full_manifest_hash: str
    upstream_full_statistics_manifest_hash: str
    upstream_full_logical_profiles_hash: str
    inherited_blockers: list[str]
    blockers: list[str]
    source_families: list[str]
    logical_instances: int = Field(ge=0)
    realizations: int = Field(ge=0)
    configurations: list[CubeConfiguration]
    source_counts: dict[str, int]
    database_counts: dict[str, int]
    sampler_config_hash: str
    sampler_seed: int
    database_packaging_mode: Literal["reflink-or-copy", "copy"]
    audit_summary: dict[str, dict[str, int]]
    quota_shortfalls: list[dict[str, Any]]
    file_hashes: dict[str, str]
    bird_format_version: str | None = None
    bird_format_manifest: str | None = None
    bird_format_manifest_hash: str | None = None
    bird_format_packaging_mode: Literal["copy", "hardlink", "symlink"] | None = None
    bird_format_distribution_scope: str | None = None

    @model_validator(mode="after")
    def validate_release_state(self) -> "CubeReleaseManifest":
        if self.realizations != 8 * self.logical_instances:
            raise ValueError("MoL-Cube must contain exactly eight realizations per logical instance")
        if self.status == "engineering-draft" and not self.non_claim_bearing:
            raise ValueError("engineering Cube must be non-claim-bearing")
        if self.status == "frozen":
            if self.non_claim_bearing:
                raise ValueError("frozen Cube cannot be non-claim-bearing")
            if self.upstream_full_status != "frozen":
                raise ValueError("frozen Cube requires a frozen upstream Full release")
            if self.blockers:
                raise ValueError("frozen Cube cannot contain blockers")
        return self
