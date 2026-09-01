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

STAGE="${1:-all}"
WORKERS="${WORKERS:-8}"
MODEL="${MODEL:-deepseek-v4-flash}"

: "${OPENAI_API_KEY:?OPENAI_API_KEY is not set}"
: "${OPENAI_BASE_URL:?OPENAI_BASE_URL is not set}"

case "${STAGE}" in
  all|prompt|infer|eval) ;;
  *)
    echo "Usage: bash code/bash/run_cube.deepseek.sh [all|prompt|infer|eval]" >&2
    exit 2
    ;;
esac

PYTHONPATH=code/src python -u -m mol_sql.cli experiments run-direct-zs \
  --cube-root data/releases/cube/mol-cube-v0.1 \
  --output-root artifacts/runs/cube/direct_zs \
  --model "${MODEL}" \
  --api-profile openai \
  --sources bird bull ehrsql kaggledbqa spider \
  --stage "${STAGE}" \
  --workers "${WORKERS}" \
  --evaluation-timeout 30
