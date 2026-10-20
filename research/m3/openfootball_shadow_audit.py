"""Read-only structural and provenance audit for the M3 shadow ledger.

This audits existing append-only events. It does not fetch data, fit models,
settle matches, create forecasts, or calculate Crown EV/ROI.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from collections import Counter, defaultdict
from datetime import date, datetime, timedelta, timezone
from pathlib import Path


def _sha256_json(value) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def _forecast_key(event: dict) -> str:
    derived = _sha256_json([
        "M3_SHADOW_FORECAST_KEY_V1", event["fixture_identity_id"],
        event["schedule_revision_id"], event["model"],
        event["training_input_sha256"],
        event.get("model_semantic_version", "penaltyblog-goal-distribution-v1"),
        event["penaltyblog_version"],
    ])
    if event.get("forecast_key_id") and event["forecast_key_id"] != derived:
        raise ValueError("stored forecast key does not match its provenance fields")
    return derived


def _utc(value: str, field: str) -> datetime:
    if not isinstance(value, str):
        raise ValueError(f"{field} must be an ISO-8601 UTC timestamp")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"{field} must be an ISO-8601 UTC timestamp") from exc
    if parsed.tzinfo is None or parsed.utcoffset().total_seconds() != 0:
        raise ValueError(f"{field} must have UTC offset zero")
    return parsed.astimezone(timezone.utc)


def build_shadow_ledger_audit(ledger_path: Path) -> dict:
    raw = ledger_path.read_bytes()
    events = []
    for line_no, line in enumerate(raw.decode("utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"invalid JSONL at line {line_no}") from exc
        if not isinstance(event, dict):
            raise ValueError(f"ledger event at line {line_no} must be an object")
        events.append(event)

    forecasts = [e for e in events if e.get("event_type") == "FORECAST"]
    if any(bool(e.get("formal_order")) for e in events):
        raise ValueError("M3 research ledger must not contain formal orders")
    if any(bool(e.get("telegram_sent")) for e in events):
        raise ValueError("M3 research ledger must not contain Telegram sends")
    forecast_ids = [e.get("forecast_id") for e in forecasts]
    if any(not isinstance(x, str) or not x for x in forecast_ids) or len(set(forecast_ids)) != len(forecast_ids):
        raise ValueError("forecast IDs must be present and unique")
    by_id = {e["forecast_id"]: e for e in forecasts}
    key_groups: dict[str, list[dict]] = defaultdict(list)
    for event in forecasts:
        required = ("fixture_identity_id", "schedule_revision_id", "model", "model_version_id",
                    "training_input_sha256", "penaltyblog_version", "quant_runner_commit",
                    "data_source", "data_source_commit", "data_fingerprint_sha256", "train_rows",
                    "source_fixture_date", "source_date_semantics", "date_guard_min_days",
                    "forecasted_at_utc", "market_data_status")
        if any(not event.get(k) for k in required):
            raise ValueError("forecast is missing required provenance")
        forecasted_at = _utc(event["forecasted_at_utc"], "forecasted_at_utc")
        if event["source_date_semantics"] != "calendar_date_only_timezone_unspecified":
            raise ValueError("source fixture date semantics must remain explicit")
        guard_days = event["date_guard_min_days"]
        if not isinstance(guard_days, int) or isinstance(guard_days, bool) or guard_days < 0:
            raise ValueError("date guard must be a non-negative integer")
        try:
            source_date = date.fromisoformat(event["source_fixture_date"])
        except (TypeError, ValueError) as exc:
            raise ValueError("source fixture date must be an ISO calendar date") from exc
        if source_date < forecasted_at.date() + timedelta(days=guard_days):
            raise ValueError("forecast violates its UTC calendar-date guard")
        if event.get("market_data_status") == "NO_CROWN_QUOTE_CAPTURED":
            if event.get("crown_snapshot_id") is not None or event.get("ev_per_unit") is not None or event.get("roi") is not None:
                raise ValueError("no-Crown forecast must keep snapshot, EV, and ROI null")
        if event.get("forecast_status") == "PREDICTED_NO_MARKET":
            one_x_two = [event.get(k) for k in ("p_home", "p_draw", "p_away")]
            ah = [event.get(k) for k in ("ah_home_0_p_win", "ah_home_0_p_push", "ah_home_0_p_lose")]
            ou = event.get("ou_p_over_2_5")
            if any(not isinstance(x, (int, float)) or isinstance(x, bool) or not math.isfinite(x) or not 0 <= x <= 1
                   for x in one_x_two + ah + [ou]):
                raise ValueError("predicted probability must be finite and in [0, 1]")
            if not math.isclose(sum(one_x_two), 1.0, abs_tol=1e-8) or not math.isclose(sum(ah), 1.0, abs_tol=1e-8):
                raise ValueError("forecast probability distributions must sum to one")
        key_groups[_forecast_key(event)].append(event)

    corrections = [e for e in events if e.get("event_type") == "FORECAST_DUPLICATE_SUPERSEDED"]
    correction_ids = [e.get("supersession_id") for e in corrections]
    if any(not isinstance(x, str) or not x for x in correction_ids) or len(set(correction_ids)) != len(correction_ids):
        raise ValueError("supersession IDs must be present and unique")
    superseded = [e.get("superseded_forecast_id") for e in corrections]
    if len(set(superseded)) != len(superseded):
        raise ValueError("forecast may be superseded at most once")
    superseded_set = set(superseded)
    if not superseded_set.issubset(by_id):
        raise ValueError("supersession references an unknown forecast")
    for correction in corrections:
        if not correction.get("reason"):
            raise ValueError("supersession correction must include an audit reason")
        old_id, canonical_id = correction.get("superseded_forecast_id"), correction.get("canonical_forecast_id")
        if canonical_id not in by_id or canonical_id in superseded_set:
            raise ValueError("supersession canonical forecast is missing or itself superseded")
        if _forecast_key(by_id[old_id]) != _forecast_key(by_id[canonical_id]):
            raise ValueError("superseded and canonical forecasts do not share a logical key")
        if correction.get("forecast_key_id") != _forecast_key(by_id[canonical_id]):
            raise ValueError("supersession key does not match its canonical forecast")

    for key, group in key_groups.items():
        active = [event for event in group if event["forecast_id"] not in superseded_set]
        if len(active) != 1:
            raise ValueError(f"logical forecast key {key} has {len(active)} canonical forecasts")
        if len(group) - 1 != sum(event["forecast_id"] in superseded_set for event in group):
            raise ValueError(f"logical forecast key {key} has unmarked duplicates")

    settlements = [e for e in events if e.get("event_type") == "SETTLEMENT"]
    settlement_ids = [e.get("settlement_id") for e in settlements]
    if any(not isinstance(x, str) or not x for x in settlement_ids) or len(set(settlement_ids)) != len(settlement_ids):
        raise ValueError("settlement IDs must be present and unique")
    if any(e.get("forecast_id") not in by_id or e.get("forecast_id") in superseded_set for e in settlements):
        raise ValueError("settlement must reference a canonical forecast")

    by_model = Counter(e.get("model", "unknown") for e in forecasts if e["forecast_id"] not in superseded_set)
    by_status = Counter(e.get("forecast_status", "unknown") for e in forecasts if e["forecast_id"] not in superseded_set)
    by_market = Counter(e.get("market_data_status", "unknown") for e in forecasts if e["forecast_id"] not in superseded_set)
    return {
        "protocol": "M3_OPENFOOTBALL_SHADOW_LEDGER_AUDIT_V1",
        "ledger_file": str(ledger_path),
        "ledger_sha256": hashlib.sha256(raw).hexdigest(),
        "ledger_event_count": len(events),
        "forecast_event_count": len(forecasts),
        "logical_forecast_key_count": len(key_groups),
        "canonical_forecast_count": len(forecasts) - len(superseded_set),
        "superseded_forecast_count": len(superseded_set),
        "duplicate_correction_event_count": len(corrections),
        "settlement_event_count": len(settlements),
        "canonical_forecasts_by_model": dict(sorted(by_model.items())),
        "canonical_forecasts_by_status": dict(sorted(by_status.items())),
        "canonical_forecasts_by_market_data_status": dict(sorted(by_market.items())),
        "crown_quote_captured_count": sum(e.get("crown_snapshot_id") is not None
                                           for e in forecasts if e["forecast_id"] not in superseded_set),
        "ev_calculable_count": sum(e.get("ev_per_unit") is not None
                                   for e in forecasts if e["forecast_id"] not in superseded_set),
        "roi_calculable_count": sum(e.get("roi") is not None
                                    for e in forecasts if e["forecast_id"] not in superseded_set),
        "formal_order_count": sum(bool(e.get("formal_order")) for e in events),
        "telegram_send_count": sum(bool(e.get("telegram_sent")) for e in events),
        "unique_forecast_keys_one_canonical_each": True,
        "strict_utc_forecast_timestamps": True,
        "no_market_ev_roi_not_fabricated": True,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ledger", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    audit = build_shadow_ledger_audit(args.ledger)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(audit, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(audit, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
