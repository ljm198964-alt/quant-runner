"""Offline validator for independently authorized M3 Crown evidence records.

This module has no HTTP client and never reads M1/M2/MR1 files. It validates a
normalized, operator-supplied record; it does not collect data from TotalCorner.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
from datetime import datetime, timezone
from pathlib import Path


SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


def _utc(value: str, field: str) -> datetime:
    if not isinstance(value, str):
        raise ValueError(f"{field} must be an ISO-8601 UTC string")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"{field} must be an ISO-8601 UTC string") from exc
    if parsed.tzinfo is None or parsed.utcoffset() != timezone.utc.utcoffset(parsed):
        raise ValueError(f"{field} must have an explicit UTC offset of zero")
    return parsed.astimezone(timezone.utc)


def _required_text(obj: dict, key: str, prefix: str = "") -> str:
    value = obj.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{prefix}{key} must be a non-empty string")
    return value.strip()


def validate_record(record: dict) -> dict:
    """Validate provenance, exact fixture identity and pre-kickoff quote timing.

    Returns a value-free audit summary. In particular, it never returns prices,
    quote lines, team names, or raw response data.
    """
    if not isinstance(record, dict) or record.get("protocol") != "M3_CROWN_EVIDENCE_V1":
        raise ValueError("protocol must be M3_CROWN_EVIDENCE_V1")

    authorization = record.get("authorization")
    if not isinstance(authorization, dict):
        raise ValueError("authorization object is required")
    if authorization.get("basis") != "written_permission":
        raise ValueError("written permission is required before processing Crown data")
    _required_text(authorization, "reference", "authorization.")

    source = record.get("source")
    if not isinstance(source, dict):
        raise ValueError("source object is required")
    if source.get("provider") != "TotalCorner" or source.get("bookmaker_slug") != "crown":
        raise ValueError("source must be the TotalCorner Crown-labelled bookmaker")
    if source.get("endpoint") != "match/bookmaker_odds":
        raise ValueError("source endpoint must identify match/bookmaker_odds")
    if source.get("capture_method") not in {"manual_authorized_export", "authorized_api"}:
        raise ValueError("capture_method must be an authorized manual export or authorized API")
    _required_text(source, "source_match_id", "source.")
    _required_text(source, "source_timezone", "source.")
    response_hash = _required_text(source, "response_sha256", "source.")
    if not SHA256_RE.fullmatch(response_hash):
        raise ValueError("source.response_sha256 must be lowercase SHA-256 hex")
    captured_at = _utc(_required_text(source, "received_at_utc", "source."), "source.received_at_utc")

    fixture = record.get("fixture")
    if not isinstance(fixture, dict):
        raise ValueError("fixture object is required")
    for key in ("competition", "home_team", "away_team", "identity_evidence_uri"):
        _required_text(fixture, key, "fixture.")
    kickoff = _utc(_required_text(fixture, "kickoff_at_utc", "fixture."), "fixture.kickoff_at_utc")
    identity = fixture.get("m3_identity")
    if not isinstance(identity, dict):
        raise ValueError("fixture.m3_identity object is required")
    if identity.get("join_method") not in {"shared_provider_id", "official_fixture_crosscheck"}:
        raise ValueError("team mapping must use a shared provider ID or cited official fixture cross-check")
    _required_text(identity, "league", "fixture.m3_identity.")
    _required_text(identity, "season", "fixture.m3_identity.")
    _required_text(identity, "home_team", "fixture.m3_identity.")
    _required_text(identity, "away_team", "fixture.m3_identity.")
    _required_text(identity, "evidence_uri", "fixture.m3_identity.")
    if identity["home_team"].strip() != fixture["home_team"].strip():
        raise ValueError("home-team mapping must be exact; fuzzy mapping is not accepted")
    if identity["away_team"].strip() != fixture["away_team"].strip():
        raise ValueError("away-team mapping must be exact; fuzzy mapping is not accepted")

    forecast = record.get("forecast")
    if not isinstance(forecast, dict):
        raise ValueError("forecast object is required")
    if forecast.get("system") != "M3":
        raise ValueError("forecast.system must be M3; cross-system forecasts are not accepted")
    if forecast.get("protocol") not in {"RECORDED_FORWARD", "STRICT_WALK_FORWARD_HINDCAST"}:
        raise ValueError("forecast.protocol must distinguish recorded forward from hindcast")
    _required_text(forecast, "model", "forecast.")
    _required_text(forecast, "model_version", "forecast.")
    prediction_hash = _required_text(forecast, "prediction_sha256", "forecast.")
    if not SHA256_RE.fullmatch(prediction_hash):
        raise ValueError("forecast.prediction_sha256 must be lowercase SHA-256 hex")
    train_end = _utc(_required_text(forecast, "train_end_utc", "forecast."), "forecast.train_end_utc")
    predicted_at = forecast.get("predicted_at_utc")
    predicted_at_dt = None if predicted_at is None else _utc(predicted_at, "forecast.predicted_at_utc")
    if train_end >= kickoff:
        raise ValueError("forecast training data must end before kickoff")
    if forecast["protocol"] == "RECORDED_FORWARD" and predicted_at_dt is None:
        raise ValueError("recorded-forward forecasts require predicted_at_utc")

    quotes = record.get("quotes")
    if not isinstance(quotes, list) or not quotes:
        raise ValueError("quotes must be a non-empty array")
    checked = {"AH": 0, "OU": 0}
    quote_times = []
    for index, quote in enumerate(quotes):
        prefix = f"quotes[{index}]."
        if not isinstance(quote, dict):
            raise ValueError(f"{prefix[:-1]} must be an object")
        market = quote.get("market")
        if market not in checked:
            raise ValueError(f"{prefix}market must be AH or OU")
        if quote.get("status") != "open" or quote.get("in_play") is not False:
            raise ValueError(f"{prefix}quote must be an open pre-match price")
        line = quote.get("line")
        if isinstance(line, bool) or not isinstance(line, (int, float)) or not math.isfinite(line):
            raise ValueError(f"{prefix}line must be finite")
        for key in ("price1", "price2"):
            price = quote.get(key)
            if isinstance(price, bool) or not isinstance(price, (int, float)) or not math.isfinite(price) or price <= 1:
                raise ValueError(f"{prefix}{key} must be a valid decimal price greater than 1")
        observed = _utc(_required_text(quote, "observed_at_utc", prefix), prefix + "observed_at_utc")
        if observed >= kickoff:
            raise ValueError(f"{prefix}quote must be observed strictly before kickoff")
        if observed > captured_at:
            raise ValueError(f"{prefix}quote cannot postdate the source snapshot receipt")
        if train_end >= observed:
            raise ValueError(f"{prefix}quote must postdate the model training cutoff")
        if predicted_at_dt is not None and predicted_at_dt > observed:
            raise ValueError(f"{prefix}quote must not predate its recorded forecast")
        row_hash = _required_text(quote, "source_row_sha256", prefix)
        if not SHA256_RE.fullmatch(row_hash):
            raise ValueError(f"{prefix}source_row_sha256 must be lowercase SHA-256 hex")
        checked[market] += 1
        quote_times.append(observed)

    return {
        "protocol": "M3_CROWN_EVIDENCE_VALIDATION_V1",
        "status": "VALID_PREMATCH_CROWN_EVIDENCE",
        "forecast_protocol": forecast["protocol"],
        "quote_counts_by_market": checked,
        "pre_kickoff_quotes": len(quotes),
        "quote_time_min_utc": min(quote_times).isoformat().replace("+00:00", "Z"),
        "quote_time_max_utc": max(quote_times).isoformat().replace("+00:00", "Z"),
        "quote_values_persisted": False,
        "crown_ev_or_roi_computed": False,
        "formal_order": False,
        "telegram_sent": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("record", type=Path, help="operator-supplied normalized M3 evidence JSON")
    args = parser.parse_args()
    record = json.loads(args.record.read_text(encoding="utf-8"))
    print(json.dumps(validate_record(record), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
