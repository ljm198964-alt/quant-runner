import unittest
from research.m3.probabilities import (
    _asian_result, evaluate, expected_unit_return, market_probabilities, settle_score,
)


class IndependentM3Test(unittest.TestCase):
    def test_quarter_handicap(self):
        self.assertEqual(_asian_result(0, -0.25, 1.95)[0], "HALF_LOSS")
        self.assertEqual(_asian_result(0, 0.25, 1.95)[0], "HALF_WIN")
        self.assertEqual(_asian_result(0.5, -0.75, 1.95)[0], "HALF_LOSS")
        self.assertEqual(_asian_result(0, 0, 1.95)[0], "PUSH")

    def test_AH_and_OU_independence(self):
        data = evaluate({"fixture_id": "fixture-1", "lambda_home": 1.5,
            "lambda_away": 1.2,
            "ah": {"home_line": -0.25, "home_decimal": 1.95, "away_decimal": 1.96},
            "ou": {"total_line": 2.5, "over_decimal": 1.91, "under_decimal": 1.99}})
        self.assertIn("ah", data)
        self.assertIn("ou", data)
        self.assertFalse(data["telegram_write"])
        for side in (data["ah"]["home"], data["ah"]["away"],
                     data["ou"]["over"], data["ou"]["under"]):
            self.assertAlmostEqual(sum(side["states"].values()), 1)
            self.assertLessEqual(abs(side["expected_profit_per_unit"]), 1)

    def test_invalid_inputs(self):
        with self.assertRaises(ValueError):
            market_probabilities(-1, 1, "OU_OVER", -2.5, 1.95)
        with self.assertRaises(ValueError):
            market_probabilities(1, 1, "OU_OVER", -2.3, 1.95)

    def test_score_settlement_full_and_quarter_lines(self):
        checks = [
            ("AH", -1.5, "home", "FULL_LOSS", -1.0, 1.93, 2, 2),
            ("AH", -1.5, "away", "FULL_WIN", .95, 1.95, 2, 2),
            ("OU", 3.5, "over", "FULL_WIN", 1.04, 2.04, 2, 2),
            ("OU", 3.5, "under", "FULL_LOSS", -1.0, 1.84, 2, 2),
            ("AH", -0.25, "home", "HALF_LOSS", -.5, 1.9, 1, 1),
            ("AH", -0.25, "away", "HALF_WIN", .45, 1.9, 1, 1),
            ("OU", 2.25, "over", "HALF_LOSS", -.5, 2.0, 1, 1),
            ("OU", 2.25, "under", "HALF_WIN", .5, 2.0, 1, 1),
        ]
        for market, line, side, state, profit, odds, home_goals, away_goals in checks:
            with self.subTest(market=market, line=line, side=side):
                actual_state, actual_profit = settle_score(market, line, side,
                                                           home_goals, away_goals, odds)
                self.assertEqual(actual_state, state)
                self.assertAlmostEqual(actual_profit, profit)

    def test_ev_from_full_and_half_settlement_probabilities(self):
        states = {"FULL_WIN": .2, "HALF_WIN": .1, "PUSH": .2,
                  "HALF_LOSS": .1, "FULL_LOSS": .4}
        self.assertAlmostEqual(expected_unit_return(states, 2.0), -.2)
        result = market_probabilities(1.1, .9, "OU_OVER", -2.25, 2.0)
        self.assertAlmostEqual(expected_unit_return(result["states"], 2.0),
                               result["expected_profit_per_unit"], places=12)

    def test_score_settlement_validates_scores_and_market(self):
        with self.assertRaisesRegex(ValueError, "non-negative integer"):
            settle_score("AH", 0, "home", -1, 0, 1.9)
        with self.assertRaisesRegex(ValueError, "market must"):
            settle_score("1X2", 0, "home", 1, 0, 1.9)


if __name__ == "__main__":
    unittest.main()
