#!/usr/bin/env python3
"""
Rewrite BULL-{cn,en}-origin samples whose SQL uses ``DATE('now', ...)``.

Why
---
The BULL FinSQL databases only contain data up to the year 2022 (the largest
table date — ``lc_mainoperincome.enddate`` — tops out at ``2021-12-31``).  Many
samples nevertheless use ``DATE('now', ...)`` in their gold SQL.  Executed
today, these queries return empty result sets, which breaks downstream
evaluation.  This script anchors "now" to ``2022-12-31`` in BOTH the natural
language question (e.g. ``去年`` -> ``2022年的上一年``; ``last year`` -> ``the
year before 2022``) and the SQL (``DATE('now', ...)`` ->
``DATE('2022-12-31', ...)``).

Two language passes
-------------------
By default this script runs two independent passes:

* Chinese pass: ``BULL-cn-origin`` -> ``BULL-cn-origin-date-reset``.  An LLM
  call rewrites BOTH ``current_question`` and ``current_sql`` in a single
  response (the SQL still goes through the deterministic anchor as a safety
  net).
* English pass: ``BULL-en-origin`` -> ``BULL-en-origin-date-reset``.  The
  candidate set is index-aligned with the Chinese pass (same q_ids, same
  ``DATE('now', ...)`` positions); only the natural-language question is
  language-specific.  We therefore use a question-only English prompt (the
  LLM is told NOT to emit ``current_sql``), and the SQL is anchored
  purely deterministically by :func:`_force_anchor_sql` — this avoids any
  risk of the model perturbing English-localized literals in the SQL
  (e.g. ``'one month'``).

Either pass can be skipped via ``--skip-chinese`` / ``--skip-english``.

Scope
-----
For now this script only rewrites ``dev.json`` (and mirrors the new questions
into the per-language sidecar — ``dev_cn.json`` for the Chinese pass,
``dev_en.json`` for the English pass — by ``q_id``).  ``train.json`` is NOT
copied; train rewriting can be added later by also calling
:func:`_rewrite_split` for it.

Output layout
-------------
Each ``BULL-{cn,en}-origin-date-reset/`` mirrors its source dir:

    database/                       -> symlink to source database/
    tables.json                     copied
    db_info.json                    copied
    convert_data_format.py          copied
    dev_gold.py                     copied if present in source (cn only today)
    dev.json                        rewritten (DATE('now') entries anchored to 2022-12-31)
    dev_{cn,en}.json                rewritten (questions mirrored from dev.json)
    dev_gold.sql                    regenerated from the rewritten dev.json
    _rewrite_cache/dev_rewrites.jsonl  raw LLM responses (resumable, keyed by q_id)

``train.json`` is intentionally NOT copied — train rewriting is deferred and we
don't want a stale copy in the output dir.

Notes
-----
The pre-parsed SQL fields that ship in BULL's ``dev.json`` (``from``,
``select``, ``where``, ``groupBy``, ``having``, ``orderBy``, ``limit``) are
**stripped from every output entry**.  They were parsed from the original
SQL and would be inconsistent with the rewritten ``sql_query``; downstream
code (see ``data_preprocess.py``) only consumes ``sql_query`` anyway.

Sample order in the output ``dev.json`` is identical to the input — entries
are mutated in place by index, never re-sorted.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
from typing import Callable, Optional

from tqdm import tqdm

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils import get_llm_client  # noqa: E402


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DEFAULT_INPUT_DIR = "dataset/BULL-FinSQL/BULL-cn-origin"
DEFAULT_OUTPUT_DIR = "dataset/BULL-FinSQL/BULL-cn-origin-date-reset"

ENGLISH_INPUT_DIR = "dataset/BULL-FinSQL/BULL-en-origin"
ENGLISH_OUTPUT_DIR = "dataset/BULL-FinSQL/BULL-en-origin-date-reset"

# Anchor "now" at the end of 2022 because BULL data extends through 2022 only.
ANCHOR_DATE = "2022-12-31"
ANCHOR_YEAR = "2022"

# Matches DATE('now'... or DATE("now"... with optional spaces, case-insensitive.
# Captures the opening paren and the 'now' literal so we can splice in the
# anchor date while preserving the rest of the call (e.g. ", '-1 year')").
NOW_PATTERN = re.compile(r"DATE\s*\(\s*['\"]now['\"]", re.IGNORECASE)

# Static files copied verbatim from the input directory into the output dir.
# Missing files are skipped with a warning, so dev_gold.py (cn-only today)
# is fine to list here for both passes.
PASS_THROUGH_FILES = ("tables.json", "db_info.json", "convert_data_format.py", "dev_gold.py")
# Files we should remove from a previous output run (e.g. earlier versions of
# this script copied ``train.json`` through; we no longer want it).
STALE_OUTPUT_FILES = ("train.json",)
# Both BULL-cn-origin and BULL-en-origin expose the sqlite tree as a symlink
# named ``database`` (pointing at database_cn / database_en respectively),
# and the downstream eval (text2sql_bull.pal.sh) reads ``${VARIANT_DIR}/database``.
DB_DIR_NAME = "database"
DEV_JSON = "dev.json"
# Per-language "sidecar" file: same q_id ordering as dev.json but only the
# natural-language question (no SQL).  Chinese pass mirrors into dev_cn.json;
# English pass mirrors into dev_en.json.
DEV_LANG_SIDECAR_CN = "dev_cn.json"
DEV_LANG_SIDECAR_EN = "dev_en.json"
DEV_GOLD_SQL = "dev_gold.sql"
CACHE_DIR_NAME = "_rewrite_cache"
DEV_CACHE_FILE = "dev_rewrites.jsonl"

# BULL's dev.json ships these structural fields parsed from the original SQL.
# Because we rewrite ``sql_query``, the parsed fields go stale, so we drop
# them from every output entry (see module docstring).
STRUCTURAL_SQL_FIELDS = ("from", "select", "where", "groupBy", "having", "orderBy", "limit")


# ---------------------------------------------------------------------------
# .env autoload (no external dependency)
# ---------------------------------------------------------------------------

# Matches one variable assignment line. Supports the repo's existing
# ``export KEY="value"`` style (see code/.env / text2sql_bull.pal.sh) as well
# as plain ``KEY=value`` and single-quoted values.
_ENV_LINE_RE = re.compile(
    r"""^\s*(?:export\s+)?
        (?P<key>[A-Za-z_][A-Za-z0-9_]*)
        \s*=\s*
        (?P<val>'[^']*'|"[^"]*"|[^\s#].*?)\s*(?:\#.*)?$""",
    re.VERBOSE,
)


