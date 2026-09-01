#!/usr/bin/env python3
"""
Translate SQL queries between languages using schema maps and
a replacements config.  Supports EN→CN and CN→EN via ``--direction``.

Merged from CrossLangSQL-Spider and CrossLangSQL-BIRD with BIRD's
hardened logic as the default (per-table column grouping, innermost-
subquery peeling, backtick-identifier protection, query timeout).
"""

import argparse
import json
import os
import re
import sqlite3
import sys
from collections import defaultdict
from typing import Iterable

from tqdm import tqdm

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import STD_DB_DIR, STD_DEV_JSON_FILE, STD_DEV_SQL_FILE, STD_TABLES_FILE, get_config
from utils import execute_query, load_json


# ---------------------------------------------------------------------------
# Schema mapping
# ---------------------------------------------------------------------------

def build_precise_maps(db_id, tables_src, tables_tgt):
    """Build table/column/value maps from paired source and target schema JSONs."""
    src = next((i for i in tables_src if i["db_id"] == db_id), None)
    tgt = next((i for i in tables_tgt if i["db_id"] == db_id), None)
    if not src or not tgt:
        return None

    table_map = {}
    for s, t in zip(src["table_names_original"], tgt["table_names_original"]):
        table_map[s.lower()] = t

    src_by_table = defaultdict(list)
    tgt_by_table = defaultdict(list)
    for col in src["column_names_original"]:
        if col[0] != -1:
            src_by_table[col[0]].append(col)
    for col in tgt["column_names_original"]:
        if col[0] != -1:
            tgt_by_table[col[0]].append(col)

    column_map = {}
    for tidx in src_by_table:
        if tidx not in tgt_by_table:
            continue
        for sc, tc in zip(src_by_table[tidx], tgt_by_table[tidx]):
            tname = src["table_names_original"][sc[0]]
            column_map[(tname.lower(), sc[1].lower())] = tc[1]

    col_to_tables = {}
    for (table, col), tgt_col in column_map.items():
        col_to_tables.setdefault(col, []).append((table, tgt_col))

    return {
        "table_map": table_map,
        "column_map": column_map,
        "col_to_tables": col_to_tables,
        "src_tables": set(table_map.keys()),
    }


# ---------------------------------------------------------------------------
# SQL helpers
# ---------------------------------------------------------------------------

_SQL_KEYWORDS = {
    "on", "where", "join", "left", "right", "inner", "outer", "cross",
    "natural", "as", "and", "or", "group", "order", "limit", "having",
    "union", "intersect", "except", "select", "from", "set", "into",
    "values", "not", "in", "between", "like", "is", "null", "true", "false",
    "case", "when", "then", "else", "end", "asc", "desc", "by", "distinct",
}

_MAX_SQL_TRANSLATE_DEPTH = 50


def _needs_quoting(ident):
    return any(ord(c) > 127 for c in ident)


def _quote(ident):
    return f"`{ident}`" if _needs_quoting(ident) else ident


# --- string-literal protection ---

def protect_string_literals(sql):
    literals, mid = {}, [0]
    def _repl(m):
        marker = f"__STRING_LITERAL_{mid[0]}__"
        literals[marker] = m.group(0)
        mid[0] += 1
        return marker
    out = re.sub(r"'(?:[^'\\]|\\.)*'|\"(?:[^\"\\]|\\.)*\"", _repl, sql)
    return out, literals


def restore_string_literals(sql, literals):
    for marker, lit in literals.items():
        sql = sql.replace(marker, lit)
    return sql


# --- backtick-identifier protection ---

def protect_backtick_identifiers(sql):
    markers, mid = {}, [0]
    def _repl(m):
        marker = f"__BACKTICK_IDENT_{mid[0]}__"
        markers[marker] = m.group(0)
        mid[0] += 1
        return marker
    out = re.sub(r"`[^`]*`", _repl, sql)
    return out, markers


def restore_backtick_identifiers(sql, markers):
    for marker, orig in markers.items():
        sql = sql.replace(marker, orig)
    return sql


# --- table-position protection ---

