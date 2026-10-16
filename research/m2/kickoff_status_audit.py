#!/usr/bin/env python3
"""Summarize confidential M2 baseline kickoff status inside authorized runner.

No teams, odds, fixture IDs, or decrypted records in output.
"""
from __future__ import annotations
import argparse,json,os
from collections import Counter
from datetime import datetime,timezone
from pathlib import Path
from research.m2.encrypted_ledger import load_locks,kickoff_utc
from research.m2.settle_forward import verified_finals

def audit(locks, formal, now):
    totals=Counter()
    finals=verified_finals(formal)
    fixtures=set()
    started_fixtures=set()
    for r in locks:
        fixtures.add(r["fixture_id"])
        kick=kickoff_utc(r["kickoff_bj"])
        if kick>now:
            totals["not_started"]+=1
            continue
        started_fixtures.add(r["fixture_id"])
        totals["kickoff_passed"]+=1
        v=finals.get(r["fixture_id"])
        if not v:totals["started_without_verified_ft"]+=1
        elif v.get("conflict"):totals["started_contested_ft"]+=1
        elif v.get("kickoff_changed"):totals["started_kickoff_changed"]+=1
        else:totals["started_with_verified_ft_candidate"]+=1
    return {"protocol":"M2_CONFIDENTIAL_KICKOFF_STATUS_AUDIT_V1",
            "asof_utc":now.isoformat(),
            "locked_market_records":len(locks),
            "distinct_fixtures":len(fixtures),
            "started_distinct_fixtures":len(started_fixtures),
            "counts":dict(totals),"private_payload_disclosed":False}

if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--ledger-folder",required=True);p.add_argument("--formal",required=True)
    a=p.parse_args()
    secret=os.environ.get("M2_LEDGER_SECRET")
    if not secret:raise ValueError("Protected ledger key unavailable")
    locks=load_locks(Path(a.ledger_folder),secret)
    data=json.loads(Path(a.formal).read_text(encoding="utf-8"))
    print(json.dumps(audit(locks,data,datetime.now(timezone.utc)),ensure_ascii=False))
