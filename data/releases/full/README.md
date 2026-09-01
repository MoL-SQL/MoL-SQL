# MoL-Full v0.1

Each logical instance has four coupled schema/value configurations:

`Q_en--S_en--V_en`, `Q_zh--S_en--V_en`, `Q_en--S_zh--V_zh`, `Q_zh--S_zh--V_zh`.

Sources: Spider (1030), BIRD mini-dev (498), BULL (1000), EHRSQL (1511),
KaggleDBQA (184).

## Files

- `logical_instances.jsonl` — language-agnostic canonical question/SQL
- `realizations.jsonl` — four-cell questions, SQL, and database references
- `legacy_id_map.jsonl` — stable IDs to original sample indices
- `source_records.jsonl` — source provenance
- `bird_format/<source>/<configuration>/` — BIRD-compatible eval packages
- `release_manifest.json`, `SHA256SUMS.json`

## Optional rebuild

```bash
PYTHONPATH=code/src python -m mol_sql.cli dataset build-full
PYTHONPATH=code/src python -m mol_sql.cli dataset audit-full \
  data/releases/full/mol-full-v0.1 --execute-equivalence
PYTHONPATH=code/src python -m mol_sql.cli dataset export-bird-full \
  data/releases/full/mol-full-v0.1 --database-mode symlink
```
