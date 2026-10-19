import unittest
from research.m3.probabilities import _asian_result, evaluate, market_probabilities


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


if __name__ == "__main__":
    unittest.main()
