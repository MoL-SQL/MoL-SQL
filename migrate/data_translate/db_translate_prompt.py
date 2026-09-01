#!/usr/bin/env python3
"""
Generate prompts for translating SQL databases (EN↔CN).

Uses PK/FK grouping (UnionFind) to ensure consistent value translation
across related columns.  Works with Spider, BIRD, and BULL datasets.
Supports both EN-to-CN and CN-to-EN via ``--direction``.
"""

import argparse
import json
import os
import re
import sqlite3

from tqdm import tqdm

import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import STD_DB_DIR, STD_TABLES_FILE
from data_translate.prompts import (
    CONTENT_PROMPT_CN2EN,
    CONTENT_PROMPT_EN2CN,
    SCHEMA_CN2EN_EXAMPLE_INPUT,
    SCHEMA_CN2EN_EXAMPLE_OUTPUT,
    SCHEMA_EN2CN_EXAMPLE_INPUT,
    SCHEMA_EN2CN_EXAMPLE_OUTPUT,
    SCHEMA_PROMPT_CN2EN,
    SCHEMA_PROMPT_EN2CN,
)


# ---------------------------------------------------------------------------
# UnionFind for PK/FK column grouping
# ---------------------------------------------------------------------------

class UnionFind:
    """Disjoint-set to group associated PK/FK columns."""

    def __init__(self):
        self.parent = {}

    def find(self, i):
        if self.parent.setdefault(i, i) == i:
            return i
        self.parent[i] = self.find(self.parent[i])
        return self.parent[i]

    def union(self, i, j):
        ri, rj = self.find(i), self.find(j)
        if ri != rj:
            self.parent[ri] = rj

    def groups(self):
        res = {}
        for k in self.parent:
            root = self.find(k)
            res.setdefault(root, []).append(k)
        return list(res.values())


# ---------------------------------------------------------------------------
# Column / value helpers
# ---------------------------------------------------------------------------

SKIP_COLUMN_KEYWORDS = [
    "name", "code", "date", "time", "_id", "password", "email",
    "composer", "country", "county", "city", "state", "district", "province",
    "address",
    "keywords", "website", "url",
]

# skip column names with suffix
SKIP_COLUMN_SUFFIX = [
    "Addr", "Manager", "Company", "Abbr", "LegalRepr", "LinkMan", "TrusteeFunctionary", "LegalPersonRepr", "RegArea", "SecretaryBD", "SponsorRepresentative", "Firm", "SignatureAccountant", "SignatureLaw", "EvalAgent", "SignatureEvaluator", "LegalPersonRepr",
    "ChiName", "ControllerName", "InvestorName", "AbbrName", "LeaderName", "SponsorName", "SHName", "CompanyName", "FPSHName", "ReceiverName", "TransfererName", 
    "Authorizer", "AuthorizedReceiver",
    "InvestAdvisorName", "TrusteeName", "InvestAdvisorAbbrName"
]

def get_text_columns(column_names, column_types):
    """Return ``[(table_index, column_name)]`` for text-type columns worth translating."""
    text_columns = []
    skip_columns = []
    for col_info, col_type in zip(column_names, column_types):
        table_idx, col_name = col_info
        # if any(kw in col_name.lower() for kw in SKIP_COLUMN_KEYWORDS): # old version
        if any(kw == col_name.lower() for kw in SKIP_COLUMN_KEYWORDS):
            skip_columns.append((table_idx, col_name))
            continue
        if any(col_name.endswith(suffix) for suffix in SKIP_COLUMN_SUFFIX):
            skip_columns.append((table_idx, col_name))
            continue
        if col_type.startswith("text"):
            text_columns.append((table_idx, col_name))
    print(f"Skipped {len(skip_columns)} columns with certain keywords or suffixes: {skip_columns}")
    return text_columns


