# `data/`

MoL-SQL dataset releases. Code reads these packages through manifests; do not hard-code temporary directory names.

## Layout

- `releases/full/mol-full-v0.1/` — four-cell source-distribution suite
  (`Q_en/zh` × `DB_en/zh`)
- `releases/cube/mol-cube-v0.1/` — eight-cell diagnostic subset with independent
  question, schema, and value languages

SQLite files live next to each BIRD-format package. They are ignored by git;
keep them on disk for execution evaluation.

Rebuild from aligned seeds only if you have the upstream four-cell directories:

```bash
PYTHONPATH=code/src python -m mol_sql.cli dataset build-full
PYTHONPATH=code/src python -m mol_sql.cli dataset build-cube \
  data/releases/full/mol-full-v0.1 \
  --overwrite
```

Most users should load the packaged releases instead of rebuilding.