def _load_dotenv(start_dir: Optional[str] = None) -> Optional[str]:
    """Find the nearest ``.env`` and merge it into ``os.environ``.

    Searches the current working directory and the script's parent directories
    (walking up to filesystem root).  Existing environment variables always
    win, matching what ``source .env`` would do in a shell.  Returns the path
    that was loaded, or ``None`` if nothing was found.
    """
    candidates: list[str] = []
    cwd = os.path.abspath(start_dir or os.getcwd())
    here = os.path.abspath(os.path.dirname(__file__))
    for base in (cwd, here):
        cur = base
        while True:
            candidates.append(os.path.join(cur, ".env"))
            parent = os.path.dirname(cur)
            if parent == cur:
                break
            cur = parent

    seen: set[str] = set()
    for path in candidates:
        if path in seen or not os.path.isfile(path):
            seen.add(path)
            continue
        seen.add(path)
        with open(path, "r", encoding="utf-8") as f:
            for raw in f:
                line = raw.rstrip("\n")
                if not line.strip() or line.lstrip().startswith("#"):
                    continue
                m = _ENV_LINE_RE.match(line)
                if not m:
                    continue
                key = m.group("key")
                val = m.group("val")
                if (val.startswith('"') and val.endswith('"')) or (
                    val.startswith("'") and val.endswith("'")
                ):
                    val = val[1:-1]
                os.environ.setdefault(key, val)
        return path
    return None


# ---------------------------------------------------------------------------
# Static-file mirroring
# ---------------------------------------------------------------------------

