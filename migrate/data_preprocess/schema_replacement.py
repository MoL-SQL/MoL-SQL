#!/usr/bin/env python3
"""
Schema replacement for BULL-FinSQL: replace English database schema names
with the Chinese aliases already present in ``tables.json``.

BULL-cn-origin has ``table_names_original`` / ``column_names_original`` in
English and ``table_names`` / ``column_names`` in Chinese.  This script:

  1. Copies the directory structure (database/, split JSONs, tables.json).
  2. Renames tables and columns in the SQLite databases from EN → CN.
  3. Rewrites ``tables.json`` so that ``*_original`` fields contain the
     Chinese names (matching what is now in the DB).
  4. Translates SQL queries in the split JSON files accordingly.
"""

import argparse
import copy
import json
import os
import shutil
import sys

from tqdm import tqdm

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import STD_DB_DIR, STD_TABLES_FILE, get_config, get_split_files

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "data_translate"))
from db_translate_sqlite import replace_entities_in_db, validate_translation
from sql_translate import (
    build_precise_maps,
    execute_query,
    is_structure_match,
    tokenize_sql,
    tokenize_sql_no_value,
    translate_sql,
)
from utils import load_json


# ---------------------------------------------------------------------------
# Build replacement config from the alias mapping in tables.json
# ---------------------------------------------------------------------------

def build_replacements_from_aliases(tables_data):
    """Build a per-db_id replacement config from the EN/CN pairs in tables.json.

    Returns ``{db_id: {"tables": [...], "columns": [...], "values": []}}``
    in the same format consumed by ``replace_entities_in_db``.
    """
    replacements = {}
    for entry in tables_data:
        db_id = entry["db_id"]
        en_tables = entry["table_names_original"]
        cn_tables = entry["table_names"]

        table_reps = []
        for en_t, cn_t in zip(en_tables, cn_tables):
            if en_t != cn_t:
                table_reps.append([en_t, cn_t])

        en_cols = entry["column_names_original"]
        cn_cols = entry["column_names"]
        col_reps = []
        for ec, cc in zip(en_cols, cn_cols):
            tidx_en, en_c = ec
            tidx_cn, cn_c = cc
            if tidx_en == -1:
                continue
            if en_c != cn_c:
                table_name = en_tables[tidx_en]
                col_reps.append([table_name, en_c, cn_c])

        replacements[db_id] = {
            "tables": table_reps,
            "columns": col_reps,
            "values": [],
        }
    return replacements


# ---------------------------------------------------------------------------
# Build target tables.json (with Chinese names in *_original fields)
# ---------------------------------------------------------------------------

def build_target_tables(tables_data):
    """Create a modified tables.json where ``*_original`` = Chinese aliases."""
    target = copy.deepcopy(tables_data)
    for entry in target:
        entry["table_names_original"] = list(entry["table_names"])
        new_cols = []
        for col_orig, col_cn in zip(entry["column_names_original"],
                                     entry["column_names"]):
            new_cols.append([col_orig[0], col_cn[1]])
        entry["column_names_original"] = new_cols
    return target


# ---------------------------------------------------------------------------
# Directory setup
# ---------------------------------------------------------------------------

