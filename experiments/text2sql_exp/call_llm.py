#!/usr/bin/env python3
"""
Read prompts from JSON, call LLM for each, write one SQL per line.

Unified from Spider, BIRD, and BULL ``call_llm.py`` variants.
Spider-specific normalisation (backtick-stripping + keyword lowering) is
opt-in via ``--normalize-for-spider``.
"""

import argparse
import json
import os
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Tuple

from tqdm import tqdm

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils import get_llm_client, qwen_thinking_kwargs


# ---------------------------------------------------------------------------
# Response parsing
# ---------------------------------------------------------------------------

def _strip_markdown_fence(s: str) -> str:
    if s.startswith("```"):
        s = re.sub(r"^```\w*\n?", "", s)
        s = re.sub(r"\n?```\s*$", "", s)
    return s.strip()


def _parse_label_sql(sql: str) -> str:
    """Extract SQL from the legacy ``Analysis:/SQL:`` format.

    Handles both ``SQL: <single line>`` and ``SQL:\\n<sql>`` shapes — the
    latter is the empty-tail case that previously yielded blank predictions
    (and then bare ``[Error]`` lines via the incremental-save fallback).
    """
    sql = _strip_markdown_fence(sql)
    m = re.search(r"(?im)^\s*SQL\s*:\s*(.*)$", sql)
    if not m:
        return sql.strip()
    rest = m.group(1).strip()
    if rest:
        return rest
    tail = sql[m.end():].lstrip("\n").strip()
    if not tail:
        return ""
    # Take the first non-blank line of the trailing block.
    for line in tail.splitlines():
        line = line.strip()
        if line:
            return line
    return ""


def parse_response_to_sql(content: str, style: str = "label") -> str:
    """Extract the SQL string from a raw LLM response.

    Parameters
    ----------
    content : str
        Raw response text from the model.
    style : str
        ``"xml"``  -> prefer ``<sql>...</sql>`` (case-insensitive, multi-line).
        ``"label"`` -> legacy ``SQL:`` extraction.
        Either style falls back to the other if its primary pattern is
        absent, so the parser is robust to mild format drift.
    """
    sql = (content or "").strip()
    if not sql:
        return ""

    if style == "xml":
        m = re.search(r"<sql\b[^>]*>(.*?)</sql\s*>",
                      sql, flags=re.IGNORECASE | re.DOTALL)
        if m:
            inner = m.group(1).strip()
            inner = _strip_markdown_fence(inner)
            return inner.strip().strip("`").strip()
        # Model ignored the XML envelope — fall through to label parsing.
    return _parse_label_sql(sql)


def to_single_line(s: str) -> str:
    return " ".join((s or "").split())


def normalize_sql_for_spider(sql: str) -> str:
    """Strip backticks and lowercase keywords for Spider evaluation."""
    if not sql or sql.startswith("--"):
        return sql
    sql = re.sub(r"`([a-zA-Z0-9_]+)`", r"\1", sql)
    keywords = (
        r"\b(SELECT|FROM|WHERE|GROUP|BY|ORDER|ASC|DESC|LIMIT|OFFSET|"
        r"JOIN|LEFT|RIGHT|INNER|OUTER|ON|AS|AND|OR|NOT|IN|IS|NULL|"
        r"COUNT|SUM|AVG|MIN|MAX|DISTINCT|HAVING|UNION|INTERSECT|EXCEPT)\b"
    )
    sql = re.sub(keywords, lambda m: m.group(1).lower(), sql, flags=re.IGNORECASE)
    return sql.strip()


# ---------------------------------------------------------------------------
# Single-entry LLM call
# ---------------------------------------------------------------------------

def _resolve_style(entry: dict, cli_style: str) -> str:
    """Pick a response style: explicit CLI override > per-entry > 'label'."""
    if cli_style in ("label", "xml"):
        return cli_style
    style = entry.get("output_style")
    if isinstance(style, str) and style in ("label", "xml"):
        return style
    return "label"


