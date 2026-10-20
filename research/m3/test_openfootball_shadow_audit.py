import json
import tempfile
import unittest
from pathlib import Path

from research.m3.openfootball_shadow_audit import _forecast_key, build_shadow_ledger_audit


def forecast(forecast_id: str, timestamp: str) -> dict:
    return {
        "event_type": "FORECAST", "forecast_id": forecast_id,
        "fixture_identity_id": "fixture-1", "schedule_revision_id": "schedule-1",
        "model": "poisson", "model_version_id": "model-1",
        "training_input_sha256": "a" * 64, "quant_runner_commit": "commit-1",
        "data_source": "openfootball/football.json", "data_source_commit": "source-1",
        "data_fingerprint_sha256": "b" * 64, "train_rows": 200,
        "source_fixture_date": "2026-10-23",
        "source_date_semantics": "calendar_date_only_timezone_unspecified", "date_guard_min_days": 3,
        "model_semantic_version": "penaltyblog-goal-distribution-v1",
        "penaltyblog_version": "1.13.1", "forecasted_at_utc": timestamp,
        "market_data_status": "NO_CROWN_QUOTE_CAPTURED", "crown_snapshot_id": None,
        "ev_per_unit": None, "roi": None, "formal_order": False, "telegram_sent": False,
        "forecast_status": "PREDICTED_NO_MARKET", "p_home": 0.5, "p_draw": 0.25,
        "p_away": 0.25, "ah_home_0_p_win": 0.5, "ah_home_0_p_push": 0.25,
        "ah_home_0_p_lose": 0.25, "ou_p_over_2_5": 0.52,
    }


class OpenFootballShadowAuditTests(unittest.TestCase):
    def _write(self, events):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        path = Path(temp.name) / "ledger.jsonl"
        path.write_text("".join(json.dumps(event) + "\n" for event in events), encoding="utf-8")
        return path

    def test_counts_one_canonical_record_and_reports_no_market_bounds(self):
        first = forecast("f1", "2026-10-20T11:00:00Z")
        second = forecast("f2", "2026-10-20T11:10:00Z")
        key = _forecast_key(first)
        correction = {"event_type": "FORECAST_DUPLICATE_SUPERSEDED", "supersession_id": "s1",
                      "superseded_forecast_id": "f2", "canonical_forecast_id": "f1",
                      "forecast_key_id": key, "reason": "duplicate implementation version"}
        result = build_shadow_ledger_audit(self._write([first, second, correction]))
        self.assertEqual(result["forecast_event_count"], 2)
        self.assertEqual(result["logical_forecast_key_count"], 1)
        self.assertEqual(result["canonical_forecast_count"], 1)
        self.assertEqual(result["superseded_forecast_count"], 1)
        self.assertEqual(result["settlement_event_count"], 0)
        self.assertEqual(result["crown_quote_captured_count"], 0)
        self.assertEqual(result["ev_calculable_count"], 0)
        self.assertEqual(result["canonical_forecasts_with_score_grid_count"], 0)
        self.assertTrue(result["unique_forecast_keys_one_canonical_each"])

    def test_validates_new_score_grid_matrix_without_requiring_it_for_legacy_rows(self):
        event = forecast("f1", "2026-10-20T11:00:00Z")
        event["score_probability_grid"] = [[0.5, 0.25], [0.15, 0.1]]
        event["score_probability_grid_semantics"] = (
            "penaltyblog_normalized_rows_home_goals_columns_away_goals")
        result = build_shadow_ledger_audit(self._write([event]))
        self.assertEqual(result["canonical_forecasts_with_score_grid_count"], 1)
        event["score_probability_grid"] = [[0.4, 0.2], [0.2, 0.1]]
        with self.assertRaisesRegex(ValueError, "must sum to one"):
            build_shadow_ledger_audit(self._write([event]))

    def test_rejects_duplicate_key_without_supersession(self):
        with self.assertRaisesRegex(ValueError, "canonical forecasts"):
            build_shadow_ledger_audit(self._write([
                forecast("f1", "2026-10-20T11:00:00Z"),
                forecast("f2", "2026-10-20T11:10:00Z"),
            ]))

    def test_rejects_naive_or_non_utc_timestamp(self):
        event = forecast("f1", "2026-10-20T11:00:00+01:00")
        with self.assertRaisesRegex(ValueError, "UTC offset zero"):
            build_shadow_ledger_audit(self._write([event]))

    def test_rejects_non_null_ev_without_crown_snapshot(self):
        event = forecast("f1", "2026-10-20T11:00:00Z")
        event["ev_per_unit"] = 0.1
        with self.assertRaisesRegex(ValueError, "must keep snapshot, EV, and ROI null"):
            build_shadow_ledger_audit(self._write([event]))

    def test_rejects_mismatched_stored_forecast_key(self):
        event = forecast("f1", "2026-10-20T11:00:00Z")
        event["forecast_key_id"] = "wrong-key"
        with self.assertRaisesRegex(ValueError, "does not match its provenance"):
            build_shadow_ledger_audit(self._write([event]))

    def test_rejects_forecast_inside_utc_date_guard(self):
        event = forecast("f1", "2026-10-20T23:59:59Z")
        event["source_fixture_date"] = "2026-10-22"
        with self.assertRaisesRegex(ValueError, "violates its UTC calendar-date guard"):
            build_shadow_ledger_audit(self._write([event]))

    def test_rejects_formal_order_on_any_ledger_event(self):
        event = {"event_type": "OTHER", "formal_order": True}
        with self.assertRaisesRegex(ValueError, "must not contain formal orders"):
            build_shadow_ledger_audit(self._write([event]))


if __name__ == "__main__":
    unittest.main()
