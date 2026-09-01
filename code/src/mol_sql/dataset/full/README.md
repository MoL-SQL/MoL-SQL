# `dataset/full/`

Build the four-cell MoL-Full release from aligned source workloads.

```bash
PYTHONPATH=code/src python -m mol_sql.cli dataset build-full
PYTHONPATH=code/src python -m mol_sql.cli dataset audit-full \
  data/releases/full/mol-full-v0.1 --execute-equivalence
PYTHONPATH=code/src python -m mol_sql.cli dataset export-bird-full \
  data/releases/full/mol-full-v0.1 --database-mode symlink
PYTHONPATH=code/src python -m mol_sql.cli dataset validate-bird-full \
  data/releases/full/mol-full-v0.1
```

- `build.py` — adapters to logical instances and realizations
- `rewrite.py` — cross-language schema/value SQL rewrite
- `audit.py` — automatic gates
- `bird_export.py` — BIRD-compatible packages
- `freeze.py` — freeze gate (provenance, audit, hashes)
