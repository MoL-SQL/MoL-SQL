#!/usr/bin/env python3
"""Mix language variants like ``mix_language_split.py``, but duplicate q_ids across variants.

``mix_language_split.py`` samples ``num_per_db`` q_ids per base database from the
validated pool of ``enq_list[0]``, then **splits** them into K disjoint groups so
each English/Chinese variant pair only sees a slice.

This script samples ``num_per_db`` q_ids once per base database and then, for
**every** index in ``--enq-list`` / ``--cnq-list``, emits rows for that **same**
set of ``q_id`` values from the corresponding variant. So if K=3 and
``num_per_db`` is 50, ``dev.json`` contains the parallel questions for the same
50 ids from all three English variants and all three Chinese variants per base
db (``2 * K * num_per_db * len(base_dbs)`` rows total by default).
"""

from __future__ import annotations

import argparse
import os
import random
import sys
from typing import Dict, List, Tuple

_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
if _THIS_DIR not in sys.path:
    sys.path.insert(0, _THIS_DIR)

import mix_language_split as mls  # noqa: E402


def _sample_per_db(
    valid_by_db: Dict[str, List[int]],
    num_per_db: int,
    rng: random.Random,
) -> Dict[str, List[int]]:
    """Sample ``num_per_db`` q_ids per base_db (no split across K variants)."""
    out: Dict[str, List[int]] = {}
    for db, qids in valid_by_db.items():
        if len(qids) < num_per_db:
            raise RuntimeError(
                f"Not enough valid q_ids for db={db}: "
                f"need {num_per_db}, have {len(qids)}"
            )
        picked = sorted(rng.sample(qids, num_per_db))
        out[db] = picked
    return out


def _build_dev_copy(
    qids_by_db: Dict[str, List[int]],
    enq_list: List[str],
    cnq_list: List[str],
    rows_by_variant: Dict[str, Dict[int, dict]],
    base_dbs: List[str],
) -> List[dict]:
    k = len(enq_list)
    if len(cnq_list) != k:
        raise ValueError(
            f"enq_list length ({k}) must match cnq_list length ({len(cnq_list)})"
        )

    merged: List[dict] = []
    for base_db in base_dbs:
        qids = qids_by_db[base_db]
        for list_idx in range(k):
            for side_list in (enq_list, cnq_list):
                variant_dir = side_list[list_idx]
                variant_short = mls._variant_short(variant_dir)
                language = mls._language_of(variant_short)
                new_db_id = f"{variant_short}-{base_db}"

                for orig_qid in qids:
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


def mix_language_copy(
    enq_list: List[str],
    cnq_list: List[str],
    output_dir: str,
    num_per_db: int = 30,
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

    base_variant = enq_list[0]
    valid_by_db = mls._validate_pool(
        base_variant, list(base_dbs), validate_timeout=validate_timeout
    )

    rng = random.Random(seed)
    qids_by_db = _sample_per_db(valid_by_db, num_per_db, rng)

    variant_dirs = enq_list + cnq_list
    rows_by_variant = {
        v: mls._index_rows(mls._load_json(os.path.join(v, "dev.json")))
        for v in variant_dirs
    }

    dev_rows = _build_dev_copy(qids_by_db, enq_list, cnq_list, rows_by_variant, list(base_dbs))
    tables = mls._build_tables(variant_dirs, list(base_dbs))

    os.makedirs(output_dir, exist_ok=True)
    mls._copy_databases(variant_dirs, list(base_dbs), output_dir)
    mls._write_json(os.path.join(output_dir, "tables.json"), tables)
    mls._write_json(os.path.join(output_dir, "dev.json"), dev_rows)
    mls._write_dev_gold(dev_rows, os.path.join(output_dir, "dev_gold.sql"))

    print(
        f"[done] wrote {len(dev_rows)} dev rows, {len(tables)} table entries, "
        f"{len(variant_dirs) * len(base_dbs)} db copies to {output_dir}"
    )


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Merge K English and K Chinese BULL-FinSQL variants; reuse the same "
            "sampled q_ids for every variant (no disjoint split across K)."
        )
    )
    parser.add_argument(
        "--enq-list",
        nargs="+",
        default=[
            "dataset/BULL-FinSQL/BULL-en-origin",
            "dataset/BULL-FinSQL/BULL-enq-cnds-cndv",
            "dataset/BULL-FinSQL/BULL-enq-ends-endv",
        ],
        metavar="DIR",
        help="English-question variant dirs in order; len must match --cnq-list.",
    )
    parser.add_argument(
        "--cnq-list",
        nargs="+",
        default=[
            "dataset/BULL-FinSQL/BULL-cn-origin",
            "dataset/BULL-FinSQL/BULL-cnq-ends-endv",
            "dataset/BULL-FinSQL/BULL-cnq-cnds-cndv",
        ],
        metavar="DIR",
        help="Chinese-question variant dirs in order; len must match --enq-list.",
    )
    parser.add_argument("--output-dir", required=True, help="Destination directory")
    parser.add_argument(
        "--num-per-db",
        type=int,
        default=30,
        help="Number of q_ids to sample per base db (shared by all K variants). Default 30.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for sampling.",
    )
    parser.add_argument(
        "--validate-timeout",
        type=float,
        default=30.0,
        help=(
            "Per-query timeout (seconds) when filtering the base dev split "
            "with check_empty_sql-style execution."
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
    mix_language_copy(
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
