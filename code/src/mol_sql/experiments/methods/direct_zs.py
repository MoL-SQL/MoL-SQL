"""Frozen Direct-ZS prompt protocol used by the paper baseline."""

from __future__ import annotations

import hashlib
import re
import sqlite3
from contextlib import closing
from pathlib import Path


PROMPT_TEMPLATE_VERSION = "direct-zs-sqlite-full-schema-first3-v1"


def _decode_text(value: bytes) -> str:
    try:
        return value.decode("utf-8")
    except UnicodeDecodeError:
        return value.decode("latin-1", errors="replace")


def serialize_database(database_path: Path, sample_rows_per_table: int = 3) -> str:
    """Serialize every user table as CREATE statements and deterministic samples."""
    with closing(sqlite3.connect(database_path)) as connection:
        connection.text_factory = _decode_text
        schema_rows = connection.execute(
            "SELECT name, sql FROM sqlite_master "
            "WHERE type='table' AND sql IS NOT NULL ORDER BY name"
        ).fetchall()
        schema_rows = [
            row for row in schema_rows if not str(row[0] or "").startswith("sqlite_")
        ]
        sections = [str(sql) for _, sql in schema_rows if sql]
        foreign_keys = []
        for table_name, _ in schema_rows:
            escaped = str(table_name).replace('"', '""')
            for foreign_key in connection.execute(
                f'PRAGMA foreign_key_list("{escaped}")'
            ).fetchall():
                foreign_keys.append(
                    f"  {table_name}.{foreign_key[3]} REFERENCES "
                    f"{foreign_key[2]}({foreign_key[4]})"
                )
        if foreign_keys:
            sections.append("-- Foreign key constraints:\n" + "\n".join(foreign_keys))

        if sample_rows_per_table <= 0:
            return "\n\n".join(sections)

        samples = []
        for table_name, _ in schema_rows:
            escaped = str(table_name).replace('"', '""')
            try:
                cursor = connection.execute(
                    f'SELECT * FROM "{escaped}" LIMIT ?', (sample_rows_per_table,)
                )
                rows = cursor.fetchall()
            except sqlite3.Error:
                continue
            samples.append(f"Table `{table_name}` (first {sample_rows_per_table} rows):")
            samples.append(
                "Columns: " + ", ".join(f"`{item[0]}`" for item in cursor.description)
            )
            for row in rows:
                samples.append(
                    "  " + " | ".join("NULL" if value is None else str(value) for value in row)
                )
            samples.append("")
        sample_text = "\n".join(samples).strip()
        if sample_text:
            sections.append(
                f"## Sample data (first {sample_rows_per_table} rows per table)\n\n"
                f"{sample_text}"
            )
        return "\n\n".join(sections)


def build_prompt(question: str, database_path: Path, sample_rows_per_table: int = 3) -> str:
    schema = serialize_database(database_path, sample_rows_per_table)
    parts = [
        "Generate a SQLite SQL query for the following question.",
        "",
        "Rules:",
        "- Use backticks around table and column names that are Chinese or contain "
        "non-ASCII characters, e.g. `名称`, `歌手`, `年龄`.",
        "- Example: SELECT `姓名`, `年龄` FROM `歌手` WHERE `国籍` = 'France' "
        "ORDER BY `年龄` DESC",
        "- For SQLite: use IIF(a,b,c) instead of IF; SUBSTR(str,start,len) for substring.",
        "",
        "## Database schema and sample data",
        schema.strip(),
        "",
        "## Question",
        question.strip(),
        "",
        "## SQL (single line, no markdown; quote Chinese/non-ASCII identifiers with backticks)",
        "",
    ]
    return "\n".join(parts)


def prompt_sha256(prompt: str) -> str:
    return hashlib.sha256(prompt.encode("utf-8")).hexdigest()


def extract_sql(response: str) -> str | None:
    text = (response or "").strip()
    if not text:
        return None
    xml = re.search(r"<sql>(.*?)</sql>", text, re.IGNORECASE | re.DOTALL)
    if xml:
        text = xml.group(1).strip()
    if text.startswith("```"):
        text = re.sub(r"^```\w*\n?", "", text)
        text = re.sub(r"\n?```\s*$", "", text).strip()
    label = re.search(r"(?im)^\s*SQL\s*:\s*(.*)$", text)
    if label:
        same_line = label.group(1).strip()
        if same_line:
            text = same_line
        else:
            tail = text[label.end() :].lstrip("\n").strip()
            text = next((line.strip() for line in tail.splitlines() if line.strip()), "")
    text = re.sub(r"\s+", " ", text).strip()
    return text or None
