#!/usr/bin/env python3
"""M2 market/residual forward observer V0.1. RESEARCH ONLY; not trading signals.

Inputs: saved M1 scan evidence; no network, Telegram, or sportsbook requests.
The output is a timestamped *observation*, NOT an approved wager or EV claim.
All features are as-of source timestamps; never retroactively price a fixture.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

VERSION = "M2_MARKET_RESIDUAL_OBSERVER_V0_1"
MAX_QUOTE_AGE_MIN = 45.0
MIN_LEAD_H = 8.0
MAX_LEAD_H = 24.0

def moment(s):
    return datetime.fromisoformat(str(s).replace("Z", "+00:00")).astimezone(timezone.utc)

def number(x):
    try:
        v = float(x)
        return v if v == v and abs(v) != float("inf") else None
    except (TypeError, ValueError):
        return None

def evaluate(match, market, scan_time):
    obj = match.get("asian" if market == "AH" else "goals") or {}
    if match.get("scope", {}).get("status") != "IN":
        return None, "OUT_OF_SCOPE"
    if match.get("time_bucket") != "FORMAL_DECISION_WINDOW":
        return None, "OUT_OF_TIME_WINDOW"
    if match.get("source_bookmaker") != "crown" or match.get("source_bookmaker_verified") is not True:
        return None, "NO_VERIFIED_CROWN"
    if obj.get("source_bookmaker") != "crown" or obj.get("source_bookmaker_verified") is not True:
        return None, "NO_VERIFIED_MARKET"
    side = obj.get("side")
    if side not in (("HOME", "AWAY") if market == "AH" else ("OVER", "UNDER")):
        return None, "NO_SIDE"
    line = number(obj.get("line"))
    price = number(obj.get("price"))
    price_hk = number(obj.get("price_hk"))
    if line is None or price is None or price_hk is None or price <= 1 or price_hk <= 0:
        return None, "NO_EXECUTABLE_PRICE"
    observed = obj.get("observed_at")
    if not observed:
        return None, "NO_QUOTE_TIMESTAMP"
    age = (scan_time - moment(observed)).total_seconds() / 60
    if age < -1 or age > MAX_QUOTE_AGE_MIN:
        return None, "STALE_OR_FUTURE_QUOTE"
    lead = number(match.get("lead_hours"))
    if lead is None or not (MIN_LEAD_H <= lead <= MAX_LEAD_H):
        return None, "INVALID_LEAD"
    # Parse quote history as features; do not choose historic "best" execution prices.
    path = obj.get("market_path") or []
    novig = number(obj.get("market_no_vig_probability"))
    probs = obj.get("settlement_probabilities") or {}
    m1ev = number(obj.get("ev"))
    if novig is None or not 0 < novig < 1 or m1ev is None:
        return None, "MISSING_COMPARISON_BASELINE"
    state = match.get("team_state") or {}
    proxy = match.get("distilled_teacher_concept_proxies") or {}
    fixture = str(match.get("fixture_id") or "")
    if not fixture:
        return None, "NO_FIXTURE_ID"
    # Repeat observations at later scan times are recorded separately; never
    # interpret multiple observations as multiple independent bets.
    token = "|".join((fixture, market, side, str(line), str(observed)))
    observation_id = hashlib.sha256(token.encode("utf-8")).hexdigest()
    record = {
        "observation_id": observation_id,
        "model_identity": VERSION,
        "status": "UNTRAINED_RESEARCH_OBSERVATION",
        "telegram_write": False,
        "shadow_order": False,
        "fixture_id": fixture,
        "kickoff_bj": match.get("kickoff_bj"),
        "league": match.get("league"),
        "market": market,
        "side": side,
        "line": line,
        "crown_decimal_price": price,
        "observed_at": observed,
        "quote_age_minutes": round(age, 2),
        "lead_hours": lead,
        "market_novig_probability": novig,
        "m1_ev_comparator_only": m1ev,
        "m1_probability_edge_comparator_only": number(obj.get("probability_edge")),
        "market_path_points": len(path),
        "opening_line": number(obj.get("opening_line")),
        "latest_market_line": number(obj.get("market_line")),
        "state_signal": obj.get("state_signal"),
        "home_history_n": state.get("home_history_n"),
        "away_history_n": state.get("away_history_n"),
        "features": {
            key: number(proxy.get(key))
            for key in (
                "home_form_goal_diff_5", "away_form_goal_diff_5",
                "home_form_goal_diff_10", "away_form_goal_diff_10",
                "home_form_goal_diff_20", "away_form_goal_diff_20",
                "home_shots_on_for_10", "away_shots_on_for_10",
                "home_dangerous_for_10", "away_dangerous_for_10",
                "home_possession_10", "away_possession_10",
                "league_avg_total_goals", "model_expected_total",
                "model_expected_goal_difference", "ah_market_depth_minus_model_goal_diff",
                "goal_line_minus_model_expected_total"
            )
        },
        "predicted_settlement_mass_comparator_only": {
            k: number(probs.get(k)) for k in ("FULL_WIN", "HALF_WIN", "PUSH", "HALF_LOSS", "FULL_LOSS")
        },
    }
    return record, None

def observe(payload):
    if payload.get("scan_status") != "COMPLETE":
        raise ValueError("M1 source scan is not COMPLETE")
    now = moment(payload["finished_at"])
    accepted, rejected, seen = [], {}, set()
    for m in payload.get("matches") or []:
        for market in ("AH", "OU"):
            observation, reason = evaluate(m, market, now)
            if reason:
                rejected[reason] = rejected.get(reason, 0) + 1
            elif observation["observation_id"] not in seen:
                seen.add(observation["observation_id"])
                accepted.append(observation)
    return {
        "protocol": VERSION,
        "research_only": True, "telegram_write": False,
        "orders_locked": 0, "settled": 0, "roi": None,
        "source_run_id": payload.get("run_id"),
        "source_scan_started_at": payload.get("started_at"),
        "source_scan_finished_at": payload.get("finished_at"),
        "observation_count": len(accepted), "rejection_counts": rejected,
        "observations": accepted,
        "limitations": [
            "No trained market/fundamental fusion; no ROI or predictive superiority claim",
            "Only M1-selected market side present; independent both-side Crown baseline still needed",
            "No injuries, weather or travel input; only source-available team features",
            "Observations are not shadow orders or Telegram picks",
        ],
    }

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--source", required=True)
    p.add_argument("--output", required=True)
    a = p.parse_args()
    doc = observe(json.loads(Path(a.source).read_text(encoding="utf-8")))
    out = Path(a.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"protocol": VERSION, "source_run_id": doc["source_run_id"],
                      "observation_count": doc["observation_count"],
                      "rejection_counts": doc["rejection_counts"], "orders_locked": 0,
                      "telegram_write": False}, ensure_ascii=False))

if __name__ == "__main__":
    main()
