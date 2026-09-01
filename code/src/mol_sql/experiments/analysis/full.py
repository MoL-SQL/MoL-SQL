"""Aggregate Direct-ZS MoL-Full run metrics into reproducible report artifacts.

Full ships four coupled cells where schema and value languages stay aligned
(`S_en--V_en` / `S_zh--V_zh`). Independent ΔS / ΔV are not identified; the
report instead treats DB language as a coupled factor and reports ΔQ, ΔDB, and
Q-DB match gap.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from statistics import mean

from mol_sql.experiments.analysis.cube import (
    DEFAULT_SOURCES,
    _accuracy,
    _fmt_acc,
    _infer_model,
    _load_cell,
    _pct,
    _pp,
    _relative_to_repo,
    _resolve,
    _summarize,
    _write_csv,
)


DEFAULT_CELLS = (
    "Q_en--S_en--V_en",
    "Q_en--S_zh--V_zh",
    "Q_zh--S_en--V_en",
    "Q_zh--S_zh--V_zh",
)

# Logical-instance counts in mol-full-v0.1 bird_format exports.
EXPECTED_ROWS_BY_SOURCE = {
    "bird": 498,
    "bull": 1000,
    "ehrsql": 1511,
    "kaggledbqa": 184,
    "spider": 1030,
}


@dataclass(frozen=True)
class FullAnalysisOptions:
    repo_root: Path
    run_root: Path
    output_dir: Path
    sources: tuple[str, ...] = DEFAULT_SOURCES
    cells: tuple[str, ...] = DEFAULT_CELLS
    expected_rows_by_source: dict[str, int] | None = None
    model: str | None = None
    method: str = "direct_zs"
    title: str | None = None
    analysis_date: str | None = None


def analyze_full(options: FullAnalysisOptions) -> dict:
    run_root = _resolve(options.repo_root, options.run_root)
    output_dir = _resolve(options.repo_root, options.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    model = options.model or _infer_model(run_root, None)
    method = options.method
    analysis_date = options.analysis_date or date.today().isoformat()
    title = options.title or f"{model} on MoL-Full"
    expected_rows_by_source = (
        options.expected_rows_by_source
        if options.expected_rows_by_source is not None
        else {
            source: EXPECTED_ROWS_BY_SOURCE[source]
            for source in options.sources
            if source in EXPECTED_ROWS_BY_SOURCE
        }
    )
    missing_expected = sorted(set(options.sources) - set(expected_rows_by_source))
    if missing_expected:
        raise ValueError(
            "Missing expected row counts for sources: "
            f"{missing_expected}; pass expected_rows_by_source"
        )

    cells_data: dict[tuple[str, str], list[dict]] = {}
    for source in options.sources:
        expected_rows = expected_rows_by_source[source]
        for cell in options.cells:
            cells_data[(source, cell)] = _load_cell(
                root=run_root,
                source=source,
                cell=cell,
                expected_rows=expected_rows,
                origin="run",
            )

    rows = [row for cell_rows in cells_data.values() for row in cell_rows]
    expected_total = sum(
        expected_rows_by_source[source] * len(options.cells) for source in options.sources
    )
    if len(rows) != expected_total:
        raise ValueError(f"Expected {expected_total} realizations, got {len(rows)}")

    summary = _summarize_full(rows)
    source_summaries = {
        source: _summarize_full([row for row in rows if row["source"] == source])
        for source in options.sources
    }
    source_macro = mean(
        source_summaries[source]["metrics"]["overall"]["accuracy"]
        for source in options.sources
    )

    cell_rows = []
    for source in options.sources:
        for cell in options.cells:
            accuracy = _accuracy(cells_data[(source, cell)])
            cell_rows.append(
                {
                    "source": source,
                    "cell": cell,
                    "correct": accuracy["correct"],
                    "total": accuracy["total"],
                    "accuracy": accuracy["accuracy"],
                }
            )

    source_rows = []
    for source in options.sources:
        source_summary = source_summaries[source]
        metrics = source_summary["metrics"]
        gaps = source_summary["gaps"]
        source_rows.append(
            {
                "source": source,
                "correct": metrics["overall"]["correct"],
                "total": metrics["overall"]["total"],
                "accuracy": metrics["overall"]["accuracy"],
                "delta_q": gaps["delta_q_en_minus_zh"],
                "delta_db": gaps["delta_db_en_minus_zh"],
                "q_db_gap": gaps["q_db_match_gap"],
                "valid_sql_rate": source_summary["operations"]["valid_sql_rate"],
            }
        )

    by_difficulty = {
        difficulty: _accuracy([row for row in rows if row["difficulty"] == difficulty])
        for difficulty in sorted({row["difficulty"] for row in rows})
    }

    payload = {
        "analysis_date": analysis_date,
        "model": model,
        "method": method,
        "title": title,
        "design": {
            "kind": "mol-full-four-cell",
            "note": (
                "S and V languages are coupled in Full; ΔDB is Acc(S=V=en) - Acc(S=V=zh). "
                "Independent ΔS / ΔV are not identified."
            ),
            "run_root": str(_relative_to_repo(options.repo_root, run_root)),
            "expected_rows_by_source": expected_rows_by_source,
        },
        "summary": summary,
        "source_macro_accuracy": source_macro,
        "per_source": source_summaries,
        "by_difficulty": by_difficulty,
    }

    with (output_dir / "summary.json").open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")

    _write_csv(
        output_dir / "cells.csv",
        cell_rows,
        ["source", "cell", "correct", "total", "accuracy"],
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
            "delta_db",
            "q_db_gap",
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
        expected_rows_by_source=expected_rows_by_source,
        summary=summary,
        cell_rows=cell_rows,
        source_rows=source_rows,
        rows=rows,
        by_difficulty=by_difficulty,
        source_summaries=source_summaries,
        source_macro=source_macro,
    )
    (output_dir / "report.md").write_text(report, encoding="utf-8")
    return payload


def _summarize_full(rows: list[dict]) -> dict:
    """Summarize Full four-cell metrics with coupled DB-language factors."""
    base = _summarize(rows)
    metrics = base["metrics"]
    # In Full, S and V are always aligned, so DB language partitions coincide.
    metrics["db_en"] = metrics["s_en"]
    metrics["db_zh"] = metrics["s_zh"]
    metrics["q_db_match"] = metrics["qs_match"]
    metrics["q_db_mismatch"] = metrics["qs_mismatch"]
    gaps = {
        "delta_q_en_minus_zh": metrics["q_en"]["accuracy"] - metrics["q_zh"]["accuracy"],
        "delta_db_en_minus_zh": metrics["db_en"]["accuracy"]
        - metrics["db_zh"]["accuracy"],
        "q_db_match_gap": metrics["q_db_match"]["accuracy"]
        - metrics["q_db_mismatch"]["accuracy"],
        # Kept for transparency; identical to ΔDB / Q-DB under Full coupling.
        "delta_s_en_minus_zh": metrics["s_en"]["accuracy"] - metrics["s_zh"]["accuracy"],
        "delta_v_en_minus_zh": metrics["v_en"]["accuracy"] - metrics["v_zh"]["accuracy"],
        "qs_match_gap": metrics["qs_match"]["accuracy"] - metrics["qs_mismatch"]["accuracy"],
        "qv_match_gap": metrics["qv_match"]["accuracy"] - metrics["qv_mismatch"]["accuracy"],
        "sv_match_gap": metrics["sv_match"]["accuracy"] - metrics["sv_mismatch"]["accuracy"],
        "q_vs_match_gap": metrics["q_vs_match"]["accuracy"]
        - metrics["q_vs_mismatch"]["accuracy"],
    }
    return {"metrics": metrics, "gaps": gaps, "operations": base["operations"]}


def _build_report(
    *,
    title: str,
    model: str,
    method: str,
    sources: tuple[str, ...],
    cells: tuple[str, ...],
    expected_total: int,
    expected_rows_by_source: dict[str, int],
    summary: dict,
    cell_rows: list[dict],
    source_rows: list[dict],
    rows: list[dict],
    by_difficulty: dict[str, dict],
    source_summaries: dict[str, dict],
    source_macro: float,
) -> str:
    metrics = summary["metrics"]
    gaps = summary["gaps"]
    operations = summary["operations"]
    overall_cells = {
        cell: _accuracy([row for row in rows if row["cell"] == cell]) for cell in cells
    }
    counts_text = ", ".join(
        f"{source}={expected_rows_by_source[source]}" for source in sources
    )

    lines = [
        f"# {title}：结果分析",
        "",
        "## 1. 分析口径",
        "",
        f"- 方法：{method}；模型：`{model}`。",
        (
            f"- 总样本：{len(sources)} 个 source × 4 个耦合 Q/(S=V) cells = "
            f"{expected_total:,} realizations（logical counts：{counts_text}）。"
        ),
        (
            "- Full 仅包含 `S_en--V_en` 与 `S_zh--V_zh`；S/V 不同时变化，因此报告 "
            "ΔQ、耦合 ΔDB（`Acc(S=V=en)-Acc(S=V=zh)`）和 Q-DB match gap，"
            "不把 ΔS/ΔV 解释为独立因子效应。"
        ),
        "- accuracy 均为 realization-level micro execution accuracy；另报告 source macro。",
        "",
        "## 2. 核心结果",
        "",
        "| 指标 | 数值 |",
        "|---|---:|",
        f"| Overall Exec Acc (micro) | {_fmt_acc(metrics['overall'])} |",
        f"| Source Macro Acc | {_pct(source_macro)} |",
        (
            f"| Valid SQL Rate | {operations['valid_sql']}/{metrics['overall']['total']} = "
            f"{_pct(operations['valid_sql_rate'])} |"
        ),
        f"| ΔQ (en−zh) | {_pp(gaps['delta_q_en_minus_zh'])} |",
        f"| ΔDB (en−zh, coupled S=V) | {_pp(gaps['delta_db_en_minus_zh'])} |",
        f"| Q-DB Match Gap | {_pp(gaps['q_db_match_gap'])} |",
        "",
        "## 3. 四格 Micro Exec Acc",
        "",
        "| Cell | Correct / Total | Accuracy |",
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
        "## 4. 问题语言与 DB 语言",
        "",
        "| 对比 | 第一组 | 第二组 | Gap（第一组−第二组） |",
        "|---|---:|---:|---:|",
        (
            f"| Q language | en {_pct(metrics['q_en']['accuracy'])} | "
            f"zh {_pct(metrics['q_zh']['accuracy'])} | {_pp(gaps['delta_q_en_minus_zh'])} |"
        ),
        (
            f"| DB language (S=V) | en {_pct(metrics['db_en']['accuracy'])} | "
            f"zh {_pct(metrics['db_zh']['accuracy'])} | {_pp(gaps['delta_db_en_minus_zh'])} |"
        ),
        (
            f"| Q-DB relation | match {_pct(metrics['q_db_match']['accuracy'])} | "
            f"mismatch {_pct(metrics['q_db_mismatch']['accuracy'])} | "
            f"{_pp(gaps['q_db_match_gap'])} |"
        ),
        "",
        "固定 Q 后的耦合 DB 切换（`Acc(S=V=en) - Acc(S=V=zh)`）：",
        "",
        "| 固定条件 | DB=en | DB=zh | ΔDB |",
        "|---|---:|---:|---:|",
    ]
    for question in ("en", "zh"):
        en_cell = f"Q_{question}--S_en--V_en"
        zh_cell = f"Q_{question}--S_zh--V_zh"
        en_acc = overall_cells[en_cell]["accuracy"]
        zh_acc = overall_cells[zh_cell]["accuracy"]
        lines.append(
            f"| Q={question} | {_pct(en_acc)} | {_pct(zh_acc)} | {_pp(en_acc - zh_acc)} |"
        )

    lines += [
        "",
        "固定 DB 后的问题语言切换（`Acc(Q=en) - Acc(Q=zh)`）：",
        "",
        "| 固定条件 | Q=en | Q=zh | ΔQ |",
        "|---|---:|---:|---:|",
    ]
    for db in ("en", "zh"):
        en_cell = f"Q_en--S_{db}--V_{db}"
        zh_cell = f"Q_zh--S_{db}--V_{db}"
        en_acc = overall_cells[en_cell]["accuracy"]
        zh_acc = overall_cells[zh_cell]["accuracy"]
        lines.append(
            f"| DB={db} | {_pct(en_acc)} | {_pct(zh_acc)} | {_pp(en_acc - zh_acc)} |"
        )

    lines += [
        "",
        "## 5. Source 分解",
        "",
        "| Source | Exec Acc | ΔQ | ΔDB | Q-DB gap | Valid SQL |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for row in source_rows:
        lines.append(
            f"| {row['source']} | {row['correct']}/{row['total']} = {_pct(row['accuracy'])} | "
            f"{_pp(row['delta_q'])} | {_pp(row['delta_db'])} | {_pp(row['q_db_gap'])} | "
            f"{_pct(row['valid_sql_rate'])} |"
        )

    if source_rows:
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

    if "bull" in source_summaries:
        bull_summary = source_summaries["bull"]
        bull_cells = {row["cell"]: row for row in cell_rows if row["source"] == "bull"}
        lines += [
            "",
            "## 6. BULL 四格",
            "",
            "| BULL cell | Correct / Total | Accuracy |",
            "|---|---:|---:|",
        ]
        for cell in cells:
            row = bull_cells[cell]
            lines.append(
                f"| `{cell}` | {row['correct']}/{row['total']} | {_pct(row['accuracy'])} |"
            )
        lines += [
            "",
            (
                f"BULL overall：{_pct(bull_summary['metrics']['overall']['accuracy'])}；"
                f"ΔQ={_pp(bull_summary['gaps']['delta_q_en_minus_zh'])}，"
                f"ΔDB={_pp(bull_summary['gaps']['delta_db_en_minus_zh'])}，"
                f"Q-DB gap={_pp(bull_summary['gaps']['q_db_match_gap'])}。"
            ),
        ]

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
        f"1. Overall Exec Acc (micro) = {_fmt_acc(metrics['overall'])}；"
        f"source macro = {_pct(source_macro)}。",
        (
            f"2. 可识别对比：ΔQ={_pp(gaps['delta_q_en_minus_zh'])}，"
            f"ΔDB={_pp(gaps['delta_db_en_minus_zh'])}，"
            f"Q-DB match gap={_pp(gaps['q_db_match_gap'])}。"
        ),
        "3. 不要把 Full 的 DB 语言切换解读为独立 schema 或 value 效应；那需要 Cube 八格。",
        "4. Source 规模与难度差异大，解释语言效应时应优先看 per-source 分解。",
        "",
        "## 10. 可复现文件",
        "",
        "- `summary.json`：完整聚合结果。",
        "- `cells.csv`：source/cell 结果。",
        "- `sources.csv`：五源 ΔQ / ΔDB / Q-DB gap。",
        "- `report.md`：本报告。",
        "",
    ]
    return "\n".join(lines)
