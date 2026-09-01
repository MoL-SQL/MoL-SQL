"""Aggregate Direct-ZS MoL-Cube run metrics into reproducible report artifacts."""

from __future__ import annotations

import csv
import json
from collections import Counter
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from statistics import mean

from mol_sql.contracts.io import load_json


DEFAULT_SOURCES = ("bird", "bull", "ehrsql", "kaggledbqa", "spider")
DEFAULT_CELLS = tuple(
    f"Q_{question}--S_{schema}--V_{value}"
    for question in ("en", "zh")
    for schema in ("en", "zh")
    for value in ("en", "zh")
)
INVALID_SQL_STATUSES = frozenset({"invalid_sql", "empty_prediction"})
EXPECTED_ROWS_PER_CELL = 96


@dataclass(frozen=True)
class CubeAnalysisOptions:
    repo_root: Path
    run_root: Path
    output_dir: Path
    baseline_root: Path | None = None
    override_cells: tuple[tuple[str, str], ...] | None = None
    sources: tuple[str, ...] = DEFAULT_SOURCES
    cells: tuple[str, ...] = DEFAULT_CELLS
    expected_rows_per_cell: int = EXPECTED_ROWS_PER_CELL
    model: str | None = None
    method: str = "direct_zs"
    title: str | None = None
    analysis_date: str | None = None


def parse_override_cell(token: str) -> tuple[str, str]:
    source, separator, cell = token.partition("/")
    if not separator or not source or not cell:
        raise ValueError(
            f"Override cell must look like 'source/Q_xx--S_xx--V_xx', got: {token}"
        )
    return source, cell


