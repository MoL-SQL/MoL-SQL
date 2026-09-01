from __future__ import annotations

import json
import sqlite3
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

import yaml

from mol_sql.contracts.io import load_jsonl, write_jsonl
from mol_sql.contracts.models import HumanAuditItem
from mol_sql.dataset.full import (
    BirdExportOptions,
    BuildOptions,
    audit_mol_full,
    build_mol_full,
    export_bird_full,
    freeze_mol_full,
    validate_bird_full,
)
from mol_sql.dataset.full.execution_repair import apply_execution_repairs
from mol_sql.dataset.full.repair import (
    restore_ehrsql_eicu_icd9code,
    restore_mapped_column_by_key,
)
from mol_sql.dataset.adapters.ehrsql import EHRSQLAdapter
from mol_sql.dataset.statistics import (
    FullLogicalProfile,
    FullStatisticsOptions,
    generate_full_statistics,
)
from mol_sql.dataset.statistics.full import _sql_features, _treatment_features


CONFIGURATIONS = {
    "Q_en--S_en--V_en": ("en_en", "en", "en", "en"),
    "Q_zh--S_en--V_en": ("zh_en", "zh", "en", "en"),
    "Q_en--S_zh--V_zh": ("en_zh", "en", "zh", "zh"),
    "Q_zh--S_zh--V_zh": ("zh_zh", "zh", "zh", "zh"),
}


def _write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False), encoding="utf-8")


