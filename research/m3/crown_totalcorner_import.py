"""Offline import/validation adapter for an authorized TotalCorner Crown export.

No HTTP client is included. The caller must provide an already captured raw
response and evidence of written authorization. CLI output is value-free.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from research.m3.crown_evidence import validate_record


def _require_written_authorization(context: dict) -> dict:
    authorization = context.get("authorization")
    if not isinstance(authorization, dict) or authorization.get("basis") != "written_permission":
        raise ValueError("written authorization is required before reading or normalizing Crown evidence")
    if not isinstance(authorization.get("reference"), str) or not authorization["reference"].strip():
        raise ValueError("authorization.reference must identify written permission")
    return authorization


def _local_wall_time_to_utc(value: str, timezone_name: str, field: str) -> datetime:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a local ISO datetime string")
    try:
        local = datetime.fromisoformat(value.strip())
    except ValueError as exc:
        raise ValueError(f"{field} must be a local ISO datetime string") from exc
    if local.tzinfo is not None:
        raise ValueError(f"{field} must be a naive source-local datetime; use source_timezone")
    try:
        zone = ZoneInfo(timezone_name)
    except (ZoneInfoNotFoundError, TypeError) as exc:
        raise ValueError("source_timezone must be a valid IANA timezone") from exc

    valid_instants = set()
    for fold in (0, 1):
        candidate = local.replace(tzinfo=zone, fold=fold)
        roundtrip = candidate.astimezone(timezone.utc).astimezone(zone).replace(tzinfo=None)
        if roundtrip == local:
            valid_instants.add(candidate.astimezone(timezone.utc))
    if not valid_instants:
        raise ValueError(f"{field} is a nonexistent wall time in {timezone_name}")
    if len(valid_instants) != 1:
        raise ValueError(f"{field} is ambiguous in {timezone_name}; refusing to guess DST fold")
    return next(iter(valid_instants))


def _sha256_json(value) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def _finite_float(value, field: str) -> float:
    if isinstance(value, bool):
        raise ValueError(f"{field} must be numeric")
    try:
        result = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{field} must be numeric") from exc
    if not math.isfinite(result):
        raise ValueError(f"{field} must be finite")
    return result


def _movement_quotes(match: dict, field: str, market: str, kickoff_utc: datetime,
                     source_timezone: str) -> list[dict]:
    rows = match.get(field, [])
    if rows is None:
        return []
    if not isinstance(rows, list):
        raise ValueError(f"data.{field} must be an array")
    quotes = []
    for index, row in enumerate(rows):
        if not isinstance(row, list) or len(row) != 8:
            raise ValueError(f"data.{field}[{index}] must use the documented 8-field movement shape")
        minute, line_raw, price1_raw, price2_raw, observed_raw, _hg, _ag, closed_raw = row
        if minute is not None:
            continue
        if closed_raw not in (0, "0", False):
            if closed_raw in (1, "1", True):
                continue
            raise ValueError(f"data.{field}[{index}].closed must be 0 or 1")
        observed = _local_wall_time_to_utc(observed_raw, source_timezone,
                                           f"data.{field}[{index}].time")
        if observed >= kickoff_utc:
            continue
        line = _finite_float(line_raw, f"data.{field}[{index}].line")
        price1 = _finite_float(price1_raw, f"data.{field}[{index}].price1")
        price2 = _finite_float(price2_raw, f"data.{field}[{index}].price2")
        row_hash = _sha256_json(row)
        quotes.append({
            "market": market,
            "status": "open",
            "in_play": False,
            "line": line,
            "price1": price1,
            "price2": price2,
            "observed_at_utc": observed.isoformat().replace("+00:00", "Z"),
            "source_row_sha256": row_hash,
        })
    return quotes


def normalize_totalcorner_payload(payload: dict, context: dict, raw_response: bytes) -> dict:
    """Normalize one API response into the existing private Crown evidence schema.

    Team identity, official kickoff, forecast data, timezone and authorization
    must be supplied in ``context``. Team joins are exact; no aliases are guessed.
    """
    if not isinstance(payload, dict) or payload.get("success") != 1:
        raise ValueError("TotalCorner response must have success=1")
    if not isinstance(context, dict):
        raise ValueError("context must be a JSON object")
    authorization = _require_written_authorization(context)
    if not isinstance(raw_response, bytes) or not raw_response:
        raise ValueError("raw_response must contain the captured response bytes")
    try:
        decoded_payload = json.loads(raw_response.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("raw_response must be UTF-8 JSON") from exc
    if decoded_payload != payload:
        raise ValueError("parsed payload must match the captured raw_response bytes")
    capture = context.get("capture")
    source_fixture = context.get("source_fixture")
    if not isinstance(capture, dict) or not isinstance(source_fixture, dict):
        raise ValueError("capture and source_fixture context objects are required")
    source_timezone = capture.get("source_timezone")
    timezone_evidence_uri = capture.get("timezone_evidence_uri")
    if not isinstance(timezone_evidence_uri, str) or not timezone_evidence_uri.strip():
        raise ValueError("capture.timezone_evidence_uri is required to substantiate the profile timezone")
    expected_id = str(capture.get("source_match_id", "")).strip()
    if not expected_id:
        raise ValueError("capture.source_match_id is required")
    data = payload.get("data")
    if not isinstance(data, list):
        raise ValueError("TotalCorner response data must be an array")
    matches = [row for row in data if isinstance(row, dict) and str(row.get("id", "")) == expected_id]
    if len(matches) != 1:
        raise ValueError("response must contain exactly one match with the authorized source_match_id")
    match = matches[0]
    if str(match.get("h", "")).strip() != source_fixture.get("home_team"):
        raise ValueError("source home-team name mismatch; exact provider identity is required")
    if str(match.get("a", "")).strip() != source_fixture.get("away_team"):
        raise ValueError("source away-team name mismatch; exact provider identity is required")
    kickoff_from_source = _local_wall_time_to_utc(match.get("start"), source_timezone, "data.start")
    fixture = context.get("fixture")
    if not isinstance(fixture, dict) or not isinstance(fixture.get("kickoff_at_utc"), str):
        raise ValueError("context.fixture.kickoff_at_utc is required")
    try:
        official_kickoff = datetime.fromisoformat(fixture["kickoff_at_utc"].replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("context.fixture.kickoff_at_utc must be ISO-8601 UTC") from exc
    if official_kickoff.tzinfo is None or official_kickoff.utcoffset() != timezone.utc.utcoffset(official_kickoff):
        raise ValueError("context.fixture.kickoff_at_utc must have UTC offset zero")
    official_kickoff = official_kickoff.astimezone(timezone.utc)
    if kickoff_from_source != official_kickoff:
        raise ValueError("source kickoff does not exactly match the independently verified UTC kickoff")

    bookmakers = match.get("bookmakers")
    if not isinstance(bookmakers, list):
        raise ValueError("data.bookmakers must be an array")
    crown_rows = [book for book in bookmakers if isinstance(book, dict) and book.get("slug") == "crown"]
    if len(crown_rows) != 1:
        raise ValueError("response must contain exactly one Crown bookmaker entry")
    crown = crown_rows[0]
    if not isinstance(crown.get("asian_list", []), list) or not isinstance(crown.get("goal_list", []), list):
        raise ValueError("Crown movement arrays must be present as documented lists")
    quotes = _movement_quotes(match=crown, field="asian_list", market="AH",
                              kickoff_utc=official_kickoff, source_timezone=source_timezone)
    quotes += _movement_quotes(match=crown, field="goal_list", market="OU",
                               kickoff_utc=official_kickoff, source_timezone=source_timezone)
    if not quotes:
        raise ValueError("no open pre-kickoff Crown AH or OU movement rows were present")

    forecast = context.get("forecast")
    if not isinstance(forecast, dict):
        raise ValueError("forecast context object is required")
    received_at_utc = capture.get("received_at_utc")
    return {
        "protocol": "M3_CROWN_EVIDENCE_V1",
        "authorization": authorization,
        "source": {
            "provider": "TotalCorner",
            "bookmaker_slug": "crown",
            "endpoint": "match/bookmaker_odds",
            "capture_method": "authorized_api",
            "source_match_id": expected_id,
            "source_timezone": source_timezone,
            "timezone_evidence_uri": timezone_evidence_uri,
            "response_sha256": hashlib.sha256(raw_response).hexdigest(),
            "received_at_utc": received_at_utc,
        },
        "fixture": fixture,
        "forecast": forecast,
        "quotes": quotes,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--response", type=Path, required=True,
                        help="already captured authorized raw API JSON; keep private")
    parser.add_argument("--context", type=Path, required=True,
                        help="private sidecar with authorization, timezone, fixture and forecast evidence")
    args = parser.parse_args()
    context = json.loads(args.context.read_text(encoding="utf-8"))
    _require_written_authorization(context)
    raw = args.response.read_bytes()
    payload = json.loads(raw.decode("utf-8"))
    result = validate_record(normalize_totalcorner_payload(payload, context, raw))
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
