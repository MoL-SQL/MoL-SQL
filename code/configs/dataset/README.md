# `configs/dataset/`

```bash
PYTHONPATH=code/src python -m mol_sql.cli dataset build-full \
  --source-config code/configs/dataset/mol_full_sources.yaml
```

- `mol_full_sources.yaml` — Spider, BIRD, BULL, EHRSQL, KaggleDBQA paths and licenses
- `PROVENANCE.md` — redistribution notes
- `replacements/` — applied replacement maps and fixed points
- `mol_cube_engineering_v0.1.yaml` — Cube sampler
- `execution_repairs_v0.1.json` / `execution_adjudications_v0.1.json`

BULL/FinSQL has no published license; do not redistribute those databases
without permission.
