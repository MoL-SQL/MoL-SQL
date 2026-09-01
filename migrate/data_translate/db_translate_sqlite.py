#!/usr/bin/env python3
"""
Apply a replacements config to SQLite databases: rename tables, columns,
and update cell values.  Supports full-rename mode (Spider/BIRD) and
values-only mode (BULL ``--values-only``).
"""

import argparse
import difflib
import json
import os
import re
import shutil
import sqlite3
import sys
import uuid

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import STD_DB_DIR, STD_TABLES_FILE
from utils import is_system_table, load_json


# ---------------------------------------------------------------------------
# SQLite schema helpers
# ---------------------------------------------------------------------------

def _quote_ident(name):
    return '"' + str(name).replace('"', '""') + '"'


def _normalize_ident(name):
    """
    Normalize SQLite identifiers for tolerant matching.
    Handles case-insensitivity and common identifier quoting styles.
    """
    if name is None:
        return ""
    ident = str(name).strip()
    if ident.startswith("[") and ident.endswith("]"):
        ident = ident[1:-1]
    elif len(ident) >= 2 and ident[0] == ident[-1] and ident[0] in ('"', "`", "'"):
        ident = ident[1:-1]
    return ident.strip().lower()


def _schema_objects(cursor, obj_type):
    rows = cursor.execute(
        "SELECT name FROM sqlite_master WHERE type=? ORDER BY name",
        (obj_type,),
    ).fetchall()
    return {
        r[0] for r in rows
        if r[0] and not is_system_table(r[0])
    }


def _schema_object_sql(cursor, obj_type):
    rows = cursor.execute(
        "SELECT name, sql FROM sqlite_master "
        "WHERE type=? AND sql IS NOT NULL ORDER BY name",
        (obj_type,),
    ).fetchall()
    return {
        r[0]: r[1] for r in rows
        if r[0] and not is_system_table(r[0])
    }


def _table_columns(cursor, table_name):
    rows = cursor.execute(f"PRAGMA table_info({_quote_ident(table_name)})").fetchall()
    return [r[1] for r in rows]


def _similarity_ratio(a, b):
    return difflib.SequenceMatcher(None, a, b).ratio()


def _resolve_name_from_candidates(candidates, wanted_name, *, allow_fuzzy=False, min_ratio=0.88):
    if wanted_name in candidates:
        return wanted_name, "exact"
    wanted_norm = _normalize_ident(wanted_name)
    matches = [name for name in candidates if _normalize_ident(name) == wanted_norm]
    if len(matches) == 1:
        return matches[0], "normalized"
    if not allow_fuzzy:
        return None, None

    wanted_sig = re.sub(r"[^a-z0-9]+", "", wanted_norm)
    scored = []
    for name in candidates:
        norm = _normalize_ident(name)
        norm_sig = re.sub(r"[^a-z0-9]+", "", norm)
        ratio = max(_similarity_ratio(wanted_norm, norm), _similarity_ratio(wanted_sig, norm_sig))
        scored.append((ratio, name))
    scored.sort(key=lambda x: x[0], reverse=True)
    if not scored:
        return None, None
    best_ratio, best_name = scored[0]
    runner_up = scored[1][0] if len(scored) > 1 else 0.0
    # Conservative fuzzy fallback: only accept a clear best candidate.
    if best_ratio >= min_ratio and (best_ratio - runner_up) >= 0.05:
        return best_name, f"fuzzy:{best_ratio:.2f}"
    return None, None


def _resolve_column_name(cursor, table_name, wanted_column, *, allow_fuzzy=False):
    columns = _table_columns(cursor, table_name)
    return _resolve_name_from_candidates(
        columns, wanted_column, allow_fuzzy=allow_fuzzy
    )


def _translation_map(pairs):
    return {
        old.lower(): new
        for old, new in pairs
        if old and new and old != new and not is_system_table(old)
    }


# ---------------------------------------------------------------------------
# CHECK constraint removal (needed before value updates)
# ---------------------------------------------------------------------------

def _remove_check_clauses(sql):
    result, i = [], 0
    while i < len(sql):
        if sql[i:i + 5].upper() == "CHECK":
            j = i + 5
            while j < len(sql) and sql[j] in " \t\n":
                j += 1
            if j < len(sql) and sql[j] == "(":
                depth, k = 1, j + 1
                while k < len(sql) and depth > 0:
                    if sql[k] == "(":
                        depth += 1
                    elif sql[k] == ")":
                        depth -= 1
                    k += 1
                while result and result[-1] in " \t\n,":
                    result.pop()
                i = k
                while i < len(sql) and sql[i] in " \t\n":
                    i += 1
                continue
        result.append(sql[i])
        i += 1
    return "".join(result)


