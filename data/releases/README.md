# `data/releases/`

Materialized MoL-SQL packages. Each release has a `release_manifest.json`,
JSONL records, checksums, and BIRD-compatible `bird_format/` folders.

## Packages

- `full/mol-full-v0.1/` — 4,223 logical instances, 16,892 four-cell realizations
- `cube/mol-cube-v0.1/` — 480 logical instances, 3,840 eight-cell realizations

Load `release_manifest.json` first, then the JSONL files or
`bird_format/<source>/<Q--S--V>/{dev.json,dev_gold.sql,tables.json,database/}`.
