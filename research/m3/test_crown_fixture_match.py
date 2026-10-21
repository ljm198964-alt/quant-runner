import unittest

from research.m3.crown_fixture_match import match_forecasts


class M3LegacyFixtureUTCRegression(unittest.TestCase):
    def setUp(self):
        self.forecast = {
            "event_type": "FORECAST",
            "forecast_id": "f-1",
            "forecast_key_id": "key-1",
            "fixture_identity_id": "m3-fixture-1",
            "league": "E0",
            "season": "2627",
            "home_team": "Home",
            "away_team": "Away",
            "forecasted_at_utc": "2026-10-21T09:00:00Z",
            "model": "poisson",
        }
        self.fixture = {
            "fixture_identity_id": "m3-fixture-1",
            "totalcorner_match_id": "123",
            "identity_evidence_uri": "private://fixture/123",
            "join_method": "official_fixture_crosscheck",
            "league": "E0",
            "season": "2627",
            "home_team": "Home",
            "away_team": "Away",
            "kickoff_at_utc": "2026-10-23T12:00:00Z",
            "kickoff_evidence_captured_at_utc": "2026-10-21T08:00:00Z",
        }

    def test_preforecast_schedule_evidence_matches(self):
        result = match_forecasts([self.forecast], [self.fixture])
        self.assertEqual(result["matched_count"], 1)

    def test_evidence_not_known_until_after_forecast_does_not_match(self):
        self.fixture["kickoff_evidence_captured_at_utc"] = "2026-10-21T10:00:00Z"
        result = match_forecasts([self.forecast], [self.fixture])
        self.assertEqual(result["matched_count"], 0)

    def test_prediction_after_kickoff_does_not_match(self):
        self.forecast["forecasted_at_utc"] = "2026-10-24T09:00:00Z"
        result = match_forecasts([self.forecast], [self.fixture])
        self.assertEqual(result["matched_count"], 0)


if __name__ == "__main__":
    unittest.main()
