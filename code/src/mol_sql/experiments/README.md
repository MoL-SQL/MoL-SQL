# `experiments/`

Direct-ZS on MoL-Cube BIRD-format packages, plus Cube/Full accuracy analysis.

```bash
PYTHONPATH=code/src python -m mol_sql.cli experiments run-direct-zs \
  --model qwen3.6-35b-a3b --api-profile dashscope --workers 2
```

Credentials: `OPENAI_API_KEY` and `OPENAI_BASE_URL`. Per-sample records go to
`artifacts/runs/cube/direct_zs/<model>/`.

Prompt protocol: `methods/DIRECT_ZS_PROTOCOL.md`.

Direct-FS, Baseline-CoT, and Q-to-DB are in the repo-root `experiments/` directory.

- `runner/` — Direct-ZS scheduling, resume, checkpoints
- `evaluation/` — SQL extract, execute, compare
- `methods/` — Direct-ZS prompt protocol
- `analysis/` — Cube and Full accuracy reports
