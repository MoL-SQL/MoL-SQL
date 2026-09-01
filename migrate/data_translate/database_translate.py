#!/usr/bin/env python3
"""
Unified frontend for the full database + SQL translation pipeline (EN↔CN).

Orchestrates four steps using functions imported from the existing modules:
  1. Prompt generation   (db_translate_prompt)
  2. LLM batch calls     (db_translate_llm_batch)
  3. SQLite DB rewriting  (db_translate_sqlite)
  4. SQL query translation (sql_translate)
"""

import argparse
import json
import os
import shutil
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import Counter

from tqdm import tqdm

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import (
    STD_DB_DIR,
    STD_TABLES_FILE,
    get_config,
    get_split_files,
)
from utils import execute_query, get_llm_client, load_json

from db_translate_llm_batch import (
    process_single_content,
    process_single_schema,
    save_config,
)
from db_translate_prompt import generate_prompts_for_db
from db_translate_sqlite import (
    replace_entities_in_db,
    update_metadata_json,
    validate_translation,
)
from sql_translate import (
    build_precise_maps,
    is_structure_match,
    tokenize_sql,
    tokenize_sql_no_value,
    translate_sql,
)
from sql_translate_CTE import (
    translate_sql_CTE,
)
from sql_translate_SQLGlot import (
    translate_sql_sqlglot,
)

# ---------------------------------------------------------------------------
# Step 1 – Prompt generation
# ---------------------------------------------------------------------------

def step_generate_prompts(source_dir, prompts_dir, direction,
                          skip_content_if_unique_above, content_chunk_size,
                          values_only=False, force=False):
    """Generate per-DB translation prompts from the source dataset."""
    db_base = os.path.join(source_dir, STD_DB_DIR)
    db_info_path = os.path.join(source_dir, STD_TABLES_FILE)
    os.makedirs(prompts_dir, exist_ok=True)

    if force:
        stale_prompt_count = 0
        for fname in os.listdir(prompts_dir):
            prompt_path = os.path.join(prompts_dir, fname)
            if fname.endswith(".json") and os.path.isfile(prompt_path):
                os.remove(prompt_path)
                stale_prompt_count += 1
        print(f"[Step 1] --force removed {stale_prompt_count} prompt JSON files")

    with open(db_info_path, "r", encoding="utf-8") as f:
        db_info_list = json.load(f)

    arrow = "EN→CN" if direction == "en2cn" else "CN→EN"
    extra = " (values only)" if values_only else ""
    print(f"[Step 1] Loaded {len(db_info_list)} databases ({arrow}{extra})")
    for db_info in tqdm(db_info_list, desc="Generating prompts"):
        generate_prompts_for_db(
            db_info,
            db_base,
            prompts_dir,
            direction=direction,
            skip_content_if_unique_above=skip_content_if_unique_above,
            content_chunk_size=content_chunk_size,
            values_only=values_only,
        )


# ---------------------------------------------------------------------------
# Step 2 – LLM batch translation → replacements config
# ---------------------------------------------------------------------------

def step_llm_batch(prompts_dir, output_config, model, workers,
                   api_key, api_base):
    """Call the LLM to produce a unified replacements config from prompts."""
    client = get_llm_client(api_key=api_key, base_url=api_base)

    schema_prompts, content_prompts = [], []
    for fname in os.listdir(prompts_dir):
        if not fname.endswith(".json"):
            continue
        with open(os.path.join(prompts_dir, fname), "r", encoding="utf-8") as f:
            data = json.load(f)
        for p in data:
            (schema_prompts if p["type"] == "schema" else content_prompts).append(p)

    final_config = {}

    if schema_prompts:
        print(f"[Step 2] Translating {len(schema_prompts)} schemas …")
        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures = {
                executor.submit(process_single_schema, client, p, model): p["db_id"]
                for p in schema_prompts
            }
            for future in tqdm(as_completed(futures), total=len(futures)):
                res = future.result()
                if res:
                    final_config[res["db_id"]] = {
                        "tables": res["tables"],
                        "columns": res["columns"],
                        "values": [],
                    }

        save_config(final_config, output_config)
        print(f"[Step 2] Saved {len(final_config)} schemas")
    else:
        print("[Step 2] No schema prompts (values-only mode)")

    print(f"[Step 2] Translating {len(content_prompts)} content batches …")
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {
            executor.submit(process_single_content, client, p, model): p["db_id"]
            for p in content_prompts
        }
        for future in tqdm(as_completed(futures), total=len(futures)):
            res = future.result()
            if res:
                final_config.setdefault(res["db_id"], {
                    "tables": [], "columns": [], "values": [],
                })["values"].extend(res["values"])

    save_config(final_config, output_config)
    print(f"[Step 2] Replacements config saved to {output_config}")