def setup_output_dir(input_dir, output_dir, split):
    """Copy / symlink the source layout into the output directory."""
    os.makedirs(output_dir, exist_ok=True)

    src_db = os.path.join(input_dir, STD_DB_DIR)
    dst_db = os.path.join(output_dir, STD_DB_DIR)
    if os.path.exists(src_db) and not os.path.exists(dst_db):
        os.makedirs(dst_db, exist_ok=True)

    split_json, split_gold = get_split_files(split)
    for fname in (split_json, STD_TABLES_FILE):
        src = os.path.join(input_dir, fname)
        dst = os.path.join(output_dir, fname)
        if os.path.exists(src) and not os.path.exists(dst):
            shutil.copy2(src, dst)

    src_gold = os.path.join(input_dir, split_gold)
    if os.path.exists(src_gold):
        dst_gold = os.path.join(output_dir, split_gold)
        if not os.path.exists(dst_gold):
            shutil.copy2(src_gold, dst_gold)


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Replace English DB schema with Chinese aliases for BULL-FinSQL.",
    )
    parser.add_argument("--input", required=True,
                        help="Source dataset directory (BULL-cn-origin)")
    parser.add_argument("--output", required=True,
                        help="Output directory (BULL-cnq-cnds-cndv)")
    parser.add_argument("--split", default="dev", choices=["dev", "train", "test"],
                        help="Data split to process (default: dev)")
    parser.add_argument("--execute-timeout", type=float, default=10,
                        help="Max seconds per SQL query execution (default: 10)")
    args = parser.parse_args()

    input_dir = os.path.abspath(args.input)
    output_dir = os.path.abspath(args.output)
    split = args.split

    cfg = get_config("BULL-cn")
    split_json, split_gold = get_split_files(split)

    # ── Load source tables.json ──────────────────────────────────────────
    src_tables_path = os.path.join(input_dir, STD_TABLES_FILE)
    tables_data = load_json(src_tables_path)
    print(f"Loaded {len(tables_data)} databases from {src_tables_path}")

    # ── Build replacement config and target tables ───────────────────────
    replacements = build_replacements_from_aliases(tables_data)
    target_tables = build_target_tables(tables_data)

    # ── Set up output directory ──────────────────────────────────────────
    setup_output_dir(input_dir, output_dir, split)

    # ── Step 1: Rename schema in SQLite databases ────────────────────────
    src_db_dir = os.path.join(input_dir, STD_DB_DIR)
    out_db_dir = os.path.join(output_dir, STD_DB_DIR)

    if os.path.isdir(src_db_dir):
        print(f"\n[Step 1] Renaming schema in {len(replacements)} databases …")
        for db_id, rep in tqdm(replacements.items(), desc="Rewriting DBs"):
            src = os.path.join(src_db_dir, db_id, f"{db_id}.sqlite")
            out = os.path.join(out_db_dir, db_id, f"{db_id}.sqlite")
            replace_entities_in_db(src, out, rep, values_only=False)
            validate_translation(src, out, rep)
    else:
        print(f"[Step 1] Skipped – no database/ directory in {input_dir}")

    # ── Step 2: Write target tables.json ─────────────────────────────────
    out_tables_path = os.path.join(output_dir, STD_TABLES_FILE)
    with open(out_tables_path, "w", encoding="utf-8") as f:
        json.dump(target_tables, f, indent=2, ensure_ascii=False)
    print(f"\n[Step 2] Saved target tables.json → {out_tables_path}")

    # ── Step 3: Translate SQL in split JSON ──────────────────────────────
    src_json_path = os.path.join(input_dir, split_json)
    if not os.path.exists(src_json_path):
        print(f"[Step 3] Skipped – {split_json} not found in {input_dir}")
        return

    split_data = load_json(src_json_path)
    print(f"\n[Step 3] Translating {len(split_data)} SQL queries ({split} split) …")

    out_entries, gold_lines = [], []
    stats = {"success": 0, "fail": 0, "warning": 0}

    for entry in tqdm(split_data, desc="Translating SQL"):
        db_id = entry.get("db_id") or entry.get("db_name", "")
        src_sql = (
            entry.get(cfg.sql_field)
            or entry.get("SQL")
            or entry.get("query")
            or entry.get("sql_query")
        )
        if not src_sql:
            stats["fail"] += 1
            out_entries.append(entry)
            continue

        maps = build_precise_maps(db_id, tables_data, target_tables)
        if not maps:
            stats["fail"] += 1
            print(f"\n  [Fail] db_id={db_id!r}: no schema maps")
            out_entries.append(entry)
            continue

        db_reps = replacements.get(db_id, {})
        tgt_sql = translate_sql(src_sql, maps, db_reps)

        src_db_path = os.path.join(src_db_dir, db_id, f"{db_id}.sqlite")
        tgt_db_path = os.path.join(out_db_dir, db_id, f"{db_id}.sqlite")

        if os.path.exists(src_db_path) and os.path.exists(tgt_db_path):
            src_res = execute_query(src_db_path, src_sql, timeout=args.execute_timeout)
            tgt_res = execute_query(tgt_db_path, tgt_sql, timeout=args.execute_timeout)

            timeout_src = src_res == "Error: timeout"
            timeout_tgt = tgt_res == "Error: timeout"

            if not timeout_src and not timeout_tgt and src_res is not None and src_res == tgt_res:
                stats["success"] += 1
            elif is_structure_match(src_res, tgt_res):
                stats["warning"] += 1
            else:
                stats["fail"] += 1
                print(
                    f"\n  [Fail] db_id={db_id!r}: execution mismatch"
                    f"\n    src_sql={src_sql}"
                    f"\n    tgt_sql={tgt_sql}"
                )
        else:
            stats["warning"] += 1

        entry[cfg.sql_field] = tgt_sql
        entry["SQL"] = tgt_sql
        entry["query"] = tgt_sql
        entry["query_toks"] = tokenize_sql(tgt_sql)
        entry["query_toks_no_value"] = tokenize_sql_no_value(tgt_sql)
        out_entries.append(entry)
        gold_lines.append(f"{tgt_sql}\t{db_id}\n")

    out_json_path = os.path.join(output_dir, split_json)
    with open(out_json_path, "w", encoding="utf-8") as f:
        json.dump(out_entries, f, indent=2, ensure_ascii=False)

    out_gold_path = os.path.join(output_dir, split_gold)
    with open(out_gold_path, "w", encoding="utf-8") as f:
        f.writelines(gold_lines)

    print(
        f"\n[Step 3] Done. "
        f"Success: {stats['success']}, Warning: {stats['warning']}, Fail: {stats['fail']}"
    )
    print(f"  Output JSON → {out_json_path}")
    print(f"  Output Gold → {out_gold_path}")
    print("\n=== Schema replacement complete ===")


if __name__ == "__main__":
    main()
