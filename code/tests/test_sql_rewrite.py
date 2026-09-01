from __future__ import annotations

import unittest

import sqlglot

from mol_sql.dataset.full.rewrite import (
    rewrite_sql,
    rewrite_sql_components,
    transplant_sql_values,
)


class SQLRewriteTests(unittest.TestCase):
    def test_scope_aware_identifier_and_literal_rewrite(self) -> None:
        replacements = {
            "tables": [["customers", "客户"]],
            "columns": [
                ["customers", "id", "编号"],
                ["customers", "currency", "货币"],
            ],
            "values": [["customers", "currency", "EUR", "欧元"]],
        }
        result = rewrite_sql(
            "SELECT c.id FROM customers AS c WHERE c.currency = 'EUR'",
            replacements,
        )
        self.assertEqual(result.status, "pass")
        self.assertIsNotNone(result.sql)
        parsed = sqlglot.parse_one(result.sql, read="sqlite")
        self.assertEqual(next(parsed.find_all(sqlglot.exp.Table)).name, "客户")
        self.assertIn("欧元", result.sql)
        self.assertIn("编号", result.sql)

    def test_value_only_rewrite_accepts_double_quoted_sqlite_literals(self) -> None:
        replacements = {
            "tables": [],
            "columns": [],
            "values": [["airports", "code", "UAL", "UAL（联合航空）"]],
        }
        result = rewrite_sql_components(
            'SELECT id FROM airports WHERE code = "UAL" AND state = "Wisconsin"',
            replacements,
            rewrite_schema=False,
            rewrite_values=True,
        )
        self.assertEqual(result.status, "pass")
        self.assertIn("UAL（联合航空）", result.sql)
        self.assertIn("'Wisconsin'", result.sql)

    def test_value_only_rewrite_falls_back_for_unique_cte_value_mapping(self) -> None:
        replacements = {
            "tables": [],
            "columns": [],
            "values": [["atom", "element", "h", "氢"]],
        }
        result = rewrite_sql_components(
            "WITH q AS (SELECT element FROM atom) "
            "SELECT COUNT(CASE WHEN element = 'h' THEN 1 END) FROM q",
            replacements,
            rewrite_schema=False,
            rewrite_values=True,
        )
        self.assertEqual(result.status, "pass")
        self.assertIn("氢", result.sql)

    def test_schema_only_rewrite_preserves_double_quoted_value_case(self) -> None:
        replacements = {
            "tables": [["airports", "机场"]],
            "columns": [["airports", "code", "代码"]],
            "values": [],
        }
        result = rewrite_sql_components(
            'SELECT code FROM airports WHERE code = "UAL"',
            replacements,
            rewrite_schema=True,
            rewrite_values=False,
        )
        self.assertEqual(result.status, "pass")
        self.assertIn("'UAL'", result.sql)
        self.assertIn("机场", result.sql)

    def test_transplants_partial_like_literal_from_coupled_donor(self) -> None:
        result = transplant_sql_values(
            "SELECT note FROM death WHERE note LIKE '%East%'",
            "SELECT `备注` FROM `伤亡` WHERE `备注` LIKE '%东%'",
        )
        self.assertEqual(result.status, "pass")
        self.assertIn("%东%", result.sql)

    def test_transplant_does_not_treat_quoted_left_column_as_value(self) -> None:
        result = transplant_sql_values(
            'SELECT airline FROM airlines WHERE abbreviation = "UAL"',
            'SELECT `航空公司名称` FROM `航空公司` WHERE `缩写` = "UAL（联合航空）"',
        )
        self.assertEqual(result.status, "pass")
        self.assertIn("UAL（联合航空）", result.sql)
        self.assertNotIn("'缩写'", result.sql)

    def test_transplant_preserves_format_literals_by_source_value(self) -> None:
        source = (
            "SELECT STRFTIME('%Y', dob) FROM drivers "
            "WHERE nationality = 'Japanese'"
        )
        target = (
            "SELECT STRFTIME('%Y', drivers.dob) FROM drivers AS drivers "
            "WHERE drivers.nationality = 'Japanese'"
        )
        donor = (
            "SELECT STRFTIME('%Y', 出生日期) FROM 车手 "
            "WHERE 国籍 = '日本籍'"
        )
        result = transplant_sql_values(target, donor, source)
        self.assertEqual(result.status, "pass")
        self.assertIn("STRFTIME('%Y'", result.sql)
        self.assertIn("日本籍", result.sql)


if __name__ == "__main__":
    unittest.main()