# ---------------------------------------------------------------------------
# Step 3 – Apply replacements to SQLite databases
# ---------------------------------------------------------------------------

def step_translate_sqlite(source_dir, output_dir, replacements_config_path,
                          values_only):
    """Rewrite SQLite databases and update tables.json using the replacements config."""
    source_db_dir = os.path.join(source_dir, STD_DB_DIR)
    output_db_dir = os.path.join(output_dir, STD_DB_DIR)
    input_tables = os.path.join(source_dir, STD_TABLES_FILE)
    output_tables = os.path.join(output_dir, STD_TABLES_FILE)

    replacements_config = load_json(replacements_config_path)
    if not replacements_config:
        print("[Step 3] Error: empty replacements config.")
        sys.exit(1)
    tables_data = load_json(input_tables) or []
    table_db_ids = [entry.get("db_id", "") for entry in tables_data if entry.get("db_id")]
    translated_db_ids = set(replacements_config.keys())

    print(f"[Step 3] Translating {len(replacements_config)} databases …")
    for db_id, tasks in tqdm(replacements_config.items(), desc="Rewriting DBs"):
        src = os.path.join(source_db_dir, db_id, f"{db_id}.sqlite")
        out = os.path.join(output_db_dir, db_id, f"{db_id}.sqlite")
        replace_entities_in_db(src, out, tasks, values_only=values_only)
        validate_translation(src, out, tasks)

    passthrough = [db_id for db_id in table_db_ids if db_id not in translated_db_ids]
    for db_id in passthrough:
        src = os.path.join(source_db_dir, db_id, f"{db_id}.sqlite")
        out = os.path.join(output_db_dir, db_id, f"{db_id}.sqlite")
        if not os.path.exists(src):
            continue
        os.makedirs(os.path.dirname(out), exist_ok=True)
        shutil.copy2(src, out)
        print(f"  [Info] pass-through DB copy for {db_id}")

    if not values_only:
        update_metadata_json(
            input_tables,
            output_tables,
            replacements_config,
            translated_db_dir=output_db_dir,
        )
    else:
        os.makedirs(os.path.dirname(output_tables) or ".", exist_ok=True)
        shutil.copy2(input_tables, output_tables)

    print("[Step 3] Database translation done.")


# ---------------------------------------------------------------------------
# Step 4 – SQL query translation
# ---------------------------------------------------------------------------

def _schema_coverage_report(split_data, tables_src, tables_tgt):
    src_ids = {entry.get("db_id", "") for entry in tables_src}
    tgt_ids = {entry.get("db_id", "") for entry in tables_tgt}
    split_counter = Counter(
        (entry.get("db_id") or entry.get("db_name") or "").strip()
        for entry in split_data
    )
    split_counter.pop("", None)
    missing = {}
    for db_id, count in split_counter.items():
        missing_sides = []
        if db_id not in src_ids:
            missing_sides.append("source tables.json")
        if db_id not in tgt_ids:
            missing_sides.append("target tables.json")
        if missing_sides:
            missing[db_id] = {"count": count, "missing": missing_sides}
    return missing


