# Language migration

Translate an English or Chinese Text-to-SQL workload into the four aligned
language cells used by MoL-Full: `enq_end`, `enq_cnd`, `cnq_cnd`, `cnq_end`
(and the BULL `S`/`V` variants).

These scripts write into `seeds/<Source>/`. Point
`code/configs/dataset/mol_full_sources.yaml` at that directory, then run
`mol-sql dataset build-full`. Most users can skip this and use
`data/releases/` directly.

## Layout

- `data_preprocess/` — normalize origin dumps
- `data_translate/` — schema/value/SQL/question translation
- `data_validation/` — empty-SQL and LLM repair helpers
- `data_postprocess/` — BIRD-format export helpers
- `bash/translate_{spider,bird,bull,EHR,KaggleDBQA}.sh`

## Usage

Place the upstream origin dump under `seeds/<Source>/..._origin`, copy `.env`,
then from the repository root:

```bash
export SEED_ROOT=seeds
bash migrate/bash/translate_spider.sh 1     # preprocess
bash migrate/bash/translate_spider.sh 2     # DB + SQL
bash migrate/bash/translate_spider.sh 3     # questions
bash migrate/bash/translate_spider.sh 4     # assemble cnq_end
# or
bash migrate/bash/translate_spider.sh all
```

LLM prompts and replacement configs go to `migrate/work/` (`WORKDIR`).
API credentials come from the repository `.env`.
