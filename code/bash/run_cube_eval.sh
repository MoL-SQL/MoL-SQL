#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "${REPO_ROOT}"

PYTHONPATH=code/src python -u -m mol_sql.cli experiments run-direct-zs \
  --cube-root data/releases/cube/mol-cube-v0.1 \
  --output-root artifacts/runs/cube/direct_zs \
  --model qwen3.6-35b-a3b \
  --api-profile dashscope \
  --sources bird \
  --limit-ids 2 \
  --stage eval \
  --workers 2
