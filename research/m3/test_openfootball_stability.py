import csv
import json
import tempfile
import unittest
from pathlib import Path

from research.m3.openfootball_stability import MODEL_NAMES, build_stability_report


def synthetic_inputs(root: Path):
    report = {
        "protocol": "M3_OPENFOOTBALL_STRICT_WALKFORWARD_V1",
        "data_source": "synthetic-test-only",
        "data_source_commit": "synthetic",
        "generated_utc": "2026-01-01T00:00:00Z",
        "input_fingerprint_sha256": "a" * 64,
        "evaluation_fingerprint_sha256": "b" * 64,
        "test_matches_total": 1,
        "scored_predictions": 3,
        "train_test_isolation": "strictly earlier cutoff",
        "models": [],
    }
    predictions = root / "predictions.csv"
    report_path = root / "report.json"
    with predictions.open("w", newline="", encoding="utf-8") as stream:
        fields = ["model", "league", "season", "match_date_utc", "home_team", "away_team",
                  "actual_home_goals", "actual_away_goals", "prediction_status", "train_end_utc",
                  "source_match_date_calendar_key_utc", "p_home", "p_draw", "p_away",
                  "actual_ou_over_2_5", "ou_p_over_2_5"]
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        for model in MODEL_NAMES:
            writer.writerow({"model": model, "league": "D1", "season": "2526",
                             "match_date_utc": "2025-08-01T00:00:00+00:00",
                             "home_team": "Home", "away_team": "Away", "actual_home_goals": "1",
                             "actual_away_goals": "0", "prediction_status": "predicted",
                             "train_end_utc": "2025-05-01T00:00:00+00:00",
                             "source_match_date_calendar_key_utc": "2025-08-01T00:00:00Z",
                             "p_home": "0.5", "p_draw": "0.25", "p_away": "0.25",
                             "actual_ou_over_2_5": "0", "ou_p_over_2_5": "0.5"})
    for model in MODEL_NAMES:
        report["models"].append({
            "model": model,
            "overall_metrics": {
                "ah_home_0": {"n_predicted": 1, "log_loss": 1.0, "brier": 0.6},
                "ou_over_2_5": {"n_predicted": 1, "log_loss": 0.69, "brier": 0.25,
                                "mean_predicted_probability": 0.5, "observed_rate": 0.0},
            },
            "by_test_season": [{"test_season": "2526", "metrics": {"D1": {
                "ah_home_0": {"n_predicted": 1, "log_loss": 1.0, "brier": 0.6},
                "ou_over_2_5": {"n_predicted": 1, "log_loss": 0.69, "brier": 0.25},
            }}}],
        })
    report_path.write_text(json.dumps(report), encoding="utf-8")
    return report_path, predictions


class OpenFootballStabilityTests(unittest.TestCase):
    def test_builds_paired_report_from_identical_oos_set(self):
        with tempfile.TemporaryDirectory() as temp:
            report_path, predictions = synthetic_inputs(Path(temp))
            result = build_stability_report(report_path, predictions)
            self.assertEqual(result["paired_scored_matches_per_model"], 1)
            self.assertEqual(result["strict_utc_cutoff_rows_verified"], 3)
            self.assertEqual(result["markets"]["AH0_DNB_3WAY"]["paired_league_season_cells"], 1)
            self.assertIsNone(result["Crown_ROI"])

    def test_rejects_future_training_cutoff(self):
        with tempfile.TemporaryDirectory() as temp:
            report_path, predictions = synthetic_inputs(Path(temp))
            with predictions.open(newline="", encoding="utf-8") as stream:
                rows = list(csv.DictReader(stream))
            for row in rows:
                row["train_end_utc"] = "2025-08-02T00:00:00Z"
            with predictions.open("w", newline="", encoding="utf-8") as stream:
                writer = csv.DictWriter(stream, fieldnames=rows[0].keys())
                writer.writeheader(); writer.writerows(rows)
            with self.assertRaisesRegex(ValueError, "future-data leakage"):
                build_stability_report(report_path, predictions)

    def test_rejects_nonidentical_model_sample_sets(self):
        with tempfile.TemporaryDirectory() as temp:
            report_path, predictions = synthetic_inputs(Path(temp))
            with predictions.open(newline="", encoding="utf-8") as stream:
                rows = list(csv.DictReader(stream))
            rows[-1]["home_team"] = "Different Identity"
            with predictions.open("w", newline="", encoding="utf-8") as stream:
                writer = csv.DictWriter(stream, fieldnames=rows[0].keys())
                writer.writeheader(); writer.writerows(rows)
            with self.assertRaisesRegex(ValueError, "identical scored match set"):
                build_stability_report(report_path, predictions)


if __name__ == "__main__":
    unittest.main()
