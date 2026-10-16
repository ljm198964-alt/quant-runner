#!/usr/bin/env python3
"""Read-only M1 weekly TG-confirmed accounting from original production ledger.

Week assignment is first actual TG SENT time (Asia/Shanghai), NEVER FT settlement
time. No writes to source ledger. No effect on formal pick selection or delivery.
"""
from __future__ import annotations
import argparse
import collections
from datetime import datetime, timedelta, timezone
from decimal import Decimal
import json
from pathlib import Path
from zoneinfo import ZoneInfo

BJ = ZoneInfo("Asia/Shanghai")
STATES = ("FULL_WIN", "HALF_WIN", "PUSH", "HALF_LOSS", "FULL_LOSS")
R1 = "M1_SELECTION_20260924_EARLY_ROBUST"

def timestamp(s):
    if not s: return None
    d = datetime.fromisoformat(str(s).replace("Z", "+00:00"))
    if d.tzinfo is None: raise ValueError("Unzoned TG sent timestamp")
    return d.astimezone(BJ)

def week_start(d):
    local = d.astimezone(BJ)
    return (local - timedelta(days=local.weekday())).date().isoformat()

def classification(p):
    market = str(p.get("market") or "").upper()
    if market == "AH": return "M1 AH"
    if market == "OU":
        strategy = str(p.get("strategy_rule_version") or p.get("selection_policy") or "")
        return "M1 OU R1" if R1 in strategy else "M1 OU old/other"
    return None

def records(ledger):
    picks = ledger.get("picks") or {}
    notifications = ledger.get("notifications") or {}
    settlements = ledger.get("settlements") or {}
    events = ledger.get("account_events") or {}
    if not isinstance(picks, dict) or not isinstance(notifications, dict):
        raise ValueError("Unsupported ledger schema: picks/notifications must be mappings")
    by_pick = {}
    for key, pick in picks.items():
        if not isinstance(pick, dict): continue
        group = classification(pick)
        if not group: continue
        by_pick[pick.get("pick_id") or key] = (key, group, pick)
    tg = {}
    for key, note in notifications.items():
        if not isinstance(note, dict): continue
        p = note.get("pick_id") or (by_pick.get(key) or (None, None, {}))[2].get("pick_id")
        receipt = note.get("telegram") or {}
        if p not in by_pick or receipt.get("status") != "SENT":
            continue
        if not receipt.get("provider_message_id"): continue
        at = timestamp(receipt.get("sent_at") or receipt.get("provider_sent_at"))
        if not at: continue
        previous = tg.get(p)
        if previous is None or at < previous[0]: tg[p] = (at, receipt)
    # Latest actual settlement event per pick, sorted by event chronology; never
    # treat an unconfirmed lock or UNKNOWN notification as a sent wager.
    latest = {}
    if isinstance(events, dict):
        for ev in events.values():
            if not isinstance(ev, dict): continue
            pid = ev.get("pick_id")
            if pid not in by_pick: continue
            s = (ev.get("settlement_revision_id") or ev.get("revision_id") or "")
            at = ev.get("created_at") or ev.get("settled_at")
            if not s or not at: continue
            t = timestamp(at)
            if pid not in latest or t > latest[pid][0]:
                latest[pid] = (t, ev.get("delta_pnl_u"), s)
    for pid, (at, receipt) in tg.items():
        key, group, pick = by_pick[pid]
        outcome = None
        pnl = None
        revisions = settlements.get(key) or []
        if isinstance(revisions, list) and revisions:
            rev = revisions[-1]
            outcome = rev.get("state")
            pnl = rev.get("pnl_u")
        # If account event corresponds to this settlement revision, its delta is
        # authoritative realized amount; otherwise keep the latest revision pnl.
        if pid in latest:
            _, amount, _ = latest[pid]
            if amount is not None: pnl = amount
        if outcome not in STATES:
            outcome, pnl = None, None
        yield dict(pick_id=pid, group=group, sent_at=at.isoformat(),
                   week=week_start(at), status=outcome or "PENDING",
                   pnl=Decimal(str(pnl)) if pnl is not None else None,
                   message_id=str(receipt.get("provider_message_id")))

def aggregate(rows):
    groups = {}
    for row in rows:
        bucket = groups.setdefault(row["group"], dict(sent=0,settled=0,pending=0,
                            pnl=Decimal("0"),states={k:0 for k in STATES}))
        bucket["sent"] += 1
        if row["status"] == "PENDING":
            bucket["pending"] += 1
        else:
            bucket["settled"] += 1
            bucket["states"][row["status"]] += 1
            if row["pnl"] is None: raise ValueError("A settlement has no realized PnL")
            bucket["pnl"] += row["pnl"]
    out = {}
    for name,v in sorted(groups.items()):
        pnl = v.pop("pnl")
        out[name] = {**v, "net_u": str(pnl),
                     "roi": str(pnl/Decimal(v["settled"])) if v["settled"] else None}
    return out

def report(ledger, requested_week=None):
    entries = list(records(ledger))
    if len({x["pick_id"] for x in entries}) != len(entries):
        raise ValueError("Duplicate TG-confirmed pick IDs")
    all_weeks = sorted({x["week"] for x in entries})
    target = requested_week or (all_weeks[-1] if all_weeks else None)
    return dict(protocol="M1_WEEKLY_TG_CONFIRMED_V1",
                timezone="Asia/Shanghai", week_start=target,
                all_time=aggregate(entries),
                requested_week=aggregate(x for x in entries if x["week"]==target),
                tg_confirmed_unique=len(entries),
                week_tg_confirmed=sum(x["week"]==target for x in entries),
                missing_week=(target not in all_weeks),
                note="Confirmed TG SENT only. Old OU and OU R1 kept separate; no shadows or UNKNOWN.")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ledger", required=True)
    parser.add_argument("--week-start", help="Beijing Monday YYYY-MM-DD")
    parser.add_argument("--reference-report", help="Required TG-confirmed production report for reconciliation")
    args=parser.parse_args()
    if args.week_start:
        d=datetime.fromisoformat(args.week_start).date()
        if d.weekday()!=0: raise ValueError("--week-start must be Monday")
    result=report(json.loads(Path(args.ledger).read_text(encoding="utf8")),args.week_start)
    if args.reference_report:
        ref=json.loads(Path(args.reference_report).read_text(encoding="utf8"))
        expected=int(ref["total"]["picks"])
        if result["tg_confirmed_unique"] != expected:
            raise ValueError(f"TG confirmed mismatch: weekly reconstruction {result['tg_confirmed_unique']} != production {expected}")
        for name,stat in (("AH",ref["markets"]["AH"]),("OU",ref["markets"]["OU"])):
            reported=sum(int(v["sent"]) for k,v in result["all_time"].items() if (k=="M1 AH" if name=="AH" else k.startswith("M1 OU")))
            if reported != stat["picks"]:
                raise ValueError(f"{name} reconciliation mismatch: {reported} != {stat['picks']}")
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()
