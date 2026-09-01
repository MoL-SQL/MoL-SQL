#!/usr/bin/env python3
"""
Clean TACO split data by removing placeholder "Unnamed*" columns/tables/samples.

In-place operations under ``<input>``:
1) For each DB JSON in ``database/<db_id>/<db_id>.json`` and SQLite
   in ``database/<db_id>/<db_id>.sqlite``:
   - remove columns whose name starts with "Unnamed" (case-insensitive)
     when the column appears empty (or has no value metadata).
   - remove tables that become empty after column cleanup.
2) For ``tables.json``:
   - mirror the same table/column removals and reindex Spider-style arrays.
3) For ``<split>.json``:
   - remove samples whose SQL references an "Unnamed*" column token.
4) Regenerate ``<split>_gold.sql`` from filtered ``<split>.json``.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sqlite3
from dataclasses import dataclass, field
from typing import Any


UNNAMED_PREFIX = "unnamed"
SQL_UNNAMED_RE = re.compile(
    r'(?i)(["`\[]\s*unnamed[^"`\]]*["`\]]|\bunnamed\s*[:_\d][\w:.-]*)'
)


def _is_unnamed(name: str) -> bool:
    return (name or "").strip().lower().startswith(UNNAMED_PREFIX)


def _has_non_empty_values(raw: Any) -> bool:
    """Return True if a value container has at least one non-empty value."""
    if isinstance(raw, list):
        for v in raw:
            if _has_non_empty_values(v):
                return True
        return False
    if isinstance(raw, dict):
        for v in raw.values():
            if _has_non_empty_values(v):
                return True
        return False
    if raw is None:
        return False
    if isinstance(raw, str):
        return raw.strip() != ""
    return True


def _column_looks_empty(column: dict[str, Any]) -> bool:
    """Best effort: treat missing value metadata as empty placeholders."""
    value_keys = (
        "values",
        "value_samples",
        "sample_values",
        "examples",
        "example_values",
        "column_values",
        "data",
    )
    found = False
    for key in value_keys:
        if key in column:
            found = True
            if _has_non_empty_values(column.get(key)):
                return False
    # No value metadata in TACO schema JSONs; treat as empty placeholder.
    return True if not found else True


def _sql_references_table(sql: str, table_name: str) -> bool:
    table_name = (table_name or "").strip()
    if not sql or not table_name:
        return False

    escaped = re.escape(table_name)
    quoted_pat = re.compile(rf'(?i)(["`\[]\s*{escaped}\s*["`\]])')
    if quoted_pat.search(sql):
        return True

    # For simple identifiers, also match bare-table usage in SQL.
    if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", table_name):
        bare_pat = re.compile(rf"(?i)\b{escaped}\b")
        return bool(bare_pat.search(sql))
    return False


def _quote_ident(name: str) -> str:
    return '"' + str(name).replace('"', '""') + '"'


def _apply_sqlite_cleanup(
    sqlite_path: str, removed_tables: set[str], removed_columns: dict[str, set[str]]
) -> tuple[int, int, int]:
    """Apply table/column removals to sqlite, returning (tables, columns, errors)."""
    if not os.path.isfile(sqlite_path):
        return 0, 0, 0

    dropped_tables = 0
    dropped_columns = 0
    errors = 0
    conn = sqlite3.connect(sqlite_path)
    try:
        cur = conn.cursor()
        cur.execute("PRAGMA foreign_keys=OFF")

        for table_name in sorted(removed_tables):
            try:
                cur.execute(f"DROP TABLE IF EXISTS {_quote_ident(table_name)}")
                dropped_tables += 1
            except sqlite3.DatabaseError:
                errors += 1

        for table_name in sorted(removed_columns.keys()):
            if table_name in removed_tables:
                continue
            for col_name in sorted(removed_columns[table_name]):
                try:
                    cur.execute(
                        f"ALTER TABLE {_quote_ident(table_name)} "
                        f"DROP COLUMN {_quote_ident(col_name)}"
                    )
                    dropped_columns += 1
                except sqlite3.DatabaseError:
                    errors += 1

        conn.commit()
    finally:
        conn.close()

    return dropped_tables, dropped_columns, errors


@dataclass
class DbCleanupResult:
    db_id: str
    removed_tables: set[str] = field(default_factory=set)
    removed_columns: dict[str, set[str]] = field(default_factory=dict)
    sqlite_removed_tables: int = 0
    sqlite_removed_columns: int = 0
    sqlite_errors: int = 0
    before_table_count: int = 0
    before_column_count: int = 0
    after_table_count: int = 0
    after_column_count: int = 0

    @property
    def removed_column_count(self) -> int:
        return sum(len(v) for v in self.removed_columns.values())


def _clean_single_db_json(path: str) -> DbCleanupResult:
    db_id = os.path.splitext(os.path.basename(path))[0]
    with open(path, "r", encoding="utf-8") as f:
        payload = json.load(f)
    tables = payload.get("tables", [])
    if not isinstance(tables, list):
        return DbCleanupResult(db_id=db_id)

    before_table_count = len(tables)
    before_column_count = sum(
        len(t.get("columns", []))
        for t in tables
        if isinstance(t, dict) and isinstance(t.get("columns", []), list)
    )

    removed_tables: set[str] = set()
    removed_columns: dict[str, set[str]] = {}
    changed = False
    new_tables: list[dict[str, Any]] = []

    for table in tables:
        table_name = str(table.get("table_name") or table.get("name") or "").strip()
        cols = table.get("columns", [])
        if not table_name or not isinstance(cols, list):
            new_tables.append(table)
            continue

        kept_cols: list[dict[str, Any]] = []
        table_removed_cols: set[str] = set()
        for col in cols:
            col_name = str(col.get("column_name") or col.get("name") or "").strip()
            if _is_unnamed(col_name) and _column_looks_empty(col):
                table_removed_cols.add(col_name)
                changed = True
            else:
                kept_cols.append(col)

        if table_removed_cols:
            removed_columns[table_name] = table_removed_cols

        # Instruction 2.1: drop tables with <=1 non-"Unnamed*" columns.
        non_unnamed_cols = [
            c
            for c in cols
            if not _is_unnamed(str(c.get("column_name") or c.get("name") or "").strip())
        ]
        if len(non_unnamed_cols) <= 1:
            removed_tables.add(table_name)
            changed = True
            continue

        if not kept_cols:
            removed_tables.add(table_name)
            changed = True
            continue

        if len(kept_cols) != len(cols):
            table = dict(table)
            table["columns"] = kept_cols
        new_tables.append(table)

    if changed:
        payload = dict(payload)
        payload["tables"] = new_tables
        with open(path, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)

    after_table_count = len(new_tables)
    after_column_count = sum(
        len(t.get("columns", []))
        for t in new_tables
        if isinstance(t, dict) and isinstance(t.get("columns", []), list)
    )

    sqlite_path = os.path.join(os.path.dirname(path), f"{db_id}.sqlite")
    sqlite_removed_tables, sqlite_removed_columns, sqlite_errors = _apply_sqlite_cleanup(
        sqlite_path, removed_tables, removed_columns
    )

    return DbCleanupResult(
        db_id=db_id,
        removed_tables=removed_tables,
        removed_columns=removed_columns,
        sqlite_removed_tables=sqlite_removed_tables,
        sqlite_removed_columns=sqlite_removed_columns,
        sqlite_errors=sqlite_errors,
        before_table_count=before_table_count,
        before_column_count=before_column_count,
        after_table_count=after_table_count,
        after_column_count=after_column_count,
    )


def _remap_tables_entry(
    entry: dict[str, Any], removed_tables: set[str], removed_columns: dict[str, set[str]]
) -> dict[str, Any]:
    names_orig = entry.get("table_names_original", [])
    names = entry.get("table_names", [])
    col_names_orig = entry.get("column_names_original", [])
    col_names = entry.get("column_names", [])
    col_types = entry.get("column_types", [])
    pks = entry.get("primary_keys", [])
    fks = entry.get("foreign_keys", [])

    # table index remap
    table_map: dict[int, int] = {}
    new_names_orig: list[str] = []
    new_names: list[str] = []
    for old_idx, t_name in enumerate(names_orig):
        if t_name in removed_tables:
            continue
        table_map[old_idx] = len(new_names_orig)
        new_names_orig.append(t_name)
        new_names.append(names[old_idx] if old_idx < len(names) else t_name)

    # column index remap (keep star at index 0)
    col_map: dict[int, int] = {}
    new_col_names_orig: list[list[Any]] = []
    new_col_names: list[list[Any]] = []
    new_col_types: list[str] = []
    for old_idx, col in enumerate(col_names_orig):
        if old_idx == 0:
            col_map[old_idx] = 0
            new_col_names_orig.append(col)
            if col_names:
                new_col_names.append(col_names[0])
            else:
                new_col_names.append(col)
            new_col_types.append(col_types[0] if col_types else "text")
            continue

        if not (isinstance(col, list) and len(col) == 2):
            continue
        old_t_idx, col_name = col
        if old_t_idx not in table_map:
            continue
        table_name = names_orig[old_t_idx]
        if col_name in removed_columns.get(table_name, set()):
            continue

        new_t_idx = table_map[old_t_idx]
        col_map[old_idx] = len(new_col_names_orig)
        new_col_names_orig.append([new_t_idx, col_name])
        if old_idx < len(col_names) and isinstance(col_names[old_idx], list) and len(col_names[old_idx]) == 2:
            new_col_names.append([new_t_idx, col_names[old_idx][1]])
        else:
            new_col_names.append([new_t_idx, col_name])
        new_col_types.append(col_types[old_idx] if old_idx < len(col_types) else "text")

    new_pks = sorted({col_map[i] for i in pks if isinstance(i, int) and i in col_map and col_map[i] != 0})
    new_fks: list[list[int]] = []
    for pair in fks:
        if not (isinstance(pair, list) and len(pair) == 2):
            continue
        a, b = pair
        if a in col_map and b in col_map:
            na, nb = col_map[a], col_map[b]
            if na != 0 and nb != 0:
                new_fks.append([na, nb])

    out = dict(entry)
    out["table_names_original"] = new_names_orig
    out["table_names"] = new_names
    out["column_names_original"] = new_col_names_orig
    out["column_names"] = new_col_names
    out["column_types"] = new_col_types
    out["primary_keys"] = new_pks
    out["foreign_keys"] = new_fks
    return out


def _update_tables_json(
    tables_path: str, db_changes: dict[str, DbCleanupResult]
) -> tuple[int, int]:
    if not os.path.isfile(tables_path):
        return 0, 0
    with open(tables_path, "r", encoding="utf-8") as f:
        tables = json.load(f)
    if not isinstance(tables, list):
        return 0, 0

    changed_db = 0
    changed_entries = 0
    new_tables: list[dict[str, Any]] = []
    for entry in tables:
        db_id = entry.get("db_id")
        change = db_changes.get(db_id)
        if not change:
            new_tables.append(entry)
            continue
        if not change.removed_tables and not change.removed_columns:
            new_tables.append(entry)
            continue

        changed_db += 1
        new_entry = _remap_tables_entry(entry, change.removed_tables, change.removed_columns)
        new_tables.append(new_entry)
        changed_entries += 1

    if changed_entries > 0:
        with open(tables_path, "w", encoding="utf-8") as f:
            json.dump(new_tables, f, ensure_ascii=False, indent=2)
    return changed_db, changed_entries


def _sample_sql(entry: dict[str, Any]) -> str:
    for key in ("sql_query", "query", "SQL", "sql"):
        value = entry.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""


def _rewrite_split(
    split_path: str, db_changes: dict[str, DbCleanupResult]
) -> tuple[int, int, int]:
    with open(split_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError(f"Expected list in {split_path}, got {type(data).__name__}")

    kept: list[dict[str, Any]] = []
    removed_unnamed = 0
    removed_deleted_table = 0
    for item in data:
        sql = _sample_sql(item)
        if sql and SQL_UNNAMED_RE.search(sql):
            removed_unnamed += 1
            continue

        # Instruction 4: drop samples that reference deleted tables.
        db_id = str(item.get("db_id") or "")
        removed_tables = db_changes.get(db_id).removed_tables if db_id in db_changes else set()
        if sql and removed_tables:
            if any(_sql_references_table(sql, t_name) for t_name in removed_tables):
                removed_deleted_table += 1
                continue

        kept.append(item)

    removed_total = removed_unnamed + removed_deleted_table
    if removed_total > 0:
        with open(split_path, "w", encoding="utf-8") as f:
            json.dump(kept, f, ensure_ascii=False, indent=2)
    return len(kept), removed_unnamed, removed_deleted_table


def _rewrite_gold_sql(input_dir: str, split: str, rows: list[dict[str, Any]]) -> str:
    out_path = os.path.join(input_dir, f"{split}_gold.sql")
    lines = []
    for row in rows:
        sql = _sample_sql(row)
        db_id = row.get("db_id") or row.get("db_name") or row.get("database") or ""
        if sql:
            lines.append(f"{sql}\t{db_id}\n")
    with open(out_path, "w", encoding="utf-8") as f:
        f.writelines(lines)
    return out_path


def run(input_dir: str, split: str) -> None:
    db_root = os.path.join(input_dir, "database")
    split_path = os.path.join(input_dir, f"{split}.json")
    tables_path = os.path.join(input_dir, "tables.json")

    if not os.path.isdir(db_root):
        raise FileNotFoundError(f"Missing database dir: {db_root}")
    if not os.path.isfile(split_path):
        raise FileNotFoundError(f"Missing split file: {split_path}")

    db_changes: dict[str, DbCleanupResult] = {}
    db_count = 0
    for db_id in sorted(os.listdir(db_root)):
        json_path = os.path.join(db_root, db_id, f"{db_id}.json")
        if not os.path.isfile(json_path):
            continue
        db_count += 1
        res = _clean_single_db_json(json_path)
        db_changes[db_id] = res

    removed_tables_total = sum(len(v.removed_tables) for v in db_changes.values())
    removed_cols_total = sum(v.removed_column_count for v in db_changes.values())
    before_tables_total = sum(v.before_table_count for v in db_changes.values())
    before_columns_total = sum(v.before_column_count for v in db_changes.values())
    after_tables_total = sum(v.after_table_count for v in db_changes.values())
    after_columns_total = sum(v.after_column_count for v in db_changes.values())
    sqlite_tables_total = sum(v.sqlite_removed_tables for v in db_changes.values())
    sqlite_columns_total = sum(v.sqlite_removed_columns for v in db_changes.values())
    sqlite_errors_total = sum(v.sqlite_errors for v in db_changes.values())

    changed_db, changed_entries = _update_tables_json(tables_path, db_changes)

    kept_n, removed_unnamed_n, removed_deleted_table_n = _rewrite_split(
        split_path, db_changes
    )
    with open(split_path, "r", encoding="utf-8") as f:
        filtered_rows = json.load(f)
    gold_path = _rewrite_gold_sql(input_dir, split, filtered_rows)

    print(
        "[delete_unnamed_column] "
        f"dbs={db_count}, removed_tables={removed_tables_total}, "
        f"removed_columns={removed_cols_total}, "
        f"tables_before={before_tables_total}, tables_after={after_tables_total}, "
        f"columns_before={before_columns_total}, columns_after={after_columns_total}"
    )
    for db_id in sorted(db_changes.keys()):
        stats = db_changes[db_id]
        print(
            "[delete_unnamed_column] "
            f"db={db_id}, "
            f"tables_before={stats.before_table_count}, "
            f"tables_after={stats.after_table_count}, "
            f"columns_before={stats.before_column_count}, "
            f"columns_after={stats.after_column_count}, "
            f"sqlite_tables_removed={stats.sqlite_removed_tables}, "
            f"sqlite_columns_removed={stats.sqlite_removed_columns}, "
            f"sqlite_errors={stats.sqlite_errors}"
        )
    print(
        "[delete_unnamed_column] "
        f"tables.json updated_db={changed_db}, updated_entries={changed_entries}"
    )
    print(
        "[delete_unnamed_column] "
        f"{split}.json kept={kept_n}, removed_unnamed={removed_unnamed_n}, "
        f"removed_deleted_tables={removed_deleted_table_n}, gold={gold_path}"
    )
    print(
        "[delete_unnamed_column] "
        f"sqlite_removed_tables={sqlite_tables_total}, "
        f"sqlite_removed_columns={sqlite_columns_total}, "
        f"sqlite_errors={sqlite_errors_total}"
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Remove placeholder Unnamed columns/tables and samples in-place."
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Dataset directory containing database/, tables.json and <split>.json.",
    )
    parser.add_argument(
        "--split",
        default="dev",
        choices=["dev", "train", "test"],
        help="Split file basename (default: dev).",
    )
    args = parser.parse_args()
    run(input_dir=args.input, split=args.split)


if __name__ == "__main__":
    main()
