"""Apply reviewed, idempotent SQL repairs to aligned legacy seed cells."""

from __future__ import annotations

import re
from pathlib import Path

from mol_sql.contracts.io import load_json, write_json
from mol_sql.dataset.adapters import load_source_specs


def _tokenize_sql(sql: str) -> list[str]:
    tokens: list[str] = []
    index = 0
    while index < len(sql):
        if sql[index].isspace():
            index += 1
            continue
        if sql[index] in {"`", "'", '"'}:
            quote = sql[index]
            end = index + 1
            while end < len(sql):
                if sql[end] == quote:
                    if end + 1 < len(sql) and sql[end + 1] == quote:
                        end += 2
                        continue
                    break
                end += 1
            tokens.append(sql[index : end + 1])
            index = end + 1
            continue
        two = sql[index : index + 2]
        if two in {">=", "<=", "<>", "!=", "||"}:
            tokens.append(two)
            index += 2
            continue
        if sql[index] in "(),;=<>+-*/.":
            tokens.append(sql[index])
            index += 1
            continue
        end = index
        while end < len(sql) and (
            sql[end].isalnum() or sql[end] == "_" or ord(sql[end]) > 127
        ):
            end += 1
        if end == index:
            index += 1
            continue
        tokens.append(sql[index:end])
        index = end
    return tokens


def _tokens_without_values(sql: str) -> list[str]:
    result = []
    for token in _tokenize_sql(sql):
        if (
            token.startswith(("'", '"'))
            and token.endswith(("'", '"'))
        ):
            result.append("value")
        elif token.startswith("`") and token.endswith("`"):
            result.append(token[1:-1].lower())
        else:
            result.append(token.lower())
    return result


def apply_execution_repairs(
    *,
    repo_root: Path,
    source_config: Path,
    repairs_path: Path,
) -> dict[str, int]:
    """Apply configured fragment replacements and rebuild per-cell gold files."""

    repo_root = repo_root.resolve()
    source_config = (
        source_config
        if source_config.is_absolute()
        else repo_root / source_config
    )
    repairs_path = (
        repairs_path if repairs_path.is_absolute() else repo_root / repairs_path
    )
    specs = {
        spec.source_family: spec for spec in load_source_specs(source_config)
    }
    repairs = load_json(repairs_path).get("sql_repairs", [])
    cache: dict[Path, list[dict]] = {}
    changed_rows: set[tuple[Path, int]] = set()
    already_applied = 0
    for repair in repairs:
        source = specs[str(repair["source_family"])]
        indices = [int(value) for value in repair["legacy_indices"]]
        schema_language = str(repair["schema_language"])
        old, new = str(repair["old_fragment"]), str(repair["new_fragment"])
        for variant in source.variants.values():
            if variant.schema_language != schema_language:
                continue
            dev_path = repo_root / source.root / variant.directory / "dev.json"
            rows = cache.setdefault(dev_path, load_json(dev_path))
            for index in indices:
                row = rows[index]
                database_id = str(row.get("db_id", row.get("db_name")))
                if database_id != str(repair["database_id"]):
                    raise ValueError(
                        f"{source.source_family}:{index}: expected "
                        f"{repair['database_id']}, found {database_id}"
                    )
                sql_fields = [
                    field
                    for field in source.sql_fields
                    if isinstance(row.get(field), str) and row[field].strip()
                ]
                if not sql_fields:
                    raise ValueError(f"{source.source_family}:{index}: no SQL")
                current = str(row[sql_fields[0]])
                if current.casefold().count(new.casefold()) == 1:
                    already_applied += 1
                    continue
                repaired, replacements = re.subn(
                    re.escape(old),
                    lambda _: new,
                    current,
                    flags=re.IGNORECASE,
                )
                if replacements != 1:
                    raise ValueError(
                        f"{source.source_family}:{index}: expected one repair fragment"
                    )
                for field in sql_fields:
                    field_value = str(row[field])
                    repaired_field, field_replacements = re.subn(
                        re.escape(old),
                        lambda _: new,
                        field_value,
                        flags=re.IGNORECASE,
                    )
                    if field_replacements != 1:
                        raise ValueError(
                            f"{source.source_family}:{index}:{field}: "
                            "expected one repair fragment"
                        )
                    row[field] = repaired_field
                if "query_toks" in row:
                    row["query_toks"] = _tokenize_sql(repaired)
                if "query_toks_no_value" in row:
                    row["query_toks_no_value"] = _tokens_without_values(repaired)
                changed_rows.add((dev_path, index))

    for dev_path, rows in cache.items():
        write_json(dev_path, rows)
        source = next(
            spec
            for spec in specs.values()
            if any(
                dev_path
                == repo_root / spec.root / variant.directory / "dev.json"
                for variant in spec.variants.values()
            )
        )
        gold_path = dev_path.with_name("dev_gold.sql")
        lines = []
        for row in rows:
            sql = next(
                str(row[field]).strip()
                for field in source.sql_fields
                if isinstance(row.get(field), str) and row[field].strip()
            )
            database_id = str(row.get("db_id", row.get("db_name")))
            lines.append(f"{sql}\t{database_id}\n")
        gold_path.write_text("".join(lines), encoding="utf-8")
    return {
        "configured_repairs": len(repairs),
        "changed_rows": len(changed_rows),
        "already_applied": already_applied,
        "changed_files": len(cache),
    }
