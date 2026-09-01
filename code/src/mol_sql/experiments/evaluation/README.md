# `experiments/evaluation/`

SQL extraction, execution, and result comparison used by the Direct-ZS runner.

`execution.py` scores predicted SQL against gold execution results with a
timeout. Each prediction records parse, execution, timeout, and mismatch.
