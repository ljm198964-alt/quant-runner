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
        "test_matches_total": 2,
        "scored_predictions": 6,
        "train_test_isolation": "strictly earlier cutoff",
        "models": [],
    }
    predictions = root / "predictions.csv"
    report_path = root / "report.json"
    with predictions.open("w", newline="", encoding="utf-8") as stream:
        fields = ["model", "league", "season", "match_date_utc", "home_team", "away_team",
                  "actual_home_goals", "actual_away_goals", "actual_result_1x2", "prediction_status", "train_end_utc",
                  "source_match_date_calendar_key_utc", "p_home", "p_draw", "p_away",
                  "actual_ah_home_0", "ah_home_0_p_win", "ah_home_0_p_push", "ah_home_0_p_lose",
                  "actual_ou_over_2_5", "ou_p_over_2_5"]
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        for model in MODEL_NAMES:
            for season, match_date, home, result in (
                ("2526", "2025-08-01", "Home", "H"),
                ("2627", "2026-08-01", "Home2", "D"),
            ):
                home_goals, away_goals = ("1", "0") if result == "H" else ("1", "1")
                writer.writerow({"model": model, "league": "D1", "season": season,
                                 "match_date_utc": match_date + "T00:00:00+00:00",
                                 "home_team": home, "away_team": "Away", "actual_home_goals": home_goals,
                                 "actual_away_goals": away_goals, "actual_result_1x2": result,
                                 "prediction_status": "predicted",
                                 "train_end_utc": "2025-05-01T00:00:00Z",
                                 "source_match_date_calendar_key_utc": match_date + "T00:00:00Z",
                                 "p_home": "0.5", "p_draw": "0.25", "p_away": "0.25",
                                 "actual_ah_home_0": {"H": "win", "D": "push", "A": "lose"}[result],
                                 "ah_home_0_p_win": "0.5", "ah_home_0_p_push": "0.25", "ah_home_0_p_lose": "0.25",
                                 "actual_ou_over_2_5": "0", "ou_p_over_2_5": "0.5"})
    for model in MODEL_NAMES:
        report["models"].append({
            "model": model,
            "overall_metrics": {
                "ah_home_0": {"n_predicted": 2, "log_loss": 1.0397207708399179, "brier": 0.625},
                "ou_over_2_5": {"n_predicted": 2, "log_loss": 0.6931471805599453, "brier": 0.25,
                                "mean_predicted_probability": 0.5, "observed_rate": 0.0},
            },
            "by_test_season": [
                {"test_season": season, "metrics": {"D1": {
                    "ah_home_0": {"n_predicted": 1, "log_loss": 0.6931471805599453 if season == "2526" else 1.3862943611198906, "brier": 0.375 if season == "2526" else 0.875},
                    "ou_over_2_5": {"n_predicted": 1, "log_loss": 0.6931471805599453, "brier": 0.25},
                }}}
                for season in ("2526", "2627")
            ],
        })
    report_path.write_text(json.dumps(report), encoding="utf-8")
    return report_path, predictions


class OpenFootballStabilityTests(unittest.TestCase):
    def test_builds_paired_report_from_identical_oos_set(self):
        with tempfile.TemporaryDirectory() as temp:
            report_path, predictions = synthetic_inputs(Path(temp))
            result = build_stability_report(report_path, predictions)
            self.assertEqual(result["paired_scored_matches_per_model"], 2)
            self.assertEqual(result["strict_utc_cutoff_rows_verified"], 6)
            self.assertEqual(result["markets"]["AH0_DNB_3WAY"]["paired_league_season_cells"], 2)
            self.assertEqual(result["source_report_generated_utc"], "2026-01-01T00:00:00Z")
            bias = result["probability_bias"]["poisson"]
            self.assertEqual(bias["overall"]["n"], 2)
            self.assertEqual(bias["by_test_season"]["2526"]["n"], 1)
            self.assertAlmostEqual(bias["overall"]["markets"]["OU_OVER_2_5"]["predicted_minus_observed"], 0.5)
            self.assertAlmostEqual(bias["overall"]["markets"]["AH0_DNB_3WAY"]["outcomes"]["push"]["predicted_minus_observed"], -0.25)
            self.assertIsNone(result["Crown_ROI"])
            self.assertTrue(result["cluster_bootstrap"]["AH0_DNB_3WAY"]["models"]["dixon_coles"]["log_loss"]["interval_includes_zero"])
            self.assertEqual(result["cluster_bootstrap"]["AH0_DNB_3WAY"]["models"]["dixon_coles"]["log_loss"]["observed_pooled_difference_vs_poisson"], 0.0)

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

    def test_rejects_metrics_not_reproducible_from_prediction_rows(self):
        with tempfile.TemporaryDirectory() as temp:
            report_path, predictions = synthetic_inputs(Path(temp))
            report = json.loads(report_path.read_text(encoding="utf-8"))
            report["models"][0]["overall_metrics"]["ou_over_2_5"]["log_loss"] += 0.01
            report_path.write_text(json.dumps(report), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "prediction-level recomputation disagrees"):
                build_stability_report(report_path, predictions)


if __name__ == "__main__":
    unittest.main()
