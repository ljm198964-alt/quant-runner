import json
import tempfile
import unittest
from pathlib import Path

from research.m3.openfootball_shadow_performance import build_report
from research.m3.test_openfootball_shadow_audit import forecast


class OpenFootballShadowPerformanceTests(unittest.TestCase):
    def _write_ledger(self, events):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        path = Path(temp.name) / "ledger.jsonl"
        path.write_text("".join(json.dumps(e, sort_keys=True) + "\n" for e in events), encoding="utf-8")
        return path

    def test_empty_forward_ledger_has_no_estimable_performance(self):
        report = build_report(self._write_ledger([]))
        self.assertEqual(report["status"], "NO_SETTLED_FORWARD_SAMPLES")
        self.assertEqual(report["settled_forward_forecast_count"], 0)
        self.assertIsNone(report["financial_metrics"]["ROI"])
        self.assertEqual(report["metrics_by_model"]["poisson"]["n"], 0)
        self.assertEqual(report["metrics_by_model"]["poisson"]["ah0_dnb_3way_brier"], None)

    def test_computes_forward_scores_by_model_period_and_paired_fixture(self):
        events = []
        models = ("poisson", "dixon_coles", "bivariate_poisson")
        probs = {
            "poisson": (0.6, 0.2, 0.2, 0.65),
            "dixon_coles": (0.5, 0.3, 0.2, 0.60),
            "bivariate_poisson": (0.55, 0.25, 0.2, 0.62),
        }
        for i, (fixture_date, score) in enumerate((("2026-10-23", (2, 1)),
                                                    ("2026-10-24", (1, 1)))):
            for model in models:
                h, d, a, ou = probs[model]
                event = forecast(f"f{i}-{model}", "2026-10-20T11:00:00Z")
                event.update({"fixture_identity_id": f"fixture-{i}",
                    "schedule_revision_id": f"schedule-{i}", "model": model,
                    "league": "D1", "season": "2627",
                    "source_fixture_date": fixture_date,
                    "p_home": h, "p_draw": d, "p_away": a,
                    "ah_home_0_p_win": h, "ah_home_0_p_push": d, "ah_home_0_p_lose": a,
                    "ou_p_over_2_5": ou})
                events.append(event)
                result = "H" if score[0] > score[1] else "A" if score[0] < score[1] else "D"
                events.append({"event_type": "SETTLEMENT", "settlement_id": f"s{i}-{model}",
                    "forecast_id": event["forecast_id"], "actual_home_goals": score[0],
                    "actual_away_goals": score[1], "actual_result_1x2": result,
                    "actual_ou_over_2_5": int(sum(score) > 2.5),
                    "settled_at_utc": "2026-10-25T10:00:00Z"})
        report = build_report(self._write_ledger(events))
        self.assertEqual(report["status"], "OK")
        self.assertEqual(report["settled_forward_forecast_count"], 6)
        self.assertEqual(report["unique_settled_fixture_count"], 2)
        self.assertEqual(report["metrics_by_model"]["poisson"]["n"], 2)
        self.assertEqual(report["same_sample_model_comparison"]["poisson_minus_dixon_coles"]
                         ["paired_fixture_count"], 2)
        self.assertEqual(report["metrics_by_period_and_league"]["source_fixture_week"]["2026-W43"]
                         ["poisson"]["n"], 2)
        self.assertEqual(report["financial_metrics"]["Crown_quotes_used"], 0)
        self.assertIsNone(report["financial_metrics"]["ROI"])

    def test_rejects_duplicate_settlement_events_for_one_forecast(self):
        event = forecast("f1", "2026-10-20T11:00:00Z")
        settlement = {"event_type": "SETTLEMENT", "settlement_id": "s1",
                      "forecast_id": "f1", "actual_home_goals": 2, "actual_away_goals": 1,
                      "actual_result_1x2": "H", "actual_ou_over_2_5": 1,
                      "settled_at_utc": "2026-10-25T10:00:00Z"}
        with self.assertRaisesRegex(ValueError, "exactly one settlement event"):
            build_report(self._write_ledger([event, settlement,
                {**settlement, "settlement_id": "s2"}]))

    def test_rejects_settlement_observed_before_forecast(self):
        event = forecast("f1", "2026-10-20T11:00:00Z")
        settlement = {"event_type": "SETTLEMENT", "settlement_id": "s1",
                      "forecast_id": "f1", "actual_home_goals": 2, "actual_away_goals": 1,
                      "actual_result_1x2": "H", "actual_ou_over_2_5": 1,
                      "settled_at_utc": "2026-10-20T10:00:00Z"}
        with self.assertRaisesRegex(ValueError, "after the forecast"):
            build_report(self._write_ledger([event, settlement]))

    def test_preserves_generated_timestamp_when_inputs_are_unchanged(self):
        path = self._write_ledger([])
        first = build_report(path)
        with tempfile.TemporaryDirectory() as temp:
            previous = Path(temp) / "previous.json"
            previous.write_text(json.dumps(first), encoding="utf-8")
            second = build_report(path, previous)
        self.assertEqual(second["generated_utc"], first["generated_utc"])
        self.assertEqual(second["input_fingerprint_sha256"], first["input_fingerprint_sha256"])


if __name__ == "__main__":
    unittest.main()
