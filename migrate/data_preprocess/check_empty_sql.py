#!/usr/bin/env python3
"""
Audit a BULL-FinSQL-style ``dev.json`` for gold SQL whose execution result is
empty.

Why
---
A non-trivial fraction of BULL gold queries return ``[]`` against the shipped
sqlite databases.  Empty-result samples are problematic for downstream EX
evaluation because *any* prediction (even a wildly wrong one) that also returns
``[]`` will be scored as correct.  This script flags such samples up front so
they can be reviewed / filtered before evaluation.

What it does
------------
For every entry in ``<input>/dev.json``:

1. Open ``<input>/database/<db_name>/<db_name>.sqlite``.
2. Execute the entry's ``sql_query`` (``query`` fallback) **as stored in JSON**
   — no literal rewriting or normalization.
3. Bucket the entry as one of:

   * ``empty``       — query ran, ``cursor.fetchall()`` returned ``[]``
   * ``non_empty``   — query ran, returned >= 1 row
   * ``has_null``    — query ran, >=1 result cell is ``NULL``
   * ``error``       — query raised (syntax / missing table / etc.)
   * ``no_db``       — referenced sqlite file does not exist
   * ``skipped``     — entry has no ``sql_query``

Each ``has_null`` / ``empty`` / ``error`` entry can be surfaced; at the end we
print a per-``db_name`` breakdown plus a global total.

Usage
-----
    python -u script/data_preprocess/check_empty_sql.py \\
        --input dataset/BULL-FinSQL-new/BULL-cn-origin-date-reset

Options
-------
    --split           split file basename without ``.json`` (default: ``dev``)
    --timeout         per-query timeout in seconds (default: 30)
    --show-non-empty  also print one line per non-empty entry (verbose)
    --output-json     write the empty-result entries to this JSON path
    --output-sample-json
                     write one execution-status record per sample to this JSON path
    --has-null        check whether query results contain NULL cells
    --delete          when used with --has-null, also deletes has_null entries
"""

from __future__ import annotations

import argparse
import json
import os
import sqlite3
import sys
from collections import defaultdict
from tqdm import tqdm


# ---------------------------------------------------------------------------
# Bucket labels (kept as constants so the summary table stays in sync).
# ---------------------------------------------------------------------------

EMPTY = "empty"
NON_EMPTY = "non_empty"
HAS_NULL = "has_null"
ERROR = "error"
NO_DB = "no_db"
SKIPPED = "skipped"
BUCKETS = (EMPTY, NON_EMPTY, HAS_NULL, ERROR, NO_DB, SKIPPED)


def _db_path(input_dir: str, db_name: str) -> str:
    """Resolve DB file under ``<input>/database/<db_name>/``.

    Preference order:
      1) ``<db_name>.sqlite``
      2) ``<db_name>.db``
      3) any ``*.sqlite`` in the folder
      4) any ``*.db`` in the folder
    """
    folder = os.path.join(input_dir, "database", db_name)
    if not os.path.isdir(folder):
        return ""

    exact_sqlite = os.path.join(folder, f"{db_name}.sqlite")
    if os.path.isfile(exact_sqlite):
        return exact_sqlite

    exact_db = os.path.join(folder, f"{db_name}.db")
    if os.path.isfile(exact_db):
        return exact_db

    for fname in sorted(os.listdir(folder)):
        if fname.endswith(".sqlite"):
            return os.path.join(folder, fname)
    for fname in sorted(os.listdir(folder)):
        if fname.endswith(".db"):
            return os.path.join(folder, fname)
    return ""


