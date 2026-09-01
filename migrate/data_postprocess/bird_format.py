#!/usr/bin/env python3
"""Normalize dataset dev.json files to a BIRD-like schema.

For each target directory, recursively find `dev.json` and rewrite rows so keys map to:
`question_id`, `db_id`, `question`, `evidence`, `SQL`, `difficulty`.

If a key cannot be mapped, it is preserved in output rows.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple


ALIASES: Dict[str, List[str]] = {
    "question_id": ["question_id", "q_id", "id", "uid"],
    "db_id": ["db_id", "db_name", "database_id"],
    "question": ["question", "utterance", "nl_question", "query_text"],
    "evidence": ["evidence", "hint", "context", "rationale"],
    "SQL": ["SQL", "sql", "query", "sql_query", "gold_sql"],
    "difficulty": ["difficulty", "hardness", "level"],
}

ORDER = ["question_id", "db_id", "question", "evidence", "SQL", "difficulty"]
DEFAULT_INPUT_DIRS = [
    "dataset/EHRSQL-typical",
    "dataset/BULL-FinSQL/BULL-mixq-mixdb-new",
]


def _first_value(item: Dict[str, Any], keys: Iterable[str]) -> Tuple[Any, str | None]:
    for key in keys:
        if key in item:
            return item[key], key
    return None, None


def _normalize_item(item: Any) -> Any:
    if not isinstance(item, dict):
        return item

    # Keep already-normalized rows unchanged to avoid accidental edits.
    if all(k in item for k in ("question_id", "db_id", "question", "SQL")):
        return item

    out: Dict[str, Any] = {}
    consumed = set()

    for target in ORDER:
        value, src_key = _first_value(item, ALIASES[target])
        if src_key is not None:
            out[target] = value
            consumed.add(src_key)
        elif target == "evidence":
            out[target] = ""

    for key, value in item.items():
        if key not in consumed and key not in out:
            out[key] = value
    return out


def _normalize_data(data: Any) -> Any:
    if isinstance(data, list):
        return [_normalize_item(row) for row in data]
    if isinstance(data, dict):
        return _normalize_item(data)
    return data


def _normalize_file(json_path: Path) -> None:
    with json_path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    normalized = _normalize_data(data)
    with json_path.open("w", encoding="utf-8") as f:
        json.dump(normalized, f, ensure_ascii=False, indent=2)
        f.write("\n")


def _iter_target_files(repo_root: Path, input_dirs: List[str], target_name: str) -> List[Path]:
    targets: List[Path] = []
    for rel_dir in input_dirs:
        abs_dir = repo_root / rel_dir
        if not abs_dir.is_dir():
            print(f"Skip missing directory: {abs_dir}")
            continue
        targets.extend(sorted(abs_dir.rglob(target_name)))
    return sorted(set(targets))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Normalize dev.json files to BIRD-like keys while preserving unmapped keys."
        )
    )
    parser.add_argument(
        "--input-dirs",
        nargs="+",
        default=DEFAULT_INPUT_DIRS,
        metavar="DIR",
        help="Dataset directories (relative to repo root) to scan recursively.",
    )
    parser.add_argument(
        "--target-name",
        default="dev.json",
        help="Target filename to normalize. Default: dev.json",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    repo_root = Path(__file__).resolve().parents[2]
    target_files = _iter_target_files(repo_root, args.input_dirs, args.target_name)

    for json_path in target_files:
        _normalize_file(json_path)
        print(f"Normalized: {json_path}")


if __name__ == "__main__":
    main()