def remove_check_constraints(cursor, table_name):
    cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
    row = cursor.fetchone()
    if not row or not row[0] or "CHECK" not in row[0].upper():
        return False

    modified = _remove_check_clauses(row[0])
    modified = re.sub(r",\s*,", ",", modified)
    modified = re.sub(r",(\s*\))", r"\1", modified)
    modified = re.sub(r"\(\s*,", "(", modified)

    temp = f"_tmp_no_check_{table_name}_{uuid.uuid4().hex[:8]}"
    modified = re.sub(
        rf"CREATE\s+TABLE\s+[`\"']?{re.escape(table_name)}[`\"']?",
        f"CREATE TABLE {_quote_ident(temp)}", modified, count=1, flags=re.IGNORECASE,
    )
    cursor.execute("PRAGMA foreign_keys")
    foreign_keys = cursor.fetchone()[0]
    savepoint = f"sp_remove_check_{uuid.uuid4().hex}"
    try:
        cursor.execute("PRAGMA foreign_keys=OFF")
        cursor.execute(f"SAVEPOINT {savepoint}")
        cursor.execute(modified)
        cursor.execute(
            f"INSERT INTO {_quote_ident(temp)} SELECT * FROM {_quote_ident(table_name)}"
        )
        cursor.execute(f"DROP TABLE {_quote_ident(table_name)}")
        cursor.execute(
            f"ALTER TABLE {_quote_ident(temp)} RENAME TO {_quote_ident(table_name)}"
        )
        cursor.execute(f"RELEASE {savepoint}")
        return True
    except Exception as e:
        print(f"  [Warning] CHECK removal failed for {table_name}: {e}")
        try:
            cursor.execute(f"ROLLBACK TO {savepoint}")
            cursor.execute(f"RELEASE {savepoint}")
        except Exception:
            pass
        return False
    finally:
        cursor.execute(f"PRAGMA foreign_keys={foreign_keys}")


def _tables_with_checks(cursor):
    cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='table'")
    return [
        r[0] for r in cursor.fetchall()
        if r[0] and r[1] and not is_system_table(r[0])
        and "CHECK" in r[1].upper() and "CHECK(" in r[1].upper().replace(" ", "")
    ]


# ---------------------------------------------------------------------------
# Duplicate-column detection
# ---------------------------------------------------------------------------

def detect_duplicate_column_translations(replacements):
    duplicates, seen = set(), {}
    for table, old_col, new_col in replacements.get("columns", []):
        key = (table.lower(), new_col)
        if key in seen:
            duplicates.add(key)
        else:
            seen[key] = old_col
    return duplicates


def _view_column_translations(replacements, view_name):
    return {
        old_col.lower(): new_col
        for table, old_col, new_col in replacements.get("columns", [])
        if table.lower() == view_name.lower()
        and old_col
        and new_col
        and old_col != new_col
    }


def create_translated_view_aliases(cursor, replacements, source_views):
    table_map = _translation_map(replacements.get("tables", []))
    existing = _schema_objects(cursor, "table") | _schema_objects(cursor, "view")

    for old_view in sorted(source_views):
        new_view = table_map.get(old_view.lower())
        if not new_view or new_view in existing:
            continue

        columns = _table_columns(cursor, old_view)
        if not columns:
            continue

        col_map = _view_column_translations(replacements, old_view)
        alias_columns = [col_map.get(col.lower(), col) for col in columns]
        column_sql = ", ".join(_quote_ident(col) for col in alias_columns)
        try:
            cursor.execute(
                f"CREATE VIEW {_quote_ident(new_view)} ({column_sql}) AS "
                f"SELECT * FROM {_quote_ident(old_view)}"
            )
            existing.add(new_view)
        except sqlite3.Error as e:
            print(f"  [Warning] view alias {old_view}->{new_view}: {e}")


# ---------------------------------------------------------------------------
# Core: apply replacements to a single DB
# ---------------------------------------------------------------------------

