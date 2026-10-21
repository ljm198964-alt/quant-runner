"""M3 isolated Crown bridge: verify recorded forecasts and imported Crown evidence.

Offline, no bookmaker HTTP, no Telegram. Raw market data stays outside repository.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from collections import Counter
from research.m3.crown_fixture_join_audit import check_pair
from research.m3.crown_totalcorner_import import normalize_totalcorner_payload
from research.m3.crown_shadow_ledger import append_records

def select_forecast(events, fixture):
    superseded = {e.get("superseded_forecast_id") for e in events if e.get("event_type") == "FORECAST_DUPLICATE_SUPERSEDED"}
    selected = [e for e in events if e.get("event_type") == "FORECAST"
                and e.get("forecast_id") not in superseded
                and e.get("forecast_status") == "PREDICTED_NO_MARKET"
                and check_pair(e, fixture)]
    unique = {}
    for event in selected:
        key = event.get("forecast_key_id") or event.get("forecast_id")
        unique.setdefault(key, event)
    return list(unique.values())

def audit_fixture_map(events, fixtures):
    counts = Counter()
    links = []
    fixture_ids = [str(f.get("fixture_identity_id", "")) for f in fixtures]
    for fixture in fixtures:
        if not fixture.get("fixture_identity_id") or fixture_ids.count(str(fixture["fixture_identity_id"])) != 1:
            counts["ambiguous_fixture"] += 1
            continue
        forecasts = select_forecast(events, fixture)
        if not forecasts:
            counts["no_verified_forecast"] += 1
        for forecast in forecasts:
            links.append((forecast, fixture))
    counts["eligible_forecast_fixture_pairs"] = len(links)
    return dict(counts), links

def import_authorized_pairs(events, entries, private_ledger, repository_root):
    """Every entry contains independent verified fixture, actual forecast, existing response.

    Calls only the established strict TotalCorner importer and private hash ledger.
    Authorization scope and timezone are validated by those existing components.
    """
    if private_ledger is None:
        raise ValueError("private ledger location required")
    fixture_map = [entry["verified_fixture"] for entry in entries]
    counts, links = audit_fixture_map(events, fixture_map)
    allowed = {(str(f["forecast_id"]), str(x["totalcorner_match_id"])): f for f, x in links}
    records = []
    for entry in entries:
        fixture = entry["verified_fixture"]
        forecast_id = str(entry["forecast_id"])
        key = (forecast_id, str(fixture["totalcorner_match_id"]))
        if key not in allowed:
            raise ValueError("unverified M3 forecast or ambiguous source fixture")
        forecast = allowed[key]
        if entry.get("source_match_id") != fixture["totalcorner_match_id"]:
            raise ValueError("source match mismatch")
        # Private sidecar carries permission, provider timezone and exact source names.
        context = dict(entry["context"])
        if str(context.get("capture", {}).get("source_match_id")) != str(fixture["totalcorner_match_id"]):
            raise ValueError("context capture identity mismatch")
        if context.get("fixture", {}).get("kickoff_at_utc") != fixture["kickoff_at_utc"]:
            raise ValueError("context UTC kickoff mismatch")
        if context.get("forecast", {}).get("system") != "M3":
            raise ValueError("M3 forecast context required")
        if context["forecast"].get("protocol") != "RECORDED_FORWARD":
            raise ValueError("recorded forward evidence required")
        if context["forecast"].get("predicted_at_utc") != forecast["forecasted_at_utc"]:
            raise ValueError("prediction time mismatch")
        raw = Path(entry["response_path"]).read_bytes()
        payload = json.loads(raw)
        records.append(normalize_totalcorner_payload(payload, context, raw))
    if not records:
        return {"bridge_counts": counts, "private_ledger": None, "crown_api_requests": 0}
    result = append_records(private_ledger, records, repository_root)
    return {"bridge_counts": counts, "private_ledger": result, "crown_api_requests": 0}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--forecast-ledger", required=True, type=Path)
    parser.add_argument("--verified-fixtures", type=Path)
    parser.add_argument("--authorized-batch", type=Path)
    parser.add_argument("--private-ledger", type=Path)
    parser.add_argument("--repository-root", type=Path)
    args = parser.parse_args()
    events = [json.loads(line) for line in args.forecast_ledger.read_text().splitlines() if line.strip()]
    if args.authorized_batch:
        if not args.repository_root or not args.private_ledger:
            parser.error("--authorized-batch requires --repository-root and --private-ledger")
        result = import_authorized_pairs(events, json.loads(args.authorized_batch.read_text()), args.private_ledger, args.repository_root)
        # No raw prices, source IDs or fixture identities in stdout.
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    else:
        if not args.verified_fixtures:
            parser.error("--verified-fixtures required for read-only audit")
        counts, _ = audit_fixture_map(events, json.loads(args.verified_fixtures.read_text()))
        print(json.dumps({"bridge_counts": counts, "crown_api_requests": 0, "telegram_sent": False}, sort_keys=True))
if __name__ == "__main__":
    main()
