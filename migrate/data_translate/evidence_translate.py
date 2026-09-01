#!/usr/bin/env python3
"""
Adapt/translate evidence for cross-language dev sets (EN↔CN).

EN-reference modes (for EN-to-CN pipeline):
  ``cndb-bird``       : EN question + CN SQL  → English evidence (CN schema refs)
  ``endb-cnqt``       : CN question + EN SQL  → Chinese evidence (EN schema refs)
  ``full-cn``         : CN question + CN SQL  → Chinese evidence (CN schema refs)

CN-reference modes (for CN-to-EN pipeline):
  ``endb-cn-dataset`` : EN question + EN SQL  → English evidence (EN schema refs)
  ``cndb-enqt``       : CN question + CN SQL  → Chinese evidence (CN schema refs)
  ``cn-enq-cnsql``    : EN question + CN SQL  → English evidence (CN schema refs)
  ``full-en``         : EN question + EN SQL  → English evidence (EN schema refs)

Only relevant when the dataset has ``has_evidence=True``.
"""

import argparse
import json
import os
import sys
from typing import Dict, Tuple

from tqdm import tqdm

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import STD_DB_DIR, STD_DEV_JSON_FILE, get_config
from data_translate.prompts import (
    EVIDENCE_CN_QUESTION_EN_SQL,
    EVIDENCE_CN_REF_CN_QUESTION_CN_SQL,
    EVIDENCE_CN_REF_EN_QUESTION_CN_SQL,
    EVIDENCE_CN_REF_EN_QUESTION_EN_SQL,
    EVIDENCE_EN_QUESTION_CN_SQL,
    EVIDENCE_FULL_CN,
    EVIDENCE_FULL_EN,
)
from utils import get_llm_client

_text2sql_mod = None


def _get_text2sql():
    global _text2sql_mod
    if _text2sql_mod is None:
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "text2sql_exp"))
        import text2sql as _t2s
        _text2sql_mod = _t2s
    return _text2sql_mod


ALL_MIX_KINDS = [
    "cndb-bird", "endb-cnqt", "full-cn",
    "endb-cn-dataset", "cndb-enqt", "cn-enq-cnsql", "full-en",
]

_TEMPLATES = {
    # EN-reference (for EN→CN pipeline)
    "cndb-bird": EVIDENCE_EN_QUESTION_CN_SQL,
    "endb-cnqt": EVIDENCE_CN_QUESTION_EN_SQL,
    "full-cn": EVIDENCE_FULL_CN,
    # CN-reference (for CN→EN pipeline)
    "endb-cn-dataset": EVIDENCE_CN_REF_EN_QUESTION_EN_SQL,
    "cndb-enqt": EVIDENCE_CN_REF_CN_QUESTION_CN_SQL,
    "cn-enq-cnsql": EVIDENCE_CN_REF_EN_QUESTION_CN_SQL,
    "full-en": EVIDENCE_FULL_EN,
}


def sqlite_path(db_root, db_id):
    return os.path.join(db_root, db_id, f"{db_id}.sqlite")


def build_schema_and_samples(db_path, sample_rows, encoding, random_rows):
    t2s = _get_text2sql()
    if not db_path or not os.path.exists(db_path):
        return "(database file not found)", ""
    schema = t2s.get_sql_style_schema(db_path, include_foreign_keys=True) or "(empty schema)"
    if sample_rows <= 0:
        return schema, ""
    samples = t2s.get_sample_rows(
        db_path, max_rows_per_table=sample_rows,
        encoding=encoding, random_rows=random_rows,
    )
    return schema, samples or ""


def _strip_outer_quotes(text):
    text = (text or "").strip()
    if len(text) >= 2 and text[0] == text[-1] and text[0] in "\"'":
        return text[1:-1].strip()
    return text


def adapt_evidence(
    client, *, mix_kind, ref_question, ref_sql, ref_evidence,
    target_question, target_sql, en_schema_block, cn_schema_block, model,
):
    if not (ref_evidence or "").strip():
        return ""

    template = _TEMPLATES[mix_kind]
    prompt = template.format(
        en_schema_block=en_schema_block,
        cn_schema_block=cn_schema_block,
        ref_question=ref_question or "",
        ref_sql=ref_sql or "",
        ref_evidence=ref_evidence or "",
        target_question=target_question or "",
        target_sql=target_sql or "",
    )
    try:
        resp = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0, max_tokens=1536,
        )
        return _strip_outer_quotes(resp.choices[0].message.content or "")
    except Exception as e:
        return f"[Translate Error: {e}]"