def get_foreign_key_groups(conn, table_names, text_columns):
    """Group columns by explicit FK + implicit same-name heuristic."""
    uf = UnionFind()
    valid = set()

    for t_idx, c_name in text_columns:
        if t_idx == -1:
            continue
        t_name = table_names[t_idx]
        uf.find((t_name, c_name))
        valid.add((t_name, c_name))

    for table in table_names:
        try:
            cur = conn.cursor()
            cur.execute(f'PRAGMA foreign_key_list("{table}")')
            for row in cur.fetchall():
                parent, from_col, to_col = row[2], row[3], row[4]
                if (table, from_col) in valid and (parent, to_col) in valid:
                    uf.union((table, from_col), (parent, to_col))
        except Exception:
            pass

    cols_map = {}
    for t_name, c_name in valid:
        cols_map.setdefault(c_name, []).append(t_name)
    for c_name, t_names in cols_map.items():
        for i in range(len(t_names) - 1):
            uf.union((t_names[i], c_name), (t_names[i + 1], c_name))

    return uf.groups()


def _fetch_raw_string_values(conn, group):
    """Fetch all distinct non-empty string values for a column group."""
    values = set()
    cur = conn.cursor()
    for table_name, column_name in group:
        try:
            cur.execute(
                f'SELECT DISTINCT "{column_name}" FROM "{table_name}" '
                f'WHERE "{column_name}" IS NOT NULL AND "{column_name}" != ""'
            )
            for row in cur.fetchall():
                if isinstance(row[0], str):
                    values.add(row[0])
        except Exception:
            pass
    return values


def merge_groups_by_shared_values(conn, groups, min_overlap_ratio=0.3):
    """Merge column groups whose value sets overlap significantly.

    Two groups are merged only when their shared values make up at least
    *min_overlap_ratio* of the smaller group AND there are at least 2
    shared values.  This prevents unrelated columns from being chained
    together through a single coincidental value.
    """
    if not groups:
        return groups

    group_values = [_fetch_raw_string_values(conn, g) for g in groups]

    uf = UnionFind()
    for i in range(len(groups)):
        uf.find(i)

    for i in range(len(groups)):
        if not group_values[i]:
            continue
        for j in range(i + 1, len(groups)):
            if not group_values[j]:
                continue
            overlap = len(group_values[i] & group_values[j])
            smaller = min(len(group_values[i]), len(group_values[j]))
            if smaller > 0 and overlap / smaller >= min_overlap_ratio:
                uf.union(i, j)

    merged = {}
    for i in range(len(groups)):
        root = uf.find(i)
        merged.setdefault(root, []).extend(groups[i])

    result = list(merged.values())
    if len(result) < len(groups):
        print(f"        Value-overlap merge: {len(groups)} groups → {len(result)} groups")
    return result


def _has_non_ascii(text):
    return any(ord(c) > 127 for c in text)


def get_unique_values_for_group(conn, group, direction="en2cn"):
    """Collect unique translatable string values across all columns in *group*.

    For EN→CN we keep English (ASCII) values and skip already-Chinese ones.
    For CN→EN we keep Chinese (non-ASCII) values and skip all-ASCII ones.
    """
    all_values = set()
    cur = conn.cursor()
    for table_name, column_name in group:
        try:
            cur.execute(
                f'SELECT DISTINCT "{column_name}" FROM "{table_name}" '
                f'WHERE "{column_name}" IS NOT NULL AND "{column_name}" != ""'
            )
            all_values.update(row[0] for row in cur.fetchall())
        except Exception:
            pass

    values = list(all_values)
    group_desc = ", ".join(f"{t}.{c}" for t, c in group)

    if not all(isinstance(v, str) for v in values):
        print(f"        Skip content [{group_desc}]: non-string values")
        return None
    if not values or all(v is None or v == "" or len(v) <= 1 for v in values):
        print(f"        Skip content [{group_desc}]: empty/single-char values")
        return None
    if not any(c.isalpha() for c in "".join(values).replace(" ", "")):
        print(f"        Skip content [{group_desc}]: no alphabetic values")
        return None

    # URLs and emails — skip regardless of direction
    if all(v.startswith("http://") or v.startswith("https://") or v.startswith("www.") for v in values):
        print(f"        Skip content [{group_desc}]: URLs")
        return None
    if all("@" in v and "." in v for v in values):
        print(f"        Skip content [{group_desc}]: emails")
        return None
    if len(values) > 1000:
        print(f"        Skip content [{group_desc}]: too many values ({len(values)})")
        return None
    if any("{" in v or "}" in v for v in values):
        print(f"        Skip content [{group_desc}]: JSON-like values")
        return None

    if direction == "en2cn":
        # EN→CN: skip values that are already non-ASCII (nothing to translate)
        if any(_has_non_ascii(v) for v in values):
            print(f"        Skip content [{group_desc}]: already non-ASCII")
            return None
        # Skip short all-uppercase codes and non-alpha-only strings
        charset = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz/,-")
        if all(" " not in v for v in values):
            if any(any(c not in charset for c in v) for v in values):
                # return None
                if all(len(v) <= 3 and v.isupper() for v in values):
                    print(f"        Skip content [{group_desc}]: short uppercase codes")
                    return None
    else:
        # CN→EN: skip values that are all ASCII (nothing to translate)
        if all(v.isascii() for v in values):
            print(f"        Skip content [{group_desc}]: all ASCII")
            return None
        # CN→EN: drop individual percentage/numeric values like "0.35%", "1%-2%"
        _pct_re = re.compile(r'^[\d.,\-~%/\s]+%$')
        before = len(values)
        values = [v for v in values if not _pct_re.match(v)]
        if before != len(values):
            print(f"        Filter content [{group_desc}]: dropped {before - len(values)} percentage values")
        if not values:
            print(f"        Skip content [{group_desc}]: all percentage values")
            return None
        # CN→EN: drop group that has values that are too long (> 100 characters)
        if any(len(v) > 100 for v in values):
            print(f"        Skip content [{group_desc}]: values are too long")
            return None

    return values


