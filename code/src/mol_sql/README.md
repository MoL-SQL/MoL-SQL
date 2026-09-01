# `mol_sql`

Python package for MoL-SQL dataset construction and Direct-ZS experiments.

```bash
PYTHONPATH=code/src python -m mol_sql.cli --help
PYTHONPATH=code/src python -m mol_sql.cli dataset --help
PYTHONPATH=code/src python -m mol_sql.cli experiments run-direct-zs --help
```

- `cli.py` — command-line entry
- `contracts/` — records, stable IDs, hashing, JSONL I/O
- `dataset/` — source adapters, Full/Cube builders, audit, statistics
- `experiments/` — Direct-ZS runner, execution eval, Cube/Full analysis
