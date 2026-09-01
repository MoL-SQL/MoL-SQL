"""Import aligned legacy Direct-ZS text predictions into formal JSONL records."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from mol_sql.experiments.contracts import PredictionRecord, PromptRecord


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _load_prompts(path: Path) -> list[PromptRecord]:
    records = []
    with path.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, 1):
            if not line.strip():
                continue
            try:
                records.append(PromptRecord.model_validate_json(line))
            except Exception as exc:
                raise ValueError(f"{path}:{line_number}: invalid prompt record") from exc
    return records


def _write_predictions(path: Path, records: list[PredictionRecord]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8") as file:
        for record in records:
            file.write(
                json.dumps(
                    record.model_dump(mode="json"),
                    ensure_ascii=False,
                    sort_keys=True,
                )
                + "\n"
            )
    temporary.replace(path)


def import_legacy_direct_zs(
    *,
    legacy_root: Path,
    output_root: Path,
    model: str,
    overwrite: bool = False,
) -> dict[str, int]:
    """Import all legacy cells whose formal prompt records already exist."""
    if not legacy_root.is_dir():
        raise FileNotFoundError(legacy_root)
    model_root = output_root / model
    counts = {
        "cells": 0,
        "legacy_rows": 0,
        "success": 0,
        "failed": 0,
        "missing": 0,
    }
    for legacy_prompts_path in sorted(legacy_root.glob("*/*/prompts.json")):
        source = legacy_prompts_path.parent.parent.name
        cell = legacy_prompts_path.parent.name
        legacy_predictions_path = legacy_prompts_path.parent / "predictions.txt"
        prompts_path = model_root / source / cell / "prompts.jsonl"
        predictions_path = model_root / source / cell / "predictions.jsonl"
        if not prompts_path.is_file():
            raise FileNotFoundError(
                f"Generate formal prompts before importing legacy results: {prompts_path}"
            )
        if predictions_path.exists() and not overwrite:
            raise FileExistsError(
                f"Target already exists: {predictions_path}; pass overwrite=True"
            )
        legacy_prompts = json.loads(legacy_prompts_path.read_text(encoding="utf-8"))
        prompts = _load_prompts(prompts_path)
        if len(legacy_prompts) != len(prompts):
            raise ValueError(
                f"Prompt count mismatch for {source}/{cell}: "
                f"legacy={len(legacy_prompts)} formal={len(prompts)}"
            )
        for index, (legacy, formal) in enumerate(zip(legacy_prompts, prompts)):
            if legacy.get("prompt") != formal.prompt:
                raise ValueError(
                    f"Prompt mismatch for {source}/{cell} row {index}; import refused"
                )
            if str(legacy.get("realization_id")) != formal.realization_id:
                raise ValueError(
                    f"Realization mismatch for {source}/{cell} row {index}; import refused"
                )
        lines = (
            legacy_predictions_path.read_text(encoding="utf-8").splitlines()
            if legacy_predictions_path.is_file()
            else []
        )
        if len(lines) > len(prompts):
            raise ValueError(
                f"Too many predictions for {source}/{cell}: {len(lines)} > {len(prompts)}"
            )
        records = []
        for prompt, prediction in zip(prompts, lines):
            is_error = prediction.startswith(("-- Error:", "[Error"))
            records.append(
                PredictionRecord(
                    instance_id=prompt.instance_id,
                    model=model,
                    status=(
                        "empty_response"
                        if is_error and "empty response" in prediction.lower()
                        else "api_error"
                        if is_error
                        else "success"
                    ),
                    prediction_sql=None if is_error else prediction,
                    raw_response=None,
                    error_type="legacy_import" if is_error else None,
                    error_message=prediction if is_error else None,
                    attempts=1,
                    latency_seconds=0.0,
                    finished_at=_now(),
                )
            )
        _write_predictions(predictions_path, records)
        counts["cells"] += 1
        counts["legacy_rows"] += len(records)
        counts["success"] += sum(record.status == "success" for record in records)
        counts["failed"] += sum(record.status != "success" for record in records)
        counts["missing"] += len(prompts) - len(records)
    return counts
