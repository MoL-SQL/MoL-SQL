#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "${REPO_ROOT}"

if [[ -f .env ]]; then
  set -a
  # shellcheck disable=SC1091
  source .env
  set +a
fi

STAGE="${STAGE:-all}"
WORKERS="${WORKERS:-8}"
MODEL="${MODEL:-qwen3.6-35b-a3b}"

PYTHONPATH=code/src python -u -m mol_sql.cli experiments run-direct-zs \
  --cube-root data/releases/cube/mol-cube-v0.1 \
  --output-root artifacts/runs/cube/direct_zs \
  --model "${MODEL}" \
  --sources bird bull ehrsql kaggledbqa spider \
  --api-profile dashscope \
  --stage "${STAGE}" \
  --workers "${WORKERS}"
