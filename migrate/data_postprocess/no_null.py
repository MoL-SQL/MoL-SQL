#!/usr/bin/env python3
"""Audit SQL execution buckets, with optional no-NULL database copies.

This script mirrors the core behavior of ``script/data_preprocess/check_empty_sql.py``
for a dataset split (default ``dev``):
  - execute each sample's gold SQL on its DB
  - bucket into ``empty`` / ``non_empty`` / ``has_null`` / ``error`` / ``no_db`` / ``skipped``

Optionally, ``--db-no-null`` performs a second pass:
  1) copy each sqlite DB to a temporary location
  2) delete rows containing at least one NULL cell from every table in the copy
  3) rerun the same SQL audit against these cleaned copies

Original sqlite files are never modified.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sqlite3
import tempfile
from collections import defaultdict
from typing import Dict, Tuple

from tqdm import tqdm


EMPTY = "empty"
NON_EMPTY = "non_empty"
HAS_NULL = "has_null"
ERROR = "error"
NO_DB = "no_db"
SKIPPED = "skipped"
BUCKETS = (EMPTY, NON_EMPTY, HAS_NULL, ERROR, NO_DB, SKIPPED)


def _quote_ident(name: str) -> str:
    return '"' + name.replace('"', '""') + '"'


def _db_path(input_dir: str, db_name: str) -> str:
    """Resolve DB file under ``<input>/database/<db_name>/``."""
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


def _execute(sql: str, db_file: str, timeout: float) -> Tuple[str, object]:
    """Run one SQL query and return ``(bucket, payload)``."""
    conn = sqlite3.connect(db_file, timeout=timeout)
    try:
        import time

        deadline = time.monotonic() + timeout

        def _abort_if_overdue() -> int:
            return 1 if time.monotonic() > deadline else 0

        conn.set_progress_handler(_abort_if_overdue, 1000)
        cursor = conn.cursor()
        try:
            cursor.execute(sql)
            rows = cursor.fetchall()
        except Exception as exc:  # noqa: BLE001
            return ERROR, f"{type(exc).__name__}: {exc}"

        if not rows:
            return EMPTY, 0
        if any(cell is None for row in rows for cell in row):
            return HAS_NULL, rows
        return NON_EMPTY, len(rows)
    finally:
        conn.close()


def _format_summary(per_db: dict[str, dict[str, int]]) -> str:
    header = f"{'db_name':<24} " + " ".join(f"{b:>10}" for b in BUCKETS) + f" {'total':>10}"
    lines = [header, "-" * len(header)]

    totals = {b: 0 for b in BUCKETS}
    for db_name in sorted(per_db):
        counts = per_db[db_name]
        row_total = sum(counts.values())
        lines.append(
            f"{db_name:<24} "
            + " ".join(f"{counts.get(b, 0):>10}" for b in BUCKETS)
            + f" {row_total:>10}"
        )
        for b in BUCKETS:
            totals[b] += counts.get(b, 0)

    grand_total = sum(totals.values())
    lines.append("-" * len(header))
    lines.append(
        f"{'TOTAL':<24} " + " ".join(f"{totals[b]:>10}" for b in BUCKETS) + f" {grand_total:>10}"
    )
    return "\n".join(lines)


def _load_split(input_dir: str, split: str) -> list[dict]:
    split_path = os.path.join(input_dir, f"{split}.json")
    if not os.path.isfile(split_path):
        raise FileNotFoundError(split_path)
    with open(split_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError(f"Expected JSON array in {split_path}, got {type(data).__name__}")
    return data


def _print_has_null_case(
    pass_tag: str,
    q_id: object,
    db_name: str,
    question: str,
    sql: str,
    rows: object,
) -> None:
    print(f"[has_null][{pass_tag}] q_id={q_id} db={db_name}")
    print(f"  Q: {question}")
    print(f"  SQL: {sql}")
    print(f"  RESULT: {rows}")


def audit(
    data: list[dict],
    input_dir: str,
    timeout: float,
    db_override: dict[str, str] | None = None,
    pass_tag: str = "original",
) -> tuple[dict[str, dict[str, int]], dict[str, int]]:
    """Run SQL bucket audit for split rows."""
    per_db: dict[str, dict[str, int]] = defaultdict(lambda: {b: 0 for b in BUCKETS})
    totals = {b: 0 for b in BUCKETS}

    for entry in tqdm(data):
        q_id = entry.get("q_id")
        db_name = (entry.get("db_name") or entry.get("db_id") or "").strip()
        question = entry.get("question", "")
        sql = (entry.get("sql_query") or entry.get("query") or entry.get("SQL") or entry.get("sql") or "").strip()

        if not sql:
            key = db_name or "<missing>"
            per_db[key][SKIPPED] += 1
            totals[SKIPPED] += 1
            continue

        if db_override and db_name in db_override:
            db_file = db_override[db_name]
        else:
            db_file = _db_path(input_dir, db_name) if db_name else ""

        if not db_file or not os.path.isfile(db_file):
            key = db_name or "<missing>"
            per_db[key][NO_DB] += 1
            totals[NO_DB] += 1
            continue

        bucket, payload = _execute(sql, db_file, timeout)
        per_db[db_name][bucket] += 1
        totals[bucket] += 1
        if bucket == HAS_NULL:
            _print_has_null_case(
                pass_tag=pass_tag,
                q_id=q_id,
                db_name=db_name,
                question=question,
                sql=sql,
                rows=payload,
            )

    return per_db, totals


def _list_tables(conn: sqlite3.Connection) -> list[str]:
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
    return [r[0] for r in cur.fetchall()]


def _table_columns(conn: sqlite3.Connection, table: str) -> list[str]:
    cur = conn.cursor()
    cur.execute(f"PRAGMA table_info({_quote_ident(table)})")
    return [r[1] for r in cur.fetchall()]


def _delete_null_rows_inplace(db_file: str) -> dict[str, int]:
    """Delete rows that contain any NULL in each table. Returns per-table deletes."""
    conn = sqlite3.connect(db_file)
    try:
        conn.execute("PRAGMA foreign_keys=OFF")
        deleted: dict[str, int] = {}
        for table in _list_tables(conn):
            cols = _table_columns(conn, table)
            if not cols:
                deleted[table] = 0
                continue
            where_clause = " OR ".join(f"{_quote_ident(col)} IS NULL" for col in cols)
            cur = conn.cursor()
            cur.execute(f"DELETE FROM {_quote_ident(table)} WHERE {where_clause}")
            deleted[table] = max(cur.rowcount, 0)
        conn.commit()
        return deleted
    finally:
        conn.close()


def build_no_null_db_copies(
    input_dir: str,
    data: list[dict],
    temp_root: str,
) -> tuple[dict[str, str], dict[str, int]]:
    """Create cleaned sqlite copies and return ``db_name -> copied_db_path``."""
    needed_dbs = sorted(
        {
            (entry.get("db_name") or entry.get("db_id") or "").strip()
            for entry in data
            if (entry.get("db_name") or entry.get("db_id") or "").strip()
        }
    )

    override: dict[str, str] = {}
    removed_rows_by_db: dict[str, int] = {}

    for db_name in needed_dbs:
        src = _db_path(input_dir, db_name)
        if not src or not os.path.isfile(src):
            continue

        dst_dir = os.path.join(temp_root, db_name)
        os.makedirs(dst_dir, exist_ok=True)
        ext = ".sqlite" if src.endswith(".sqlite") else ".db"
        dst = os.path.join(dst_dir, f"{db_name}{ext}")
        shutil.copy2(src, dst)

        deleted_by_table = _delete_null_rows_inplace(dst)
        removed_rows_by_db[db_name] = sum(deleted_by_table.values())
        override[db_name] = dst

    return override, removed_rows_by_db


def _print_totals(tag: str, totals: dict[str, int]) -> None:
    total = sum(totals.values())
    parts = " ".join(f"{k}={totals.get(k, 0)}" for k in BUCKETS)
    print(f"[{tag}] {parts} total={total}")


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Check gold SQL buckets (empty/non-empty/has-null/error/etc.) and "
            "optionally rerun after dropping NULL-containing rows in copied DBs."
        )
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Dataset directory containing <split>.json and database/<db>/<db>.sqlite",
    )
    parser.add_argument(
        "--split",
        default="dev",
        choices=["dev", "train", "test"],
        help="Split file name without extension (default: dev).",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=30.0,
        help="Per-query timeout in seconds (default: 30).",
    )
    parser.add_argument(
        "--db-no-null",
        action="store_true",
        help=(
            "Create temporary DB copies, delete rows with any NULL cell, and rerun "
            "the same audit against these cleaned copies."
        ),
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    data = _load_split(args.input, args.split)
    print(f"[no_null] loaded {len(data)} rows from {os.path.join(args.input, f'{args.split}.json')}")

    per_db, totals = audit(
        data=data,
        input_dir=args.input,
        timeout=args.timeout,
        pass_tag="original",
    )
    print("\n=== pass #1: original databases ===")
    print(_format_summary(per_db))
    _print_totals("original", totals)

    if not args.db_no_null:
        return

    with tempfile.TemporaryDirectory(prefix="no_null_db_") as temp_root:
        db_override, removed_rows = build_no_null_db_copies(args.input, data, temp_root)
        print(
            f"\n[db-no-null] prepared {len(db_override)} copied DBs; "
            f"removed_rows_total={sum(removed_rows.values())}"
        )

        per_db_clean, totals_clean = audit(
            data=data,
            input_dir=args.input,
            timeout=args.timeout,
            db_override=db_override,
            pass_tag="db_no_null",
        )
        print("\n=== pass #2: copied DBs with NULL rows removed ===")
        print(_format_summary(per_db_clean))
        _print_totals("db_no_null", totals_clean)


if __name__ == "__main__":
    main()