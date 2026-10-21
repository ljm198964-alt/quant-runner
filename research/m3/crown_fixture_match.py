"""Offline exact-ID M3 forecast ↔ Crown fixture matcher.

Reads only M3 shadow FORECAST events and an independently supplied, verified
TotalCorner crosswalk. Makes no bookmaker calls, writes no private odds and
never infers timezone from OpenFootball's calendar date.
"""
from __future__ import annotations
import argparse
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

def utc(value: str) -> datetime:
    if not isinstance(value, str):
        raise ValueError("explicit UTC time required")
    instant = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if instant.tzinfo is None or instant.utcoffset().total_seconds() != 0:
        raise ValueError("explicit UTC time required")
    return instant.astimezone(timezone.utc)

def match_forecasts(events: list[dict], crosswalk: list[dict]) -> dict:
    """Return value-free pairing references; fail closed on ambiguous identities."""
    by_id: dict[str, dict] = {}
    rejected = Counter()
    for row in crosswalk:
        fixture_id = str(row.get("fixture_identity_id", ""))
        source_id = str(row.get("totalcorner_match_id", ""))
        if not fixture_id or not source_id or not row.get("identity_evidence_uri"):
            rejected["missing_identity_evidence"] += 1
            continue
        if row.get("join_method") not in ("shared_provider_id", "official_fixture_crosscheck"):
            rejected["unverified_join"] += 1
            continue
        try:
            kickoff = utc(row["kickoff_at_utc"])
            observed = utc(row["kickoff_evidence_captured_at_utc"])
        except (KeyError, ValueError, AttributeError):
            rejected["invalid_utc"] += 1
            continue
        if observed >= kickoff:
            rejected["kickoff_evidence_not_prematch"] += 1
            continue
        if fixture_id in by_id:
            rejected["duplicate_fixture_identity"] += 1
            by_id[fixture_id] = {"ambiguous": True}
            continue
        by_id[fixture_id] = {"source_id": source_id, "kickoff": kickoff,
                             "captured": observed, "league": row.get("league"),
                             "season": row.get("season"),
                             "home": row.get("home_team"), "away": row.get("away_team")}
    superseded = {row.get("superseded_forecast_id") for row in events
                  if row.get("event_type") == "FORECAST_DUPLICATE_SUPERSEDED"}
    selected = []
    seen = set()
    for row in events:
        if row.get("event_type") != "FORECAST" or row.get("forecast_id") in superseded:
            continue
        key = row.get("forecast_key_id") or row.get("forecast_id")
        if key in seen:
            continue
        seen.add(key)
        f = by_id.get(str(row.get("fixture_identity_id", "")))
        if not f:
            rejected["unmapped_forecast"] += 1
            continue
        if f.get("ambiguous"):
            rejected["ambiguous_forecast"] += 1
            continue
        if any(str(row.get(k)) != str(f.get(v)) for k, v in
               (("league", "league"), ("season", "season"),
                ("home_team", "home"), ("away_team", "away"))):
            rejected["identity_mismatch"] += 1
            continue
        try:
            predicted = utc(row["forecasted_at_utc"])
        except (KeyError, ValueError, AttributeError):
            rejected["invalid_prediction_time"] += 1
            continue
        if predicted >= f["kickoff"] or predicted > f["captured"]:
            rejected["no_contemporaneous_evidence"] += 1
            continue
        selected.append({"forecast_id": row["forecast_id"],
                         "totalcorner_match_id": f["source_id"],
                         "kickoff_at_utc": f["kickoff"].isoformat().replace("+00:00", "Z"),
                         "model": row.get("model")})
    # This output is only safe for *private* work; CLI prints counts only.
    return {"matched": selected, "rejected": dict(rejected), "matched_count": len(selected)}

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ledger", type=Path, required=True)
    parser.add_argument("--verified-crosswalk", type=Path, required=True)
    args = parser.parse_args()
    events = [json.loads(x) for x in args.ledger.read_text().splitlines() if x.strip()]
    rows = json.loads(args.verified_crosswalk.read_text())
    report = match_forecasts(events, rows)
    print(json.dumps({"matched_count": report["matched_count"],
                      "rejected": report["rejected"], "api_calls": 0,
                      "telegram_sent": False}, sort_keys=True))

if __name__ == "__main__":
    main()