def _mirror_static_files(input_dir: str, output_dir: str) -> None:
    """Set up the output directory: symlink the DB and copy pass-through files.

    The database directory is exposed as a relative symlink so the (large)
    sqlite files aren't duplicated.  Pass-through metadata files
    (:data:`PASS_THROUGH_FILES`) are copied so the output dir is a
    self-contained drop-in for the input.  ``train.json`` is intentionally
    NOT copied (deferred rewrite — see module docstring).
    """
    os.makedirs(output_dir, exist_ok=True)

    src_db = os.path.join(input_dir, DB_DIR_NAME)
    dst_db = os.path.join(output_dir, DB_DIR_NAME)
    if os.path.islink(dst_db) or os.path.isfile(dst_db):
        os.remove(dst_db)
    elif os.path.isdir(dst_db):
        shutil.rmtree(dst_db)
    if os.path.isdir(src_db) or os.path.islink(src_db):
        real_src_db = os.path.realpath(src_db)
        rel_target = os.path.relpath(real_src_db, start=os.path.abspath(output_dir))
        os.symlink(rel_target, dst_db)
    else:
        print(f"[warn] {src_db} not found; skipping database symlink", file=sys.stderr)

    for fname in PASS_THROUGH_FILES:
        src = os.path.join(input_dir, fname)
        dst = os.path.join(output_dir, fname)
        if not os.path.exists(src):
            print(f"[warn] {src} not found; skipping", file=sys.stderr)
            continue
        shutil.copy2(src, dst)

    # Tidy up artifacts a previous version of this script may have left
    # behind (e.g. an earlier ``train.json`` pass-through).
    for fname in STALE_OUTPUT_FILES:
        stale = os.path.join(output_dir, fname)
        if os.path.isfile(stale) or os.path.islink(stale):
            os.remove(stale)
            print(f"[clean] removed stale {stale}", file=sys.stderr)


# ---------------------------------------------------------------------------
# Prompt construction
# ---------------------------------------------------------------------------

_FEW_SHOT_EXAMPLES = [
    {
        "input": {
            "original_question": "去年哪家公司的成本最多",
            "original_sql": (
                "select chinameabbr from lc_mainoperincome  where strftime('%Y', enddate) = "
                "strftime('%Y', DATE('now', '-1 year')) order by  mainopercost desc limit 1 ;"
            ),
        },
        "output": {
            "current_question": "2022年的上一年哪家公司的成本最多",
            "current_sql": (
                "select chinameabbr from lc_mainoperincome  where strftime('%Y', enddate) = "
                "strftime('%Y', DATE('2022-12-31', '-1 year')) order by  mainopercost desc limit 1 ;"
            ),
        },
    },
    {
        "input": {
            "original_question": "我朋友最近想买股票，帮我看看近三年利润贡献超过1的公司有哪些，列出股票代码",
            "original_sql": (
                "select  secucode  from lc_mainoperincome  where strftime('%Y', enddate) > "
                "strftime('%Y', DATE('now', '-3 year')) and grossprofit >1;"
            ),
        },
        "output": {
            "current_question": "我朋友最近想买股票，帮我看看2022年的近三年利润贡献超过1的公司有哪些，列出股票代码",
            "current_sql": (
                "select  secucode  from lc_mainoperincome  where strftime('%Y', enddate) > "
                "strftime('%Y', DATE('2022-12-31', '-3 year')) and grossprofit >1;"
            ),
        },
    },
]

_PROMPT_HEADER = """你正在为一个中文 NL2SQL 数据集做"日期重设"。BULL FinSQL 数据库只覆盖到 2022 年，因此 SQL 中的 ``DATE('now', ...)`` 在今天执行会返回空结果。我们要把"现在"显式锚定到 2022 年（具体到 ``2022-12-31``），让问题与 SQL 的日期语义保持一致。

输入：
- ``original_question``: 中文自然语言问题，包含相对时间词（如 "去年" / "前一年" / "近 N 年" / "过去 N 年" / "这两年" / "近 30 天" 等）。
- ``original_sql``: 与之对应的 SQLite 查询，至少包含一个 ``DATE('now', ...)`` 或 ``DATE('now')``。

输出（只返回一个 JSON 对象 ``{"current_question": "...", "current_sql": "..."}``，不要 markdown 代码块、不要解释）：
- ``current_question``: 把相对时间词替换成显式以 2022 年为锚的表达。例如：
  * "去年" → "2022年的上一年"
  * "前一年" → "2022年的前一年"
  * "近三年" / "过去三年" → "2022年的近三年" / "2022年的过去三年"
  * "过去五年" → "2022年的过去五年"
  * "这两年" → "2022年的近两年"
  * "近 N 天" → "2022年12月31日的近 N 天"
  其余字符（表名/列名/数字/标点/空格）必须与 ``original_question`` **完全一致**，不要改写、不要加字、不要删字。
- ``current_sql``: 把每一处 ``DATE('now', ...)`` 替换为 ``DATE('2022-12-31', ...)``，把 ``DATE('now')`` 替换为 ``DATE('2022-12-31')``。其余字符（包括大小写、空格、引号、标识符、字面量、末尾分号等）必须与 ``original_sql`` **逐字符相同**。

严格要求：
1. 不要新增、删除或改写任何与日期无关的内容。
2. 不要把 ``DATE('now', ...)`` 改成其他形式（例如不要展开成具体年份再相减）；只把 ``'now'`` 替换成 ``'2022-12-31'``。
3. 不要在输出里再出现 ``'now'`` 这个字面量。
4. 直接输出 JSON，不要任何前后缀。"""


