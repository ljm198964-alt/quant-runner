"""Forward-only, no-market calibration report from the isolated M3 shadow ledger.

Uses only canonical M3 forecasts and their source-backed FT settlements. It
reports descriptive probability quality, not financial returns or decisions.
Fixture calendar dates are source date keys with unspecified timezone; this
module never treats them as UTC kickoff instants.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from datetime import date, datetime, timezone
import hashlib
import json
import math
from pathlib import Path

from research.m3.openfootball_shadow_audit import build_shadow_ledger_audit

MODELS = ("poisson", "dixon_coles", "bivariate_poisson")
OUTCOMES = ("H", "D", "A")
EPSILON = 1e-15


def _canonical(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()


def _sha(value: object) -> str:
    return hashlib.sha256(_canonical(value)).hexdigest()


def _code_sha() -> str:
    return hashlib.sha256(Path(__file__).read_bytes()).hexdigest()


def _read_events(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _log_loss(probs: list[float], actual: int) -> float:
    return -math.log(max(EPSILON, probs[actual]))


def _brier(probs: list[float], actual: int) -> float:
    return sum((p - int(i == actual)) ** 2 for i, p in enumerate(probs))


def _binary_log_loss(probability: float, actual: int) -> float:
    p = min(1 - EPSILON, max(EPSILON, probability))
    return -(actual * math.log(p) + (1 - actual) * math.log(1 - p))


def _accumulate(rows: list[dict]) -> dict:
    if not rows:
        return {"n": 0, "ah0_dnb_3way_log_loss": None, "ah0_dnb_3way_brier": None,
                "ou_o2_5_log_loss": None, "ou_o2_5_brier": None}
    ah_ll, ah_br, ou_ll, ou_br = [], [], [], []
    for row in rows:
        probs = row["p_1x2"]
        actual = OUTCOMES.index(row["actual_result"])
        ah_ll.append(_log_loss(probs, actual))
        ah_br.append(_brier(probs, actual))
        ou_ll.append(_binary_log_loss(row["p_over_2_5"], row["actual_over_2_5"]))
        ou_br.append((row["p_over_2_5"] - row["actual_over_2_5"]) ** 2)
    n = len(rows)
    return {"n": n,
            "ah0_dnb_3way_log_loss": sum(ah_ll) / n,
            "ah0_dnb_3way_brier": sum(ah_br) / n,
            "ou_o2_5_log_loss": sum(ou_ll) / n,
            "ou_o2_5_brier": sum(ou_br) / n}


def _calibration(rows: list[dict]) -> dict:
    output = {"AH0_DNB_3WAY": {}, "OU_O2_5": {}}
    for outcome_index, outcome in enumerate(OUTCOMES):
        bins = [[] for _ in range(10)]
        for row in rows:
            p = row["p_1x2"][outcome_index]
            index = min(9, int(p * 10))
            bins[index].append((p, float(row["actual_result"] == outcome)))
        output["AH0_DNB_3WAY"][outcome] = [
            {"bin_lower": i / 10, "bin_upper": (i + 1) / 10, "n": len(values),
             "mean_predicted": sum(x[0] for x in values) / len(values) if values else None,
             "observed_rate": sum(x[1] for x in values) / len(values) if values else None}
            for i, values in enumerate(bins)]
    bins = [[] for _ in range(10)]
    for row in rows:
        p = row["p_over_2_5"]
        bins[min(9, int(p * 10))].append((p, float(row["actual_over_2_5"])))
    output["OU_O2_5"] = [
        {"bin_lower": i / 10, "bin_upper": (i + 1) / 10, "n": len(values),
         "mean_predicted": sum(x[0] for x in values) / len(values) if values else None,
         "observed_rate": sum(x[1] for x in values) / len(values) if values else None}
        for i, values in enumerate(bins)]
    return output


def _weekly_key(value: date) -> str:
    year, week, _ = value.isocalendar()
    return f"{year}-W{week:02d}"


def build_report(ledger_path: Path, previous_report_path: Path | None = None) -> dict:
    audit = build_shadow_ledger_audit(ledger_path)
    events = _read_events(ledger_path)
    forecasts = {e["forecast_id"]: e for e in events if e.get("event_type") == "FORECAST"}
    superseded = {e.get("superseded_forecast_id") for e in events
                  if e.get("event_type") == "FORECAST_DUPLICATE_SUPERSEDED"}
    settlements_by_forecast = defaultdict(list)
    for event in events:
        if event.get("event_type") == "SETTLEMENT":
            settlements_by_forecast[event.get("forecast_id")].append(event)
    duplicated_settlements = {k: v for k, v in settlements_by_forecast.items() if len(v) != 1}
    if duplicated_settlements:
        raise ValueError("a canonical forecast must have exactly one settlement event")

    rows_by_model = {model: [] for model in MODELS}
    fixtures: dict[tuple[str, str], dict] = {}
    for forecast_id, settlement_rows in settlements_by_forecast.items():
        forecast = forecasts.get(forecast_id)
        if forecast is None or forecast_id in superseded:
            raise ValueError("settlement references a missing or superseded forecast")
        if forecast.get("forecast_status") != "PREDICTED_NO_MARKET":
            continue
        result = settlement_rows[0]
        try:
            fixture_date = date.fromisoformat(forecast["source_fixture_date"])
            actual_result = result["actual_result_1x2"]
            hg, ag = int(result["actual_home_goals"]), int(result["actual_away_goals"])
            forecasted_at = datetime.fromisoformat(forecast["forecasted_at_utc"].replace("Z", "+00:00"))
            settled_at = datetime.fromisoformat(result["settled_at_utc"].replace("Z", "+00:00"))
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError("forecast/settlement is missing valid date or result fields") from exc
        for timestamp, label in ((forecasted_at, "forecasted_at_utc"), (settled_at, "settled_at_utc")):
            if timestamp.tzinfo is None or timestamp.utcoffset().total_seconds() != 0:
                raise ValueError(f"{label} must be explicit UTC")
        if settled_at <= forecasted_at or settled_at.date() < fixture_date:
            raise ValueError("settlement must be observed after the forecast and fixture calendar date")
        if actual_result not in OUTCOMES or hg < 0 or ag < 0:
            raise ValueError("invalid settled match result")
        derived_result = "H" if hg > ag else "A" if hg < ag else "D"
        if actual_result != derived_result or result.get("actual_ou_over_2_5") != int(hg + ag > 2.5):
            raise ValueError("stored settlement does not agree with the full-time score")
        model = forecast.get("model")
        if model not in MODELS:
            continue
        row = {"forecast_id": forecast_id,
               "fixture_identity_id": forecast["fixture_identity_id"],
               "schedule_revision_id": forecast["schedule_revision_id"],
               "league": forecast["league"], "season": forecast["season"],
               "fixture_date": fixture_date, "actual_result": actual_result,
               "p_1x2": [forecast["p_home"], forecast["p_draw"], forecast["p_away"]],
               "p_over_2_5": forecast["ou_p_over_2_5"],
               "actual_over_2_5": int(hg + ag > 2.5)}
        rows_by_model[model].append(row)
        key = (row["fixture_identity_id"], row["schedule_revision_id"])
        fixture_state = fixtures.setdefault(key, {"actual_result": actual_result,
            "actual_over_2_5": row["actual_over_2_5"], "models": {}})
        if (fixture_state["actual_result"] != actual_result
                or fixture_state["actual_over_2_5"] != row["actual_over_2_5"]):
            raise ValueError("paired model forecasts disagree on settled outcome")
        fixture_state["models"][model] = row

    by_model = {}
    time_groups = {"source_fixture_month": {}, "source_fixture_week": {},
                   "league_season": {}}
    all_rows = []
    for model in MODELS:
        rows = sorted(rows_by_model[model], key=lambda x: (x["fixture_date"], x["fixture_identity_id"]))
        all_rows.extend(rows)
        by_model[model] = _accumulate(rows)
        by_model[model]["calibration_deciles"] = _calibration(rows)
        by_model[model]["source_date_semantics"] = "calendar_date_only_timezone_unspecified_not_kickoff_utc"
        for row in rows:
            month = row["fixture_date"].strftime("%Y-%m")
            week = _weekly_key(row["fixture_date"])
            league_season = f"{row['league']}:{row['season']}"
            for group_name, group_key in (("source_fixture_month", month),
                                          ("source_fixture_week", week),
                                          ("league_season", league_season)):
                time_groups[group_name].setdefault(group_key, {}).setdefault(model, []).append(row)
    grouped = {dimension: {key: {model: _accumulate(by_model_rows.get(model, []))
                                          for model in MODELS}
                            for key, by_model_rows in sorted(groups.items())}
               for dimension, groups in time_groups.items()}

    pairwise = {}
    model_pairs = ((MODELS[0], MODELS[1]), (MODELS[0], MODELS[2]), (MODELS[1], MODELS[2]))
    for left, right in model_pairs:
        ah_deltas, ou_deltas = [], []
        for fixture in fixtures.values():
            pair = fixture["models"]
            if left not in pair or right not in pair:
                continue
            actual = OUTCOMES.index(fixture["actual_result"])
            a, b = pair[left], pair[right]
            ah_deltas.append(_brier(a["p_1x2"], actual) - _brier(b["p_1x2"], actual))
            ou_deltas.append((a["p_over_2_5"] - fixture["actual_over_2_5"]) ** 2
                             - (b["p_over_2_5"] - fixture["actual_over_2_5"]) ** 2)
        pairwise[f"{left}_minus_{right}"] = {
            "paired_fixture_count": len(ah_deltas),
            "ah0_dnb_3way_mean_brier_delta": sum(ah_deltas) / len(ah_deltas) if ah_deltas else None,
            "ou_o2_5_mean_brier_delta": sum(ou_deltas) / len(ou_deltas) if ou_deltas else None,
            "inference": "descriptive_paired_difference_no_significance_or_selection",
        }

    code_digest = _code_sha()
    input_fingerprint = _sha(["M3_OPENFOOTBALL_SHADOW_PERFORMANCE_V1",
                              audit["ledger_sha256"], code_digest])
    previous_generated = None
    if previous_report_path and previous_report_path.is_file():
        previous = json.loads(previous_report_path.read_text(encoding="utf-8"))
        if previous.get("input_fingerprint_sha256") == input_fingerprint:
            previous_generated = previous.get("generated_utc")
    generated = previous_generated or datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    return {
        "protocol": "M3_OPENFOOTBALL_SHADOW_PERFORMANCE_V1",
        "generated_utc": generated,
        "input_fingerprint_sha256": input_fingerprint,
        "shadow_ledger_sha256": audit["ledger_sha256"],
        "analysis_code_sha256": code_digest,
        "canonical_forecast_count": audit["canonical_forecast_count"],
        "settled_forward_forecast_count": len(all_rows),
        "unique_settled_fixture_count": len(fixtures),
        "status": "OK" if all_rows else "NO_SETTLED_FORWARD_SAMPLES",
        "source_date_semantics": "fixture calendar date only; source timezone unspecified; not kickoff UTC",
        "financial_metrics": {"Crown_quotes_used": 0, "EV": None, "ROI": None,
                              "cumulative_profit": None, "maximum_drawdown": None},
        "metrics_by_model": by_model,
        "metrics_by_period_and_league": grouped,
        "same_sample_model_comparison": pairwise,
        "significance_testing": False,
        "model_selection_or_parameter_tuning": False,
        "formal_order": False,
        "telegram_sent": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ledger", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--previous", type=Path)
    args = parser.parse_args()
    report = build_report(args.ledger, args.previous)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({k: report[k] for k in ("protocol", "status", "canonical_forecast_count",
          "settled_forward_forecast_count", "unique_settled_fixture_count", "financial_metrics",
          "input_fingerprint_sha256")}, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
