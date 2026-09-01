from __future__ import annotations

import json
import sqlite3
import tempfile
import unittest
import unittest.mock
from contextlib import closing
from pathlib import Path

from mol_sql.experiments.methods.direct_zs import build_prompt, extract_sql
from mol_sql.experiments.runner.direct_zs import DirectZSOptions, run_direct_zs


class DirectZSTest(unittest.TestCase):
    def _database(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with closing(sqlite3.connect(path)) as connection:
            connection.executescript(
                """
                CREATE TABLE `歌手` (`编号` INTEGER PRIMARY KEY, `姓名` TEXT, `国籍` TEXT);
                INSERT INTO `歌手` VALUES (1, 'Alice', 'France');
                INSERT INTO `歌手` VALUES (2, 'Bob', 'China');
                INSERT INTO `歌手` VALUES (3, 'Carol', 'France');
                INSERT INTO `歌手` VALUES (4, 'Dave', 'US');
                """
            )

    def test_prompt_freezes_baseline_visibility(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "demo.sqlite"
            self._database(database)
            prompt = build_prompt("Which singers are French?", database, 3)
        self.assertTrue(prompt.startswith("Generate a SQLite SQL query"))
        self.assertIn("CREATE TABLE `歌手`", prompt)
        self.assertIn("Alice | France", prompt)
        self.assertIn("Carol | France", prompt)
        self.assertNotIn("Dave", prompt)
        self.assertIn("## Question\nWhich singers are French?", prompt)
        self.assertNotIn("evidence", prompt.lower())
        self.assertIn("## SQL (single line, no markdown", prompt)

    def test_extract_sql_accepts_format_noise(self) -> None:
        self.assertEqual(extract_sql("SELECT 1"), "SELECT 1")
        self.assertEqual(extract_sql("```sql\nSELECT 1\n```"), "SELECT 1")
        self.assertEqual(extract_sql("Analysis: short\nSQL: SELECT 1"), "SELECT 1")
        self.assertEqual(extract_sql("<cot>x</cot><sql>SELECT 1</sql>"), "SELECT 1")

    def test_prompt_stage_writes_formal_records(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo_root = Path(directory)
            package = (
                repo_root / "cube" / "bird_format" / "demo" / "Q_en--S_en--V_en"
            )
            database = package / "database" / "db" / "db.sqlite"
            self._database(database)
            package.mkdir(parents=True, exist_ok=True)
            (package / "dev.json").write_text(
                json.dumps(
                    [
                        {
                            "question_id": 0,
                            "db_id": "db",
                            "question": "Count singers.",
                            "SQL": "SELECT count(*) FROM `歌手`",
                            "difficulty": "simple",
                            "logical_id": "logical_1",
                            "realization_id": "realization_1",
                        }
                    ]
                ),
                encoding="utf-8",
            )
            manifest = run_direct_zs(
                DirectZSOptions(
                    repo_root=repo_root,
                    cube_root=Path("cube"),
                    output_root=Path("runs"),
                    model="test-model",
                    stages=("prompt",),
                    workers=1,
                )
            )
            prompt_path = (
                repo_root
                / "runs"
                / "test-model"
                / "demo"
                / "Q_en--S_en--V_en"
                / "prompts.jsonl"
            )
            record = json.loads(prompt_path.read_text(encoding="utf-8"))
            progress = json.loads(
                (repo_root / "runs" / "test-model" / "progress.json").read_text(
                    encoding="utf-8"
                )
            )
            progress_log = (
                repo_root / "runs" / "test-model" / "progress.log"
            ).read_text(encoding="utf-8")
        self.assertEqual(manifest.status, "completed")
        self.assertEqual(
            record["prompt_template_version"],
            "direct-zs-sqlite-full-schema-first3-v1",
        )
        self.assertEqual(record["sample_rows_per_table"], 3)
        self.assertEqual(progress["status"], "completed")
        self.assertEqual(progress["stages"]["prompt"]["percentage"], 100.0)
        self.assertIn("percent=100.00%", progress_log)

    def test_prompt_stage_filters_requested_cells(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo_root = Path(directory)
            for cell in ("Q_en--S_en--V_en", "Q_zh--S_zh--V_zh"):
                package = repo_root / "cube" / "bird_format" / "demo" / cell
                database = package / "database" / "db" / "db.sqlite"
                self._database(database)
                package.mkdir(parents=True, exist_ok=True)
                (package / "dev.json").write_text(
                    json.dumps(
                        [
                            {
                                "question_id": 0,
                                "db_id": "db",
                                "question": "Count singers.",
                                "SQL": "SELECT count(*) FROM `歌手`",
                                "difficulty": "simple",
                                "logical_id": "logical_1",
                                "realization_id": f"realization_{cell}",
                            }
                        ]
                    ),
                    encoding="utf-8",
                )
            manifest = run_direct_zs(
                DirectZSOptions(
                    repo_root=repo_root,
                    cube_root=Path("cube"),
                    output_root=Path("runs"),
                    model="test-model",
                    sources=("demo",),
                    cells=("Q_zh--S_zh--V_zh",),
                    stages=("prompt",),
                    workers=1,
                )
            )
            self.assertEqual(manifest.cells, ["Q_zh--S_zh--V_zh"])
            self.assertEqual(manifest.counts["prompts"], 1)
            self.assertFalse(
                (
                    repo_root
                    / "runs"
                    / "test-model"
                    / "demo"
                    / "Q_en--S_en--V_en"
                ).exists()
            )

    def test_eval_stage_resumes_correct_and_wrong_results(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo_root = Path(directory)
            package = (
                repo_root / "cube" / "bird_format" / "demo" / "Q_en--S_en--V_en"
            )
            database = package / "database" / "db" / "db.sqlite"
            self._database(database)
            package.mkdir(parents=True, exist_ok=True)
            (package / "dev.json").write_text(
                json.dumps(
                    [
                        {
                            "question_id": 0,
                            "db_id": "db",
                            "question": "Count singers.",
                            "SQL": "SELECT count(*) FROM `歌手`",
                            "difficulty": "simple",
                            "logical_id": "logical_1",
                            "realization_id": "realization_keep",
                        },
                        {
                            "question_id": 1,
                            "db_id": "db",
                            "question": "Count French singers.",
                            "SQL": "SELECT count(*) FROM `歌手` WHERE `国籍` = 'France'",
                            "difficulty": "simple",
                            "logical_id": "logical_2",
                            "realization_id": "realization_retry",
                        },
                    ]
                ),
                encoding="utf-8",
            )
            cell_root = (
                repo_root / "runs" / "test-model" / "demo" / "Q_en--S_en--V_en"
            )
            cell_root.mkdir(parents=True)
            (cell_root / "predictions.jsonl").write_text(
                "\n".join(
                    [
                        json.dumps(
                            {
                                "experiment_protocol_version": "mol-sql-experiment-v0.1",
                                "instance_id": "realization_keep",
                                "model": "test-model",
                                "status": "success",
                                "prediction_sql": "SELECT count(*) FROM `歌手`",
                                "raw_response": "SELECT count(*) FROM `歌手`",
                                "error_type": None,
                                "error_message": None,
                                "attempts": 1,
                                "latency_seconds": 0.1,
                                "prompt_tokens": 1,
                                "completion_tokens": 1,
                                "total_tokens": 2,
                                "finished_at": "2026-01-01T00:00:00+00:00",
                            },
                            sort_keys=True,
                        ),
                        json.dumps(
                            {
                                "experiment_protocol_version": "mol-sql-experiment-v0.1",
                                "instance_id": "realization_retry",
                                "model": "test-model",
                                "status": "success",
                                "prediction_sql": (
                                    "SELECT count(*) FROM `歌手` WHERE `国籍` = 'France'"
                                ),
                                "raw_response": (
                                    "SELECT count(*) FROM `歌手` WHERE `国籍` = 'France'"
                                ),
                                "error_type": None,
                                "error_message": None,
                                "attempts": 1,
                                "latency_seconds": 0.1,
                                "prompt_tokens": 1,
                                "completion_tokens": 1,
                                "total_tokens": 2,
                                "finished_at": "2026-01-01T00:00:00+00:00",
                            },
                            sort_keys=True,
                        ),
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            (cell_root / "evaluation.jsonl").write_text(
                "\n".join(
                    [
                        json.dumps(
                            {
                                "experiment_protocol_version": "mol-sql-experiment-v0.1",
                                "instance_id": "realization_keep",
                                "status": "correct",
                                "execution_match": 1,
                                "error_message": None,
                                "latency_seconds": 0.01,
                            },
                            sort_keys=True,
                        ),
                        json.dumps(
                            {
                                "experiment_protocol_version": "mol-sql-experiment-v0.1",
                                "instance_id": "realization_retry",
                                "status": "prediction_missing",
                                "execution_match": 0,
                                "error_message": "no successful prediction",
                                "latency_seconds": 0.0,
                            },
                            sort_keys=True,
                        ),
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            with unittest.mock.patch(
                "mol_sql.experiments.runner.direct_zs.evaluate_sql",
                wraps=__import__(
                    "mol_sql.experiments.evaluation.execution", fromlist=["evaluate_sql"]
                ).evaluate_sql,
            ) as mocked_evaluate:
                manifest = run_direct_zs(
                    DirectZSOptions(
                        repo_root=repo_root,
                        cube_root=Path("cube"),
                        output_root=Path("runs"),
                        model="test-model",
                        sources=("demo",),
                        cells=("Q_en--S_en--V_en",),
                        stages=("eval",),
                        workers=1,
                    )
                )
            evaluations = {
                json.loads(line)["instance_id"]: json.loads(line)
                for line in (cell_root / "evaluation.jsonl")
                .read_text(encoding="utf-8")
                .splitlines()
                if line.strip()
            }
            progress = json.loads(
                (repo_root / "runs" / "test-model" / "progress.json").read_text(
                    encoding="utf-8"
                )
            )
        self.assertEqual(manifest.status, "completed")
        self.assertEqual(manifest.counts["evaluated"], 2)
        self.assertEqual(manifest.counts["correct"], 2)
        self.assertEqual(evaluations["realization_keep"]["status"], "correct")
        self.assertEqual(evaluations["realization_retry"]["status"], "correct")
        self.assertEqual(mocked_evaluate.call_count, 1)
        self.assertEqual(
            mocked_evaluate.call_args.kwargs["instance_id"], "realization_retry"
        )
        self.assertEqual(progress["stages"]["eval"]["completed"], 2)
        self.assertEqual(progress["stages"]["eval"]["correct"], 2)


if __name__ == "__main__":
    unittest.main()
