#!/usr/bin/env python3
"""Shared utilities for MoL-Cube Text-to-SQL experiment runners."""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping, Sequence


CELLS = (
    "Q_en--S_en--V_en",
    "Q_en--S_en--V_zh",
    "Q_en--S_zh--V_en",
    "Q_en--S_zh--V_zh",
    "Q_zh--S_en--V_en",
    "Q_zh--S_en--V_zh",
    "Q_zh--S_zh--V_en",
    "Q_zh--S_zh--V_zh",
)
FULL_CELLS = (
    "Q_en--S_en--V_en",
    "Q_en--S_zh--V_zh",
    "Q_zh--S_en--V_en",
    "Q_zh--S_zh--V_zh",
)
SOURCES = ("bird", "bull", "ehrsql", "kaggledbqa", "spider")

EXPERIMENTS_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = EXPERIMENTS_ROOT.parent
DEFAULT_CUBE_ROOT = REPO_ROOT / "data/releases/cube/mol-cube-v0.1/bird_format"
DEFAULT_FULL_ROOT = REPO_ROOT / "data/releases/full/mol-full-v0.1/bird_format"
DEFAULT_OUTPUT_ROOT = REPO_ROOT / "artifacts/experiments/cube"
DEFAULT_FULL_OUTPUT_ROOT = REPO_ROOT / "artifacts/experiments/full"
CUBE_OUTPUT_STYLE = "xml"
BIRD_EVALUATOR = Path(__file__).resolve().parent / "evaluation/bird/evaluation_ex.py"
DEFAULT_DIRECT_FS_EXAMPLES = (
    Path(__file__).resolve().parent / "few_shot_examples/cube_direct_fs.json"
)


@dataclass(frozen=True)
class CellPackage:
    source: str
    cell: str
    root: Path
    questions: Path
    gold: Path
    tables: Path
    databases: Path


def slugify(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "-", value).strip("-")


