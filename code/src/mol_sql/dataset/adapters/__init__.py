"""Source adapters for the five MoL-Full core workloads."""

from __future__ import annotations

from .base import AdaptedSource, SourceAdapter, load_source_specs
from .bird import BirdAdapter
from .bull import BullAdapter
from .ehrsql import EHRSQLAdapter
from .kaggledbqa import KaggleDBQAAdapter
from .spider import SpiderAdapter

ADAPTERS: dict[str, type[SourceAdapter]] = {
    "spider": SpiderAdapter,
    "bird": BirdAdapter,
    "bull": BullAdapter,
    "ehrsql": EHRSQLAdapter,
    "kaggledbqa": KaggleDBQAAdapter,
}


def adapter_for(source_family: str, repo_root, spec) -> SourceAdapter:
    try:
        adapter_type = ADAPTERS[source_family]
    except KeyError as exc:
        raise ValueError(f"unsupported source_family: {source_family}") from exc
    return adapter_type(repo_root, spec)


def execution_sql_for(source_family: str, sql: str) -> str:
    """Apply the source evaluator's deterministic SQL preprocessing."""

    try:
        adapter_type = ADAPTERS[source_family]
    except KeyError:
        return sql
    return adapter_type.execution_sql(sql)


__all__ = [
    "AdaptedSource",
    "SourceAdapter",
    "adapter_for",
    "execution_sql_for",
    "load_source_specs",
]
