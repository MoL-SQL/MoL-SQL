#!/usr/bin/env python3
"""
Generate Text2SQL prompts for dev examples and save to JSON.

Unified CLI for Spider, BIRD, and BULL using ``DATASET_REGISTRY``.
"""

import argparse
import json
import os
import sys

from tqdm import tqdm

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import (
    DATASET_REGISTRY,
    STD_DB_DIR,
    STD_DEV_JSON_FILE,
    STD_TABLES_FILE,
    get_config,
    get_split_files,
)
from text2sql_exp.prompts import DEFAULT_FEW_SHOT_EXAMPLES
from text2sql_exp.text2sql import build_prompt_only, get_db_path, get_schema, load_tables


def _resolve_dataset_dir(dataset: str, script_dir: str) -> str:
    return os.path.normpath(os.path.join(script_dir, "..", "..", "dataset", dataset))


def _parse_few_shot_items(raw, sql_field_candidates) -> list:
    items = []
    for item in raw:
        q = item.get("question", "")
        sql = None
        for field in sql_field_candidates:
            sql = item.get(field)
            if sql and isinstance(sql, str):
                break
        knowledge = item.get("knowledge") or item.get("evidence")
        if q and sql:
            items.append((q, sql, knowledge or None))
    return items


def _few_shots_for_example(example: dict, index: int, few_shot_map, global_examples):
    if few_shot_map is None:
        return global_examples
    for key in (
        example.get("logical_id"),
        example.get("question_id"),
        str(index),
    ):
        if key is None or key == "":
            continue
        mapped = few_shot_map.get(str(key))
        if mapped is not None:
            return mapped
    raise SystemExit(
        "No few-shot map entry for "
        f"index={index} logical_id={example.get('logical_id')!r} "
        f"question_id={example.get('question_id')!r}"
    )


def _lookup_mapped(example: dict, index: int, mapping):
    if mapping is None:
        return None
    for key in (
        example.get("logical_id"),
        example.get("question_id"),
        str(index),
    ):
        if key is None or key == "":
            continue
        mapped = mapping.get(str(key))
        if mapped is not None:
            return mapped
    raise SystemExit(
        "No map entry for "
        f"index={index} logical_id={example.get('logical_id')!r} "
        f"question_id={example.get('question_id')!r}"
    )


def _value_text_for_example(example: dict, index: int, value_map):
    if value_map is None:
        return None
    mapped = _lookup_mapped(example, index, value_map)
    if isinstance(mapped, str):
        return mapped
    if isinstance(mapped, dict):
        text = mapped.get("text")
        if isinstance(text, str):
            return text
    raise SystemExit(
        "Value map entry must be a string or an object with a text field: "
        f"index={index} logical_id={example.get('logical_id')!r}"
    )


def _load_schema_linking(path: str):
    if not path:
        return {}
    if not os.path.isfile(path):
        print(f"Schema-linking file not found: {path}", file=sys.stderr)
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)
    entries = raw.get("examples", raw) if isinstance(raw, dict) else raw
    links = {}
    for idx, item in enumerate(entries):
        if not isinstance(item, dict):
            continue
        item_idx = item.get("index", idx)
        links[int(item_idx)] = item.get("tables", [])
    return links


