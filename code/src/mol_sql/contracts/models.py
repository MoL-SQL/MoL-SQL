"""Strict versioned records for MoL-Full construction and audit."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

CONTRACT_VERSION = "mol-sql-contract-v0.1"
Language = Literal["en", "zh"]
ReleaseStatus = Literal["draft", "frozen"]
AuditStatus = Literal["pass", "fail", "warning", "not_run", "not_applicable"]


class ContractModel(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_assignment=True)
    contract_version: Literal["mol-sql-contract-v0.1"] = CONTRACT_VERSION


class SourceRecord(ContractModel):
    source_family: str
    release_role: Literal["core", "extension"]
    upstream_version: str | None
    source_url: str | None
    snapshot_date: str | None
    license_spdx: str | None
    license_evidence_url: str | None
    redistribution_policy: Literal[
        "redistributable_with_attribution",
        "upstream_download_only",
        "unresolved",
    ] = "unresolved"
    license_notes: str | None = None
    native_language: Language
    split: str
    seed_root: str
    replacement_proposals: str | None = None
    replacement_map: str | None = None
    fixed_points: str | None = None
    execution_repairs: str | None = None
    execution_adjudications: str | None = None
    input_hashes: dict[str, str]
    provenance_complete: bool
    blockers: list[str] = Field(default_factory=list)


class LogicalInstance(ContractModel):
    logical_id: str
    source_family: str
    source_sample_key: str
    legacy_index: int = Field(ge=0)
    database_id: str
    split: str
    canonical_question: str
    canonical_sql: str
    answer_semantics: Literal["ordered", "multiset"]
    difficulty: str | None = None
    phenomena: list[str] = Field(default_factory=list)
    provenance_refs: list[str]
    input_hashes: dict[str, str]


class Realization(ContractModel):
    realization_id: str
    logical_id: str
    source_family: str
    source_sample_key: str
    configuration: Literal[
        "Q_en--S_en--V_en",
        "Q_zh--S_en--V_en",
        "Q_en--S_zh--V_zh",
        "Q_zh--S_zh--V_zh",
    ]
    question_language: Language
    schema_language: Language
    value_language: Language
    database_id: str
    split: str
    question: str
    gold_sql: str
    dataset_path: str
    tables_path: str
    database_path: str | None
    replacement_proposals: str | None = None
    replacement_map: str | None = None
    fixed_points: str | None = None
    execution_repairs: str | None = None
    execution_adjudications: str | None = None
    input_hashes: dict[str, str]

    @model_validator(mode="after")
    def configuration_matches_languages(self) -> "Realization":
        expected = (
            f"Q_{self.question_language}--S_{self.schema_language}"
            f"--V_{self.value_language}"
        )
        if self.configuration != expected:
            raise ValueError(
                f"configuration {self.configuration!r} does not match {expected!r}"
            )
        if self.schema_language != self.value_language:
            raise ValueError("MoL-Full requires coupled schema/value languages")
        return self


class AuditRecord(ContractModel):
    audit_id: str
    subject_type: Literal["source", "logical_instance", "realization", "database"]
    subject_id: str
    gate: str
    status: AuditStatus
    error_codes: list[str] = Field(default_factory=list)
    details: dict[str, Any] = Field(default_factory=dict)
    artifact_refs: list[str] = Field(default_factory=list)


class HumanAuditItem(ContractModel):
    audit_item_id: str
    logical_id: str
    source_family: str
    stratum: str
    questions: dict[str, str]
    sql: dict[str, str]
    criteria: list[
        Literal["question_fidelity", "naturalness", "entity_value_grounding"]
    ]
    reviewer_1: dict[str, Any] | None = None
    reviewer_2: dict[str, Any] | None = None
    adjudication: dict[str, Any] | None = None


class ReleaseManifest(ContractModel):
    release_id: str
    release_kind: Literal["mol-full"]
    status: ReleaseStatus
    source_families: list[str]
    logical_instances: int = Field(ge=0)
    realizations: int = Field(ge=0)
    configurations: list[str]
    source_counts: dict[str, int]
    file_hashes: dict[str, str]
    audit_summary: dict[str, dict[str, int]]
    blockers: list[str] = Field(default_factory=list)
    build_config_hash: str
    bird_format_version: str | None = None
    bird_format_manifest: str | None = None
    bird_format_manifest_hash: str | None = None
    bird_format_packaging_mode: Literal["copy", "hardlink", "symlink"] | None = None
    bird_format_distribution_scope: Literal[
        "redistributable_with_attribution",
        "upstream_required",
        "local_only",
    ] | None = None

    @model_validator(mode="after")
    def frozen_has_no_blockers(self) -> "ReleaseManifest":
        if self.status == "frozen" and self.blockers:
            raise ValueError("a frozen release cannot contain blockers")
        if self.realizations != 4 * self.logical_instances:
            raise ValueError("MoL-Full must contain exactly four realizations per logical instance")
        return self