def analyze_cube(options: CubeAnalysisOptions) -> dict:
    run_root = _resolve(options.repo_root, options.run_root)
    baseline_root = (
        _resolve(options.repo_root, options.baseline_root)
        if options.baseline_root is not None
        else None
    )
    output_dir = _resolve(options.repo_root, options.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    model = options.model or _infer_model(run_root, baseline_root)
    method = options.method
    analysis_date = options.analysis_date or date.today().isoformat()
    title = options.title or f"{model} on MoL-Cube"

    override_cells = _resolve_override_cells(
        run_root=run_root,
        baseline_root=baseline_root,
        sources=options.sources,
        cells=options.cells,
        override_cells=options.override_cells,
    )

    baseline_cells: dict[tuple[str, str], list[dict]] = {}
    merged_cells: dict[tuple[str, str], list[dict]] = {}
    for source in options.sources:
        for cell in options.cells:
            key = (source, cell)
            use_override = key in override_cells
            if baseline_root is None:
                merged_cells[key] = _load_cell(
                    root=run_root,
                    source=source,
                    cell=cell,
                    expected_rows=options.expected_rows_per_cell,
                    origin="run",
                )
            else:
                baseline_cells[key] = _load_cell(
                    root=baseline_root,
                    source=source,
                    cell=cell,
                    expected_rows=options.expected_rows_per_cell,
                    origin="baseline",
                )
                merged_cells[key] = _load_cell(
                    root=run_root if use_override else baseline_root,
                    source=source,
                    cell=cell,
                    expected_rows=options.expected_rows_per_cell,
                    origin="override" if use_override else "baseline",
                )

    baseline_rows = [row for rows in baseline_cells.values() for row in rows]
    merged_rows = [row for rows in merged_cells.values() for row in rows]
    expected_total = (
        len(options.sources) * len(options.cells) * options.expected_rows_per_cell
    )
    if len(merged_rows) != expected_total:
        raise ValueError(
            f"Expected {expected_total} realizations, got {len(merged_rows)}"
        )
    if baseline_root is not None and len(baseline_rows) != expected_total:
        raise ValueError(
            f"Expected {expected_total} baseline realizations, got {len(baseline_rows)}"
        )

    has_baseline = baseline_root is not None
    merged_summary = _summarize(merged_rows)
    baseline_summary = _summarize(baseline_rows) if has_baseline else None
    source_summaries = {
        source: _summarize([row for row in merged_rows if row["source"] == source])
        for source in options.sources
    }
    source_macro = mean(
        source_summaries[source]["metrics"]["overall"]["accuracy"]
        for source in options.sources
    )

    cell_rows = []
    for source in options.sources:
        for cell in options.cells:
            key = (source, cell)
            summary = _accuracy(merged_cells[key])
            if has_baseline:
                old = _accuracy(baseline_cells[key])
                old_accuracy = old["accuracy"]
                change = summary["accuracy"] - old["accuracy"]
            else:
                old_accuracy = None
                change = None
            cell_rows.append(
                {
                    "source": source,
                    "cell": cell,
                    "correct": summary["correct"],
                    "total": summary["total"],
                    "accuracy": summary["accuracy"],
                    "old_accuracy": old_accuracy,
                    "change": change,
                    "origin": (
                        "override"
                        if key in override_cells
                        else ("run" if not has_baseline else "baseline")
                    ),
                }
            )

    source_rows = []
    for source in options.sources:
        summary = source_summaries[source]
        metrics = summary["metrics"]
        gaps = summary["gaps"]
        source_rows.append(
            {
                "source": source,
                "correct": metrics["overall"]["correct"],
                "total": metrics["overall"]["total"],
                "accuracy": metrics["overall"]["accuracy"],
                "delta_q": gaps["delta_q_en_minus_zh"],
                "delta_s": gaps["delta_s_en_minus_zh"],
                "delta_v": gaps["delta_v_en_minus_zh"],
                "qs_gap": gaps["qs_match_gap"],
                "qv_gap": gaps["qv_match_gap"],
                "sv_gap": gaps["sv_match_gap"],
                "q_vs_gap": gaps["q_vs_match_gap"],
                "valid_sql_rate": summary["operations"]["valid_sql_rate"],
            }
        )

    transitions = {}
    for key in sorted(override_cells):
        if not has_baseline:
            break
        source, cell = key
        transitions[f"{source}/{cell}"] = _paired_transition(
            baseline_cells[key], merged_cells[key]
        )

    by_difficulty = {
        difficulty: _accuracy(
            [row for row in merged_rows if row["difficulty"] == difficulty]
        )
        for difficulty in sorted({row["difficulty"] for row in merged_rows})
    }

    payload = {
        "analysis_date": analysis_date,
        "model": model,
        "method": method,
        "title": title,
        "merge_policy": {
            "run_root": str(_relative_to_repo(options.repo_root, run_root)),
            "baseline_root": (
                str(_relative_to_repo(options.repo_root, baseline_root))
                if baseline_root is not None
                else None
            ),
            "replaced_cells": [
                f"{source}/{cell}" for source, cell in sorted(override_cells)
            ],
        },
        "baseline_summary": baseline_summary,
        "summary": merged_summary,
        "source_macro_accuracy": source_macro,
        "per_source": source_summaries,
        "by_difficulty": by_difficulty,
        "override_cell_transitions": transitions,
    }
    # Keep qwen-compatible alias used by older reports.
    payload["corrected_summary"] = merged_summary
    payload["old_summary"] = baseline_summary

    with (output_dir / "summary.json").open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")

    _write_csv(
        output_dir / "cells.csv",
        cell_rows,
        [
            "source",
            "cell",
            "correct",
            "total",
            "accuracy",
            "old_accuracy",
            "change",
            "origin",
        ],
    )
    _write_csv(
        output_dir / "sources.csv",
        source_rows,
        [
            "source",
            "correct",
            "total",
            "accuracy",
            "delta_q",
            "delta_s",
            "delta_v",
            "qs_gap",
            "qv_gap",
            "sv_gap",
            "q_vs_gap",
            "valid_sql_rate",
        ],
    )

    report = _build_report(
        title=title,
        model=model,
        method=method,
        sources=options.sources,
        cells=options.cells,
        expected_total=expected_total,
        has_baseline=has_baseline,
        override_cells=override_cells,
        merged_summary=merged_summary,
        baseline_summary=baseline_summary,
        cell_rows=cell_rows,
        source_rows=source_rows,
        merged_rows=merged_rows,
        by_difficulty=by_difficulty,
        transitions=transitions,
        source_summaries=source_summaries,
    )
    (output_dir / "report.md").write_text(report, encoding="utf-8")
    return payload


def _resolve(repo_root: Path, path: Path) -> Path:
    return path if path.is_absolute() else (repo_root / path).resolve()


def _relative_to_repo(repo_root: Path, path: Path) -> Path:
    try:
        return path.resolve().relative_to(repo_root.resolve())
    except ValueError:
        return path.resolve()


def _infer_model(run_root: Path, baseline_root: Path | None) -> str:
    for root in (run_root, baseline_root):
        if root is None:
            continue
        manifest_path = root / "run_manifest.json"
        if manifest_path.exists():
            manifest = load_json(manifest_path)
            model = manifest.get("model")
            if model:
                return str(model)
    return run_root.name


def _resolve_override_cells(
    *,
    run_root: Path,
    baseline_root: Path | None,
    sources: tuple[str, ...],
    cells: tuple[str, ...],
    override_cells: tuple[tuple[str, str], ...] | None,
) -> set[tuple[str, str]]:
    if baseline_root is None:
        return set()
    if override_cells is not None:
        unknown = [
            f"{source}/{cell}"
            for source, cell in override_cells
            if source not in sources or cell not in cells
        ]
        if unknown:
            raise ValueError(f"Unknown override cells: {unknown}")
        return set(override_cells)
    discovered = set()
    for source in sources:
        for cell in cells:
            evaluation = run_root / source / cell / "evaluation.jsonl"
            if evaluation.exists():
                discovered.add((source, cell))
    if not discovered:
        raise ValueError(
            "baseline_root was set but no override cells were found under run_root; "
            "pass --override-cells explicitly"
        )
    return discovered


def _load_jsonl(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def _axes(cell: str) -> dict[str, str]:
    return {part[0]: part[2:] for part in cell.split("--")}


def _index_by_instance_id(
    rows: list[dict],
    *,
    prefer_success: bool,
) -> dict[str, dict]:
    """Collapse retries: later rows win; optionally keep success over failures."""
    by_id: dict[str, dict] = {}
    for row in rows:
        instance_id = row["instance_id"]
        existing = by_id.get(instance_id)
        if existing is None:
            by_id[instance_id] = row
            continue
        if prefer_success and existing.get("status") == "success" and row.get("status") != "success":
            continue
        by_id[instance_id] = row
    return by_id


def _load_cell(
    *,
    root: Path,
    source: str,
    cell: str,
    expected_rows: int,
    origin: str,
) -> list[dict]:
    cell_root = root / source / cell
    prompts = _load_jsonl(cell_root / "prompts.jsonl")
    predictions = _load_jsonl(cell_root / "predictions.jsonl")
    evaluations = _load_jsonl(cell_root / "evaluation.jsonl")
    if len(prompts) != expected_rows:
        raise ValueError(
            f"Unexpected prompt count for {root}/{source}/{cell}: "
            f"prompts={len(prompts)} expected={expected_rows}"
        )

    prediction_by_id = _index_by_instance_id(predictions, prefer_success=True)
    evaluation_by_id = _index_by_instance_id(evaluations, prefer_success=False)
    if len(prediction_by_id) != expected_rows or len(evaluation_by_id) != expected_rows:
        raise ValueError(
            f"Unexpected unique instance count for {root}/{source}/{cell}: "
            f"predictions={len(prediction_by_id)} evaluation={len(evaluation_by_id)} "
            f"expected={expected_rows}"
        )
    missing_pred = [
        row["instance_id"] for row in prompts if row["instance_id"] not in prediction_by_id
    ]
    missing_eval = [
        row["instance_id"] for row in prompts if row["instance_id"] not in evaluation_by_id
    ]
    if missing_pred or missing_eval:
        raise ValueError(
            f"Missing joined records for {root}/{source}/{cell}: "
            f"predictions_missing={len(missing_pred)} evaluation_missing={len(missing_eval)}"
        )

    parsed_axes = _axes(cell)
    rows = []
    for prompt in prompts:
        instance_id = prompt["instance_id"]
        prediction = prediction_by_id[instance_id]
        evaluation = evaluation_by_id[instance_id]
        rows.append(
            {
                "source": source,
                "cell": cell,
                "Q": parsed_axes["Q"],
                "S": parsed_axes["S"],
                "V": parsed_axes["V"],
                "logical_id": prompt["logical_id"],
                "instance_id": instance_id,
                "difficulty": prompt.get("difficulty", "unknown"),
                "correct": int(evaluation["execution_match"]),
                "evaluation_status": evaluation["status"],
                "prediction_status": prediction["status"],
                "prompt_tokens": prediction.get("prompt_tokens"),
                "completion_tokens": prediction.get("completion_tokens"),
                "latency_seconds": prediction.get("latency_seconds"),
                "result_origin": origin,
            }
        )
    return rows


def _accuracy(rows: list[dict]) -> dict:
    total = len(rows)
    correct = sum(row["correct"] for row in rows)
    return {
        "correct": correct,
        "total": total,
        "accuracy": (correct / total) if total else 0.0,
    }


def _metric(rows: list[dict], predicate) -> dict:
    return _accuracy([row for row in rows if predicate(row)])


def _summarize(rows: list[dict]) -> dict:
    metrics = {
        "overall": _accuracy(rows),
        "q_en": _metric(rows, lambda row: row["Q"] == "en"),
        "q_zh": _metric(rows, lambda row: row["Q"] == "zh"),
        "s_en": _metric(rows, lambda row: row["S"] == "en"),
        "s_zh": _metric(rows, lambda row: row["S"] == "zh"),
        "v_en": _metric(rows, lambda row: row["V"] == "en"),
        "v_zh": _metric(rows, lambda row: row["V"] == "zh"),
        "qs_match": _metric(rows, lambda row: row["Q"] == row["S"]),
        "qs_mismatch": _metric(rows, lambda row: row["Q"] != row["S"]),
        "qv_match": _metric(rows, lambda row: row["Q"] == row["V"]),
        "qv_mismatch": _metric(rows, lambda row: row["Q"] != row["V"]),
        "sv_match": _metric(rows, lambda row: row["S"] == row["V"]),
        "sv_mismatch": _metric(rows, lambda row: row["S"] != row["V"]),
        "q_vs_match": _metric(
            rows, lambda row: row["S"] == row["V"] and row["Q"] == row["S"]
        ),
        "q_vs_mismatch": _metric(
            rows, lambda row: row["S"] == row["V"] and row["Q"] != row["S"]
        ),
    }
    gaps = {
        "delta_q_en_minus_zh": metrics["q_en"]["accuracy"]
        - metrics["q_zh"]["accuracy"],
        "delta_s_en_minus_zh": metrics["s_en"]["accuracy"]
        - metrics["s_zh"]["accuracy"],
        "delta_v_en_minus_zh": metrics["v_en"]["accuracy"]
        - metrics["v_zh"]["accuracy"],
        "qs_match_gap": metrics["qs_match"]["accuracy"]
        - metrics["qs_mismatch"]["accuracy"],
        "qv_match_gap": metrics["qv_match"]["accuracy"]
        - metrics["qv_mismatch"]["accuracy"],
        "sv_match_gap": metrics["sv_match"]["accuracy"]
        - metrics["sv_mismatch"]["accuracy"],
        "q_vs_match_gap": metrics["q_vs_match"]["accuracy"]
        - metrics["q_vs_mismatch"]["accuracy"],
    }
    status_counts = Counter(row["evaluation_status"] for row in rows)
    prediction_counts = Counter(row["prediction_status"] for row in rows)
    valid_sql = sum(
        count
        for status, count in status_counts.items()
        if status not in INVALID_SQL_STATUSES
    )
    token_rows = [row for row in rows if row["prompt_tokens"] is not None]
    latency_rows = [
        row
        for row in rows
        if row["latency_seconds"] is not None and row["latency_seconds"] > 0
    ]
    operations = {
        "evaluation_status": dict(sorted(status_counts.items())),
        "prediction_status": dict(sorted(prediction_counts.items())),
        "valid_sql": valid_sql,
        "valid_sql_rate": valid_sql / len(rows) if rows else 0.0,
        "usage_record_count": len(token_rows),
        "prompt_tokens": sum(row["prompt_tokens"] for row in token_rows),
        "completion_tokens": sum(row["completion_tokens"] or 0 for row in token_rows),
        "latency_record_count": len(latency_rows),
        "mean_latency_seconds": (
            mean(row["latency_seconds"] for row in latency_rows)
            if latency_rows
            else None
        ),
        "total_latency_seconds": sum(row["latency_seconds"] for row in latency_rows),
    }
    return {"metrics": metrics, "gaps": gaps, "operations": operations}


def _paired_transition(old_rows: list[dict], new_rows: list[dict]) -> dict:
    old = {row["logical_id"]: row for row in old_rows}
    new = {row["logical_id"]: row for row in new_rows}
    if old.keys() != new.keys():
        raise ValueError("Baseline and override logical IDs do not align")
    transitions = Counter()
    status_transitions = Counter()
    for logical_id in old:
        transitions[(old[logical_id]["correct"], new[logical_id]["correct"])] += 1
        status_transitions[
            (
                old[logical_id]["evaluation_status"],
                new[logical_id]["evaluation_status"],
            )
        ] += 1
    return {
        "wrong_to_wrong": transitions[(0, 0)],
        "wrong_to_correct": transitions[(0, 1)],
        "correct_to_wrong": transitions[(1, 0)],
        "correct_to_correct": transitions[(1, 1)],
        "net_correct_change": transitions[(0, 1)] - transitions[(1, 0)],
        "status_transitions": {
            f"{old_status}->{new_status}": count
            for (old_status, new_status), count in sorted(status_transitions.items())
        },
    }


def _pct(value: float) -> str:
    return f"{value * 100:.2f}%"


def _pp(value: float) -> str:
    return f"{value * 100:+.2f} pp"


def _write_csv(path: Path, rows: list[dict], columns: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def _fmt_acc(result: dict) -> str:
    return f"{result['correct']}/{result['total']} = {_pct(result['accuracy'])}"


def _build_report(
    *,
    title: str,
    model: str,
    method: str,
    sources: tuple[str, ...],
    cells: tuple[str, ...],
    expected_total: int,
    has_baseline: bool,
    override_cells: set[tuple[str, str]],
    merged_summary: dict,
    baseline_summary: dict | None,
    cell_rows: list[dict],
    source_rows: list[dict],
    merged_rows: list[dict],
    by_difficulty: dict[str, dict],
    transitions: dict[str, dict],
    source_summaries: dict[str, dict],
) -> str:
    metrics = merged_summary["metrics"]
    gaps = merged_summary["gaps"]
    operations = merged_summary["operations"]
    old_metrics = baseline_summary["metrics"] if baseline_summary else None
    old_gaps = baseline_summary["gaps"] if baseline_summary else None
    old_operations = baseline_summary["operations"] if baseline_summary else None

    overall_cells = {
        cell: _accuracy([row for row in merged_rows if row["cell"] == cell])
        for cell in cells
    }
    bull_cells = {row["cell"]: row for row in cell_rows if row["source"] == "bull"}
    rows_per_cell = metrics["overall"]["total"] // len(cells)

    policy_line = (
        f"- 以 baseline run 为基线，并用 override run 替换 "
        f"{len(override_cells)} 个 cell：`"
        + "`, `".join(f"{source}/{cell}" for source, cell in sorted(override_cells))
        + "`。"
        if has_baseline
        else "- 直接分析完整 run（无 baseline 合并）。"
    )

    lines = [
        f"# {title}：结果分析",
        "",
        "## 1. 分析口径",
        "",
        f"- 方法：{method}；模型：`{model}`。",
        f"- 总样本：{len(sources)} 个 source × "
        f"{metrics['overall']['total'] // (len(sources) * len(cells))} 个 logical "
        f"instances × {len(cells)} 个 Q/S/V cells = {expected_total:,}。",
        policy_line,
        "- `Q-(VS)` 仅保留 `S=V` 的四格；match 表示 `Q=S=V`，mismatch 表示 `S=V≠Q`。",
        "- accuracy 均为 realization-level micro execution accuracy。",
        "",
        "## 2. 核心结果",
        "",
    ]

    if has_baseline and old_metrics is not None and old_gaps is not None and old_operations is not None:
        lines += [
            "| 指标 | 当前 | 基线 | 变化 |",
            "|---|---:|---:|---:|",
            (
                f"| Overall Exec Acc | {_fmt_acc(metrics['overall'])} | "
                f"{_fmt_acc(old_metrics['overall'])} | "
                f"{_pp(metrics['overall']['accuracy'] - old_metrics['overall']['accuracy'])} |"
            ),
            (
                f"| Valid SQL Rate | {operations['valid_sql']}/{metrics['overall']['total']} = "
                f"{_pct(operations['valid_sql_rate'])} | "
                f"{old_operations['valid_sql']}/{old_metrics['overall']['total']} = "
                f"{_pct(old_operations['valid_sql_rate'])} | "
                f"{_pp(operations['valid_sql_rate'] - old_operations['valid_sql_rate'])} |"
            ),
            (
                f"| Q-S Match Gap | {_pp(gaps['qs_match_gap'])} | "
                f"{_pp(old_gaps['qs_match_gap'])} | "
                f"{_pp(gaps['qs_match_gap'] - old_gaps['qs_match_gap'])} |"
            ),
            (
                f"| Q-V Match Gap | {_pp(gaps['qv_match_gap'])} | "
                f"{_pp(old_gaps['qv_match_gap'])} | "
                f"{_pp(gaps['qv_match_gap'] - old_gaps['qv_match_gap'])} |"
            ),
            (
                f"| S-V Match Gap | {_pp(gaps['sv_match_gap'])} | "
                f"{_pp(old_gaps['sv_match_gap'])} | "
                f"{_pp(gaps['sv_match_gap'] - old_gaps['sv_match_gap'])} |"
            ),
            (
                f"| Q-(VS) Match Gap | {_pp(gaps['q_vs_match_gap'])} | "
                f"{_pp(old_gaps['q_vs_match_gap'])} | "
                f"{_pp(gaps['q_vs_match_gap'] - old_gaps['q_vs_match_gap'])} |"
            ),
            "",
        ]
    else:
        lines += [
            "| 指标 | 数值 |",
            "|---|---:|",
            f"| Overall Exec Acc | {_fmt_acc(metrics['overall'])} |",
            (
                f"| Valid SQL Rate | {operations['valid_sql']}/{metrics['overall']['total']} = "
                f"{_pct(operations['valid_sql_rate'])} |"
            ),
            f"| Q-S Match Gap | {_pp(gaps['qs_match_gap'])} |",
            f"| Q-V Match Gap | {_pp(gaps['qv_match_gap'])} |",
            f"| S-V Match Gap | {_pp(gaps['sv_match_gap'])} |",
            f"| Q-(VS) Match Gap | {_pp(gaps['q_vs_match_gap'])} |",
            "",
        ]

    lines += [
        "## 3. 八格 Micro Exec Acc",
        "",
        f"| Cell | Correct / {rows_per_cell} | Accuracy |",
        "|---|---:|---:|",
    ]
    for cell in cells:
        result = overall_cells[cell]
        lines.append(
            f"| `{cell}` | {result['correct']}/{result['total']} | {_pct(result['accuracy'])} |"
        )

    best_cell = max(cells, key=lambda cell: overall_cells[cell]["accuracy"])
    worst_cell = min(cells, key=lambda cell: overall_cells[cell]["accuracy"])
    lines += [
        "",
        (
            f"最优 cell：`{best_cell}`（{_pct(overall_cells[best_cell]['accuracy'])}）；"
            f"最差 cell：`{worst_cell}`（{_pct(overall_cells[worst_cell]['accuracy'])}）。"
        ),
        "",
        "## 4. 轴边际与匹配分析",
        "",
        "| 对比 | 第一组 | 第二组 | Gap（第一组−第二组） |",
        "|---|---:|---:|---:|",
        (
            f"| Q language | en {_pct(metrics['q_en']['accuracy'])} | "
            f"zh {_pct(metrics['q_zh']['accuracy'])} | {_pp(gaps['delta_q_en_minus_zh'])} |"
        ),
        (
            f"| S language | en {_pct(metrics['s_en']['accuracy'])} | "
            f"zh {_pct(metrics['s_zh']['accuracy'])} | {_pp(gaps['delta_s_en_minus_zh'])} |"
        ),
        (
            f"| V language | en {_pct(metrics['v_en']['accuracy'])} | "
            f"zh {_pct(metrics['v_zh']['accuracy'])} | {_pp(gaps['delta_v_en_minus_zh'])} |"
        ),
        (
            f"| Q-S relation | match {_pct(metrics['qs_match']['accuracy'])} | "
            f"mismatch {_pct(metrics['qs_mismatch']['accuracy'])} | {_pp(gaps['qs_match_gap'])} |"
        ),
        (
            f"| Q-V relation | match {_pct(metrics['qv_match']['accuracy'])} | "
            f"mismatch {_pct(metrics['qv_mismatch']['accuracy'])} | {_pp(gaps['qv_match_gap'])} |"
        ),
        (
            f"| S-V relation | match {_pct(metrics['sv_match']['accuracy'])} | "
            f"mismatch {_pct(metrics['sv_mismatch']['accuracy'])} | {_pp(gaps['sv_match_gap'])} |"
        ),
        (
            f"| Q-(VS), only S=V | match {_pct(metrics['q_vs_match']['accuracy'])} | "
            f"mismatch {_pct(metrics['q_vs_mismatch']['accuracy'])} | {_pp(gaps['q_vs_match_gap'])} |"
        ),
        "",
        "## 5. Source 分解",
        "",
        "| Source | Exec Acc | ΔQ | ΔS | ΔV | Q-S gap | Q-V gap | S-V gap | Q-(VS) gap | Valid SQL |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in source_rows:
        lines.append(
            f"| {row['source']} | {row['correct']}/{row['total']} = {_pct(row['accuracy'])} | "
            f"{_pp(row['delta_q'])} | {_pp(row['delta_s'])} | {_pp(row['delta_v'])} | "
            f"{_pp(row['qs_gap'])} | {_pp(row['qv_gap'])} | {_pp(row['sv_gap'])} | "
            f"{_pp(row['q_vs_gap'])} | {_pct(row['valid_sql_rate'])} |"
        )

    source_accs = [row["accuracy"] for row in source_rows]
    if source_accs:
        best_source = max(source_rows, key=lambda row: row["accuracy"])
        worst_source = min(source_rows, key=lambda row: row["accuracy"])
        lines += [
            "",
            (
                f"Source overall 从 {worst_source['source']} 的 "
                f"{_pct(worst_source['accuracy'])} 到 {best_source['source']} 的 "
                f"{_pct(best_source['accuracy'])}，相差 "
                f"{_pp(best_source['accuracy'] - worst_source['accuracy'])}。"
            ),
        ]

    lines += [
        "",
        "## 6. BULL 八格",
        "",
    ]
    if has_baseline:
        lines += [
            "| BULL cell | 当前 | 基线 | 变化 |",
            "|---|---:|---:|---:|",
        ]
        for cell in cells:
            row = bull_cells[cell]
            lines.append(
                f"| `{cell}` | {row['correct']}/{row['total']} = {_pct(row['accuracy'])} | "
                f"{_pct(row['old_accuracy'])} | {_pp(row['change'])} |"
            )
    else:
        lines += [
            "| BULL cell | Correct / Total | Accuracy |",
            "|---|---:|---:|",
        ]
        for cell in cells:
            row = bull_cells[cell]
            lines.append(
                f"| `{cell}` | {row['correct']}/{row['total']} | {_pct(row['accuracy'])} |"
            )

    if transitions:
        lines += ["", "Override cell 成对迁移（按相同 `logical_id`）：", ""]
        for key, transition in transitions.items():
            lines.append(
                f"- `{key}`：wrong→correct {transition['wrong_to_correct']}，"
                f"correct→wrong {transition['correct_to_wrong']}，"
                f"correct→correct {transition['correct_to_correct']}，"
                f"wrong→wrong {transition['wrong_to_wrong']}，"
                f"净变化 {transition['net_correct_change']:+d}。"
            )

    if "bull" in source_summaries:
        bull_summary = source_summaries["bull"]
        lines += [
            "",
            f"BULL overall：{_pct(bull_summary['metrics']['overall']['accuracy'])}；"
            f"ΔQ={_pp(bull_summary['gaps']['delta_q_en_minus_zh'])}，"
            f"ΔS={_pp(bull_summary['gaps']['delta_s_en_minus_zh'])}，"
            f"ΔV={_pp(bull_summary['gaps']['delta_v_en_minus_zh'])}。",
            "",
            "BULL 内部 S 切换（`Acc(S=en) - Acc(S=zh)`，固定 Q 与 V）：",
            "",
            "| 固定条件 | S=en | S=zh | ΔS |",
            "|---|---:|---:|---:|",
        ]
        for question in ("en", "zh"):
            for value in ("en", "zh"):
                en_cell = f"Q_{question}--S_en--V_{value}"
                zh_cell = f"Q_{question}--S_zh--V_{value}"
                en_acc = bull_cells[en_cell]["accuracy"]
                zh_acc = bull_cells[zh_cell]["accuracy"]
                lines.append(
                    f"| Q={question}, V={value} | {_pct(en_acc)} | {_pct(zh_acc)} | "
                    f"{_pp(en_acc - zh_acc)} |"
                )

    eval_status = operations["evaluation_status"]
    pred_status = operations["prediction_status"]
    gold_error = eval_status.get("gold_error", 0)
    lines += [
        "",
        "## 7. 错误与运行状态",
        "",
        (
            f"- API prediction：{pred_status.get('success', 0)}/{metrics['overall']['total']} "
            f"success；failed={pred_status.get('failed', 0)}。"
        ),
        (
            f"- Evaluation：correct {eval_status.get('correct', 0)}，"
            f"wrong_result {eval_status.get('wrong_result', 0)}，"
            f"invalid_sql {eval_status.get('invalid_sql', 0)}，"
            f"timeout {eval_status.get('timeout', 0)}，"
            f"gold_error {gold_error}。"
        ),
        (
            f"- Token usage：{operations['usage_record_count']}/{metrics['overall']['total']} "
            f"条有记录；prompt {operations['prompt_tokens']:,}，"
            f"completion {operations['completion_tokens']:,}，"
            f"合计 {operations['prompt_tokens'] + operations['completion_tokens']:,}。"
        ),
    ]
    if operations["mean_latency_seconds"] is not None:
        lines.append(
            f"- API latency：{operations['latency_record_count']}/{metrics['overall']['total']} "
            f"条有非零记录；均值 {operations['mean_latency_seconds']:.2f}s/条，"
            f"总和 {operations['total_latency_seconds'] / 3600:.2f} 小时。"
        )
    if gold_error:
        denom = metrics["overall"]["total"] - gold_error
        lines.append(
            f"- 若仅作诊断并排除 {gold_error} 条 gold_error，accuracy 为 "
            f"{_pct(metrics['overall']['correct'] / denom)}（不可替代主指标）。"
        )

    lines += [
        "",
        "## 8. Difficulty",
        "",
        "| Difficulty | Correct / Total | Exec Acc |",
        "|---|---:|---:|",
    ]
    for difficulty in sorted(by_difficulty):
        result = by_difficulty[difficulty]
        lines.append(
            f"| {difficulty} | {result['correct']}/{result['total']} | "
            f"{_pct(result['accuracy'])} |"
        )

    lines += [
        "",
        "## 9. 结论",
        "",
        f"1. Overall Exec Acc = {_fmt_acc(metrics['overall'])}。",
        (
            f"2. 单轴边际：ΔQ={_pp(gaps['delta_q_en_minus_zh'])}，"
            f"ΔS={_pp(gaps['delta_s_en_minus_zh'])}，"
            f"ΔV={_pp(gaps['delta_v_en_minus_zh'])}。"
        ),
        (
            f"3. 匹配 gap：Q-S={_pp(gaps['qs_match_gap'])}，"
            f"Q-V={_pp(gaps['qv_match_gap'])}，"
            f"S-V={_pp(gaps['sv_match_gap'])}，"
            f"Q-(VS)={_pp(gaps['q_vs_match_gap'])}。"
        ),
        "4. Source 间准确率与语言效应方向可能不一致，解释时应优先做 per-source 分解。",
        "",
        "## 10. 可复现文件",
        "",
        "- `summary.json`：完整聚合结果与（如有）迁移统计。",
        "- `cells.csv`：source/cell 结果。",
        "- `sources.csv`：五源轴效应与匹配 gap。",
        "- `report.md`：本报告。",
        "",
    ]
    return "\n".join(lines)
