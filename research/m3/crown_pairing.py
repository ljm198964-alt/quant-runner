"""Value-suppressing, M3-only audit of authorized Crown evidence against forecasts.

This module never fetches data or reads other systems' ledgers. Evidence must
first pass crown_evidence.validate_record. It reports eligible counts only.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path

from research.m3.crown_evidence import validate_record


def _utc(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None or parsed.utcoffset().total_seconds() != 0:
        raise ValueError("timestamps must have explicit UTC offsets")
    return parsed.astimezone(timezone.utc)


def audit_records(records: list[dict]) -> dict:
    """Validate and pair import records; return no fixture IDs, prices, or lines."""
    counts = {"AH": 0, "OU": 0}
    hindcast_candidates = {"AH": 0, "OU": 0}
    forecast_protocols: dict[str, int] = {}
    for record in records:
        summary = validate_record(record)
        forecast = record["forecast"]
        forecast_protocols[summary["forecast_protocol"]] = forecast_protocols.get(summary["forecast_protocol"], 0) + 1
        kickoff = _utc(record["fixture"]["kickoff_at_utc"])
        predicted = forecast.get("predicted_at_utc")
        for quote in record["quotes"]:
            observed = _utc(quote["observed_at_utc"])
            if not (observed < kickoff and observed <= _utc(record["source"]["received_at_utc"])):
                continue
            if summary["forecast_protocol"] != "RECORDED_FORWARD":
                hindcast_candidates[quote["market"]] += 1
                continue
            if predicted and _utc(predicted) > observed:
                continue
            counts[quote["market"]] += 1
    return {
        "protocol": "M3_CROWN_PAIRING_STATUS_V1",
        "generated_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "validated_record_count": len(records),
        "forecast_protocol_counts": forecast_protocols,
        "eligible_quote_pairs_by_market": counts,
        "retrospective_hindcast_candidates_excluded_by_market": hindcast_candidates,
        "EV_and_ROI": "not_computed_without_market_specific_model_probability_grid_and_settlement policy",
        "quote_values_persisted": False,
        "other_model_data_read": False,
        "formal_order": False,
        "telegram_sent": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("records", type=Path, help="private JSON array of authorized M3 Crown records")
    parser.add_argument("--output", type=Path, help="optional value-free status JSON")
    args = parser.parse_args()
    result = audit_records(json.loads(args.records.read_text(encoding="utf-8")))
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
