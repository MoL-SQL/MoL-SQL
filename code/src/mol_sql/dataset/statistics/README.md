# `dataset/statistics/`

Composition, difficulty, treatment, and quality reports from Full/Cube releases.

```bash
PYTHONPATH=code/src python -m mol_sql.cli dataset stats-full \
  data/releases/full/mol-full-v0.1 --allow-draft --overwrite
PYTHONPATH=code/src python -m mol_sql.cli dataset stats-cube \
  data/releases/cube/mol-cube-v0.1 \
  artifacts/paper_stats/dataset/provisional/mol-full-v0.1 \
  --allow-engineering --overwrite
```

Outputs go under `artifacts/paper_stats/dataset/`.
