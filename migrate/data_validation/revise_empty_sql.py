#!/usr/bin/env python3
"""
Revise gold samples whose SQL returns an EMPTY result set.

Pipeline position
-----------------
This is "step 0" of ``data_validation_revise.sh``. It consumes:

  * the original split JSON (e.g. ``.../spider_cnq_end/dev.json``), and
  * the per-sample execution record emitted by
    ``script/data_preprocess/check_empty_sql.py`` (``--output-sample-json``).

For every sample whose ``exec_status == "empty"`` it builds the
``REVISE_EMPTY_SQL_PROMPT`` (schema + random sample rows + question + the
empty-returning SQL) and asks the LLM to revise the *question and the SQL
together* so the SQL returns a non-empty result while staying mutually
consistent. Non-empty / errored / skipped samples are passed through
unchanged.

The output is a full revised split (``<split>_revised_1.json``) that the rest
of the revise pipeline (step 1+) treats as its input split.
"""

import argparse
import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Tuple

from tqdm import tqdm

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from data_validation.prompt import REVISE_EMPTY_SQL_PROMPT
from utils import get_llm_client, parse_llm_json, qwen_thinking_kwargs
from text2sql_exp.text2sql import get_db_path, get_sample_rows, get_sql_style_schema

EMPTY_STATUS = "empty"


def build_schema_desc(db_path: str, sample_rows: int) -> str:
    """CREATE TABLE DDL plus random sample rows per table."""
    sql_schema = get_sql_style_schema(db_path)
    if not sql_schema:
        return ""
    samples = get_sample_rows(
        db_path,
        max_rows_per_table=sample_rows,
        random_rows=True,
    )
    if samples:
        sql_schema += (
            f"\n\n## Sample data (random {sample_rows} rows per table)\n\n"
            f"{samples}"
        )
    return sql_schema


def build_revise_prompt(schema: str, question: str, sql: str) -> str:
    return REVISE_EMPTY_SQL_PROMPT.format(schema=schema, nl=question, sql=sql)


def revise_one(
    index: int,
    entry: dict,
    api_client,
    model: str,
    max_tokens: int,
) -> Tuple[int, dict]:
    prompt = entry.get("prompt", "")
    base = {
        # Record the sample's position in the dataset (carried on ``entry``),
        # not the positional id within the empty-sample batch, so the revision
        # is applied back to the correct row.
        "index": entry.get("index", index),
        "db_id": entry.get("db_id", ""),
        "question": entry.get("question", ""),
        "original_sql": entry.get("original_sql", ""),
    }
    if not prompt:
        return (index, {**base, "revised_question": "", "revised_sql": "",
                        "reasoning": "", "raw": "-- Error: empty prompt"})
    try:
        resp = api_client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
            max_tokens=max_tokens,
            **qwen_thinking_kwargs(model),
        )
        content = (resp.choices[0].message.content or "").strip()
        parsed = parse_llm_json(content, context_info=f"index {index}")
        result = {
            **base,
            "reasoning": (parsed or {}).get("reasoning", ""),
            "revised_question": (parsed or {}).get("revised_question", ""),
            "revised_sql": (parsed or {}).get("revised_sql", ""),
        }
        if not parsed:
            result["raw"] = content
        return (index, result)
    except Exception as e:  # noqa: BLE001
        return (index, {**base, "revised_question": "", "revised_sql": "",
                        "reasoning": "", "raw": f"-- Error: {e}"})


def load_json_list(path: str, label: str) -> list:
    if not os.path.isfile(path):
        print(f"{label} file not found: {path}", file=sys.stderr)
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        print(f"Expected a JSON list in {path}", file=sys.stderr)
        sys.exit(1)
    return data