def parse_cell(cell: str) -> dict[str, str]:
    parts = cell.split("--")
    if len(parts) != 3:
        raise ValueError(f"Invalid Cube cell: {cell}")
    axes: dict[str, str] = {}
    for part in parts:
        if len(part) < 3 or part[1] != "_":
            raise ValueError(f"Invalid Cube cell axis: {part}")
        axes[part[0]] = part[2:]
    return axes


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def dump_json(path: Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        json.dump(payload, file, ensure_ascii=False, indent=2)
        file.write("\n")


def resolve_sources(value: str) -> tuple[str, ...]:
    if value == "all":
        return SOURCES
    requested = tuple(part.strip().lower() for part in value.split(",") if part.strip())
    invalid = sorted(set(requested) - set(SOURCES))
    if invalid:
        raise ValueError(f"Unsupported Cube sources: {', '.join(invalid)}")
    if not requested:
        raise ValueError("At least one Cube source is required")
    return requested


def resolve_cells(value: str) -> tuple[str, ...]:
    if value in ("all", "cube"):
        return CELLS
    if value == "full":
        return FULL_CELLS
    requested = tuple(part.strip() for part in value.split(",") if part.strip())
    invalid = [cell for cell in requested if cell not in CELLS]
    if invalid:
        raise ValueError(f"Unsupported Cube cells: {', '.join(invalid)}")
    if not requested:
        raise ValueError("At least one Cube cell is required")
    return requested


def discover_packages(
    cube_root: Path,
    sources: Iterable[str],
    cells: Iterable[str] | None = None,
) -> list[CellPackage]:
    selected_cells = tuple(cells) if cells is not None else CELLS
    packages: list[CellPackage] = []
    for source in sources:
        source_root = cube_root / source
        for cell in selected_cells:
            root = source_root / cell
            package = CellPackage(
                source=source,
                cell=cell,
                root=root,
                questions=root / "dev.json",
                gold=root / "dev_gold.sql",
                tables=root / "tables.json",
                databases=root / "database",
            )
            missing = [
                path
                for path in (
                    package.questions,
                    package.gold,
                    package.tables,
                    package.databases,
                )
                if not path.exists()
            ]
            if missing:
                formatted = ", ".join(str(path) for path in missing)
                raise FileNotFoundError(f"Incomplete Cube package {source}/{cell}: {formatted}")
            packages.append(package)
    return packages


def validate_aligned_logical_ids(
    packages: Sequence[CellPackage], limit_ids: int | None = None
) -> dict[str, list[str]]:
    by_source: dict[str, list[CellPackage]] = {}
    for package in packages:
        by_source.setdefault(package.source, []).append(package)

    selected: dict[str, list[str]] = {}
    for source, source_packages in by_source.items():
        reference: list[str] | None = None
        for package in source_packages:
            rows = load_json(package.questions)
            logical_ids = [str(row.get("logical_id", "")) for row in rows]
            if not all(logical_ids):
                raise ValueError(f"Missing logical_id in {package.questions}")
            if len(logical_ids) != len(set(logical_ids)):
                raise ValueError(f"Duplicate logical_id in {package.questions}")
            if reference is None:
                reference = logical_ids
            elif logical_ids != reference:
                raise ValueError(
                    f"Cell order mismatch for {source}: {package.cell} does not match {source_packages[0].cell}"
                )
        assert reference is not None
        selected[source] = reference[:limit_ids] if limit_ids is not None else reference
    return selected


def api_environment(profile: str, base: Mapping[str, str] | None = None) -> dict[str, str]:
    env = dict(base or os.environ)
    if profile == "dashscope":
        required = ("OPENAI_API_KEY", "OPENAI_BASE_URL")
    elif profile == "hkustgz":
        required = ("HKUSTGZ_API_KEY", "HKUSTGZ_BASE_URL")
        env["OPENAI_API_KEY"] = env.get("HKUSTGZ_API_KEY", "")
        env["OPENAI_BASE_URL"] = env.get("HKUSTGZ_BASE_URL", "")
    else:
        raise ValueError(f"Unsupported API profile: {profile}")

    missing = [name for name in required if not env.get(name)]
    if missing:
        raise RuntimeError(f"Missing API environment variables: {', '.join(missing)}")
    return env


def run_command(
    command: Sequence[str],
    *,
    cwd: Path = REPO_ROOT,
    env: Mapping[str, str] | None = None,
    dry_run: bool = False,
) -> None:
    printable = " ".join(str(part) for part in command)
    print(f"+ {printable}", file=sys.stderr)
    if dry_run:
        return
    merged = dict(env) if env is not None else dict(os.environ)
    pythonpath = merged.get("PYTHONPATH", "")
    prefix = str(EXPERIMENTS_ROOT)
    merged["PYTHONPATH"] = prefix if not pythonpath else f"{prefix}:{pythonpath}"
    subprocess.run(command, cwd=cwd, env=merged, check=True)


def cube_generate_prompts_command(
    dataset_dir: Path,
    db_base_dir: Path,
    output: Path,
    *,
    sample_rows: int,
    limit_ids: int | None,
    few_shot_file: Path | None = None,
    few_shot_map: Path | None = None,
    value_map: Path | None = None,
    prompt_mode: str = "none",
) -> list[str]:
    command = [
        sys.executable,
        "experiments/text2sql_exp/generate_prompts.py",
        "--dataset",
        "bird",
        "--dataset_dir",
        str(dataset_dir),
        "--db_base_dir",
        str(db_base_dir),
        "--output",
        str(output),
        "--sample_rows",
        str(sample_rows),
        "--output_style",
        CUBE_OUTPUT_STYLE,
        "--prompt_mode",
        prompt_mode,
    ]
    if few_shot_map is not None:
        command.extend(("--few_shot", "--few_shot_map", str(few_shot_map)))
    elif few_shot_file is not None:
        command.extend(("--few_shot", "--few_shot_file", str(few_shot_file)))
    if value_map is not None:
        command.extend(("--value_map", str(value_map)))
    if limit_ids is not None:
        command.extend(("--end_index", str(limit_ids)))
    return command


def cube_call_llm_command(
    prompt_json: Path,
    predictions_txt: Path,
    *,
    model: str,
    workers: int,
    max_tokens: int,
) -> list[str]:
    return [
        sys.executable,
        "experiments/text2sql_exp/call_llm.py",
        "--input",
        str(prompt_json),
        "--output",
        str(predictions_txt),
        "--model",
        model,
        "--workers",
        str(workers),
        "--max_tokens",
        str(max_tokens),
        "--output_style",
        CUBE_OUTPUT_STYLE,
    ]


def prepare_evaluation_inputs(
    package: CellPackage,
    predictions_txt: Path,
    output_dir: Path,
    limit_ids: int | None = None,
) -> tuple[Path, Path, Path, int]:
    questions = load_json(package.questions)
    if limit_ids is not None:
        questions = questions[:limit_ids]

    with predictions_txt.open("r", encoding="utf-8") as file:
        predictions = [line.rstrip("\n") for line in file]
    if len(predictions) != len(questions):
        raise ValueError(
            f"Prediction count mismatch for {package.source}/{package.cell}: "
            f"{len(predictions)} predictions vs {len(questions)} questions"
        )

    with package.gold.open("r", encoding="utf-8") as file:
        gold_lines = [line.rstrip("\n") for line in file]
    gold_lines = gold_lines[: len(questions)]
    if len(gold_lines) != len(questions):
        raise ValueError(
            f"Gold count mismatch for {package.source}/{package.cell}: "
            f"{len(gold_lines)} gold rows vs {len(questions)} questions"
        )

    output_dir.mkdir(parents=True, exist_ok=True)
    pred_json = output_dir / "predictions.json"
    gold_sql = output_dir / "gold.sql"
    diff_jsonl = output_dir / "difficulty.jsonl"
    dump_json(pred_json, {str(index): sql for index, sql in enumerate(predictions)})
    with gold_sql.open("w", encoding="utf-8") as file:
        for line in gold_lines:
            if "\t" in line:
                file.write(line + "\n")
                continue
            parts = line.rsplit(None, 1)
            file.write(("\t".join(parts) if len(parts) == 2 else line) + "\n")
    with diff_jsonl.open("w", encoding="utf-8") as file:
        for row in questions:
            payload = {"difficulty": row.get("difficulty", "simple")}
            file.write(json.dumps(payload, ensure_ascii=False) + "\n")
    return pred_json, gold_sql, diff_jsonl, len(questions)


def evaluate_predictions(
    package: CellPackage,
    predictions_txt: Path,
    output_dir: Path,
    *,
    limit_ids: int | None = None,
    num_cpus: int = 16,
    timeout: float = 30.0,
    dry_run: bool = False,
) -> Path:
    if dry_run:
        questions = load_json(package.questions)
        count = min(len(questions), limit_ids) if limit_ids is not None else len(questions)
        pred_json = output_dir / "predictions.json"
        gold_sql = output_dir / "gold.sql"
        diff_jsonl = output_dir / "difficulty.jsonl"
    else:
        pred_json, gold_sql, diff_jsonl, count = prepare_evaluation_inputs(
            package, predictions_txt, output_dir, limit_ids=limit_ids
        )
    eval_json = output_dir / "evaluation.json"
    command = [
        sys.executable,
        str(BIRD_EVALUATOR),
        "--predicted_sql_path",
        str(pred_json),
        "--ground_truth_path",
        str(gold_sql),
        "--db_root_path",
        f"{package.databases}/",
        "--num_cpus",
        str(num_cpus),
        "--meta_time_out",
        str(timeout),
        "--diff_json_path",
        str(diff_jsonl),
        "--questions_json_path",
        str(package.questions),
        "--sql_dialect",
        "SQLite",
        "--output",
        str(eval_json),
    ]
    run_command(command, dry_run=dry_run)
    print(
        f"Evaluated {count} rows for {package.source}/{package.cell} -> {eval_json}",
        file=sys.stderr,
    )
    return eval_json


def link_or_copy(source: Path, target: Path) -> None:
    if target.exists() or target.is_symlink():
        if target.is_dir() and not target.is_symlink():
            shutil.rmtree(target)
        else:
            target.unlink()
    target.parent.mkdir(parents=True, exist_ok=True)
    target.symlink_to(source.resolve(), target_is_directory=source.is_dir())