def _execute(sql: str, db_file: str, timeout: float, check_has_null: bool) -> tuple[str, object]:
    """Run ``sql`` against ``db_file`` and return ``(bucket, payload)``.

    ``payload`` is the row count for ``empty`` / ``non_empty`` / ``has_null``
    and an error message string for ``error``. ``timeout`` is forwarded to
    :func:`sqlite3.connect` as ``timeout=`` (lock wait) and also enforced as a
    statement-level interrupt via ``conn.set_progress_handler``.
    ``check_has_null`` controls whether result-cell NULL checks are enabled.
    """
    conn = sqlite3.connect(db_file, timeout=timeout)
    try:
        # Best-effort statement timeout: SQLite calls the progress handler
        # roughly every N VM ops; returning non-zero aborts the statement.
        # We compute an op budget from wall time using time.monotonic so that
        # CPU-heavy queries can't run forever.
        import time

        deadline = time.monotonic() + timeout

        def _abort_if_overdue() -> int:
            return 1 if time.monotonic() > deadline else 0

        conn.set_progress_handler(_abort_if_overdue, 1000)

        cursor = conn.cursor()
        try:
            cursor.execute(sql)
            rows = cursor.fetchall()
        except Exception as e:  # noqa: BLE001 — surface any sqlite/runtime err
            return ERROR, f"{type(e).__name__}: {e}"
        n = len(rows)
        if n == 0:
            return EMPTY, n
        if check_has_null and any(cell is None for row in rows for cell in row):
            return HAS_NULL, n
        return NON_EMPTY, n
    finally:
        conn.close()


def _format_summary(per_db: dict[str, dict[str, int]]) -> str:
    """Render the per-``db_name`` breakdown plus a TOTAL row."""
    header = f"{'db_name':<24} " + " ".join(f"{b:>10}" for b in BUCKETS) + f" {'total':>10}"
    lines = [header, "-" * len(header)]

    totals = {b: 0 for b in BUCKETS}
    for db_name in sorted(per_db):
        counts = per_db[db_name]
        row_total = sum(counts.values())
        row = f"{db_name:<24} " + " ".join(f"{counts.get(b, 0):>10}" for b in BUCKETS) + f" {row_total:>10}"
        lines.append(row)
        for b in BUCKETS:
            totals[b] += counts.get(b, 0)

    grand_total = sum(totals.values())
    lines.append("-" * len(header))
    lines.append(
        f"{'TOTAL':<24} " + " ".join(f"{totals[b]:>10}" for b in BUCKETS) + f" {grand_total:>10}"
    )
    return "\n".join(lines)


