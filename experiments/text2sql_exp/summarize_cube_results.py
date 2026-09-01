#!/usr/bin/env python3
"""Summarize MoL-Cube evaluation JSON files into Main-style Exec Acc tables."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Sequence

from cube_common import (
    CELLS,
    SOURCES,
    CellPackage,
    dump_json,
    parse_cell,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_roots", type=Path, nargs="+")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--source",
        default=None,
        help="Restrict the summary to one Cube source, e.g. bird",
    )
    return parser.parse_args()


def load_cell_accuracy(path: Path) -> tuple[float, int]:
    with path.open("r", encoding="utf-8") as file:
        payload = json.load(file)
    total = payload["statistic"]["total"]
    return float(total["exec"]), int(total["count"])


def weighted_accuracy(rows: list[dict], predicate=None) -> tuple[float, int]:
    selected = [row for row in rows if predicate is None or predicate(row)]
    count = sum(row["count"] for row in selected)
    correct = sum(row["accuracy"] * row["count"] for row in selected)
    return ((correct / count) if count else 0.0, count)


def source_evaluations_complete(
    run_root: Path,
    source: str,
    cells: Sequence[str] | None = None,
) -> bool:
    selected_cells = tuple(cells) if cells is not None else CELLS
    return all(
        (run_root / source / cell / "evaluation/evaluation.json").exists()
        for cell in selected_cells
    )


def summarize_run(
    run_root: Path,
    sources: Sequence[str] | None = None,
) -> dict:
    manifest_path = run_root / "run_manifest.json"
    with manifest_path.open("r", encoding="utf-8") as file:
        manifest = json.load(file)

    selected_sources = tuple(sources) if sources is not None else SOURCES
    rows = []
    for source in selected_sources:
        for cell in CELLS:
            eval_path = run_root / source / cell / "evaluation/evaluation.json"
            if not eval_path.exists():
                continue
            accuracy, count = load_cell_accuracy(eval_path)
            axes = parse_cell(cell)
            rows.append(
                {
                    "source": source,
                    "cell": cell,
                    "Q": axes["Q"],
                    "S": axes["S"],
                    "V": axes["V"],
                    "qs_match": axes["Q"] == axes["S"],
                    "accuracy": accuracy,
                    "count": count,
                }
            )
    if not rows:
        raise ValueError(f"No evaluation files found under {run_root}")

    metrics = {}
    for name, predicate in (
        ("overall", None),
        ("q_en", lambda row: row["Q"] == "en"),
        ("q_zh", lambda row: row["Q"] == "zh"),
        ("s_en", lambda row: row["S"] == "en"),
        ("s_zh", lambda row: row["S"] == "zh"),
        ("v_en", lambda row: row["V"] == "en"),
        ("v_zh", lambda row: row["V"] == "zh"),
        ("qs_match", lambda row: row["qs_match"]),
        ("qs_mismatch", lambda row: not row["qs_match"]),
    ):
        accuracy, count = weighted_accuracy(rows, predicate)
        metrics[name] = {"exec": accuracy, "count": count}

    metrics["delta_q"] = metrics["q_en"]["exec"] - metrics["q_zh"]["exec"]
    metrics["delta_s"] = metrics["s_en"]["exec"] - metrics["s_zh"]["exec"]
    metrics["delta_v"] = metrics["v_en"]["exec"] - metrics["v_zh"]["exec"]
    metrics["delta_qs_mismatch"] = (
        metrics["qs_match"]["exec"] - metrics["qs_mismatch"]["exec"]
    )

    per_source = {}
    for source in sorted({row["source"] for row in rows}):
        source_rows = [row for row in rows if row["source"] == source]
        accuracy, count = weighted_accuracy(source_rows)
        per_source[source] = {"exec": accuracy, "count": count}

    cell_metrics = {
        f"{row['source']}/{row['cell']}": {
            "exec": row["accuracy"],
            "count": row["count"],
        }
        for row in rows
    }
    return {
        "method": manifest.get("method"),
        "model": manifest.get("model"),
        "api_profile": manifest.get("api_profile"),
        "run_root": str(run_root),
        "summarized_sources": list(selected_sources),
        "metrics": metrics,
        "per_source": per_source,
        "cells": cell_metrics,
    }


def write_csv(path: Path, summaries: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    columns = (
        "method",
        "model",
        "api_profile",
        "overall",
        "q_en",
        "q_zh",
        "s_en",
        "s_zh",
        "v_en",
        "v_zh",
        "qs_match",
        "qs_mismatch",
        "delta_q",
        "delta_s",
        "delta_v",
        "delta_qs_mismatch",
    )
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        for summary in summaries:
            metrics = summary["metrics"]
            writer.writerow(
                {
                    "method": summary["method"],
                    "model": summary["model"],
                    "api_profile": summary["api_profile"],
                    "overall": metrics["overall"]["exec"],
                    "q_en": metrics["q_en"]["exec"],
                    "q_zh": metrics["q_zh"]["exec"],
                    "s_en": metrics["s_en"]["exec"],
                    "s_zh": metrics["s_zh"]["exec"],
                    "v_en": metrics["v_en"]["exec"],
                    "v_zh": metrics["v_zh"]["exec"],
                    "qs_match": metrics["qs_match"]["exec"],
                    "qs_mismatch": metrics["qs_mismatch"]["exec"],
                    "delta_q": metrics["delta_q"],
                    "delta_s": metrics["delta_s"],
                    "delta_v": metrics["delta_v"],
                    "delta_qs_mismatch": metrics["delta_qs_mismatch"],
                }
            )


def write_accuracy_summary(
    run_root: Path,
    output: Path,
    *,
    sources: Sequence[str] | None = None,
) -> tuple[Path, Path]:
    summary = summarize_run(run_root, sources=sources)
    output_json = output.with_suffix(".json")
    output_csv = output.with_suffix(".csv")
    dump_json(output_json, {"runs": [summary]})
    write_csv(output_csv, [summary])
    print(f"Wrote {output_json}", file=sys.stderr)
    print(f"Wrote {output_csv}", file=sys.stderr)
    return output_json, output_csv


def write_source_accuracy_summary(
    run_root: Path,
    source: str,
    cells: Sequence[str] | None = None,
) -> tuple[Path, Path]:
    selected_cells = tuple(cells) if cells is not None else CELLS
    if not source_evaluations_complete(run_root, source, selected_cells):
        raise ValueError(f"Incomplete evaluations for {source} under {run_root}")
    return write_accuracy_summary(
        run_root,
        run_root / source / "accuracy_summary",
        sources=(source,),
    )


def maybe_write_source_accuracy_summary(
    run_root: Path,
    packages: Sequence[CellPackage],
    index: int,
    *,
    eval_enabled: bool,
    dry_run: bool,
) -> None:
    """Write ``<run_root>/<source>/accuracy_summary`` when a source's selected cells finish."""
    if dry_run or not eval_enabled:
        return
    if index < 0 or index >= len(packages):
        return
    if index + 1 < len(packages) and packages[index + 1].source == packages[index].source:
        return
    source = packages[index].source
    source_cells = tuple(package.cell for package in packages if package.source == source)
    if not source_evaluations_complete(run_root, source, source_cells):
        return
    write_source_accuracy_summary(run_root, source, source_cells)


def main() -> None:
    args = parse_args()
    sources = (args.source,) if args.source else None
    if sources is not None and sources[0] not in SOURCES:
        raise SystemExit(f"Unsupported Cube source: {args.source}")
    summaries = [
        summarize_run(path.resolve(), sources=sources) for path in args.run_roots
    ]
    output_json = args.output.with_suffix(".json")
    output_csv = args.output.with_suffix(".csv")
    dump_json(output_json, {"runs": summaries})
    write_csv(output_csv, summaries)
    print(f"Wrote {output_json}")
    print(f"Wrote {output_csv}")


if __name__ == "__main__":
    main()
