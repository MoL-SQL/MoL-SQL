#!/usr/bin/env python3
"""
Replace NL questions in one dataset variant with questions from another
(index-aligned).

Used for cross-lingual variants: e.g. take an English-DB / English-SQL
dataset and graft Chinese translated questions onto it (or vice versa),
producing a ``cnq_end`` style merged dataset.

Standard pipeline argument format (mirrors ``nl_translate.py``):

    --dataset    DATASET_NAME            (registry key for tokenizer/direction defaults)
    --base-dir   DIR                     (provides DB / SQL / tables; questions overwritten)
    --donor-dir  DIR                     (provides NL questions to graft)
    --output-dir DIR                     (merged dataset output)
    --direction  en2cn|cn2en             (optional; defaults to dataset config)
    --split      dev|train|test          (optional; defaults to dev)
"""

import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import get_config, get_split_files
from data_translate.nl_translate import sync_static_dataset_artifacts


def main():
    parser = argparse.ArgumentParser(
        description="Replace questions in base dataset with questions from donor dataset (index-aligned)."
    )
    parser.add_argument("--dataset", required=True,
                        help="Dataset name (for config: tokenizer, direction)")
    parser.add_argument("--base-dir", dest="base_dir", required=True,
                        help="Base dataset directory (keeps DB/SQL/tables; questions will be overwritten)")
    parser.add_argument("--donor-dir", dest="donor_dir", required=True,
                        help="Donor dataset directory (provides questions)")
    parser.add_argument("--output-dir", dest="output_dir", required=True,
                        help="Output dataset directory")
    parser.add_argument("--direction", default=None, choices=["en2cn", "cn2en"],
                        help="Translation direction (default: from dataset config). "
                             "Selects question_toks tokeniser: en2cn=char, cn2en=word.")
    parser.add_argument("--split", default="dev", help="Split to merge (dev/train/test)")
    args = parser.parse_args()

    cfg = get_config(args.dataset)
    direction = args.direction or cfg.translate_direction
    tokenizer = "char" if direction == "en2cn" else "word"

    json_file, gold_file = get_split_files(args.split)
    base_path = os.path.join(args.base_dir, json_file)
    donor_path = os.path.join(args.donor_dir, json_file)
    output_path = os.path.join(args.output_dir, json_file)
    output_gold = os.path.join(args.output_dir, gold_file)

    with open(base_path, "r", encoding="utf-8") as f:
        data_base = json.load(f)
    with open(donor_path, "r", encoding="utf-8") as f:
        data_donor = json.load(f)

    if len(data_base) != len(data_donor):
        print(
            f"Warning: length mismatch — base has {len(data_base)}, "
            f"donor has {len(data_donor)}",
            file=sys.stderr,
        )

    out = []
    for i, entry in enumerate(data_base):
        new = {**entry}
        if i < len(data_donor):
            new["question"] = data_donor[i]["question"]
            if "question_toks" in data_donor[i]:
                new["question_toks"] = data_donor[i]["question_toks"]
            else:
                q = data_donor[i]["question"]
                new["question_toks"] = list(q) if tokenizer == "char" else q.split()
        out.append(new)

    os.makedirs(args.output_dir, exist_ok=True)
    sync_static_dataset_artifacts(args.base_dir, args.output_dir)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)

    if cfg.has_gold:
        gold_lines = []
        for entry in out:
            sql = (entry.get(cfg.sql_field)
                   or entry.get("SQL")
                   or entry.get("query")
                   or entry.get("sql_query")
                   or entry.get("sql", ""))
            db_id = entry.get(cfg.db_id_field) or entry.get("db_id") or entry.get("db_name", "")
            flat_sql = re.sub(r"\s+", " ", sql).strip()
            gold_lines.append(f"{flat_sql}\t{db_id}\n")
        with open(output_gold, "w", encoding="utf-8") as f:
            f.writelines(gold_lines)
        print(f"Written {len(out)} entries to {output_path} and {output_gold}")
    else:
        print(f"Written {len(out)} entries to {output_path}")


if __name__ == "__main__":
    main()
