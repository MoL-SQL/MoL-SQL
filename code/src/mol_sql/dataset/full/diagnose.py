"""Detailed, reproducible diagnostics for aggregate execution failures."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from mol_sql.contracts.io import write_jsonl
from mol_sql.dataset.adapters import adapter_for, load_source_specs
from mol_sql.dataset.audit.automatic import (
    _execute,
    _normalized_rows,
    _sql,
    _value_canonicalizer,
)


def _preview(rows: list[tuple[Any, ...]], limit: int = 10) -> list[list[Any]]:
    return [
        [
            value
            if value is None or isinstance(value, (int, float, str, bool))
            else repr(value)
            for value in row
        ]
        for row in rows[:limit]
    ]


def diagnose_execution_failures(
    *,
    repo_root: Path,
    source_config: Path,
    failures_path: Path,
    output_path: Path,
    timeout_seconds: float,
) -> int:
    """Re-execute failed samples and retain SQL plus bounded result previews."""

    repo_root = repo_root.resolve()
    source_config = (
        source_config
        if source_config.is_absolute()
        else repo_root / source_config
    )
    failures_path = (
        failures_path
        if failures_path.is_absolute()
        else repo_root / failures_path
    )
    specs = load_source_specs(source_config)
    adapted = {
        spec.source_family: adapter_for(spec.source_family, repo_root, spec).load()
        for spec in specs
    }
    failures = [
        json.loads(line)
        for line in failures_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    diagnostics: list[dict[str, Any]] = []
    for failure in failures:
        source = adapted[str(failure["source_family"])]
        legacy_index = int(failure["legacy_index"])
        sample = next(
            (
                item
                for item in source.samples
                if item.legacy_index == legacy_index
            ),
            None,
        )
        if sample is None:
            raise ValueError(
                f"{source.spec.source_family}: retained sample not found "
                f"for legacy index {legacy_index}"
            )
        en_sql = source.execution_sql(
            _sql(source, sample.rows["Q_en--S_en--V_en"])
        )
        zh_sql = source.execution_sql(
            _sql(source, sample.rows["Q_en--S_zh--V_zh"])
        )
        row: dict[str, Any] = {
            **failure,
            "question_en": sample.rows["Q_en--S_en--V_en"].get("question"),
            "question_zh": sample.rows["Q_zh--S_zh--V_zh"].get("question"),
            "sql_en": en_sql,
            "sql_zh": zh_sql,
        }
        mapping = _value_canonicalizer(source).get(sample.database_id, {})
        for language, sql in (("en", en_sql), ("zh", zh_sql)):
            database = source.database_paths[(language, sample.database_id)]
            if database is None:
                row[f"{language}_error"] = "missing_database_artifact"
                continue
            try:
                result = _execute(database, sql, timeout_seconds)
                normalized = _normalized_rows(result, mapping)
                row[f"{language}_row_count"] = len(result)
                row[f"{language}_preview"] = _preview(result)
                row[f"{language}_normalized_preview"] = _preview(normalized)
            except Exception as exc:
                row[f"{language}_error"] = f"{type(exc).__name__}:{exc}"
        diagnostics.append(row)
    return write_jsonl(output_path, diagnostics)
