# `dataset/audit/`

Automatic quality gates and human-audit summary for MoL-Full.

```bash
PYTHONPATH=code/src python -m mol_sql.cli dataset audit-full \
  data/releases/full/mol-full-v0.1 --execute-equivalence
PYTHONPATH=code/src python -m mol_sql.cli dataset human-audit-summary \
  data/releases/full/mol-full-v0.1/human_audit_queue.jsonl
```

- `automatic.py` — four-cell alignment, SQL rewrite, SQLite integrity, execution equivalence
- `human_audit.py` — reviewer completeness summary
