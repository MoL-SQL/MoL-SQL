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
MODEL="${MODEL:-qwen3.6-27b}"

PYTHONPATH=code/src python -u -m mol_sql.cli experiments run-direct-zs \
  --cube-root data/releases/full/mol-full-v0.1 \
  --output-root artifacts/runs/full/direct_zs \
  --model "${MODEL}" \
  --api-profile dashscope \
  --sources bird bull ehrsql kaggledbqa spider \
  --cells Q_en--S_en--V_en Q_en--S_zh--V_zh Q_zh--S_en--V_en Q_zh--S_zh--V_zh \
  --stage "${STAGE}" \
  --workers "${WORKERS}"
