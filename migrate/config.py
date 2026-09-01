"""
Dataset registry and shared configuration for CrossLangSQL.

After preprocessing, every dataset directory uses a **canonical** layout:

    dataset/<name>/
        database/           symlink to source DB dir
        tables.json         schema file
        dev.json            dev-split questions   (or train/test)
        dev_gold.sql        gold SQL              (optional)

Each dataset variant gets its **own** directory, so ``dev_file``,
``tables_file``, ``db_subdir``, and ``gold_file`` are always the
standard defaults.  Only behavioural knobs (``sql_field``,
``has_evidence``, …) differ between entries.
"""

from dataclasses import dataclass
from typing import Optional

# Canonical file / directory names (never overridden per dataset)
STD_TABLES_FILE = "tables.json"
STD_DB_DIR = "database"

# Split-specific file names
STD_DEV_JSON_FILE = "dev.json"
STD_DEV_SQL_FILE = "dev_gold.sql"
STD_TRAIN_JSON_FILE = "train.json"
STD_TRAIN_SQL_FILE = "train_gold.sql"
STD_TEST_JSON_FILE = "test.json"
STD_TEST_SQL_FILE = "test_gold.sql"

SPLIT_FILES = {
    "dev":   (STD_DEV_JSON_FILE,   STD_DEV_SQL_FILE),
    "dev_zh": ("dev_zh.json", "dev_zh_gold.sql"),
    "train": (STD_TRAIN_JSON_FILE, STD_TRAIN_SQL_FILE),
    "test":  (STD_TEST_JSON_FILE,  STD_TEST_SQL_FILE),
}


def get_split_files(split: str):
    """Return ``(json_file, gold_sql_file)`` for a given split name."""
    if split not in SPLIT_FILES:
        raise ValueError(
            f"Unknown split '{split}'. Available: {', '.join(sorted(SPLIT_FILES))}"
        )
    return SPLIT_FILES[split]


@dataclass
class DatasetConfig:
    # --- database encoding ---
    db_encoding: str = "utf-8"

    # --- JSON field names ---
    sql_field: str = "query"
    db_id_field: str = "db_id"

    # --- feature flags ---
    has_evidence: bool = False
    supports_chinese_prompt: bool = False
    has_gold: bool = True

    # When the DB directory lives under a *different* dataset root
    # (e.g. endb-cnqt-bird uses bird's database/).
    db_base_dataset: Optional[str] = None

    # Few-shot example SQL field names to try (in order).
    sql_field_candidates: tuple = ("query", "SQL", "sql_query", "sql")

    # --- translation direction ---
    translate_direction: str = "en2cn"  # or "cn2en"
    question_tokenizer: str = "char"    # "char" for Chinese, "word" for English


DATASET_REGISTRY = {
    # ---- Spider family ----
    "spider": DatasetConfig(),
    "cspider": DatasetConfig(
        supports_chinese_prompt=True,
    ),
    "multispider": DatasetConfig(
        supports_chinese_prompt=True,
    ),
    "cndb-spider": DatasetConfig(),
    "cndb-cnqt-spider": DatasetConfig(
        db_base_dataset="cndb-spider",
    ),
    "endb-cnqt-spider": DatasetConfig(
        db_base_dataset="spider",
    ),

    # ---- Spider2-lite family (local SQLite subset only) ----
    # The preprocessor rewrites Spider2's ``db`` field → ``db_id`` and
    # attaches gold SQL under ``query`` (per-instance .sql files), so the
    # default Spider config applies as-is.
    "spider2": DatasetConfig(),
    "cndb-spider2": DatasetConfig(),
    "cndb-cnqt-spider2": DatasetConfig(
        db_base_dataset="cndb-spider2",
    ),
    "endb-cnqt-spider2": DatasetConfig(
        db_base_dataset="spider2",
    ),

    # ---- BIRD family ----
    "bird": DatasetConfig(
        db_encoding="latin-1",
        sql_field="SQL",
        has_evidence=True,
        supports_chinese_prompt=True,
    ),
    "cndb-bird": DatasetConfig(
        sql_field="SQL",
        has_evidence=True,
        supports_chinese_prompt=True,
    ),
    "cndb-cnqt-bird": DatasetConfig(
        sql_field="SQL",
        has_evidence=True,
        supports_chinese_prompt=True,
        db_base_dataset="cndb-bird",
    ),
    "endb-cnqt-bird": DatasetConfig(
        db_encoding="latin-1",
        sql_field="SQL",
        has_evidence=True,
        supports_chinese_prompt=True,
        db_base_dataset="bird",
    ),

    # ---- FinSQL BULL family ----
    # Note: BULL's raw source does not ship a separate ``dev_gold.sql``, but
    # the SQL lives inside ``dev.json`` under the ``sql_query`` field. The
    # preprocessor synthesizes ``dev_gold.sql`` from there, so all BULL
    # variants have a gold file from Part 0 onward.
    "BULL-en": DatasetConfig(
        sql_field="sql_query",
        db_id_field="db_name",
    ),
    "BULL-cn": DatasetConfig(
        sql_field="sql_query",
        db_id_field="db_name",
        translate_direction="cn2en",
        question_tokenizer="word",
    ),
    "cnqt-BULL-en": DatasetConfig(
        sql_field="sql_query",
        db_id_field="db_name",
    ),
    "enqt-BULL-cn": DatasetConfig(
        sql_field="sql_query",
        db_id_field="db_name",
        translate_direction="cn2en",
        question_tokenizer="word",
    ),

    # ---- EHRSQL family ----
    # EHRSQL ships per-DB train/valid/test under EHRSQL-origin/<db>/<split>.json
    # with the canonical Spider-style ``query`` + ``db_id`` fields, and a
    # combined ``tables.json`` at the dataset root. The preprocessor merges
    # eicu + mimic_iii into a single ``dev.json`` and splits off the
    # ``is_impossible`` (null-SQL) items into ``dev_unanswerable.json``.
    "ehrsql": DatasetConfig(),
    "cndb-ehrsql": DatasetConfig(),
    "cndb-cnqt-ehrsql": DatasetConfig(
        db_base_dataset="cndb-ehrsql",
    ),
    "endb-cnqt-ehrsql": DatasetConfig(
        db_base_dataset="ehrsql",
    ),

    # ---- LogicCat family ----
    # LogicCat uses Spider-style ``query`` + ``db_id`` fields in JSON.
    "logiccat": DatasetConfig(),

    # ---- KaggleDBQA family ----
    # KaggleDBQA test samples use Spider-style ``query`` + ``db_id`` fields.
    "kaggledbqa": DatasetConfig(),

    # ---- SynSQL family ----
    # SynSQL uses Spider-style ``tables.json`` and ``query`` + ``db_id`` fields.
    "synsql": DatasetConfig(),

    # ---- TACO-Beijing family ----
    # TACO ships Chinese NL + Chinese DB names and uses ``sql`` in raw files.
    # After preprocessing we standardize SQL to ``SQL`` (BIRD style).
    "taco": DatasetConfig(
        sql_field="SQL",
        has_evidence=True,
        supports_chinese_prompt=True,
        translate_direction="cn2en",
        question_tokenizer="word",
    ),
}


def get_config(dataset: str) -> DatasetConfig:
    """Look up a dataset config by name; raise ValueError if unknown."""
    if dataset not in DATASET_REGISTRY:
        raise ValueError(
            f"Unknown dataset '{dataset}'. "
            f"Available: {', '.join(sorted(DATASET_REGISTRY))}"
        )
    return DATASET_REGISTRY[dataset]