def empty_indices_from_check(check_records: list) -> set:
    """Collect dataset indices whose execution status is 'empty'."""
    indices = set()
    for position, rec in enumerate(check_records):
        if str(rec.get("exec_status", "")).strip().lower() != EMPTY_STATUS:
            continue
        idx = rec.get("index", position)
        try:
            indices.add(int(idx))
        except (TypeError, ValueError):
            continue
    return indices


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Revise empty-result gold samples (question + SQL together) with an LLM")
    parser.add_argument("--dataset", required=True,
                        help="Original split JSON (e.g. .../spider_cnq_end/dev.json)")
    parser.add_argument("--check-sql-input", required=True,
                        help="Per-sample execution record JSON from check_empty_sql.py "
                             "(--output-sample-json)")
    parser.add_argument("--output", required=True,
                        help="Output revised split JSON path (e.g. dev_revised_1.json)")
    parser.add_argument("--db_base_dir", required=True,
                        help="DB base dir holding <db_dir>/<db_id>/<db_id>.sqlite")
    parser.add_argument("--db_dir", default="database",
                        help="DB subdir name relative to db_base_dir (default: database)")
    parser.add_argument("--sql_field", default="query",
                        help="Dataset field holding the SQL (default: query)")
    parser.add_argument("--limit", type=int, default=None,
                        help="Only process the first N samples (must match the check input)")
    parser.add_argument("--sample_rows", type=int, default=3,
                        help="Random sample rows per table in the prompt (default: 3)")
    parser.add_argument("--workers", type=int, default=5)
    parser.add_argument("--max_tokens", type=int, default=2048)
    parser.add_argument("--model", type=str, default="qwen-plus")
    parser.add_argument("--api_key", type=str, default=None)
    parser.add_argument("--api_base", type=str, default=None)
    parser.add_argument("--prompts_output", type=str, default=None,
                        help="Optional path to dump the per-empty-sample prompts as JSON")
    parser.add_argument("--results_output", type=str, default=None,
                        help="Optional path to dump the raw LLM revision results as JSON")
    args = parser.parse_args()

    examples = load_json_list(args.dataset, "Dataset")
    check_records = load_json_list(args.check_sql_input, "Check-SQL")

    if args.limit is not None:
        examples = examples[: args.limit]

    empty_idx = empty_indices_from_check(check_records)
    empty_idx = {i for i in empty_idx if 0 <= i < len(examples)}

    if not empty_idx:
        print("[revise_empty_sql] no empty-result samples found; "
              "writing the split through unchanged.", file=sys.stderr)

    # Build prompts only for the empty-result samples.
    entries = []
    schema_cache: dict = {}
    for idx in tqdm(sorted(empty_idx), desc="Building revise prompts"):
        ex = examples[idx]
        question = ex.get("question", "")
        db_id = ex.get("db_id") or ex.get("db_name", "")
        sql = ex.get(args.sql_field) or ex.get("query") or ex.get("SQL", "")
        db_path = get_db_path(args.db_base_dir, db_id, db_subdir=args.db_dir)
        if db_id not in schema_cache:
            schema_cache[db_id] = build_schema_desc(db_path, args.sample_rows)
        schema = schema_cache[db_id]
        prompt = build_revise_prompt(schema, question, sql) if schema else ""
        entries.append({
            "index": idx,
            "db_id": db_id,
            "question": question,
            "original_sql": sql,
            "prompt": prompt,
        })

    if args.prompts_output:
        os.makedirs(os.path.dirname(args.prompts_output) or ".", exist_ok=True)
        with open(args.prompts_output, "w", encoding="utf-8") as f:
            json.dump(entries, f, ensure_ascii=False, indent=2)
        print(f"[revise_empty_sql] wrote {len(entries)} prompts -> {args.prompts_output}",
              file=sys.stderr)

    results = [None] * len(entries)
    if entries:
        api_client = get_llm_client(api_key=args.api_key, base_url=args.api_base)
        with ThreadPoolExecutor(max_workers=args.workers) as executor:
            futures = {
                executor.submit(revise_one, i, entry, api_client, args.model,
                                args.max_tokens): i
                for i, entry in enumerate(entries)
            }
            for future in tqdm(as_completed(futures), total=len(futures),
                               desc="Revising empty SQL"):
                pos, res = future.result()
                results[pos] = res

    if args.results_output:
        os.makedirs(os.path.dirname(args.results_output) or ".", exist_ok=True)
        with open(args.results_output, "w", encoding="utf-8") as f:
            json.dump([r for r in results if r is not None], f,
                      ensure_ascii=False, indent=2)
        print(f"[revise_empty_sql] wrote {len(results)} revision results "
              f"-> {args.results_output}", file=sys.stderr)

    # Apply revisions back onto the full split (in dataset order).
    revised_q = 0
    revised_sql = 0
    for res in results:
        if not res:
            continue
        idx = res.get("index")
        if not isinstance(idx, int) or not (0 <= idx < len(examples)):
            continue
        entry = examples[idx]
        new_q = (res.get("revised_question") or "").strip()
        new_sql = (res.get("revised_sql") or "").strip()
        if new_q and new_q != str(entry.get("question", "")).strip():
            entry["question"] = new_q
            revised_q += 1
        if new_sql and new_sql != str(entry.get(args.sql_field, "")).strip():
            entry[args.sql_field] = new_sql
            revised_sql += 1

    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(examples, f, ensure_ascii=False, indent=2)

    print(
        f"[revise_empty_sql] wrote {len(examples)} samples to {args.output} "
        f"(empty={len(empty_idx)}, revised_question={revised_q}, "
        f"revised_sql={revised_sql})",
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()