def _render_example(example: dict) -> str:
    return (
        "Input:\n"
        + json.dumps(example["input"], ensure_ascii=False, indent=2)
        + "\nOutput:\n"
        + json.dumps(example["output"], ensure_ascii=False, indent=2)
    )


def _build_prompt(original_question: str, original_sql: str) -> str:
    examples_block = "\n\n".join(_render_example(ex) for ex in _FEW_SHOT_EXAMPLES)
    current_input = json.dumps(
        {"original_question": original_question, "original_sql": original_sql},
        ensure_ascii=False,
        indent=2,
    )
    return (
        f"{_PROMPT_HEADER}\n\n"
        f"### Examples\n{examples_block}\n\n"
        f"### Current Input\n{current_input}\n\n"
        f"### Current Output (JSON only):\n"
    )


# --- English prompt (question-only) ----------------------------------------
#
# The English split is index-aligned with the Chinese split: same q_ids, same
# ``DATE('now', ...)`` positions, only the natural-language question differs.
# We therefore ask the LLM to rewrite ONLY the English question and forbid it
# from emitting a ``current_sql`` field.  The SQL is anchored deterministically
# downstream by :func:`_force_anchor_sql`, which avoids any chance of the
# model perturbing English-localized literals (e.g. ``'one month'``) that the
# Chinese split doesn't have.
#
# Few-shot examples reuse the same SQL templates as ``_FEW_SHOT_EXAMPLES`` so
# the model sees the exact ``DATE('now', '-N year')`` shape it will encounter
# in the dataset.
_FEW_SHOT_EXAMPLES_EN = [
    {
        "input": {
            "original_question": "Which company had the highest cost last year?",
            "original_sql": (
                "select chinameabbr from lc_mainoperincome  where strftime('%Y', enddate) = "
                "strftime('%Y', DATE('now', '-1 year')) order by  mainopercost desc limit 1 ;"
            ),
        },
        "output": {
            "current_question": "Which company had the highest cost in the year before 2022?",
        },
    },
    {
        "input": {
            "original_question": (
                "My friend recently wants to buy stocks. Help me check which companies "
                "have profit contributions exceeding 1 in the past three years. List the stock codes."
            ),
            "original_sql": (
                "select  secucode  from lc_mainoperincome  where strftime('%Y', enddate) > "
                "strftime('%Y', DATE('now', '-3 year')) and grossprofit >1;"
            ),
        },
        "output": {
            "current_question": (
                "My friend recently wants to buy stocks. Help me check which companies "
                "have profit contributions exceeding 1 in the three years up to 2022. List the stock codes."
            ),
        },
    },
    {
        "input": {
            "original_question": (
                "Could you please help me check the shareholders and the number of shares "
                "held by shareholders for 000948 in the past three years?"
            ),
            "original_sql": (
                "select shname, holdshares from lc_shnumber where secucode='000948' and "
                "strftime('%Y', enddate) > strftime('%Y', DATE('now', '-3 year'));"
            ),
        },
        "output": {
            "current_question": (
                "Could you please help me check the shareholders and the number of shares "
                "held by shareholders for 000948 in the three years up to 2022?"
            ),
        },
    },
]

_PROMPT_HEADER_EN = """You are doing "date reset" for an English NL2SQL dataset. The BULL FinSQL databases only cover up to year 2022, so SQL using ``DATE('now', ...)`` returns empty results when executed today. We anchor "now" explicitly to the end of 2022 (``2022-12-31``) so that the question and the SQL stay semantically aligned.

Input:
- ``original_question``: an English natural-language question containing a relative time expression (e.g. "last year" / "the previous year" / "in the past N years" / "over the past N years" / "in the past N days" / "in the fourth quarter of last year" / "the same period last year" / "from two years ago").
- ``original_sql``: the corresponding SQLite query, which contains at least one ``DATE('now', ...)`` or ``DATE('now')`` call. This is provided FOR CONTEXT ONLY — you must NOT echo or rewrite it.

Output (return EXACTLY one JSON object ``{"current_question": "..."}``; no markdown, no code fences, no explanation, and NO ``current_sql`` field):
- ``current_question``: ``original_question`` with each relative time expression replaced by an explicit version anchored at 2022. Suggested rewrites:
  * "last year" / "the previous year" / "in the previous year" → "the year before 2022"
  * "in the past N years" / "over the past N years" / "in the past N year" → "in the N years up to 2022"
  * "in the past year" → "in the year up to 2022"
  * "in the past N months" → "in the N months up to 2022-12-31"
  * "in the past N days" / "in the past N day" → "in the N days up to 2022-12-31"
  * "in the fourth quarter of last year" → "in the fourth quarter of the year before 2022" (similarly for first/second/third quarter)
  * "the same period last year" → "the same period of the year before 2022"
  * "from two years ago" / "since two years ago" → "from two years before 2022" / "since two years before 2022"
  All other characters (table/column names, numbers, quoted literals like "one month", punctuation, casing, spacing) MUST stay CHARACTER-FOR-CHARACTER identical to ``original_question``.

Strict requirements:
1. Do NOT add, remove, or rephrase any content unrelated to the date.
2. Do NOT include a ``current_sql`` field — output ONLY ``current_question``.
3. Do NOT include the literal word "now" anywhere in ``current_question``.
4. Output JSON only, with no prefix or suffix."""


