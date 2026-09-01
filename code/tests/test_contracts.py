from __future__ import annotations

import unittest

from pydantic import ValidationError

from mol_sql.contracts.ids import stable_id
from mol_sql.contracts.models import Realization


class ContractTests(unittest.TestCase):
    def test_stable_id_is_deterministic_and_typed(self) -> None:
        self.assertEqual(
            stable_id("logical", "spider", 1),
            stable_id("logical", "spider", 1),
        )
        self.assertNotEqual(
            stable_id("logical", "spider", 1),
            stable_id("logical", "spider", 2),
        )
        self.assertTrue(stable_id("logical", "spider", 1).startswith("logical_"))

    def test_full_realization_requires_coupled_languages(self) -> None:
        with self.assertRaises(ValidationError):
            Realization(
                realization_id="r",
                logical_id="l",
                source_family="spider",
                source_sample_key="0",
                configuration="Q_en--S_en--V_en",
                question_language="en",
                schema_language="en",
                value_language="zh",
                database_id="db",
                split="dev",
                question="q",
                gold_sql="select 1",
                dataset_path="dev.json",
                tables_path="tables.json",
                database_path=None,
                replacement_map=None,
                input_hashes={},
            )


if __name__ == "__main__":
    unittest.main()
