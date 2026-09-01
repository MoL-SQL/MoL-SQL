#!/usr/bin/env python3
"""
Step 3 of data validation: cross-dataset comparison.

The benchmarks validated by steps 1-2 (e.g. ``spider`` / ``cspider`` /
``multispider`` / ``spider_cnq_end``) are parallel language variants of the same
underlying examples: they share the gold SQL and are aligned by sample index,
differing only in the natural-language question. This step lines those variants
up and flags every sample whose gold SQL is *not* judged correct uniformly
across all datasets, so disagreements (correct in one language but buggy in
another) and globally broken samples surface for manual review.

Input is the per-dataset JSON written by ``statistic_validation.py`` (which
embeds ``classified_samples`` with a ``major_type`` per sample). A raw
``nl2sql_debug.py`` result list is also accepted as a fallback, in which case
correctness is read from the boolean ``result`` field.

Algorithm (mirrors the spec):
    take the sample id list of the reference dataset (default: first input)
    for each sample id
        for each dataset in the dataset list
            if the sample is correct in all datasets, continue
            if the sample is incorrect in any dataset, emit a record:
                {
                    "sample_id": ...,
                    "correct_datasets": [...],
                    "incorrect_datasets": [...],
                    "sample_info": [{dataset, question, gold_sql, exec_result}, ...],
                    "error_details": [{dataset, error_detail}, ...],
                }
"""

import argparse
import json
import os
import sys
from typing import Any, Dict, List, Optional, Tuple


CORRECT = "correct"


def normalize_result(value: Any) -> str:
    """Collapse the LLM ``result`` field to 'true' / 'false' / 'none' / 'other'."""
    if isinstance(value, bool):
        return str(value).lower()
    if value is None:
        return "none"
    normalized = str(value).strip().lower()
    if normalized in {"true", "false"}:
        return normalized
    if not normalized:
        return "none"
    return "other"


def parse_input_spec(spec: str) -> Tuple[str, str]:
    """Parse a ``name=path`` (or bare ``path``) input specification."""
    if "=" in spec:
        name, path = spec.split("=", 1)
        name, path = name.strip(), path.strip()
        if name and path:
            return name, path
    path = spec.strip()
    name = os.path.basename(path)
    for suffix in ("_stats.json", ".json"):
        if name.endswith(suffix):
            name = name[: -len(suffix)]
            break
    return name or path, path


def load_samples(path: str) -> List[Dict[str, Any]]:
    """Return the per-sample list from a stats file or a raw debug result file."""
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, dict):
        samples = data.get("classified_samples")
        if samples is None:
            raise ValueError(
                f"{path}: object input has no 'classified_samples' "
                f"(is this a statistic_validation.py output?)"
            )
        if not isinstance(samples, list):
            raise ValueError(f"{path}: 'classified_samples' is not a list")
        return samples
    if isinstance(data, list):
        return data
    raise ValueError(f"{path}: expected a JSON object or list")


def index_by_sample_id(samples: List[Dict[str, Any]], source: str) -> Dict[int, Dict[str, Any]]:
    indexed: Dict[int, Dict[str, Any]] = {}
    for position, row in enumerate(samples):
        raw_index = row.get("index", position)
        try:
            sample_id = int(raw_index)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"{source} row {position} has invalid index: {raw_index!r}") from exc
        if sample_id in indexed:
            raise ValueError(f"{source} has duplicate sample index: {sample_id}")
        indexed[sample_id] = row
    return indexed


def is_correct(row: Optional[Dict[str, Any]]) -> Optional[bool]:
    """True/False correctness for a sample, or None when the sample is absent.

    Prefer the step-2 ``major_type`` (which folds in execution errors / empty
    results), and fall back to the raw boolean ``result`` field.
    """
    if row is None:
        return None
    major_type = row.get("major_type")
    if major_type is not None:
        return str(major_type).strip().lower() == CORRECT
    return normalize_result(row.get("result")) == "true"


def build_exec_result(row: Dict[str, Any]) -> str:
    """Compose a compact execution-result string from the available fields."""
    if "exec_result" in row and row["exec_result"] not in (None, ""):
        return str(row["exec_result"])
    status = row.get("exec_status")
    if status in (None, ""):
        return "unknown"
    parts = [str(status)]
    row_count = row.get("row_count")
    if row_count is not None:
        parts.append(f"rows={row_count}")
    exec_error = row.get("exec_error")
    if exec_error:
        parts.append(f"error={exec_error}")
    return " ".join(parts)


def build_error_detail(row: Dict[str, Any]) -> Dict[str, Any]:
    """Summarize *why* the gold SQL is considered incorrect in this dataset."""
    detail: Dict[str, Any] = {
        "major_type": row.get("major_type"),
        "result": row.get("result"),
        "error_types": row.get("error_types", []),
    }
    if row.get("exec_status") not in (None, ""):
        detail["exec_status"] = row.get("exec_status")
    reasoning = row.get("reasoning")
    if reasoning:
        detail["reasoning"] = reasoning
    return detail


