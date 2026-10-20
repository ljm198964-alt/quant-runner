import unittest
from research.m3.compare_penaltyblog_snapshots import compare


def snapshot(test_hash, input_hash="i1", version="1.13.1"):
    return {"generated_utc": "2026-10-20T00:00:00+00:00", "test_set_fingerprint_sha256": test_hash,
            "input_fingerprint_sha256": input_hash, "penaltyblog_version": version,
            "models": [{"model": "poisson", "overall_metrics": {
                "1x2": {"log_loss": 1.0, "brier": 0.6, "n_predicted": 100, "n_test_total": 120},
                "ah_home_0": {"log_loss": 1.0, "brier": 0.6, "n_predicted": 100, "n_test_total": 120},
                "ou_over_2_5": {"log_loss": 0.7, "brier": 0.25, "n_predicted": 100, "n_test_total": 120}}}]}


class PenaltyblogComparisonTests(unittest.TestCase):
    def test_initial_baseline_has_no_delta(self):
        result = compare(None, snapshot("a"))
        self.assertEqual(result["status"], "INITIAL_BASELINE_NO_COMPARISON")
        self.assertFalse(result["automatic_model_promotion"])

    def test_changed_test_set_suppresses_deltas(self):
        result = compare(snapshot("a"), snapshot("b"))
        self.assertEqual(result["status"], "TEST_SET_CHANGED_NO_DIRECT_DELTA")
        self.assertIsNone(result["comparison"][0]["metrics"]["log_loss"]["delta"])

    def test_same_test_set_reports_descriptive_delta(self):
        current = snapshot("a", input_hash="i2")
        current["models"][0]["overall_metrics"]["1x2"]["log_loss"] = 0.9
        result = compare(snapshot("a"), current)
        self.assertEqual(result["status"], "COMPARABLE_TEST_SET")
        self.assertAlmostEqual(result["comparison"][0]["metrics"]["log_loss"]["delta"], -0.1)
        self.assertFalse(result["input_fingerprint_matches"])


if __name__ == "__main__":
    unittest.main()
