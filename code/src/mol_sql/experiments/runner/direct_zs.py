"""Manifest-driven Direct-ZS runner for MoL-Cube BIRD-format packages."""

from __future__ import annotations

import json
import os
import re
import statistics
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Iterable, Literal

from mol_sql.contracts.io import load_json, write_json
from mol_sql.experiments.contracts import (
    EvaluationRecord,
    PredictionRecord,
    PromptRecord,
    RunManifest,
)
from mol_sql.experiments.evaluation.execution import evaluate_sql
from mol_sql.experiments.methods.direct_zs import (
    PROMPT_TEMPLATE_VERSION,
    build_prompt,
    extract_sql,
    prompt_sha256,
)
from mol_sql.experiments.runner.openai_compatible import (
    ChatRequestError,
    chat_completion,
)
from mol_sql.experiments.runner.progress import ProgressTracker


Stage = Literal["prompt", "infer", "eval"]
STAGES: tuple[Stage, ...] = ("prompt", "infer", "eval")


@dataclass(frozen=True)
class DirectZSOptions:
    repo_root: Path
    cube_root: Path
    output_root: Path
    model: str
    api_profile: Literal["dashscope", "openai", "hkustgz"] = "dashscope"
    sources: tuple[str, ...] | None = None
    cells: tuple[str, ...] | None = None
    stages: tuple[Stage, ...] = STAGES
    limit_ids: int | None = None
    sample_rows_per_table: int = 3
    workers: int = 2
    temperature: float = 0.0
    max_tokens: int = 4096
    request_timeout_seconds: float = 180.0
    max_retries: int = 6
    retry_backoff_seconds: float = 15.0
    evaluation_timeout_seconds: float = 30.0
    dry_run: bool = False


@dataclass(frozen=True)
class CellPackage:
    source: str
    cell: str
    root: Path
    questions: Path
    database_root: Path


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9._-]+", "-", value.strip()).strip("-")
    return slug or "model"


def _resolve(repo_root: Path, path: Path) -> Path:
    return path if path.is_absolute() else repo_root / path


def _discover_packages(
    cube_root: Path,
    sources: tuple[str, ...] | None,
    cells: tuple[str, ...] | None,
) -> list[CellPackage]:
    bird_root = cube_root / "bird_format"
    if not bird_root.is_dir():
        raise FileNotFoundError(f"BIRD-format Cube directory not found: {bird_root}")
    available = sorted(path.name for path in bird_root.iterdir() if path.is_dir())
    selected = available if sources is None else list(sources)
    missing = sorted(set(selected) - set(available))
    if missing:
        raise ValueError(f"Unknown Cube sources: {missing}; available={available}")
    packages = []
    for source in selected:
        available_cells = sorted(
            path.name for path in (bird_root / source).iterdir() if path.is_dir()
        )
        selected_cells = available_cells if cells is None else list(cells)
        missing_cells = sorted(set(selected_cells) - set(available_cells))
        if missing_cells:
            raise ValueError(
                f"Unknown Cube cells for {source}: {missing_cells}; "
                f"available={available_cells}"
            )
        for root in sorted((bird_root / source).iterdir()):
            if not root.is_dir():
                continue
            if root.name not in selected_cells:
                continue
            questions = root / "dev.json"
            database_root = root / "database"
            if not questions.is_file() or not database_root.is_dir():
                raise FileNotFoundError(f"Incomplete BIRD package: {root}")
            packages.append(
                CellPackage(
                    source=source,
                    cell=root.name,
                    root=root,
                    questions=questions,
                    database_root=database_root,
                )
            )
    return packages


def _load_rows(package: CellPackage, limit_ids: int | None) -> list[dict]:
    rows = load_json(package.questions)
    if not isinstance(rows, list) or not all(isinstance(row, dict) for row in rows):
        raise ValueError(f"{package.questions}: expected a JSON list of objects")
    return rows[:limit_ids] if limit_ids is not None else rows