def protect_table_positions(sql, src_tables):
    markers, mid = {}, [0]
    for table in sorted(src_tables, key=len, reverse=True):
        def _make_repl(tbl):
            def _repl(m):
                marker = f"__TABLE_MARKER_{mid[0]}__"
                markers[marker] = tbl
                mid[0] += 1
                return f"{m.group(1)}{marker}{m.group(3)}"
            return _repl
        tail = r"(\s+AS\s+|\s+(?=[A-Za-z])|\s*(?=[,\)])|\s+(?:WHERE|ON|GROUP|ORDER|LIMIT|HAVING|UNION|INTERSECT|EXCEPT|;|$))"
        for kw in ("FROM", "JOIN"):
            pat = rf"(\b{kw}\s+)`?({re.escape(table)})`?{tail}"
            sql = re.sub(pat, _make_repl(table), sql, flags=re.IGNORECASE)
    return sql, markers


def restore_table_markers(sql, markers, table_map):
    for marker, en_t in markers.items():
        cn_t = table_map.get(en_t.lower(), en_t)
        sql = sql.replace(marker, _quote(cn_t))
    return sql


# --- CTE identifier protection ---

def extract_cte_names(sql):
    """Return CTE names introduced by a top-level WITH clause.

    CTE identifiers are local SQL aliases, not schema identifiers.  They can
    collide with real column names (e.g. f1 has a ``max_points`` column), so
    protecting them prevents the column replacement pass from renaming only
    part of the CTE reference graph.
    """
    if not re.search(r"\bWITH\b", sql, re.IGNORECASE):
        return set()
    return {
        m.group(1).lower()
        for m in re.finditer(
            r"(?:\bWITH\b|,)\s+(?:RECURSIVE\s+)?`?(\w+)`?\s+AS\s*\(",
            sql, re.IGNORECASE,
        )
    }


def protect_cte_identifiers(sql, cte_names):
    markers, mid = {}, [0]

    def _marker(name):
        marker = f"__CTE_IDENT_{mid[0]}__"
        markers[marker] = name
        mid[0] += 1
        return marker

    for name in sorted(cte_names, key=len, reverse=True):
        # WITH/`,` declaration position: ``max_points AS (...)``.
        def _decl_repl(m):
            return f"{m.group(1)}{_marker(m.group(2))}{m.group(3)}"
        sql = re.sub(
            rf"(\bWITH\s+(?:RECURSIVE\s+)?|,\s*)`?({re.escape(name)})`?(\s+AS\s*\()",
            _decl_repl, sql, flags=re.IGNORECASE,
        )

        # Relation position: ``FROM max_points`` / ``JOIN max_points``.
        def _from_repl(m):
            return f"{m.group(1)}{_marker(m.group(2))}{m.group(3)}"
        sql = re.sub(
            rf"(\b(?:FROM|JOIN)\s+)`?({re.escape(name)})`?(\b)",
            _from_repl, sql, flags=re.IGNORECASE,
        )

        # Qualified-prefix position: ``max_points.year``.
        sql = re.sub(
            rf"\b{re.escape(name)}\b(?=\s*\.)",
            lambda m: _marker(m.group(0)),
            sql,
            flags=re.IGNORECASE,
        )

    return sql, markers


def restore_cte_identifiers(sql, markers):
    for marker, ident in markers.items():
        sql = sql.replace(marker, ident)
    return sql


# --- alias / FROM-table extraction ---

def extract_table_aliases(sql, src_tables):
    alias_map = {}
    for m in re.finditer(r"(?:FROM|JOIN)\s+(\w+)\s+AS\s+(\w+)", sql, re.IGNORECASE):
        t, a = m.groups()
        if t.lower() in src_tables:
            alias_map[a.lower()] = t.lower()
    for m in re.finditer(r"(?:FROM|JOIN)\s+(\w+)\s+(\w+)", sql, re.IGNORECASE):
        t, a = m.groups()
        tl, al = t.lower(), a.lower()
        if tl in src_tables and al not in _SQL_KEYWORDS and al not in src_tables:
            alias_map[al] = tl
    for t in src_tables:
        alias_map.setdefault(t, t)
    return alias_map


def extract_from_tables(sql, src_tables):
    tables = set()
    for m in re.finditer(r"(?:FROM|JOIN)\s+`?(\w+)`?", sql, re.IGNORECASE):
        t = m.group(1).lower()
        if t in src_tables:
            tables.add(t)
    return tables


# --- subquery handling ---

def find_subqueries(sql):
    subs, depth, start = [], 0, -1
    for i, c in enumerate(sql):
        if c == "(":
            if depth == 0:
                start = i
            depth += 1
        elif c == ")":
            depth -= 1
            if depth == 0 and start != -1:
                content = sql[start + 1 : i]
                if re.search(r"\bSELECT\b", content, re.IGNORECASE):
                    subs.append((start, i + 1, content))
                start = -1
    return subs


