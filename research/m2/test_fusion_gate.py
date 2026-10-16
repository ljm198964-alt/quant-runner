import unittest
from research.m2.fusion_gate import diagnostics, target
def example(market="OU", h=2, a=1, line=2.5):
    return {"fixture_id":"123","market":market,"asof":"2026-10-16T00:00:00+00:00",
            "ft_home":h,"ft_away":a,"market_line":line,
            "crown_no_vig_first":0.52,
            "m1_goal_total":2.5,"m1_goal_diff":0.2,
            "form_diff_home5":0.1,"form_diff_away5":0.0,
            "form_diff_home20":0.2,"form_diff_away20":0.1}
class FusionTests(unittest.TestCase):
    def test_no_model_training_from_tiny_dataset(self):
        d=diagnostics([example()])
        self.assertEqual(d["OU"]["status"],"INSUFFICIENT_PREDECLARED_SAMPLE")
        self.assertEqual(d["OU"]["complete_fundamentals"],1)
    def test_half_payout_and_push_excluded(self):
        self.assertIsNone(target(example("OU",h=2,a=0,line=2.25)))
        self.assertIsNone(target(example("OU",h=2,a=0,line=2)))
        self.assertEqual(target(example("OU",h=3,a=1,line=2.5)),1)
    def test_AH_separate(self):
        self.assertEqual(target(example("AH",h=2,a=1,line=-0.5)),1)
        self.assertEqual(target(example("AH",h=0,a=1,line=0.25)),0)
if __name__=="__main__":
    unittest.main()
