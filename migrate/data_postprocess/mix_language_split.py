#!/usr/bin/env python3
"""Mix language variants of BULL-FinSQL into a single mixed-question/mixed-db dataset.

For K English-question subdatasets (`enq_list`) and K matching Chinese-question
subdatasets (`cnq_list`), build a new dataset directory with ``2*K*3`` renamed
databases (2*K variants x 3 base dbs by default), a merged `tables.json`, a
balanced `dev.json`, and a bird-style `dev_gold.sql`. Each side must list the
same number of dirs; ``--num-per-db`` must be divisible by K.

Example::

    python code/script/data_postprocess/mix_language.py \\
        --enq-list code/dataset/BULL-FinSQL/BULL-en-origin \\
                   code/dataset/BULL-FinSQL/BULL-enq-cnds-cndv \\
                   code/dataset/BULL-FinSQL/BULL-enq-ends-endv \\
        --cnq-list code/dataset/BULL-FinSQL/BULL-cn-origin \\
                   code/dataset/BULL-FinSQL/BULL-cnq-ends-endv \\
                   code/dataset/BULL-FinSQL/BULL-cnq-cnds-cndv \\
        --output-dir code/dataset/BULL-FinSQL/BULL-mixq-mixdb \\
        --seed 42

Layout produced:

(1) `database/` and `tables.json`
    - 12 databases: <variant_short>-<base_db>
      (e.g. ``en-origin-ccks_fund``, ``enq-cnds-cndv-ccks_macro``).
    - Each new db is a hard copy of the original variant's per-db folder.
      Source paths are resolved with ``os.path.realpath`` so that variants
      whose ``database/`` is itself a symlink (e.g. BULL-en-origin/database
      points outside the repo) get materialized from the real on-disk files.
    - `tables.json` contains 12 entries (the matching schema from each
      variant's `tables.json`, with `db_id` rewritten).

(2) `dev.json` (filter + balance)
    - Filter `enq_list[0]` (the en base dataset) like ``check_empty_sql.py``:
      keep rows whose gold SQL runs on that variant's sqlite **and** returns
      at least one row (exclude ``empty``, ``error``, and missing SQL); those
      ``q_id``s define the candidate pool.
    - For every base db, randomly sample ``num_per_db`` q_ids (default 50) and
      split into K equal groups (K = ``len(enq_list)``, same as ``len(cnq_list)``).
      Group i uses ``enq_list[i]`` and ``cnq_list[i]``. With K=2 and default
      settings this is 25/25 per group; total dev rows =
      ``num_per_db * 2 * len(base_dbs)`` (two language sides per group).
    - Each row carries: ``q_id`` (``"<orig>_<variant_short>_<index>"``),
      ``db_name`` (new id), ``sql_query``, ``question`` and
      ``question_language`` (``"en"`` / ``"cn"``).

(3) `dev_gold.sql`
    - bird style: ``<sql>\\t<db_id>\\n`` per row in the merged `dev.json`.
"""

from __future__ import annotations

import argparse
import copy
import json
import os
import random
import re
import shutil
import sys
from typing import Dict, List, Tuple

_PREP_DIR = os.path.normpath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data_preprocess")
)
if _PREP_DIR not in sys.path:
    sys.path.insert(0, _PREP_DIR)

from check_empty_sql import EMPTY, NON_EMPTY, _execute  # noqa: E402


