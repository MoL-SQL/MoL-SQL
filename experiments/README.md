# Text-to-SQL experiments

Four Cube baselines on `data/releases/cube/mol-cube-v0.1/bird_format`.

| Method | Script |
|--------|--------|
| Direct-ZS | `bash/run_cube_direct_zs.sh` |
| Direct-FS | `bash/run_cube_direct_fs.sh` |
| Baseline-CoT | `bash/run_cube_baseline_cot.sh` |
| Q-to-DB Translate | `bash/run_cube_q_to_db_translate.sh` |

All methods use the same full-schema prompt budget and BIRD execution evaluator.
Direct-FS adds frozen English demonstrations. Baseline-CoT asks for
`<thinking>` then `<sql>`. Q-to-DB asks the model to rewrite the question into
the database language before emitting SQL.

## Setup

```bash
cp .env.example .env
pip install openai tqdm func_timeout requests
```

## Smoke (2 logical IDs, BIRD only)

```bash
bash experiments/bash/run_cube_direct_zs.sh qwen \
  --source bird \
  --limit-ids 2
```

`--stage prompt` writes prompts without calling the API.

## Full Cube (480 × 8)

```bash
bash experiments/bash/run_cube_direct_zs.sh qwen --source all
bash experiments/bash/run_cube_direct_fs.sh qwen --source all
bash experiments/bash/run_cube_baseline_cot.sh qwen --source all
bash experiments/bash/run_cube_q_to_db_translate.sh qwen --source all
```

Outputs: `artifacts/experiments/cube/<method>/<model>/<source>/<cell>/`.

Direct-ZS is also available as:

```bash
PYTHONPATH=code/src python -m mol_sql.cli experiments run-direct-zs \
  --model qwen3.6-35b-a3b --api-profile dashscope --workers 2
```