def step_translate_sql(dataset, source_dir, target_dir, replacements_path,
                       output_dir, direction, split, manual_sql,
                       manual_replace_sql, execute_timeout,
                       schema_missing_policy="fail", translator="manual"):
    """Translate SQL queries using schema maps and the replacements config."""
    cfg = get_config(dataset)
    direction = direction or cfg.translate_direction
    split_json, split_gold = get_split_files(split)
    input_json = split_json
    if translator == "cte":
        # CTE-aware mode writes to new_<split>.json / new_<split>_gold.sql so the
        # default outputs are left untouched for side-by-side comparison.
        split_json = f"new_{split_json}"
        split_gold = f"new_{split_gold}"
        sql_translator = translate_sql_CTE
    elif translator == "sqlglot":
        # SQLGlot mode writes to <split>_sqlglot.json / <split>_sqlglot_gold.sql
        # (e.g. dev_sqlglot.json) for side-by-side comparison.
        base, ext = os.path.splitext(split_json)
        split_json = f"{base}_sqlglot{ext}"
        split_gold = split_gold.replace("_gold.sql", "_sqlglot_gold.sql")
        sql_translator = translate_sql_sqlglot
    else:
        sql_translator = translate_sql

    src_db_dir = os.path.join(source_dir, STD_DB_DIR)
    tgt_db_dir = os.path.join(target_dir, STD_DB_DIR)
    tables_src_path = os.path.join(source_dir, STD_TABLES_FILE)
    tables_tgt_path = os.path.join(target_dir, STD_TABLES_FILE)
    input_json_path = os.path.join(source_dir, input_json)

    if direction == "en2cn":
        src_encoding = cfg.db_encoding
        tgt_encoding = "utf-8"
    else:
        src_encoding = "utf-8"
        tgt_encoding = cfg.db_encoding

    tables_src = load_json(tables_src_path)
    tables_tgt = load_json(tables_tgt_path)
    replacements = load_json(replacements_path)
    split_data = load_json(input_json_path)
    manual = (
        load_json(manual_sql)
        if manual_sql and os.path.exists(manual_sql)
        else []
    )
    manual_replace = (
        load_json(manual_replace_sql)
        if manual_replace_sql and os.path.exists(manual_replace_sql)
        else []
    )
    manual_replace_map = {}
    for item in manual_replace:
        key = (item.get("db_id", ""), item.get("gold_sql", ""))
        manual_replace_map[key] = item.get("translated_sql", "")

    output_json = os.path.join(output_dir, split_json)
    output_gold = os.path.join(output_dir, split_gold)
    os.makedirs(output_dir, exist_ok=True)

    out_entries, gold_lines = [], []
    stats = {
        "success": 0, "fail": 0, "warning": 0,
        "manual_success": 0, "manual_fail": 0, "manual_warning": 0,
    }

    def _sql_preview(sql, max_len=120):
        if not sql:
            return ""
        s = sql.replace("\n", " ").strip()
        return s if len(s) <= max_len else s[: max_len - 3] + "..."

    def _one_line_sql(sql):
        """Gold SQL files expect exactly one query per physical line."""
        return " ".join(
            line.strip()
            for line in str(sql).replace("\r\n", "\n").replace("\r", "\n").split("\n")
            if line.strip()
        )

    missing_schema = _schema_coverage_report(split_data, tables_src, tables_tgt)
    missing_db_ids = set(missing_schema.keys())
    if missing_schema:
        print("[Step 4][Preflight] Missing schema maps for db_id(s):")
        for db_id, info in sorted(missing_schema.items()):
            sides = ", ".join(info["missing"])
            print(f"  - {db_id}: {info['count']} entries (missing in {sides})")
        if schema_missing_policy == "fail":
            raise RuntimeError(
                "Schema coverage preflight failed. "
                "Use --schema-missing-policy skip to skip these db_ids."
            )
        print(
            f"[Step 4][Preflight] Continuing with skip policy for "
            f"{len(missing_schema)} db_id(s)."
        )

    print(f"[Step 4] Translating {len(split_data)} SQL queries ({split} split) …")
    for entry in tqdm(split_data, desc="Translating SQL"):
        db_id = entry.get("db_id") or entry.get("db_name", "")
        if db_id in missing_db_ids:
            stats["warning"] += 1
            continue
        src_sql = (
            entry.get(cfg.sql_field)
            or entry.get("SQL")
            or entry.get("query")
            or entry.get("sql_query")
            or entry.get("sql")
        )
        if not src_sql:
            stats["fail"] += 1
            print(f"\n[Fail] db_id={db_id!r}: missing SQL in entry")
            continue

        maps = build_precise_maps(db_id, tables_src, tables_tgt)
        if not maps:
            stats["fail"] += 1
            print(f"\n[Fail] db_id={db_id!r}: no schema maps ({_sql_preview(src_sql)})")
            continue

        db_reps = replacements.get(db_id, {})
        tgt_sql = sql_translator(src_sql, maps, db_reps)

        src_res = execute_query(
            os.path.join(src_db_dir, db_id, f"{db_id}.sqlite"),
            src_sql, encoding=src_encoding, timeout=execute_timeout,
        )
        tgt_res = execute_query(
            os.path.join(tgt_db_dir, db_id, f"{db_id}.sqlite"),
            tgt_sql, encoding=tgt_encoding, timeout=execute_timeout,
        )

        timeout_src = src_res == "Error: timeout"
        timeout_tgt = tgt_res == "Error: timeout"

        if not timeout_src and not timeout_tgt and src_res is not None and src_res == tgt_res:
            stats["success"] += 1
        elif is_structure_match(src_res, tgt_res):
            stats["warning"] += 1
            hint = []
            if timeout_src:
                hint.append("gold timeout")
            if timeout_tgt:
                hint.append("translated timeout")
            extra = f"; {', '.join(hint)}" if hint else ""
            # print(
            #     f"[Warning] db_id={db_id!r}: results differ but structure matches"
            #     f"{extra} (gold={_sql_preview(str(src_res))}, translated={_sql_preview(str(tgt_res))})"
            # )
        else:
            flag = False
            for item in manual:
                if item.get("src_sql") == src_sql or item.get("en_sql") == src_sql:
                    tgt_sql = item.get("tgt_sql") or item.get("cn_sql", tgt_sql)
                    stats["success"] += 1
                    flag = True
                    break
            if not flag:
                print(
                    f"\n[Fail] db_id={db_id!r}: execution mismatch\n"
                    f" (gold={_sql_preview(str(src_res))}, translated={_sql_preview(str(tgt_res))})\n"
                    f" (gold_sql={src_sql},\n translated_sql={tgt_sql})"
                )
                manual_key = (db_id, src_sql)
                manual_key = (db_id, src_sql)
                if manual_key in manual_replace_map:
                    manual_tgt_sql = manual_replace_map[manual_key]
                    manual_res = execute_query(
                        os.path.join(tgt_db_dir, db_id, f"{db_id}.sqlite"),
                        manual_tgt_sql, encoding=tgt_encoding,
                        timeout=execute_timeout,
                    )
                    manual_timeout = manual_res == "Error: timeout"
                    if (not timeout_src and not manual_timeout
                            and manual_res is not None
                            and src_res == manual_res):
                        tgt_sql = manual_tgt_sql
                        stats["manual_success"] += 1
                        print(
                            f"[Manual Success] db_id={db_id!r}: manual replacement succeeded"
                            f" ({manual_tgt_sql})"
                        )
                    elif is_structure_match(src_res, manual_res):
                        tgt_sql = manual_tgt_sql
                        stats["manual_warning"] += 1
                        print(
                            f"[Manual Warning] db_id={db_id!r}: manual replacement structure matches"
                            f" ({manual_tgt_sql})"
                        )
                    else:
                        stats["manual_fail"] += 1
                        print(
                            f"[Manual Fail] db_id={db_id!r}: manual replacement also failed"
                            f" (manual_res={_sql_preview(str(manual_res))},"
                            f" manual_sql={manual_tgt_sql})"
                        )
                else:
                    stats["fail"] += 1

        tgt_sql = _one_line_sql(tgt_sql)
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
    print(f"[Step 4] Done ({arrow}). "
          f"Success: {stats['success']}, Warning: {stats['warning']}, Fail: {stats['fail']}, "
          f"Manual Success: {stats['manual_success']}, Manual Warning: {stats['manual_warning']}, "
          f"Manual Fail: {stats['manual_fail']}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Unified database + SQL translation pipeline (EN↔CN).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Example (full pipeline):
  python database_translate.py \\
      --dataset spider \\
      --source-dir dataset/Spider/spider_enq_end \\
      --output-dir dataset/Spider/spider_cndb \\
      --replacements-config intermediate_data/replacements/spider.json \\
      --direction en2cn

Example (SQL only, reuse existing replacements and translated DBs):
  python database_translate.py \\
      --dataset spider \\
      --source-dir dataset/Spider/spider_enq_end \\
      --output-dir dataset/Spider/spider_cndb \\
      --replacements-config intermediate_data/replacements/spider.json \\
      --skip-prompts --skip-llm --skip-db-translate
""",
    )

    # --- required ---
    parser.add_argument("--dataset", required=True,
                        help="Dataset name (for config lookup)")
    parser.add_argument("--source-dir", required=True,
                        help="Source dataset directory (database/ + tables.json + dev.json)")
    parser.add_argument("--output-dir", required=True,
                        help="Output directory (translated DBs, tables.json, dev.json, dev_gold.sql)")
    parser.add_argument("--replacements-config", required=True,
                        help="Path for the replacements config JSON (created by step 2, used by steps 3–4)")

    # --- translation ---
    parser.add_argument("--direction", default=None, choices=["en2cn", "cn2en"],
                        help="Translation direction (default: from dataset config)")

    # --- prompt generation (step 1) ---
    parser.add_argument("--prompts-dir", default=None,
                        help="Intermediate prompts directory (default: <output-dir>/../intermediate/prompts)")
    parser.add_argument("--skip-content-if-unique-above", type=int, default=1000, metavar="N",
                        help="Skip content translation when unique values > N (default: 1000)")
    parser.add_argument("--content-chunk-size", type=int, default=100, metavar="K",
                        help="Max values per content prompt (default: 100)")
    parser.add_argument("--force", action="store_true",
                        help="Delete existing prompt JSON files before regenerating step 1")

    # --- LLM (step 2) ---
    parser.add_argument("--model", default="qwen-plus",
                        help="LLM model name (default: qwen-plus)")
    parser.add_argument("--workers", type=int, default=10,
                        help="Max concurrent LLM requests (default: 10)")
    parser.add_argument("--api-key", default=None,
                        help="API key (or set OPENAI_API_KEY)")
    parser.add_argument("--api-base", default=None,
                        help="API base URL (or set OPENAI_BASE_URL)")

    # --- DB translation (step 3) ---
    parser.add_argument("--values-only", action="store_true",
                        help="Only update cell values; skip column/table renames (for BULL)")

    # --- SQL translation (step 4) ---
    parser.add_argument("--split", default="dev", choices=["dev", "train", "test"],
                        help="Data split to translate (default: dev)")
    parser.add_argument("--manual-sql", default=None,
                        help="Optional manual SQL overrides JSON")
    parser.add_argument("--manual-replace-sql", default=None,
                        help="Manual replacement SQL JSON (list of {db_id, gold_sql, translated_sql})")
    parser.add_argument("--execute-timeout", type=float, default=10,
                        help="Max seconds per SQL query execution (default: 10)")
    parser.add_argument("--sql-translator", default=None,
                        choices=["manual", "cte", "sqlglot"],
                        help="SQL translator backend: 'manual' (regex pipeline, "
                             "default), 'cte' (CTE-aware regex, writes "
                             "new_<split>.json), or 'sqlglot' (AST-based, writes "
                             "<split>_sqlglot.json / <split>_sqlglot_gold.sql)")
    parser.add_argument("--sql-translate-CTE", default="false",
                        choices=["true", "false"],
                        help="[Deprecated: use --sql-translator cte] Use the "
                             "CTE-aware SQL translator and write "
                             "new_<split>.json / new_<split>_gold.sql (default: false)")
    parser.add_argument(
        "--schema-missing-policy",
        default="fail",
        choices=["fail", "skip"],
        help=(
            "How to handle db_id values missing from source/target tables.json "
            "during Step 4 preflight (default: fail)."
        ),
    )

    # --- step control ---
    parser.add_argument("--skip-prompts", action="store_true",
                        help="Skip step 1 (prompt generation)")
    parser.add_argument("--skip-llm", action="store_true",
                        help="Skip step 2 (LLM batch translation)")
    parser.add_argument("--skip-db-translate", action="store_true",
                        help="Skip step 3 (SQLite DB rewriting)")
    parser.add_argument("--skip-sql-translate", action="store_true",
                        help="Skip step 4 (SQL query translation)")

    args = parser.parse_args()

    cfg = get_config(args.dataset)
    direction = args.direction or cfg.translate_direction
    prompts_dir = args.prompts_dir or os.path.join(
        os.path.dirname(os.path.abspath(args.output_dir)),
        "intermediate", "prompts",
    )

    arrow = "EN→CN" if direction == "en2cn" else "CN→EN"
    print(f"=== Database + SQL Translation Pipeline ({arrow}) ===")
    print(f"  Dataset:      {args.dataset}")
    print(f"  Source:       {args.source_dir}")
    print(f"  Output:       {args.output_dir}")
    print(f"  Replacements: {args.replacements_config}")
    print(f"  Split:        {args.split}")
    print()

    # Step 1
    if not args.skip_prompts:
        step_generate_prompts(
            source_dir=args.source_dir,
            prompts_dir=prompts_dir,
            direction=direction,
            skip_content_if_unique_above=args.skip_content_if_unique_above,
            content_chunk_size=args.content_chunk_size,
            values_only=args.values_only,
            force=args.force,
        )
    else:
        print("[Step 1] Skipped (--skip-prompts)")

    # Step 2
    if not args.skip_llm:
        step_llm_batch(
            prompts_dir=prompts_dir,
            output_config=args.replacements_config,
            model=args.model,
            workers=args.workers,
            api_key=args.api_key,
            api_base=args.api_base,
        )
    else:
        print("[Step 2] Skipped (--skip-llm)")

    # Step 3
    if not args.skip_db_translate:
        step_translate_sqlite(
            source_dir=args.source_dir,
            output_dir=args.output_dir,
            replacements_config_path=args.replacements_config,
            values_only=args.values_only,
        )
    else:
        print("[Step 3] Skipped (--skip-db-translate)")

    # Step 4
    if not args.skip_sql_translate:
        translator = args.sql_translator or (
            "cte" if getattr(args, "sql_translate_CTE", "false") == "true"
            else "manual"
        )
        step_translate_sql(
            dataset=args.dataset,
            source_dir=args.source_dir,
            target_dir=args.output_dir,
            replacements_path=args.replacements_config,
            output_dir=args.output_dir,
            direction=direction,
            split=args.split,
            manual_sql=args.manual_sql,
            manual_replace_sql=args.manual_replace_sql,
            execute_timeout=args.execute_timeout,
            schema_missing_policy=args.schema_missing_policy,
            translator=translator,
        )
    else:
        print("[Step 4] Skipped (--skip-sql-translate)")

    print("\n=== Pipeline complete ===")


if __name__ == "__main__":
    main()