def find_innermost_subqueries(sql):
    return [s for s in find_subqueries(sql) if not find_subqueries(s[2])]


# ---------------------------------------------------------------------------
# Column-aware value replacement helpers
# ---------------------------------------------------------------------------

def _resolve_col_table(prefix, col, alias_map, query_tables, col_to_tables):
    """Return (table_lower | None, col_lower) for a column reference."""
    cl = col.lower()
    if prefix:
        return (alias_map.get(prefix.lower()), cl)
    possible = col_to_tables.get(cl, [])
    if len(possible) == 1:
        return (possible[0][0], cl)
    relevant = [t for t, _ in possible if t in query_tables]
    if len(relevant) == 1:
        return (relevant[0], cl)
    return (None, cl)


def _extract_marker_column_context(protected_sql, alias_map, query_tables, col_to_tables):
    """Map each __STRING_LITERAL_N__ marker to (table_lower | None, col_lower).

    Scans the SQL for patterns like ``column = MARKER``, ``column LIKE MARKER``,
    and ``column IN (MARKER, ...)`` so that value replacements can be restricted
    to the correct (table, column) pair.
    """
    ctx = {}

    # [prefix.]column op MARKER
    for m in re.finditer(
        r'(?:(\w+)\.)?(\w+)\s*(?:=|!=|<>|(?:NOT\s+)?LIKE)\s*(__STRING_LITERAL_\d+__)',
        protected_sql, re.IGNORECASE,
    ):
        prefix, col, marker = m.group(1), m.group(2), m.group(3)
        if marker not in ctx and not col.startswith("__"):
            ctx[marker] = _resolve_col_table(prefix, col, alias_map, query_tables, col_to_tables)

    # MARKER op [prefix.]column  (reversed comparison)
    for m in re.finditer(
        r'(__STRING_LITERAL_\d+__)\s*(?:=|!=|<>)\s*(?:(\w+)\.)?(\w+)',
        protected_sql, re.IGNORECASE,
    ):
        marker, prefix, col = m.group(1), m.group(2), m.group(3)
        if marker not in ctx and col.lower() not in _SQL_KEYWORDS and not col.startswith("__"):
            ctx[marker] = _resolve_col_table(prefix, col, alias_map, query_tables, col_to_tables)

    # column IN (…MARKER…)
    for m in re.finditer(
        r'(?:(\w+)\.)?(\w+)\s+(?:NOT\s+)?IN\s*\(([^)]+)\)',
        protected_sql, re.IGNORECASE,
    ):
        prefix, col, body = m.group(1), m.group(2), m.group(3)
        if col.startswith("__"):
            continue
        info = _resolve_col_table(prefix, col, alias_map, query_tables, col_to_tables)
        for mm in re.finditer(r'__STRING_LITERAL_\d+__', body):
            mk = mm.group(0)
            if mk not in ctx:
                ctx[mk] = info

    return ctx


# ---------------------------------------------------------------------------
# Single-level SQL translation
# ---------------------------------------------------------------------------

