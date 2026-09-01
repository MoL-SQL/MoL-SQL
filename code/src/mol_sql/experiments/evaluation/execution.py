"""SQLite execution-match evaluator compatible with the legacy Direct-ZS runs."""

from __future__ import annotations

import sqlite3
import time
from contextlib import closing
from pathlib import Path

from mol_sql.experiments.contracts import EvaluationRecord


def _execute(database_path: Path, sql: str, timeout_seconds: float) -> list[tuple]:
    started = time.monotonic()
    uri = f"file:{database_path.resolve()}?mode=ro"
    with closing(sqlite3.connect(uri, uri=True)) as connection:
        connection.set_progress_handler(
            lambda: int(time.monotonic() - started > timeout_seconds), 10_000
        )
        cursor = connection.execute(sql)
        if cursor.description is None:
            raise sqlite3.OperationalError("query returned no result set")
        return cursor.fetchall()


def evaluate_sql(
    *,
    instance_id: str,
    database_path: Path,
    prediction_sql: str | None,
    gold_sql: str,
    timeout_seconds: float,
) -> EvaluationRecord:
    started = time.monotonic()
    if not prediction_sql:
        return EvaluationRecord(
            instance_id=instance_id,
            status="prediction_missing",
            execution_match=0,
            error_message="no successful prediction",
            latency_seconds=time.monotonic() - started,
        )
    try:
        predicted = _execute(database_path, prediction_sql, timeout_seconds)
    except sqlite3.Error as exc:
        status = "timeout" if str(exc) == "interrupted" else "invalid_sql"
        return EvaluationRecord(
            instance_id=instance_id,
            status=status,
            execution_match=0,
            error_message=str(exc),
            latency_seconds=time.monotonic() - started,
        )
    try:
        gold = _execute(database_path, gold_sql, timeout_seconds)
    except sqlite3.Error as exc:
        return EvaluationRecord(
            instance_id=instance_id,
            status="gold_error",
            execution_match=0,
            error_message=str(exc),
            latency_seconds=time.monotonic() - started,
        )
    matched = set(predicted) == set(gold)
    return EvaluationRecord(
        instance_id=instance_id,
        status="correct" if matched else "wrong_result",
        execution_match=int(matched),
        error_message=None if matched else "execution result mismatch",
        latency_seconds=time.monotonic() - started,
    )