def replace_entities_in_db(db_path, output_db_path, replacements, values_only=False):
    if not os.path.exists(db_path):
        print(f"Warning: Source DB {db_path} not found.")
        return

    os.makedirs(os.path.dirname(output_db_path), exist_ok=True)
    shutil.copyfile(db_path, output_db_path)

    conn = sqlite3.connect(output_db_path)
    cur = conn.cursor()

    try:
        source_tables = _schema_objects(cur, "table")
        source_views = _schema_objects(cur, "view")

        # Remove CHECK constraints
        for tbl in _tables_with_checks(cur):
            if tbl not in source_tables:
                continue
            remove_check_constraints(cur, tbl)
        conn.commit()
        conn.close()
        conn = sqlite3.connect(output_db_path)
        cur = conn.cursor()
        current_tables = _schema_objects(cur, "table")

        # Step 1: values
        for table, col, old_val, new_val in replacements.get("values", []):
            if is_system_table(table) or table not in current_tables:
                continue
            actual_col, resolve_mode = _resolve_column_name(
                cur, table, col, allow_fuzzy=True
            )
            if not actual_col:
                print(f"  [Warning] value update {table}.{col}: unresolved column name")
                continue
            if resolve_mode and resolve_mode.startswith("fuzzy:"):
                print(
                    f"  [Info] value update {table}.{col}: "
                    f"resolved to {actual_col} ({resolve_mode})"
                )
            try:
                cur.execute(
                    f"UPDATE {_quote_ident(table)} "
                    f"SET {_quote_ident(actual_col)} = ? "
                    f"WHERE {_quote_ident(actual_col)} = ?",
                    (new_val, old_val),
                )
            except sqlite3.Error as e:
                print(f"  [Warning] value update {table}.{col}: {e}")

        if values_only:
            conn.commit()
            return

        # Step 2: columns
        dupes = detect_duplicate_column_translations(replacements)
        for table, old_col, new_col in replacements.get("columns", []):
            if is_system_table(table) or table not in current_tables or old_col == new_col:
                continue
            if (table.lower(), new_col) in dupes:
                continue
            actual_old_col, resolve_mode = _resolve_column_name(
                cur, table, old_col, allow_fuzzy=True
            )
            if not actual_old_col:
                print(f"  [Warning] column rename {table}.{old_col}: unresolved column name")
                continue
            if resolve_mode and resolve_mode.startswith("fuzzy:"):
                print(
                    f"  [Info] column rename {table}.{old_col}: "
                    f"resolved to {actual_old_col} ({resolve_mode})"
                )
            try:
                cur.execute(
                    f"ALTER TABLE {_quote_ident(table)} "
                    f"RENAME COLUMN {_quote_ident(actual_old_col)} TO {_quote_ident(new_col)}"
                )
            except sqlite3.Error as e:
                print(f"  [Warning] column rename {table}.{old_col}: {e}")

        # Step 3: tables
        for old_t, new_t in replacements.get("tables", []):
            if is_system_table(old_t) or old_t not in current_tables or old_t == new_t:
                continue
            try:
                cur.execute(f'ALTER TABLE `{old_t}` RENAME TO `{new_t}`')
                current_tables.remove(old_t)
                current_tables.add(new_t)
            except sqlite3.Error as e:
                print(f"  [Warning] table rename {old_t}: {e}")

        # Step 4: views
        create_translated_view_aliases(cur, replacements, source_views)

        conn.commit()
    except sqlite3.Error as e:
        print(f"  [Error] {e}")
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def validate_translation(src_db, out_db, replacements):
    if not os.path.exists(src_db) or not os.path.exists(out_db):
        return False

    sc = sqlite3.connect(src_db)
    oc = sqlite3.connect(out_db)
    try:
        s_tables = _schema_objects(sc, "table")
        s_views = _schema_objects(sc, "view")
        o_tables = _schema_objects(oc, "table")
        o_views = _schema_objects(oc, "view")
        table_map = _translation_map(replacements.get("tables", []))

        temp_tables = [
            t for t in sorted(o_tables)
            if t.startswith("_temp_") or t.startswith("_tmp_no_check_")
        ]
        if temp_tables:
            print(f"  [Fail] leftover temp tables: {temp_tables}")
            return False

        expected_tables = {
            table_map.get(t.lower(), t)
            for t in s_tables
        }
        missing_tables = sorted(expected_tables - o_tables)
        if missing_tables:
            print(f"  [Fail] missing translated tables: {missing_tables}")
            return False

        expected_view_aliases = {
            table_map[v.lower()]
            for v in s_views
            if v.lower() in table_map
        }
        missing_views = sorted(expected_view_aliases - o_views)
        if missing_views:
            print(f"  [Fail] missing translated view aliases: {missing_views}")
            return False

        for view in sorted(expected_view_aliases):
            try:
                oc.execute(f"SELECT * FROM {_quote_ident(view)} LIMIT 0")
            except sqlite3.Error as e:
                print(f"  [Fail] invalid translated view alias {view}: {e}")
                return False

        if len(s_tables) != len(o_tables):
            print(f"  [Warning] table count: {len(s_tables)} vs {len(o_tables)}")
        print(f"  [OK] Validation passed for {os.path.basename(out_db)}")
        return True
    finally:
        sc.close()
        oc.close()


