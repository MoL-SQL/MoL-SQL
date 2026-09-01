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

DATASET="BULL-cn"
SPLIT="dev"
DIRECTION="cn2en"
MODEL="qwen-plus"

PROMPTS_DIR="${WORKDIR}/prompts/bull/db_translate_prompt"
REPLACEMENT_CONFIGS_DIR="${WORKDIR}/replacement_configs/bull_replacements.json"
MANUAL_REPLACE_SQL="${WORKDIR}/replacement_configs/bull_manual_sql.json"

DATASET_DIR="${SEED_ROOT}/BULL-FinSQL"
CN_ORIGIN_ORIGIN_DIR="${DATASET_DIR}/BULL-cn-origin"
EN_ORIGIN_DIR="${DATASET_DIR}/BULL-en-origin"
CN_ORIGIN_DIR="${DATASET_DIR}/BULL-cnq-ends-cndv"
CNQ_CNDS_CNDV_DIR="${DATASET_DIR}/BULL-cnq-cnds-cndv"
CNQ_ENDS_ENDV_DIR="${DATASET_DIR}/BULL-cnq-ends-endv"
ENQ_ENDS_ENDV_DIR="${DATASET_DIR}/BULL-enq-ends-endv"
ENQ_CNDS_CNDV_DIR="${DATASET_DIR}/BULL-enq-cnds-cndv"


# Part 0: data preprocess (standardise BULL-cn-origin → BULL-cnq-ends-cndv)
if [ "$PART" = "all" ] || [ "$PART" = "0" ]; then
python -u migrate/data_preprocess/data_preprocess.py --dataset bull \
    --input ${CN_ORIGIN_ORIGIN_DIR} \
    --output ${CN_ORIGIN_DIR} \
    --split ${SPLIT} \
    --lang cn

# add hardness level
python -u migrate/data_preprocess/add_sql_level.py \
    --input ${CN_ORIGIN_DIR} \
    --split ${SPLIT}
fi

# Part 1: schema replacement preprocess (BULL-cnq-ends-cndv → BULL-cnq-cnds-cndv)
if [ "$PART" = "all" ] || [ "$PART" = "1" ]; then
python -u migrate/data_preprocess/schema_replacement.py \
    --input ${CN_ORIGIN_DIR} \
    --output ${CNQ_CNDS_CNDV_DIR} \
    --split ${SPLIT}
fi

# Part 2: database value translation (BULL-cnq-ends-cndv → BULL-cnq-ends-endv)
if [ "$PART" = "all" ] || [ "$PART" = "2" ]; then
python -u migrate/data_translate/database_translate.py --dataset ${DATASET} \
    --source-dir ${CN_ORIGIN_DIR} \
    --output-dir ${CNQ_ENDS_ENDV_DIR} \
    --replacements-config ${REPLACEMENT_CONFIGS_DIR} \
    --prompts-dir ${PROMPTS_DIR} \
    --direction ${DIRECTION} \
    --split ${SPLIT} \
    --model ${MODEL} \
    --values-only \
    --manual-replace-sql ${MANUAL_REPLACE_SQL} \
    --skip-prompts \
    --skip-llm \
    # --skip-db-translate \
    # --skip-sql-translate
fi

# Part 3: NL replace (BULL-cnq-ends-endv + EN questions from BULL-en-origin → BULL-enq-ends-endv)
# Use the dataset-provided English questions (index-aligned by q_id) instead of LLM-translating CN→EN.
if [ "$PART" = "all" ] || [ "$PART" = "3" ]; then
python -u migrate/data_translate/nl_replacement.py --dataset ${DATASET} \
    --base-dir ${CNQ_ENDS_ENDV_DIR} \
    --donor-dir ${EN_ORIGIN_DIR} \
    --output-dir ${ENQ_ENDS_ENDV_DIR} \
    --direction ${DIRECTION} \
    --split ${SPLIT}
fi

# Part 4: NL replace (DB from BULL-cnq-cnds-cndv + question from BULL-enq-ends-endv → BULL-enq-cnds-cndv)
if [ "$PART" = "all" ] || [ "$PART" = "4" ]; then
python -u migrate/data_translate/nl_replacement.py --dataset ${DATASET} \
    --base-dir ${CNQ_CNDS_CNDV_DIR} \
    --donor-dir ${ENQ_ENDS_ENDV_DIR} \
    --output-dir ${ENQ_CNDS_CNDV_DIR} \
    --direction ${DIRECTION} \
    --split ${SPLIT}
fi