def call_llm_one(
    index: int,
    entry: dict,
    api_client,
    model: str,
    max_tokens: int = 4096,
    normalize_for_spider: bool = False,
    output_style: str = "auto",
    max_retries: int = 3,
    retry_backoff: float = 2.0,
) -> Tuple[int, str, str]:
    prompt = entry.get("prompt", "")
    if not prompt:
        return (index, "-- Error: empty prompt", "")
    for attempt in range(max_retries + 1):
        try:
            resp = api_client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.0,
                max_tokens=max_tokens,
                **qwen_thinking_kwargs(model),
            )
            content = (resp.choices[0].message.content or "").strip()
            style = _resolve_style(entry, output_style)
            sql = parse_response_to_sql(content, style=style)
            sql = to_single_line(sql)
            if normalize_for_spider and sql and not sql.startswith("--"):
                sql = normalize_sql_for_spider(sql)
            return (index, sql, content)
        except Exception as e:
            if attempt >= max_retries:
                return (index, f"-- Error: {e}", "")
            time.sleep(retry_backoff * (2 ** attempt))
    return (index, "-- Error: retry loop exhausted", "")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Call LLM with prompts, write SQL predictions")
    parser.add_argument("--input", type=str, required=True, help="Input prompt JSON")
    parser.add_argument("--output", type=str, required=True, help="Output predictions .txt")
    parser.add_argument("--model", type=str, default="qwen-plus", help="Model name")
    parser.add_argument("--end_index", type=int, default=None)
    parser.add_argument("--workers", type=int, default=10)
    parser.add_argument("--max_tokens", type=int, default=4096)
    parser.add_argument("--save_interval", type=int, default=20)
    parser.add_argument("--max_retries", type=int, default=3)
    parser.add_argument("--retry_backoff", type=float, default=2.0)
    parser.add_argument("--normalize-for-spider", action="store_true",
                        help="Strip backticks + lowercase keywords (Spider eval)")
    parser.add_argument("--output_style", type=str, default="auto",
                        choices=["auto", "label", "xml"],
                        help="Response parser style. 'auto' reads each entry's "
                             "'output_style' field (falling back to 'label').")
    parser.add_argument("--api_key", type=str, default=None)
    parser.add_argument("--api_base", type=str, default=None)
    args = parser.parse_args()

    if not os.path.isfile(args.input):
        print(f"Input not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    with open(args.input, "r", encoding="utf-8") as f:
        entries = json.load(f)

    end = args.end_index if args.end_index is not None else len(entries)
    entries = entries[:end]

    api_client = get_llm_client(api_key=args.api_key, base_url=args.api_base)

    # Resume from existing output
    predictions = [None] * len(entries)
    raw_responses = [""] * len(entries)
    if os.path.isfile(args.output):
        with open(args.output, "r", encoding="utf-8") as f:
            lines = f.readlines()
        for i, line in enumerate(lines):
            if i >= len(entries):
                break
            value = line.rstrip("\n")
            if value.startswith(("-- Error:", "[Error")):
                continue
            predictions[i] = value
        loaded = sum(1 for p in predictions if p is not None)
        if loaded > 0:
            print(f"Loaded {loaded} existing predictions, skipping", file=sys.stderr)

    to_process = [(i, entries[i]) for i in range(len(entries)) if predictions[i] is None]
    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)

    if not to_process:
        print("All entries have results.", file=sys.stderr)
        with open(args.output, "w", encoding="utf-8") as f:
            for p in predictions:
                f.write(to_single_line(p or "[Error: empty response]") + "\n")
        return

    _n0 = sum(1 for p in predictions if p is not None)
    last_milestone = (_n0 // args.save_interval) * args.save_interval

    def _prefix_len():
        n = 0
        while n < len(predictions) and predictions[n] is not None:
            n += 1
        return n

    def _maybe_save():
        nonlocal last_milestone
        n = _prefix_len()
        nxt = last_milestone + args.save_interval
        if n >= nxt:
            while n >= nxt:
                last_milestone = nxt
                nxt += args.save_interval
            with open(args.output, "w", encoding="utf-8") as f:
                for j in range(n):
                    f.write(to_single_line(predictions[j] or "[Error]") + "\n")
            print(f"Incremental save: {n} predictions", file=sys.stderr)

    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {
            executor.submit(
                call_llm_one, i, entry, api_client, args.model,
                args.max_tokens, args.normalize_for_spider, args.output_style,
                args.max_retries, args.retry_backoff,
            ): i
            for i, entry in to_process
        }
        for future in tqdm(as_completed(futures), total=len(futures), desc="Calling LLM"):
            idx, sql, raw = future.result()
            predictions[idx] = sql
            raw_responses[idx] = raw or ""
            _maybe_save()

    with open(args.output, "w", encoding="utf-8") as f:
        for p in predictions:
            f.write(to_single_line(p or "[Error: empty response]") + "\n")
    print(f"Wrote {len(predictions)} predictions to {args.output}", file=sys.stderr)

    cot_pattern = re.compile(r"SQL:|<\s*cot\b|<\s*sql\b", re.IGNORECASE)
    if any(cot_pattern.search(r) for r in raw_responses):
        base, ext = os.path.splitext(args.output)
        cot_path = f"{base}_cot{ext}"
        with open(cot_path, "w", encoding="utf-8") as f:
            for i, raw in enumerate(raw_responses):
                f.write(f"========== {i} ==========\n")
                f.write(raw if raw else "(no response)")
                f.write("\n")
        print(f"Wrote CoT to {cot_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
