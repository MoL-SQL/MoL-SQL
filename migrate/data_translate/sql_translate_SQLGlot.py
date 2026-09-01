#!/usr/bin/env python3
"""
SQLGlot-based SQL translation (EN↔CN).

Drop-in alternative to the regex pipeline in ``sql_translate.py`` /
``sql_translate_CTE.py``.  Instead of "protect → replace → restore" string
surgery, the query is parsed into an AST (``sqlglot.parse_one``), every column
is resolved to its source relation with the schema-aware qualifier
(``sqlglot.optimizer.qualify``), and identifiers are renamed directly on the
tree:

* columns / tables whose source is a *base table* are renamed via the
  ``column_map`` / ``table_map`` built by ``build_precise_maps()``;
* columns whose source is a CTE or derived table keep their source-language
  names — ``qualify`` injects explicit ``AS <name>`` projection aliases, so the
  virtual-relation namespace stays consistent (what ``translate_sql_CTE``
  approximates with regexes);
* value replacements are applied on exact (table, column, value) matches by
  resolving each string literal's column context from its comparison node.

On any parse/qualify error the translator falls back to the legacy
``translate_sql`` so no query is ever dropped.
"""

import argparse
import json
import os
import sys

import sqlglot
from sqlglot import exp
from sqlglot.dialects.sqlite import SQLite
from sqlglot.optimizer.qualify import qualify
from sqlglot.optimizer.scope import traverse_scope
from tqdm import tqdm

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import STD_DB_DIR, STD_TABLES_FILE, get_config, get_split_files
from utils import execute_query, load_json

from sql_translate import (
    build_precise_maps,
    is_structure_match,
    tokenize_sql,
    tokenize_sql_no_value,
    translate_sql,
)


# ---------------------------------------------------------------------------
# Output dialect: SQLite with backtick identifiers
# ---------------------------------------------------------------------------

class SQLiteBacktick(SQLite):
    """SQLite dialect that emits backtick-quoted identifiers.

    The datasets consistently use backticks around translated (non-ASCII)
    identifiers, so generation must match that style instead of the SQL
    standard double quotes.
    """

    class Tokenizer(SQLite.Tokenizer):
        IDENTIFIERS = ["`", '"', ("[", "]")]


READ_DIALECT = "sqlite"


def _needs_quoting(ident):
    return any(ord(c) > 127 for c in ident)


# ---------------------------------------------------------------------------
# Schema helpers
# ---------------------------------------------------------------------------

def build_sqlglot_schema(maps):
    """Build a ``{table: {column: type}}`` mapping in the *source* language.

    ``qualify`` only needs column membership, not real types, so every column
    is declared as TEXT.  Names are lowercased; sqlglot's SQLite normalization
    is case-insensitive so lookups still work for any casing in the SQL.
    """
    schema = {}
    for (table, col) in maps["column_map"]:
        schema.setdefault(table, {})[col] = "TEXT"
    return schema


def _known_identifier_names(ast, schema):
    """All identifier names (lowercased) that may legally appear as columns."""
    known = {c for cols in schema.values() for c in cols}
    known |= set(schema)
    for alias in ast.find_all(exp.TableAlias):
        known.add(alias.name.lower())
    for alias in ast.find_all(exp.Alias):
        known.add(alias.alias.lower())
    for cte in ast.find_all(exp.CTE):
        known.add(cte.alias.lower())
    return known


def fix_double_quoted_literals(ast, schema):
    """Convert Spider-style ``"value"`` pseudo-identifiers to string literals.

    Spider gold SQL frequently writes string values in double quotes.  The
    SQLite parser reads those as quoted identifiers, which breaks column
    qualification.  Real SQLite applies the same fallback at runtime (an
    unresolvable double-quoted identifier becomes a string), so mirroring it
    here is faithful: any quoted, unqualified column whose name is not a known
    column/table/alias becomes a string literal.
    """
    known = _known_identifier_names(ast, schema)
    for col in list(ast.find_all(exp.Column)):
        ident = col.this
        if (
            isinstance(ident, exp.Identifier)
            and ident.args.get("quoted")
            and not col.table
            and ident.name.lower() not in known
        ):
            col.replace(exp.Literal.string(ident.name))
    return ast


# ---------------------------------------------------------------------------
# Value replacement
# ---------------------------------------------------------------------------

