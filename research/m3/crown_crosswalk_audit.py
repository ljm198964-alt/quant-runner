"""Read-only M3 fixture crosswalk diagnostics; no betting API calls."""
from collections import Counter
from research.m3.crown_fixture_join_audit import check_pair

def audit_crosswalk(events, source_fixtures):
    sources = {}
    duplicates = set()
    for record in source_fixtures:
        key = record.get("fixture_identity_id")
        if not key:
            continue
        if key in sources:
            duplicates.add(key)
        sources[key] = record
    superseded = {e.get("superseded_forecast_id") for e in events if e.get("event_type") == "FORECAST_DUPLICATE_SUPERSEDED"}
    seen = set()
    counts = Counter()
    for event in events:
        if event.get("event_type") != "FORECAST" or event.get("forecast_id") in superseded:
            continue
        key = event.get("forecast_key_id") or event.get("forecast_id")
        if key in seen:
            continue
        seen.add(key)
        identity = event.get("fixture_identity_id")
        if identity in duplicates:
            counts["ambiguous"] += 1
        elif identity not in sources:
            counts["missing"] += 1
        elif check_pair(event, sources[identity]):
            counts["verified"] += 1
        else:
            counts["invalid"] += 1
    return dict(counts)
