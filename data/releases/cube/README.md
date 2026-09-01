# MoL-Cube v0.1

Balanced diagnostic subset sampled from MoL-Full. Each logical instance has all
eight `Q × S × V` realizations (English or Chinese on each axis).

480 logical instances × 8 cells = 3,840 realizations, 96 per source
(Spider, BIRD, BULL, EHRSQL, KaggleDBQA).

## Files

- `realizations.jsonl`, `membership.jsonl`, `candidate_profiles.jsonl`
- `databases/S_en--V_zh` and `databases/S_zh--V_en` — mixed-language SQLite
- `bird_format/<source>/<Q--S--V>/` — BIRD-compatible eval packages
- `audits/final-fixed-30s/` — eight-cell execution-equivalence audit
- `release_manifest.json`, `SHA256SUMS.json`

## Optional rebuild

```bash
PYTHONPATH=code/src python -m mol_sql.cli dataset build-cube \
  data/releases/full/mol-full-v0.1 \
  --overwrite
PYTHONPATH=code/src python -m mol_sql.cli dataset audit-cube \
  data/releases/cube/mol-cube-v0.1
```
