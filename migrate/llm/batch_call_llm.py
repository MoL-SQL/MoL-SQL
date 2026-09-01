#!/usr/bin/env python3
"""
Generic concurrent LLM caller.

Reads prompt items from a JSON file, calls an OpenAI-compatible API in
parallel, and writes results (one line per item) to an output file.

Features:
- ThreadPoolExecutor parallelism
- Resume from partial output (prefix-based)
- Incremental save every N completed entries
- CoT sidecar file when responses contain ``SQL:`` markers
- Pluggable response parser
"""

import argparse
import json
import os
import re
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Callable, Optional, Tuple

from tqdm import tqdm

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils import get_llm_client, qwen_thinking_kwargs


# ---------------------------------------------------------------------------
# Default response parser (SQL-oriented)
# ---------------------------------------------------------------------------

def default_parse_response(content: str) -> str:
    """Strip markdown code-block, extract ``SQL:`` line, single-line."""
    sql = (content or "").strip()
    if sql.startswith("```"):
        sql = re.sub(r"^```\w*\n?", "", sql)
        sql = re.sub(r"\n?```\s*$", "", sql)
        sql = sql.strip()
    if "SQL:" in sql:
        for line in sql.split("\n"):
            line = line.strip()
            if line.upper().startswith("SQL:"):
                sql = line[4:].strip()
                break
    return " ".join(sql.split())


# ---------------------------------------------------------------------------
# Core batch caller
# ---------------------------------------------------------------------------

def batch_call_llm(
    entries: list,
    api_client,
    model: str,
    output_path: str,
    max_tokens: int = 4096,
    workers: int = 10,
    save_interval: int = 20,
    prompt_key: str = "prompt",
    parse_fn: Optional[Callable[[str], str]] = None,
    post_process_fn: Optional[Callable[[str], str]] = None,
) -> list:
    """Call LLM for each entry and write results.

    Returns list of (parsed_result, raw_response) tuples, one per entry.
    """
    if parse_fn is None:
        parse_fn = default_parse_response

    def _call_one(index, entry) -> Tuple[int, str, str]:
        prompt = entry.get(prompt_key, "")
        if not prompt:
            return (index, "-- Error: empty prompt", "")
        try:
            resp = api_client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.0,
                max_tokens=max_tokens,
                **qwen_thinking_kwargs(model),
            )
            raw = (resp.choices[0].message.content or "").strip()
            parsed = parse_fn(raw)
            if post_process_fn and parsed:
                parsed = post_process_fn(parsed)
            return (index, parsed, raw)
        except Exception as e:
            return (index, f"-- Error: {e}", "")

    predictions = [None] * len(entries)
    raw_responses = [""] * len(entries)

    # Resume from existing file
    if os.path.isfile(output_path):
        with open(output_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        for i, line in enumerate(lines):
            if i >= len(entries):
                break
            predictions[i] = line.rstrip("\n")
        loaded = sum(1 for p in predictions if p is not None)
        if loaded:
            print(f"Loaded {loaded} existing results, skipping", file=sys.stderr)

    to_process = [(i, entries[i]) for i in range(len(entries)) if predictions[i] is None]
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    if not to_process:
        print("All entries have results.", file=sys.stderr)
        _write_predictions(predictions, output_path)
        return list(zip(predictions, raw_responses))

    n0 = sum(1 for p in predictions if p is not None)
    last_milestone = (n0 // save_interval) * save_interval

    def _prefix():
        n = 0
        while n < len(predictions) and predictions[n] is not None:
            n += 1
        return n

    def _save():
        nonlocal last_milestone
        n = _prefix()
        nxt = last_milestone + save_interval
        if n >= nxt:
            while n >= nxt:
                last_milestone = nxt
                nxt += save_interval
            _write_predictions(predictions[:n], output_path)
            print(f"Incremental save: {n} entries", file=sys.stderr)

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {
            executor.submit(_call_one, i, entry): i
            for i, entry in to_process
        }
        for future in tqdm(as_completed(futures), total=len(futures), desc="Calling LLM"):
            idx, parsed, raw = future.result()
            predictions[idx] = parsed
            raw_responses[idx] = raw or ""
            _save()

    _write_predictions(predictions, output_path)
    print(f"Wrote {len(predictions)} results to {output_path}", file=sys.stderr)
    return list(zip(predictions, raw_responses))


def _write_predictions(predictions, path):
    with open(path, "w", encoding="utf-8") as f:
        for p in predictions:
            f.write(" ".join((p or "[Error: empty response]").split()) + "\n")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Generic batch LLM caller")
    parser.add_argument("--input", required=True, help="Input JSON (list of dicts with 'prompt')")
    parser.add_argument("--output", required=True, help="Output file (one result per line)")
    parser.add_argument("--model", default="qwen-plus")
    parser.add_argument("--end_index", type=int, default=None)
    parser.add_argument("--workers", type=int, default=10)
    parser.add_argument("--max_tokens", type=int, default=4096)
    parser.add_argument("--save_interval", type=int, default=20)
    parser.add_argument("--prompt_key", default="prompt")
    parser.add_argument("--api_key", default=None)
    parser.add_argument("--api_base", default=None)
    args = parser.parse_args()

    if not os.path.isfile(args.input):
        print(f"Input not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    with open(args.input, "r", encoding="utf-8") as f:
        entries = json.load(f)

    end = args.end_index if args.end_index is not None else len(entries)
    entries = entries[:end]

    client = get_llm_client(api_key=args.api_key, base_url=args.api_base)
    results = batch_call_llm(
        entries, client, args.model, args.output,
        max_tokens=args.max_tokens, workers=args.workers,
        save_interval=args.save_interval, prompt_key=args.prompt_key,
    )

    # CoT sidecar
    if any("SQL:" in (r or "") for _, r in results):
        base, ext = os.path.splitext(args.output)
        cot_path = f"{base}_cot{ext}"
        with open(cot_path, "w", encoding="utf-8") as f:
            for i, (_, raw) in enumerate(results):
                f.write(f"========== {i} ==========\n")
                f.write(raw if raw else "(no response)")
                f.write("\n")
        print(f"Wrote CoT to {cot_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
