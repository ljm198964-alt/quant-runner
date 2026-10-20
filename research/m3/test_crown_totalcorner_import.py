import hashlib
import json
import unittest

from research.m3.crown_totalcorner_import import normalize_totalcorner_payload
from research.m3.crown_evidence import validate_record


def context():
    return {
        "authorization": {"basis": "written_permission", "reference": "TEST-ONLY-WRITTEN-PERMISSION"},
        "capture": {
            "source_match_id": "12345", "source_timezone": "UTC",
            "timezone_evidence_uri": "https://example.invalid/profile-timezone",
            "received_at_utc": "2026-10-01T10:00:00Z",
        },
        "source_fixture": {"home_team": "Synthetic Home", "away_team": "Synthetic Away"},
        "fixture": {
            "competition": "Synthetic League", "home_team": "Synthetic Home",
            "away_team": "Synthetic Away", "kickoff_at_utc": "2026-10-01T12:00:00Z",
            "identity_evidence_uri": "https://example.invalid/official-fixture",
            "m3_identity": {
                "join_method": "official_fixture_crosscheck", "league": "SYN", "season": "2627",
                "home_team": "Synthetic Home", "away_team": "Synthetic Away",
                "evidence_uri": "https://example.invalid/official-fixture",
            },
        },
        "forecast": {
            "system": "M3", "protocol": "STRICT_WALK_FORWARD_HINDCAST", "model": "poisson",
            "model_version": "test-only", "prediction_sha256": "b" * 64,
            "train_end_utc": "2026-09-01T00:00:00Z", "predicted_at_utc": None,
        },
    }


def response():
    return {
        "success": 1,
        "data": [{
            "id": "12345", "h": "Synthetic Home", "a": "Synthetic Away",
            "start": "2026-10-01 12:00:00",
            "bookmakers": [{
                "slug": "crown", "name": "Crown",
                "asian_list": [
                    [None, -0.25, 1.91, 1.93, "2026-10-01 09:00:00", None, None, 0],
                    [None, 0, 1.8, 2.1, "2026-10-01 12:00:00", None, None, 0],
                    ["3", -0.25, 1.7, 2.2, "2026-10-01 12:30:00", 1, 0, 0],
                    [None, -0.5, 1.9, 1.9, "2026-10-01 08:00:00", None, None, 1],
                ],
                "goal_list": [
                    [None, 2.5, 1.9, 1.95, "2026-10-01 09:01:00", None, None, 0],
                ],
            }],
        }],
    }


class CrownTotalCornerImportTests(unittest.TestCase):
    def test_normalizes_only_open_prematch_crown_rows_and_returns_value_free_audit(self):
        raw = json.dumps(response(), separators=(",", ":")).encode()
        record = normalize_totalcorner_payload(response(), context(), raw)
        result = validate_record(record)
        self.assertEqual(result["quote_counts_by_market"], {"AH": 1, "OU": 1})
        self.assertEqual(result["pre_kickoff_quotes"], 2)
        self.assertEqual(record["source"]["response_sha256"], hashlib.sha256(raw).hexdigest())
        self.assertEqual(record["quotes"][0]["observed_at_utc"], "2026-10-01T09:00:00Z")
        self.assertNotIn("price1", str(result))
        self.assertNotIn("line", str(result))

    def test_written_permission_is_required_before_normalization(self):
        ctx = context()
        ctx["authorization"]["basis"] = "vip_api_key"
        with self.assertRaisesRegex(ValueError, "written authorization"):
            normalize_totalcorner_payload(response(), ctx, json.dumps(response()).encode())

    def test_raw_bytes_must_match_parsed_payload(self):
        with self.assertRaisesRegex(ValueError, "must match the captured raw_response"):
            normalize_totalcorner_payload(response(), context(), b"{}")

    def test_rejects_nonexact_team_identity_or_kickoff(self):
        payload = response()
        payload["data"][0]["h"] = "Synthetic H."
        with self.assertRaisesRegex(ValueError, "exact provider identity"):
            normalize_totalcorner_payload(payload, context(), json.dumps(payload).encode())
        payload = response()
        ctx = context()
        ctx["fixture"]["kickoff_at_utc"] = "2026-10-01T12:01:00Z"
        with self.assertRaisesRegex(ValueError, "does not exactly match"):
            normalize_totalcorner_payload(payload, ctx, json.dumps(payload).encode())

    def test_rejects_ambiguous_dst_wall_time(self):
        ctx = context()
        ctx["capture"]["source_timezone"] = "Europe/London"
        ctx["fixture"]["kickoff_at_utc"] = "2026-10-25T02:00:00Z"
        payload = response()
        payload["data"][0]["start"] = "2026-10-25 02:00:00"
        payload["data"][0]["bookmakers"][0]["asian_list"][0][4] = "2026-10-25 01:30:00"
        with self.assertRaisesRegex(ValueError, "ambiguous"):
            normalize_totalcorner_payload(payload, ctx, json.dumps(payload).encode())

    def test_rejects_unresolved_compound_line_and_wrong_bookmaker(self):
        payload = response()
        payload["data"][0]["bookmakers"][0]["goal_list"][0][1] = "2.5,3.0"
        with self.assertRaisesRegex(ValueError, "must be numeric"):
            normalize_totalcorner_payload(payload, context(), json.dumps(payload).encode())
        payload = response()
        payload["data"][0]["bookmakers"][0]["slug"] = "pinnacle"
        with self.assertRaisesRegex(ValueError, "exactly one Crown"):
            normalize_totalcorner_payload(payload, context(), json.dumps(payload).encode())


if __name__ == "__main__":
    unittest.main()
