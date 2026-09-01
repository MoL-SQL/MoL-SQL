#!/usr/bin/env python3
"""
LLM-based gold-SQL bug detector for a subset of a Spider-style dev split.

For each example we build the ``NL2SQL_BUGS_PROMPT`` from the database schema,
random sample rows per table, the natural-language question, the (empty)
evidence, and the dataset's gold SQL, then ask the LLM to judge whether the
SQL is correct (True/False) and, if not, classify the error according to the
prompt's taxonomy.

Mirrors the conventions of ``script/text2sql_exp/generate_prompts.py`` +
``call_llm.py`` (schema + sample rows from the live sqlite DB, threaded LLM
calls, resumable output).
"""

import argparse
import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Tuple

from tqdm import tqdm

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from data_validation.prompt import NL2SQL_BUGS_PROMPT
from utils import execute_query, get_llm_client, parse_llm_json, qwen_thinking_kwargs
from text2sql_exp.text2sql import get_db_path, get_sample_rows, get_sql_style_schema

MAX_EXEC_RESULT_CHARS = 200


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


def run_gold_sql(db_path: str, sql: str) -> str:
    """Execute *sql* and return a compact result string for the prompt.

    On error, return the error message. On success, return the rows truncated
    to ``MAX_EXEC_RESULT_CHARS`` characters.
    """
    if not sql:
        return "Error: empty SQL"
    result = execute_query(db_path, sql)
    if isinstance(result, str):
        # ``execute_query`` returns an "Error: ..." string on failure.
        return result
    text = str(result)
    if len(text) > MAX_EXEC_RESULT_CHARS:
        text = text[:MAX_EXEC_RESULT_CHARS] + " ... (truncated)"
    return text


def build_debug_prompt(schema: str, question: str, sql: str,
                       exec_result: str = "None",
                       evidence: str = "None") -> str:
    """Fill the bug-detection template (the example's ``{{ }}`` collapse here)."""
    return NL2SQL_BUGS_PROMPT.format(
        schema=schema,
        nl=question,
        evidence=evidence or "None",
        sql=sql,
        exec_result=exec_result or "None",
    )


def debug_one(
    index: int,
    entry: dict,
    api_client,
    model: str,
    max_tokens: int,
) -> Tuple[int, dict]:
    prompt = entry.get("prompt", "")
    base = {
        "index": index,
        "db_id": entry.get("db_id", ""),
        "question": entry.get("question", ""),
        "gold_sql": entry.get("gold_sql", ""),
    }
    if not prompt:
        return (index, {**base, "result": None, "error_types": [],
                        "reasoning": "", "revised_sql": "",
                        "raw": "-- Error: empty prompt"})
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
            "result": (parsed or {}).get("result"),
            "error_types": (parsed or {}).get("error_types", []),
            "reasoning": (parsed or {}).get("reasoning", ""),
            "revised_sql": (parsed or {}).get("revised_sql", ""),
        }
        # Only keep the raw response when parsing failed (for debugging).
        if not parsed:
            result["raw"] = content
        return (index, result)
    except Exception as e:
        return (index, {**base, "result": None, "error_types": [],
                        "reasoning": "", "revised_sql": "",
                        "raw": f"-- Error: {e}"})


