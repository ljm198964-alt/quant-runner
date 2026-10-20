import copy
import json
import tempfile
import unittest
from pathlib import Path

from research.m3.crown_shadow_ledger import append_records
from research.m3.test_crown_evidence import synthetic_record


class CrownShadowLedgerTests(unittest.TestCase):
    def test_append_is_idempotent_private_and_value_suppressed(self):
        with tempfile.TemporaryDirectory() as root:
            repo = Path(root) / "repo"
            repo.mkdir()
            destination = Path(root) / "private" / "crown.jsonl"
            record = synthetic_record()
            record["authorization"]["allowed_uses"] = ["m3_research", "quote_retention", "automated_api"]
            record["forecast"]["protocol"] = "RECORDED_FORWARD"
            record["forecast"]["predicted_at_utc"] = "2026-10-01T08:30:00Z"
            summary = append_records(destination, [record], repo)
            self.assertEqual(summary["event_count"], 1)
            self.assertEqual(summary["retained_quote_count_by_market"], {"AH": 1, "OU": 1})
            self.assertEqual(destination.stat().st_mode & 0o777, 0o600)
            self.assertEqual(append_records(destination, [record], repo)["event_count"], 1)
            self.assertNotIn("Synthetic Home", str(summary))
            self.assertNotIn("1.9", str(summary))

    def test_requires_explicit_retention_scope(self):
        with tempfile.TemporaryDirectory() as root:
            repo = Path(root) / "repo"
            repo.mkdir()
            record = synthetic_record()
            with self.assertRaisesRegex(ValueError, "quote retention"):
                append_records(Path(root) / "private.jsonl", [record], repo)

    def test_refuses_repository_destination(self):
        with tempfile.TemporaryDirectory() as root:
            repo = Path(root) / "repo"
            repo.mkdir()
            record = synthetic_record()
            record["authorization"]["allowed_uses"] = ["m3_research", "quote_retention"]
            with self.assertRaisesRegex(ValueError, "outside the repository"):
                append_records(repo / "quotes.jsonl", [record], repo)

    def test_api_capture_requires_automated_scope(self):
        with tempfile.TemporaryDirectory() as root:
            repo = Path(root) / "repo"
            repo.mkdir()
            record = synthetic_record()
            record["authorization"]["allowed_uses"] = ["m3_research", "quote_retention"]
            record["forecast"]["protocol"] = "RECORDED_FORWARD"
            record["forecast"]["predicted_at_utc"] = "2026-10-01T08:00:00Z"
            with self.assertRaisesRegex(ValueError, "automated API capture"):
                append_records(Path(root) / "private.jsonl", [record], repo)


if __name__ == "__main__":
    unittest.main()
