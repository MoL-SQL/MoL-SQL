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
SEED_ROOT="${SEED_ROOT:-seeds}"
WORKDIR="${WORKDIR:-migrate/work}"
PART=${1:-all}

DATASET="bird"
SPLIT="dev"
DIRECTION="en2cn"
MODEL="qwen-plus"
NL_TRANSLATE_PROMPT_STYLE="BIRD"

PROMPTS_DIR="${WORKDIR}/prompts/bird/db_translate_prompt"
REPLACEMENT_CONFIGS_DIR="${WORKDIR}/replacement_configs/bird_replacements.json"
MANUAL_REPLACE_SQL="${WORKDIR}/replacement_configs/bird_manual.json"

DATASET_DIR="${SEED_ROOT}/BIRD"
ORIGIN_DIR="${DATASET_DIR}/minidev_origin"
ENQ_END_DIR="${DATASET_DIR}/minidev_enq_end"
ENQ_CND_DIR="${DATASET_DIR}/minidev_enq_cnd"
CNQ_CND_DIR="${DATASET_DIR}/minidev_cnq_cnd"
CNQ_END_DIR="${DATASET_DIR}/minidev_cnq_end"


# Part 1: data preprocess (output dataset of enq_end)
if [ "$PART" = "all" ] || [ "$PART" = "1" ]; then
python -u migrate/data_preprocess/data_preprocess.py --dataset ${DATASET} \
    --input ${ORIGIN_DIR} \
    --output ${ENQ_END_DIR} \
    --split ${SPLIT}
fi

# Part 2: database and SQL translation (output dataset of enq_cnd)
if [ "$PART" = "all" ] || [ "$PART" = "2" ]; then
python -u migrate/data_translate/database_translate.py --dataset ${DATASET} \
    --source-dir ${ENQ_END_DIR} \
    --output-dir ${ENQ_CND_DIR} \
    --replacements-config ${REPLACEMENT_CONFIGS_DIR} \
    --prompts-dir ${PROMPTS_DIR} \
    --direction ${DIRECTION} \
    --split ${SPLIT} \
    --model ${MODEL} \
    # --skip-prompts --skip-llm \
    # --skip-db-translate \
    # --manual-replace-sql ${MANUAL_REPLACE_SQL} 
fi

# Part 3: NL translation (output dataset of cnq_cnd)
if [ "$PART" = "all" ] || [ "$PART" = "3" ]; then
python -u migrate/data_translate/nl_translate.py --dataset ${DATASET} \
    --source-dir ${ENQ_CND_DIR} \
    --output-dir ${CNQ_CND_DIR} \
    --replacements ${REPLACEMENT_CONFIGS_DIR} \
    --direction ${DIRECTION} \
    --split ${SPLIT} \
    --model ${MODEL} \
    --prompt_style ${NL_TRANSLATE_PROMPT_STYLE} \
    --no-sql
fi

# Part 4: NL replace (output dataset of cnq_end)
if [ "$PART" = "all" ] || [ "$PART" = "4" ]; then
python -u migrate/data_translate/nl_replacement.py --dataset ${DATASET} \
    --base-dir ${ENQ_END_DIR} \
    --donor-dir ${CNQ_CND_DIR} \
    --output-dir ${CNQ_END_DIR} \
    --direction ${DIRECTION} \
    --split ${SPLIT}
fi