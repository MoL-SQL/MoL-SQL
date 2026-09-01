#!/usr/bin/env python3
"""Keep only databases referenced by ``<split>_gold.sql``.

For a canonical dataset directory this script:

1. creates ``<split>_gold.sql`` from ``<split>.json`` when needed;
2. reads used DB ids from ``<input>/<split>_gold.sql``;
3. writes ``tables_new.json`` with only those DB schemas from ``tables.json``;
4. hard-copies only the used DB directories into ``database_new`` (or
   ``databases_new`` when the input uses ``databases``);
5. replaces the old ``tables.json`` and DB root with the new filtered copies.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from pathlib import Path


def _create_gold_from_json(split_path: Path, gold_path: Path) -> int:
    """Create canonical ``<sql>\t<db_id>`` gold lines from split JSON."""
    if not split_path.is_file():
        raise FileNotFoundError(
            f"Missing gold SQL file: {gold_path}; cannot create it because "
            f"the split JSON is also missing: {split_path}"
        )

    with split_path.open("r", encoding="utf-8") as f:
        rows = json.load(f)
    if not isinstance(rows, list):
        raise ValueError(f"Expected a JSON list in {split_path}, got {type(rows).__name__}")

    gold_lines: list[str] = []
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            raise ValueError(
                f"Invalid entry {index} in {split_path}: expected object, "
                f"got {type(row).__name__}"
            )
        sql = row.get("sql_query") or row.get("query") or row.get("SQL") or row.get("sql")
        db_id = row.get("db_id") or row.get("db_name")
        if not sql or not db_id:
            missing = "SQL" if not sql else "db_id"
            raise ValueError(f"Invalid entry {index} in {split_path}: missing {missing}")
        flat_sql = " ".join(str(sql).split())
        gold_lines.append(f"{flat_sql}\t{str(db_id).strip()}\n")

    if not gold_lines:
        raise ValueError(f"No entries found in {split_path}")

    with gold_path.open("w", encoding="utf-8") as f:
        f.writelines(gold_lines)
    return len(gold_lines)


def _read_used_db_ids(gold_path: Path) -> list[str]:
    """Return DB ids from canonical ``<sql>\t<db_id>`` gold lines."""
    if not gold_path.is_file():
        raise FileNotFoundError(f"Missing gold SQL file: {gold_path}")

    used: list[str] = []
    seen: set[str] = set()
    with gold_path.open("r", encoding="utf-8") as f:
        for line_no, raw_line in enumerate(f, start=1):
            line = raw_line.rstrip("\n")
            if not line.strip():
                continue
            if "\t" not in line:
                raise ValueError(
                    f"Invalid gold line {line_no} in {gold_path}: expected '<sql>\\t<db_id>'"
                )
            db_id = line.rsplit("\t", 1)[1].strip()
            if not db_id:
                raise ValueError(f"Invalid gold line {line_no} in {gold_path}: empty db_id")
            if db_id not in seen:
                seen.add(db_id)
                used.append(db_id)
    if not used:
        raise ValueError(f"No DB ids found in {gold_path}")
    return used


def _load_tables(tables_path: Path) -> list[dict]:
    if not tables_path.is_file():
        raise FileNotFoundError(f"Missing tables file: {tables_path}")
    with tables_path.open("r", encoding="utf-8") as f:
        tables = json.load(f)
    if not isinstance(tables, list):
        raise ValueError(f"Expected a JSON list in {tables_path}, got {type(tables).__name__}")
    return tables


def _find_db_root(input_dir: Path, requested_db_dir: str | None) -> Path:
    candidates = [requested_db_dir] if requested_db_dir else ["database", "databases"]
    for name in candidates:
        if not name:
            continue
        db_root = input_dir / name
        if db_root.is_dir():
            return db_root
    names = ", ".join(candidates)
    raise FileNotFoundError(f"Missing database root under {input_dir}; tried: {names}")


def _remove_path(path: Path) -> None:
    if path.is_symlink() or path.is_file():
        path.unlink()
    elif path.is_dir():
        shutil.rmtree(path)


def _copy_used_dbs(db_root: Path, new_db_root: Path, used_db_ids: list[str]) -> None:
    if new_db_root.exists() or new_db_root.is_symlink():
        _remove_path(new_db_root)
    new_db_root.mkdir(parents=True, exist_ok=False)

    missing: list[str] = []
    for db_id in used_db_ids:
        src = db_root / db_id
        if not src.exists():
            missing.append(db_id)
            continue
        dst = new_db_root / db_id
        if src.is_dir():
            shutil.copytree(src, dst, symlinks=False)
        else:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)

    if missing:
        _remove_path(new_db_root)
        preview = ", ".join(missing[:20])
        if len(missing) > 20:
            preview += f", ... (+{len(missing) - 20} more)"
        raise FileNotFoundError(f"Missing {len(missing)} used DB(s) under {db_root}: {preview}")


def prune(input_dir: Path, split: str, db_dir: str | None = None) -> tuple[int, int]:
    input_dir = input_dir.resolve()
    gold_path = input_dir / f"{split}_gold.sql"
    split_path = input_dir / f"{split}.json"
    tables_path = input_dir / "tables.json"

    if not gold_path.is_file():
        gold_count = _create_gold_from_json(split_path, gold_path)
        print(
            f"[only_copy_used_db] created {gold_path} from {split_path} "
            f"({gold_count} entries)",
            file=sys.stderr,
        )

    used_db_ids = _read_used_db_ids(gold_path)
    used_set = set(used_db_ids)

    tables = _load_tables(tables_path)
    filtered_tables = [entry for entry in tables if entry.get("db_id") in used_set]
    table_db_ids = {entry.get("db_id") for entry in filtered_tables}
    missing_schema = [db_id for db_id in used_db_ids if db_id not in table_db_ids]
    if missing_schema:
        preview = ", ".join(missing_schema[:20])
        if len(missing_schema) > 20:
            preview += f", ... (+{len(missing_schema) - 20} more)"
        raise ValueError(f"Missing {len(missing_schema)} used DB schema(s) in {tables_path}: {preview}")

    db_root = _find_db_root(input_dir, db_dir)
    new_tables_path = input_dir / "tables_new.json"
    new_db_root = input_dir / f"{db_root.name}_new"

    with new_tables_path.open("w", encoding="utf-8") as f:
        json.dump(filtered_tables, f, ensure_ascii=False, indent=2)

    try:
        _copy_used_dbs(db_root, new_db_root, used_db_ids)

        _remove_path(tables_path)
        new_tables_path.rename(tables_path)

        _remove_path(db_root)
        new_db_root.rename(db_root)
    except Exception:
        if new_tables_path.exists():
            _remove_path(new_tables_path)
        if new_db_root.exists() or new_db_root.is_symlink():
            _remove_path(new_db_root)
        raise

    return len(used_db_ids), len(filtered_tables)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Copy only DBs used by <split>_gold.sql and filter tables.json in place."
    )
    parser.add_argument("--input", required=True, help="Dataset directory containing tables.json and <split>_gold.sql.")
    parser.add_argument("--split", default="dev", choices=["dev", "train", "test"], help="Split name (default: dev).")
    parser.add_argument(
        "--db-dir",
        default=None,
        help="Database root name under --input. Defaults to auto-detecting database then databases.",
    )
    args = parser.parse_args()

    used_count, table_count = prune(Path(args.input), args.split, args.db_dir)
    print(
        f"[only_copy_used_db] kept {used_count} used database(s); "
        f"wrote {table_count} tables.json record(s)",
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()
