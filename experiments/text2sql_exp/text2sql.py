"""
Text2SQL pipeline: SQL-style schema + sample rows per table, then prompt assembly.

Unified from Spider, BIRD, and BULL variants. Supports:
- Configurable DB subdirectory layout
- Random vs first-N sample rows
- Optional evidence and Chinese prompt mode
"""

import json
import os
import sqlite3
from typing import Any, Dict, Iterable, List, Optional, Tuple

import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from text2sql_exp.prompts import build_text2sql_prompt


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_tables(tables_path: str) -> Dict[str, dict]:
    """Load tables JSON into ``{db_id: schema_dict}``."""
    with open(tables_path, "r", encoding="utf-8") as f:
        raw = json.load(f)
    return {item["db_id"]: item for item in raw}


def get_schema(schemas: Dict[str, dict], db_id: str) -> Optional[dict]:
    return schemas.get(db_id)


def get_db_path(
    dataset_dir: str,
    db_id: str,
    db_subdir: str = "database",
) -> str:
    """Return path to ``{db_id}.sqlite``."""
    return os.path.join(dataset_dir, db_subdir, db_id, f"{db_id}.sqlite")


# ---------------------------------------------------------------------------
# SQL-style schema and sample rows
# ---------------------------------------------------------------------------

def _normalize_table_filter(table_names: Optional[Iterable[str]]) -> Optional[set]:
    if table_names is None:
        return None
    return {str(name).lower() for name in table_names if str(name)}


def _table_allowed(table_name: str, table_filter: Optional[set]) -> bool:
    return table_filter is None or table_name.lower() in table_filter


def get_sql_style_schema(
    db_path: str,
    include_foreign_keys: bool = True,
    table_names: Optional[Iterable[str]] = None,
) -> str:
    """Extract CREATE TABLE statements from sqlite_master."""
    if not os.path.exists(db_path):
        return ""
    table_filter = _normalize_table_filter(table_names)
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute(
            "SELECT name, sql FROM sqlite_master "
            "WHERE type='table' AND sql IS NOT NULL ORDER BY name"
        )
        rows = [
            r for r in cur.fetchall()
            if r[1] and not (r[0] or "").startswith("sqlite_")
            and _table_allowed(r[0], table_filter)
        ]
        parts = [r[1] for r in rows]
        table_names = [r[0] for r in rows]

        if include_foreign_keys and table_names:
            fk_lines = []
            for tbl in table_names:
                try:
                    cur.execute(f'PRAGMA foreign_key_list("{tbl}")')
                    for fk in cur.fetchall():
                        if not _table_allowed(fk[2], table_filter):
                            continue
                        fk_lines.append(
                            f"  {tbl}.{fk[3]} REFERENCES {fk[2]}({fk[4]})"
                        )
                except Exception:
                    continue
            if fk_lines:
                parts.append("-- Foreign key constraints:\n" + "\n".join(fk_lines))

        conn.close()
        return "\n\n".join(parts) if parts else ""
    except Exception:
        return ""


def get_sample_rows(
    db_path: str,
    max_rows_per_table: int = 10,
    encoding: str = "utf-8",
    random_rows: bool = False,
    table_names: Optional[Iterable[str]] = None,
) -> str:
    """Get sample rows for each table (first-N or random-N)."""
    if not os.path.exists(db_path):
        return ""
    table_filter = _normalize_table_filter(table_names)
    def _utf8_first(b: bytes):
        # Prefer UTF-8 so Chinese table/column names and cells decode correctly.
        # Fall back to ``encoding`` (e.g. latin-1 for BIRD mini-dev) only when
        # UTF-8 fails, so mixed-encoding DBs don't silently drop whole tables.
        try:
            return b.decode("utf-8")
        except UnicodeDecodeError:
            return b.decode(encoding, errors="replace")

    try:
        conn = sqlite3.connect(db_path)
        conn.text_factory = _utf8_first
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        table_names = [
            r[0] for r in cur.fetchall()
            if not (r[0] or "").startswith("sqlite_")
            and _table_allowed(r[0], table_filter)
        ]
        lines = []
        mode = "random" if random_rows else "first"
        for tbl in table_names:
            try:
                order = "ORDER BY RANDOM()" if random_rows else ""
                cur.execute(f'SELECT * FROM "{tbl}" {order} LIMIT {max_rows_per_table}')
                rows = cur.fetchall()
                col_names = [d[0] for d in cur.description]
                lines.append(f"Table `{tbl}` ({mode} {max_rows_per_table} rows):")
                lines.append("Columns: " + ", ".join(f"`{c}`" for c in col_names))
                for row in rows:
                    cells = [str(c) if c is not None else "NULL" for c in row]
                    lines.append("  " + " | ".join(cells))
                lines.append("")
            except Exception:
                continue
        conn.close()
        return "\n".join(lines).strip()
    except Exception:
        return ""


# ---------------------------------------------------------------------------
# Prompt builder (no LLM call)
# ---------------------------------------------------------------------------

def build_prompt_only(
    question: str,
    db_path: str,
    db_id: str = "",
    sample_rows_per_table: int = 10,
    db_encoding: str = "utf-8",
    use_cot: bool = False,
    few_shot_examples: Optional[List[Tuple[str, str]]] = None,
    random_sample_rows: bool = False,
    evidence: Optional[str] = None,
    chinese_prompt: bool = False,
    prompt_mode: str = "none",
    table_names: Optional[Iterable[str]] = None,
    output_style: str = "label",
    retrieved_values_text: Optional[str] = None,
) -> str:
    """Build the Text2SQL prompt string from schema + sample rows."""
    sql_schema = get_sql_style_schema(db_path, table_names=table_names)
    samples = get_sample_rows(
        db_path,
        max_rows_per_table=sample_rows_per_table,
        encoding=db_encoding,
        random_rows=random_sample_rows,
        table_names=table_names,
    )
    mode = "random" if random_sample_rows else "first"
    schema_desc = sql_schema
    if samples:
        schema_desc += f"\n\n## Sample data ({mode} {sample_rows_per_table} rows per table)\n\n{samples}"

    return build_text2sql_prompt(
        question=question,
        schema_desc=schema_desc,
        db_id=db_id,
        use_cot=use_cot,
        few_shot_examples=few_shot_examples,
        evidence=evidence,
        chinese_prompt=chinese_prompt,
        prompt_mode=prompt_mode,
        output_style=output_style,
        retrieved_values_text=retrieved_values_text,
    )
