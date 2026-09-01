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

DATASET="ehrsql"
SPLIT="dev"
DIRECTION="en2cn"
MODEL="qwen-plus"
NL_TRANSLATE_PROMPT_STYLE="EHRSQL"

PROMPTS_DIR="${WORKDIR}/prompts/ehrsql/db_translate_prompt"
REPLACEMENT_CONFIGS_DIR="${WORKDIR}/replacement_configs/ehrsql_replacements.json"
MANUAL_REPLACE_SQL="${WORKDIR}/replacement_configs/ehrsql_manual.json"

DATASET_DIR="${SEED_ROOT}/EHRSQL"
ORIGIN_DIR="${DATASET_DIR}/EHRSQL-origin"
ENQ_END_DIR="${DATASET_DIR}/EHR-enq-end"
ENQ_CND_DIR="${DATASET_DIR}/EHR-enq-cnd"
CNQ_CND_DIR="${DATASET_DIR}/EHR-cnq-cnd"
CNQ_END_DIR="${DATASET_DIR}/EHR-cnq-end"


# Part 1: data preprocess (output dataset of enq_end)
# Merges eicu + mimic_iii valid splits into one dev.json (answerable only),
# splits off is_impossible items into dev_unanswerable.json, copies tables.json,
# symlinks both <db>.sqlite under database/<db>/, and writes
# ${ORIGIN_DIR}/statistic.json with db/table/column/row counts.
if [ "$PART" = "all" ] || [ "$PART" = "1" ]; then
python -u migrate/data_preprocess/data_preprocess.py --dataset ${DATASET} \
    --input ${ORIGIN_DIR} \
    --output ${ENQ_END_DIR} \
    --split ${SPLIT}
fi

# Part 2a: regenerate the replacements config via LLM (reuses existing prompts).
# Only rewrites ${REPLACEMENT_CONFIGS_DIR}; DB/SQL translation is done in Part 2.
# After the LLM run, re-applies the manual overrides documented in
# ${WORKDIR}/replacement_configs/ehrsql_manual.txt and fails loudly if
# any db ends up with an empty "values" list (guards against the truncated
# schema-phase save that previously wiped all value translations).
if [ "$PART" = "2a" ]; then
BACKUP="${REPLACEMENT_CONFIGS_DIR}.bak.$(date +%s)"
cp "${REPLACEMENT_CONFIGS_DIR}" "${BACKUP}"
echo "[Part 2a] Backed up config to ${BACKUP}"

python -u migrate/data_translate/database_translate.py --dataset ${DATASET} \
    --source-dir ${ENQ_END_DIR} \
    --output-dir ${ENQ_CND_DIR} \
    --replacements-config ${REPLACEMENT_CONFIGS_DIR} \
    --prompts-dir ${PROMPTS_DIR} \
    --direction ${DIRECTION} \
    --split ${SPLIT} \
    --model ${MODEL} \
    --skip-prompts --skip-db-translate --skip-sql-translate

python -u - "${REPLACEMENT_CONFIGS_DIR}" <<'PYEOF'
import json, sys

path = sys.argv[1]
with open(path, "r", encoding="utf-8") as f:
    config = json.load(f)

# Manual overrides from ehrsql_manual.txt: disambiguate LLM value-collapses.
OVERRIDES = {
    ("eicu", "medication", "routeadmin", "oral"): "口服(oral)",
    ("eicu", "medication", "routeadmin", "po"): "口服(po)",
    ("mimic_iii", "PRESCRIPTIONS", "ROUTE", "oral"): "口服(oral)",
    ("mimic_iii", "PRESCRIPTIONS", "ROUTE", "po"): "口服(po)",
    ("eicu", "treatment", "treatmentname", "anticonvulsant"): "抗惊厥药(anticonvulsant)",
    ("eicu", "treatment", "treatmentname", "anticonvulsants"): "抗惊厥药(anticonvulsants)",
}
applied = 0
for db_id, db_config in config.items():
    for entry in db_config.get("values", []):
        key = (db_id, entry[0], entry[1], entry[2])
        if key in OVERRIDES and entry[3] != OVERRIDES[key]:
            print(f"[Part 2a] Override {db_id}.{entry[0]}.{entry[1]}: "
                  f"{entry[2]!r} -> {OVERRIDES[key]!r} (was {entry[3]!r})")
            entry[3] = OVERRIDES[key]
            applied += 1

empty = [db_id for db_id, c in config.items() if not c.get("values")]
if empty:
    sys.exit(f"[Part 2a] ERROR: empty 'values' for db(s): {empty}. "
             f"Step 2 content phase did not complete; config NOT usable.")

with open(path, "w", encoding="utf-8") as f:
    json.dump(config, f, ensure_ascii=False, indent=2)

for db_id, c in config.items():
    print(f"[Part 2a] {db_id}: {len(c['values'])} value translations")
print(f"[Part 2a] Applied {applied} manual overrides.")
PYEOF
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
    --skip-prompts --skip-llm \
        # --manual-replace-sql ${MANUAL_REPLACE_SQL} \
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
