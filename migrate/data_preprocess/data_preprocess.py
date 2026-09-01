#!/usr/bin/env python3
"""
Preprocess raw datasets into a standardised layout under ``dataset/<name>/``.

After preprocessing, every output directory has the **same** file names:

    <output>/
        database/           -> symlink to source DB dir
        tables.json         copy of schema file (renamed if needed)
        dev.json            copy of dev split  (renamed if needed)
        dev_gold.sql        copy of gold SQL   (optional)

This lets all downstream scripts use identical paths regardless of the
source dataset.  ``--split`` controls which split name is used
(``dev``, ``train``, ``test``).
"""

import csv
import glob
import json
import os
import re
import shutil
import sqlite3
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import STD_DB_DIR, STD_TABLES_FILE, get_config


def _std_split_json(split: str) -> str:
    """e.g. ``dev`` → ``dev.json``"""
    return f"{split}.json"


def _std_split_sql(split: str) -> str:
    """e.g. ``dev`` → ``dev_gold.sql``"""
    return f"{split}_gold.sql"


class _BasePreprocessor:
    """Shared logic for all datasets."""

    def __init__(self, input_path: str, output_path: str, dataset: str, split: str = "dev"):
        self.input_path = os.path.abspath(input_path)
        self.output_path = os.path.abspath(output_path)
        self.dataset = dataset
        self.split = split
        self.cfg = get_config(dataset)

    def _ensure_output(self):
        os.makedirs(self.output_path, exist_ok=True)

    def _normalise_dev_json(self, data: list) -> list:
        """Ensure every entry has ``db_id`` (alias ``db_name`` if needed)."""
        for entry in data:
            if "db_id" not in entry and "db_name" in entry:
                entry["db_id"] = entry["db_name"]
        return data

    def _copy_file(self, src: str, dst: str):
        """Copy a single file (src name may differ from dst name)."""
        if not os.path.exists(src):
            return
        if os.path.exists(dst):
            return
        os.makedirs(os.path.dirname(dst) or ".", exist_ok=True)
        shutil.copy2(src, dst)

    def _symlink_dir(self, src: str, dst: str):
        """Create an absolute symlink to a directory to save storage."""
        if not os.path.exists(src):
            return
        if os.path.exists(dst) or os.path.islink(dst):
            return
        os.makedirs(os.path.dirname(dst) or ".", exist_ok=True)
        os.symlink(os.path.abspath(src), dst)

    def preprocess(self):
        raise NotImplementedError


# ---- source-name → standard-name mapping per dataset ----

# { source_name: standard_function }
# DB dirs and split files are handled separately in each subclass.

class DataPreprocessSpider(_BasePreprocessor):
    """Spider already uses standard names; just symlink the database dir."""

    def __init__(self, input_path: str, output_path: str, split: str = "dev"):
        super().__init__(input_path, output_path, "spider", split)

    def preprocess(self):
        self._ensure_output()
        # dev.json / train.json / test.json  →  <split>.json
        self._copy_file(
            os.path.join(self.input_path, _std_split_json(self.split)),
            os.path.join(self.output_path, _std_split_json(self.split)),
        )
        # tables.json
        self._copy_file(
            os.path.join(self.input_path, STD_TABLES_FILE),
            os.path.join(self.output_path, STD_TABLES_FILE),
        )
        # dev_gold.sql
        src_gold = os.path.join(self.input_path, _std_split_sql(self.split))
        if os.path.exists(src_gold):
            self._copy_file(src_gold, os.path.join(self.output_path, _std_split_sql(self.split)))
        # database/ → symlink
        self._symlink_dir(
            os.path.join(self.input_path, "database"),
            os.path.join(self.output_path, STD_DB_DIR),
        )
        print(f"[Spider] Preprocessed → {self.output_path}")


class DataPreprocessSynSQL(_BasePreprocessor):
    """SynSQL preprocessor.

    SynSQL schema and records follow Spider conventions, with a custom
    dev split file name:

      * ``data-500-dev.json`` for dev
      * ``tables.json`` in Spider format
      * database directory may be ``database/`` or ``databases/``
    """

    _SRC_SPLIT = {"dev": "dev.json"}

    def __init__(self, input_path: str, output_path: str, split: str = "dev"):
        super().__init__(input_path, output_path, "synsql", split)

    def preprocess(self):
        self._ensure_output()

        src_split = self._SRC_SPLIT.get(self.split, _std_split_json(self.split))
        dst_split = os.path.join(self.output_path, _std_split_json(self.split))
        self._copy_file(
            os.path.join(self.input_path, src_split),
            dst_split,
        )

        self._copy_file(
            os.path.join(self.input_path, STD_TABLES_FILE),
            os.path.join(self.output_path, STD_TABLES_FILE),
        )

        # SynSQL stores gold SQL inside split JSON; synthesize <split>_gold.sql
        # in the canonical "<sql>\t<db_id>\n" format expected downstream.
        dst_gold = os.path.join(self.output_path, _std_split_sql(self.split))
        if os.path.exists(dst_split):
            with open(dst_split, "r", encoding="utf-8") as f:
                rows = json.load(f)
            gold_lines = []
            for row in rows:
                sql = (
                    row.get(self.cfg.sql_field)
                    or row.get("query")
                    or row.get("SQL")
                    or row.get("sql")
                    or row.get("sql_query")
                    or ""
                )
                db_id = row.get(self.cfg.db_id_field) or row.get("db_id") or row.get("db_name") or ""
                if sql and db_id:
                    flat_sql = " ".join(str(sql).split())
                    gold_lines.append(f"{flat_sql}\t{db_id}\n")
            with open(dst_gold, "w", encoding="utf-8") as f:
                f.writelines(gold_lines)

        src_db_candidates = [
            os.path.join(self.input_path, "database"),
            os.path.join(self.input_path, "databases"),
        ]
        for src_db in src_db_candidates:
            if os.path.isdir(src_db):
                self._symlink_dir(src_db, os.path.join(self.output_path, STD_DB_DIR))
                break

        print(f"[SynSQL] Preprocessed → {self.output_path}")


class DataPreprocessBIRD(_BasePreprocessor):
    """BIRD uses non-standard names that need renaming."""

    # Source → standard mapping
    _SRC_SPLIT = {"dev": "mini_dev_sqlite.json"}
    _SRC_TABLES = "dev_tables.json"
    _SRC_GOLD = {"dev": "mini_dev_sqlite_gold.sql"}
    _SRC_DB_DIR = "dev_databases"

    def __init__(self, input_path: str, output_path: str, split: str = "dev"):
        super().__init__(input_path, output_path, "bird", split)

    def preprocess(self):
        self._ensure_output()
        # mini_dev_sqlite.json → dev.json
        src_split = self._SRC_SPLIT.get(self.split, _std_split_json(self.split))
        self._copy_file(
            os.path.join(self.input_path, src_split),
            os.path.join(self.output_path, _std_split_json(self.split)),
        )
        # dev_tables.json → tables.json
        self._copy_file(
            os.path.join(self.input_path, self._SRC_TABLES),
            os.path.join(self.output_path, STD_TABLES_FILE),
        )
        # dev_gold.sql → dev_gold.sql (same name but copy anyway)
        src_gold = self._SRC_GOLD.get(self.split)
        if src_gold and os.path.exists(os.path.join(self.input_path, src_gold)):
            self._copy_file(
                os.path.join(self.input_path, src_gold),
                os.path.join(self.output_path, _std_split_sql(self.split)),
            )
        # dev_databases/ → database/
        self._symlink_dir(
            os.path.join(self.input_path, self._SRC_DB_DIR),
            os.path.join(self.output_path, STD_DB_DIR),
        )
        print(f"[BIRD] Preprocessed → {self.output_path}")


