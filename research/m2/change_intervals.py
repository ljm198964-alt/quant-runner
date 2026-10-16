#!/usr/bin/env python3
"""M2 read-only Crown cross-scan price-change evidence.

A changed value between two successfully fetched snapshots establishes only
a change *interval*, not the precise time of an exchange update.
Never treat provider historical event time as a verified fetch timestamp.
"""
from __future__ import annotations
import argparse, json
from collections import Counter
from pathlib import Path
from .market_dataset import utc, val

def transitions(scans):
    previous = {}
    counts = Counter()
    examples = []
    ordered = sorted(scans, key=lambda x: str(x.get("finished_at") or ""))
    for scan in ordered:
        if scan.get("scan_status") != "COMPLETE":
            continue
        finished = utc(scan.get("finished_at"))
        if finished is None:
            continue
        for m in scan.get("matches") or []:
            if not isinstance(m, dict):
                continue
            raw = m.get("market_raw_evidence")
            if not isinstance(raw, dict) or raw.get("source_bookmaker") != "crown" or raw.get("source_bookmaker_verified") is not True:
                continue
            fixture = str(m.get("fixture_id") or "")
            if not fixture:
                continue
            capture = m.get("market_capture_evidence") or {}
            fetch = utc(capture.get("last_successful_fetch_at"))
            for market, field in (("AH","asian_list"),("OU","goal_list")):
                available=[]
                for q in raw.get(field) or []:
                    if not isinstance(q,(list,tuple)) or len(q)<5:
                        continue
                    at=utc(q[4])
                    price=(val(q[1]),val(q[2]),val(q[3]))
                    if at is not None and at<=finished and None not in price and price[1]>1 and price[2]>1:
                        available.append((at,price))
                if not available:
                    continue
                event,quote=max(available,key=lambda a:a[0])
                key=(fixture,market)
                current={"price":quote,"fetch":fetch,"provider_event":event,"scan":finished}
                counts[f"{market}_snapshots"]+=1
                old=previous.get(key)
                if old is not None:
                    if old["price"]==quote:
                        counts[f"{market}_unchanged_pairs"]+=1
                    else:
                        counts[f"{market}_changed_pairs"]+=1
                        if old["fetch"] and fetch and old["fetch"]<fetch:
                            counts[f"{market}_verified_fetch_brackets"]+=1
                            # No exact exchange-change timestamp is inferred.
                        else:
                            counts[f"{market}_change_time_unknown_pairs"]+=1
                previous[key]=current
    return dict(counts)

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--runs",required=True)
    args=parser.parse_args()
    scans=[]
    for p in Path(args.runs).glob("M1_*.json"):
        try: scans.append(json.loads(p.read_text(encoding="utf-8")))
        except (OSError,ValueError): continue
    print(json.dumps({"protocol":"M2_CROWN_CHANGE_INTERVAL_AUDIT_V1",
                      "counts":transitions(scans),
                      "exact_price_change_time_inferred":False},ensure_ascii=False))
if __name__=="__main__":main()