def main():
    parser = argparse.ArgumentParser(
        description="Detect bugs in gold SQL for a Spider-style dev subset")
    parser.add_argument("--dataset_dir", type=str,
                        default="dataset/Spider/spider_origin",
                        help="Dataset root holding <split>.json")
    parser.add_argument("--db_base_dir", type=str, default=None,
                        help="DB base dir (default: dataset_dir)")
    parser.add_argument("--split", type=str, default="dev",
                        help="Split basename for the questions JSON")
    parser.add_argument("--db_dir", type=str, default="database",
                        help="DB subdir name relative to db_base_dir")
    parser.add_argument("--sql_field", type=str, default="query",
                        help="JSON field holding the gold SQL")
    parser.add_argument("--limit", type=int, default=20,
                        help="Process only the first N examples (subset)")
    parser.add_argument("--sample_rows", type=int, default=3,
                        help="Random sample rows per table in the prompt")
    parser.add_argument("--workers", type=int, default=5)
    parser.add_argument("--max_tokens", type=int, default=2048)
    parser.add_argument("--model", type=str, default="qwen-plus")
    parser.add_argument("--api_key", type=str, default=None)
    parser.add_argument("--api_base", type=str, default=None)
    parser.add_argument("--output", type=str, default=None,
                        help="Output JSON path (default: auto-generated)")
    parser.add_argument("--prompts_dir", type=str, default=None,
                        help="Directory for prompt JSON "
                             "(default: intermediate_data/prompts/"
                             "<dataset_basename>/nl2sql_debug)")
    parser.add_argument("--prompts_output", type=str, default=None,
                        help="Prompt JSON path (overrides --prompts_dir)")
    args = parser.parse_args()

    db_base_dir = args.db_base_dir or args.dataset_dir
    dev_path = os.path.join(args.dataset_dir, f"{args.split}.json")
    if not os.path.isfile(dev_path):
        print(f"{args.split} questions file not found: {dev_path}", file=sys.stderr)
        sys.exit(1)

    with open(dev_path, "r", encoding="utf-8") as f:
        examples = json.load(f)
    if args.limit is not None:
        examples = examples[: args.limit]

    # Build per-example prompts (schema + random sample rows from sqlite DB).
    entries = []
    schema_cache: dict = {}
    for ex in tqdm(examples, desc="Building prompts"):
        question = ex.get("question", "")
        db_id = ex.get("db_id") or ex.get("db_name", "")
        gold_sql = ex.get(args.sql_field) or ex.get("query") or ex.get("SQL", "")
        db_path = get_db_path(db_base_dir, db_id, db_subdir=args.db_dir)
        if db_id not in schema_cache:
            schema_cache[db_id] = build_schema_desc(db_path, args.sample_rows)
        schema = schema_cache[db_id]
        exec_result = run_gold_sql(db_path, gold_sql)
        prompt = (build_debug_prompt(schema, question, gold_sql, exec_result)
                  if schema else "")
        entries.append({
            "index": len(entries),
            "db_id": db_id,
            "question": question,
            "gold_sql": gold_sql,
            "exec_result": exec_result,
            "prompt": prompt,
        })

    ds_tag = os.path.basename(args.dataset_dir.rstrip("/"))
    prompts_path = args.prompts_output
    if prompts_path is None:
        prompts_dir = args.prompts_dir or os.path.join(
            "intermediate_data", "prompts", ds_tag, "nl2sql_debug")
        prompts_path = os.path.join(
            prompts_dir, f"{ds_tag}_{args.split}_nl2sql_debug.json")
    os.makedirs(os.path.dirname(prompts_path) or ".", exist_ok=True)
    with open(prompts_path, "w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)
    print(f"Wrote {len(entries)} prompts to {prompts_path}", file=sys.stderr)

    out_path = args.output
    if out_path is None:
        model_tag = args.model.replace("/", "_")
        out_path = os.path.join(
            "intermediate_data", "nl2sql_debug", "spider",
            f"{ds_tag}_{args.split}_gold_debug_{model_tag}.json")
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)

    api_client = get_llm_client(api_key=args.api_key, base_url=args.api_base)

    results = [None] * len(entries)
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {
            executor.submit(debug_one, i, entry, api_client, args.model,
                            args.max_tokens): i
            for i, entry in enumerate(entries)
        }
        for future in tqdm(as_completed(futures), total=len(futures),
                           desc="Debugging gold SQL"):
            idx, res = future.result()
            results[idx] = res

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    n_false = sum(1 for r in results if r and str(r.get("result")).lower() == "false")
    print(f"Wrote {len(results)} results to {out_path} "
          f"({n_false} flagged as buggy)", file=sys.stderr)


if __name__ == "__main__":
    main()
