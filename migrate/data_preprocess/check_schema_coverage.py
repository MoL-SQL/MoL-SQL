#!/usr/bin/env python3
"""
Check split/tables/database schema coverage consistency.

Reports db_ids that appear in split JSON but are missing from:
  - tables.json
  - database/<db_id>/<db_id>.sqlite (or *.db fallback)
"""

import argparse
import json
import os
import sqlite3
from collections import Counter


def _load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _find_db_file(database_dir, db_id):
    if not db_id:
        return None
    db_folder = os.path.join(database_dir, db_id)
    sqlite_path = os.path.join(db_folder, f"{db_id}.sqlite")
    if os.path.isfile(sqlite_path):
        return sqlite_path
    if not os.path.isdir(db_folder):
        return None
    for name in os.listdir(db_folder):
        if name.lower().endswith((".sqlite", ".db")):
            return os.path.join(db_folder, name)
    return None


def _map_sqlite_type(raw_type):
    t = (raw_type or "").upper()
    if "INT" in t:
        return "integer"
    if any(x in t for x in ("REAL", "DOUBLE", "FLOAT", "NUMERIC", "DECIMAL")):
        return "real"
    if any(x in t for x in ("CHAR", "TEXT", "CLOB")):
        return "text"
    if "BLOB" in t:
        return "others"
    return "text"


def _build_tables_entry_from_db(db_id, db_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    try:
        table_rows = cur.execute(
            "SELECT name FROM sqlite_master "
            "WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name"
        ).fetchall()
        table_names = [row[0] for row in table_rows]
        table_idx = {name: i for i, name in enumerate(table_names)}

        column_names = [[-1, "*"]]
        column_names_original = [[-1, "*"]]
        column_types = [""]
        col_index_by_table_col = {}
        primary_keys = []

        for tname in table_names:
            tidx = table_idx[tname]
            for col in cur.execute(f'PRAGMA table_info("{tname}")').fetchall():
                # cid, name, type, notnull, dflt_value, pk
                cname = col[1]
                ctype = _map_sqlite_type(col[2])
                gidx = len(column_names)
                column_names.append([tidx, cname])
                column_names_original.append([tidx, cname])
                column_types.append(ctype)
                col_index_by_table_col[(tname, cname)] = gidx
                if int(col[5] or 0) > 0:
                    primary_keys.append(gidx)

        foreign_keys = []
        for tname in table_names:
            for fk in cur.execute(f'PRAGMA foreign_key_list("{tname}")').fetchall():
                # id, seq, table, from, to, on_update, on_delete, match
                ref_table = fk[2]
                from_col = fk[3]
                to_col = fk[4]
                src_idx = col_index_by_table_col.get((tname, from_col))
                dst_idx = col_index_by_table_col.get((ref_table, to_col))
                if src_idx is not None and dst_idx is not None:
                    foreign_keys.append([src_idx, dst_idx])

        return {
            "db_id": db_id,
            "table_names": table_names[:],
            "table_names_original": table_names[:],
            "column_names": column_names,
            "column_names_original": column_names_original,
            "column_types": column_types,
            "primary_keys": primary_keys,
            "foreign_keys": foreign_keys,
        }
    finally:
        conn.close()


def main():
    parser = argparse.ArgumentParser(
        description="Validate db_id coverage across split JSON, tables.json, and database files."
    )
    parser.add_argument("--dataset-dir", required=True, help="Dataset root containing database/ and tables.json")
    parser.add_argument("--split", default="dev", choices=["dev", "train", "test"], help="Split name (default: dev)")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Return non-zero exit code if any db_id is missing in tables/database.",
    )
    parser.add_argument(
        "--backfill-tables",
        action="store_true",
        help="Append missing db_id schemas to tables.json by introspecting SQLite files.",
    )
    args = parser.parse_args()

    split_path = os.path.join(args.dataset_dir, f"{args.split}.json")
    tables_path = os.path.join(args.dataset_dir, "tables.json")
    database_dir = os.path.join(args.dataset_dir, "database")

    split_data = _load_json(split_path)
    tables_data = _load_json(tables_path)
    table_ids = {entry.get("db_id", "") for entry in tables_data}

    split_counter = Counter(
        (entry.get("db_id") or entry.get("db_name") or "").strip()
        for entry in split_data
    )
    split_counter.pop("", None)

    missing_tables = {}
    missing_db_files = {}
    for db_id, count in split_counter.items():
        if db_id not in table_ids:
            missing_tables[db_id] = count
        if not _find_db_file(database_dir, db_id):
            missing_db_files[db_id] = count

    print(f"[SchemaCoverage] split={args.split} entries={len(split_data)} unique_db_ids={len(split_counter)}")
    if missing_tables:
        print("[SchemaCoverage][Missing tables.json entries]")
        for db_id in sorted(missing_tables):
            print(f"  - {db_id}: {missing_tables[db_id]} entries")
    else:
        print("[SchemaCoverage] tables.json coverage: OK")

    if missing_db_files:
        print("[SchemaCoverage][Missing database files]")
        for db_id in sorted(missing_db_files):
            print(f"  - {db_id}: {missing_db_files[db_id]} entries")
    else:
        print("[SchemaCoverage] database coverage: OK")

    if args.backfill_tables and missing_tables:
        existing_ids = {entry.get("db_id", "") for entry in tables_data}
        appended = 0
        for db_id in sorted(missing_tables):
            if db_id in existing_ids:
                continue
            db_path = _find_db_file(database_dir, db_id)
            if not db_path:
                print(f"[SchemaCoverage][Backfill] skip {db_id}: no database file")
                continue
            entry = _build_tables_entry_from_db(db_id, db_path)
            tables_data.append(entry)
            existing_ids.add(db_id)
            appended += 1
            print(f"[SchemaCoverage][Backfill] added {db_id} from {db_path}")
        if appended:
            with open(tables_path, "w", encoding="utf-8") as f:
                json.dump(tables_data, f, indent=2, ensure_ascii=False)
            print(f"[SchemaCoverage][Backfill] wrote {appended} entries to {tables_path}")

    if args.strict and (missing_tables or missing_db_files):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
