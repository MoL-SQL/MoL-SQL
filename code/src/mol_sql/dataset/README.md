# `dataset/`

Unify source Text-to-SQL workloads into logical instances, then materialize,
audit, and export language configurations.

```bash
PYTHONPATH=code/src python -m mol_sql.cli dataset --help
```

- `adapters/` — Spider, BIRD, BULL, EHRSQL, KaggleDBQA
- `full/` — four-cell MoL-Full
- `cube/` — eight-cell MoL-Cube
- `audit/` — automatic gates
- `statistics/` — composition and quality reports
