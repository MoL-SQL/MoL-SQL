#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "${REPO_ROOT}"

MODEL="${MODEL:-deepseek-v4-flash}"
RUN_ROOT="${RUN_ROOT:-artifacts/runs/cube/direct_zs-fixed/${MODEL}}"
OUTPUT_DIR="${OUTPUT_DIR:-artifacts/analysis/cube/${MODEL}-fixed}"
METHOD="${METHOD:-direct_zs}"
TITLE="${TITLE:-${MODEL} on MoL-Cube}"

echo "Analyzing Cube run"
echo "model=${MODEL}"
echo "run_root=${RUN_ROOT}"
echo "output_dir=${OUTPUT_DIR}"

PYTHONPATH=code/src python -u -m mol_sql.cli experiments analyze-cube \
  --run-root "${RUN_ROOT}" \
  --output-dir "${OUTPUT_DIR}" \
  --model "${MODEL}" \
  --method "${METHOD}" \
  --title "${TITLE}"

echo "Completed. See ${OUTPUT_DIR}/report.md"