def translate_sql_single_level(sql, maps, db_replacements, outer_cte_names=None):
    table_map = maps["table_map"]
    column_map = maps["column_map"]
    col_to_tables = maps["col_to_tables"]
    src_tables = maps["src_tables"]

    translated, string_lits = protect_string_literals(sql)
    cte_names = set(outer_cte_names or set()) | extract_cte_names(sql)
    translated, cte_markers = protect_cte_identifiers(translated, cte_names)
    alias_map = extract_table_aliases(sql, src_tables)
    query_tables = extract_from_tables(sql, src_tables)
    translated, table_markers = protect_table_positions(translated, src_tables)

    # Column-aware value replacements inside string literals.
    # Each replacement entry carries (table, column, old, new).  We only apply
    # a replacement when the marker's column context matches the entry's
    # (table, column) pair, preventing cross-column value leakage.
    marker_ctx = _extract_marker_column_context(
        translated, alias_map, query_tables, col_to_tables
    )
    sorted_values = sorted(
        db_replacements.get("values", []), key=lambda x: len(str(x[2])), reverse=True
    )
    for marker, lit in list(string_lits.items()):
        ctx = marker_ctx.get(marker)
        for repl_tbl, repl_col, old_v, new_v in sorted_values:
            if lit != f"'{old_v}'" and lit != f'"{old_v}"':
                continue
            # ``repl_tbl`` / ``repl_col`` in db_replacements["values"] are
            # SOURCE-language names (matching the source SQL and ``column_map``
            # keys), so the marker's resolved (table, col) must be compared
            # against them in the source language. Comparing against the
            # translated ``tgt_col`` would never match once the schema itself
            # has been translated (e.g. ``eventtype`` -> ``事件类型``), which
            # silently dropped every value replacement on translated schemas.
            if ctx is not None:
                src_table, src_col = ctx
                if src_table is not None:
                    if repl_tbl.lower() != src_table or repl_col.lower() != src_col.lower():
                        continue
                else:
                    # Couldn't pin a single source table — require the column
                    # name to match and the entry's table to be one of the
                    # tables referenced by this query.
                    if (repl_col.lower() != src_col.lower()
                            or repl_tbl.lower() not in query_tables):
                        continue
            escaped = str(new_v).replace("'", "''") if lit.startswith("'") else str(new_v).replace('"', '""')
            string_lits[marker] = f"'{escaped}'" if lit.startswith("'") else f'"{escaped}"'
            break

    # qualified columns (alias.column)
    def _repl_qualified(m):
        prefix, col = m.group(1), m.group(2)
        pl, cl = prefix.lower(), col.lower()
        actual = alias_map.get(pl, pl)
        key = (actual, cl)
        if key in column_map:
            nc = column_map[key]
        else:
            possible = col_to_tables.get(cl, [])
            if len(possible) == 1:
                nc = possible[0][1]
            elif possible:
                relevant = [(t, cn) for t, cn in possible if t in query_tables]
                nc = relevant[0][1] if relevant else possible[0][1]
            else:
                nc = col
        np = table_map.get(pl, prefix) if pl in src_tables else prefix
        qp = _quote(np) if pl in src_tables else np
        return f"{qp}.{_quote(nc)}"

    translated = re.sub(r"\b(\w+)\.(\w+)\b", _repl_qualified, translated)

    # standalone columns – protect already-translated (non-ASCII) backtick
    # identifiers so the standalone regex doesn't double-replace substrings
    # inside them, while leaving original English backtick idents untouched
    _bt_mid = [0]
    _bt_pre = {}
    def _protect_translated(m):
        ident = m.group(0)
        if any(ord(c) > 127 for c in ident):
            marker = f"__BT_TRANSLATED_{_bt_mid[0]}__"
            _bt_pre[marker] = ident
            _bt_mid[0] += 1
            return marker
        return ident
    translated = re.sub(r"`[^`]*`", _protect_translated, translated)
    translated_lower = translated.lower()
    for col in sorted(col_to_tables, key=len, reverse=True):
        if col.lower() not in translated_lower:
            continue
        possible = col_to_tables[col]
        if len(possible) == 1:
            nc = possible[0][1]
        else:
            relevant = [(t, cn) for t, cn in possible if t in query_tables]
            nc = (relevant[0][1] if relevant else possible[0][1]) if relevant or possible else col
        qc = _quote(nc)
        translated = re.sub(rf"`{re.escape(col)}`", qc, translated, flags=re.IGNORECASE)
        translated = re.sub(
            rf"(?<!\.)(?<!\w)\b{re.escape(col)}\b(?!\s*\.)(?!\w)(?!\s*\()",
            qc, translated, flags=re.IGNORECASE,
        )
    for marker, orig in _bt_pre.items():
        translated = translated.replace(marker, orig)

    translated = restore_table_markers(translated, table_markers, table_map)

    translated, bt_idents = protect_backtick_identifiers(translated)
    kw_phrases = ("order", "group")
    for old_t in sorted(table_map, key=len, reverse=True):
        new_t = table_map[old_t]
        pat = rf"\b{re.escape(old_t)}\b"
        if old_t.lower() in kw_phrases:
            pat += r"(?!\s+BY\b)"
        translated = re.sub(pat, _quote(new_t), translated, flags=re.IGNORECASE)
    translated = restore_backtick_identifiers(translated, bt_idents)

    translated = restore_cte_identifiers(translated, cte_markers)
    translated = restore_string_literals(translated, string_lits)
    return translated


# ---------------------------------------------------------------------------
# Recursive translation (innermost-first)
# ---------------------------------------------------------------------------

