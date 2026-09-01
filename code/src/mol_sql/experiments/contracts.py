"""Versioned records for reproducible MoL-SQL experiments."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import Field

from mol_sql.contracts.models import ContractModel


EXPERIMENT_PROTOCOL_VERSION = "mol-sql-experiment-v0.1"


class PromptRecord(ContractModel):
    experiment_protocol_version: Literal["mol-sql-experiment-v0.1"] = (
        EXPERIMENT_PROTOCOL_VERSION
    )
    instance_id: str
    logical_id: str
    realization_id: str
    source_family: str
    configuration: str
    question_id: int = Field(ge=0)
    database_id: str
    database_path: str
    question: str
    gold_sql: str
    difficulty: str
    method: Literal["direct_zs"] = "direct_zs"
    prompt_template_version: str
    prompt: str
    prompt_sha256: str
    prompt_characters: int = Field(ge=0)
    sample_rows_per_table: int = Field(ge=0)


class PredictionRecord(ContractModel):
    experiment_protocol_version: Literal["mol-sql-experiment-v0.1"] = (
        EXPERIMENT_PROTOCOL_VERSION
    )
    instance_id: str
    model: str
    status: Literal["success", "api_error", "empty_response", "parse_error"]
    prediction_sql: str | None = None
    raw_response: str | None = None
    error_type: str | None = None
    error_message: str | None = None
    attempts: int = Field(ge=1)
    latency_seconds: float = Field(ge=0)
    prompt_tokens: int | None = Field(default=None, ge=0)
    completion_tokens: int | None = Field(default=None, ge=0)
    total_tokens: int | None = Field(default=None, ge=0)
    finished_at: str


class EvaluationRecord(ContractModel):
    experiment_protocol_version: Literal["mol-sql-experiment-v0.1"] = (
        EXPERIMENT_PROTOCOL_VERSION
    )
    instance_id: str
    status: Literal[
        "correct",
        "wrong_result",
        "prediction_missing",
        "invalid_sql",
        "execution_error",
        "timeout",
        "gold_error",
    ]
    execution_match: int = Field(ge=0, le=1)
    error_message: str | None = None
    latency_seconds: float = Field(ge=0)


class RunManifest(ContractModel):
    experiment_protocol_version: Literal["mol-sql-experiment-v0.1"] = (
        EXPERIMENT_PROTOCOL_VERSION
    )
    run_id: str
    release: str
    method: Literal["direct_zs"] = "direct_zs"
    model: str
    api_base: str | None
    sources: list[str]
    cells: list[str]
    stages: list[str]
    prompt_template_version: str
    sample_rows_per_table: int
    candidate_budget: Literal[1] = 1
    temperature: float
    max_tokens: int
    workers: int
    max_retries: int
    started_at: str
    finished_at: str | None = None
    status: Literal["running", "completed", "completed_with_errors", "failed"]
    counts: dict[str, int] = Field(default_factory=dict)
    outputs: dict[str, str] = Field(default_factory=dict)
    notes: dict[str, Any] = Field(default_factory=dict)
