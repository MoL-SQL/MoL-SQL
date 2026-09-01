"""Scope-aware SQL rewriting for a frozen database replacement map."""

from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass
from typing import Any

import sqlglot
from sqlglot import exp
from sqlglot.optimizer.qualify import qualify
from sqlglot.optimizer.scope import traverse_scope


@dataclass(frozen=True)
class RewriteResult:
    status: str
    sql: str | None
    error_code: str | None = None


def _maps(
    replacements: dict[str, Any],
) -> tuple[dict[str, str], dict[tuple[str, str], str]]:
    tables = {
        str(source).casefold(): str(target)
        for source, target in replacements.get("tables", [])
    }
    columns = {
        (str(table).casefold(), str(source).casefold()): str(target)
        for table, source, target in replacements.get("columns", [])
    }
    return tables, columns


def _schema(replacements: dict[str, Any]) -> dict[str, dict[str, str]]:
    schema: dict[str, dict[str, str]] = {}
    for table, column, _ in replacements.get("columns", []):
        schema.setdefault(str(table).casefold(), {})[
            str(column).casefold()
        ] = "TEXT"
    for table, column, _, _ in replacements.get("values", []):
        schema.setdefault(str(table).casefold(), {})[
            str(column).casefold()
        ] = "TEXT"
    return schema


def _quote(identifier: exp.Identifier, target: str) -> None:
    identifier.set("this", target)
    identifier.set(
        "quoted",
        any(ord(character) > 127 or not character.isalnum() for character in target),
    )


def _base_table(scope: Any, qualifier: str) -> str | None:
    source = scope.sources.get(qualifier)
    return source.name.casefold() if isinstance(source, exp.Table) else None


def _literal_context(literal: exp.Literal, scope: Any) -> tuple[str, str] | None:
    node: exp.Expression = literal
    while node.parent is not None:
        parent = node.parent
        if isinstance(
            parent,
            (exp.EQ, exp.NEQ, exp.Like, exp.ILike, exp.In, exp.Between),
        ):
            column = parent.find(exp.Column)
            if column is None or not column.table:
                return None
            table = _base_table(scope, column.table)
            return (table, column.name.casefold()) if table else None
        if isinstance(parent, exp.Select):
            return None
        node = parent
    return None


def _normalize_double_quoted_predicate_values(tree: exp.Expression) -> None:
    for column in list(tree.find_all(exp.Column)):
        predicate = column.find_ancestor(
            exp.EQ,
            exp.NEQ,
            exp.GT,
            exp.GTE,
            exp.LT,
            exp.LTE,
            exp.Like,
            exp.ILike,
            exp.In,
            exp.Between,
        )
        if (
            not column.table
            and isinstance(column.this, exp.Identifier)
            and bool(column.this.args.get("quoted"))
            and predicate is not None
            and all(node is not column for node in predicate.this.walk())
        ):
            column.replace(exp.Literal.string(column.name))


def rewrite_sql_components(
    sql: str,
    replacements: dict[str, Any],
    *,
    rewrite_schema: bool,
    rewrite_values: bool,
) -> RewriteResult:
    """Rewrite selected SQL components after resolving their SQL scope."""

    try:
        table_map, column_map = _maps(replacements)
        tree = sqlglot.parse_one(sql, read="sqlite")
        _normalize_double_quoted_predicate_values(tree)
        tree = qualify(
            tree,
            schema=_schema(replacements),
            dialect="sqlite",
            allow_partial_qualification=True,
            validate_qualify_columns=False,
            quote_identifiers=False,
        )
        values = replacements.get("values", [])
        unique_value_targets: dict[str, set[str]] = {}
        for _, _, source, target in values:
            unique_value_targets.setdefault(str(source), set()).add(str(target))
        for scope in traverse_scope(tree):
            if rewrite_values:
                for literal in scope.expression.find_all(exp.Literal):
                    if (
                        not literal.is_string
                        or literal.find_ancestor(exp.Select) is not scope.expression
                    ):
                        continue
                    context = _literal_context(literal, scope)
                    rewritten = False
                    for table, column, source, target in values:
                        if (
                            literal.this == str(source)
                            and context
                            == (str(table).casefold(), str(column).casefold())
                        ):
                            literal.set("this", str(target))
                            rewritten = True
                            break
                    if not rewritten:
                        targets = unique_value_targets.get(str(literal.this), set())
                        if len(targets) == 1:
                            literal.set("this", next(iter(targets)))

            if rewrite_schema:
                for column in scope.columns:
                    table = _base_table(scope, column.table)
                    target = (
                        column_map.get((table, column.name.casefold()))
                        if table
                        else None
                    )
                    if target:
                        _quote(column.this, target)

                renamed_qualifiers: dict[str, str] = {}
                for alias, source in scope.sources.items():
                    if not isinstance(source, exp.Table):
                        continue
                    target = table_map.get(source.name.casefold())
                    if target:
                        _quote(source.this, target)
                        if alias.casefold() == source.name.casefold():
                            source.set("alias", None)
                            renamed_qualifiers[alias] = target
                for column in scope.columns:
                    if column.table in renamed_qualifiers:
                        _quote(
                            column.args["table"],
                            renamed_qualifiers[column.table],
                        )
        return RewriteResult(status="pass", sql=tree.sql(dialect="sqlite"))
    except Exception as exc:
        return RewriteResult(
            status="fail",
            sql=None,
            error_code=f"{type(exc).__name__}:{exc}",
        )


def transplant_sql_values(
    target_sql: str,
    donor_sql: str,
    source_sql: str | None = None,
) -> RewriteResult:
    """Copy ordered string literals from a coupled donor SQL realization."""

    try:
        target_tree = sqlglot.parse_one(target_sql, read="sqlite")
        donor_tree = sqlglot.parse_one(donor_sql, read="sqlite")
        _normalize_double_quoted_predicate_values(target_tree)
        _normalize_double_quoted_predicate_values(donor_tree)
        target_literals = [
            literal
            for literal in target_tree.find_all(exp.Literal)
            if literal.is_string
        ]
        donor_literals = [
            literal
            for literal in donor_tree.find_all(exp.Literal)
            if literal.is_string
        ]
        if source_sql is None:
            source_literals = target_literals
        else:
            source_tree = sqlglot.parse_one(source_sql, read="sqlite")
            _normalize_double_quoted_predicate_values(source_tree)
            source_literals = [
                literal
                for literal in source_tree.find_all(exp.Literal)
                if literal.is_string
            ]
        if len(source_literals) != len(donor_literals):
            raise ValueError(
                "source/donor string literal counts differ: "
                f"{len(source_literals)} != {len(donor_literals)}"
            )
        translations: dict[str, deque[str]] = defaultdict(deque)
        for source, donor in zip(source_literals, donor_literals):
            translations[str(source.this)].append(str(donor.this))
        for target in target_literals:
            donors = translations.get(str(target.this))
            if donors:
                target.set("this", donors.popleft())
        return RewriteResult(status="pass", sql=target_tree.sql(dialect="sqlite"))
    except Exception as exc:
        return RewriteResult(
            status="fail",
            sql=None,
            error_code=f"{type(exc).__name__}:{exc}",
        )


def rewrite_sql(sql: str, replacements: dict[str, Any]) -> RewriteResult:
    """Rewrite identifiers and literals after resolving their SQL scope."""

    return rewrite_sql_components(
        sql,
        replacements,
        rewrite_schema=True,
        rewrite_values=True,
    )
