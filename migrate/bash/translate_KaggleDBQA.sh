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

DATASET="kaggledbqa"
SPLIT="dev"
DIRECTION="en2cn"
MODEL="qwen-plus"
NL_TRANSLATE_PROMPT_STYLE="Kaggle"

PROMPTS_DIR="${WORKDIR}/prompts/kaggledbqa/db_translate_prompt"
REPLACEMENT_CONFIGS_DIR="${WORKDIR}/replacement_configs/kaggledbqa_replacements.json"
MANUAL_REPLACE_SQL="${WORKDIR}/replacement_configs/kaggledbqa_manual.json"

DATASET_DIR="${SEED_ROOT}/KaggleDBQA"
ORIGIN_DIR="${DATASET_DIR}/kaggle-origin"
ENQ_END_DIR="${DATASET_DIR}/kaggle_enq_end"
ENQ_CND_DIR="${DATASET_DIR}/kaggle_enq_cnd"
CNQ_CND_DIR="${DATASET_DIR}/kaggle_cnq_cnd"
CNQ_END_DIR="${DATASET_DIR}/kaggle_cnq_end"


# Part 1: data preprocess (merge samples/*_test.json -> dev.json in enq_end)
if [ "$PART" = "all" ] || [ "$PART" = "1" ]; then
# python -u migrate/data_preprocess/data_preprocess.py --dataset ${DATASET} \
#     --input ${ORIGIN_DIR} \
#     --output ${ENQ_END_DIR} \
#     --split ${SPLIT}
# # use check_empty_sql.py to check if the sql is empty
# python -u migrate/data_preprocess/check_empty_sql.py \
#     --input "${ENQ_END_DIR}" \
#     --split "${SPLIT}" \
#     --output-json "${ENQ_END_DIR}/${SPLIT}_empty_sql.json" \
#     # --delete
# use script/data_preprocess/add_sql_level.py to add difficulty level
python -u migrate/data_preprocess/add_sql_level.py \
    --input "${ENQ_END_DIR}" \
    --split "${SPLIT}"
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
    --manual-replace-sql ${MANUAL_REPLACE_SQL} \
    --skip-prompts --skip-llm \
    # --skip-db-translate
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