#!/usr/bin/env python3
"""Read-only aggregate audit of persisted encrypted M2 research baseline.

Print no fixture IDs, teams, quotes, encrypted plaintext or secret.
This measures M1-side M2 V0 comparator; it is not trained M2 ROI.
"""
from __future__ import annotations
import argparse
import json
import os
from collections import Counter
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
from research.m2.encrypted_ledger import decode, load_locks, kickoff_utc
from research.m2.settle_forward import STATES, summarize, verified_finals


def extra_diagnostics(locks, confirmed, formal, alternate, now):
    """Read-only privacy-safe cohorts; neither selects bets nor settles additional FT."""
    settled_keys = {(str(r["fixture_id"]), r["market"]) for r in confirmed}
    final_map = verified_finals(formal)
    formal_pick_ids = {str(k).split("|")[0] for k in (formal.get("picks") or {})}
    formal_result_ids = {str(k).split("|")[0] for k in (formal.get("results") or {})}
    alternate_results = (alternate or {}).get("results") or {}
    missing = []
    for lock in locks:
        fid = str(lock["fixture_id"])
        if (fid, lock["market"]) in settled_keys or kickoff_utc(lock["kickoff_bj"]) >= now:
            continue
        proof = final_map.get(fid)
        if proof is None:
            reason = "NO_STRICT_VERIFIED_FT"
        elif proof.get("conflict"):
            reason = "CONTESTED_FT"
        elif proof.get("kickoff_changed") or proof.get("locked_kickoff") != kickoff_utc(lock["kickoff_bj"]).isoformat():
            reason = "KICKOFF_EVIDENCE_MISMATCH"
        else:
            reason = "VERIFIED_FT_AVAILABLE_NOT_PERSISTED"
        missing.append((lock, reason))
    causes = Counter(reason for _, reason in missing)
    source_presence = {
        "has_any_m1_formal_pick": sum(str(lock["fixture_id"]) in formal_pick_ids for lock, _ in missing),
        "has_any_m1_result_revision": sum(str(lock["fixture_id"]) in formal_result_ids for lock, _ in missing),
        "has_alternate_saved_ft_entry_research_only": sum(
            str(lock["fixture_id"]) in alternate_results for lock, _ in missing
        ),
    }
    by_market_pending = {
        market: {
            "started_without_settlement": sum(lock["market"] == market for lock, _ in missing),
            "missing_strict_verified_ft": sum(
                lock["market"] == market and reason == "NO_STRICT_VERIFIED_FT"
                for lock, reason in missing
            ),
        }
        for market in ("AH", "OU")
    }
    settled_by_direction = {}
    locked_side = {(str(lock["fixture_id"]), lock["market"]): lock["side"] for lock in locks}
    for market, sides in (("AH", ("HOME", "AWAY")), ("OU", ("OVER", "UNDER"))):
        rs = [r for r in confirmed if r["market"] == market]
        cohorts = {}
        for side in sides:
            subset = [r for r in rs if locked_side.get((str(r["fixture_id"]), market)) == side]
            pnl = sum((Decimal(str(r["pnl_u"])) for r in subset), Decimal(0))
            cohorts[side] = {
                "settled": len(subset),
                "net_u": str(pnl),
                "roi": str(pnl / len(subset)) if subset else None,
                "states": {state: sum(r["state"] == state for r in subset) for state in STATES},
            }
        settled_by_direction[market] = cohorts
    return {
        "pending_started_reason_counts": dict(causes),
        "pending_started_unique_fixtures": len({str(r["fixture_id"]) for r, _ in missing}),
        "pending_started_source_presence": source_presence,
        "pending_started_by_market": by_market_pending,
        "persisted_settlements_by_direction": settled_by_direction,
        "descriptive_only_no_new_settlement_or_rule": True,
    }


def audit(folder: Path, formal: dict, secret: str, alternate: dict | None = None) -> dict:
    locks = load_locks(folder, secret)
    settlement_rows = []
    for f in sorted((folder / "settlements").glob("*.enc.json")):
        payload = decode(f.read_text(encoding="utf-8"), secret)
        if payload.get("protocol") != "M2_V0_VERIFIED_SETTLEMENT_V1":
            raise ValueError("Unknown encrypted settlement payload")
        settlement_rows.extend(payload.get("settlements", []))

    unique = {}
    duplicated = 0
    for row in settlement_rows:
        key = (str(row["fixture_id"]), row["market"])
        if key in unique:
            duplicated += 1
            if unique[key] != row:
                raise ValueError("Conflicting persisted settlements")
        else:
            unique[key] = row
    confirmed = list(unique.values())
    pnl = sum((Decimal(str(r["pnl_u"])) for r in confirmed), Decimal(0))
    by_market = {}
    for market in ("AH", "OU"):
        rs = [r for r in confirmed if r["market"] == market]
        total = sum((Decimal(str(r["pnl_u"])) for r in rs), Decimal(0))
        by_market[market] = {
            "settled": len(rs),
            "net_u": str(total),
            "roi": str(total / len(rs)) if rs else None,
            "states": {state: sum(r["state"] == state for r in rs) for state in STATES},
        }

    potential, pending_reasons = summarize(
        locks, confirmed, formal, datetime.now(timezone.utc)
    )
    pending_by_market = Counter(r["market"] for r in locks)
    for row in confirmed:
        pending_by_market[row["market"]] -= 1
    return {
        "protocol": "M2_PERSISTED_BASELINE_AGGREGATE_AUDIT_V1",
        "asof_utc": datetime.now(timezone.utc).isoformat(),
        "baseline_not_trained_m2": True,
        "telegram_sent": 0,
        "persisted_locks": len(locks),
        "unique_fixtures": len({r["fixture_id"] for r in locks}),
        "persisted_settled": len(confirmed),
        "persisted_pending": len(locks) - len(confirmed),
        "persisted_duplicate_settlement_rows": duplicated,
        "persisted_net_u": str(pnl),
        "persisted_roi": str(pnl / len(confirmed)) if confirmed else None,
        "persisted_by_market": by_market,
        "pending_by_market": dict(pending_by_market),
        "new_verified_ft_available_but_not_persisted": len(potential),
        "other_pending_reasons": pending_reasons,
        "ft_and_side_diagnostics": extra_diagnostics(locks, confirmed, formal, alternate, datetime.now(timezone.utc)),
        "private_payload_disclosed": False,
    }


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--ledger-folder", required=True)
    p.add_argument("--verified-formal-ledger", required=True)
    p.add_argument("--alternate-saved-ft", required=False)
    args = p.parse_args()
    secret = os.environ.get("M2_LEDGER_SECRET")
    if not secret:
        raise ValueError("Existing M2 ledger protection key unavailable")
    formal = json.loads(Path(args.verified_formal_ledger).read_text(encoding="utf-8"))
    alternate = json.loads(Path(args.alternate_saved_ft).read_text(encoding="utf-8")) if args.alternate_saved_ft else None
    report = audit(Path(args.ledger_folder), formal, secret, alternate)
    print(json.dumps(report, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
