#!/usr/bin/env python3
"""
Summarize SQL validation results.

The main input is the JSON list emitted by ``nl2sql_debug.py``. When paired with
the sample-level execution cache from ``check_empty_sql.py``, this script assigns
each sample exactly one major type: exec error, exec empty, semantic error, or
correct.
"""

import argparse
import json
import os
import sys
from collections import Counter
from typing import Any, Dict, Iterable, List, Optional, Tuple


EXEC_ERROR = "exec error"
EXEC_EMPTY = "exec empty"
SEMANTIC_ERROR = "semantic error"
CORRECT = "correct"
MAJOR_TYPES = (EXEC_ERROR, EXEC_EMPTY, SEMANTIC_ERROR, CORRECT)
EXEC_ERROR_STATUSES = {"error", "no_db", "skipped"}
EXEC_EMPTY_STATUSES = {"empty"}


def normalize_result(value: Any) -> str:
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


def iter_error_types(value: Any) -> Iterable[Tuple[str, str]]:
    if isinstance(value, list):
        for item in value:
            if isinstance(item, dict):
                error_type = str(item.get("error_type", "")).strip()
                sub_error_type = str(item.get("sub_error_type", "")).strip()
                if error_type or sub_error_type:
                    yield error_type or "unknown", sub_error_type or "unknown"
            else:
                label = str(item).strip()
                if label:
                    yield label, ""
    elif isinstance(value, str):
        label = value.strip()
        if label:
            yield label, ""


def _index_by_sample(results: List[Dict[str, Any]], source: str) -> Dict[int, Dict[str, Any]]:
    indexed: Dict[int, Dict[str, Any]] = {}
    for position, row in enumerate(results):
        index = row.get("index", position)
        try:
            index = int(index)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"{source} row {position} has invalid index: {index!r}") from exc
        if index in indexed:
            raise ValueError(f"{source} has duplicate sample index: {index}")
        indexed[index] = row
    return indexed


def _same_key(left: Dict[str, Any], right: Dict[str, Any], keys: Iterable[str]) -> bool:
    for key in keys:
        left_value = left.get(key)
        right_value = right.get(key)
        if left_value not in (None, "") and right_value not in (None, ""):
            if str(left_value) != str(right_value):
                return False
    return True


def classify_major_type(debug_row: Optional[Dict[str, Any]],
                        exec_row: Optional[Dict[str, Any]]) -> str:
    exec_status = (exec_row or {}).get("exec_status")
    exec_status = str(exec_status).strip().lower() if exec_status is not None else ""

    if exec_status in EXEC_ERROR_STATUSES:
        return EXEC_ERROR
    if exec_status in EXEC_EMPTY_STATUSES:
        return EXEC_EMPTY

    result = normalize_result((debug_row or {}).get("result"))
    if result == "true":
        return CORRECT
    return SEMANTIC_ERROR


