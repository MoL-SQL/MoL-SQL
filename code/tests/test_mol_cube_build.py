from __future__ import annotations

import sqlite3
import tempfile
import unittest
from pathlib import Path

import yaml

from mol_sql.contracts.hashing import sha256_file
from mol_sql.contracts.ids import stable_id
from mol_sql.contracts.io import load_json, load_jsonl, write_json, write_jsonl
from mol_sql.contracts.models import LogicalInstance, Realization, ReleaseManifest
from mol_sql.dataset.adapters import execution_sql_for
from mol_sql.dataset.cube import (
    CubeBirdExportOptions,
    CubeBuildOptions,
    CubeRealization,
    build_mol_cube,
    export_bird_cube,
    validate_bird_cube,
)
from mol_sql.dataset.cube.build import _execute
from mol_sql.dataset.statistics import CubeStatisticsOptions, generate_cube_statistics
from mol_sql.dataset.statistics.models import (
    FullLogicalProfile,
    FullStatisticsManifest,
)


def _database(path: Path, *, chinese: bool) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    table = "表" if chinese else "t"
    column = "名称" if chinese else "name"
    values = ("甲", "乙") if chinese else ("a", "b")
    with sqlite3.connect(path) as connection:
        connection.execute(
            f'CREATE TABLE "{table}" (id INTEGER, "{column}" TEXT)'
        )
        connection.executemany(
            f'INSERT INTO "{table}" VALUES (?, ?)',
            [(1, values[0]), (2, values[1])],
        )


