# `data/sources/`

Upstream Text-to-SQL workload provenance. The machine-readable registry is
`code/configs/dataset/mol_full_sources.yaml`. The Full builder copies
normalized evidence into each release's `source_records.jsonl`.

Do not commit raw upstream dumps here. Point the yaml `root` fields at local
seed directories when rebuilding.
