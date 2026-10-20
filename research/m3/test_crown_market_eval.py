import unittest

from research.m3.crown_market_eval import expected_unit_return, settle_unit


class CrownMarketEvaluationTests(unittest.TestCase):
    def test_full_asian_handicap_win_loss_and_push(self):
        self.assertEqual(settle_unit("AH", -1.0, "home", 2, 0, 1.9)["outcome"], "win")
        self.assertEqual(settle_unit("AH", -1.0, "home", 1, 0, 1.9)["outcome"], "push")
        self.assertEqual(settle_unit("AH", -1.0, "home", 0, 0, 1.9)["net_units"], -1.0)

    def test_quarter_handicap_half_win_and_half_loss(self):
        half_loss = settle_unit("AH", -0.25, "home", 1, 1, 1.9)
        half_win = settle_unit("AH", -0.25, "away", 1, 1, 1.9)
        self.assertEqual(half_loss["outcome"], "half_loss")
        self.assertAlmostEqual(half_loss["net_units"], -0.5)
        self.assertEqual(half_win["outcome"], "half_win")
        self.assertAlmostEqual(half_win["net_units"], 0.45)
        self.assertEqual(settle_unit("AH", -0.25, "home", 2, 0, 1.9)["outcome"], "win")
        self.assertEqual(settle_unit("AH", -0.25, "home", 0, 2, 1.9)["outcome"], "loss")

    def test_quarter_totals_half_win_and_half_loss(self):
        over = settle_unit("OU", 2.25, "over", 1, 1, 2.0)
        under = settle_unit("OU", 2.25, "under", 1, 1, 2.0)
        self.assertEqual(over["outcome"], "half_loss")
        self.assertAlmostEqual(over["net_units"], -0.5)
        self.assertEqual(under["outcome"], "half_win")
        self.assertAlmostEqual(under["net_units"], 0.5)

    def test_decimal_ev_includes_quarter_line_outcome_weights(self):
        p = {"win": 0.2, "half_win": 0.1, "push": 0.2,
             "half_loss": 0.1, "loss": 0.4}
        self.assertAlmostEqual(expected_unit_return(2.0, p), -0.2)

    def test_rejects_invalid_market_line_and_probability_mass(self):
        with self.assertRaisesRegex(ValueError, "quarter Asian line"):
            settle_unit("AH", -0.1, "home", 2, 0, 1.9)
        with self.assertRaisesRegex(ValueError, "sum to 1"):
            expected_unit_return(2.0, {"win": 1.0, "half_win": 0.0, "push": 0.0,
                                       "half_loss": 0.0, "loss": 0.1})


if __name__ == "__main__":
    unittest.main()
