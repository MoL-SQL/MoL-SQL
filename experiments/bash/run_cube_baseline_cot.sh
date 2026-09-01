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

MODEL_ALIAS="${1:-qwen}"
shift || true

case "${MODEL_ALIAS}" in
  qwen)
    MODEL="${MODEL:-qwen3.6-35b-a3b}"
    API_PROFILE="dashscope"
    ;;
  deepseek|deepseek-pro|deepseek-v4-pro)
    MODEL="${MODEL:-deepseek-v4-pro}"
    API_PROFILE="dashscope"
    ;;
  deepseek-flash|deepseek-v4-flash)
    MODEL="${MODEL:-deepseek-v4-flash}"
    API_PROFILE="dashscope"
    ;;
  hkust-deepseek-pro)
    MODEL="${MODEL:-DeepSeek-V4-Pro}"
    API_PROFILE="hkustgz"
    ;;
  *)
    echo "Usage: bash experiments/bash/run_cube_baseline_cot.sh [qwen|deepseek-pro|deepseek-flash|hkust-deepseek-pro] [runner args...]" >&2
    exit 2
    ;;
esac

OUTPUT_ROOT="artifacts/experiments/cube/baseline_cot"
SOURCE="all"
STAGE="all"
DRY_RUN=0
ARGS=("$@")
for ((i = 0; i < ${#ARGS[@]}; i++)); do
  case "${ARGS[i]}" in
    --output-root)
      OUTPUT_ROOT="${ARGS[i + 1]}"
      ;;
    --output-root=*)
      OUTPUT_ROOT="${ARGS[i]#*=}"
      ;;
    --source)
      SOURCE="${ARGS[i + 1]}"
      ;;
    --source=*)
      SOURCE="${ARGS[i]#*=}"
      ;;
    --stage)
      STAGE="${ARGS[i + 1]}"
      ;;
    --stage=*)
      STAGE="${ARGS[i]#*=}"
      ;;
    --dry-run)
      DRY_RUN=1
      ;;
  esac
done

PYTHONPATH="${REPO_ROOT}/experiments${PYTHONPATH:+:${PYTHONPATH}}" python -u experiments/text2sql_exp/run_cube_baseline_cot.py \
  --model "${MODEL}" \
  --api-profile "${API_PROFILE}" \
  "$@"

if [[ "${DRY_RUN}" -eq 0 && ("${STAGE}" == "all" || "${STAGE}" == "eval") ]]; then
  RUN_ROOT="${OUTPUT_ROOT%/}/${MODEL}"
  if [[ "${SOURCE}" != "all" && "${SOURCE}" != *,* ]]; then
    SUMMARY_OUTPUT="${RUN_ROOT}/${SOURCE}/accuracy_summary"
  else
    SUMMARY_OUTPUT="${RUN_ROOT}/accuracy_summary"
  fi
  PYTHONPATH="${REPO_ROOT}/experiments${PYTHONPATH:+:${PYTHONPATH}}" python -u experiments/text2sql_exp/summarize_cube_results.py \
    "${RUN_ROOT}" \
    --output "${SUMMARY_OUTPUT}"
fi