def infer_column_types(conn, table_names_original, column_names_original):
    """Infer column types from DB when ``column_types`` is missing."""
    cur = conn.cursor()
    types = []
    for col_entry in column_names_original:
        if col_entry[0] == -1:
            types.append("text")
            continue
        table_name = table_names_original[col_entry[0]]
        col_name = col_entry[1]
        try:
            cur.execute(f'SELECT typeof("{col_name}") FROM "{table_name}" LIMIT 1')
            row = cur.fetchone()
            if row and row[0]:
                t = row[0].lower()
                types.append("integer" if t == "integer" else "real" if t == "real" else "text")
            else:
                types.append("text")
        except Exception:
            types.append("text")
    return types


# ---------------------------------------------------------------------------
# Prompt generators
# ---------------------------------------------------------------------------

def generate_schema_prompt(db_id, table_names, column_names, direction="en2cn"):
    current_input = {"table_names": table_names, "column_names": column_names}
    if direction == "cn2en":
        return SCHEMA_PROMPT_CN2EN.format(
            example_input=SCHEMA_CN2EN_EXAMPLE_INPUT,
            example_output=SCHEMA_CN2EN_EXAMPLE_OUTPUT,
            current_input=current_input,
        )
    return SCHEMA_PROMPT_EN2CN.format(
        example_input=SCHEMA_EN2CN_EXAMPLE_INPUT,
        example_output=SCHEMA_EN2CN_EXAMPLE_OUTPUT,
        current_input=current_input,
    )


def generate_content_prompt(db_id, tables_columns, values, direction="en2cn"):
    if not values:
        return None
    values_str = "\n".join(f"- {v}" for v in values)
    context_str = "\n".join(f"  - Table: {t}, Column: {c}" for t, c in tables_columns)
    template = CONTENT_PROMPT_CN2EN if direction == "cn2en" else CONTENT_PROMPT_EN2CN
    return template.format(
        db_id=db_id, context_str=context_str, values=values_str,
    )


# ---------------------------------------------------------------------------
# Main per-DB driver
# ---------------------------------------------------------------------------