def run_evidence_translation(
    *, mix_kind, ref_dir, en_dir, cn_dir, target_dir, output_dir,
    sample_rows, random_sample_rows, en_encoding, cn_encoding,
    model, api_key=None, api_base=None,
):
    en_db_dir = os.path.join(en_dir, STD_DB_DIR)
    cn_db_dir = os.path.join(cn_dir, STD_DB_DIR)
    ref_json = os.path.join(ref_dir, STD_DEV_JSON_FILE)
    target_json = os.path.join(target_dir, STD_DEV_JSON_FILE)
    output_json = os.path.join(output_dir, STD_DEV_JSON_FILE)

    with open(ref_json, "r", encoding="utf-8") as f:
        ref_list = json.load(f)
    with open(target_json, "r", encoding="utf-8") as f:
        target_list = json.load(f)

    ref_by_id = {int(e["question_id"]): e for e in ref_list}
    client = get_llm_client(api_key=api_key, base_url=api_base)
    cache: Dict[str, Tuple[str, str]] = {}

    def _blocks(db_id):
        if db_id in cache:
            return cache[db_id]
        en_s, en_d = build_schema_and_samples(
            sqlite_path(en_db_dir, db_id), sample_rows, en_encoding, random_sample_rows,
        )
        cn_s, cn_d = build_schema_and_samples(
            sqlite_path(cn_db_dir, db_id), sample_rows, cn_encoding, random_sample_rows,
        )
        en_blk = "## Schema (DDL + FKs)\n" + en_s + (f"\n\n## Sample data\n\n{en_d}" if en_d else "")
        cn_blk = "## Schema (DDL + FKs)\n" + cn_s + (f"\n\n## Sample data\n\n{cn_d}" if cn_d else "")
        cache[db_id] = (en_blk, cn_blk)
        return en_blk, cn_blk

    out = []
    for entry in tqdm(target_list, desc=f"Evidence ({mix_kind})"):
        qid = int(entry.get("question_id", -1))
        db_id = entry.get("db_id", "")
        ref = ref_by_id.get(qid)
        if not ref:
            out.append({**entry, "evidence": entry.get("evidence", "")})
            continue
        ref_sql = ref.get("SQL") or ref.get("query", "")
        target_sql = entry.get("SQL") or entry.get("query", "")
        en_blk, cn_blk = _blocks(db_id)
        new_ev = adapt_evidence(
            client, mix_kind=mix_kind,
            ref_question=ref.get("question", ""), ref_sql=ref_sql,
            ref_evidence=ref.get("evidence", ""),
            target_question=entry.get("question", ""), target_sql=target_sql,
            en_schema_block=en_blk, cn_schema_block=cn_blk, model=model,
        )
        out.append({**entry, "evidence": new_ev})

    os.makedirs(output_dir, exist_ok=True)
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print(f"Written {output_json} ({len(out)} entries), mode={mix_kind}.")


def main():
    parser = argparse.ArgumentParser(description="Translate/adapt evidence for cross-lingual dev sets (EN↔CN).")
    parser.add_argument("--dataset", required=True, help="Base dataset name (for config: encoding)")
    parser.add_argument("--mix", choices=ALL_MIX_KINDS, required=True,
                        help="Evidence adaptation mode")
    parser.add_argument("--ref-dir", required=True,
                        help="Reference dataset directory (has dev.json with original evidence)")
    parser.add_argument("--en-dir", required=True, help="English dataset directory (for schema/samples)")
    parser.add_argument("--cn-dir", required=True, help="Chinese dataset directory (for schema/samples)")
    parser.add_argument("--target-dir", required=True,
                        help="Target variant directory (provides the dev.json to adapt)")
    parser.add_argument("--output-dir", required=True, help="Output directory")
    parser.add_argument("--sample-rows", type=int, default=5)
    parser.add_argument("--random-sample-rows", action="store_true")
    parser.add_argument("--model", default=None,
                        help="LLM model (default: env EVIDENCE_TRANSLATE_MODEL or qwen-plus)")
    parser.add_argument("--api-key", default=None)
    parser.add_argument("--api-base", default=None)
    args = parser.parse_args()

    cfg = get_config(args.dataset)
    model = args.model or os.environ.get("EVIDENCE_TRANSLATE_MODEL", "qwen-plus")
    run_evidence_translation(
        mix_kind=args.mix, ref_dir=args.ref_dir,
        en_dir=args.en_dir, cn_dir=args.cn_dir,
        target_dir=args.target_dir, output_dir=args.output_dir,
        sample_rows=args.sample_rows, random_sample_rows=args.random_sample_rows,
        en_encoding=cfg.db_encoding, cn_encoding="utf-8",
        model=model, api_key=args.api_key, api_base=args.api_base,
    )


if __name__ == "__main__":
    main()