def _database(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(path) as connection:
        connection.execute("CREATE TABLE t (id INTEGER, name TEXT)")
        connection.executemany("INSERT INTO t VALUES (?, ?)", [(1, "a"), (2, "b")])


def _fixture(repo: Path) -> Path:
    root = repo / "seed"
    for _, (directory, q_language, _, _) in CONFIGURATIONS.items():
        question = "名称是什么？" if q_language == "zh" else "What are the names?"
        _write_json(
            root / directory / "dev.json",
            [
                {
                    "db_id": "db",
                    "question": question,
                    "query": "SELECT name FROM t ORDER BY id",
                }
            ],
        )
        _write_json(
            root / directory / "tables.json",
            [
                {
                    "db_id": "db",
                    "table_names": ["t"],
                    "table_names_original": ["t"],
                    "column_names": [[-1, "*"], [0, "id"], [0, "name"]],
                    "column_names_original": [
                        [-1, "*"],
                        [0, "id"],
                        [0, "name"],
                    ],
                    "column_types": ["text", "number", "text"],
                    "primary_keys": [],
                    "foreign_keys": [],
                }
            ],
        )
    _database(root / "db_en" / "db" / "db.sqlite")
    _database(root / "db_zh" / "db" / "db.sqlite")
    _write_json(
        repo / "replacement.json",
        {
            "db": {"tables": [], "columns": [], "values": []},
            "outside_release": {
                "tables": [],
                "columns": [["t", "left", "same"], ["t", "right", "same"]],
                "values": [],
            },
        },
    )

    source = {
        "schema_version": "mol-full-sources-v0.1",
        "sources": [
            {
                "source_family": "spider",
                "release_role": "core",
                "root": "seed",
                "native_language": "en",
                "split": "dev",
                "id_field": None,
                "sql_fields": ["query"],
                "difficulty_field": None,
                "upstream_version": "fixture-v1",
                "source_url": "https://example.invalid/source",
                "snapshot_date": "2026-07-28",
                "license_spdx": "CC0-1.0",
                "license_evidence_url": "https://example.invalid/license",
                "redistribution_policy": "redistributable_with_attribution",
                "license_notes": "fixture",
                "replacement_map": "replacement.json",
                "database_roots": {"en": "seed/db_en", "zh": "seed/db_zh"},
                "variants": {
                    configuration: {
                        "directory": directory,
                        "question_language": q_language,
                        "schema_language": s_language,
                        "value_language": v_language,
                    }
                    for configuration, (
                        directory,
                        q_language,
                        s_language,
                        v_language,
                    ) in CONFIGURATIONS.items()
                },
            }
        ],
    }
    config = repo / "sources.yaml"
    config.write_text(yaml.safe_dump(source, allow_unicode=True), encoding="utf-8")
    return config


class MoLFullBuildTests(unittest.TestCase):
    def test_statistics_treats_unknown_double_quoted_columns_as_values(self) -> None:
        known_columns = {"Country", "Status"}
        sql_en = (
            'SELECT "Status" FROM nuclear_power_plants '
            'WHERE Country = "Japan" AND Status = "Under Construction"'
        )
        sql_zh = (
            'SELECT "Status" FROM nuclear_power_plants '
            'WHERE Country = "Japan" AND Status = "建设中"'
        )
        features, _ = _sql_features(sql_en, known_columns)
        self.assertEqual(features["referenced_columns"], ["Country", "Status"])
        self.assertEqual(
            features["string_literals"],
            ["Japan", "Under Construction"],
        )

        realizations = {
            "Q_en--S_en--V_en": SimpleNamespace(
                question="Which plants are under construction?",
                gold_sql=sql_en,
            ),
            "Q_zh--S_en--V_en": SimpleNamespace(
                question="哪些核电站正在建设中？",
                gold_sql=sql_en,
            ),
            "Q_en--S_zh--V_zh": SimpleNamespace(
                question="Which plants are under construction?",
                gold_sql=sql_zh,
            ),
            "Q_zh--S_zh--V_zh": SimpleNamespace(
                question="哪些核电站正在建设中？",
                gold_sql=sql_zh,
            ),
        }
        support, value_features, controls = _treatment_features(
            realizations,
            features,
            {
                "tables": [],
                "columns": [],
                "values": [
                    [
                        "nuclear_power_plants",
                        "Status",
                        "Under Construction",
                        "建设中",
                    ]
                ],
            },
            [],
            [],
            known_columns,
        )
        self.assertTrue(support["v_treatment_present"])
        self.assertEqual(support["v_actual_literal_change_count"], 1)
        self.assertEqual(value_features["mapped_literal_count"], 1)
        self.assertTrue(controls["value_bearing"])
        self.assertTrue(controls["mapped_value_bearing"])

    def test_ehrsql_execution_sql_uses_official_constants(self) -> None:
        adapter = object.__new__(EHRSQLAdapter)
        processed = adapter.execution_sql(
            "SELECT strftime('%y', current_time) "
            "WHERE label = '平均红细胞血红蛋白浓度（MCHC）' "
            "AND x BETWEEN heart_rate_lower AND heart_rate_upper"
        )
        self.assertIn("strftime('%Y', '2105-12-31 23:59:00')", processed)
        self.assertIn("between 60.0 and 100.0", processed.lower())
        self.assertIn("（MCHC）", processed)

    def test_build_audit_review_and_freeze(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            tmp_path = Path(temporary)
            (tmp_path / "code").mkdir(exist_ok=True)
            (tmp_path / "code" / "pyproject.toml").write_text(
                "[project]\nname = 'mol-sql'\n", encoding="utf-8"
            )
            config = _fixture(tmp_path)
            release_dir = tmp_path / "release"
            manifest = build_mol_full(
                BuildOptions(
                    repo_root=tmp_path,
                    source_config=config,
                    output_dir=release_dir,
                    release_id="fixture-full-v1",
                    execute_equivalence=True,
                    human_audit_per_source=1,
                )
            )
            self.assertEqual(manifest.status, "draft")
            self.assertEqual(manifest.logical_instances, 1)
            self.assertEqual(manifest.realizations, 4)
            self.assertEqual(manifest.source_counts, {"spider": 1})
            self.assertEqual(
                manifest.audit_summary["execution_equivalence"], {"pass": 1}
            )
            replacement_audit = next(
                json.loads(line)
                for line in (
                    release_dir / "audit_records.jsonl"
                ).read_text(encoding="utf-8").splitlines()
                if json.loads(line)["gate"] == "replacement_map_consistency"
            )
            self.assertEqual(replacement_audit["status"], "pass")
            self.assertEqual(
                replacement_audit["details"]["out_of_scope_databases"],
                ["outside_release"],
            )
            self.assertEqual(
                manifest.blockers,
                ["bird_format:missing", "human_audit:incomplete"],
            )
            audited = audit_mol_full(
                repo_root=tmp_path,
                source_config=config,
                release_dir=release_dir,
                check_database_integrity=True,
                execute_equivalence=True,
                execution_timeout_seconds=5,
            )
            self.assertEqual(
                audited.audit_summary["execution_equivalence"], {"pass": 1}
            )
            self.assertEqual(
                audited.blockers,
                ["bird_format:missing", "human_audit:incomplete"],
            )
            second_release = tmp_path / "release-second"
            repeated = build_mol_full(
                BuildOptions(
                    repo_root=tmp_path,
                    source_config=config,
                    output_dir=second_release,
                    release_id="fixture-full-v1",
                    execute_equivalence=True,
                    human_audit_per_source=1,
                )
            )
            self.assertEqual(manifest.file_hashes, repeated.file_hashes)
            self.assertEqual(manifest.build_config_hash, repeated.build_config_hash)

            queue_path = release_dir / "human_audit_queue.jsonl"
            queue = load_jsonl(queue_path, HumanAuditItem)
            reviewed = [
                item.model_copy(
                    update={
                        "reviewer_1": {
                            "question_fidelity": "pass",
                            "naturalness": "pass",
                            "entity_value_grounding": "pass",
                        },
                        "reviewer_2": {
                            "question_fidelity": "pass",
                            "naturalness": "pass",
                            "entity_value_grounding": "pass",
                        },
                        "adjudication": {"status": "pass"},
                    }
                )
                for item in queue
            ]
            write_jsonl(queue_path, reviewed)
            with self.assertRaisesRegex(
                ValueError,
                "public BIRD export requires database mode 'copy'",
            ):
                export_bird_full(
                    BirdExportOptions(
                        repo_root=tmp_path,
                        release_dir=release_dir,
                        output_dir=release_dir / "public-bird-format",
                        database_mode="symlink",
                        distribution="public",
                    )
                )
            exported = export_bird_full(
                BirdExportOptions(
                    repo_root=tmp_path,
                    release_dir=release_dir,
                    database_mode="hardlink",
                )
            )
            self.assertTrue(exported["valid"])
            self.assertEqual(exported["packages"], 4)
            self.assertEqual(exported["samples"], 4)
            validated = validate_bird_full(tmp_path, release_dir)
            self.assertEqual(validated["source_sample_counts"], {"spider": 4})
            package = (
                release_dir
                / "bird_format"
                / "spider"
                / "Q_en--S_en--V_en"
            )
            self.assertTrue((package / "database/db/db.sqlite").is_file())
            self.assertEqual(
                (package / "dev_gold.sql").read_text(encoding="utf-8"),
                "SELECT name FROM t ORDER BY id\tdb\n",
            )
            with self.assertRaisesRegex(
                ValueError,
                "draft Full statistics require allow_draft=True",
            ):
                generate_full_statistics(
                    FullStatisticsOptions(
                        repo_root=tmp_path,
                        release_dir=release_dir,
                        output_dir=tmp_path / "draft-stats-refused",
                    )
                )
            provisional = generate_full_statistics(
                FullStatisticsOptions(
                    repo_root=tmp_path,
                    release_dir=release_dir,
                    output_dir=tmp_path / "draft-stats",
                    allow_draft=True,
                )
            )
            self.assertTrue(provisional.provisional)
            self.assertEqual(provisional.logical_instances, 1)
            profiles = load_jsonl(
                tmp_path / "draft-stats/logical_profiles.jsonl",
                FullLogicalProfile,
            )
            self.assertEqual(len(profiles), 1)
            self.assertEqual(profiles[0].difficulty["composite_tier"], "easy")
            frozen = freeze_mol_full(release_dir)
            self.assertEqual(frozen.status, "frozen")
            self.assertEqual(frozen.blockers, [])
            final_statistics = generate_full_statistics(
                FullStatisticsOptions(
                    repo_root=tmp_path,
                    release_dir=release_dir,
                    output_dir=tmp_path / "frozen-stats",
                )
            )
            self.assertFalse(final_statistics.provisional)

    def test_execution_adjudication_drops_aligned_logical_sample(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            tmp_path = Path(temporary)
            (tmp_path / "code").mkdir(exist_ok=True)
            (tmp_path / "code" / "pyproject.toml").write_text(
                "[project]\nname = 'mol-sql'\n", encoding="utf-8"
            )
            config = _fixture(tmp_path)
            _write_json(
                tmp_path / "execution_adjudications.json",
                {
                    "schema_version": "mol-execution-adjudications-v0.1",
                    "decisions": [
                        {
                            "source_family": "spider",
                            "legacy_index": 0,
                            "source_sample_key": "index:0",
                            "database_id": "db",
                            "decision": "drop",
                            "reason_code": "language_dependent_text_order",
                            "rationale": "fixture",
                        }
                    ],
                },
            )
            raw_config = yaml.safe_load(config.read_text(encoding="utf-8"))
            raw_config["sources"][0]["execution_adjudications"] = (
                "execution_adjudications.json"
            )
            config.write_text(
                yaml.safe_dump(raw_config, allow_unicode=True),
                encoding="utf-8",
            )
            release_dir = tmp_path / "release"
            manifest = build_mol_full(
                BuildOptions(
                    repo_root=tmp_path,
                    source_config=config,
                    output_dir=release_dir,
                    release_id="fixture-with-drop",
                    human_audit_per_source=0,
                )
            )
            self.assertEqual(manifest.logical_instances, 0)
            self.assertEqual(manifest.realizations, 0)
            self.assertEqual(
                len(
                    (
                        release_dir / "execution_adjudications.jsonl"
                    ).read_text(encoding="utf-8").splitlines()
                ),
                1,
            )

    def test_execution_sql_repairs_are_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            tmp_path = Path(temporary)
            config = _fixture(tmp_path)
            _write_json(
                tmp_path / "execution_repairs.json",
                {
                    "schema_version": "mol-execution-repairs-v0.1",
                    "sql_repairs": [
                        {
                            "source_family": "spider",
                            "legacy_indices": [0],
                            "database_id": "db",
                            "schema_language": "en",
                            "old_fragment": "ORDER BY id",
                            "new_fragment": "ORDER BY id ASC",
                            "reason": "fixture",
                        }
                    ],
                },
            )
            first = apply_execution_repairs(
                repo_root=tmp_path,
                source_config=config,
                repairs_path=tmp_path / "execution_repairs.json",
            )
            second = apply_execution_repairs(
                repo_root=tmp_path,
                source_config=config,
                repairs_path=tmp_path / "execution_repairs.json",
            )
            self.assertEqual(first["changed_rows"], 2)
            self.assertEqual(second["changed_rows"], 0)
            self.assertEqual(second["already_applied"], 2)

    def test_fixed_point_overlap_fails_replacement_gate(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            tmp_path = Path(temporary)
            (tmp_path / "code").mkdir(exist_ok=True)
            (tmp_path / "code" / "pyproject.toml").write_text(
                "[project]\nname = 'mol-sql'\n", encoding="utf-8"
            )
            config = _fixture(tmp_path)
            _write_json(
                tmp_path / "replacement.json",
                {
                    "db": {
                        "tables": [],
                        "columns": [["t", "id", "编号"]],
                        "values": [],
                    }
                },
            )
            _write_json(
                tmp_path / "fixed_points.json",
                {
                    "schema_version": "mol-fixed-points-v0.1",
                    "source_family": "spider",
                    "columns": [
                        {
                            "database_id": "db",
                            "table": "t",
                            "column": "id",
                            "reason": "test",
                        }
                    ],
                    "value_columns": [],
                },
            )
            raw_config = yaml.safe_load(config.read_text(encoding="utf-8"))
            raw_config["sources"][0]["fixed_points"] = "fixed_points.json"
            config.write_text(
                yaml.safe_dump(raw_config, allow_unicode=True),
                encoding="utf-8",
            )
            release_dir = tmp_path / "release"
            manifest = build_mol_full(
                BuildOptions(
                    repo_root=tmp_path,
                    source_config=config,
                    output_dir=release_dir,
                    release_id="fixture-full-v1",
                    human_audit_per_source=0,
                )
            )
            self.assertIn(
                "spider:automatic_gate_failed:replacement_map_consistency",
                manifest.blockers,
            )

    def test_restore_ehrsql_code_fixed_points(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            tmp_path = Path(temporary)
            source = tmp_path / "source.sqlite"
            target = tmp_path / "target.sqlite"
            backup = tmp_path / "target.before.sqlite"
            with sqlite3.connect(source) as connection:
                connection.execute(
                    "CREATE TABLE diagnosis "
                    "(diagnosisid INTEGER PRIMARY KEY, icd9code TEXT)"
                )
                connection.executemany(
                    "INSERT INTO diagnosis VALUES (?, ?)",
                    [(1, "518.81"), (2, "572.2"), (3, None)],
                )
            with sqlite3.connect(target) as connection:
                connection.execute(
                    'CREATE TABLE "诊断" '
                    '("诊断编号" INTEGER PRIMARY KEY, "ICD-9编码" TEXT)'
                )
                connection.executemany(
                    'INSERT INTO "诊断" VALUES (?, ?)',
                    [(1, "急性肺损伤"), (2, "门静脉高压"), (3, None)],
                )
            dry_run = restore_ehrsql_eicu_icd9code(
                source_database=source,
                target_database=target,
                apply=False,
            )
            self.assertEqual(dry_run.mismatches_before, 2)
            repaired = restore_ehrsql_eicu_icd9code(
                source_database=source,
                target_database=target,
                apply=True,
                backup_path=backup,
            )
            self.assertEqual(repaired.mismatches_before, 2)
            self.assertEqual(repaired.mismatches_after, 0)
            self.assertTrue(backup.is_file())
            with sqlite3.connect(target) as connection:
                values = connection.execute(
                    'SELECT "ICD-9编码" FROM "诊断" ORDER BY "诊断编号"'
                ).fetchall()
            self.assertEqual(values, [("518.81",), ("572.2",), (None,)])

    def test_restore_mapped_column_by_key(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            tmp_path = Path(temporary)
            source = tmp_path / "source.sqlite"
            target = tmp_path / "target.sqlite"
            replacement_map = tmp_path / "replacement.json"
            with sqlite3.connect(source) as connection:
                connection.execute("CREATE TABLE awards (id INTEGER PRIMARY KEY, name TEXT)")
                connection.executemany(
                    "INSERT INTO awards VALUES (?, ?)",
                    [(1, "Gold"), (2, "Silver"), (3, None)],
                )
            with sqlite3.connect(target) as connection:
                connection.execute(
                    'CREATE TABLE "奖项" ("编号" INTEGER PRIMARY KEY, "名称" TEXT)'
                )
                connection.executemany(
                    'INSERT INTO "奖项" VALUES (?, ?)',
                    [(1, "金"), (2, "错误"), (3, None)],
                )
            _write_json(
                replacement_map,
                {
                    "db": {
                        "tables": [],
                        "columns": [],
                        "values": [
                            ["awards", "name", "Gold", "金"],
                            ["awards", "name", "Silver", "银"],
                        ],
                    }
                },
            )
            repaired = restore_mapped_column_by_key(
                source_database=source,
                target_database=target,
                replacement_map=replacement_map,
                database_id="db",
                source_table="awards",
                source_key="id",
                source_column="name",
                target_table="奖项",
                target_key="编号",
                target_column="名称",
                apply=True,
            )
            self.assertEqual(repaired.mismatches_before, 1)
            self.assertEqual(repaired.mismatches_after, 0)

    def test_fixed_value_column_checks_database_rows(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            tmp_path = Path(temporary)
            (tmp_path / "code").mkdir(exist_ok=True)
            (tmp_path / "code" / "pyproject.toml").write_text(
                "[project]\nname = 'mol-sql'\n", encoding="utf-8"
            )
            config = _fixture(tmp_path)
            _write_json(
                tmp_path / "fixed_points.json",
                {
                    "schema_version": "mol-fixed-points-v0.1",
                    "source_family": "spider",
                    "columns": [],
                    "value_columns": [
                        {
                            "database_id": "db",
                            "table": "t",
                            "column": "name",
                            "key_column": "id",
                            "reason": "test",
                        }
                    ],
                },
            )
            raw_config = yaml.safe_load(config.read_text(encoding="utf-8"))
            raw_config["sources"][0]["fixed_points"] = "fixed_points.json"
            config.write_text(
                yaml.safe_dump(raw_config, allow_unicode=True),
                encoding="utf-8",
            )
            passing = build_mol_full(
                BuildOptions(
                    repo_root=tmp_path,
                    source_config=config,
                    output_dir=tmp_path / "passing",
                    release_id="passing",
                    human_audit_per_source=0,
                )
            )
            self.assertEqual(
                passing.audit_summary["fixed_point_data_consistency"],
                {"pass": 1},
            )
            with sqlite3.connect(root := tmp_path / "seed/db_zh/db/db.sqlite") as connection:
                connection.execute("UPDATE t SET name = '翻译值' WHERE id = 1")
            self.assertTrue(root.is_file())
            failing = build_mol_full(
                BuildOptions(
                    repo_root=tmp_path,
                    source_config=config,
                    output_dir=tmp_path / "failing",
                    release_id="failing",
                    human_audit_per_source=0,
                )
            )
            self.assertEqual(
                failing.audit_summary["fixed_point_data_consistency"],
                {"fail": 1},
            )


if __name__ == "__main__":
    unittest.main()
