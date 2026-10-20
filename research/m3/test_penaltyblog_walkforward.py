import csv
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from research.m3 import penaltyblog_walkforward as wf


class FakeGrid:
    home_draw_away = [0.45, 0.30, 0.25]

    def asian_handicap_probs(self, side, line):
        assert side == "home" and line == 0.0
        return {"win": 0.45, "push": 0.30, "lose": 0.25}

    def total_goals(self, side, line):
        assert side == "over" and line == 2.5
        return 0.52


class FakeModel:
    def __init__(self, goals_home, goals_away, teams_home, teams_away):
        self.teams = sorted(set(teams_home) | set(teams_away))
        self.fit_rows = len(goals_home)

    def fit(self):
        return self

    def predict(self, home, away):
        return FakeGrid()


class PenaltyblogWalkForwardTests(unittest.TestCase):
    def test_predicts_only_after_strict_utc_date_cutoff(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with (root / "1718_E0.csv").open("w", newline="") as f:
                w = csv.writer(f)
                w.writerow(["Date", "HomeTeam", "AwayTeam", "FTHG", "FTAG", "B365H"])
                w.writerow(["11/08/2017", "A", "B", 2, 0, 1.5])
                w.writerow(["12/08/2017", "B", "A", 1, 1, 2.0])
            with (root / "1819_E0.csv").open("w", newline="") as f:
                w = csv.writer(f)
                w.writerow(["Date", "HomeTeam", "AwayTeam", "FTHG", "FTAG", "B365H"])
                w.writerow(["10/08/2018", "A", "B", 0, 1, 2.1])
            data, files = wf.read_matches(root)
            with patch.dict(wf.MODEL_TYPES, {name: FakeModel for name in wf.MODEL_TYPES}):
                predictions, splits = wf.build_predictions(data)
            split = next(s for s in splits if s["test_season"] == "1819")
            self.assertEqual(split["train_rows"], 2)
            self.assertLess(split["train_end_utc"], split["test_start_utc"])
            self.assertEqual(len(predictions), 3)
            self.assertTrue(all(p["train_rows"] == 2 for p in predictions))
            self.assertTrue(all(p["actual_result_1x2"] == "A" for p in predictions))
            self.assertTrue(all(p["prediction_status"] == "predicted" for p in predictions))
            self.assertEqual(len(files), 2)

    def test_unseen_team_is_reported_without_fabricated_forecast(self):
        data = __import__("pandas").DataFrame([
            {"season": "1718", "league": "E0", "match_date_utc": __import__("pandas").Timestamp("2017-08-11T00:00:00Z"),
             "home_team": "A", "away_team": "B", "home_goals": 1, "away_goals": 0,
             "kickoff_date_utc": "2017-08-11T00:00:00Z", "source_file": "1718_E0.csv"},
            {"season": "1819", "league": "E0", "match_date_utc": __import__("pandas").Timestamp("2018-08-10T00:00:00Z"),
             "home_team": "New", "away_team": "B", "home_goals": 0, "away_goals": 0,
             "kickoff_date_utc": "2018-08-10T00:00:00Z", "source_file": "1819_E0.csv"},
        ])
        with patch.dict(wf.MODEL_TYPES, {name: FakeModel for name in wf.MODEL_TYPES}):
            predictions, _ = wf.build_predictions(data)
        self.assertTrue(all(p["prediction_status"] == "unseen_team_in_training" for p in predictions))
        self.assertTrue(all(p["p_home"] == "" for p in predictions))

    def test_multiclass_metrics_use_actual_outcome_and_probabilities(self):
        rows = [{"model": "x", "prediction_status": "predicted", "p_home": 0.45, "p_draw": 0.30,
                 "p_away": 0.25, "actual_result_1x2": "H", "train_rows": 10}]
        result = wf.score_rows(rows, "x", "1x2")
        self.assertEqual(result["n_predicted"], 1)
        self.assertAlmostEqual(result["log_loss"], -__import__("math").log(0.45))
        self.assertAlmostEqual(result["brier"], (0.45 - 1) ** 2 + 0.30 ** 2 + 0.25 ** 2)


if __name__ == "__main__":
    unittest.main()