def generate_prompts_for_db(
    db_info,
    db_base_path,
    prompts_dir,
    direction="en2cn",
    skip_content_if_unique_above=None,
    content_chunk_size=50,
    values_only=False,
    merge_overlap_ratio=0.3,
):
    db_id = db_info["db_id"]
    table_names_original = db_info["table_names_original"]
    column_names_original = db_info["column_names_original"]
    column_types = db_info.get("column_types")
    prompts = []

    db_path = os.path.join(db_base_path, db_id, f"{db_id}.sqlite")
    print(f"    Database path: {db_path}")
    conn = sqlite3.connect(db_path)

    if column_types is None or len(column_types) != len(column_names_original):
        column_types = infer_column_types(conn, table_names_original, column_names_original)

    # Print per-table column type summary
    table_type_counts = {}
    for col_info, col_type in zip(column_names_original, column_types):
        tidx = col_info[0]
        if tidx == -1:
            continue
        tname = table_names_original[tidx]
        table_type_counts.setdefault(tname, {})
        table_type_counts[tname][col_type] = table_type_counts[tname].get(col_type, 0) + 1
    for tname, counts in table_type_counts.items():
        summary = ", ".join(f"{t}: {n}" for t, n in sorted(counts.items()))
        print(f"      {tname}: {summary}")

    if not values_only:
        schema_prompt = generate_schema_prompt(
            db_id, table_names_original, column_names_original, direction=direction,
        )
        prompts.append({
            "db_id": db_id, "type": "schema",
            "table_names": table_names_original,
            "column_names": column_names_original,
            "prompt": schema_prompt,
        })

    # Content prompts (grouped by PK/FK, then merged by shared values)
    text_columns = get_text_columns(column_names_original, column_types)
    groups = get_foreign_key_groups(conn, table_names_original, text_columns)
    groups = merge_groups_by_shared_values(conn, groups, min_overlap_ratio=merge_overlap_ratio)

    for group in groups:
        unique_values = get_unique_values_for_group(conn, group, direction=direction)
        n = len(unique_values) if unique_values else 0
        if n == 0:
            continue
        if skip_content_if_unique_above is not None and n > skip_content_if_unique_above:
            print(f"        Skip content: group has {n} values (> {skip_content_if_unique_above})")
            continue

        if n <= content_chunk_size:
            cp = generate_content_prompt(db_id, group, unique_values, direction=direction)
            if cp:
                prompts.append({
                    "db_id": db_id, "type": "content",
                    "tables_columns": group, "values": unique_values,
                    "prompt": cp,
                })
        else:
            for i in range(0, n, content_chunk_size):
                chunk = unique_values[i : i + content_chunk_size]
                cp = generate_content_prompt(db_id, group, chunk, direction=direction)
                if cp:
                    prompts.append({
                        "db_id": db_id, "type": "content",
                        "tables_columns": group, "values": chunk,
                        "prompt": cp,
                    })

    conn.close()

    output_file = os.path.join(prompts_dir, f"{db_id}.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(prompts, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(prompts)} prompts to {output_file}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate prompts for DB translation (EN↔CN).")
    parser.add_argument("--dataset-dir", required=True,
                        help="Preprocessed dataset directory (contains database/ and tables.json)")
    parser.add_argument("--direction", default="en2cn", choices=["en2cn", "cn2en"],
                        help="Translation direction (default: en2cn)")
    parser.add_argument("--prompts-dir", default=None,
                        help="Output directory for prompt JSON files (default: ../../intermediate_data/prompts)")
    parser.add_argument("--skip-content-if-unique-above", type=int, default=1000, metavar="N",
                        help="Skip content translation when unique values > N (default: 1000)")
    parser.add_argument("--content-chunk-size", type=int, default=100, metavar="K",
                        help="Max values per content prompt (default: 100)")
    parser.add_argument("--merge-overlap-ratio", type=float, default=0.3, metavar="R",
                        help="Min overlap ratio to merge column groups by shared values (default: 0.3)")
    args = parser.parse_args()

    if args.content_chunk_size < 1:
        parser.error("--content-chunk-size must be >= 1")

    db_base = os.path.join(args.dataset_dir, STD_DB_DIR)
    db_info_path = os.path.join(args.dataset_dir, STD_TABLES_FILE)
    prompts_dir = args.prompts_dir or os.path.join(
        os.path.dirname(__file__), "..", "..", "intermediate_data", "prompts",
    )
    os.makedirs(prompts_dir, exist_ok=True)

    with open(db_info_path, "r", encoding="utf-8") as f:
        db_info_list = json.load(f)

    arrow = "EN→CN" if args.direction == "en2cn" else "CN→EN"
    print(f"Loaded {len(db_info_list)} databases from {db_info_path} (direction: {arrow})")
    for db_info in tqdm(db_info_list, desc="Generating prompts"):
        print(f"Generating prompts for database: {db_info['db_id']}...")
        generate_prompts_for_db(
            db_info, db_base, prompts_dir,
            direction=args.direction,
            skip_content_if_unique_above=args.skip_content_if_unique_above,
            content_chunk_size=args.content_chunk_size,
            merge_overlap_ratio=args.merge_overlap_ratio,
        )