def _validate_alignment(packages: list[CellPackage], limit_ids: int | None) -> None:
    by_source: dict[str, list[list[str]]] = {}
    for package in packages:
        logical_ids = [str(row["logical_id"]) for row in _load_rows(package, limit_ids)]
        by_source.setdefault(package.source, []).append(logical_ids)
    for source, cells in by_source.items():
        reference = cells[0]
        if any(cell != reference for cell in cells[1:]):
            raise ValueError(f"Logical IDs are not aligned across Cube cells for {source}")


def _write_jsonl(path: Path, records: Iterable[object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8") as file:
        for record in records:
            payload = record.model_dump(mode="json") if hasattr(record, "model_dump") else record
            file.write(json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n")
    temporary.replace(path)


def _append_jsonl(path: Path, record: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = record.model_dump(mode="json") if hasattr(record, "model_dump") else record
    with path.open("a", encoding="utf-8") as file:
        file.write(json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n")
        file.flush()
        os.fsync(file.fileno())


def _load_latest_predictions(path: Path) -> dict[str, PredictionRecord]:
    records: dict[str, PredictionRecord] = {}
    if not path.is_file():
        return records
    with path.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, 1):
            if not line.strip():
                continue
            try:
                record = PredictionRecord.model_validate_json(line)
            except Exception as exc:
                raise ValueError(f"{path}:{line_number}: invalid prediction record") from exc
            records[record.instance_id] = record
    return records


_REUSABLE_EVAL_STATUSES = frozenset({"correct", "wrong_result"})


def _load_latest_evaluations(path: Path) -> dict[str, EvaluationRecord]:
    records: dict[str, EvaluationRecord] = {}
    if not path.is_file():
        return records
    with path.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, 1):
            if not line.strip():
                continue
            try:
                record = EvaluationRecord.model_validate_json(line)
            except Exception as exc:
                raise ValueError(f"{path}:{line_number}: invalid evaluation record") from exc
            records[record.instance_id] = record
    return records


def _is_reusable_evaluation(record: EvaluationRecord | None) -> bool:
    return record is not None and record.status in _REUSABLE_EVAL_STATUSES


def _prompt_records(package: CellPackage, options: DirectZSOptions) -> list[PromptRecord]:
    records = []
    for row in _load_rows(package, options.limit_ids):
        database_id = str(row["db_id"])
        database_path = package.database_root / database_id / f"{database_id}.sqlite"
        if not database_path.is_file():
            raise FileNotFoundError(database_path)
        try:
            prompt = build_prompt(
                str(row["question"]),
                database_path,
                sample_rows_per_table=options.sample_rows_per_table,
            )
        except Exception as exc:
            raise RuntimeError(
                f"Prompt generation failed for {package.source}/{package.cell} "
                f"question_id={row.get('question_id')} db_id={database_id}: {exc}"
            ) from exc
        records.append(
            PromptRecord(
                instance_id=str(row["realization_id"]),
                logical_id=str(row["logical_id"]),
                realization_id=str(row["realization_id"]),
                source_family=package.source,
                configuration=package.cell,
                question_id=int(row["question_id"]),
                database_id=database_id,
                database_path=str(database_path.resolve()),
                question=str(row["question"]),
                gold_sql=str(row["SQL"]),
                difficulty=str(row.get("difficulty", "simple")),
                prompt_template_version=PROMPT_TEMPLATE_VERSION,
                prompt=prompt,
                prompt_sha256=prompt_sha256(prompt),
                prompt_characters=len(prompt),
                sample_rows_per_table=options.sample_rows_per_table,
            )
        )
    return records


def _api_credentials(profile: str) -> tuple[str, str]:
    if profile == "hkustgz":
        key = os.environ.get("HKUSTGZ_API_KEY", "")
        base = os.environ.get("HKUSTGZ_BASE_URL", "")
    else:
        key = os.environ.get("OPENAI_API_KEY", "")
        base = os.environ.get("OPENAI_BASE_URL", "")
    missing = []
    if not key:
        missing.append("API key")
    if not base:
        missing.append("API base URL")
    if missing:
        raise RuntimeError(f"Missing {' and '.join(missing)} for profile {profile}")
    return key, base


def _infer_one(
    prompt_record: PromptRecord,
    options: DirectZSOptions,
    api_key: str,
    api_base: str,
) -> PredictionRecord:
    try:
        result = chat_completion(
            api_key=api_key,
            api_base=api_base,
            model=options.model,
            prompt=prompt_record.prompt,
            temperature=options.temperature,
            max_tokens=options.max_tokens,
            timeout_seconds=options.request_timeout_seconds,
            max_retries=options.max_retries,
            retry_backoff_seconds=options.retry_backoff_seconds,
        )
        sql = extract_sql(result.content)
        return PredictionRecord(
            instance_id=prompt_record.instance_id,
            model=options.model,
            status="success" if sql else "parse_error",
            prediction_sql=sql,
            raw_response=result.content,
            error_type=None if sql else "parse_error",
            error_message=None if sql else "response contained no SQL",
            attempts=result.attempts,
            latency_seconds=result.latency_seconds,
            prompt_tokens=result.usage["prompt_tokens"],
            completion_tokens=result.usage["completion_tokens"],
            total_tokens=result.usage["total_tokens"],
            finished_at=_now(),
        )
    except ChatRequestError as exc:
        empty = "empty response" in str(exc).lower()
        return PredictionRecord(
            instance_id=prompt_record.instance_id,
            model=options.model,
            status="empty_response" if empty else "api_error",
            error_type="empty_response" if empty else "api_error",
            error_message=str(exc),
            attempts=exc.attempts,
            latency_seconds=exc.latency_seconds,
            finished_at=_now(),
        )


def _run_inference(
    prompts: list[PromptRecord],
    predictions_path: Path,
    options: DirectZSOptions,
    on_result: Callable[[PredictionRecord], None] | None = None,
) -> dict[str, PredictionRecord]:
    current = _load_latest_predictions(predictions_path)
    pending = [
        prompt for prompt in prompts if current.get(prompt.instance_id, None) is None
        or current[prompt.instance_id].status != "success"
    ]
    if not pending:
        return current
    api_key, api_base = _api_credentials(options.api_profile)
    with ThreadPoolExecutor(max_workers=options.workers) as executor:
        futures = {
            executor.submit(_infer_one, prompt, options, api_key, api_base): prompt
            for prompt in pending
        }
        for future in as_completed(futures):
            record = future.result()
            current[record.instance_id] = record
            _append_jsonl(predictions_path, record)
            if on_result is not None:
                on_result(record)
    ordered = [current[prompt.instance_id] for prompt in prompts if prompt.instance_id in current]
    _write_jsonl(predictions_path, ordered)
    return current


def _run_evaluation(
    prompts: list[PromptRecord],
    predictions: dict[str, PredictionRecord],
    evaluation_path: Path,
    options: DirectZSOptions,
    on_result: Callable[[EvaluationRecord], None] | None = None,
) -> list[EvaluationRecord]:
    current = _load_latest_evaluations(evaluation_path)
    pending = [
        prompt
        for prompt in prompts
        if not _is_reusable_evaluation(current.get(prompt.instance_id))
    ]
    if pending:

        def task(prompt: PromptRecord) -> EvaluationRecord:
            prediction = predictions.get(prompt.instance_id)
            sql = (
                prediction.prediction_sql
                if prediction and prediction.status == "success"
                else None
            )
            return evaluate_sql(
                instance_id=prompt.instance_id,
                database_path=Path(prompt.database_path),
                prediction_sql=sql,
                gold_sql=prompt.gold_sql,
                timeout_seconds=options.evaluation_timeout_seconds,
            )

        with ThreadPoolExecutor(max_workers=options.workers) as executor:
            futures = {
                executor.submit(task, prompt): prompt.instance_id for prompt in pending
            }
            for future in as_completed(futures):
                record = future.result()
                current[record.instance_id] = record
                _append_jsonl(evaluation_path, record)
                if on_result is not None:
                    on_result(record)
    ordered = [
        current[prompt.instance_id]
        for prompt in prompts
        if prompt.instance_id in current
    ]
    _write_jsonl(evaluation_path, ordered)
    return ordered


def _initial_inference_successes(packages: list[CellPackage], run_root: Path) -> int:
    successes = 0
    for package in packages:
        predictions_path = run_root / package.source / package.cell / "predictions.jsonl"
        successes += sum(
            record.status == "success"
            for record in _load_latest_predictions(predictions_path).values()
        )
    return successes


def _initial_evaluation_progress(
    packages: list[CellPackage], run_root: Path
) -> tuple[int, int]:
    completed = 0
    correct = 0
    for package in packages:
        evaluation_path = run_root / package.source / package.cell / "evaluation.jsonl"
        for record in _load_latest_evaluations(evaluation_path).values():
            if not _is_reusable_evaluation(record):
                continue
            completed += 1
            correct += record.execution_match
    return completed, correct


def _initial_inference_rate(
    packages: list[CellPackage], run_root: Path, workers: int
) -> float | None:
    latencies = []
    for package in packages:
        predictions_path = run_root / package.source / package.cell / "predictions.jsonl"
        latencies.extend(
            record.latency_seconds
            for record in _load_latest_predictions(predictions_path).values()
            if record.status == "success" and record.latency_seconds > 0
        )
    if not latencies:
        return None
    return workers / statistics.median(latencies)


def run_direct_zs(options: DirectZSOptions) -> RunManifest:
    if options.limit_ids is not None and options.limit_ids <= 0:
        raise ValueError("limit_ids must be positive")
    if options.sample_rows_per_table < 0:
        raise ValueError("sample_rows_per_table must be non-negative")
    cube_root = _resolve(options.repo_root, options.cube_root).resolve()
    output_root = _resolve(options.repo_root, options.output_root).resolve()
    packages = _discover_packages(cube_root, options.sources, options.cells)
    _validate_alignment(packages, options.limit_ids)
    run_root = output_root / _slugify(options.model)
    expected_total = sum(len(_load_rows(package, options.limit_ids)) for package in packages)
    api_base = None
    if "infer" in options.stages and not options.dry_run:
        _, api_base = _api_credentials(options.api_profile)
    manifest = RunManifest(
        run_id=f"direct-zs-{_slugify(options.model)}",
        release=str(cube_root),
        model=options.model,
        api_base=api_base,
        sources=sorted({package.source for package in packages}),
        cells=sorted({package.cell for package in packages}),
        stages=list(options.stages),
        prompt_template_version=PROMPT_TEMPLATE_VERSION,
        sample_rows_per_table=options.sample_rows_per_table,
        temperature=options.temperature,
        max_tokens=options.max_tokens,
        workers=options.workers,
        max_retries=options.max_retries,
        started_at=_now(),
        status="running",
        notes={
            "schema_visibility": "full",
            "few_shot_examples": 0,
            "evidence_visible": False,
            "system_message": False,
            "question_translation": False,
            "thinking_disabled_for_qwen3": True,
            "response_parser": "bare_sql_or_label_or_fence_or_xml",
            "evaluation": "SQLite set execution equivalence",
        },
    )
    manifest_path = run_root / "run_manifest.json"
    if not options.dry_run:
        write_json(manifest_path, manifest.model_dump(mode="json"))
    initial_inference_successes = (
        _initial_inference_successes(packages, run_root)
        if "infer" in options.stages and not options.dry_run
        else 0
    )
    initial_evaluation_completed = 0
    initial_evaluation_correct = 0
    if "eval" in options.stages and not options.dry_run:
        initial_evaluation_completed, initial_evaluation_correct = (
            _initial_evaluation_progress(packages, run_root)
        )
    initial_inference_rate = (
        _initial_inference_rate(packages, run_root, options.workers)
        if "infer" in options.stages and not options.dry_run
        else None
    )
    initial_completed: dict[str, int] = {}
    if "infer" in options.stages:
        initial_completed["infer"] = initial_inference_successes
    if "eval" in options.stages:
        initial_completed["eval"] = initial_evaluation_completed
    tracker = (
        ProgressTracker(
            run_root=run_root,
            run_id=manifest.run_id,
            model=options.model,
            stage_totals={stage: expected_total for stage in options.stages},
            initial_completed=initial_completed,
            initial_correct=initial_evaluation_correct,
            initial_rates_per_second={"infer": initial_inference_rate}
            if initial_inference_rate is not None
            else None,
        )
        if not options.dry_run
        else None
    )
    total_prompts = total_success = total_errors = total_evaluated = total_correct = 0
    try:
        for package in packages:
            if tracker is not None:
                tracker.begin("prepare", package.source, package.cell)
            cell_root = run_root / package.source / package.cell
            prompts_path = cell_root / "prompts.jsonl"
            predictions_path = cell_root / "predictions.jsonl"
            evaluation_path = cell_root / "evaluation.jsonl"
            prompts = _prompt_records(package, options)
            total_prompts += len(prompts)
            if "prompt" in options.stages and not options.dry_run:
                if tracker is not None:
                    tracker.begin("prompt", package.source, package.cell)
                _write_jsonl(prompts_path, prompts)
                if tracker is not None:
                    tracker.advance("prompt", len(prompts))
            predictions: dict[str, PredictionRecord] = {}
            if "infer" in options.stages and not options.dry_run:
                if tracker is not None:
                    tracker.begin("infer", package.source, package.cell)
                predictions = _run_inference(
                    prompts,
                    predictions_path,
                    options,
                    on_result=(
                        lambda record: tracker.advance(
                            "infer",
                            1,
                            successful=int(record.status == "success"),
                            failed=int(record.status != "success"),
                        )
                        if tracker is not None
                        else None
                    ),
                )
            elif predictions_path.is_file():
                predictions = _load_latest_predictions(predictions_path)
            total_success += sum(record.status == "success" for record in predictions.values())
            total_errors += sum(record.status != "success" for record in predictions.values())
            if "eval" in options.stages and not options.dry_run:
                if tracker is not None:
                    tracker.begin("eval", package.source, package.cell)
                evaluations = _run_evaluation(
                    prompts,
                    predictions,
                    evaluation_path,
                    options,
                    on_result=(
                        lambda record: tracker.advance(
                            "eval", 1, correct=record.execution_match
                        )
                        if tracker is not None
                        else None
                    ),
                )
                total_evaluated += len(evaluations)
                total_correct += sum(record.execution_match for record in evaluations)
            manifest.outputs[f"{package.source}/{package.cell}"] = str(cell_root)
            manifest.counts = {
                "prompts": total_prompts,
                "successful_predictions": total_success,
                "failed_predictions": total_errors,
                "evaluated": total_evaluated,
                "correct": total_correct,
            }
            if not options.dry_run:
                write_json(manifest_path, manifest.model_dump(mode="json"))
    except BaseException as exc:
        manifest.status = "failed"
        manifest.finished_at = _now()
        if not options.dry_run:
            write_json(manifest_path, manifest.model_dump(mode="json"))
        if tracker is not None:
            tracker.finish("failed", f"{type(exc).__name__}: {exc}")
        raise
    manifest.status = "completed_with_errors" if total_errors else "completed"
    manifest.finished_at = _now()
    if not options.dry_run:
        write_json(manifest_path, manifest.model_dump(mode="json"))
    if tracker is not None:
        tracker.finish(manifest.status)
    return manifest