class DataPreprocessBULL(_BasePreprocessor):
    """BULL has separate EN/CN database dirs.

    Preprocess into one output per language variant, each with a
    standard ``database/`` symlink pointing to the right source dir.
    Pass ``--lang en`` or ``--lang cn`` to select which.
    """

    def __init__(self, input_path: str, output_path: str, split: str = "dev", lang: str = "en"):
        ds = "BULL-en" if lang == "en" else "BULL-cn"
        super().__init__(input_path, output_path, ds, split)
        self.lang = lang

    def _ensure_sqlite(self, db_dir: str, db_id: str):
        """Materialise ``.sqlite`` from ``.sql`` if the sqlite file is missing."""
        sqlite_path = os.path.join(db_dir, db_id, f"{db_id}.sqlite")
        sql_path = os.path.join(db_dir, db_id, f"{db_id}.sql")
        if not os.path.exists(sqlite_path) and os.path.exists(sql_path):
            conn = sqlite3.connect(sqlite_path)
            with open(sql_path, "r", encoding="utf-8") as f:
                conn.executescript(f.read())
            conn.close()

    def preprocess(self):
        self._ensure_output()
        # dev.json → dev.json  (normalise db_name → db_id)
        src_split = os.path.join(self.input_path, _std_split_json(self.split))
        dst_split = os.path.join(self.output_path, _std_split_json(self.split))
        self._copy_file(src_split, dst_split)
        if os.path.exists(dst_split):
            with open(dst_split, "r", encoding="utf-8") as f:
                data = json.load(f)
            data = self._normalise_dev_json(data)
            with open(dst_split, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

        # tables.json
        self._copy_file(
            os.path.join(self.input_path, STD_TABLES_FILE),
            os.path.join(self.output_path, STD_TABLES_FILE),
        )
        # database_en or database_cn → database/
        src_db = os.path.join(self.input_path, f"database_{self.lang}")
        self._symlink_dir(src_db, os.path.join(self.output_path, STD_DB_DIR))

        # <split>_gold.sql — BULL ships SQL inside dev.json rather than as a
        # separate file, so synthesize it from the `sql_query` + `db_name`
        # fields (canonical "{sql}\t{db_id}\n" format used downstream).
        if os.path.exists(dst_split):
            with open(dst_split, "r", encoding="utf-8") as f:
                data = json.load(f)
            gold_lines = []
            for entry in data:
                sql = (entry.get(self.cfg.sql_field)
                       or entry.get("sql_query")
                       or entry.get("query")
                       or entry.get("SQL", ""))
                db_id = (entry.get(self.cfg.db_id_field)
                         or entry.get("db_id")
                         or entry.get("db_name", ""))
                if sql:
                    gold_lines.append(f"{sql}\t{db_id}\n")
            dst_gold = os.path.join(self.output_path, _std_split_sql(self.split))
            with open(dst_gold, "w", encoding="utf-8") as f:
                f.writelines(gold_lines)

        print(f"[BULL-{self.lang}] Preprocessed → {self.output_path}")


class DataPreprocessSpider2(_BasePreprocessor):
    """Spider2-lite preprocessor (local SQLite subset only).

    Spider2-lite ships an unusual layout:

      * Questions live in ``spider2-lite.jsonl`` (jsonl, not json) with the
        DB id under the field ``db`` instead of ``db_id``.
      * Gold SQL is split into one file per instance under
        ``evaluation_suite/gold/sql/<instance_id>.sql`` (so only a subset of
        instances actually carries a gold query).
      * There is no ``tables.json``. Schemas are described by per-DB
        ``DDL.csv`` files (one row per table containing its raw
        ``CREATE TABLE …`` statement).
      * The real ``.sqlite`` files for the ``local*`` subset are *not*
        shipped in the repo; the user must download the
        ``spider2-localdb`` bundle and unpack it under
        ``resource/databases/spider2-localdb/``.

    This preprocessor only handles the ``local*`` subset (BigQuery /
    Snowflake instances are skipped). It produces the canonical layout
    expected downstream:

        <output>/
            database/<db_id>/<db_id>.sqlite   (symlink into spider2-localdb)
            tables.json                       (parsed from each db's DDL.csv)
            dev.json                          (filtered jsonl, db→db_id, gold attached)
            dev_gold.sql                      (only instances with gold sql)
    """

    _JSONL_FILE = "spider2-lite.jsonl"
    _DDL_BASE_REL = os.path.join("resource", "databases", "sqlite")
    _LOCALDB_REL = os.path.join("resource", "databases", "spider2-localdb")
    _GOLD_SQL_REL = os.path.join("evaluation_suite", "gold", "sql")

    def __init__(self, input_path: str, output_path: str,
                 split: str = "dev", subset: str = "local"):
        super().__init__(input_path, output_path, "spider2", split)
        self.subset = subset

    # ----- DDL parsing helpers -----

    @staticmethod
    def _humanise_name(name: str) -> str:
        """``Perpetrator_ID`` → ``perpetrator id`` (matches Spider conventions)."""
        return re.sub(r"_+", " ", name).strip().lower()

    @staticmethod
    def _normalise_type(raw: str) -> str:
        """Map a SQL type token to one of Spider's canonical types."""
        t = (raw or "").strip().lower()
        if not t:
            return "text"
        if any(k in t for k in ("int", "real", "float", "numeric", "decimal", "double", "number")):
            return "number"
        if any(k in t for k in ("date", "time", "year")):
            return "time"
        if any(k in t for k in ("char", "text", "string", "clob")):
            return "text"
        if any(k in t for k in ("bool", "blob", "json", "uuid", "bytes", "binary")):
            return "others"
        return "text"

    @staticmethod
    def _split_top_level_commas(body: str) -> list:
        """Split a CREATE TABLE body on commas at depth 0 (handles ``VARCHAR(19)``)."""
        parts, depth, buf = [], 0, []
        for ch in body:
            if ch == "(":
                depth += 1
                buf.append(ch)
            elif ch == ")":
                depth = max(0, depth - 1)
                buf.append(ch)
            elif ch == "," and depth == 0:
                parts.append("".join(buf).strip())
                buf = []
            else:
                buf.append(ch)
        tail = "".join(buf).strip()
        if tail:
            parts.append(tail)
        return parts

    @classmethod
    def _parse_create_table(cls, ddl: str):
        """Extract ``([(col, type)], [pk_col], [(from_col, ref_table, ref_col)])``.

        Tolerates the variants we see in Spider2's DDL.csv:
        plain identifiers, backticked / bracketed names, inline ``PRIMARY KEY``
        on a column, separate ``PRIMARY KEY (...)`` / ``FOREIGN KEY (...) REFERENCES ...``
        clauses, and SQLite-style ``IF NOT EXISTS`` headers.
        """
        head_re = re.compile(
            r"CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?"
            r"(?:[`\"\[]?[\w\.\-]+[`\"\]]?\s*\.\s*)?"   # optional schema.
            r"[`\"\[]?[\w\.\-]+[`\"\]]?\s*\(",
            flags=re.IGNORECASE,
        )
        m = head_re.search(ddl)
        if not m:
            return [], [], []
        # Find matching closing paren after the opening one consumed by head_re.
        start = m.end() - 1  # points at "("
        depth = 0
        end = None
        for i in range(start, len(ddl)):
            ch = ddl[i]
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
                if depth == 0:
                    end = i
                    break
        if end is None:
            return [], [], []
        body = ddl[start + 1:end]
        parts = cls._split_top_level_commas(body)

        columns, pk_cols, fk_pairs = [], [], []
        kw_re = re.compile(
            r"^(PRIMARY\s+KEY|FOREIGN\s+KEY|CONSTRAINT|UNIQUE|CHECK|KEY|INDEX)\b",
            re.IGNORECASE,
        )

        def _strip_id(s: str) -> str:
            return s.strip().strip(' `"[]')

        for part in parts:
            part = part.strip().rstrip(",").strip()
            if not part:
                continue
            if kw_re.match(part):
                pk_m = re.match(r"^PRIMARY\s+KEY\s*\(([^)]+)\)", part, re.IGNORECASE)
                if pk_m:
                    pk_cols.extend(_strip_id(c) for c in pk_m.group(1).split(","))
                    continue
                fk_m = re.match(
                    r"^FOREIGN\s+KEY\s*\(([^)]+)\)\s+REFERENCES\s+"
                    r"[`\"\[]?([^\s`\"\[\]\(]+)[`\"\]]?\s*\(([^)]+)\)",
                    part, re.IGNORECASE,
                )
                if fk_m:
                    fcols = [_strip_id(c) for c in fk_m.group(1).split(",")]
                    rtable = _strip_id(fk_m.group(2))
                    rcols = [_strip_id(c) for c in fk_m.group(3).split(",")]
                    for fc, rc in zip(fcols, rcols):
                        fk_pairs.append((fc, rtable, rc))
                continue

            tokens = part.split()
            if not tokens:
                continue
            col_name = _strip_id(tokens[0])
            if not col_name or kw_re.match(col_name):
                continue
            # Spider2's DDL.csv occasionally omits the column type
            # (e.g. ``name UNIQUE`` or just ``name``). Treat the next
            # token as a type only when it's not a column-level keyword
            # like UNIQUE / PRIMARY / NOT / DEFAULT / REFERENCES /
            # COLLATE / CHECK; otherwise leave the type empty so the
            # column is still captured.
            col_type = ""
            if len(tokens) > 1:
                cand = _strip_id(tokens[1].rstrip(","))
                if cand and not re.match(
                    r"^(UNIQUE|PRIMARY|NOT|NULL|DEFAULT|REFERENCES|"
                    r"COLLATE|CHECK|CONSTRAINT|GENERATED|AS)$",
                    cand, re.IGNORECASE,
                ):
                    col_type = cand
            if re.search(r"\bPRIMARY\s+KEY\b", part, re.IGNORECASE):
                pk_cols.append(col_name)
            ref_m = re.search(
                r"\bREFERENCES\s+[`\"\[]?([^\s`\"\[\]\(]+)[`\"\]]?\s*\(([^)]+)\)",
                part, re.IGNORECASE,
            )
            if ref_m:
                rtable = _strip_id(ref_m.group(1))
                rcol = _strip_id(ref_m.group(2).split(",")[0])
                fk_pairs.append((col_name, rtable, rcol))
            columns.append((col_name, col_type))
        return columns, pk_cols, fk_pairs

    @classmethod
    def _build_tables_entry(cls, db_id: str, ddl_csv_path: str):
        """Parse a single ``DDL.csv`` into a Spider-shaped tables.json record."""
        if not os.path.exists(ddl_csv_path):
            return None

        table_names_original = []
        column_names_original = [[-1, "*"]]
        column_types = ["text"]
        pk_indices = []
        deferred_fks = []           # (from_table, from_col, to_table, to_col)
        col_lookup = {}             # (table_name, col_name) -> index

        with open(ddl_csv_path, "r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                table_name = (row.get("table_name")
                              or row.get("Table_Name")
                              or row.get("TABLE_NAME") or "").strip()
                ddl_text = (row.get("DDL")
                            or row.get("ddl")
                            or row.get("Ddl") or "")
                if not table_name or not ddl_text:
                    continue

                t_idx = len(table_names_original)
                table_names_original.append(table_name)

                cols, pk_cols, fk_pairs = cls._parse_create_table(ddl_text)
                for c_name, c_type in cols:
                    col_lookup[(table_name, c_name)] = len(column_names_original)
                    column_names_original.append([t_idx, c_name])
                    column_types.append(cls._normalise_type(c_type))

                for pk in pk_cols:
                    if (table_name, pk) in col_lookup:
                        pk_indices.append(col_lookup[(table_name, pk)])

                for fc, rt, rc in fk_pairs:
                    deferred_fks.append((table_name, fc, rt, rc))

        foreign_keys = []
        for ft, fc, rt, rc in deferred_fks:
            a = col_lookup.get((ft, fc))
            b = col_lookup.get((rt, rc))
            if a is not None and b is not None:
                foreign_keys.append([a, b])

        column_names = []
        for t_idx, name in column_names_original:
            if t_idx == -1:
                column_names.append([-1, "*"])
            else:
                column_names.append([t_idx, cls._humanise_name(name)])

        return {
            "column_names": column_names,
            "column_names_original": column_names_original,
            "column_types": column_types,
            "db_id": db_id,
            "foreign_keys": foreign_keys,
            "primary_keys": sorted(set(pk_indices)),
            "table_names": [cls._humanise_name(t) for t in table_names_original],
            "table_names_original": table_names_original,
        }

    # ----- name resolution (case / separator insensitive) -----

    @staticmethod
    def _norm_id(s: str) -> str:
        """Spider2's jsonl uses casings like ``Db-IMDB`` while the on-disk
        directory is ``DB_IMDB``. Compare ids by lowercasing and stripping
        ``_``/``-`` so we can resolve the canonical name from either side.
        """
        return (s or "").lower().replace("_", "").replace("-", "")

    @classmethod
    def _resolve_db_id(cls, db_id: str, ddl_base: str) -> str:
        """Map ``db_id`` to the actual sqlite/<dir> name under ``ddl_base``.

        Returns the original ``db_id`` if no fuzzy match is found (the
        downstream code will then surface a clear "missing" warning).
        """
        if not db_id:
            return db_id
        if os.path.isdir(os.path.join(ddl_base, db_id)):
            return db_id
        if not os.path.isdir(ddl_base):
            return db_id
        target = cls._norm_id(db_id)
        for entry in os.listdir(ddl_base):
            if cls._norm_id(entry) == target:
                return entry
        return db_id

    # ----- localdb resolution -----

    @classmethod
    def _find_localdb_sqlite(cls, localdb_dir: str, db_id: str):
        """Locate ``<db_id>.sqlite`` under ``spider2-localdb/``.

        Tries flat ``spider2-localdb/<db_id>.sqlite`` and nested
        ``spider2-localdb/<db_id>/<db_id>.sqlite`` first, then falls back
        to a case-/separator-insensitive recursive scan so the bundle's
        casing doesn't have to match the jsonl's.
        """
        if not os.path.isdir(localdb_dir):
            return None
        candidates = [
            os.path.join(localdb_dir, f"{db_id}.sqlite"),
            os.path.join(localdb_dir, db_id, f"{db_id}.sqlite"),
        ]
        for c in candidates:
            if os.path.exists(c):
                return c
        target = cls._norm_id(db_id)
        for root, _, files in os.walk(localdb_dir):
            for fn in files:
                if fn.endswith(".sqlite") and cls._norm_id(fn[:-7]) == target:
                    return os.path.join(root, fn)
        return None

    # ----- main entry point -----

    def preprocess(self):
        self._ensure_output()

        jsonl_path = os.path.join(self.input_path, self._JSONL_FILE)
        if not os.path.exists(jsonl_path):
            raise FileNotFoundError(f"Spider2 jsonl missing: {jsonl_path}")
        with open(jsonl_path, "r", encoding="utf-8") as f:
            rows = [json.loads(l) for l in f if l.strip()]
        rows = [r for r in rows if r.get("instance_id", "").startswith(self.subset)]
        print(f"[Spider2] Filtered subset='{self.subset}*': {len(rows)} instances")

        ddl_base = os.path.join(self.input_path, self._DDL_BASE_REL)
        gold_dir = os.path.join(self.input_path, self._GOLD_SQL_REL)
        out_entries, gold_lines = [], []
        with_gold = 0
        renamed = []
        for r in rows:
            iid = r["instance_id"]
            raw_db_id = r.get("db") or r.get("db_id") or ""
            db_id = self._resolve_db_id(raw_db_id, ddl_base)
            if db_id != raw_db_id:
                renamed.append((raw_db_id, db_id))
            entry = dict(r)
            entry["db_id"] = db_id
            entry.pop("db", None)

            gold_path = os.path.join(gold_dir, f"{iid}.sql")
            if os.path.exists(gold_path):
                with open(gold_path, "r", encoding="utf-8") as gf:
                    sql = gf.read().strip().rstrip(";").strip()
                entry["query"] = sql
                if sql:
                    # dev_gold.sql is one entry per line; collapse Spider2's
                    # multi-line CTE-heavy queries into a single line.
                    flat = re.sub(r"\s+", " ", sql).strip()
                    gold_lines.append(f"{flat}\t{db_id}\n")
                    with_gold += 1
            else:
                entry["query"] = ""
            out_entries.append(entry)
        print(f"[Spider2] Gold SQL attached to {with_gold}/{len(out_entries)} instances")
        if renamed:
            uniq = sorted(set(renamed))
            preview = ", ".join(f"{a}→{b}" for a, b in uniq[:5])
            tail = "…" if len(uniq) > 5 else ""
            print(f"[Spider2] Resolved {len(uniq)} db_id(s) to on-disk casing: {preview}{tail}")

        dev_json_path = os.path.join(self.output_path, _std_split_json(self.split))
        with open(dev_json_path, "w", encoding="utf-8") as f:
            json.dump(out_entries, f, ensure_ascii=False, indent=2)

        gold_json_path = os.path.join(self.output_path, _std_split_sql(self.split))
        with open(gold_json_path, "w", encoding="utf-8") as f:
            f.writelines(gold_lines)

        unique_dbs = sorted({e["db_id"] for e in out_entries if e["db_id"]})
        tables_records = []
        missing_ddl = []
        for db_id in unique_dbs:
            ddl_csv = os.path.join(ddl_base, db_id, "DDL.csv")
            rec = self._build_tables_entry(db_id, ddl_csv)
            if rec is None:
                missing_ddl.append(db_id)
                continue
            tables_records.append(rec)
        if missing_ddl:
            preview = ", ".join(missing_ddl[:5]) + ("…" if len(missing_ddl) > 5 else "")
            print(f"[Spider2] WARNING: missing DDL.csv for {len(missing_ddl)} db(s): {preview}")
        with open(os.path.join(self.output_path, STD_TABLES_FILE), "w", encoding="utf-8") as f:
            json.dump(tables_records, f, ensure_ascii=False, indent=2)
        print(f"[Spider2] Wrote tables.json with {len(tables_records)} databases")

        localdb_dir = os.path.join(self.input_path, self._LOCALDB_REL)
        db_root = os.path.join(self.output_path, STD_DB_DIR)
        os.makedirs(db_root, exist_ok=True)
        linked, missing_sqlite = 0, []
        for db_id in unique_dbs:
            target = self._find_localdb_sqlite(localdb_dir, db_id)
            if target is None:
                missing_sqlite.append(db_id)
                continue
            sub = os.path.join(db_root, db_id)
            os.makedirs(sub, exist_ok=True)
            link = os.path.join(sub, f"{db_id}.sqlite")
            if not os.path.exists(link) and not os.path.islink(link):
                os.symlink(os.path.abspath(target), link)
            linked += 1
        if missing_sqlite:
            preview = ", ".join(missing_sqlite[:5]) + ("…" if len(missing_sqlite) > 5 else "")
            print(f"[Spider2] WARNING: spider2-localdb missing .sqlite for "
                  f"{len(missing_sqlite)} db(s): {preview}")
            print(f"[Spider2]   (expected under {localdb_dir})")
        print(f"[Spider2] Linked {linked}/{len(unique_dbs)} sqlite database(s)")

        print(f"[Spider2] Preprocessed → {self.output_path}")


class DataPreprocessEHRSQL(_BasePreprocessor):
    """EHRSQL preprocessor.

    EHRSQL ships an unusual layout:

      * Two databases (``eicu`` and ``mimic_iii``) each live in their own
        subdirectory with their own ``train.json`` / ``valid.json`` /
        ``test.json`` and their own ``<db>.sqlite``.
      * The combined schema for both DBs is at ``EHRSQL-origin/tables.json``
        (already in canonical Spider shape).
      * ~32% of valid/test items are ``is_impossible: true`` with
        ``query: null`` (unanswerable questions); these cannot flow through
        the SQL/DB translation pipeline.

    This preprocessor maps EHRSQL's ``valid`` split to the canonical
    ``dev.json`` (most dev-set-like in size: 1117+1122=2239 items), splits
    off the unanswerable items into ``dev_unanswerable.json``, and
    materialises the standard layout:

        <output>/
            database/eicu/eicu.sqlite             (symlink)
            database/mimic_iii/mimic_iii.sqlite   (symlink)
            tables.json                           (copy)
            dev.json                              (answerable, eicu+mimic_iii)
            dev_gold.sql                          ("{sql}\\t{db_id}\\n")
            dev_unanswerable.json                 (is_impossible=true items)

    It also emits a one-off ``statistic.json`` at the *origin* root
    (``EHRSQL-origin/statistic.json``) summarising db / table / column /
    row counts per database.
    """

    _SUBDIRS = ("eicu", "mimic_iii")
    # EHRSQL ships train/valid/test but the downstream translation pipeline
    # operates on dev.json — map valid -> dev as the canonical split.
    _SPLIT_TO_SRC = {"dev": "valid.json", "train": "train.json", "test": "test.json"}

    def __init__(self, input_path: str, output_path: str, split: str = "dev"):
        super().__init__(input_path, output_path, "ehrsql", split)

    def _write_statistic_json(self):
        """Compute and write ``EHRSQL-origin/statistic.json``.

        Format:
            {
              "num_dbs": N,
              "dbs": {
                "<db_id>": {
                  "num_tables": M,
                  "tables": {
                    "<table>": {"num_columns": C, "num_rows": R}, ...
                  }
                }, ...
              }
            }
        """
        stats = {"num_dbs": 0, "dbs": {}}
        for db_id in self._SUBDIRS:
            sqlite_path = os.path.join(self.input_path, db_id, f"{db_id}.sqlite")
            if not os.path.exists(sqlite_path):
                continue
            conn = sqlite3.connect(sqlite_path)
            try:
                cur = conn.cursor()
                tables = [
                    r[0] for r in cur.execute(
                        "SELECT name FROM sqlite_master "
                        "WHERE type='table' AND name NOT LIKE 'sqlite_%'"
                    )
                ]
                tbl_stats = {}
                for t in tables:
                    cols = cur.execute(f'PRAGMA table_info("{t}")').fetchall()
                    rows = cur.execute(f'SELECT COUNT(*) FROM "{t}"').fetchone()[0]
                    tbl_stats[t] = {"num_columns": len(cols), "num_rows": rows}
                stats["dbs"][db_id] = {
                    "num_tables": len(tables),
                    "tables": tbl_stats,
                }
                stats["num_dbs"] += 1
            finally:
                conn.close()

        stat_path = os.path.join(self.input_path, "statistic.json")
        with open(stat_path, "w", encoding="utf-8") as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)
        total_tables = sum(v["num_tables"] for v in stats["dbs"].values())
        print(
            f"[EHRSQL] Wrote statistic.json "
            f"({stats['num_dbs']} db, {total_tables} tables) → {stat_path}"
        )

    def preprocess(self):
        self._ensure_output()

        # 1) statistic.json on the *origin* root (per user spec).
        self._write_statistic_json()

        # 2) tables.json copy (canonical Spider shape; covers both DBs).
        self._copy_file(
            os.path.join(self.input_path, STD_TABLES_FILE),
            os.path.join(self.output_path, STD_TABLES_FILE),
        )

        # 3) Symlink each DB into the canonical database/<db_id>/<db_id>.sqlite layout.
        db_root = os.path.join(self.output_path, STD_DB_DIR)
        os.makedirs(db_root, exist_ok=True)
        for db_id in self._SUBDIRS:
            src_sqlite = os.path.join(self.input_path, db_id, f"{db_id}.sqlite")
            if not os.path.exists(src_sqlite):
                print(f"[EHRSQL] WARNING: missing {src_sqlite}")
                continue
            sub = os.path.join(db_root, db_id)
            os.makedirs(sub, exist_ok=True)
            link = os.path.join(sub, f"{db_id}.sqlite")
            if not (os.path.exists(link) or os.path.islink(link)):
                os.symlink(os.path.abspath(src_sqlite), link)

        # 4) Merge per-DB split files into a single dev.json (answerable only)
        #    and a dev_unanswerable.json (is_impossible == true).
        src_split_file = self._SPLIT_TO_SRC.get(self.split, _std_split_json(self.split))
        merged_ok, merged_imp = [], []
        for db_id in self._SUBDIRS:
            split_path = os.path.join(self.input_path, db_id, src_split_file)
            if not os.path.exists(split_path):
                print(f"[EHRSQL] WARNING: missing {split_path}")
                continue
            with open(split_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            for entry in data:
                entry = self._normalise_dev_json([entry])[0]
                # EHRSQL already carries db_id; just safety-net it.
                if not entry.get("db_id"):
                    entry["db_id"] = db_id
                # ``is_impossible`` items have ``query: null`` and cannot flow
                # through database_translate.py; route them to the
                # unanswerable file.
                if entry.get("is_impossible") or not entry.get("query"):
                    merged_imp.append(entry)
                else:
                    merged_ok.append(entry)

        dev_json_path = os.path.join(self.output_path, _std_split_json(self.split))
        with open(dev_json_path, "w", encoding="utf-8") as f:
            json.dump(merged_ok, f, ensure_ascii=False, indent=2)

        if merged_imp:
            imp_path = os.path.join(
                self.output_path, f"{self.split}_unanswerable.json"
            )
            with open(imp_path, "w", encoding="utf-8") as f:
                json.dump(merged_imp, f, ensure_ascii=False, indent=2)

        # 5) Synthesize dev_gold.sql ("{sql}\t{db_id}\n", one line per answerable item).
        gold_lines = []
        for e in merged_ok:
            sql = e.get(self.cfg.sql_field) or e.get("query") or ""
            db_id = e.get("db_id", "")
            if sql:
                gold_lines.append(f"{sql}\t{db_id}\n")
        gold_path = os.path.join(self.output_path, _std_split_sql(self.split))
        with open(gold_path, "w", encoding="utf-8") as f:
            f.writelines(gold_lines)

        print(
            f"[EHRSQL] Preprocessed → {self.output_path} "
            f"(answerable={len(merged_ok)}, unanswerable={len(merged_imp)})"
        )


class DataPreprocessLogicCat(_BasePreprocessor):
    """LogicCat preprocessor.

    LogicCat origin layout:
      * ``dev_500.json`` / ``dev_800.json`` / ``train.json`` / ``test.json``
      * ``table_traindev.json`` and ``table_test.json``
      * ``database/*.sql`` (one SQL script per DB)

    This preprocessor creates canonical files and materialises sqlite DBs as:
      ``database/<db_id>/<db_id>.sqlite``.
    """

    _SRC_SPLIT = {
        "dev": "dev_500.json",
        "train": "train.json",
        "test": "test.json",
    }
    _SRC_TABLES = {
        "dev": "table_traindev.json",
        "train": "table_traindev.json",
        "test": "table_test.json",
    }

    def __init__(self, input_path: str, output_path: str, split: str = "dev"):
        super().__init__(input_path, output_path, "logiccat", split)

    @staticmethod
    def _mysql_to_sqlite_script(sql_text: str) -> str:
        """Convert a MySQL dump into SQLite-compatible SQL (best effort)."""
        script = re.sub(r"/\*.*?\*/", "", sql_text, flags=re.DOTALL)
        lines = []
        for raw in script.splitlines():
            line = raw.strip()
            if not line:
                continue

            upper = line.upper()
            if (
                upper.startswith("SET ")
                or upper.startswith("LOCK TABLES")
                or upper.startswith("UNLOCK TABLES")
                or upper.startswith("DELIMITER ")
            ):
                continue

            # Drop MySQL secondary index lines from CREATE TABLE;
            # queries in this pipeline do not depend on those indexes.
            if re.match(r"^\s*(UNIQUE\s+)?KEY\b", line, flags=re.IGNORECASE):
                continue
            if re.match(r"^\s*INDEX\b", line, flags=re.IGNORECASE):
                continue

            line = line.replace("`", '"')
            line = re.sub(
                r"\s+COMMENT\s+'(?:\\'|''|[^'])*'",
                "",
                line,
                flags=re.IGNORECASE,
            )
            line = re.sub(r"\benum\s*\([^)]*\)", "TEXT", line, flags=re.IGNORECASE)
            line = re.sub(r"\s+CHARACTER\s+SET\s+\w+", "", line, flags=re.IGNORECASE)
            line = re.sub(r"\s+COLLATE\s+\w+", "", line, flags=re.IGNORECASE)
            line = re.sub(r"\s+UNSIGNED\b", "", line, flags=re.IGNORECASE)
            line = re.sub(r"\s+AUTO_INCREMENT\b", "", line, flags=re.IGNORECASE)
            line = re.sub(r"\s+USING\s+BTREE\b", "", line, flags=re.IGNORECASE)
            line = re.sub(r"\bCURRENT_TIMESTAMP\(\d+\)", "CURRENT_TIMESTAMP", line, flags=re.IGNORECASE)
            line = re.sub(
                r"\s+ON\s+UPDATE\s+CURRENT_TIMESTAMP(?:\(\d+\)|\(\))?\b",
                "",
                line,
                flags=re.IGNORECASE,
            )
            line = re.sub(r"\)\s*ENGINE\s*=\s*[^;]*;", ");", line, flags=re.IGNORECASE)
            lines.append(line)

        cleaned = "\n".join(lines)
        cleaned = re.sub(r",\s*\)", "\n)", cleaned)
        return cleaned + "\n"

    def _materialize_sqlite(self, src_sql_path: str, dst_sqlite_path: str):
        os.makedirs(os.path.dirname(dst_sqlite_path), exist_ok=True)
        if os.path.exists(dst_sqlite_path):
            os.remove(dst_sqlite_path)
        conn = sqlite3.connect(dst_sqlite_path)
        try:
            with open(src_sql_path, "r", encoding="utf-8") as f:
                sql = self._mysql_to_sqlite_script(f.read())
            conn.execute("PRAGMA foreign_keys = OFF;")
            for stmt in sql.split(";"):
                statement = stmt.strip()
                if not statement:
                    continue
                try:
                    conn.execute(statement)
                except Exception:
                    # LogicCat SQL dumps contain some MySQL-only statements/
                    # values. Continue so we can still materialize usable DBs.
                    continue
            conn.commit()
            cur = conn.cursor()
            cur.execute(
                "SELECT COUNT(*) FROM sqlite_master "
                "WHERE type='table' AND name NOT LIKE 'sqlite_%'"
            )
            table_count = int(cur.fetchone()[0])
            if table_count <= 0:
                raise RuntimeError("no tables created from SQL script")
        finally:
            conn.close()

    def preprocess(self):
        self._ensure_output()

        src_split_name = self._SRC_SPLIT.get(self.split, _std_split_json(self.split))
        src_split_path = os.path.join(self.input_path, src_split_name)
        if not os.path.exists(src_split_path):
            raise FileNotFoundError(f"[LogicCat] Missing split file: {src_split_path}")
        with open(src_split_path, "r", encoding="utf-8") as f:
            rows = json.load(f)
        rows = self._normalise_dev_json(rows)

        out_split = os.path.join(self.output_path, _std_split_json(self.split))
        with open(out_split, "w", encoding="utf-8") as f:
            json.dump(rows, f, ensure_ascii=False, indent=2)

        out_gold = os.path.join(self.output_path, _std_split_sql(self.split))
        with open(out_gold, "w", encoding="utf-8") as f:
            for row in rows:
                sql = (row.get("query") or row.get("sql_query") or row.get("SQL") or "").strip()
                db_id = (row.get("db_id") or row.get("db_name") or "").strip()
                if sql and db_id:
                    f.write(f"{sql}\t{db_id}\n")

        src_tables_name = self._SRC_TABLES.get(self.split, STD_TABLES_FILE)
        src_tables_path = os.path.join(self.input_path, src_tables_name)
        if not os.path.exists(src_tables_path):
            raise FileNotFoundError(f"[LogicCat] Missing tables file: {src_tables_path}")
        with open(src_tables_path, "r", encoding="utf-8") as f:
            raw_tables = json.load(f)
        active_db_ids = {str(row.get("db_id") or row.get("db_name") or "").strip() for row in rows}
        active_db_ids.discard("")
        tables = []
        for entry in raw_tables:
            db_id = str(entry.get("db_id", "")).strip()
            if active_db_ids and db_id not in active_db_ids:
                continue
            norm = dict(entry)
            if "table_names_original" not in norm and "table_names" in norm:
                norm["table_names_original"] = norm.get("table_names", [])
            if "column_names_original" not in norm and "column_names" in norm:
                norm["column_names_original"] = norm.get("column_names", [])
            tables.append(norm)
        with open(os.path.join(self.output_path, STD_TABLES_FILE), "w", encoding="utf-8") as f:
            json.dump(tables, f, ensure_ascii=False, indent=2)

        src_db_root = os.path.join(self.input_path, "database")
        if not os.path.isdir(src_db_root):
            raise FileNotFoundError(f"[LogicCat] Missing database dir: {src_db_root}")
        out_db_root = os.path.join(self.output_path, STD_DB_DIR)
        if os.path.lexists(out_db_root):
            if os.path.islink(out_db_root) or os.path.isfile(out_db_root):
                os.remove(out_db_root)
            else:
                shutil.rmtree(out_db_root)
        os.makedirs(out_db_root, exist_ok=True)

        sqlite_built = 0
        sqlite_failed = 0
        for filename in sorted(os.listdir(src_db_root)):
            if not filename.lower().endswith(".sql"):
                continue
            db_id = os.path.splitext(filename)[0]
            src_sql = os.path.join(src_db_root, filename)
            dst_sqlite = os.path.join(out_db_root, db_id, f"{db_id}.sqlite")
            try:
                self._materialize_sqlite(src_sql, dst_sqlite)
                sqlite_built += 1
            except Exception as exc:  # noqa: BLE001 - keep processing remaining DBs
                sqlite_failed += 1
                print(f"[LogicCat] WARNING: failed to build sqlite for {db_id}: {exc}")

        print(
            f"[LogicCat] Preprocessed → {self.output_path} "
            f"(rows={len(rows)}, sqlite_built={sqlite_built}, sqlite_failed={sqlite_failed})"
        )


class DataPreprocessKaggleDBQA(_BasePreprocessor):
    """KaggleDBQA preprocessor.

    Expected origin layout:
      * ``samples/*_test.json``: Spider-style rows (``db_id``, ``query``, ``question``)
      * ``database/`` (or ``databases/``): sqlite files per DB
      * optional ``tables.json``
    """

    def __init__(self, input_path: str, output_path: str, split: str = "dev"):
        super().__init__(input_path, output_path, "kaggledbqa", split)

    @staticmethod
    def _normalise_type(type_str: str) -> str:
        t = (type_str or "").lower()
        if any(k in t for k in ("int", "numeric", "real", "double", "float", "decimal")):
            return "number"
        if "bool" in t:
            return "boolean"
        if any(k in t for k in ("date", "time")):
            return "time"
        return "text"

    @staticmethod
    def _table_count(sqlite_path: str) -> int:
        try:
            conn = sqlite3.connect(sqlite_path)
            try:
                cur = conn.cursor()
                cur.execute(
                    "SELECT COUNT(*) FROM sqlite_master "
                    "WHERE type='table' AND name NOT LIKE 'sqlite_%'"
                )
                row = cur.fetchone()
                return int(row[0]) if row else 0
            finally:
                conn.close()
        except Exception:
            return -1

    def _find_sample_files(self):
        pattern = os.path.join(self.input_path, "samples", "*_test.json")
        return sorted(glob.glob(pattern))

    def _resolve_db_root(self) -> str:
        candidates = [
            os.path.join(self.input_path, "database"),
            os.path.join(self.input_path, "databases"),
            os.path.join(self.input_path, "database", "databases"),
        ]
        for path in candidates:
            if os.path.isdir(path):
                return path
        return ""

    def _discover_sqlite_files(self, db_root: str):
        files = []
        if not db_root:
            return files
        for root, _, names in os.walk(db_root):
            for name in names:
                if not (name.endswith(".sqlite") or name.endswith(".db")):
                    continue
                fp = os.path.join(root, name)
                if self._table_count(fp) > 0:
                    files.append(fp)
        return files

    @staticmethod
    def _build_sqlite_index(sqlite_files):
        index = {}
        for fp in sqlite_files:
            stem = os.path.splitext(os.path.basename(fp))[0]
            parent = os.path.basename(os.path.dirname(fp))
            index.setdefault(stem, []).append(fp)
            index.setdefault(parent, []).append(fp)
        return index

    def _pick_sqlite_for_db(self, db_id: str, sqlite_index: dict):
        candidates = sqlite_index.get(db_id, [])
        if not candidates:
            return None
        preferred = []
        for fp in candidates:
            parent = os.path.basename(os.path.dirname(fp))
            stem = os.path.splitext(os.path.basename(fp))[0]
            if stem == db_id and parent == db_id:
                preferred.append((0, fp))
            elif stem == db_id:
                preferred.append((1, fp))
            elif parent == db_id:
                preferred.append((2, fp))
            else:
                preferred.append((3, fp))
        preferred.sort(key=lambda x: (x[0], x[1]))
        return preferred[0][1]

    def _build_tables_entry_from_sqlite(self, db_id: str, sqlite_path: str):
        table_names_original = []
        table_names = []
        column_names_original = [[-1, "*"]]
        column_names = [[-1, "*"]]
        column_types = ["text"]
        primary_keys = []
        foreign_keys = []
        col_lookup = {}

        conn = sqlite3.connect(sqlite_path)
        try:
            cur = conn.cursor()
            tables = [
                r[0]
                for r in cur.execute(
                    "SELECT name FROM sqlite_master "
                    "WHERE type='table' AND name NOT LIKE 'sqlite_%' "
                    "ORDER BY name"
                ).fetchall()
            ]
            for t_name in tables:
                t_idx = len(table_names_original)
                table_names_original.append(t_name)
                table_names.append(t_name)

                safe_t = t_name.replace('"', '""')
                cols = cur.execute(f'PRAGMA table_info("{safe_t}")').fetchall()
                for col in cols:
                    c_name = str(col[1])
                    c_type = str(col[2] or "")
                    column_names_original.append([t_idx, c_name])
                    column_names.append([t_idx, c_name])
                    column_types.append(self._normalise_type(c_type))
                    col_idx = len(column_names_original) - 1
                    col_lookup[(t_name, c_name)] = col_idx
                    if int(col[5] or 0) > 0:
                        primary_keys.append(col_idx)

            for t_name in tables:
                safe_t = t_name.replace('"', '""')
                fks = cur.execute(f'PRAGMA foreign_key_list("{safe_t}")').fetchall()
                for fk in fks:
                    ref_table = str(fk[2])
                    from_col = str(fk[3])
                    to_col = str(fk[4])
                    a = col_lookup.get((t_name, from_col))
                    b = col_lookup.get((ref_table, to_col))
                    if a is not None and b is not None:
                        foreign_keys.append([a, b])
        finally:
            conn.close()

        return {
            "db_id": db_id,
            "table_names_original": table_names_original,
            "table_names": table_names,
            "column_names_original": column_names_original,
            "column_names": column_names,
            "column_types": column_types,
            "primary_keys": sorted(set(primary_keys)),
            "foreign_keys": foreign_keys,
        }

    def preprocess(self):
        self._ensure_output()

        sample_files = self._find_sample_files()
        if not sample_files:
            raise FileNotFoundError(
                f"[KaggleDBQA] No test sample files found under {self.input_path}/samples/*_test.json"
            )

        rows = []
        for sample_path in sample_files:
            with open(sample_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if not isinstance(data, list):
                continue
            for entry in data:
                if not isinstance(entry, dict):
                    continue
                row = dict(entry)
                if "db_id" not in row and "db_name" in row:
                    row["db_id"] = row.get("db_name")
                rows.append(row)

        rows = self._normalise_dev_json(rows)
        rows.sort(key=lambda x: (str(x.get("db_id", "")), str(x.get("question", ""))))

        out_split = os.path.join(self.output_path, _std_split_json(self.split))
        with open(out_split, "w", encoding="utf-8") as f:
            json.dump(rows, f, ensure_ascii=False, indent=2)

        out_gold = os.path.join(self.output_path, _std_split_sql(self.split))
        with open(out_gold, "w", encoding="utf-8") as f:
            for row in rows:
                sql = (
                    row.get(self.cfg.sql_field)
                    or row.get("query")
                    or row.get("SQL")
                    or row.get("sql_query")
                    or row.get("sql")
                    or ""
                )
                db_id = row.get("db_id") or row.get("db_name") or ""
                if sql and db_id:
                    f.write(f"{sql}\t{db_id}\n")

        src_tables = os.path.join(self.input_path, STD_TABLES_FILE)
        active_db_ids = {str(r.get("db_id") or r.get("db_name") or "").strip() for r in rows}
        active_db_ids.discard("")

        db_root = self._resolve_db_root()
        sqlite_files = self._discover_sqlite_files(db_root)
        sqlite_index = self._build_sqlite_index(sqlite_files)

        out_db_root = os.path.join(self.output_path, STD_DB_DIR)
        if os.path.lexists(out_db_root):
            if os.path.islink(out_db_root) or os.path.isfile(out_db_root):
                os.remove(out_db_root)
            else:
                shutil.rmtree(out_db_root)
        os.makedirs(out_db_root, exist_ok=True)

        linked_sqlite = 0
        missing_sqlite = 0
        tables = []
        for db_id in sorted(active_db_ids):
            sqlite_src = self._pick_sqlite_for_db(db_id, sqlite_index)
            if sqlite_src is None:
                missing_sqlite += 1
                continue

            sub = os.path.join(out_db_root, db_id)
            os.makedirs(sub, exist_ok=True)
            dst_sqlite = os.path.join(sub, f"{db_id}.sqlite")
            if os.path.lexists(dst_sqlite):
                os.remove(dst_sqlite)
            os.symlink(os.path.abspath(sqlite_src), dst_sqlite)
            linked_sqlite += 1

            try:
                tables.append(self._build_tables_entry_from_sqlite(db_id, sqlite_src))
            except Exception as exc:  # noqa: BLE001
                print(f"[KaggleDBQA] WARNING: failed to inspect schema for {db_id}: {exc}")

        if os.path.isfile(src_tables):
            self._copy_file(src_tables, os.path.join(self.output_path, STD_TABLES_FILE))
        else:
            with open(os.path.join(self.output_path, STD_TABLES_FILE), "w", encoding="utf-8") as f:
                json.dump(tables, f, ensure_ascii=False, indent=2)

        print(
            f"[KaggleDBQA] Preprocessed -> {self.output_path} "
            f"(rows={len(rows)}, dbs={len(active_db_ids)}, sqlite_linked={linked_sqlite}, "
            f"sqlite_missing={missing_sqlite}, sample_files={len(sample_files)})"
        )


class DataPreprocessTACO(_BasePreprocessor):
    """TACO-Beijing preprocessor.

    TACO-Beijing origin layout:

      * ``natural_language_queries/<db_name>/*.json``: one JSON file per
        question, each carrying ``natural_language_query`` + ``sql``.
      * ``natural_language_queries/cross_database/*.json``: cross-DB queries
        (skip for single-db benchmark variants).
      * ``databases/<db_name>/<db_name>.json``: schema metadata per DB.

    This preprocessor builds a canonical split under ``<output>/`` with:

        database/      (copied DB dirs; only <db_id>.json + <db_id>.sqlite)
        tables.json    (Spider-shaped schema built from per-db JSON files)
        dev.json       (BIRD-style rows)
        dev_gold.sql   ("{sql}\\t{db_id}\\n")
    """

    _NL_DIR = "natural_language_queries"
    _DB_DIR = "databases"

    def __init__(self, input_path: str, output_path: str, split: str = "dev"):
        super().__init__(input_path, output_path, "taco", split)

    @staticmethod
    def _normalise_type(raw_type: str) -> str:
        t = (raw_type or "").strip().lower()
        if not t:
            return "text"
        if any(k in t for k in ("int", "long", "short")):
            return "number"
        if any(k in t for k in ("real", "float", "double", "decimal", "numeric")):
            return "number"
        if "bool" in t:
            return "boolean"
        if any(k in t for k in ("date", "time", "year", "timestamp")):
            return "time"
        return "text"

    @staticmethod
    def _difficulty_from_metadata(meta: dict) -> str:
        if not isinstance(meta, dict):
            return "unknown"
        if meta.get("has_subquery"):
            return "hard"
        if meta.get("has_join") or meta.get("has_aggregate"):
            return "medium"
        return "simple"

    @staticmethod
    def _extract_question_id(filename: str, fallback: int) -> int:
        m = re.search(r"(\d+)", os.path.basename(filename))
        if m:
            try:
                return int(m.group(1))
            except ValueError:
                pass
        return fallback

    @staticmethod
    def _table_count(db_path: str) -> int:
        """Best-effort table count for a SQLite file (-1 on failure)."""
        if not os.path.isfile(db_path):
            return -1
        try:
            conn = sqlite3.connect(db_path)
            try:
                cur = conn.cursor()
                cur.execute(
                    "SELECT COUNT(*) FROM sqlite_master "
                    "WHERE type='table' AND name NOT LIKE 'sqlite_%'"
                )
                row = cur.fetchone()
                return int(row[0]) if row else 0
            finally:
                conn.close()
        except Exception:
            return -1

    def _find_sqlite_source(self, db_dir: str, db_id: str):
        """Find a populated sqlite/db file usable as ``<db_id>.sqlite``."""
        preferred = [
            os.path.join(db_dir, f"{db_id}.sqlite"),
            os.path.join(db_dir, f"{db_id}.db"),
        ]
        others = []
        for fn in sorted(os.listdir(db_dir)):
            fp = os.path.join(db_dir, fn)
            if not os.path.isfile(fp):
                continue
            if fn.endswith(".sqlite") or fn.endswith(".db"):
                if fp not in preferred:
                    others.append(fp)
        candidates = preferred + others
        for fp in candidates:
            if self._table_count(fp) > 0:
                return fp
        return None

    def _copy_taco_databases(self, src_db_root: str, dst_db_root: str) -> tuple[int, int]:
        """Copy DB dirs with only ``<db_id>.json`` and ``<db_id>.sqlite`` files."""
        copied_sqlite = 0
        missing_sqlite = 0
        for db_id in sorted(os.listdir(src_db_root)):
            src_db_dir = os.path.join(src_db_root, db_id)
            if not os.path.isdir(src_db_dir):
                continue

            dst_db_dir = os.path.join(dst_db_root, db_id)
            os.makedirs(dst_db_dir, exist_ok=True)

            src_json = os.path.join(src_db_dir, f"{db_id}.json")
            dst_json = os.path.join(dst_db_dir, f"{db_id}.json")
            if os.path.isfile(src_json):
                shutil.copy2(src_json, dst_json)

            sqlite_source = self._find_sqlite_source(src_db_dir, db_id)
            if sqlite_source is None:
                missing_sqlite += 1
                continue
            dst_sqlite = os.path.join(dst_db_dir, f"{db_id}.sqlite")
            shutil.copy2(sqlite_source, dst_sqlite)
            copied_sqlite += 1

        return copied_sqlite, missing_sqlite

    def _build_tables_entry(self, db_id: str, schema_path: str):
        if not os.path.exists(schema_path):
            return None
        with open(schema_path, "r", encoding="utf-8") as f:
            raw = json.load(f)

        tables = raw.get("tables", [])
        table_names_original = []
        table_names = []
        column_names_original = [[-1, "*"]]
        column_names = [[-1, "*"]]
        column_types = ["text"]
        primary_keys = []
        foreign_keys = []
        col_lookup = {}  # (table_name, col_name) -> global column index

        for t_idx, table in enumerate(tables):
            t_name = (table.get("table_name") or table.get("name") or "").strip()
            if not t_name:
                continue
            table_names_original.append(t_name)
            table_names.append(table.get("table_comment") or t_name)

            cols = table.get("columns", [])
            for col in cols:
                c_name = (col.get("column_name") or col.get("name") or "").strip()
                if not c_name:
                    continue
                col_lookup[(t_name, c_name)] = len(column_names_original)
                column_names_original.append([len(table_names_original) - 1, c_name])
                column_names.append([len(table_names_original) - 1, c_name])
                column_types.append(self._normalise_type(col.get("data_type", "")))

            for pk in table.get("primary_keys", []) or []:
                pk_name = pk.get("column_name") if isinstance(pk, dict) else str(pk)
                idx = col_lookup.get((t_name, pk_name))
                if idx is not None:
                    primary_keys.append(idx)

        for table in tables:
            t_name = (table.get("table_name") or table.get("name") or "").strip()
            for fk in table.get("foreign_keys", []) or []:
                if not isinstance(fk, dict):
                    continue
                from_col = (fk.get("column_name") or fk.get("from_column") or "").strip()
                ref_table = (fk.get("referenced_table") or fk.get("to_table") or "").strip()
                ref_col = (fk.get("referenced_column") or fk.get("to_column") or "").strip()
                a = col_lookup.get((t_name, from_col))
                b = col_lookup.get((ref_table, ref_col))
                if a is not None and b is not None:
                    foreign_keys.append([a, b])

        return {
            "db_id": db_id,
            "table_names_original": table_names_original,
            "table_names": table_names,
            "column_names_original": column_names_original,
            "column_names": column_names,
            "column_types": column_types,
            "primary_keys": sorted(set(primary_keys)),
            "foreign_keys": foreign_keys,
        }

    def preprocess(self):
        self._ensure_output()

        nl_root = os.path.join(self.input_path, self._NL_DIR)
        db_root = os.path.join(self.input_path, self._DB_DIR)
        if not os.path.isdir(nl_root):
            raise FileNotFoundError(f"[TACO] Missing NL root: {nl_root}")
        if not os.path.isdir(db_root):
            raise FileNotFoundError(f"[TACO] Missing DB root: {db_root}")

        rows = []
        serial = 1
        skipped_cross = 0
        skipped_no_sql = 0

        for root, _, files in os.walk(nl_root):
            rel = os.path.relpath(root, nl_root)
            if rel == ".":
                continue
            top = rel.split(os.sep)[0]
            if top == "cross_database":
                skipped_cross += len([f for f in files if f.lower().endswith(".json")])
                continue

            for name in sorted(files):
                if not name.lower().endswith(".json"):
                    continue
                path = os.path.join(root, name)
                with open(path, "r", encoding="utf-8") as f:
                    item = json.load(f)

                meta = item.get("metadata", {})
                if isinstance(meta, dict) and meta.get("is_cross_database"):
                    skipped_cross += 1
                    continue

                sql = str(item.get("sql") or item.get("SQL") or "").strip()
                item.pop("sql", None)
                item.pop("SQL", None)
                if not sql:
                    skipped_no_sql += 1
                    continue

                db_id = (item.get("database") or top or "").strip()
                item.pop("database")
                if not db_id:
                    skipped_no_sql += 1
                    continue

                question = (item.get("natural_language_query")
                            or item.get("question")
                            or "").strip()
                item.pop("natural_language_query", None)
                item.pop("question", None)
                q_id = self._extract_question_id(name, serial)
                serial += 1

                evidence = item.get("evidence", "")
                item.pop("evidence", None)

                difficulty = item.get("difficulty")
                item.pop("difficulty", None)

                row = {}
                row["question_id"] = q_id
                row["db_id"] = db_id
                row["question"] = question
                row["evidence"] = evidence
                row["SQL"] = sql
                row["difficulty"] = difficulty
                row.update(item)
                rows.append(row)

        rows.sort(key=lambda x: (str(x.get("db_id", "")), int(x.get("question_id", 0))))
        dev_path = os.path.join(self.output_path, _std_split_json(self.split))
        with open(dev_path, "w", encoding="utf-8") as f:
            json.dump(rows, f, ensure_ascii=False, indent=2)

        gold_path = os.path.join(self.output_path, _std_split_sql(self.split))
        with open(gold_path, "w", encoding="utf-8") as f:
            for row in rows:
                f.write(f"{row.get('SQL', '')}\t{row.get('db_id', '')}\n")

        tables = []
        for db_file in sorted(os.listdir(db_root)):
            schema_path = os.path.join(db_root, db_file, f"{db_file}.json")
            if not os.path.isfile(schema_path):
                continue
            entry = self._build_tables_entry(db_file, schema_path)
            if entry is not None:
                tables.append(entry)
        total_tables = sum(len(t.get("table_names_original", [])) for t in tables)
        tables_path = os.path.join(self.output_path, STD_TABLES_FILE)
        with open(tables_path, "w", encoding="utf-8") as f:
            json.dump(tables, f, ensure_ascii=False, indent=2)

        out_db_root = os.path.join(self.output_path, STD_DB_DIR)
        if os.path.lexists(out_db_root):
            if os.path.islink(out_db_root) or os.path.isfile(out_db_root):
                os.remove(out_db_root)
            else:
                shutil.rmtree(out_db_root)
        os.makedirs(out_db_root, exist_ok=True)
        copied_sqlite, missing_sqlite = self._copy_taco_databases(db_root, out_db_root)

        print(
            f"[TACO] Preprocessed -> {self.output_path} "
            f"(rows={len(rows)}, dbs={len(tables)}, total_tables={total_tables}, "
            f"skipped_cross={skipped_cross}, skipped_no_sql={skipped_no_sql}, "
            f"sqlite_copied={copied_sqlite}, sqlite_missing={missing_sqlite})"
        )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Preprocess raw dataset into standard layout "
                    "(database/, tables.json, <split>.json, <split>_gold.sql)."
    )
    parser.add_argument("--dataset",
                        choices=["spider", "synsql", "spider2", "bird", "bull", "ehrsql", "logiccat", "kaggledbqa", "taco"],
                        required=True)
    parser.add_argument("--input", required=True, help="Path to raw dataset")
    parser.add_argument("--output", required=True, help="Output directory")
    parser.add_argument("--split", default="dev", choices=["dev", "train", "test"],
                        help="Data split to preprocess (default: dev)")
    parser.add_argument("--lang", default="en", choices=["en", "cn"],
                        help="Language variant for BULL (default: en)")
    parser.add_argument("--subset", default="local",
                        help="Spider2-only: instance-id prefix to keep (default: local)")
    args = parser.parse_args()

    if args.dataset == "spider":
        DataPreprocessSpider(args.input, args.output, args.split).preprocess()
    elif args.dataset == "synsql":
        DataPreprocessSynSQL(args.input, args.output, args.split).preprocess()
    elif args.dataset == "spider2":
        DataPreprocessSpider2(args.input, args.output, args.split, args.subset).preprocess()
    elif args.dataset == "bird":
        DataPreprocessBIRD(args.input, args.output, args.split).preprocess()
    elif args.dataset == "bull":
        DataPreprocessBULL(args.input, args.output, args.split, args.lang).preprocess()
    elif args.dataset == "ehrsql":
        DataPreprocessEHRSQL(args.input, args.output, args.split).preprocess()
    elif args.dataset == "logiccat":
        DataPreprocessLogicCat(args.input, args.output, args.split).preprocess()
    elif args.dataset == "kaggledbqa":
        DataPreprocessKaggleDBQA(args.input, args.output, args.split).preprocess()
    elif args.dataset == "taco":
        DataPreprocessTACO(args.input, args.output, args.split).preprocess()