def _base_table_of(scope, qualifier):
    """Return the lowercased base-table name behind ``qualifier`` (or None)."""
    source = scope.sources.get(qualifier)
    if isinstance(source, exp.Table):
        return source.name.lower()
    return None


def _column_context(literal, scope):
    """Resolve the (source_table, source_column) a string literal is compared to.

    Walks up from the literal to the nearest comparison-like ancestor
    (=, !=, <>, LIKE, IN, BETWEEN) and resolves the column on the other side
    through the scope's sources.  Returns ``None`` when no column context can
    be pinned (e.g. literals inside function calls).
    """
    node = literal
    while node.parent is not None:
        parent = node.parent
        if isinstance(parent, (exp.EQ, exp.NEQ, exp.Like, exp.ILike, exp.In, exp.Between)):
            column = parent.find(exp.Column)
            if column is not None and column.table:
                table = _base_table_of(scope, column.table)
                if table is not None:
                    return (table, column.name.lower())
            return None
        if isinstance(parent, (exp.Select, exp.Where, exp.Having)):
            return None
        node = parent
    return None


def apply_value_replacements(qualified, db_replacements):
    """Apply (table, column, old, new) value replacements on string literals.

    Must run *before* identifier renaming so the resolved column context is
    still in the source language (matching the replacement entries).
    """
    values = db_replacements.get("values", [])
    if not values:
        return

    for scope in traverse_scope(qualified):
        for literal in scope.expression.find_all(exp.Literal):
            if not literal.is_string:
                continue
            # Only touch literals that belong to this scope directly (not to a
            # nested subquery scope, which traverse_scope visits separately).
            select_ancestor = literal.find_ancestor(exp.Select)
            if select_ancestor is not scope.expression:
                continue
            ctx = _column_context(literal, scope)
            for repl_tbl, repl_col, old_v, new_v in values:
                if literal.this != str(old_v):
                    continue
                if ctx is not None:
                    if (repl_tbl.lower(), repl_col.lower()) != ctx:
                        continue
                literal.set("this", str(new_v))
                break


# ---------------------------------------------------------------------------
# Identifier renaming
# ---------------------------------------------------------------------------

def _rename_identifier(ident, new_name):
    ident.set("this", new_name)
    ident.set("quoted", _needs_quoting(new_name))


def rename_columns(qualified, maps):
    """Rename every column whose source is a base table via ``column_map``.

    Columns sourced from CTEs / derived tables are left untouched: their
    namespace is defined by the (source-language) projection aliases that
    ``qualify`` made explicit.
    """
    column_map = maps["column_map"]
    for scope in traverse_scope(qualified):
        for col in scope.columns:
            table = _base_table_of(scope, col.table)
            if table is None:
                continue
            new_col = column_map.get((table, col.name.lower()))
            if new_col is not None:
                _rename_identifier(col.this, new_col)


def rename_tables(qualified, maps):
    """Rename base tables via ``table_map``.

    ``qualify`` gives unaliased tables an auto-alias equal to their own name
    (``FROM stadium AS stadium``).  Those auto-aliases — and every column
    qualifier that uses them — are renamed to the target language as well, so
    no source-language identifier survives.  User-written aliases (``AS T1``)
    are preserved.
    """
    table_map = maps["table_map"]
    for scope in traverse_scope(qualified):
        renamed_aliases = {}
        for alias_name, source in scope.sources.items():
            if not isinstance(source, exp.Table):
                continue
            src_name = source.name.lower()
            new_table = table_map.get(src_name)
            if new_table is None:
                continue
            auto_alias = alias_name.lower() == src_name
            _rename_identifier(source.this, new_table)
            if auto_alias and source.args.get("alias"):
                # Drop the redundant auto-alias qualify added for unaliased
                # tables and point former qualifiers at the new table name.
                source.set("alias", None)
                renamed_aliases[alias_name] = new_table
        if renamed_aliases:
            for col in scope.columns:
                new_qualifier = renamed_aliases.get(col.table)
                if new_qualifier is not None:
                    _rename_identifier(col.args["table"], new_qualifier)


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def translate_sql_sqlglot(sql, maps, db_reps, verbose_fallback=True):
    """AST-based translation with fallback to the legacy regex translator."""
    try:
        schema = build_sqlglot_schema(maps)
        ast = sqlglot.parse_one(sql, read=READ_DIALECT)
        ast = fix_double_quoted_literals(ast, schema)
        qualified = qualify(
            ast,
            schema=schema,
            dialect=READ_DIALECT,
            quote_identifiers=False,
        )
        apply_value_replacements(qualified, db_reps)
        rename_columns(qualified, maps)
        rename_tables(qualified, maps)
        return qualified.sql(dialect=SQLiteBacktick)
    except Exception as e:
        if verbose_fallback:
            print(f"[sqlglot fallback] {type(e).__name__}: {e} | sql={sql!r}")
        return translate_sql(sql, maps, db_reps)