def check(
    input_dir: str,
    split: str,
    timeout: float,
    show_non_empty: bool,
    check_has_null: bool,
    delete_has_null: bool,
    limit: int | None = None,
) -> tuple[list[dict], dict[str, dict[str, int]], list[int], list[int], list[dict], list[dict]]:
    """Audit ``<input>/<split>.json``.

    Side effect: prints one line per ``has_null`` / ``empty`` / ``error`` /
    ``no_db`` / ``skipped`` entry to stdout as it goes (so users see progress
    on big splits). ``empty_entries`` is the list of original dev.json entries
    whose gold SQL returned no rows; the caller can dump it to a file. Also
    returns the empty entry indices, delete indices, the full loaded split data,
    and sample-level execution records.
    """
    split_path = os.path.join(input_dir, f"{split}.json")
    if not os.path.isfile(split_path):
        raise FileNotFoundError(split_path)

    with open(split_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError(f"Expected a JSON array in {split_path}, got {type(data).__name__}")

    if limit is not None:
        data = data[:limit]

    print(f"[check_empty_sql] {split_path}: {len(data)} entries", file=sys.stderr)

    per_db: dict[str, dict[str, int]] = defaultdict(lambda: {b: 0 for b in BUCKETS})
    empty_entries: list[dict] = []
    empty_indices: list[int] = []
    delete_indices: list[int] = []
    sample_results: list[dict] = []
    missing_dbs: set[str] = set()

    for idx, entry in enumerate(tqdm(data)):
        q_id = entry.get("q_id")
        db_name = (entry.get("db_name") or entry.get("db_id") or "").strip()
        question = entry.get("question", "")
        sql = (entry.get("sql_query") or entry.get("query") or entry.get("SQL") or entry.get("sql") or "").strip()
        sample_result = {
            "index": idx,
            "q_id": q_id,
            "db_id": db_name,
            "db_name": db_name,
            "question": question,
            "sql": sql,
            "exec_status": None,
            "row_count": None,
            "exec_error": "",
            "db_path": "",
        }

        # if "2022-12-31" in sql:
        #     sql = sql.replace("2022-12-31", "2019-12-31")

        if not sql:
            per_db[db_name or "<missing>"][SKIPPED] += 1
            sample_result.update({
                "exec_status": SKIPPED,
                "exec_error": "no sql_query",
            })
            sample_results.append(sample_result)
            print(f"[skipped] q_id={q_id} db={db_name} (no sql_query)")
            continue

        db_file = _db_path(input_dir, db_name) if db_name else ""
        if not db_file or not os.path.isfile(db_file):
            per_db[db_name or "<missing>"][NO_DB] += 1
            db_dir = os.path.join(input_dir, "database", db_name) if db_name else ""
            if not db_name:
                detail = "empty db_name in sample"
            elif not os.path.isdir(db_dir):
                detail = f"missing db directory: {db_dir}"
            elif not db_file:
                detail = f"no .sqlite/.db found under: {db_dir}"
            else:
                detail = f"resolved db path missing: {db_file}"
            sample_result.update({
                "exec_status": NO_DB,
                "exec_error": detail,
                "db_path": db_file,
            })
            sample_results.append(sample_result)
            if db_name not in missing_dbs:
                missing_dbs.add(db_name)
                print(f"[no_db] db={db_name!r} {detail}")
            continue

        bucket, payload = _execute(sql, db_file, timeout, check_has_null=check_has_null)
        per_db[db_name][bucket] += 1
        sample_result.update({
            "exec_status": bucket,
            "row_count": payload if isinstance(payload, int) else None,
            "exec_error": payload if bucket == ERROR else "",
            "db_path": db_file,
        })
        sample_results.append(sample_result)

        if bucket == EMPTY:
            empty_entries.append(entry)
            empty_indices.append(idx)
            delete_indices.append(idx)
            # print(f"[empty] q_id={q_id} db={db_name}")
            # print(f"    Q: {question}")
            # print(f"  SQL: {sql}")
        elif bucket == HAS_NULL:
            print(f"[has_null] q_id={q_id} db={db_name} rows={payload}")
            if delete_has_null:
                delete_indices.append(idx)
        elif bucket == ERROR:
            delete_indices.append(idx)
            # print(f"[error] q_id={q_id} db={db_name}: {payload}")
            # print(f"  SQL: {sql}")
        # elif show_non_empty:
        #     print(f"[ok] q_id={q_id} db={db_name} rows={payload}")

    return empty_entries, per_db, empty_indices, delete_indices, data, sample_results


def _delete_invalid_inplace(input_dir: str, split: str, delete_indices: list[int], data: list[dict]) -> tuple[int, int]:
    """Remove empty/error-result entries from ``<split>.json`` and ``<split>_gold.sql`` in place."""
    if not delete_indices:
        return 0, 0

    delete_set = set(delete_indices)

    split_path = os.path.join(input_dir, f"{split}.json")
    kept_data = [entry for idx, entry in enumerate(data) if idx not in delete_set]
    with open(split_path, "w", encoding="utf-8") as f:
        json.dump(kept_data, f, ensure_ascii=False, indent=2)

    removed_gold = 0
    gold_path = os.path.join(input_dir, f"{split}_gold.sql")
    if os.path.isfile(gold_path):
        with open(gold_path, "r", encoding="utf-8") as f:
            gold_lines = f.readlines()
        if len(gold_lines) == len(data):
            kept_lines = [line for idx, line in enumerate(gold_lines) if idx not in delete_set]
            removed_gold = len(gold_lines) - len(kept_lines)
            with open(gold_path, "w", encoding="utf-8") as f:
                f.writelines(kept_lines)
        else:
            # Best effort fallback when gold line count drifts from split size.
            # Remove by exact "<sql>\\t<db_id>\\n" payload matching.
            to_remove: dict[str, int] = {}
            for idx in delete_indices:
                e = data[idx]
                sql = (e.get("sql_query") or e.get("query") or e.get("SQL") or e.get("sql") or "").strip()
                db_id = (e.get("db_name") or e.get("db_id") or "").strip()
                key = f"{sql}\t{db_id}"
                to_remove[key] = to_remove.get(key, 0) + 1

            kept_lines = []
            for line in gold_lines:
                key = line.rstrip("\n")
                cnt = to_remove.get(key, 0)
                if cnt > 0:
                    to_remove[key] = cnt - 1
                    removed_gold += 1
                else:
                    kept_lines.append(line)
            with open(gold_path, "w", encoding="utf-8") as f:
                f.writelines(kept_lines)

    return len(data) - len(kept_data), removed_gold


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Check how many gold SQL queries in a BULL-FinSQL-style "
                    "split return an empty result set, and break it down by db_name."
    )
    parser.add_argument(
        "--input", required=True,
        help="Dataset directory containing <split>.json and database/<db_id>/<db_id>.sqlite "
             "(e.g. dataset/BULL-FinSQL-new/BULL-cn-origin-date-reset).",
    )
    parser.add_argument(
        "--split", default="dev",
        help="Which split file to audit (default: dev).",
    )
    parser.add_argument(
        "--timeout", type=float, default=30.0,
        help="Per-query timeout in seconds (default: 30).",
    )
    parser.add_argument(
        "--show-non-empty", action="store_true",
        help="Also print a one-line summary for non-empty entries (verbose).",
    )
    parser.add_argument(
        "--output-json", default=None,
        help="Optional path to write the list of empty-result entries as JSON.",
    )
    parser.add_argument(
        "--output-sample-json", default=None,
        help="Optional path to write one execution-status record per sample as JSON.",
    )
    parser.add_argument(
        "--limit", type=int, default=None,
        help="Only audit the first N entries of the split (default: all).",
    )
    parser.add_argument(
        "--has-null", action="store_true",
        help="Check if any SQL result cell is NULL and bucket such entries as has_null.",
    )
    parser.add_argument(
        "--delete", action="store_true",
        help="Delete empty/error-result samples in place from <split>.json and <split>_gold.sql. "
             "If --has-null is also set, has_null samples are deleted too.",
    )
    args = parser.parse_args()

    if args.limit is not None and args.delete:
        print("--limit cannot be combined with --delete (would truncate the split).",
              file=sys.stderr)
        sys.exit(1)

    empty_entries, per_db, empty_indices, delete_indices, split_data, sample_results = check(
        input_dir=args.input,
        split=args.split,
        timeout=args.timeout,
        show_non_empty=args.show_non_empty,
        check_has_null=args.has_null,
        delete_has_null=(args.has_null and args.delete),
        limit=args.limit,
    )

    print()
    print(_format_summary(per_db))

    if args.output_json:
        os.makedirs(os.path.dirname(args.output_json) or ".", exist_ok=True)
        with open(args.output_json, "w", encoding="utf-8") as f:
            json.dump(empty_entries, f, ensure_ascii=False, indent=2)
        print(f"\n[check_empty_sql] wrote {len(empty_entries)} empty-result entries -> {args.output_json}",
              file=sys.stderr)

    if args.output_sample_json:
        os.makedirs(os.path.dirname(args.output_sample_json) or ".", exist_ok=True)
        with open(args.output_sample_json, "w", encoding="utf-8") as f:
            json.dump(sample_results, f, ensure_ascii=False, indent=2)
        print(
            f"\n[check_empty_sql] wrote {len(sample_results)} sample execution results "
            f"-> {args.output_sample_json}",
            file=sys.stderr,
        )

    if args.delete:
        removed_json, removed_gold = _delete_invalid_inplace(
            input_dir=args.input,
            split=args.split,
            delete_indices=delete_indices,
            data=split_data,
        )
        print(
            f"[check_empty_sql] deleted empty/error"
            f"{'/has_null' if args.has_null else ''}-result entries in place: "
            f"{removed_json} from {args.split}.json, {removed_gold} from {args.split}_gold.sql",
            file=sys.stderr,
        )


if __name__ == "__main__":
    main()
