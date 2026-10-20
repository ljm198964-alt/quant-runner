import copy
import unittest

from research.m3.crown_pairing import audit_records
from research.m3.test_crown_evidence import synthetic_record


class CrownPairingTests(unittest.TestCase):
    def test_value_free_m3_pairing_summary(self):
        record = synthetic_record()
        result = audit_records([record])
        self.assertEqual(result["eligible_quote_pairs_by_market"], {"AH": 1, "OU": 1})
        rendered = str(result)
        self.assertNotIn("1.9", rendered)
        self.assertNotIn("Synthetic Home", rendered)

    def test_rejects_unverified_or_other_system_record(self):
        record = synthetic_record()
        record["forecast"]["system"] = "M1"
        with self.assertRaisesRegex(ValueError, "forecast.system must be M3"):
            audit_records([record])

    def test_no_rows_is_zero_coverage(self):
        result = audit_records([])
        self.assertEqual(result["validated_record_count"], 0)
        self.assertEqual(result["eligible_quote_pairs_by_market"], {"AH": 0, "OU": 0})


if __name__ == "__main__":
    unittest.main()
