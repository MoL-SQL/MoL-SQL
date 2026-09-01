# `tests/`

Offline regression tests for contracts, Full/Cube build, SQL rewrite, and
Direct-ZS plumbing. They use temporary SQLite fixtures and do not call APIs.

```bash
PYTHONPATH=code/src python -m unittest discover -s code/tests -v
```