def compare(
    datasets: List[Tuple[str, Dict[int, Dict[str, Any]]]],
    reference: str,
    include_consistent_incorrect: bool = True,
) -> Dict[str, Any]:
    ref_index = next((idx for idx, (name, _) in enumerate(datasets) if name == reference), None)
    if ref_index is None:
        raise ValueError(
            f"reference dataset '{reference}' not in inputs: "
            f"{[name for name, _ in datasets]}"
        )
    _, ref_samples = datasets[ref_index]

    flagged: List[Dict[str, Any]] = []
    inconsistent_count = 0
    all_incorrect_count = 0

    for sample_id in sorted(ref_samples):
        rows: List[Tuple[str, Optional[Dict[str, Any]]]] = [
            (name, samples.get(sample_id)) for name, samples in datasets
        ]

        correct_datasets: List[str] = []
        incorrect_datasets: List[str] = []
        missing_datasets: List[str] = []
        for name, row in rows:
            verdict = is_correct(row)
            if verdict is None:
                missing_datasets.append(name)
            elif verdict:
                correct_datasets.append(name)
            else:
                incorrect_datasets.append(name)

        # Correct everywhere it appears -> nothing to report.
        if not incorrect_datasets:
            continue
        if correct_datasets:
            inconsistent_count += 1
        else:
            all_incorrect_count += 1
            if not include_consistent_incorrect:
                continue

        sample_info = [
            {
                "dataset": name,
                "question": row.get("question", ""),
                "gold_sql": row.get("gold_sql", ""),
                "exec_result": build_exec_result(row),
            }
            for name, row in rows
            if row is not None
        ]
        error_details = [
            {"dataset": name, "error_detail": build_error_detail(row)}
            for name, row in rows
            if row is not None and is_correct(row) is False
        ]

        flagged.append({
            "sample_id": sample_id,
            "correct_datasets": correct_datasets,
            "incorrect_datasets": incorrect_datasets,
            "missing_datasets": missing_datasets,
            "sample_info": sample_info,
            "error_details": error_details,
        })

    return {
        "datasets": [name for name, _ in datasets],
        "reference": reference,
        "reference_total": len(ref_samples),
        "flagged_total": len(flagged),
        "inconsistent_count": inconsistent_count,
        "all_incorrect_count": all_incorrect_count,
        "flagged_samples": flagged,
    }


def print_report(report: Dict[str, Any]) -> None:
    print(f"Datasets compared : {', '.join(report['datasets'])}")
    print(f"Reference dataset : {report['reference']} "
          f"({report['reference_total']} samples)")
    print(f"Flagged samples   : {report['flagged_total']}")
    print(f"  inconsistent (correct somewhere, wrong elsewhere): "
          f"{report['inconsistent_count']}")
    print(f"  incorrect in every dataset                       : "
          f"{report['all_incorrect_count']}")

    if not report["flagged_samples"]:
        return
    print()
    print("Inconsistent samples (correct in some datasets, incorrect in others):")
    shown = 0
    for sample in report["flagged_samples"]:
        if not sample["correct_datasets"]:
            continue
        shown += 1
        if shown > 20:
            remaining = report["inconsistent_count"] - 20
            if remaining > 0:
                print(f"  ... and {remaining} more")
            break
        print(f"  id={sample['sample_id']:>5}  "
              f"correct={sample['correct_datasets']}  "
              f"incorrect={sample['incorrect_datasets']}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compare gold-SQL validation results across parallel datasets")
    parser.add_argument(
        "--input", dest="inputs", action="append", required=True,
        metavar="NAME=PATH",
        help="Per-dataset stats JSON (statistic_validation.py output) or raw "
             "nl2sql_debug.py result list. May be given multiple times. "
             "Use NAME=PATH to label the dataset, or a bare path to infer it.")
    parser.add_argument(
        "--reference", default=None,
        help="Dataset name whose sample ids drive the comparison "
             "(default: first --input).")
    parser.add_argument(
        "--output", default=None,
        help="Optional JSON report output path.")
    parser.add_argument(
        "--only-inconsistent", action="store_true",
        help="Report only samples that disagree across datasets (drop samples "
             "that are incorrect in every dataset).")
    args = parser.parse_args()

    datasets: List[Tuple[str, Dict[int, Dict[str, Any]]]] = []
    seen_names: set = set()
    for spec in args.inputs:
        name, path = parse_input_spec(spec)
        if not os.path.isfile(path):
            print(f"Input file not found: {path}", file=sys.stderr)
            sys.exit(1)
        if name in seen_names:
            print(f"Duplicate dataset name: {name}", file=sys.stderr)
            sys.exit(1)
        seen_names.add(name)
        try:
            samples = load_samples(path)
            indexed = index_by_sample_id(samples, path)
        except ValueError as exc:
            print(f"Failed to load {path}: {exc}", file=sys.stderr)
            sys.exit(1)
        datasets.append((name, indexed))

    if len(datasets) < 2:
        print("Need at least two --input datasets to compare", file=sys.stderr)
        sys.exit(1)

    reference = args.reference or datasets[0][0]
    try:
        report = compare(
            datasets,
            reference,
            include_consistent_incorrect=not args.only_inconsistent,
        )
    except ValueError as exc:
        print(f"Failed to compare datasets: {exc}", file=sys.stderr)
        sys.exit(1)

    print_report(report)

    if args.output:
        os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"\nWrote comparison report to {args.output}")


if __name__ == "__main__":
    main()