def main():
    parser = argparse.ArgumentParser(description="Generate Text2SQL prompts to JSON")
    parser.add_argument("--dataset", type=str, required=True,
                        choices=sorted(DATASET_REGISTRY.keys()),
                        help="Dataset variant name")
    parser.add_argument("--output", type=str, default=None,
                        help="Output JSON path (default: auto-generated)")
    parser.add_argument("--end_index", type=int, default=None,
                        help="Process only [0, end_index)")
    parser.add_argument("--dataset_dir", type=str, default=None,
                        help="Override dataset root directory")
    parser.add_argument("--db_base_dir", type=str, default=None,
                        help="Override DB base directory (when DBs live elsewhere)")
    parser.add_argument("--split", type=str, default="dev",
                        help="Question/gold split to load (dev|train|test). "
                             "Selects the questions JSON file name.")
    parser.add_argument("--tables_file", type=str, default=None,
                        help="Override schema (tables) file name relative to "
                             f"the dataset dir (default: {STD_TABLES_FILE})")
    parser.add_argument("--db_dir", type=str, default=None,
                        help="Override DB subdirectory name relative to the DB "
                             f"base dir (default: {STD_DB_DIR})")
    parser.add_argument("--sample_rows", type=int, default=10,
                        help="Sample rows per table (default: 10)")
    parser.add_argument("--random_sample_rows", action="store_true",
                        help="Use random rows instead of first N")
    parser.add_argument("--include_evidence", action="store_true",
                        help="Include evidence field in prompt (BIRD)")
    parser.add_argument("--chinese_prompt", action="store_true",
                        help="Use Chinese instruction text")
    parser.add_argument("--cot", action="store_true",
                        help="Add Chain-of-Thought analysis")
    parser.add_argument("--few_shot", action="store_true",
                        help="Add few-shot examples")
    parser.add_argument("--few_shot_file", type=str, default=None,
                        help="JSON file with few-shot examples")
    parser.add_argument("--few_shot_map", type=str, default=None,
                        help="JSON object mapping logical_id/question_id/index "
                             "to a list of per-example few-shot examples")
    parser.add_argument("--value_map", type=str, default=None,
                        help="JSON object mapping logical_id/question_id/index "
                             "to a retrieved-values block or an object with a "
                             "``text`` field")
    parser.add_argument("--schema_linking_file", type=str, default=None,
                        help="JSON file with per-example linked tables")
    parser.add_argument("--prompt_mode", type=str, default="none",
                        choices=["bull", "spider", "bird", "none", "q_to_db", "baseline_cot"],
                        help="Dataset-specific prompt note mode")
    parser.add_argument("--output_style", type=str, default="label",
                        choices=["label", "xml"],
                        help="Response format: 'label' (Analysis:/SQL:) or "
                             "'xml' (<cot>...</cot><sql>...</sql>). xml implies CoT.")
    args = parser.parse_args()

    cfg = get_config(args.dataset)
    script_dir = os.path.dirname(os.path.abspath(__file__))

    dataset_dir = args.dataset_dir or _resolve_dataset_dir(args.dataset, script_dir)
    if not os.path.isdir(dataset_dir):
        print(f"Dataset dir not found: {dataset_dir}", file=sys.stderr)
        sys.exit(1)

    # DB base dir: might differ from dataset dir (e.g. endb-cnqt uses bird DBs)
    if args.db_base_dir:
        db_base_dir = args.db_base_dir
    elif cfg.db_base_dataset:
        db_base_dir = _resolve_dataset_dir(cfg.db_base_dataset, script_dir)
    else:
        db_base_dir = dataset_dir

    split_json_file, _ = get_split_files(args.split)
    db_subdir = args.db_dir or STD_DB_DIR
    dev_path = os.path.join(dataset_dir, split_json_file)
    tables_path = os.path.join(dataset_dir, args.tables_file or STD_TABLES_FILE)
    for p, label in [(dev_path, f"{args.split} questions file"), (tables_path, "Tables file")]:
        if not os.path.isfile(p):
            print(f"{label} not found: {p}", file=sys.stderr)
            sys.exit(1)

    with open(dev_path, "r", encoding="utf-8") as f:
        examples = json.load(f)
    schemas = load_tables(tables_path)
    schema_links = _load_schema_linking(args.schema_linking_file)

    end = args.end_index if args.end_index is not None else len(examples)
    examples = examples[:end]

    # Few-shot examples
    few_shot_examples = None
    few_shot_map = None
    if args.few_shot_map:
        if not os.path.isfile(args.few_shot_map):
            print(f"Few-shot map not found: {args.few_shot_map}", file=sys.stderr)
            sys.exit(1)
        with open(args.few_shot_map, "r", encoding="utf-8") as f:
            raw_map = json.load(f)
        if not isinstance(raw_map, dict):
            print(f"Few-shot map must be a JSON object: {args.few_shot_map}", file=sys.stderr)
            sys.exit(1)
        few_shot_map = {
            str(key): _parse_few_shot_items(value, cfg.sql_field_candidates)
            for key, value in raw_map.items()
        }
    elif args.few_shot or args.few_shot_file:
        fs_path = args.few_shot_file
        if not fs_path or not os.path.isfile(fs_path):
            fs_path = os.path.join(script_dir, "few_shot_examples", f"{args.dataset}.json")
        if fs_path and os.path.isfile(fs_path):
            with open(fs_path, "r", encoding="utf-8") as f:
                raw = json.load(f)
            few_shot_examples = _parse_few_shot_items(raw, cfg.sql_field_candidates)
        if not few_shot_examples:
            few_shot_examples = DEFAULT_FEW_SHOT_EXAMPLES

    value_map = None
    if args.value_map:
        if not os.path.isfile(args.value_map):
            print(f"Value map not found: {args.value_map}", file=sys.stderr)
            sys.exit(1)
        with open(args.value_map, "r", encoding="utf-8") as f:
            raw_value_map = json.load(f)
        if not isinstance(raw_value_map, dict):
            print(f"Value map must be a JSON object: {args.value_map}", file=sys.stderr)
            sys.exit(1)
        value_map = {str(key): value for key, value in raw_value_map.items()}

    # Output path
    out_path = args.output
    if out_path is None:
        suffix = f"_{args.split}"
        if args.cot:
            suffix += "_cot"
        if args.few_shot or args.few_shot_map:
            suffix += "_fewshot"
        if args.output_style != "label":
            suffix += f"_{args.output_style}"
        out_dir = os.path.join(script_dir, "..", "..", "intermediate_data", "prompts")
        out_path = os.path.join(out_dir, f"{args.dataset}{suffix}.json")
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)

    out_entries = []
    for idx, ex in enumerate(tqdm(examples, desc="Generating prompts")):
        question = ex.get("question", "")
        db_id = ex.get(cfg.db_id_field) or ex.get("db_id") or ex.get("db_name", "")
        evidence = ex.get("evidence", "") if args.include_evidence else None
        schema = get_schema(schemas, db_id)
        if not schema:
            out_entries.append({**ex, "prompt": "", "output_style": args.output_style})
            continue
        db_path = get_db_path(db_base_dir, db_id, db_subdir=db_subdir)
        selected_tables = schema_links.get(idx, []) if args.schema_linking_file else None
        prompt = build_prompt_only(
            question=question,
            db_path=db_path,
            db_id=db_id,
            sample_rows_per_table=args.sample_rows,
            db_encoding=cfg.db_encoding,
            use_cot=args.cot,
            few_shot_examples=_few_shots_for_example(
                ex, idx, few_shot_map, few_shot_examples
            ),
            random_sample_rows=args.random_sample_rows,
            evidence=evidence,
            chinese_prompt=args.chinese_prompt,
            prompt_mode=args.prompt_mode,
            table_names=selected_tables,
            output_style=args.output_style,
            retrieved_values_text=_value_text_for_example(ex, idx, value_map),
        )
        extra = {"schema_linking_tables": selected_tables} if selected_tables is not None else {}
        out_entries.append({
            **ex,
            **extra,
            "prompt": prompt,
            "output_style": args.output_style,
        })

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out_entries, f, ensure_ascii=False, indent=2)
    print(f"Wrote {len(out_entries)} entries to {out_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