def _fixture(repo: Path) -> tuple[Path, Path, Path]:
    (repo / "code").mkdir(exist_ok=True)
    (repo / "code" / "pyproject.toml").write_text(
        "[project]\nname = 'mol-sql'\n", encoding="utf-8"
    )
    release_dir = repo / "full"
    statistics_dir = repo / "stats"
    release_dir.mkdir()
    statistics_dir.mkdir()
    _database(repo / "db/en/db.sqlite", chinese=False)
    _database(repo / "db/zh/db.sqlite", chinese=True)
    replacement_path = repo / "replacement.json"
    write_json(
        replacement_path,
        {
            "db": {
                "tables": [["t", "表"]],
                "columns": [["t", "name", "名称"]],
                "values": [["t", "name", "a", "甲"], ["t", "name", "b", "乙"]],
            }
        },
    )
    for language in ("en", "zh"):
        write_json(
            repo / f"tables_{language}.json",
            [
                {
                    "db_id": "db",
                    "table_names": ["t" if language == "en" else "表"],
                    "table_names_original": ["t" if language == "en" else "表"],
                    "column_names": [
                        [-1, "*"],
                        [0, "id"],
                        [0, "name" if language == "en" else "名称"],
                    ],
                    "column_names_original": [
                        [-1, "*"],
                        [0, "id"],
                        [0, "name" if language == "en" else "名称"],
                    ],
                    "column_types": ["text", "number", "text"],
                    "primary_keys": [1],
                    "foreign_keys": [],
                }
            ],
        )

    logical_id = stable_id("logical", "fixture")
    logical = LogicalInstance(
        logical_id=logical_id,
        source_family="fixture",
        source_sample_key="index:0",
        legacy_index=0,
        database_id="db",
        split="dev",
        canonical_question="Find a",
        canonical_sql="SELECT name FROM t WHERE name = 'a'",
        answer_semantics="multiset",
        provenance_refs=["fixture"],
        input_hashes={},
    )
    write_jsonl(release_dir / "logical_instances.jsonl", [logical])

    configurations = (
        ("Q_en--S_en--V_en", "en", "en", "Find a"),
        ("Q_zh--S_en--V_en", "zh", "en", "查找 a"),
        ("Q_en--S_zh--V_zh", "en", "zh", "Find 甲"),
        ("Q_zh--S_zh--V_zh", "zh", "zh", "查找甲"),
    )
    realizations = []
    for configuration, q_language, database_language, question in configurations:
        sql = (
            "SELECT name FROM t WHERE name = 'a'"
            if database_language == "en"
            else 'SELECT "名称" FROM "表" WHERE "名称" = \'甲\''
        )
        realizations.append(
            Realization(
                realization_id=stable_id("realization", logical_id, configuration),
                logical_id=logical_id,
                source_family="fixture",
                source_sample_key="index:0",
                configuration=configuration,
                question_language=q_language,
                schema_language=database_language,
                value_language=database_language,
                database_id="db",
                split="dev",
                question=question,
                gold_sql=sql,
                dataset_path="fixture.json",
                tables_path=f"tables_{database_language}.json",
                database_path=f"db/{database_language}/db.sqlite",
                replacement_map="replacement.json",
                input_hashes={},
            )
        )
    write_jsonl(release_dir / "realizations.jsonl", realizations)
    full_manifest = ReleaseManifest(
        release_id="full-fixture-draft",
        release_kind="mol-full",
        status="draft",
        source_families=["fixture"],
        logical_instances=1,
        realizations=4,
        configurations=[row[0] for row in configurations],
        source_counts={"fixture": 1},
        file_hashes={},
        audit_summary={},
        blockers=["human_audit:incomplete"],
        build_config_hash="fixture",
    )
    write_json(release_dir / "release_manifest.json", full_manifest.model_dump(mode="json"))

    profile = FullLogicalProfile(
        logical_id=logical_id,
        source_family="fixture",
        database_id="db",
        split="dev",
        source_sample_key="index:0",
        legacy_index=0,
        source_difficulty=None,
        answer_semantics="multiset",
        phenomena=["selection"],
        sql_features={"condition_count": 1, "join_count": 0},
        schema_features={
            "distractor_table_count": 0,
            "distractor_column_count": 1,
            "requires_join": False,
        },
        value_features={"recurring_entity_count": 0},
        treatment_support={
            "q_treatment_present": True,
            "s_treatment_present": True,
            "s_mapped_reference_count": 2,
            "s_treatment_intensity": 1.0,
            "v_treatment_present": True,
            "v_mapped_literal_count": 1,
            "v_treatment_intensity": 1.0,
        },
        controls={
            "literal_free": False,
            "recurring_entity": False,
            "value_bearing": True,
        },
        difficulty={"composite_tier": "hard", "composite_score": 1.0},
    )
    write_jsonl(statistics_dir / "logical_profiles.jsonl", [profile])
    statistics_manifest = FullStatisticsManifest(
        release_id=full_manifest.release_id,
        release_status="draft",
        release_manifest_hash=sha256_file(release_dir / "release_manifest.json"),
        canonical_artifact_hashes={},
        provisional=True,
        blockers=full_manifest.blockers,
        generated_at_utc="2026-07-29T00:00:00+00:00",
        code_commit=None,
        code_dirty=None,
        config_hash="fixture",
        logical_instances=1,
        files={"logical_profiles.jsonl": sha256_file(statistics_dir / "logical_profiles.jsonl")},
    )
    write_json(
        statistics_dir / "report_manifest.json",
        statistics_manifest.model_dump(mode="json"),
    )

    sampler = repo / "sampler.yaml"
    sampler.write_text(
        yaml.safe_dump(
            {
                "schema_version": "mol-cube-sampler-v0.1",
                "release_id": "cube-fixture-engineering",
                "seed": 7,
                "target_per_source": 1,
                "difficulty_proportions": {"hard": 1.0},
                "minimums_per_source": {"v_support": 1},
                "database_max_fraction": 1.0,
            }
        ),
        encoding="utf-8",
    )
    return release_dir, statistics_dir, sampler


