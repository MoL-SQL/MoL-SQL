#!/usr/bin/env python3
"""
Annotate each sample in ``<input>/<split>.json`` with a ``difficulty`` field
(in-place) based on the SQL structure.

Classification rules (from the Spider hardness heuristic, simplified):

    easy       no join,           no sub-select
    medium     one join,          no sub-select
    hard       two or more joins, no sub-select
    extra      has sub-select query

Examples
--------
easy:
    SELECT COUNT(*) FROM cars_data WHERE cylinders > 4

medium (one join):
    SELECT T2.name, COUNT(*)
    FROM concert AS T1 JOIN stadium AS T2
      ON T1.stadium_id = T2.stadium_id
    GROUP BY T1.stadium_id

hard (two or more joins):
    SELECT T1.country_name
    FROM countries AS T1 JOIN continents AS T2 ON T1.continent = T2.cont_id
    JOIN car_makers AS T3 ON T1.country_id = T3.country
    WHERE T2.continent = 'Europe'
    GROUP BY T1.country_name
    HAVING COUNT(*) >= 3

extra (sub-select):
    SELECT AVG(life_expectancy)
    FROM country
    WHERE name NOT IN (
        SELECT T1.name
        FROM country AS T1 JOIN country_language AS T2
          ON T1.code = T2.country_code
        WHERE T2.language = "English" AND T2.is_official = "T"
    )

Usage
-----
    python -u script/data_preprocess/add_sql_level.py \\
        --input dataset/BULL-FinSQL/BULL-cnq-ends-cndv \\
        --split dev
"""

import argparse
import json
import os
import re
from collections import Counter

DIFFICULTY_LEVELS = ("easy", "medium", "hard", "extra")

# Match a single-quoted or double-quoted string literal. SQL single-quotes
# escape via '', so we allow that inside the group.
_STRING_LITERAL_RE = re.compile(r"'(?:''|[^'])*'|\"(?:\"\"|[^\"])*\"")
# /* ... */ block comments and -- line comments.
_BLOCK_COMMENT_RE = re.compile(r"/\*.*?\*/", re.DOTALL)
_LINE_COMMENT_RE = re.compile(r"--[^\n]*")

_JOIN_RE = re.compile(r"\bjoin\b", re.IGNORECASE)
_SELECT_RE = re.compile(r"\bselect\b", re.IGNORECASE)


def _strip_literals_and_comments(sql: str) -> str:
    """Remove string literals and SQL comments so keyword counting isn't
    fooled by e.g. values like ``'select ...'`` inside a WHERE clause."""
    sql = _BLOCK_COMMENT_RE.sub(" ", sql)
    sql = _LINE_COMMENT_RE.sub(" ", sql)
    sql = _STRING_LITERAL_RE.sub("''", sql)
    return sql


def classify_sql(sql: str) -> str:
    """Return the difficulty label for a single SQL string."""
    if not sql or not sql.strip():
        return "easy"
    cleaned = _strip_literals_and_comments(sql)
    n_select = len(_SELECT_RE.findall(cleaned))
    n_join = len(_JOIN_RE.findall(cleaned))

    # More than one SELECT ⇒ contains a sub-select.
    if n_select >= 2:
        return "extra"
    if n_join == 0:
        return "easy"
    if n_join == 1:
        return "medium"
    return "hard"


def _pick_sql(entry: dict) -> str:
    """Return the SQL text for an entry, tolerating different field names."""
    for key in ("sql_query", "query", "SQL", "sql"):
        val = entry.get(key)
        if isinstance(val, str) and val.strip():
            return val
    return ""


def add_difficulty_inplace(json_path: str) -> Counter:
    """Annotate every sample in ``json_path`` with ``difficulty`` (in place).

    Returns a Counter of difficulty labels for logging.
    """
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError(f"Expected a JSON array in {json_path}, got {type(data).__name__}")

    counts: Counter = Counter()
    for entry in data:
        sql = _pick_sql(entry)
        label = classify_sql(sql)
        entry["difficulty"] = label
        counts[label] += 1

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return counts


def _format_counts(counts: Counter) -> str:
    total = sum(counts.values()) or 1
    parts = []
    for level in DIFFICULTY_LEVELS:
        n = counts.get(level, 0)
        parts.append(f"{level}={n} ({n / total:.1%})")
    return ", ".join(parts) + f", total={sum(counts.values())}"


def main():
    parser = argparse.ArgumentParser(
        description="Add a 'difficulty' field to each sample in <input>/<split>.json."
    )
    parser.add_argument("--input", required=True,
                        help="Dataset directory containing <split>.json")
    parser.add_argument("--split", default="dev",
                        choices=["dev", "train", "test"],
                        help="Which split to annotate (default: dev)")
    args = parser.parse_args()

    json_path = os.path.join(args.input, f"{args.split}.json")
    if not os.path.exists(json_path):
        raise FileNotFoundError(json_path)

    counts = add_difficulty_inplace(json_path)
    print(f"[add_sql_level] Annotated {json_path}")
    print(f"[add_sql_level] {_format_counts(counts)}")


if __name__ == "__main__":
    main()
