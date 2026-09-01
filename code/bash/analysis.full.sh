#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "${REPO_ROOT}"

MODEL="${MODEL:-qwen3.6-27b}"
RUN_ROOT="${RUN_ROOT:-artifacts/runs/full/direct_zs/${MODEL}}"
OUTPUT_DIR="${OUTPUT_DIR:-artifacts/analysis/full/${MODEL}}"
METHOD="${METHOD:-direct_zs}"
TITLE="${TITLE:-${MODEL} on MoL-Full}"

echo "Analyzing Full run"
echo "model=${MODEL}"
echo "run_root=${RUN_ROOT}"
echo "output_dir=${OUTPUT_DIR}"

PYTHONPATH=code/src python -u -m mol_sql.cli experiments analyze-full \
  --run-root "${RUN_ROOT}" \
  --output-dir "${OUTPUT_DIR}" \
  --model "${MODEL}" \
  --method "${METHOD}" \
  --title "${TITLE}"

echo "Completed. See ${OUTPUT_DIR}/report.md"
