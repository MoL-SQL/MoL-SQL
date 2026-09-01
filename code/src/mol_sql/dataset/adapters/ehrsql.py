"""EHRSQL source adapter."""

import re

from .base import SourceAdapter


class EHRSQLAdapter(SourceAdapter):
    source_family = "ehrsql"

    _VITAL_RANGES = {
        "temperature": (35.5, 38.1),
        "sao2": (95.0, 100.0),
        "heart rate": (60.0, 100.0),
        "respiration": (12.0, 18.0),
        "systolic bp": (90.0, 120.0),
        "diastolic bp": (60.0, 90.0),
        "mean bp": (60.0, 110.0),
    }
    _CURRENT_TIME = "2105-12-31 23:59:00"

    @classmethod
    def execution_sql(cls, sql: str) -> str:
        """Apply EHRSQL constants without lowercasing translated literals.

        The official evaluator lowercases English SQL.  Doing that to the
        translated workload corrupts case-sensitive values such as ``MCHC``,
        ``ACEI``, ``SC``, and ``μL`` in the Chinese database.
        """

        query = re.sub(
            r"\bcurrent_time\b",
            f"'{cls._CURRENT_TIME}'",
            sql,
            flags=re.IGNORECASE,
        )
        lowers = re.findall(
            r"\b([a-zA-Z0-9_]+_lower)\b", query, flags=re.IGNORECASE
        )
        uppers = re.findall(
            r"\b([a-zA-Z0-9_]+_upper)\b", query, flags=re.IGNORECASE
        )
        if lowers and uppers:
            lower, upper = lowers[0], uppers[0]
            lower_name = re.sub(r"_lower$", "", lower, flags=re.IGNORECASE)
            upper_name = re.sub(r"_upper$", "", upper, flags=re.IGNORECASE)
            if lower_name == upper_name:
                vital_range = cls._VITAL_RANGES.get(
                    lower_name.lower().replace("_", " ")
                )
                if vital_range:
                    query = re.sub(
                        rf"\b{re.escape(lower)}\b",
                        str(vital_range[0]),
                        query,
                        flags=re.IGNORECASE,
                    )
                    query = re.sub(
                        rf"\b{re.escape(upper)}\b",
                        str(vital_range[1]),
                        query,
                        flags=re.IGNORECASE,
                    )
        query = query.replace("''", "'").replace("< =", "<=")
        query = re.sub(r"%y", "%Y", query, flags=re.IGNORECASE)
        query = re.sub(r"%j", "%J", query, flags=re.IGNORECASE)
        return re.sub(
            r"'now'",
            f"'{cls._CURRENT_TIME}'",
            query,
            flags=re.IGNORECASE,
        )
