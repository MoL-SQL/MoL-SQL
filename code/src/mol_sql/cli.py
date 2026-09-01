"""Command-line entry point for the MoL-SQL pipeline."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from mol_sql.contracts.io import load_jsonl, write_json
from mol_sql.contracts.models import HumanAuditItem
from mol_sql.dataset.audit.human_audit import summarize_human_audit
from mol_sql.dataset.full import (
    BirdExportOptions,
    BuildOptions,
    audit_mol_full,
    build_mol_full,
    export_bird_full,
    freeze_mol_full,
    validate_bird_full,
)
from mol_sql.dataset.full.repair import (
    restore_ehrsql_eicu_icd9code,
    restore_mapped_column_by_key,
)
from mol_sql.dataset.full.diagnose import diagnose_execution_failures
from mol_sql.dataset.full.execution_repair import apply_execution_repairs
from mol_sql.dataset.cube import (
    CubeAuditOptions,
    CubeBirdExportOptions,
    CubeBuildOptions,
    audit_mol_cube,
    build_mol_cube,
    export_bird_cube,
    load_logical_ids,
    validate_bird_cube,
)
from mol_sql.dataset.statistics import (
    CubeStatisticsOptions,
    DatasetPaperReportOptions,
    FullStatisticsOptions,
    generate_cube_statistics,
    generate_dataset_paper_report,
    generate_full_statistics,
)
from mol_sql.experiments.analysis.cube import (
    DEFAULT_CELLS,
    DEFAULT_SOURCES,
    CubeAnalysisOptions,
    analyze_cube,
    parse_override_cell,
)
from mol_sql.experiments.analysis.full import (
    DEFAULT_CELLS as FULL_DEFAULT_CELLS,
    FullAnalysisOptions,
    analyze_full,
)
from mol_sql.experiments.runner.direct_zs import DirectZSOptions, run_direct_zs
from mol_sql.experiments.runner.legacy_import import import_legacy_direct_zs


def _looks_like_repo_root(path: Path) -> bool:
    return (path / "code" / "pyproject.toml").is_file()


def _repo_root(value: str) -> Path:
    path = Path(value).resolve()
    if not _looks_like_repo_root(path):
        raise argparse.ArgumentTypeError(
            f"{path} does not look like the MoL-SQL repository root"
        )
    return path


def _build_full(args: argparse.Namespace) -> int:
    manifest = build_mol_full(
        BuildOptions(
            repo_root=args.repo_root,
            source_config=Path(args.source_config),
            output_dir=Path(args.output_dir),
            release_id=args.release_id,
            check_database_integrity=not args.skip_database_integrity,
            execute_equivalence=args.execute_equivalence,
            execution_timeout_seconds=args.execution_timeout,
            human_audit_per_source=args.human_audit_per_source,
            requested_status="frozen" if args.freeze else "draft",
            source_families=tuple(args.sources) if args.sources else None,
        )
    )
    print(json.dumps(manifest.model_dump(mode="json"), ensure_ascii=False, indent=2))
    if args.freeze and manifest.status != "frozen":
        print(
            f"Freeze refused: {len(manifest.blockers)} blocker(s); "
            "a draft release was written."
        )
        return 2
    return 0


def _freeze_full(args: argparse.Namespace) -> int:
    try:
        manifest = freeze_mol_full(args.release_dir)
    except ValueError as exc:
        print(str(exc))
        return 2
    print(json.dumps(manifest.model_dump(mode="json"), ensure_ascii=False, indent=2))
    return 0


def _audit_full(args: argparse.Namespace) -> int:
    manifest = audit_mol_full(
        repo_root=args.repo_root,
        source_config=Path(args.source_config),
        release_dir=args.release_dir,
        check_database_integrity=not args.skip_database_integrity,
        execute_equivalence=args.execute_equivalence,
        execution_timeout_seconds=args.execution_timeout,
    )
    print(json.dumps(manifest.model_dump(mode="json"), ensure_ascii=False, indent=2))
    return 0 if not manifest.blockers else 2


def _human_summary(args: argparse.Namespace) -> int:
    items = load_jsonl(args.queue, HumanAuditItem)
    summary = summarize_human_audit(items)
    if args.output:
        write_json(args.output, summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if summary["ready_for_freeze"] else 2


def _repair_ehrsql_icd9code(args: argparse.Namespace) -> int:
    result = restore_ehrsql_eicu_icd9code(
        source_database=args.source_database,
        target_database=args.target_database,
        apply=args.apply,
        backup_path=args.backup,
    )
    print(json.dumps(result.__dict__, ensure_ascii=False, indent=2))
    return 0 if result.mismatches_after == 0 or not args.apply else 2


def _diagnose_execution(args: argparse.Namespace) -> int:
    count = diagnose_execution_failures(
        repo_root=args.repo_root,
        source_config=Path(args.source_config),
        failures_path=args.failures,
        output_path=args.output,
        timeout_seconds=args.execution_timeout,
    )
    print(json.dumps({"diagnosed": count, "output": str(args.output)}, indent=2))
    return 0


def _repair_mapped_column(args: argparse.Namespace) -> int:
    result = restore_mapped_column_by_key(
        source_database=args.source_database,
        target_database=args.target_database,
        replacement_map=args.replacement_map,
        database_id=args.database_id,
        source_table=args.source_table,
        source_key=args.source_key,
        source_column=args.source_column,
        target_table=args.target_table,
        target_key=args.target_key,
        target_column=args.target_column,
        map_table=args.map_table,
        map_column=args.map_column,
        apply=args.apply,
        backup_path=args.backup,
    )
    print(json.dumps(result.__dict__, ensure_ascii=False, indent=2))
    return 0 if result.mismatches_after == 0 or not args.apply else 2


def _apply_execution_repairs(args: argparse.Namespace) -> int:
    result = apply_execution_repairs(
        repo_root=args.repo_root,
        source_config=Path(args.source_config),
        repairs_path=args.repairs,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def _export_bird_full(args: argparse.Namespace) -> int:
    result = export_bird_full(
        BirdExportOptions(
            repo_root=args.repo_root,
            release_dir=args.release_dir,
            output_dir=args.output_dir,
            database_mode=args.database_mode,
            distribution=args.distribution,
            overwrite=args.overwrite,
        )
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def _validate_bird_full(args: argparse.Namespace) -> int:
    result = validate_bird_full(
        repo_root=args.repo_root,
        release_dir=args.release_dir,
        output_dir=args.output_dir,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def _stats_full(args: argparse.Namespace) -> int:
    manifest = generate_full_statistics(
        FullStatisticsOptions(
            repo_root=args.repo_root,
            release_dir=args.release_dir,
            output_dir=args.output_dir,
            allow_draft=args.allow_draft,
            overwrite=args.overwrite,
        )
    )
    print(json.dumps(manifest.model_dump(mode="json"), ensure_ascii=False, indent=2))
    return 0


def _stats_cube(args: argparse.Namespace) -> int:
    manifest = generate_cube_statistics(
        CubeStatisticsOptions(
            repo_root=args.repo_root,
            cube_release_dir=args.cube_release_dir,
            full_statistics_dir=args.full_statistics_dir,
            output_dir=args.output_dir,
            allow_engineering=args.allow_engineering,
            overwrite=args.overwrite,
        )
    )
    print(json.dumps(manifest.model_dump(mode="json"), ensure_ascii=False, indent=2))
    return 0


def _export_bird_cube(args: argparse.Namespace) -> int:
    result = export_bird_cube(
        CubeBirdExportOptions(
            repo_root=args.repo_root,
            release_dir=args.release_dir,
            output_dir=args.output_dir,
            database_mode=args.database_mode,
            distribution=args.distribution,
            overwrite=args.overwrite,
        )
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def _validate_bird_cube(args: argparse.Namespace) -> int:
    result = validate_bird_cube(
        repo_root=args.repo_root,
        release_dir=args.release_dir,
        output_dir=args.output_dir,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def _paper_dataset_report(args: argparse.Namespace) -> int:
    output = generate_dataset_paper_report(
        DatasetPaperReportOptions(
            repo_root=args.repo_root,
            full_statistics_dir=args.full_statistics_dir,
            cube_statistics_dir=args.cube_statistics_dir,
            output_path=args.output,
        )
    )
    print(json.dumps({"output": output.as_posix()}, ensure_ascii=False, indent=2))
    return 0


def _build_cube(args: argparse.Namespace) -> int:
    manifest = build_mol_cube(
        CubeBuildOptions(
            repo_root=args.repo_root,
            full_release_dir=args.full_release_dir,
            full_statistics_dir=args.full_statistics_dir,
            sampler_config=Path(args.sampler_config),
            output_dir=Path(args.output_dir),
            allow_draft=args.allow_draft,
            overwrite=args.overwrite,
            resume=args.resume,
            execute_equivalence=not args.skip_execution_equivalence,
            execution_timeout_seconds=args.execution_timeout,
        )
    )
    print(json.dumps(manifest.model_dump(mode="json"), ensure_ascii=False, indent=2))
    return 0 if not any(item.startswith("cube_build_failures:") for item in manifest.blockers) else 2


def _run_direct_zs(args: argparse.Namespace) -> int:
    stages = ("prompt", "infer", "eval") if args.stage == "all" else (args.stage,)
    manifest = run_direct_zs(
        DirectZSOptions(
            repo_root=args.repo_root,
            cube_root=args.cube_root,
            output_root=args.output_root,
            model=args.model,
            api_profile=args.api_profile,
            sources=tuple(args.sources) if args.sources else None,
            cells=tuple(args.cells) if args.cells else None,
            stages=stages,
            limit_ids=args.limit_ids,
            sample_rows_per_table=args.sample_rows,
            workers=args.workers,
            temperature=args.temperature,
            max_tokens=args.max_tokens,
            request_timeout_seconds=args.request_timeout,
            max_retries=args.max_retries,
            retry_backoff_seconds=args.retry_backoff,
            evaluation_timeout_seconds=args.evaluation_timeout,
            dry_run=args.dry_run,
        )
    )
    print(json.dumps(manifest.model_dump(mode="json"), ensure_ascii=False, indent=2))
    return 2 if manifest.status in {"failed", "completed_with_errors"} else 0


def _import_legacy_direct_zs(args: argparse.Namespace) -> int:
    summary = import_legacy_direct_zs(
        legacy_root=args.legacy_root.resolve(),
        output_root=args.output_root.resolve(),
        model=args.model,
        overwrite=args.overwrite,
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


def _analyze_cube(args: argparse.Namespace) -> int:
    override_cells = (
        tuple(parse_override_cell(token) for token in args.override_cells)
        if args.override_cells
        else None
    )
    payload = analyze_cube(
        CubeAnalysisOptions(
            repo_root=args.repo_root,
            run_root=args.run_root,
            output_dir=args.output_dir,
            baseline_root=args.baseline_root,
            override_cells=override_cells,
            sources=tuple(args.sources) if args.sources else DEFAULT_SOURCES,
            cells=tuple(args.cells) if args.cells else DEFAULT_CELLS,
            expected_rows_per_cell=args.expected_rows,
            model=args.model,
            method=args.method,
            title=args.title,
            analysis_date=args.analysis_date,
        )
    )
    print(json.dumps(payload["summary"]["metrics"]["overall"], ensure_ascii=False, indent=2))
    print(f"Wrote report to {Path(args.output_dir) / 'report.md'}")
    return 0


def _analyze_full(args: argparse.Namespace) -> int:
    payload = analyze_full(
        FullAnalysisOptions(
            repo_root=args.repo_root,
            run_root=args.run_root,
            output_dir=args.output_dir,
            sources=tuple(args.sources) if args.sources else DEFAULT_SOURCES,
            cells=tuple(args.cells) if args.cells else FULL_DEFAULT_CELLS,
            model=args.model,
            method=args.method,
            title=args.title,
            analysis_date=args.analysis_date,
        )
    )
    print(json.dumps(payload["summary"]["metrics"]["overall"], ensure_ascii=False, indent=2))
    print(f"Wrote report to {Path(args.output_dir) / 'report.md'}")
    return 0


def _audit_cube(args: argparse.Namespace) -> int:
    summary = audit_mol_cube(
        CubeAuditOptions(
            repo_root=args.repo_root,
            cube_release_dir=args.cube_release_dir,
            full_release_dir=args.full_release_dir,
            output_dir=args.output_dir,
            timeout_seconds=args.execution_timeout,
            workers=args.workers,
            logical_ids=(
                load_logical_ids(args.logical_ids_from)
                if args.logical_ids_from
                else None
            ),
        )
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    failed = any(
        summary["status_counts"].get(key, 0)
        for key in ("error", "mismatch", "timeout")
    )
    return 2 if failed else 0


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(prog="mol-sql")
    root.add_argument(
        "--repo-root",
        type=_repo_root,
        default=Path.cwd().resolve(),
        help="MoL-SQL repository root (default: current directory)",
    )
    commands = root.add_subparsers(dest="command", required=True)
    dataset = commands.add_parser("dataset")
    dataset_commands = dataset.add_subparsers(dest="dataset_command", required=True)

    build = dataset_commands.add_parser("build-full")
    build.add_argument(
        "--source-config",
        default="code/configs/dataset/mol_full_sources.yaml",
    )
    build.add_argument(
        "--output-dir",
        default="data/releases/full/mol-full-v0.1",
    )
    build.add_argument("--release-id", default="mol-full-v0.1")
    build.add_argument("--skip-database-integrity", action="store_true")
    build.add_argument("--execute-equivalence", action="store_true")
    build.add_argument("--execution-timeout", type=float, default=30.0)
    build.add_argument("--human-audit-per-source", type=int, default=20)
    build.add_argument(
        "--sources",
        nargs="+",
        help="Optional source-family subset for smoke/audit runs",
    )
    build.add_argument("--freeze", action="store_true")
    build.set_defaults(handler=_build_full)

    repair = dataset_commands.add_parser("repair-ehrsql-icd9code")
    repair.add_argument("source_database", type=Path)
    repair.add_argument("target_database", type=Path)
    repair.add_argument(
        "--apply",
        action="store_true",
        help="Apply the repair; without this flag the command is read-only.",
    )
    repair.add_argument(
        "--backup",
        type=Path,
        help="Optional non-existing path for a pre-repair database copy.",
    )
    repair.set_defaults(handler=_repair_ehrsql_icd9code)

    diagnose = dataset_commands.add_parser("diagnose-execution")
    diagnose.add_argument("failures", type=Path)
    diagnose.add_argument("output", type=Path)
    diagnose.add_argument(
        "--source-config",
        default="code/configs/dataset/mol_full_sources.yaml",
    )
    diagnose.add_argument("--execution-timeout", type=float, default=60.0)
    diagnose.set_defaults(handler=_diagnose_execution)

    mapped = dataset_commands.add_parser("repair-mapped-column")
    mapped.add_argument("source_database", type=Path)
    mapped.add_argument("target_database", type=Path)
    mapped.add_argument("replacement_map", type=Path)
    mapped.add_argument("database_id")
    mapped.add_argument("source_table")
    mapped.add_argument("source_key")
    mapped.add_argument("source_column")
    mapped.add_argument("target_table")
    mapped.add_argument("target_key")
    mapped.add_argument("target_column")
    mapped.add_argument("--map-table")
    mapped.add_argument("--map-column")
    mapped.add_argument("--apply", action="store_true")
    mapped.add_argument("--backup", type=Path)
    mapped.set_defaults(handler=_repair_mapped_column)

    execution_repair = dataset_commands.add_parser("apply-execution-repairs")
    execution_repair.add_argument("repairs", type=Path)
    execution_repair.add_argument(
        "--source-config",
        default="code/configs/dataset/mol_full_sources.yaml",
    )
    execution_repair.set_defaults(handler=_apply_execution_repairs)

    bird_export = dataset_commands.add_parser("export-bird-full")
    bird_export.add_argument("release_dir", type=Path)
    bird_export.add_argument("--output-dir", type=Path)
    bird_export.add_argument(
        "--database-mode",
        choices=("copy", "hardlink", "symlink"),
        default="symlink",
    )
    bird_export.add_argument(
        "--distribution",
        choices=("local", "public"),
        default="local",
    )
    bird_export.add_argument("--overwrite", action="store_true")
    bird_export.set_defaults(handler=_export_bird_full)

    bird_validate = dataset_commands.add_parser("validate-bird-full")
    bird_validate.add_argument("release_dir", type=Path)
    bird_validate.add_argument("--output-dir", type=Path)
    bird_validate.set_defaults(handler=_validate_bird_full)

    statistics = dataset_commands.add_parser("stats-full")
    statistics.add_argument("release_dir", type=Path)
    statistics.add_argument("--output-dir", type=Path)
    statistics.add_argument("--allow-draft", action="store_true")
    statistics.add_argument("--overwrite", action="store_true")
    statistics.set_defaults(handler=_stats_full)

    cube_statistics = dataset_commands.add_parser("stats-cube")
    cube_statistics.add_argument("cube_release_dir", type=Path)
    cube_statistics.add_argument("full_statistics_dir", type=Path)
    cube_statistics.add_argument("--output-dir", type=Path)
    cube_statistics.add_argument("--allow-engineering", action="store_true")
    cube_statistics.add_argument("--overwrite", action="store_true")
    cube_statistics.set_defaults(handler=_stats_cube)

    paper_dataset = dataset_commands.add_parser("paper-dataset-report")
    paper_dataset.add_argument("full_statistics_dir", type=Path)
    paper_dataset.add_argument("cube_statistics_dir", type=Path)
    paper_dataset.add_argument(
        "--output",
        type=Path,
        default=Path(
            "artifacts/paper_stats/dataset/provisional/"
            "PAPER_DATASET_TABLES_FIGURES.md"
        ),
    )
    paper_dataset.set_defaults(handler=_paper_dataset_report)

    cube = dataset_commands.add_parser("build-cube")
    cube.add_argument("full_release_dir", type=Path)
    cube.add_argument("full_statistics_dir", type=Path)
    cube.add_argument(
        "--sampler-config",
        default="code/configs/dataset/mol_cube_engineering_v0.1.yaml",
    )
    cube.add_argument(
        "--output-dir",
        default="data/releases/cube/mol-cube-v0.1",
    )
    cube.add_argument("--allow-draft", action="store_true")
    cube.add_argument("--overwrite", action="store_true")
    cube.add_argument("--resume", action="store_true")
    cube.add_argument("--execution-timeout", type=float, default=30.0)
    cube.add_argument("--skip-execution-equivalence", action="store_true")
    cube.set_defaults(handler=_build_cube)

    cube_audit = dataset_commands.add_parser("audit-cube")
    cube_audit.add_argument("cube_release_dir", type=Path)
    cube_audit.add_argument("full_release_dir", type=Path)
    cube_audit.add_argument("--output-dir", type=Path)
    cube_audit.add_argument("--logical-ids-from", type=Path)
    cube_audit.add_argument("--execution-timeout", type=float, default=5.0)
    cube_audit.add_argument("--workers", type=int, default=4)
    cube_audit.set_defaults(handler=_audit_cube)

    cube_bird_export = dataset_commands.add_parser("export-bird-cube")
    cube_bird_export.add_argument("release_dir", type=Path)
    cube_bird_export.add_argument("--output-dir", type=Path)
    cube_bird_export.add_argument(
        "--database-mode",
        choices=("copy", "hardlink", "symlink"),
        default="hardlink",
    )
    cube_bird_export.add_argument(
        "--distribution",
        choices=("local", "public"),
        default="local",
    )
    cube_bird_export.add_argument("--overwrite", action="store_true")
    cube_bird_export.set_defaults(handler=_export_bird_cube)

    cube_bird_validate = dataset_commands.add_parser("validate-bird-cube")
    cube_bird_validate.add_argument("release_dir", type=Path)
    cube_bird_validate.add_argument("--output-dir", type=Path)
    cube_bird_validate.set_defaults(handler=_validate_bird_cube)

    freeze = dataset_commands.add_parser("freeze-full")
    freeze.add_argument("release_dir", type=Path)
    freeze.set_defaults(handler=_freeze_full)

    audit = dataset_commands.add_parser("audit-full")
    audit.add_argument("release_dir", type=Path)
    audit.add_argument(
        "--source-config",
        default="code/configs/dataset/mol_full_sources.yaml",
    )
    audit.add_argument("--skip-database-integrity", action="store_true")
    audit.add_argument("--execute-equivalence", action="store_true")
    audit.add_argument("--execution-timeout", type=float, default=30.0)
    audit.set_defaults(handler=_audit_full)

    human = dataset_commands.add_parser("human-audit-summary")
    human.add_argument("queue", type=Path)
    human.add_argument("--output", type=Path)
    human.set_defaults(handler=_human_summary)

    experiments = commands.add_parser("experiments")
    experiment_commands = experiments.add_subparsers(
        dest="experiment_command", required=True
    )
    direct_zs = experiment_commands.add_parser("run-direct-zs")
    direct_zs.add_argument(
        "--cube-root",
        type=Path,
        default=Path("data/releases/cube/mol-cube-v0.1"),
    )
    direct_zs.add_argument(
        "--output-root",
        type=Path,
        default=Path("artifacts/runs/cube/direct_zs"),
    )
    direct_zs.add_argument("--model", required=True)
    direct_zs.add_argument(
        "--api-profile",
        choices=("dashscope", "openai", "hkustgz"),
        default="dashscope",
    )
    direct_zs.add_argument("--sources", nargs="+")
    direct_zs.add_argument("--cells", nargs="+")
    direct_zs.add_argument(
        "--stage", choices=("all", "prompt", "infer", "eval"), default="all"
    )
    direct_zs.add_argument("--limit-ids", type=int)
    direct_zs.add_argument("--sample-rows", type=int, default=3)
    direct_zs.add_argument("--workers", type=int, default=2)
    direct_zs.add_argument("--temperature", type=float, default=0.0)
    direct_zs.add_argument("--max-tokens", type=int, default=4096)
    direct_zs.add_argument("--request-timeout", type=float, default=180.0)
    direct_zs.add_argument("--max-retries", type=int, default=6)
    direct_zs.add_argument("--retry-backoff", type=float, default=15.0)
    direct_zs.add_argument("--evaluation-timeout", type=float, default=30.0)
    direct_zs.add_argument("--dry-run", action="store_true")
    direct_zs.set_defaults(handler=_run_direct_zs)

    legacy_import = experiment_commands.add_parser("import-legacy-direct-zs")
    legacy_import.add_argument("legacy_root", type=Path)
    legacy_import.add_argument("--model", required=True)
    legacy_import.add_argument(
        "--output-root",
        type=Path,
        default=Path("artifacts/runs/cube/direct_zs"),
    )
    legacy_import.add_argument("--overwrite", action="store_true")
    legacy_import.set_defaults(handler=_import_legacy_direct_zs)

    analyze = experiment_commands.add_parser("analyze-cube")
    analyze.add_argument(
        "--run-root",
        type=Path,
        required=True,
        help="Primary run directory under artifacts/runs/...",
    )
    analyze.add_argument(
        "--output-dir",
        type=Path,
        required=True,
        help="Directory for report.md / summary.json / cells.csv / sources.csv",
    )
    analyze.add_argument(
        "--baseline-root",
        type=Path,
        help="Optional baseline run to merge against; override cells come from --run-root",
    )
    analyze.add_argument(
        "--override-cells",
        nargs="+",
        help="source/cell tokens replaced from --run-root when --baseline-root is set",
    )
    analyze.add_argument("--sources", nargs="+")
    analyze.add_argument("--cells", nargs="+")
    analyze.add_argument("--expected-rows", type=int, default=96)
    analyze.add_argument("--model")
    analyze.add_argument("--method", default="direct_zs")
    analyze.add_argument("--title")
    analyze.add_argument("--analysis-date")
    analyze.set_defaults(handler=_analyze_cube)

    analyze_full_cmd = experiment_commands.add_parser("analyze-full")
    analyze_full_cmd.add_argument(
        "--run-root",
        type=Path,
        required=True,
        help="Primary Full run directory under artifacts/runs/...",
    )
    analyze_full_cmd.add_argument(
        "--output-dir",
        type=Path,
        required=True,
        help="Directory for report.md / summary.json / cells.csv / sources.csv",
    )
    analyze_full_cmd.add_argument("--sources", nargs="+")
    analyze_full_cmd.add_argument("--cells", nargs="+")
    analyze_full_cmd.add_argument("--model")
    analyze_full_cmd.add_argument("--method", default="direct_zs")
    analyze_full_cmd.add_argument("--title")
    analyze_full_cmd.add_argument("--analysis-date")
    analyze_full_cmd.set_defaults(handler=_analyze_full)
    return root


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    return args.handler(args)


if __name__ == "__main__":
    raise SystemExit(main())
