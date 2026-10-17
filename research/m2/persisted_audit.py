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
from research.m2.encrypted_ledger import decode, load_locks
from research.m2.settle_forward import STATES, summarize


def audit(folder: Path, formal: dict, secret: str) -> dict:
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
        "private_payload_disclosed": False,
    }


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--ledger-folder", required=True)
    p.add_argument("--verified-formal-ledger", required=True)
    args = p.parse_args()
    secret = os.environ.get("M2_LEDGER_SECRET")
    if not secret:
        raise ValueError("Existing M2 ledger protection key unavailable")
    formal = json.loads(Path(args.verified_formal_ledger).read_text(encoding="utf-8"))
    report = audit(Path(args.ledger_folder), formal, secret)
    print(json.dumps(report, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