# ---------------------------------------------------------------------------
# CLI (standalone, mirrors sql_translate.py)
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Translate SQL (EN↔CN) using SQLGlot AST rewriting."
    )
    parser.add_argument("--dataset", required=True,
                        help="Base dataset name (for config: sql_field, encoding)")
    parser.add_argument("--source-dir", required=True,
                        help="Source-language dataset directory")
    parser.add_argument("--target-dir", required=True,
                        help="Target-language dataset directory")
    parser.add_argument("--direction", default=None, choices=["en2cn", "cn2en"],
                        help="Translation direction (default: from dataset config)")
    parser.add_argument("--replacements", required=True,
                        help="Replacements config JSON")
    parser.add_argument("--output-dir", required=True, help="Output directory")
    parser.add_argument("--split", default="dev",
                        help="Data split to translate (default: dev)")
    parser.add_argument("--execute-timeout", type=float, default=10,
                        help="Max seconds per query (default: 10)")
    args = parser.parse_args()

    cfg = get_config(args.dataset)
    direction = args.direction or cfg.translate_direction
    split_json, split_gold = get_split_files(args.split)
    base, ext = os.path.splitext(split_json)
    output_json = os.path.join(args.output_dir, f"{base}_sqlglot{ext}")
    output_gold = os.path.join(
        args.output_dir, split_gold.replace("_gold.sql", "_sqlglot_gold.sql")
    )

    src_db_dir = os.path.join(args.source_dir, STD_DB_DIR)
    tgt_db_dir = os.path.join(args.target_dir, STD_DB_DIR)
    tables_src = load_json(os.path.join(args.source_dir, STD_TABLES_FILE))
    tables_tgt = load_json(os.path.join(args.target_dir, STD_TABLES_FILE))
    replacements = load_json(args.replacements)
    split_data = load_json(os.path.join(args.source_dir, split_json))

    if direction == "en2cn":
        src_encoding, tgt_encoding = cfg.db_encoding, "utf-8"
    else:
        src_encoding, tgt_encoding = "utf-8", cfg.db_encoding

    os.makedirs(args.output_dir, exist_ok=True)
    out_entries, gold_lines = [], []
    stats = {"success": 0, "fail": 0, "warning": 0}

    for entry in tqdm(split_data):
        db_id = entry.get("db_id") or entry.get("db_name", "")
        src_sql = (
            entry.get(cfg.sql_field) or entry.get("SQL")
            or entry.get("query") or entry.get("sql_query")
        )
        if not src_sql:
            stats["fail"] += 1
            continue
        maps = build_precise_maps(db_id, tables_src, tables_tgt)
        if not maps:
            stats["fail"] += 1
            continue

        tgt_sql = translate_sql_sqlglot(src_sql, maps, replacements.get(db_id, {}))

        src_res = execute_query(
            os.path.join(src_db_dir, db_id, f"{db_id}.sqlite"),
            src_sql, encoding=src_encoding, timeout=args.execute_timeout,
        )
        tgt_res = execute_query(
            os.path.join(tgt_db_dir, db_id, f"{db_id}.sqlite"),
            tgt_sql, encoding=tgt_encoding, timeout=args.execute_timeout,
        )
        if (src_res != "Error: timeout" and tgt_res != "Error: timeout"
                and src_res is not None and src_res == tgt_res):
            stats["success"] += 1
        elif is_structure_match(src_res, tgt_res):
            stats["warning"] += 1
        else:
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
    print(f"\nDone ({arrow}). Success: {stats['success']}, "
          f"Fail: {stats['fail']}, Warning: {stats['warning']}")


if __name__ == "__main__":
    main()