# ---------------------------------------------------------------------------
# Metadata JSON update
# ---------------------------------------------------------------------------

def update_metadata_json(input_json, output_json, replacements_map, translated_db_dir=None):
    with open(input_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    for entry in data:
        db_id = entry["db_id"]
        if db_id not in replacements_map:
            continue
        rep = replacements_map[db_id]
        dupes = detect_duplicate_column_translations(rep)

        orig_tables = entry["table_names_original"]
        table_map = _translation_map(rep.get("tables", []))
        db_cols = {}
        if translated_db_dir:
            db_path = os.path.join(translated_db_dir, db_id, f"{db_id}.sqlite")
            if os.path.exists(db_path):
                try:
                    conn = sqlite3.connect(db_path)
                    cur = conn.cursor()
                    for tbl in _schema_objects(cur, "table"):
                        db_cols[tbl.lower()] = _table_columns(cur, tbl)
                except sqlite3.Error as e:
                    print(f"  [Warning] metadata check {db_id}: failed to inspect DB ({e})")
                finally:
                    try:
                        conn.close()
                    except Exception:
                        pass

        for old_t, new_t in rep.get("tables", []):
            if is_system_table(old_t):
                continue
            entry["table_names_original"] = [
                new_t if t.lower() == old_t.lower() else t
                for t in entry["table_names_original"]
            ]

        table_idx_map = {n.lower(): i for i, n in enumerate(orig_tables)}
        for table_name, old_c, new_c in rep.get("columns", []):
            if is_system_table(table_name) or (table_name.lower(), new_c) in dupes:
                continue
            t_idx = table_idx_map.get(table_name.lower())
            if t_idx is None:
                continue
            cols_for_table = [
                col_orig
                for col_orig in entry["column_names_original"]
                if col_orig[0] == t_idx
            ]
            existing_names = [col_orig[1] for col_orig in cols_for_table]
            actual_old_c, resolve_mode = _resolve_name_from_candidates(
                existing_names, old_c, allow_fuzzy=True
            )
            if not actual_old_c:
                print(
                    f"  [Warning] metadata column rename {db_id}.{table_name}.{old_c}: "
                    "unresolved source column name"
                )
                continue

            translated_table = table_map.get(table_name.lower(), table_name)
            translated_cols = db_cols.get(translated_table.lower())
            if translated_cols:
                actual_new_c, _ = _resolve_name_from_candidates(
                    translated_cols, new_c, allow_fuzzy=False
                )
                if not actual_new_c:
                    print(
                        f"  [Warning] metadata column rename {db_id}.{table_name}.{old_c}: "
                        f"target column {new_c} not present in translated DB table {translated_table}"
                    )
                    continue
            if resolve_mode and str(resolve_mode).startswith("fuzzy:"):
                print(
                    f"  [Info] metadata column rename {db_id}.{table_name}.{old_c}: "
                    f"resolved to {actual_old_c} ({resolve_mode})"
                )

            for col_orig in cols_for_table:
                if _normalize_ident(col_orig[1]) == _normalize_ident(actual_old_c):
                    col_orig[1] = new_c
                    break

    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=3, ensure_ascii=False)
    print(f"Metadata saved to {output_json}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build translated SQLite DBs and update schema JSON.")
    parser.add_argument("--replacements-config", required=True, help="Replacements config JSON")
    parser.add_argument("--source-dir", required=True,
                        help="Source dataset directory (contains database/ and tables.json)")
    parser.add_argument("--output-dir", required=True,
                        help="Output dataset directory (database/ and tables.json will be created)")
    parser.add_argument("--values-only", action="store_true",
                        help="Only update cell values; skip column/table renames (for BULL)")
    args = parser.parse_args()

    source_db_dir = os.path.join(args.source_dir, STD_DB_DIR)
    output_db_dir = os.path.join(args.output_dir, STD_DB_DIR)
    input_tables = os.path.join(args.source_dir, STD_TABLES_FILE)
    output_tables = os.path.join(args.output_dir, STD_TABLES_FILE)

    replacements_config = load_json(args.replacements_config)
    if not replacements_config:
        print("Error: empty replacements config.")
        sys.exit(1)

    for db_id, tasks in replacements_config.items():
        print(f"Processing: {db_id}...")
        src = os.path.join(source_db_dir, db_id, f"{db_id}.sqlite")
        out = os.path.join(output_db_dir, db_id, f"{db_id}.sqlite")
        replace_entities_in_db(src, out, tasks, values_only=args.values_only)
        validate_translation(src, out, tasks)

    if not args.values_only:
        update_metadata_json(
            input_tables,
            output_tables,
            replacements_config,
            translated_db_dir=output_db_dir,
        )

    print("Done.")