def _build_prompt_en(original_question: str, original_sql: str) -> str:
    examples_block = "\n\n".join(_render_example(ex) for ex in _FEW_SHOT_EXAMPLES_EN)
    current_input = json.dumps(
        {"original_question": original_question, "original_sql": original_sql},
        ensure_ascii=False,
        indent=2,
    )
    return (
        f"{_PROMPT_HEADER_EN}\n\n"
        f"### Examples\n{examples_block}\n\n"
        f"### Current Input\n{current_input}\n\n"
        f"### Current Output (JSON only):\n"
    )


# ---------------------------------------------------------------------------
# Response parsing & safety post-process
# ---------------------------------------------------------------------------

_JSON_OBJECT_RE = re.compile(r"\{.*\}", re.DOTALL)


def _extract_json_object(text: str) -> Optional[dict]:
    """Best-effort: get a dict out of a possibly-fenced LLM JSON response."""
    if not text:
        return None
    cleaned = text.strip()
    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\s*```$", "", cleaned).strip()

    try:
        obj = json.loads(cleaned)
        if isinstance(obj, dict):
            return obj
    except (json.JSONDecodeError, ValueError):
        pass

    m = _JSON_OBJECT_RE.search(cleaned)
    if m:
        try:
            obj = json.loads(m.group(0))
            if isinstance(obj, dict):
                return obj
        except (json.JSONDecodeError, ValueError):
            return None
    return None


def _force_anchor_sql(sql: str) -> str:
    """Deterministically replace any remaining ``DATE('now'`` with the anchor.

    Acts as a safety net regardless of what the LLM returned.  Preserves the
    exact spacing/quote style the model used after the ``'now'`` literal.
    """
    return NOW_PATTERN.sub(f"DATE('{ANCHOR_DATE}'", sql)


# Insert a Chinese comma before "2022年" when it is glued onto an alphanumeric
# token (typically a stock code like ``000948``).  Without this, rewrites like
# ``帮我看下000948近三年的...`` collapse to ``帮我看下0009482022年的近三年的...``
# which reads as a single 10-digit number to a Chinese reader.
_GLUED_ANCHOR_RE = re.compile(rf"(?<=[A-Za-z0-9]){ANCHOR_YEAR}年")


def _normalize_question(question: str) -> str:
    """Lightweight readability fixes on top of the LLM's rewrite."""
    if not question:
        return question
    return _GLUED_ANCHOR_RE.sub(f"，{ANCHOR_YEAR}年", question)


def _parse_response(
    text: str,
    fallback_question: str,
    fallback_sql: str,
) -> tuple[str, str, bool]:
    """Return ``(question, sql, ok)`` for the Chinese pass.

    ``ok`` is False when we had to fall back to the original question (the SQL
    is always safe because the deterministic post-process guarantees no
    ``DATE('now'`` survives).
    """
    obj = _extract_json_object(text)

    question = fallback_question
    sql = fallback_sql
    ok = False

    if obj is not None:
        q_val = obj.get("current_question")
        s_val = obj.get("current_sql")
        if isinstance(q_val, str) and q_val.strip():
            question = q_val.strip()
            ok = True
        if isinstance(s_val, str) and s_val.strip():
            sql = s_val

    question = _normalize_question(question)
    sql = _force_anchor_sql(sql)
    return question, sql, ok


def _parse_response_en(
    text: str,
    fallback_question: str,
    fallback_sql: str,
) -> tuple[str, str, bool]:
    """Return ``(question, sql, ok)`` for the English pass.

    Unlike :func:`_parse_response`, this never trusts ``current_sql`` from
    the LLM — the English prompt forbids that field and the SQL is always
    derived deterministically from ``fallback_sql`` via
    :func:`_force_anchor_sql`.  This protects English-localized SQL literals
    (e.g. ``'one month'``) from being silently mangled by the model.
    The Chinese-comma normalization is also skipped (no-op on English text).
    """
    obj = _extract_json_object(text)

    question = fallback_question
    ok = False

    if obj is not None:
        q_val = obj.get("current_question")
        if isinstance(q_val, str) and q_val.strip():
            question = q_val.strip()
            ok = True

    sql = _force_anchor_sql(fallback_sql)
    return question, sql, ok


# ---------------------------------------------------------------------------
# Cache (jsonl, keyed by q_id)
# ---------------------------------------------------------------------------

def _load_cache(path: str) -> dict[int, dict]:
    """Load existing rewrites; tolerant of partial / corrupt last lines."""
    cache: dict[int, dict] = {}
    if not os.path.isfile(path):
        return cache
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            qid = obj.get("q_id")
            if isinstance(qid, int):
                cache[qid] = obj
    return cache


def _append_cache(path: str, record: dict, lock: Lock) -> None:
    line = json.dumps(record, ensure_ascii=False)
    with lock:
        with open(path, "a", encoding="utf-8") as f:
            f.write(line + "\n")


# ---------------------------------------------------------------------------
# Split rewriting
# ---------------------------------------------------------------------------

PromptBuilder = Callable[[str, str], str]
ResponseParser = Callable[[str, str, str], "tuple[str, str, bool]"]


def _rewrite_split(
    split_path: str,
    out_path: str,
    cache_path: str,
    client,
    model: str,
    workers: int,
    max_tokens: int = 1024,
    prompt_builder: PromptBuilder = _build_prompt,
    parse_response: ResponseParser = _parse_response,
) -> dict:
    """Rewrite one split (e.g. dev.json) in place at ``out_path``.

    ``prompt_builder`` constructs the LLM prompt from
    ``(original_question, original_sql)`` (default: Chinese both-fields prompt).
    ``parse_response`` extracts ``(question, sql, ok)`` from the raw LLM
    response (default: Chinese parser that accepts ``current_sql``).  The
    English pass passes :func:`_build_prompt_en` and :func:`_parse_response_en`.

    Returns a summary dict ``{total, candidates, rewritten, fallback, cached}``.
    """
    with open(split_path, "r", encoding="utf-8") as f:
        entries = json.load(f)

    candidates_idx = [
        i for i, e in enumerate(entries)
        if NOW_PATTERN.search(e.get("sql_query", "") or "")
    ]
    print(
        f"[{os.path.basename(split_path)}] {len(candidates_idx)}/{len(entries)} "
        f"entries reference DATE('now', ...)",
        file=sys.stderr,
    )

    os.makedirs(os.path.dirname(cache_path) or ".", exist_ok=True)
    cache = _load_cache(cache_path)
    if cache:
        print(f"[cache] loaded {len(cache)} prior rewrites from {cache_path}",
              file=sys.stderr)

    cache_lock = Lock()
    rewritten = 0
    fallback = 0
    cached = 0

    def _apply(idx: int, record: dict) -> None:
        nonlocal rewritten, fallback
        question, sql, ok = parse_response(
            record.get("raw", ""),
            entries[idx]["question"],
            entries[idx].get("sql_query", "") or "",
        )
        entries[idx]["question"] = question
        entries[idx]["sql_query"] = sql
        if ok:
            rewritten += 1
        else:
            fallback += 1

    pending: list[int] = []
    for idx in candidates_idx:
        qid = entries[idx].get("q_id")
        if isinstance(qid, int) and qid in cache:
            _apply(idx, cache[qid])
            cached += 1
        else:
            pending.append(idx)

    def _call_one(idx: int) -> tuple[int, str]:
        entry = entries[idx]
        prompt = prompt_builder(entry.get("question", ""), entry.get("sql_query", "") or "")
        try:
            resp = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.0,
                max_tokens=max_tokens,
            )
            raw = (resp.choices[0].message.content or "").strip()
        except Exception as e:
            raw = ""
            print(f"[error] q_id={entry.get('q_id')}: {e}", file=sys.stderr)
        return idx, raw

    if pending:
        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures = {executor.submit(_call_one, idx): idx for idx in pending}
            for fut in tqdm(
                as_completed(futures),
                total=len(futures),
                desc=f"Rewriting {os.path.basename(split_path)}",
            ):
                idx, raw = fut.result()
                qid = entries[idx].get("q_id")
                record = {"q_id": qid, "raw": raw}
                _append_cache(cache_path, record, cache_lock)
                _apply(idx, record)

    # Drop the now-stale structural SQL fields from every entry so the output
    # schema stays consistent (changed and unchanged samples alike).  Mutate
    # in place so the original list order is preserved bit-for-bit.
    stripped_count = 0
    for entry in entries:
        removed_any = False
        for field in STRUCTURAL_SQL_FIELDS:
            if field in entry:
                entry.pop(field, None)
                removed_any = True
        if removed_any:
            stripped_count += 1

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)

    return {
        "total": len(entries),
        "candidates": len(candidates_idx),
        "rewritten": rewritten,
        "fallback": fallback,
        "cached": cached,
        "stripped": stripped_count,
    }


# ---------------------------------------------------------------------------
# Per-language sidecar mirror (dev_cn.json / dev_en.json) and dev_gold.sql
# ---------------------------------------------------------------------------

def _write_dev_gold(dev_json_path: str, gold_out_path: str) -> int:
    """Regenerate ``dev_gold.sql`` from the rewritten ``dev.json``.

    Mirrors the source dataset's ``dev_gold.py`` script: one ``sql_query`` per
    line, in the same order as ``dev.json``, skipping empty queries.  We
    regenerate (rather than copy the source ``dev_gold.sql``) because the
    rewritten queries no longer match the original gold file.
    """
    with open(dev_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    written = 0
    with open(gold_out_path, "w", encoding="utf-8") as out:
        for item in data:
            sql = (item.get("sql_query") or "").strip()
            if sql:
                out.write(sql + "\n")
                written += 1
    return written


def _mirror_dev_lang_sidecar(
    dev_json_path: str,
    sidecar_in_path: str,
    sidecar_out_path: str,
) -> int:
    """Replace ``question`` in the language sidecar with the rewritten dev.json question.

    The "sidecar" is ``dev_cn.json`` for the Chinese pass and ``dev_en.json``
    for the English pass — both are q_id-keyed, question-only mirrors of
    ``dev.json``.  Match is by ``q_id``.  Returns the number of entries
    whose question was actually changed.
    """
    with open(dev_json_path, "r", encoding="utf-8") as f:
        dev = json.load(f)
    with open(sidecar_in_path, "r", encoding="utf-8") as f:
        sidecar = json.load(f)

    qid_to_question: dict[int, str] = {
        e["q_id"]: e["question"] for e in dev if "q_id" in e and "question" in e
    }

    replaced = 0
    for entry in sidecar:
        qid = entry.get("q_id")
        if isinstance(qid, int) and qid in qid_to_question:
            new_q = qid_to_question[qid]
            if entry.get("question") != new_q:
                entry["question"] = new_q
                replaced += 1

    with open(sidecar_out_path, "w", encoding="utf-8") as f:
        json.dump(sidecar, f, ensure_ascii=False, indent=2)
    return replaced


# ---------------------------------------------------------------------------
# Per-language driver: full pipeline for one language pass
# ---------------------------------------------------------------------------

def _run_language_pass(
    *,
    label: str,
    input_dir: str,
    output_dir: str,
    sidecar_filename: str,
    prompt_builder: PromptBuilder,
    parse_response: ResponseParser,
    client,
    model: str,
    workers: int,
    max_tokens: int,
) -> None:
    """Run the full mirror+rewrite+gold pipeline for one language.

    ``label`` is a short human-readable tag (e.g. ``"cn"`` / ``"en"``) used
    only in log output.  ``sidecar_filename`` is the language-specific
    question-only mirror file (``dev_cn.json`` or ``dev_en.json``).
    """
    print(f"\n=== [{label}] {input_dir} -> {output_dir} ===", file=sys.stderr)

    if not os.path.isdir(input_dir):
        print(f"[{label}] [error] input dir not found: {input_dir}", file=sys.stderr)
        return

    print(f"[{label}] mirroring static files {input_dir} -> {output_dir}",
          file=sys.stderr)
    _mirror_static_files(input_dir, output_dir)

    dev_in = os.path.join(input_dir, DEV_JSON)
    dev_out = os.path.join(output_dir, DEV_JSON)
    cache_path = os.path.join(output_dir, CACHE_DIR_NAME, DEV_CACHE_FILE)
    summary = _rewrite_split(
        split_path=dev_in,
        out_path=dev_out,
        cache_path=cache_path,
        client=client,
        model=model,
        workers=workers,
        max_tokens=max_tokens,
        prompt_builder=prompt_builder,
        parse_response=parse_response,
    )
    print(
        f"[{label}] [dev.json] total={summary['total']} candidates={summary['candidates']} "
        f"rewritten={summary['rewritten']} fallback={summary['fallback']} "
        f"cached={summary['cached']} stripped_structural={summary['stripped']}",
        file=sys.stderr,
    )

    sidecar_in = os.path.join(input_dir, sidecar_filename)
    sidecar_out = os.path.join(output_dir, sidecar_filename)
    if os.path.isfile(sidecar_in):
        replaced = _mirror_dev_lang_sidecar(dev_out, sidecar_in, sidecar_out)
        print(
            f"[{label}] [{sidecar_filename}] replaced {replaced} question(s) by q_id",
            file=sys.stderr,
        )
    else:
        print(
            f"[{label}] [warn] {sidecar_in} not found; skipping {sidecar_filename} mirror",
            file=sys.stderr,
        )

    gold_out = os.path.join(output_dir, DEV_GOLD_SQL)
    written = _write_dev_gold(dev_out, gold_out)
    print(f"[{label}] [dev_gold.sql] wrote {written} SQL line(s) -> {gold_out}",
          file=sys.stderr)

    print(f"[{label}] done. output -> {output_dir}", file=sys.stderr)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Rewrite BULL-{cn,en}-origin dev.json so DATE('now', ...) is "
                    "anchored to 2022-12-31 in both questions and SQL.  By default "
                    "runs both the Chinese and English passes; use --skip-chinese "
                    "or --skip-english to run only one."
    )
    # Chinese pass.
    parser.add_argument(
        "--input-dir", default=DEFAULT_INPUT_DIR,
        help=f"Chinese input dir (default: {DEFAULT_INPUT_DIR})",
    )
    parser.add_argument(
        "--output-dir", default=DEFAULT_OUTPUT_DIR,
        help=f"Chinese output dir (default: {DEFAULT_OUTPUT_DIR})",
    )
    parser.add_argument(
        "--skip-chinese", action="store_true",
        help="Skip the Chinese pass (BULL-cn-origin -> BULL-cn-origin-date-reset).",
    )
    # English pass.
    parser.add_argument(
        "--english-input-dir", default=ENGLISH_INPUT_DIR,
        help=f"English input dir (default: {ENGLISH_INPUT_DIR})",
    )
    parser.add_argument(
        "--english-output-dir", default=ENGLISH_OUTPUT_DIR,
        help=f"English output dir (default: {ENGLISH_OUTPUT_DIR})",
    )
    parser.add_argument(
        "--skip-english", action="store_true",
        help="Skip the English pass (BULL-en-origin -> BULL-en-origin-date-reset).",
    )
    # Shared LLM / runtime options.
    parser.add_argument(
        "--model",
        default=os.environ.get("NOW_RESET_MODEL", "qwen-plus"),
        help="LLM model name (default: $NOW_RESET_MODEL or qwen-plus)",
    )
    parser.add_argument("--workers", type=int, default=10)
    parser.add_argument("--max-tokens", type=int, default=1024)
    parser.add_argument("--api-key", default=None)
    parser.add_argument("--api-base", default=None)
    args = parser.parse_args()

    if args.skip_chinese and args.skip_english:
        print("[error] --skip-chinese and --skip-english given together; nothing to do.",
              file=sys.stderr)
        sys.exit(1)

    loaded = _load_dotenv()
    if loaded:
        print(f"[env] loaded {loaded}", file=sys.stderr)

    client = get_llm_client(api_key=args.api_key, base_url=args.api_base)

    if not args.skip_chinese:
        _run_language_pass(
            label="cn",
            input_dir=args.input_dir,
            output_dir=args.output_dir,
            sidecar_filename=DEV_LANG_SIDECAR_CN,
            prompt_builder=_build_prompt,
            parse_response=_parse_response,
            client=client,
            model=args.model,
            workers=args.workers,
            max_tokens=args.max_tokens,
        )
    else:
        print("[cn] skipped (--skip-chinese)", file=sys.stderr)

    if not args.skip_english:
        _run_language_pass(
            label="en",
            input_dir=args.english_input_dir,
            output_dir=args.english_output_dir,
            sidecar_filename=DEV_LANG_SIDECAR_EN,
            prompt_builder=_build_prompt_en,
            parse_response=_parse_response_en,
            client=client,
            model=args.model,
            workers=args.workers,
            max_tokens=args.max_tokens,
        )
    else:
        print("[en] skipped (--skip-english)", file=sys.stderr)

    print("\nAll requested passes finished.", file=sys.stderr)


if __name__ == "__main__":
    main()