def build_sample_classifications(
    debug_results: List[Dict[str, Any]],
    exec_results: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    debug_by_index = _index_by_sample(debug_results, "nl2sql debug input")
    exec_by_index = _index_by_sample(exec_results, "check sql input")

    missing_exec = sorted(set(debug_by_index) - set(exec_by_index))
    if missing_exec:
        preview = ", ".join(str(i) for i in missing_exec[:10])
        raise ValueError(f"Missing execution results for sample indices: {preview}")

    classifications: List[Dict[str, Any]] = []
    for index in sorted(debug_by_index):
        debug_row = debug_by_index[index]
        exec_row = exec_by_index[index]
        if not _same_key(debug_row, exec_row, ("q_id", "db_id", "db_name")):
            raise ValueError(f"Sample key mismatch at index {index}")

        major_type = classify_major_type(debug_row, exec_row)
        classifications.append({
            "index": index,
            "q_id": debug_row.get("q_id", exec_row.get("q_id")),
            "db_id": debug_row.get("db_id", exec_row.get("db_id")),
            "question": debug_row.get("question", exec_row.get("question", "")),
            "gold_sql": debug_row.get("gold_sql", exec_row.get("sql", "")),
            "exec_status": exec_row.get("exec_status"),
            "row_count": exec_row.get("row_count"),
            "result": debug_row.get("result"),
            "error_types": debug_row.get("error_types", []),
            "major_type": major_type,
        })

    return classifications


def build_summary(
    results: List[Dict[str, Any]],
    input_path: str,
    check_sql_path: Optional[str] = None,
    check_sql_results: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    result_counts = Counter(normalize_result(row.get("result")) for row in results)

    total = len(results)
    valid_count = result_counts.get("true", 0)
    buggy_count = result_counts.get("false", 0)

    summary = {
        "input": input_path,
        "check_sql_input": check_sql_path,
        "total": total,
        "valid_count": valid_count,
        "buggy_count": buggy_count,
        "unknown_count": total - valid_count - buggy_count,
        "result_counts": dict(sorted(result_counts.items())),
    }

    if check_sql_results is not None:
        classifications = build_sample_classifications(results, check_sql_results)
        major_type_counts = Counter(row["major_type"] for row in classifications)
        semantic_error_type_counts = Counter(
            error_type
            for row in classifications
            if row["major_type"] == SEMANTIC_ERROR
            for error_type in iter_error_types(row.get("error_types"))
        )
        summary["major_type_counts"] = {
            label: major_type_counts.get(label, 0)
            for label in MAJOR_TYPES
        }
        summary["semantic_error_type_counts"] = [
            {
                "error_type": error_type,
                "sub_error_type": sub_error_type,
                "count": count,
            }
            for (error_type, sub_error_type), count
            in sorted(semantic_error_type_counts.items())
        ]
        summary["classified_samples"] = classifications
    else:
        semantic_error_type_counts = Counter(
            error_type
            for row in results
            if normalize_result(row.get("result")) == "false"
            for error_type in iter_error_types(row.get("error_types"))
        )
        summary["semantic_error_type_counts"] = [
            {
                "error_type": error_type,
                "sub_error_type": sub_error_type,
                "count": count,
            }
            for (error_type, sub_error_type), count
            in sorted(semantic_error_type_counts.items())
        ]

    return summary


def print_table(headers: List[str], rows: List[List[Any]]) -> None:
    table_rows = [[str(cell) for cell in row] for row in rows]
    widths = [
        max(len(header), *(len(row[index]) for row in table_rows))
        if table_rows else len(header)
        for index, header in enumerate(headers)
    ]

    def format_row(row: List[str]) -> str:
        return " | ".join(cell.ljust(widths[index]) for index, cell in enumerate(row))

    print(format_row(headers))
    print("-+-".join("-" * width for width in widths))
    for row in table_rows:
        print(format_row(row))


def print_summary(summary: Dict[str, Any]) -> None:
    if "major_type_counts" in summary:
        print("Major type counts:")
        print_table(
            ["major_type", "count"],
            [[label, count] for label, count in summary["major_type_counts"].items()],
        )
    else:
        print("Major type counts:")
        print_table(
            ["major_type", "count"],
            [
                ["correct", summary["valid_count"]],
                ["semantic error", summary["buggy_count"]],
                ["unknown", summary["unknown_count"]],
            ],
        )

    print()
    print("Semantic error type counts:")
    semantic_sample_count = summary.get("major_type_counts", {}).get(
        SEMANTIC_ERROR,
        summary["buggy_count"],
    )
    print(
        "NOTE: one sample can have multiple semantic errors, "
        f"so counts may sum to more than semantic error samples ({semantic_sample_count})."
    )
    semantic_error_type_counts = summary.get("semantic_error_type_counts", [])
    print_table(
        ["error_type", "sub_error_type", "count"],
        [
            [row["error_type"], row["sub_error_type"], row["count"]]
            for row in semantic_error_type_counts
        ] or [["none", "", 0]],
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Summarize results from script/data_validation/nl2sql_debug.py")
    parser.add_argument("--input", required=True,
                        help="JSON result path emitted by nl2sql_debug.py")
    parser.add_argument("--check-sql-input", default=None,
                        help="Optional sample-level JSON emitted by check_empty_sql.py "
                             "--output-sample-json")
    parser.add_argument("--output", default=None,
                        help="Optional JSON summary output path")
    args = parser.parse_args()

    if not os.path.isfile(args.input):
        print(f"Input result file not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    with open(args.input, "r", encoding="utf-8") as f:
        results = json.load(f)

    if not isinstance(results, list):
        print(f"Expected a JSON list in {args.input}", file=sys.stderr)
        sys.exit(1)

    check_sql_results = None
    if args.check_sql_input:
        if not os.path.isfile(args.check_sql_input):
            print(f"Check SQL result file not found: {args.check_sql_input}", file=sys.stderr)
            sys.exit(1)
        with open(args.check_sql_input, "r", encoding="utf-8") as f:
            check_sql_results = json.load(f)
        if not isinstance(check_sql_results, list):
            print(f"Expected a JSON list in {args.check_sql_input}", file=sys.stderr)
            sys.exit(1)

    try:
        summary = build_summary(
            results,
            args.input,
            check_sql_path=args.check_sql_input,
            check_sql_results=check_sql_results,
        )
    except ValueError as exc:
        print(f"Failed to build statistics: {exc}", file=sys.stderr)
        sys.exit(1)
    print_summary(summary)

    if args.output:
        os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
        omit_keys = {"valid_count", "buggy_count", "unknown_count", "result_counts"}
        output_summary = {k: v for k, v in summary.items() if k not in omit_keys}
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(output_summary, f, ensure_ascii=False, indent=2)
        print(f"Wrote statistics to {args.output}")


if __name__ == "__main__":
    main()
