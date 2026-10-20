import copy
import unittest

from research.m3.crown_evidence import validate_record


def synthetic_record():
    return {
        "protocol": "M3_CROWN_EVIDENCE_V1",
        "authorization": {"basis": "written_permission", "reference": "TEST-ONLY"},
        "source": {
            "provider": "TotalCorner", "bookmaker_slug": "crown",
            "endpoint": "match/bookmaker_odds", "capture_method": "authorized_api",
            "source_match_id": "SYNTHETIC-TEST-ONLY", "source_timezone": "UTC",
            "response_sha256": "a" * 64, "received_at_utc": "2026-10-01T10:00:00Z",
        },
        "fixture": {
            "competition": "Synthetic League", "home_team": "Synthetic Home",
            "away_team": "Synthetic Away", "kickoff_at_utc": "2026-10-01T12:00:00Z",
            "identity_evidence_uri": "https://example.invalid/synthetic",
            "m3_identity": {
                "join_method": "official_fixture_crosscheck", "league": "SYN",
                "season": "2627", "home_team": "Synthetic Home", "away_team": "Synthetic Away",
                "evidence_uri": "https://example.invalid/synthetic",
            },
        },
        "forecast": {
            "protocol": "STRICT_WALK_FORWARD_HINDCAST", "model": "synthetic",
            "model_version": "test-only", "prediction_sha256": "b" * 64,
            "train_end_utc": "2026-09-01T00:00:00Z", "predicted_at_utc": None,
        },
        "quotes": [
            {"market": "AH", "status": "open", "in_play": False, "line": 0,
             "price1": 1.9, "price2": 1.9, "observed_at_utc": "2026-10-01T09:00:00Z",
             "source_row_sha256": "c" * 64},
            {"market": "OU", "status": "open", "in_play": False, "line": 2.5,
             "price1": 1.9, "price2": 1.9, "observed_at_utc": "2026-10-01T09:00:00Z",
             "source_row_sha256": "d" * 64},
        ],
    }


class CrownEvidenceTests(unittest.TestCase):
    def test_valid_synthetic_hindcast_is_value_free(self):
        result = validate_record(synthetic_record())
        self.assertEqual(result["forecast_protocol"], "STRICT_WALK_FORWARD_HINDCAST")
        self.assertEqual(result["quote_counts_by_market"], {"AH": 1, "OU": 1})
        self.assertNotIn("price1", str(result))
        self.assertNotIn("line", str(result))

    def test_requires_written_authorization(self):
        record = synthetic_record()
        record["authorization"]["basis"] = "public_page"
        with self.assertRaisesRegex(ValueError, "written permission"):
            validate_record(record)

    def test_rejects_fuzzy_fixture_mapping(self):
        record = synthetic_record()
        record["fixture"]["m3_identity"]["home_team"] = "Home"
        with self.assertRaisesRegex(ValueError, "exact"):
            validate_record(record)

    def test_rejects_non_crown_bookmaker(self):
        record = synthetic_record()
        record["source"]["bookmaker_slug"] = "other"
        with self.assertRaisesRegex(ValueError, "Crown-labelled"):
            validate_record(record)

    def test_rejects_quote_after_kickoff(self):
        record = synthetic_record()
        record["quotes"][0]["observed_at_utc"] = "2026-10-01T12:00:00Z"
        with self.assertRaisesRegex(ValueError, "strictly before kickoff"):
            validate_record(record)

    def test_recorded_forecast_cannot_postdate_quote(self):
        record = synthetic_record()
        record["forecast"]["protocol"] = "RECORDED_FORWARD"
        record["forecast"]["predicted_at_utc"] = "2026-10-01T09:30:00Z"
        with self.assertRaisesRegex(ValueError, "must not predate its recorded forecast"):
            validate_record(record)

    def test_requires_both_valid_prices(self):
        record = synthetic_record()
        record["quotes"][1]["price2"] = None
        with self.assertRaisesRegex(ValueError, "price2"):
            validate_record(record)

    def test_recorded_forward_requires_prediction_time(self):
        record = synthetic_record()
        record["forecast"]["protocol"] = "RECORDED_FORWARD"
        with self.assertRaisesRegex(ValueError, "predicted_at_utc"):
            validate_record(record)


if __name__ == "__main__":
    unittest.main()
