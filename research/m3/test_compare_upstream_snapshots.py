import csv
import tempfile
import unittest
from pathlib import Path

from research.m3.compare_upstream_snapshots import compare


class UpstreamSnapshotComparisonTests(unittest.TestCase):
    def test_metric_delta_is_suppressed_when_test_sample_count_changes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            old, new = root / "old.csv", root / "new.csv"
            fields = ["model", "test_season", "n_test", "log_loss", "brier"]
            for path, n_test, log_loss in ((old, 100, 0.60), (new, 120, 0.55)):
                with path.open("w", newline="") as f:
                    writer = csv.DictWriter(f, fieldnames=fields)
                    writer.writeheader()
                    writer.writerow({"model": "lightgbm", "test_season": "2627",
                                     "n_test": n_test, "log_loss": log_loss, "brier": 0.2})
            result = compare(old, new, "test")
        row = result["comparison"][0]
        self.assertFalse(row["same_test_row_count"])
        self.assertIsNone(row["metrics"]["log_loss"]["delta"])

    def test_delta_is_reported_when_row_counts_match_but_identity_caveat_remains(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            old, new = root / "old.csv", root / "new.csv"
            fields = ["model", "test_season", "n_test", "log_loss"]
            for path, log_loss in ((old, 0.60), (new, 0.55)):
                with path.open("w", newline="") as f:
                    writer = csv.DictWriter(f, fieldnames=fields)
                    writer.writeheader()
                    writer.writerow({"model": "lightgbm", "test_season": "2627",
                                     "n_test": 100, "log_loss": log_loss})
            result = compare(old, new, "test")
        row = result["comparison"][0]
        self.assertTrue(row["same_test_row_count"])
        self.assertFalse(row["test_sample_identity_verified"])
        self.assertAlmostEqual(row["metrics"]["log_loss"]["delta"], -0.05)


if __name__ == "__main__":
    unittest.main()
