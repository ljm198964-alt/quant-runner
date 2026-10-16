import unittest
from datetime import datetime, timedelta, timezone
from research.m2.m2_shadow import evaluate, observe

BASE = datetime(2026, 10, 15, 12, tzinfo=timezone.utc)

def match():
    return {
        "fixture_id": "123", "kickoff_bj": "2026-10-16 01:00",
        "league": "Test Premier", "scope": {"status": "IN"},
        "time_bucket": "FORMAL_DECISION_WINDOW",
        "source_bookmaker": "crown", "source_bookmaker_verified": True,
        "lead_hours": 15.0, "team_state": {"home_history_n": 30},
        "distilled_teacher_concept_proxies": {"home_form_goal_diff_5": 0.4},
        "asian": {
            "source_bookmaker": "crown", "source_bookmaker_verified": True,
            "side": "HOME", "line": -0.25, "price": 2.0, "price_hk": 1.0,
            "market_no_vig_probability": 0.5, "ev": 0.03,
            "observed_at": (BASE - timedelta(minutes=10)).isoformat(),
            "market_path": [{"line": -0.25}],
        },
    }

class M2Test(unittest.TestCase):
    def test_strict_crown_and_no_orders(self):
        m = match()
        a, reason = evaluate(m, "AH", BASE)
        self.assertIsNone(reason)
        self.assertEqual(a["status"], "UNTRAINED_RESEARCH_OBSERVATION")
        self.assertFalse(a["telegram_write"])
        self.assertFalse(a["shadow_order"])
        m["asian"]["source_bookmaker"] = "bet365"
        self.assertEqual(evaluate(m, "AH", BASE)[1], "NO_VERIFIED_MARKET")

    def test_stale_and_future_rejected(self):
        m = match()
        m["asian"]["observed_at"] = (BASE - timedelta(hours=3)).isoformat()
        self.assertEqual(evaluate(m, "AH", BASE)[1], "STALE_OR_FUTURE_QUOTE")
        m["asian"]["observed_at"] = (BASE + timedelta(minutes=3)).isoformat()
        self.assertEqual(evaluate(m, "AH", BASE)[1], "STALE_OR_FUTURE_QUOTE")

    def test_incomplete_scan_rejected(self):
        with self.assertRaises(ValueError):
            observe({"scan_status": "PARTIAL", "started_at": BASE.isoformat()})

    def test_no_leakage_or_duplicate(self):
        m = match()
        r = observe({"scan_status": "COMPLETE", "started_at": (BASE-timedelta(minutes=20)).isoformat(),
                     "finished_at": BASE.isoformat(), "matches": [m,m]})
        self.assertEqual(r["observation_count"], 1)
        self.assertEqual(r["orders_locked"], 0)
        self.assertIsNone(r["roi"])

if __name__ == "__main__":
    unittest.main()
