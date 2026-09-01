# `code/`

MoL-SQL Python package: dataset build/audit/export, Direct-ZS experiments, and
Cube/Full analysis.

## Setup

```bash
pip install -e code/
# or
PYTHONPATH=code/src python -m mol_sql.cli --help
```

## Dataset

```bash
PYTHONPATH=code/src python -m mol_sql.cli dataset build-full
PYTHONPATH=code/src python -m mol_sql.cli dataset audit-full \
  data/releases/full/mol-full-v0.1 --execute-equivalence
PYTHONPATH=code/src python -m mol_sql.cli dataset export-bird-full \
  data/releases/full/mol-full-v0.1 --database-mode symlink
PYTHONPATH=code/src python -m mol_sql.cli dataset stats-full \
  data/releases/full/mol-full-v0.1 --allow-draft --overwrite
PYTHONPATH=code/src python -m mol_sql.cli dataset build-cube \
  data/releases/full/mol-full-v0.1 \
  artifacts/paper_stats/dataset/provisional/mol-full-v0.1 \
  --allow-draft --overwrite
```

Rebuilding Full needs aligned four-cell seeds under `seeds/` (see
`configs/dataset/mol_full_sources.yaml`). Packaged `data/releases/` can be used
without those seeds.

## Direct-ZS

```bash
PYTHONPATH=code/src python -m mol_sql.cli experiments run-direct-zs \
  --model qwen3.6-35b-a3b --api-profile dashscope --workers 2
```

Direct-FS, Baseline-CoT, and Q-to-DB live under `experiments/` at the repo root.

## Tests

```bash
PYTHONPATH=code/src python -m unittest discover -s code/tests -v
```
