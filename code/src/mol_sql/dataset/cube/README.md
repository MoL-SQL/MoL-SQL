# `dataset/cube/`

Sample a balanced eight-cell diagnostic subset from MoL-Full and materialize
independent question, schema, and value languages.

```bash
PYTHONPATH=code/src python -m mol_sql.cli dataset build-cube \
  data/releases/full/mol-full-v0.1 \
  artifacts/paper_stats/dataset/provisional/mol-full-v0.1 \
  --allow-draft --overwrite
PYTHONPATH=code/src python -m mol_sql.cli dataset audit-cube \
  data/releases/cube/mol-cube-v0.1 \
  data/releases/full/mol-full-v0.1
PYTHONPATH=code/src python -m mol_sql.cli dataset export-bird-cube \
  data/releases/cube/mol-cube-v0.1 --overwrite
```

Use `--resume` after an interrupted mixed-SQLite build.
`dataset audit-cube` checks eight-cell execution equivalence.
