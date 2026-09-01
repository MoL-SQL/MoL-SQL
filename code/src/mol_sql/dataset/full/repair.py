"""Deterministic repairs for legacy MoL-Full seed artifacts."""

from __future__ import annotations

import shutil
import sqlite3
from dataclasses import dataclass
from pathlib import Path

from mol_sql.contracts.io import load_json


@dataclass(frozen=True)
class FixedPointRepairResult:
    source_rows: int
    target_rows: int
    mismatches_before: int
    mismatches_after: int
    applied: bool
    backup_path: str | None


@dataclass(frozen=True)
class MappedColumnRepairResult:
    source_rows: int
    target_rows: int
    mapped_values: int
    mismatches_before: int
    mismatches_after: int
    applied: bool
    backup_path: str | None


def _quote(identifier: str) -> str:
    return '"' + identifier.replace('"', '""') + '"'


def restore_mapped_column_by_key(
    *,
    source_database: Path,
    target_database: Path,
    replacement_map: Path,
    database_id: str,
    source_table: str,
    source_key: str,
    source_column: str,
    target_table: str,
    target_key: str,
    target_column: str,
    apply: bool,
    map_table: str | None = None,
    map_column: str | None = None,
    backup_path: Path | None = None,
) -> MappedColumnRepairResult:
    """Regenerate one translated column from a source column and reviewed map."""

    source_database = source_database.resolve()
    target_database = target_database.resolve()
    replacement_map = replacement_map.resolve()
    if not source_database.is_file() or not target_database.is_file():
        raise FileNotFoundError("source and target databases must both exist")
    raw_map = load_json(replacement_map)
    map_table = map_table or source_table
    map_column = map_column or source_column
    value_map = {
        str(row[2]): str(row[3])
        for row in raw_map[database_id].get("values", [])
        if len(row) == 4
        and str(row[0]) == map_table
        and str(row[1]) == map_column
    }
    if not value_map:
        raise ValueError(
            f"no reviewed values for {database_id}.{map_table}.{map_column}"
        )
    with sqlite3.connect(
        f"file:{source_database}?mode=ro", uri=True
    ) as source_connection:
        source_rows = source_connection.execute(
            f"SELECT {_quote(source_key)}, {_quote(source_column)} "
            f"FROM {_quote(source_table)}"
        ).fetchall()
    with sqlite3.connect(
        f"file:{target_database}?mode={'rw' if apply else 'ro'}", uri=True
    ) as target_connection:
        target_rows = target_connection.execute(
            f"SELECT {_quote(target_key)}, {_quote(target_column)} "
            f"FROM {_quote(target_table)}"
        ).fetchall()
        current = dict(target_rows)
        expected = {
            key: (
                value_map.get(str(value), value)
                if value is not None
                else None
            )
            for key, value in source_rows
        }
        if len(expected) != len(source_rows) or set(expected) != set(current):
            raise ValueError("source and target keys are not one-to-one aligned")
        mismatches = [
            (value, key)
            for key, value in expected.items()
            if current[key] != value
        ]
        if apply and mismatches:
            if backup_path is not None:
                backup_path = backup_path.resolve()
                if backup_path.exists():
                    raise FileExistsError(f"backup already exists: {backup_path}")
                backup_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(target_database, backup_path)
            target_connection.execute("BEGIN IMMEDIATE")
            target_connection.executemany(
                f"UPDATE {_quote(target_table)} "
                f"SET {_quote(target_column)} = ? "
                f"WHERE {_quote(target_key)} = ?",
                mismatches,
            )
            target_connection.commit()
            after = dict(
                target_connection.execute(
                    f"SELECT {_quote(target_key)}, {_quote(target_column)} "
                    f"FROM {_quote(target_table)}"
                ).fetchall()
            )
        else:
            after = current
    mismatches_after = sum(after[key] != value for key, value in expected.items())
    if apply and mismatches_after:
        raise RuntimeError(
            f"mapped-column repair left {mismatches_after} mismatched rows"
        )
    return MappedColumnRepairResult(
        source_rows=len(source_rows),
        target_rows=len(target_rows),
        mapped_values=len(value_map),
        mismatches_before=len(mismatches),
        mismatches_after=mismatches_after,
        applied=apply,
        backup_path=backup_path.as_posix() if backup_path is not None else None,
    )


