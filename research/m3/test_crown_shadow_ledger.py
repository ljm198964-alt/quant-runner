import copy
import json
import tempfile
import unittest
from pathlib import Path

from research.m3.crown_shadow_ledger import add_line_ev, append_records
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
            record["forecast"].update({"ah_home_0_p_win": 0.5, "ah_home_0_p_push": 0.25,
                                       "ah_home_0_p_lose": 0.25, "ou_p_over_2_5": 0.6})
            summary = append_records(destination, [record], repo)
            self.assertEqual(summary["event_count"], 1)
            self.assertEqual(summary["retained_quote_count_by_market"], {"AH": 1, "OU": 1})
            self.assertEqual(destination.stat().st_mode & 0o777, 0o600)
            self.assertEqual(append_records(destination, [record], repo)["event_count"], 1)
            self.assertNotIn("Synthetic Home", str(summary))
            self.assertNotIn("1.9", str(summary))
            stored = json.loads(destination.read_text().splitlines()[0])["record"]
            self.assertAlmostEqual(stored["quotes"][0]["m3_line_probability_evaluation"]
                                   ["side_results"]["home"]["expected_unit_return"], 0.2)
            self.assertAlmostEqual(stored["quotes"][1]["m3_line_probability_evaluation"]
                                   ["side_results"]["over"]["expected_unit_return"], 0.14)

    def test_full_score_grid_supports_any_quarter_line_and_marks_coverage(self):
        record = synthetic_record()
        record["forecast"]["score_probability_grid"] = [
            {"home_goals": 0, "away_goals": 0, "probability": 0.5},
            {"home_goals": 1, "away_goals": 0, "probability": 0.3},
            {"home_goals": 0, "away_goals": 1, "probability": 0.2},
        ]
        record["quotes"][1]["line"] = 2.5
        enriched = add_line_ev(record)
        evaluation = enriched["quotes"][1]["m3_line_probability_evaluation"]
        self.assertEqual(evaluation["probability_source"], "full_score_grid")
        self.assertEqual(evaluation["score_grid_probability_coverage"], 1.0)
        self.assertAlmostEqual(evaluation["side_results"]["over"]
                               ["expected_unit_return_conditional_on_grid"], -1.0)

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

    def test_refuses_broad_existing_parent_without_chmod(self):
        with tempfile.TemporaryDirectory() as root:
            repo = Path(root) / "repo"
            repo.mkdir()
            parent = Path(root) / "private"
            parent.mkdir(mode=0o755)
            parent.chmod(0o755)
            record = synthetic_record()
            record["authorization"]["allowed_uses"] = ["m3_research", "quote_retention", "automated_api"]
            record["forecast"]["protocol"] = "RECORDED_FORWARD"
            record["forecast"]["predicted_at_utc"] = "2026-10-01T08:30:00Z"
            with self.assertRaisesRegex(ValueError, "mode 0700"):
                append_records(parent / "ledger.jsonl", [record], repo)
            self.assertEqual(parent.stat().st_mode & 0o777, 0o755)

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