def _load_json(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _write_json(path: str, data) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _reset_dir(path: str) -> None:
    if os.path.exists(path) or os.path.islink(path):
        if os.path.isdir(path) and not os.path.islink(path):
            shutil.rmtree(path)
        else:
            os.remove(path)
    os.makedirs(path, exist_ok=True)


def _variant_short(variant_dir: str) -> str:
    name = os.path.basename(os.path.normpath(variant_dir))
    return name[len("BULL-"):] if name.startswith("BULL-") else name


def _language_of(variant_short: str) -> str:
    # variant short names start with "en..." (en-origin, enq-cnds-cndv)
    # or "cn..." (cn-origin, cnq-ends-endv).
    return "en" if variant_short.startswith("en") else "cn"


def _sqlite_path(variant_dir: str, base_db: str) -> str:
    return os.path.join(variant_dir, "database", base_db, f"{base_db}.sqlite")


def _index_rows(rows: List[dict]) -> Dict[int, dict]:
    return {row["q_id"]: row for row in rows}


def _validate_pool(
    base_variant_dir: str,
    base_dbs: List[str],
    *,
    validate_timeout: float,
) -> Dict[str, List[int]]:
    """Filter the base dataset's dev.json using ``check_empty_sql``'s ``non_empty`` rule.

    Returns a mapping ``base_db -> [valid q_ids]`` (sorted ascending).
    """
    dev_rows = _load_json(os.path.join(base_variant_dir, "dev.json"))
    valid: Dict[str, List[int]] = {db: [] for db in base_dbs}
    skipped_unknown_db = 0
    skipped_no_sql = 0
    skipped_empty = 0
    skipped_error = 0
    db_path_cache = {db: _sqlite_path(base_variant_dir, db) for db in base_dbs}

    for row in dev_rows:
        db = row.get("db_name")
        if db not in valid:
            skipped_unknown_db += 1
            continue
        sql = (row.get("sql_query") or row.get("query") or "").strip()
        if not sql:
            skipped_no_sql += 1
            continue
        bucket, _ = _execute(
            sql,
            db_path_cache[db],
            validate_timeout,
            check_has_null=True,
        )
        if bucket == NON_EMPTY:
            valid[db].append(row["q_id"])
        elif bucket == EMPTY:
            skipped_empty += 1
        else:
            skipped_error += 1

    print(
        f"[validate] base={os.path.basename(base_variant_dir)} "
        f"total={len(dev_rows)} "
        f"valid={ {db: len(v) for db, v in valid.items()} } "
        f"skipped_unknown_db={skipped_unknown_db} "
        f"skipped_no_sql={skipped_no_sql} "
        f"skipped_empty_result={skipped_empty} "
        f"skipped_error={skipped_error}"
    )
    return valid


def _sample_and_split(
    valid_by_db: Dict[str, List[int]],
    num_per_db: int,
    num_groups: int,
    rng: random.Random,
) -> Dict[str, Tuple[List[int], ...]]:
    """For each base_db, sample up to ``num_per_db`` q_ids and split into groups.

    If a db has fewer than ``num_per_db`` valid q_ids, keep all available q_ids.
    Group sizes are balanced with at most 1-item difference.

    Returns ``{base_db: (group0, group1, ...)}`` with sorted q_id lists.
    """
    if num_groups < 1:
        raise ValueError(f"num_groups must be >= 1, got {num_groups}")
    if num_per_db % num_groups != 0:
        raise ValueError(
            f"--num-per-db ({num_per_db}) must be divisible by the number of "
            f"variant slots per language ({num_groups})"
        )
    splits: Dict[str, Tuple[List[int], ...]] = {}
    for db, qids in valid_by_db.items():
        target = min(num_per_db, len(qids))
        if target < num_per_db:
            print(
                f"[sample] db={db} has only {len(qids)} valid q_ids "
                f"(requested {num_per_db}); keeping all available."
            )

        picked = rng.sample(qids, target)
        rng.shuffle(picked)
        base_chunk = target // num_groups
        remainder = target % num_groups
        parts_list: List[List[int]] = []
        start = 0
        for i in range(num_groups):
            size = base_chunk + (1 if i < remainder else 0)
            end = start + size
            parts_list.append(sorted(picked[start:end]))
            start = end
        parts = tuple(parts_list)
        splits[db] = parts
    return splits


def _flatten_sql(sql: str) -> str:
    return re.sub(r"\s+", " ", sql).strip()


def _build_dev(
    splits: Dict[str, Tuple[List[int], ...]],
    enq_list: List[str],
    cnq_list: List[str],
    rows_by_variant: Dict[str, Dict[int, dict]],
    base_dbs: List[str],
) -> List[dict]:
    """Compose the merged dev list in a stable, deterministic order."""
    k = len(enq_list)
    if len(cnq_list) != k:
        raise ValueError(
            f"enq_list length ({k}) must match cnq_list length ({len(cnq_list)})"
        )

    merged: List[dict] = []
    for base_db in base_dbs:
        group_id_lists = splits[base_db]
        if len(group_id_lists) != k:
            raise ValueError(
                f"split has {len(group_id_lists)} groups but enq_list has {k}"
            )

        for list_idx in range(k):
            qids_for_group = group_id_lists[list_idx]
            for side_list in (enq_list, cnq_list):
                variant_dir = side_list[list_idx]
                variant_short = _variant_short(variant_dir)
                language = _language_of(variant_short)
                new_db_id = f"{variant_short}-{base_db}"

                for orig_qid in qids_for_group:
                    row = rows_by_variant[variant_dir].get(orig_qid)
                    if row is None:
                        raise KeyError(
                            f"q_id {orig_qid} missing in variant {variant_dir}"
                        )
                    new_index = len(merged)
                    merged.append(
                        {
                            "q_id": f"{orig_qid}_{variant_short}_{new_index}",
                            "db_name": new_db_id,
                            "sql_query": row["sql_query"],
                            "question": row["question"],
                            "question_language": language,
                        }
                    )
    return merged


def _build_tables(
    variant_dirs: List[str],
    base_dbs: List[str],
) -> List[dict]:
    """Merge schema entries from each (variant, base_db) into one tables.json."""
    out: List[dict] = []
    for variant_dir in variant_dirs:
        variant_short = _variant_short(variant_dir)
        tables = _load_json(os.path.join(variant_dir, "tables.json"))
        by_db = {entry["db_id"]: entry for entry in tables}
        for base_db in base_dbs:
            if base_db not in by_db:
                raise KeyError(
                    f"tables.json in {variant_dir} has no db_id={base_db}"
                )
            entry = copy.deepcopy(by_db[base_db])
            entry["db_id"] = f"{variant_short}-{base_db}"
            out.append(entry)
    return out


def _ignore_junk_sqlite(_src_dir: str, names: List[str]) -> List[str]:
    """copytree ignore-callable that filters out upstream junk sqlite files.

    Some BULL exports leave 0-byte sqlite files whose name is a python-list
    repr (e.g. ``['ccks_fund', 'ccks_stock', 'ccks_macro'].sqlite``) sitting
    next to the real ``<base_db>.sqlite``. They confuse downstream tooling
    and waste a directory entry, so we drop them at copy time.
    """
    return [n for n in names if n.startswith("[") and n.endswith(".sqlite")]


def _copy_databases(
    variant_dirs: List[str],
    base_dbs: List[str],
    output_dir: str,
) -> None:
    """Hard-copy each (variant, base_db) directory under its new id.

    The source path is resolved with ``os.path.realpath`` so that variants
    whose ``database/`` (or whose entire variant dir) is a symlink to an
    external location get copied from the real files. ``shutil.copytree``
    is called with ``symlinks=False`` so any nested symlinks inside the
    source are also followed and materialized as real files.

    After the copy, the inner sqlite is renamed from ``<base_db>.sqlite``
    to ``<new_db_id>.sqlite`` so it matches the Spider-style path convention
    ``<db_dir>/<db_id>/<db_id>.sqlite`` that downstream evaluators rely on.
    Without this rename, the evaluator opens a non-existent file, sqlite3
    silently creates a 0-byte placeholder, and every gold + pred SQL fails
    with ``no such table: ...``.
    """
    db_root = os.path.join(output_dir, "database")
    _reset_dir(db_root)
    for variant_dir in variant_dirs:
        variant_short = _variant_short(variant_dir)
        for base_db in base_dbs:
            src = os.path.join(variant_dir, "database", base_db)
            if not os.path.isdir(src):
                raise FileNotFoundError(f"Missing source db dir: {src}")
            real_src = os.path.realpath(src)
            new_db_id = f"{variant_short}-{base_db}"
            dst = os.path.join(db_root, new_db_id)
            shutil.copytree(real_src, dst, symlinks=False, ignore=_ignore_junk_sqlite)

            src_sqlite = os.path.join(dst, f"{base_db}.sqlite")
            dst_sqlite = os.path.join(dst, f"{new_db_id}.sqlite")
            if not os.path.isfile(src_sqlite):
                raise FileNotFoundError(
                    f"Expected {base_db}.sqlite inside {real_src} after copy; "
                    f"got {os.listdir(dst)}"
                )
            if os.path.getsize(src_sqlite) == 0:
                raise RuntimeError(
                    f"Source sqlite is 0 bytes: {src_sqlite} "
                    f"(real_src={real_src}); refusing to propagate an empty db"
                )
            os.replace(src_sqlite, dst_sqlite)
            print(f"  copied {real_src} -> {dst} "
                  f"(renamed {base_db}.sqlite -> {new_db_id}.sqlite)")


def _write_dev_gold(dev_rows: List[dict], path: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        for row in dev_rows:
            f.write(f"{_flatten_sql(row['sql_query'])}\t{row['db_name']}\n")


def mix_language(
    enq_list: List[str],
    cnq_list: List[str],
    output_dir: str,
    num_per_db: int = 50,
    seed: int = 42,
    base_dbs: Tuple[str, ...] = ("ccks_fund", "ccks_macro", "ccks_stock"),
    validate_timeout: float = 30.0,
) -> None:
    if len(enq_list) != len(cnq_list):
        raise ValueError(
            "enq_list and cnq_list must have the same length "
            f"(got {len(enq_list)} vs {len(cnq_list)})"
        )
    if len(enq_list) < 1:
        raise ValueError("enq_list and cnq_list must each have at least one directory")

    k = len(enq_list)
    base_variant = enq_list[0]
    valid_by_db = _validate_pool(
        base_variant, list(base_dbs), validate_timeout=validate_timeout
    )

    rng = random.Random(seed)
    splits = _sample_and_split(valid_by_db, num_per_db, k, rng)

    variant_dirs = enq_list + cnq_list
    rows_by_variant = {
        v: _index_rows(_load_json(os.path.join(v, "dev.json")))
        for v in variant_dirs
    }

    dev_rows = _build_dev(splits, enq_list, cnq_list, rows_by_variant, list(base_dbs))
    tables = _build_tables(variant_dirs, list(base_dbs))

    os.makedirs(output_dir, exist_ok=True)
    _copy_databases(variant_dirs, list(base_dbs), output_dir)
    _write_json(os.path.join(output_dir, "tables.json"), tables)
    _write_json(os.path.join(output_dir, "dev.json"), dev_rows)
    _write_dev_gold(dev_rows, os.path.join(output_dir, "dev_gold.sql"))

    print(
        f"[done] wrote {len(dev_rows)} dev rows, {len(tables)} table entries, "
        f"{len(variant_dirs) * len(base_dbs)} db copies to {output_dir}"
    )


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Combine K English-question variants and K Chinese-question "
            "variants of BULL-FinSQL into a single mixed dataset (same K, "
            "aligned by index)."
        )
    )
    parser.add_argument(
        "--enq-list",
        nargs="+",
        default=[
            "dataset/BULL-FinSQL/BULL-en-origin",
            "dataset/BULL-FinSQL/BULL-enq-cnds-cndv",
            # "dataset/BULL-FinSQL/BULL-enq-ends-endv",
        ],
        metavar="DIR",
        help=(
            "English-question variant dirs in order; len must match --cnq-list. "
            "num-per-db must be divisible by this count."
        ),
    )
    parser.add_argument(
        "--cnq-list",
        nargs="+",
        default=[
            "dataset/BULL-FinSQL/BULL-cn-origin",
            "dataset/BULL-FinSQL/BULL-cnq-ends-endv",
            # "dataset/BULL-FinSQL/BULL-cnq-cnds-cndv",
        ],
        metavar="DIR",
        help=(
            "Chinese-question variant dirs in order; len must match --enq-list. "
            "num-per-db must be divisible by this count."
        ),
    )
    parser.add_argument("--output-dir", required=True, help="Destination directory")
    parser.add_argument(
        "--num-per-db",
        type=int,
        default=50,
        help=(
            "Number of q_ids to sample per base db; must be divisible by the "
            "number of dirs in --enq-list (same as --cnq-list). Default 50."
        ),
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for sampling and splitting.",
    )
    parser.add_argument(
        "--validate-timeout",
        type=float,
        default=30.0,
        help=(
            "Per-query timeout (seconds) when filtering the base dev split "
            "with check_empty_sql-style execution; default matches "
            "check_empty_sql.py --timeout."
        ),
    )
    parser.add_argument(
        "--base-db",
        action="append",
        default=None,
        help=(
            "Optional override for the list of base dbs. Pass once per db. "
            "Defaults to ccks_fund, ccks_macro, ccks_stock."
        ),
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    base_dbs = tuple(args.base_db) if args.base_db else (
        "ccks_fund",
        "ccks_macro",
        "ccks_stock",
    )
    mix_language(
        enq_list=args.enq_list,
        cnq_list=args.cnq_list,
        output_dir=args.output_dir,
        num_per_db=args.num_per_db,
        seed=args.seed,
        base_dbs=base_dbs,
        validate_timeout=args.validate_timeout,
    )


if __name__ == "__main__":
    main()