class MoLCubeBuildTests(unittest.TestCase):
    def test_cube_execution_uses_source_preprocessing_and_bad_text_fallback(self) -> None:
        processed = execution_sql_for(
            "ehrsql",
            "SELECT 1 WHERE x BETWEEN systolic_bp_lower AND systolic_bp_upper",
        )
        self.assertIn("between 90.0 and 120.0", processed.lower())
        with tempfile.TemporaryDirectory() as temporary:
            database = Path(temporary) / "bad.sqlite"
            with sqlite3.connect(database) as connection:
                connection.execute("CREATE TABLE t (value TEXT)")
                connection.execute("INSERT INTO t VALUES (CAST(X'E38D4E' AS TEXT))")
            rows = _execute(database, "SELECT value FROM t", False, {}, 1.0)
            self.assertEqual(rows, [(repr("ãN"),)])

    def test_builds_and_executes_complete_eight_cell_cube(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repo = Path(temporary)
            release_dir, statistics_dir, sampler = _fixture(repo)
            output_dir = repo / "cube"
            manifest = build_mol_cube(
                CubeBuildOptions(
                    repo_root=repo,
                    full_release_dir=release_dir,
                    full_statistics_dir=statistics_dir,
                    sampler_config=sampler,
                    output_dir=output_dir,
                    allow_draft=True,
                )
            )
            self.assertEqual(manifest.logical_instances, 1)
            self.assertEqual(manifest.realizations, 8)
            self.assertTrue(manifest.non_claim_bearing)
            self.assertEqual(
                manifest.audit_summary["eight_cell_execution_equivalence"],
                {"pass": 1},
            )
            rows = load_jsonl(output_dir / "realizations.jsonl", CubeRealization)
            mixed = {row.configuration: row for row in rows if row.schema_language != row.value_language}
            self.assertIn("'甲'", mixed["Q_en--S_en--V_zh"].gold_sql)
            self.assertIn('"表"', mixed["Q_en--S_zh--V_en"].gold_sql)
            self.assertIn("'a'", mixed["Q_en--S_zh--V_en"].gold_sql)

    def test_derives_missing_schema_replacements_from_paired_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repo = Path(temporary)
            release_dir, statistics_dir, sampler = _fixture(repo)
            write_json(
                repo / "replacement.json",
                {
                    "db": {
                        "tables": [],
                        "columns": [],
                        "values": [
                            ["t", "name", "a", "甲"],
                            ["t", "name", "b", "乙"],
                        ],
                    }
                },
            )
            output_dir = repo / "cube"
            build_mol_cube(
                CubeBuildOptions(
                    repo_root=repo,
                    full_release_dir=release_dir,
                    full_statistics_dir=statistics_dir,
                    sampler_config=sampler,
                    output_dir=output_dir,
                    allow_draft=True,
                )
            )
            rows = load_jsonl(output_dir / "realizations.jsonl", CubeRealization)
            mixed = next(
                row
                for row in rows
                if row.configuration == "Q_en--S_zh--V_en"
            )
            with sqlite3.connect(repo / mixed.database_path) as connection:
                table = connection.execute(
                    "SELECT name FROM sqlite_master WHERE type='table'"
                ).fetchone()[0]
                columns = [
                    row[1]
                    for row in connection.execute('PRAGMA table_info("表")').fetchall()
                ]
            self.assertEqual(table, "表")
            self.assertEqual(columns, ["id", "名称"])
            self.assertIn('"表"', mixed.gold_sql)
            self.assertIn('"名称"', mixed.gold_sql)

    def test_cube_statistics_and_bird_export_round_trip(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repo = Path(temporary)
            release_dir, statistics_dir, sampler = _fixture(repo)
            cube_dir = repo / "cube"
            build_mol_cube(
                CubeBuildOptions(
                    repo_root=repo,
                    full_release_dir=release_dir,
                    full_statistics_dir=statistics_dir,
                    sampler_config=sampler,
                    output_dir=cube_dir,
                    allow_draft=True,
                )
            )
            exported = export_bird_cube(
                CubeBirdExportOptions(
                    repo_root=repo,
                    release_dir=cube_dir,
                    database_mode="hardlink",
                )
            )
            self.assertTrue(exported["valid"])
            self.assertEqual(exported["packages"], 8)
            self.assertEqual(exported["samples"], 8)
            self.assertTrue(validate_bird_cube(repo, cube_dir)["valid"])

            report_dir = repo / "cube-stats"
            report = generate_cube_statistics(
                CubeStatisticsOptions(
                    repo_root=repo,
                    cube_release_dir=cube_dir,
                    full_statistics_dir=statistics_dir,
                    output_dir=report_dir,
                    allow_engineering=True,
                )
            )
            self.assertEqual(report.logical_instances, 1)
            self.assertEqual(report.realizations, 8)
            self.assertTrue(load_json(report_dir / "cube_completeness.json")["contract_satisfied"])


if __name__ == "__main__":
    unittest.main()