def translate_sql_recursive(sql, maps, db_reps, depth=0, cte_names=None):
    active_cte_names = set(cte_names or set()) | extract_cte_names(sql)
    if depth > _MAX_SQL_TRANSLATE_DEPTH:
        return translate_sql_single_level(sql, maps, db_reps, active_cte_names)
    innermost = find_innermost_subqueries(sql)
    if not innermost:
        return translate_sql_single_level(sql, maps, db_reps, active_cte_names)
    innermost.sort(key=lambda x: x[0], reverse=True)
    t = sql
    for start, end, sub in innermost:
        ts = translate_sql_recursive(sub, maps, db_reps, depth + 1, active_cte_names)
        t = t[: start + 1] + ts + t[end - 1 :]
    return translate_sql_single_level(t, maps, db_reps, active_cte_names)


def translate_sql(sql, maps, db_reps):
    return translate_sql_recursive(sql, maps, db_reps)


# ---------------------------------------------------------------------------
# Tokenisation (for query_toks / query_toks_no_value)
# ---------------------------------------------------------------------------

def tokenize_sql(sql):
    tokens, i = [], 0
    sql = sql.strip()
    while i < len(sql):
        if sql[i].isspace():
            i += 1; continue
        if sql[i] == "`":
            j = i + 1
            while j < len(sql) and sql[j] != "`":
                j += 1
            tokens.append(sql[i : j + 1]); i = j + 1; continue
        if sql[i] == "'":
            j = i + 1
            while j < len(sql):
                if sql[j] == "'" and (j + 1 >= len(sql) or sql[j + 1] != "'"):
                    break
                if sql[j] == "'" and j + 1 < len(sql) and sql[j + 1] == "'":
                    j += 2; continue
                j += 1
            tokens.append(sql[i : j + 1]); i = j + 1; continue
        if sql[i] == '"':
            j = i + 1
            while j < len(sql):
                if sql[j] == '"' and (j + 1 >= len(sql) or sql[j + 1] != '"'):
                    break
                if sql[j] == '"' and j + 1 < len(sql) and sql[j + 1] == '"':
                    j += 2; continue
                j += 1
            tokens.append(sql[i : j + 1]); i = j + 1; continue
        two = sql[i : i + 2]
        if two in (">=", "<=", "<>", "!=", "||"):
            tokens.append(two); i += 2; continue
        if sql[i] in "(),;=<>+-*/.":
            tokens.append(sql[i]); i += 1; continue
        if sql[i].isdigit() or (sql[i] == "." and i + 1 < len(sql) and sql[i + 1].isdigit()):
            j = i
            while j < len(sql) and (sql[j].isdigit() or sql[j] == "."):
                j += 1
            tokens.append(sql[i:j]); i = j; continue
        if sql[i].isalnum() or sql[i] == "_" or ord(sql[i]) > 127:
            j = i
            while j < len(sql) and (sql[j].isalnum() or sql[j] == "_" or ord(sql[j]) > 127):
                j += 1
            tokens.append(sql[i:j]); i = j; continue
        i += 1
    return tokens


def tokenize_sql_no_value(sql):
    tokens = tokenize_sql(sql)
    result = []
    for tok in tokens:
        if (tok.startswith("'") and tok.endswith("'")) or (tok.startswith('"') and tok.endswith('"')):
            result.append("value")
        elif tok.replace(".", "").isdigit():
            result.append(tok)
        elif tok.startswith("`") and tok.endswith("`"):
            result.append(tok[1:-1].lower())
        else:
            result.append(tok.lower())
    return result


# ---------------------------------------------------------------------------
# Result comparison
# ---------------------------------------------------------------------------

def is_structure_match(en_res, cn_res):
    if not isinstance(en_res, list) or not isinstance(cn_res, list):
        return False
    if len(en_res) != len(cn_res):
        return False
    if en_res and isinstance(en_res[0], Iterable) and isinstance(cn_res[0], Iterable):
        for er, cr in zip(en_res, cn_res):
            if len(er) != len(cr):
                return False
    return True


