#!/usr/bin/env python3
"""Run Direct-ZS on MoL-Cube with a uniform prompt and evaluator."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from cube_common import (
    CUBE_OUTPUT_STYLE,
    DEFAULT_CUBE_ROOT,
    DEFAULT_OUTPUT_ROOT,
    api_environment,
    cube_call_llm_command,
    cube_generate_prompts_command,
    discover_packages,
    dump_json,
    evaluate_predictions,
    resolve_cells,
    resolve_sources,
    run_command,
    slugify,
    validate_aligned_logical_ids,
)
from summarize_cube_results import maybe_write_source_accuracy_summary


STAGES = ("prompt", "infer", "eval")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", required=True)
    parser.add_argument(
        "--api-profile",
        required=True,
        choices=("dashscope", "hkustgz"),
    )
    parser.add_argument("--source", default="all", help="all or comma-separated sources")
    parser.add_argument(
        "--cells",
        default="all",
        help="all/cube (8-cell), full (4-cell Q×DB), or comma-separated cells",
    )
    parser.add_argument("--cube-root", type=Path, default=DEFAULT_CUBE_ROOT)
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT / "direct_zs")
    parser.add_argument("--stage", choices=("all", *STAGES), default="all")
    parser.add_argument("--limit-ids", type=int, default=None)
    parser.add_argument("--sample-rows", type=int, default=3)
    parser.add_argument("--workers", type=int, default=10)
    parser.add_argument("--max-tokens", type=int, default=4096)
    parser.add_argument("--num-cpus", type=int, default=16)
    parser.add_argument("--eval-timeout", type=float, default=30.0)
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def selected_stages(stage: str) -> tuple[str, ...]:
    return STAGES if stage == "all" else (stage,)


def main() -> None:
    args = parse_args()
    if args.limit_ids is not None and args.limit_ids <= 0:
        raise SystemExit("--limit-ids must be positive")
    if args.sample_rows < 0:
        raise SystemExit("--sample-rows must be non-negative")

    sources = resolve_sources(args.source)
    cells = resolve_cells(args.cells)
    packages = discover_packages(args.cube_root.resolve(), sources, cells)
    selected_ids = validate_aligned_logical_ids(packages, args.limit_ids)
    stages = selected_stages(args.stage)
    env = api_environment(args.api_profile) if "infer" in stages and not args.dry_run else None

    run_root = args.output_root.resolve() / slugify(args.model)
    started_at = datetime.now(timezone.utc)
    manifest = {
        "version": 1,
        "release": str(args.cube_root.resolve()),
        "method": "direct_zs",
        "model": args.model,
        "api_profile": args.api_profile,
        "sources": list(sources),
        "cells": sorted({package.cell for package in packages}),
        "output_style": CUBE_OUTPUT_STYLE,
        "limit_ids": args.limit_ids,
        "sample_rows": args.sample_rows,
        "workers": args.workers,
        "max_tokens": args.max_tokens,
        "stages": list(stages),
        "started_at": started_at.isoformat(),
        "status": "running",
        "logical_ids": selected_ids,
        "outputs": {},
    }
    manifest_path = run_root / "run_manifest.json"
    if not args.dry_run:
        dump_json(manifest_path, manifest)

    try:
        for index, package in enumerate(packages):
            cell_root = run_root / package.source / package.cell
            prompt_json = cell_root / "prompts.json"
            predictions_txt = cell_root / "predictions.txt"
            eval_root = cell_root / "evaluation"
            cell_output = {
                "questions": str(package.questions),
                "prompts": str(prompt_json),
                "predictions": str(predictions_txt),
            }

            if "prompt" in stages:
                run_command(
                    cube_generate_prompts_command(
                        package.root,
                        package.root,
                        prompt_json,
                        sample_rows=args.sample_rows,
                        limit_ids=args.limit_ids,
                    ),
                    dry_run=args.dry_run,
                )

            if "infer" in stages:
                if not prompt_json.exists() and not args.dry_run:
                    raise FileNotFoundError(f"Prompt file missing: {prompt_json}")
                run_command(
                    cube_call_llm_command(
                        prompt_json,
                        predictions_txt,
                        model=args.model,
                        workers=args.workers,
                        max_tokens=args.max_tokens,
                    ),
                    env=env,
                    dry_run=args.dry_run,
                )

            if "eval" in stages:
                if not predictions_txt.exists() and not args.dry_run:
                    raise FileNotFoundError(f"Prediction file missing: {predictions_txt}")
                eval_json = evaluate_predictions(
                    package,
                    predictions_txt,
                    eval_root,
                    limit_ids=args.limit_ids,
                    num_cpus=args.num_cpus,
                    timeout=args.eval_timeout,
                    dry_run=args.dry_run,
                )
                cell_output["evaluation"] = str(eval_json)

            manifest["outputs"][f"{package.source}/{package.cell}"] = cell_output
            if not args.dry_run:
                dump_json(manifest_path, manifest)
            maybe_write_source_accuracy_summary(
                run_root,
                packages,
                index,
                eval_enabled="eval" in stages,
                dry_run=args.dry_run,
            )
    except Exception:
        manifest["status"] = "failed"
        manifest["finished_at"] = datetime.now(timezone.utc).isoformat()
        if not args.dry_run:
            dump_json(manifest_path, manifest)
        raise

    manifest["status"] = "completed"
    manifest["finished_at"] = datetime.now(timezone.utc).isoformat()
    manifest["expected_generation_calls"] = sum(
        len(ids) * len(cells) for ids in selected_ids.values()
    )
    if not args.dry_run:
        dump_json(manifest_path, manifest)
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
