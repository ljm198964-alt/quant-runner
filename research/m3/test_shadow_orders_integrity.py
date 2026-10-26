"""Regression checks for M3 forecast/quote identity and order policy."""
import unittest
from unittest.mock import patch
from research.m3 import m3_shadow_orders as orders

class ShadowOrdersIntegrity(unittest.TestCase):
    def test_match_id_from_quote_when_forecast_has_no_match_id(self):
        forecast = {
            "protocol":"M3_TOTALCORNER_FORWARD_FORECAST_V1",
            "forecast_id":"forecast-1","run_id":"run-1","fixture_identity_id":"fixture-1",
            "home_team":"Home","away_team":"Away","kickoff_utc_verified":"2026-10-27T10:00:00+00:00",
            "model":"poisson","score_probability_grid":[[1.0]],
            "forecasted_at_utc":"2026-10-26T10:00:00+00:00"
        }
        base = {
            "protocol":"M3_TOTALCORNER_FORWARD_EV_V1","forecast_id":"forecast-1",
            "market":"AH","line":0.0,"decimal_odd":1.95,
            "expected_unit_return":0.1,"quote_snapshot_recorded_utc":"2026-10-26T10:00:00+00:00",
            "totalcorner_match_id":"12345"
        }
        quotes = [dict(base,side="home"),dict(base,side="away")]
        with patch.object(orders,"calculate",return_value=0.1):
            new,missing,count = orders.build([forecast,*quotes],run_id="run-1")
        self.assertEqual(count,1)
        self.assertEqual(len(new),1)
        self.assertEqual(new[0]["totalcorner_match_id"],"12345")
        self.assertEqual(new[0]["selection_basis"],"MODEL_ONLY_NEUTRAL_ODDS_2_NO_EV_GATE")
        self.assertEqual(missing,{"OU":1})
        with patch.object(orders,"calculate",return_value=0.1):
            repeat,_,_ = orders.build([forecast,*quotes,*new],run_id="run-1")
        self.assertEqual(repeat,[])

if __name__=="__main__":
    unittest.main()