def load_db_schema(db_path):
    schema = {}
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
        for (tbl,) in cur.fetchall():
            cur.execute(f"PRAGMA table_info(`{tbl}`)")
            schema[tbl] = [c[1] for c in cur.fetchall()]
        conn.close()
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    return schema


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Translate SQL (EN↔CN) using schema maps.")
    parser.add_argument("--dataset", required=True, help="Base dataset name (for config: sql_field, encoding)")
    parser.add_argument("--source-dir", required=True, help="Source-language dataset directory")
    parser.add_argument("--target-dir", required=True, help="Target-language dataset directory")
    parser.add_argument("--direction", default=None, choices=["en2cn", "cn2en"],
                        help="Translation direction (default: from dataset config)")
    parser.add_argument("--replacements", required=True, help="Replacements config JSON")
    parser.add_argument("--output-dir", required=True, help="Output directory")
    parser.add_argument("--manual-sql", default=None, help="Optional manual SQL overrides JSON")
    parser.add_argument("--execute-timeout", type=float, default=10, help="Max seconds per query (default: 10)")
    args = parser.parse_args()

    cfg = get_config(args.dataset)
    direction = args.direction or cfg.translate_direction

    src_db_dir = os.path.join(args.source_dir, STD_DB_DIR)
    tgt_db_dir = os.path.join(args.target_dir, STD_DB_DIR)
    tables_src_path = os.path.join(args.source_dir, STD_TABLES_FILE)
    tables_tgt_path = os.path.join(args.target_dir, STD_TABLES_FILE)
    dev_json_path = os.path.join(args.source_dir, STD_DEV_JSON_FILE)

    # Encoding: source uses the dataset's native encoding; target is always
    # the "other" language's default (utf-8 for CN, cfg.db_encoding for EN).
    if direction == "en2cn":
        src_encoding = cfg.db_encoding
        tgt_encoding = "utf-8"
    else:
        src_encoding = "utf-8"
        tgt_encoding = cfg.db_encoding

    TABLES_SRC = load_json(tables_src_path)
    TABLES_TGT = load_json(tables_tgt_path)
    REPLACEMENTS = load_json(args.replacements)
    dev_data = load_json(dev_json_path)
    manual = load_json(args.manual_sql) if args.manual_sql and os.path.exists(args.manual_sql) else []

    output_json = os.path.join(args.output_dir, STD_DEV_JSON_FILE)
    output_gold = os.path.join(args.output_dir, STD_DEV_SQL_FILE)
    os.makedirs(args.output_dir, exist_ok=True)

    out_entries, gold_lines = [], []
    stats = {"success": 0, "fail": 0, "warning": 0}

    for i, entry in enumerate(tqdm(dev_data)):
        db_id = entry.get("db_id") or entry.get("db_name", "")
        src_sql = entry.get(cfg.sql_field) or entry.get("SQL") or entry.get("query") or entry.get("sql_query")
        if not src_sql:
            stats["fail"] += 1
            continue

        maps = build_precise_maps(db_id, TABLES_SRC, TABLES_TGT)
        if not maps:
            stats["fail"] += 1
            continue

        db_reps = REPLACEMENTS.get(db_id, {})
        tgt_sql = translate_sql(src_sql, maps, db_reps)

        src_res = execute_query(
            os.path.join(src_db_dir, db_id, f"{db_id}.sqlite"),
            src_sql, encoding=src_encoding, timeout=args.execute_timeout,
        )
        tgt_res = execute_query(
            os.path.join(tgt_db_dir, db_id, f"{db_id}.sqlite"),
            tgt_sql, encoding=tgt_encoding, timeout=args.execute_timeout,
        )

        timeout_src = src_res == "Error: timeout"
        timeout_tgt = tgt_res == "Error: timeout"

        if not timeout_src and not timeout_tgt and src_res is not None and src_res == tgt_res:
            stats["success"] += 1
        elif is_structure_match(src_res, tgt_res):
            stats["warning"] += 1
        else:
            flag = False
            for item in manual:
                if item.get("src_sql") == src_sql or item.get("en_sql") == src_sql or item.get("gold_sql") == src_sql:
                    tgt_sql = item.get("tgt_sql") or item.get("cn_sql") or item.get("translated_sql") or tgt_sql
                    stats["success"] += 1
                    flag = True
                    break
            if not flag:
                stats["fail"] += 1

        entry["original_sql"] = src_sql
        entry["SQL"] = tgt_sql
        entry["query"] = tgt_sql
        entry["query_toks"] = tokenize_sql(tgt_sql)
        entry["query_toks_no_value"] = tokenize_sql_no_value(tgt_sql)
        out_entries.append(entry)
        gold_lines.append(f"{tgt_sql}\t{db_id}\n")

    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(out_entries, f, indent=2, ensure_ascii=False)
    with open(output_gold, "w", encoding="utf-8") as f:
        f.writelines(gold_lines)

    arrow = "EN→CN" if direction == "en2cn" else "CN→EN"
    print(f"\nDone ({arrow}). Success: {stats['success']}, Fail: {stats['fail']}, Warning: {stats['warning']}")


if __name__ == "__main__":
    main()
