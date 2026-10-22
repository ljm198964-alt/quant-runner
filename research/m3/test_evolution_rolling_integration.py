import unittest
from research.m3.evolution_rolling_gate import evaluate

class RollingGateTests(unittest.TestCase):
    def test_no_settlements_means_no_promotion(self):
        candidate={"model":"poisson","train_years":2,"fixture_id":"fx","source_date":"2026-10-28",
            "registered_at_utc":"2026-10-22T00:00:00+00:00",
            "score_grid":[[0.25,0.25],[0.25,0.25]]}
        result=evaluate([], [candidate])
        self.assertEqual(result["models"]["poisson"]["rolling_shadow_active"],"baseline")
        self.assertEqual(result["models"]["poisson"]["decision"],"HOLD")
    def test_invalid_previous_active_rollback(self):
        prior={"models":{"poisson":{"rolling_shadow_active":"rolling_2y"}}}
        result=evaluate([], [], prior)
        self.assertEqual(result["models"]["poisson"]["decision"],"ROLLBACK_SHADOW_ONLY")
        self.assertEqual(result["models"]["poisson"]["rolling_shadow_active"],"baseline")

if __name__=="__main__": unittest.main()
