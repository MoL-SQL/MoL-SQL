# `experiments/runner/`

Direct-ZS orchestration for MoL-Cube: prompt, infer, eval, resume.

`direct_zs.py` writes append-only checkpoints and, on a clean finish, one
record per instance. Reruns skip successes and retry request-level failures.

API credentials come from `OPENAI_API_KEY` / `OPENAI_BASE_URL`. Progress is in
`progress.json` and `progress.log` under the run directory.
