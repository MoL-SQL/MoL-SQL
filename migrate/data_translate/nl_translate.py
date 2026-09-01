#!/usr/bin/env python3
"""
Translate natural-language questions (EN↔CN) using an LLM.

Supports both directions via ``--direction en2cn|cn2en``.  Works with
Spider, BIRD, and BULL datasets.
"""

import argparse
import json
import os
import re
import shutil
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

from tqdm import tqdm

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import STD_DB_DIR, STD_DEV_JSON_FILE, STD_DEV_SQL_FILE, STD_TABLES_FILE, get_config
from data_translate.prompts import build_nl_translate_prompt
from utils import get_llm_client


_JSON_OBJECT_RE = re.compile(r"\{.*\}", re.DOTALL)


def _parse_translated_question(text, fallback):
    """Extract ``current_question`` from an LLM response.

    Accepts raw JSON, JSON wrapped in ```json fences, or a bare string.
    Falls back to ``fallback`` (the original question) only when nothing
    usable is found.
    """
    if not text:
        return fallback

    cleaned = text.strip()
    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\s*```$", "", cleaned)
    cleaned = cleaned.strip()

    # Try: full response is valid JSON.
    try:
        obj = json.loads(cleaned)
        if isinstance(obj, dict) and "current_question" in obj:
            val = obj["current_question"]
            if isinstance(val, str) and val.strip():
                return val.strip()
    except (json.JSONDecodeError, ValueError):
        pass

    # Try: locate the first JSON-like object in the text.
    m = _JSON_OBJECT_RE.search(cleaned)
    if m:
        try:
            obj = json.loads(m.group(0))
            if isinstance(obj, dict) and "current_question" in obj:
                val = obj["current_question"]
                if isinstance(val, str) and val.strip():
                    return val.strip()
        except (json.JSONDecodeError, ValueError):
            pass

    # Last resort: treat as plain text, strip outer quotes.
    stripped = re.sub(r'^["\']|["\']\s*$', "", cleaned).strip()
    return stripped or fallback


def _pick_current_sql(entry, sql_field):
    """Return the translated (target-language) SQL stored on ``entry``."""
    for key in (sql_field, "SQL", "query", "sql_query", "sql"):
        val = entry.get(key)
        if val:
            return val
    return ""


def _pick_original_sql(entry, current_sql):
    """Return the pre-translation SQL if available, else fall back."""
    return entry.get("original_sql") or current_sql


def translate_question(
    client, original_sql, original_question, current_sql, model, direction, prompt_style, no_sql,
):
    prompt = build_nl_translate_prompt(
        direction=direction,
        original_sql=original_sql,
        original_question=original_question,
        current_sql=current_sql,
        prompt_style=prompt_style,
        no_sql=no_sql,
    )
    try:
        resp = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
            max_tokens=512,
        )
        text = (resp.choices[0].message.content or "").strip()
        return _parse_translated_question(text, fallback=original_question)
    except Exception as e:
        return f"[Translate Error: {e}]"


def process_single_entry(
    client, idx, entry, model, direction, sql_field, no_sql=False, prompt_style="default",
):
    original_question = entry.get("question", "")
    if not original_question:
        return idx, entry

    current_sql = "" if no_sql else _pick_current_sql(entry, sql_field)
    original_sql = "" if no_sql else _pick_original_sql(entry, current_sql)

    translated = translate_question(
        client, original_sql, original_question, current_sql, model, direction, prompt_style, no_sql,
    )
    new_entry = {**entry, "question": translated}
    if direction == "en2cn":
        new_entry["question_toks"] = list(translated)
    else:
        new_entry["question_toks"] = translated.split()
    return idx, new_entry


def _is_error_question(question):
    return isinstance(question, str) and question.startswith("[Translate Error:")


def write_outputs(output_data, output_json, output_gold, sql_field):
    """Write the translated dev JSON and gold SQL file (original order preserved)."""
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    gold_lines = []
    for entry in output_data:
        sql = (
            entry.get(sql_field)
            or entry.get("SQL")
            or entry.get("query")
            or entry.get("sql_query", "")
        )
        db_id = entry.get("db_id") or entry.get("db_name", "")
        gold_lines.append(f"{sql}\t{db_id}\n")
    with open(output_gold, "w", encoding="utf-8") as f:
        f.writelines(gold_lines)


def save_checkpoint(output_data, done, output_json, output_gold, progress_file, sql_field):
    """Persist the current (partial) results plus the set of completed indices."""
    write_outputs(output_data, output_json, output_gold, sql_field)
    with open(progress_file, "w", encoding="utf-8") as f:
        json.dump(sorted(done), f)


def sync_static_dataset_artifacts(source_dir, output_dir):
    """Mirror the non-translated artifacts from ``source_dir`` into ``output_dir``.

    - ``tables.json`` is copied (so the translated variant can be edited
      independently).
    - ``database/`` is exposed via a relative symlink pointing at the
      resolved source directory, to avoid duplicating large DB files.
    """
    os.makedirs(output_dir, exist_ok=True)

    src_tables = os.path.join(source_dir, STD_TABLES_FILE)
    dst_tables = os.path.join(output_dir, STD_TABLES_FILE)
    if os.path.isfile(src_tables):
        shutil.copy2(src_tables, dst_tables)
    else:
        print(f"[warn] {src_tables} not found; skipping tables.json copy")

    src_db = os.path.join(source_dir, STD_DB_DIR)
    dst_db = os.path.join(output_dir, STD_DB_DIR)
    if os.path.islink(src_db) or os.path.isdir(src_db):
        if os.path.islink(dst_db) or os.path.isfile(dst_db):
            os.remove(dst_db)
        elif os.path.isdir(dst_db):
            shutil.rmtree(dst_db)
        real_src_db = os.path.realpath(src_db)
        rel_target = os.path.relpath(real_src_db, start=os.path.abspath(output_dir))
        os.symlink(rel_target, dst_db)
    else:
        print(f"[warn] {src_db} not found; skipping database symlink")


def main():
    parser = argparse.ArgumentParser(description="Translate NL questions (EN↔CN).")
    parser.add_argument("--dataset", required=True, help="Dataset name (for config: sql_field, direction)")
    # Keep backward compatibility with previous --dataset-dir callers while
    # following the source-dir/output-dir style used by pipeline scripts.
    parser.add_argument(
        "--source-dir",
        dest="source_dir",
        required=True,
        help="Preprocessed source dataset directory",
    )
    parser.add_argument("--output-dir", required=True, help="Output dataset directory")
    parser.add_argument("--direction", default=None, choices=["en2cn", "cn2en"],
                        help="Translation direction (default: from dataset config)")
    # Accepted for CLI compatibility with other translation scripts.
    parser.add_argument("--split", default=None, help="Unused compatibility argument")
    parser.add_argument("--replacements", default=None, help="Unused compatibility argument")
    parser.add_argument("--model", default=None,
                        help="LLM model (default: env NL_TRANSLATE_MODEL or qwen-plus)")
    parser.add_argument("--workers", type=int, default=10, help="Max concurrent LLM requests")
    parser.add_argument("--api-key", default=None)
    parser.add_argument("--api-base", default=None)
    parser.add_argument(
        "--prompt-style",
        "--prompt_style",
        dest="prompt_style",
        default="default",
        help='Prompt style for NL translation (e.g. "Kaggle", "LogicCat", "TACO", "EHRSQL", "Spider", "BIRD", "BULL")',
    )
    parser.add_argument(
        "--no-sql",
        action="store_true",
        help="Do not include SQL context in NL translation prompts",
    )
    args = parser.parse_args()

    cfg = get_config(args.dataset)
    direction = args.direction or cfg.translate_direction
    model = args.model or os.environ.get("NL_TRANSLATE_MODEL", "qwen-plus")
    client = get_llm_client(api_key=args.api_key, base_url=args.api_base)

    input_json = os.path.join(args.source_dir, STD_DEV_JSON_FILE)
    output_json = os.path.join(args.output_dir, STD_DEV_JSON_FILE)
    output_gold = os.path.join(args.output_dir, STD_DEV_SQL_FILE)
    os.makedirs(args.output_dir, exist_ok=True)
    sync_static_dataset_artifacts(args.source_dir, args.output_dir)

    with open(input_json, "r", encoding="utf-8") as f:
        dev_data = json.load(f)

    progress_file = output_json + ".progress"
    save_every = 100

    # Initialise the output buffer in original order. Untranslated slots keep
    # the original entry so any partial save is still well-formed.
    output_data = [dict(entry) for entry in dev_data]
    done = set()

    # Resume from a previous (partial) run if a matching checkpoint exists.
    if os.path.exists(output_json) and os.path.exists(progress_file):
        try:
            with open(output_json, "r", encoding="utf-8") as f:
                existing = json.load(f)
            with open(progress_file, "r", encoding="utf-8") as f:
                prev_done = set(json.load(f))
            if len(existing) == len(dev_data):
                for i in prev_done:
                    if 0 <= i < len(output_data):
                        output_data[i] = existing[i]
                        done.add(i)
                print(f"Resuming: {len(done)} of {len(dev_data)} entries already translated.")
            else:
                print("Existing output length mismatch; starting fresh.")
        except (json.JSONDecodeError, ValueError, OSError) as e:
            print(f"Could not load checkpoint ({e}); starting fresh.")

    todo = [idx for idx in range(len(dev_data)) if idx not in done]

    if todo:
        completed_since_save = 0
        with ThreadPoolExecutor(max_workers=args.workers) as executor:
            futures = {
                executor.submit(
                    process_single_entry, client, idx, dev_data[idx], model, direction,
                    cfg.sql_field, args.no_sql, args.prompt_style,
                ): idx
                for idx in todo
            }
            for future in tqdm(as_completed(futures), total=len(futures), desc="Translating questions"):
                idx, new_entry = future.result()
                output_data[idx] = new_entry
                # Only mark as done when not an error, so errors are retried on resume.
                if not _is_error_question(new_entry.get("question", "")):
                    done.add(idx)
                completed_since_save += 1
                if completed_since_save >= save_every:
                    save_checkpoint(output_data, done, output_json, output_gold, progress_file, cfg.sql_field)
                    completed_since_save = 0

    # Final save (full, in original order).
    save_checkpoint(output_data, done, output_json, output_gold, progress_file, cfg.sql_field)

    print(f"Written {output_json} and {output_gold} ({len(output_data)} entries, {len(done)} translated).")


if __name__ == "__main__":
    main()
