"""Append-only private M3 Crown evidence store; offline and value-suppressing.

Quote values are retained only outside the repository after the evidence record
passes M3 Crown checks and its written permission explicitly covers retention.
No network client, model ledger access, order, or Telegram integration exists.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path

from research.m3.crown_evidence import validate_record
from research.m3.probabilities import expected_unit_return, settle_score

GENESIS = "0" * 64


def _canonical(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _sha(value: object) -> str:
    return hashlib.sha256(_canonical(value)).hexdigest()


def _check_private_destination(path: Path, repository_root: Path) -> Path:
    destination = path.expanduser().resolve()
    root = repository_root.expanduser().resolve()
    if destination == root or root in destination.parents:
        raise ValueError("private Crown ledger must be outside the repository")
    return destination


def add_line_ev(record: dict) -> dict:
    """Attach conditional line EV from a complete M3 score grid, if supplied."""
    forecast = record.get("forecast", {})
    grid = forecast.get("score_probability_grid")
    normalized_rows = []
    mass = 0.0
    grid_hash = None
    if grid is not None:
        if not isinstance(grid, list) or not grid:
            raise ValueError("forecast.score_probability_grid must be a non-empty array")
        for index, cell in enumerate(grid):
            if not isinstance(cell, dict):
                raise ValueError(f"score_probability_grid[{index}] must be an object")
            h, a, probability = cell.get("home_goals"), cell.get("away_goals"), cell.get("probability")
            if (isinstance(h, bool) or not isinstance(h, int) or h < 0
                    or isinstance(a, bool) or not isinstance(a, int) or a < 0
                    or isinstance(probability, bool) or not isinstance(probability, (int, float))
                    or not 0 <= probability <= 1):
                raise ValueError(f"score_probability_grid[{index}] has invalid values")
            normalized_rows.append((h, a, float(probability)))
            mass += float(probability)
        if mass <= 0 or mass > 1 + 1e-9:
            raise ValueError("score probability mass must be in (0, 1]")
        grid_hash = _sha(grid)
    quote_rows = []
    for quote in record["quotes"]:
        line = quote["line"]
        prices = (quote["price1"], quote["price2"])
        sides = ("home", "away") if quote["market"] == "AH" else ("over", "under")
        side_results = {}
        evaluation = None
        if grid is not None:
            for side, price in zip(sides, prices):
                states = {name: 0.0 for name in
                          ("FULL_WIN", "HALF_WIN", "PUSH", "HALF_LOSS", "FULL_LOSS")}
                for h, a, probability in normalized_rows:
                    state, _ = settle_score(quote["market"], line, side, h, a, price)
                    states[state] += probability / mass
                side_results[side] = {
                    "settlement_probabilities_conditional_on_grid": states,
                    "expected_unit_return_conditional_on_grid": expected_unit_return(states, price),
                    "quoted_decimal_price": price,
                }
            evaluation = {"probability_source": "full_score_grid",
                "score_grid_sha256": grid_hash,
                "score_grid_probability_coverage": mass,
                "omitted_probability_mass": max(0.0, 1.0 - mass),
                "side_results": side_results, "roi": None}
        elif quote["market"] == "OU" and abs(line - 2.5) <= 1e-9 \
                and isinstance(forecast.get("ou_p_over_2_5"), (int, float)):
            p = float(forecast["ou_p_over_2_5"])
            if not 0 <= p <= 1:
                raise ValueError("forecast.ou_p_over_2_5 must be between 0 and 1")
            for side, price, win_probability in (("over", prices[0], p), ("under", prices[1], 1-p)):
                states = {name: 0.0 for name in
                          ("FULL_WIN", "HALF_WIN", "PUSH", "HALF_LOSS", "FULL_LOSS")}
                states["FULL_WIN"], states["FULL_LOSS"] = win_probability, 1-win_probability
                side_results[side] = {"settlement_probabilities": states,
                    "expected_unit_return": expected_unit_return(states, price),
                    "quoted_decimal_price": price}
            evaluation = {"probability_source": "m3_o2_5_probability",
                "score_grid_probability_coverage": 1.0, "side_results": side_results, "roi": None}
        elif quote["market"] == "AH" and abs(line) <= 1e-9 \
                and all(isinstance(forecast.get(key), (int, float)) for key in
                        ("ah_home_0_p_win", "ah_home_0_p_push", "ah_home_0_p_lose")):
            win, push, lose = (float(forecast[k]) for k in
                               ("ah_home_0_p_win", "ah_home_0_p_push", "ah_home_0_p_lose"))
            if any(not 0 <= p <= 1 for p in (win, push, lose)) or abs(win + push + lose - 1) > 1e-9:
                raise ValueError("AH0 probabilities must be in [0,1] and sum to 1")
            for side, price, wp, pp, lp in (("home", prices[0], win, push, lose),
                                             ("away", prices[1], lose, push, win)):
                states = {name: 0.0 for name in
                          ("FULL_WIN", "HALF_WIN", "PUSH", "HALF_LOSS", "FULL_LOSS")}
                states.update({"FULL_WIN": wp, "PUSH": pp, "FULL_LOSS": lp})
                side_results[side] = {"settlement_probabilities": states,
                    "expected_unit_return": expected_unit_return(states, price),
                    "quoted_decimal_price": price}
            evaluation = {"probability_source": "m3_ah0_three_state_probability",
                "score_grid_probability_coverage": 1.0, "side_results": side_results, "roi": None}
        if evaluation is None:
            evaluation = {"available": False,
                "reason": "forecast_has_no_probability_for_this_exact_market_line", "roi": None}
        else:
            evaluation["available"] = True
        quote_rows.append({**quote, "m3_line_probability_evaluation": evaluation})
    result = dict(record)
    result["quotes"] = quote_rows
    result["forecast"] = {**forecast}
    if grid is not None:
        result["forecast"]["score_probability_grid_sha256"] = grid_hash
    return result


def _read(path: Path) -> list[dict]:
    if not path.exists():
        return []
    rows = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"invalid private ledger JSON at line {number}") from exc
        if not isinstance(row, dict):
            raise ValueError(f"invalid private ledger event at line {number}")
        expected = row.get("event_sha256")
        body = {k: v for k, v in row.items() if k != "event_sha256"}
        if expected != _sha(body):
            raise ValueError(f"private ledger hash mismatch at line {number}")
        rows.append(row)
    previous = GENESIS
    for number, row in enumerate(rows, 1):
        if row.get("previous_event_sha256") != previous:
            raise ValueError(f"private ledger chain mismatch at line {number}")
        previous = row["event_sha256"]
    return rows


def append_records(path: Path, records: list[dict], repository_root: Path) -> dict:
    destination = _check_private_destination(path, repository_root)
    if not isinstance(records, list):
        raise ValueError("input must be an array of validated evidence records")
    destination.parent.mkdir(parents=True, exist_ok=True)
    os.chmod(destination.parent, 0o700)
    if destination.exists():
        os.chmod(destination, 0o600)
    events = _read(destination)
    existing = {e["record_sha256"] for e in events}
    added = 0
    previous = events[-1]["event_sha256"] if events else GENESIS
    for record in records:
        validate_record(record)
        authorization = record["authorization"]
        uses = authorization.get("allowed_uses", [])
        if not isinstance(uses, list) or not {"m3_research", "quote_retention"}.issubset(set(uses)):
            raise ValueError("written permission must explicitly cover M3 research and quote retention")
        if record["source"].get("capture_method") == "authorized_api" and "automated_api" not in uses:
            raise ValueError("written permission must explicitly cover automated API capture")
        if record["forecast"].get("protocol") != "RECORDED_FORWARD":
            raise ValueError("private Crown shadow ledger accepts recorded-forward forecasts only")
        stored_record = add_line_ev(record)
        record_hash = _sha(stored_record)
        if record_hash in existing:
            continue
        body = {
            "event_type": "CROWN_EVIDENCE_IMPORTED",
            "protocol": "M3_PRIVATE_CROWN_LEDGER_V1",
            "event_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "record_sha256": record_hash,
            "previous_event_sha256": previous,
            "record": stored_record,
        }
        event = {**body, "event_sha256": _sha(body)}
        with destination.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")
        os.chmod(destination, 0o600)
        previous = event["event_sha256"]
        existing.add(record_hash)
        added += 1
    return audit_private_ledger(destination, repository_root, appended=added)


def audit_private_ledger(path: Path, repository_root: Path, appended: int = 0) -> dict:
    destination = _check_private_destination(path, repository_root)
    events = _read(destination)
    counts = {"AH": 0, "OU": 0}
    for event in events:
        record = event["record"]
        validate_record(record)
        for quote in record["quotes"]:
            counts[quote["market"]] += 1
    return {
        "protocol": "M3_PRIVATE_CROWN_LEDGER_AUDIT_V1",
        "generated_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "ledger_sha256": hashlib.sha256(destination.read_bytes()).hexdigest() if destination.exists() else None,
        "event_count": len(events),
        "appended_this_run": appended,
        "retained_quote_count_by_market": counts,
        "quote_values_persisted_outside_repository": True,
        "integrity_chain_valid": True,
        "formal_order": False,
        "telegram_sent": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ledger", type=Path, help="private JSONL ledger path outside the repository")
    parser.add_argument("--repository-root", type=Path, required=True)
    parser.add_argument("--input", type=Path, help="private JSON array of authorized evidence records")
    args = parser.parse_args()
    if args.input:
        records = json.loads(args.input.read_text(encoding="utf-8"))
        result = append_records(args.ledger, records, args.repository_root)
    else:
        result = audit_private_ledger(args.ledger, args.repository_root)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
