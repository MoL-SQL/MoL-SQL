#!/usr/bin/env python3
"""
Apply the LLM-suggested ``revised_sql`` from ``nl2sql_debug.py`` back onto a
Spider-style dataset split, producing a ``<split>_revised.json``.

The debug output (a JSON list emitted by ``nl2sql_debug.py``) carries one record
per sample with an ``index`` aligned to the original dataset order plus a
``revised_sql`` field. For each matched sample we overwrite the dataset's SQL
field (``query`` by default) with the revised SQL. Samples without a usable
revision keep their original SQL.
"""

import argparse
import json
import os
import sys
from typing import Any, Dict, List


def load_json_list(path: str, label: str) -> List[Dict[str, Any]]:
    if not os.path.isfile(path):
        print(f"{label} file not found: {path}", file=sys.stderr)
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        print(f"Expected a JSON list in {path}", file=sys.stderr)
        sys.exit(1)
    return data


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Replace dataset SQL with revised SQL from nl2sql_debug.py")
    parser.add_argument("--dataset", required=True,
                        help="Original split JSON (e.g. .../spider_cnq_end/dev.json)")
    parser.add_argument("--debug", required=True,
                        help="Debug result JSON emitted by nl2sql_debug.py")
    parser.add_argument("--output", required=True,
                        help="Output revised split JSON path")
    parser.add_argument("--sql_field", default="query",
                        help="Dataset field holding the SQL to replace (default: query)")
    parser.add_argument("--only-buggy", action="store_true",
                        help="Only replace SQL when the debug result is 'False' "
                             "(skip samples judged correct)")
    parser.add_argument("--limit", type=int, default=None,
                        help="Only keep (and revise) the first N samples in the output")
    args = parser.parse_args()

    examples = load_json_list(args.dataset, "Dataset")
    debug = load_json_list(args.debug, "Debug result")

    if args.limit is not None:
        examples = examples[: args.limit]

    debug_by_index: Dict[int, Dict[str, Any]] = {}
    for position, row in enumerate(debug):
        index = row.get("index", position)
        try:
            index = int(index)
        except (TypeError, ValueError):
            print(f"Debug row {position} has invalid index: {index!r}", file=sys.stderr)
            sys.exit(1)
        debug_by_index[index] = row

    replaced = 0
    skipped_correct = 0
    missing_revision = 0
    for idx, entry in enumerate(examples):
        row = debug_by_index.get(idx)
        if row is None:
            continue

        result = str(row.get("result", "")).strip().lower()
        if args.only_buggy and result != "false":
            skipped_correct += 1
            continue

        revised = (row.get("revised_sql") or "").strip()
        if not revised:
            missing_revision += 1
            continue

        original = entry.get(args.sql_field)
        if isinstance(original, str) and original.strip() == revised:
            continue

        entry[args.sql_field] = revised
        replaced += 1

    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(examples, f, ensure_ascii=False, indent=2)

    print(
        f"Wrote {len(examples)} samples to {args.output} "
        f"(replaced={replaced}, skipped_correct={skipped_correct}, "
        f"missing_revision={missing_revision})",
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()