def restore_ehrsql_eicu_icd9code(
    *,
    source_database: Path,
    target_database: Path,
    apply: bool,
    backup_path: Path | None = None,
) -> FixedPointRepairResult:
    """Restore eICU diagnosis codes by the stable diagnosis primary key.

    The Chinese database translates table/column identifiers, but values in
    ``diagnosis.icd9code`` are medical code identifiers and must be copied
    verbatim from the English source database.
    """

    source_database = source_database.resolve()
    target_database = target_database.resolve()
    if source_database == target_database:
        raise ValueError("source and target databases must differ")
    if not source_database.is_file() or not target_database.is_file():
        raise FileNotFoundError("source and target databases must both exist")
    if backup_path is not None:
        backup_path = backup_path.resolve()
        if backup_path == target_database:
            raise ValueError("backup path must differ from target database")
        if backup_path.exists():
            raise FileExistsError(f"backup already exists: {backup_path}")

    source_uri = f"file:{source_database}?mode=ro"
    target_uri = f"file:{target_database}?mode={'rw' if apply else 'ro'}"
    with sqlite3.connect(source_uri, uri=True) as source_connection:
        source_rows = int(
            source_connection.execute("SELECT COUNT(*) FROM diagnosis").fetchone()[0]
        )
        source_ids = int(
            source_connection.execute(
                "SELECT COUNT(DISTINCT diagnosisid) FROM diagnosis"
            ).fetchone()[0]
        )

    with sqlite3.connect(target_uri, uri=True) as target_connection:
        target_rows = int(
            target_connection.execute('SELECT COUNT(*) FROM "诊断"').fetchone()[0]
        )
        target_ids = int(
            target_connection.execute(
                'SELECT COUNT(DISTINCT "诊断编号") FROM "诊断"'
            ).fetchone()[0]
        )
        target_connection.execute("ATTACH DATABASE ? AS source_db", (source_database.as_posix(),))
        joined_rows = int(
            target_connection.execute(
                'SELECT COUNT(*) FROM "诊断" AS target '
                "JOIN source_db.diagnosis AS source "
                'ON source.diagnosisid = target."诊断编号"'
            ).fetchone()[0]
        )
        if not (
            source_rows
            == source_ids
            == target_rows
            == target_ids
            == joined_rows
        ):
            raise ValueError(
                "diagnosis primary-key alignment failed: "
                f"source_rows={source_rows}, source_ids={source_ids}, "
                f"target_rows={target_rows}, target_ids={target_ids}, "
                f"joined_rows={joined_rows}"
            )
        mismatch_sql = (
            'SELECT COUNT(*) FROM "诊断" AS target '
            "JOIN source_db.diagnosis AS source "
            'ON source.diagnosisid = target."诊断编号" '
            'WHERE target."ICD-9编码" IS NOT source.icd9code'
        )
        mismatches_before = int(target_connection.execute(mismatch_sql).fetchone()[0])
        if apply and mismatches_before:
            if backup_path is not None:
                backup_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(target_database, backup_path)
            target_connection.execute("BEGIN IMMEDIATE")
            target_connection.execute(
                'UPDATE "诊断" AS target SET "ICD-9编码" = ('
                "SELECT source.icd9code FROM source_db.diagnosis AS source "
                'WHERE source.diagnosisid = target."诊断编号")'
            )
            target_connection.commit()
        mismatches_after = int(target_connection.execute(mismatch_sql).fetchone()[0])

    if apply and mismatches_after:
        raise RuntimeError(
            f"fixed-point repair left {mismatches_after} mismatched rows"
        )
    return FixedPointRepairResult(
        source_rows=source_rows,
        target_rows=target_rows,
        mismatches_before=mismatches_before,
        mismatches_after=mismatches_after,
        applied=apply,
        backup_path=backup_path.as_posix() if backup_path is not None else None,
    )
