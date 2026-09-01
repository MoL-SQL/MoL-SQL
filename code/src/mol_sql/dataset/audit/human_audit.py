"""Deterministic human-audit queue and completed-review summary."""

from __future__ import annotations

from collections import Counter
from typing import Iterable

from mol_sql.contracts.ids import stable_id
from mol_sql.contracts.models import HumanAuditItem
from mol_sql.dataset.adapters.base import AdaptedSource, FULL_CONFIGURATIONS


def build_human_audit_queue(
    sources: Iterable[AdaptedSource],
    *,
    per_source: int,
) -> list[HumanAuditItem]:
    queue: list[HumanAuditItem] = []
    for adapted in sources:
        ranked = sorted(
            adapted.samples,
            key=lambda sample: stable_id(
                "rank",
                adapted.spec.source_family,
                sample.source_sample_key,
                length=64,
            ),
        )
        for sample in ranked[: min(per_source, len(ranked))]:
            logical_id = stable_id(
                "logical",
                adapted.spec.source_family,
                adapted.spec.upstream_version or "unfrozen",
                adapted.spec.split,
                sample.database_id,
                sample.source_sample_key,
            )
            queue.append(
                HumanAuditItem(
                    audit_item_id=stable_id("human", logical_id),
                    logical_id=logical_id,
                    source_family=adapted.spec.source_family,
                    stratum=sample.difficulty or "unlabelled",
                    questions={
                        configuration: _question(sample.rows[configuration])
                        for configuration in FULL_CONFIGURATIONS
                    },
                    sql={
                        configuration: _sql(adapted, sample.rows[configuration])
                        for configuration in FULL_CONFIGURATIONS
                    },
                    criteria=[
                        "question_fidelity",
                        "naturalness",
                        "entity_value_grounding",
                    ],
                )
            )
    return queue


def summarize_human_audit(items: Iterable[HumanAuditItem]) -> dict:
    """Summarize only genuinely completed two-reviewer items."""

    rows = list(items)
    completed = [
        item
        for item in rows
        if item.reviewer_1 is not None
        and item.reviewer_2 is not None
        and all(criterion in item.reviewer_1 for criterion in item.criteria)
        and all(criterion in item.reviewer_2 for criterion in item.criteria)
    ]
    adjudicated = [item for item in completed if item.adjudication is not None]
    failed = [
        item
        for item in adjudicated
        if item.adjudication.get("status") != "pass"
    ]
    agreement_counts: Counter[str] = Counter()
    for item in completed:
        for criterion in item.criteria:
            left = item.reviewer_1.get(criterion)
            right = item.reviewer_2.get(criterion)
            agreement_counts[criterion] += int(left == right)
    return {
        "queued": len(rows),
        "completed_by_two_reviewers": len(completed),
        "adjudicated": len(adjudicated),
        "failed_after_adjudication": len(failed),
        "agreement": {
            criterion: (
                agreement_counts[criterion] / len(completed) if completed else None
            )
            for criterion in (
                "question_fidelity",
                "naturalness",
                "entity_value_grounding",
            )
        },
        "ready": bool(rows) and len(adjudicated) == len(rows),
        "ready_for_freeze": (
            bool(rows) and len(adjudicated) == len(rows) and not failed
        ),
    }


def _question(row: dict) -> str:
    value = row.get("question")
    return value.strip() if isinstance(value, str) else ""


def _sql(adapted: AdaptedSource, row: dict) -> str:
    for field in adapted.spec.sql_fields:
        value = row.get(field)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""
