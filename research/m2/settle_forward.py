#!/usr/bin/env python3
"""Read-only verified-FT settlement for encrypted M2 V0 research baseline.

Results from existing M1 verified FT ledger only. No market API, wagers, TG.
Do not interpret this baseline as independently trained M2 performance.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
from decimal import Decimal
import hashlib
import json
from pathlib import Path

from research.m2.encrypted_ledger import encode, decode, load_locks, kickoff_utc

SOURCE = "TotalCorner API /match/view"
STATES = ("FULL_WIN","HALF_WIN","PUSH","HALF_LOSS","FULL_LOSS")

def components(line):
    q=Decimal(str(line))*4
    if q != int(q): raise ValueError("Non-quarter Asian handicap")
    n=int(q)
    return (n,) if n%2==0 else (n-1,n+1)

def realized(lock, home, away):
    price=Decimal(str(lock["crown_decimal_price"]))
    if price <= 1: raise ValueError("Invalid locked price")
    hk=price-1
    market=lock["market"]
    if market == "AH":
        if lock["side"] not in ("HOME","AWAY"): raise ValueError("Bad AH side")
        margin=(home-away) if lock["side"]=="HOME" else (away-home)
        checks=[4*margin+q for q in components(lock["line"])]
    elif market == "OU":
        if lock["side"] not in ("OVER","UNDER"): raise ValueError("Bad OU side")
        sign=1 if lock["side"]=="OVER" else -1
        checks=[sign*(4*(home+away)-q) for q in components(lock["line"])]
    else: raise ValueError("Bad market")
    portions=[hk if v>0 else (Decimal(0) if v==0 else Decimal(-1)) for v in checks]
    pnl=sum(portions)/len(portions)
    if pnl==hk: state="FULL_WIN"
    elif pnl==hk/2: state="HALF_WIN"
    elif pnl==0: state="PUSH"
    elif pnl==Decimal("-0.5"): state="HALF_LOSS"
    elif pnl==-1: state="FULL_LOSS"
    else: raise ValueError("Impossible Asian settlement")
    return state,pnl

def verified_finals(ledger):
    by_fixture={}
    for key, revisions in (ledger.get("results") or {}).items():
        for ev in revisions if isinstance(revisions,list) else ():
            if not isinstance(ev,dict): continue
            if ev.get("source")!=SOURCE or not ev.get("raw_sha256"): continue
            fid=str(ev.get("fixture_id") or key.split("|")[0])
            if fid != key.split("|")[0]: raise ValueError("Mismatched verified FT fixture")
            try:
                h=int(ev["home_goals"]); a=int(ev["away_goals"])
                if h<0 or a<0: continue
            except (KeyError,TypeError,ValueError): continue
            if not ev.get("observed_at") or not ev.get("locked_kickoff"): continue
            current=by_fixture.get(fid)
            if current is not None:
                if (current["h"],current["a"])!=(h,a):
                    # Do not settle contested result revisions.
                    by_fixture[fid]={"conflict":True}
                    continue
                if current.get("conflict"): continue
            by_fixture[fid]={"h":h,"a":a,"hash":ev["raw_sha256"],
                              "locked_kickoff":ev["locked_kickoff"],
                              "kickoff_changed":ev.get("kickoff_changed",False),
                              "observed_at":ev["observed_at"]}
    return by_fixture

def summarize(locks,existing,source,now=None):
    now=now or datetime.now(timezone.utc)
    if now.tzinfo is None: raise ValueError("Time requires timezone")
    finals=verified_finals(source)
    keys={(x["fixture_id"],x["market"]) for x in existing}
    staged=[]
    reasons={}
    for lock in locks:
        k=(lock["fixture_id"],lock["market"])
        if k in keys: continue
        if kickoff_utc(lock["kickoff_bj"])>=now: 
            reasons["NOT_STARTED"]=reasons.get("NOT_STARTED",0)+1;continue
        verified=finals.get(lock["fixture_id"])
        if not verified or verified.get("conflict"):
            reasons["NO_UNCONTESTED_VERIFIED_FT"]=reasons.get("NO_UNCONTESTED_VERIFIED_FT",0)+1;continue
        if verified["kickoff_changed"] or datetime.fromisoformat(verified["locked_kickoff"]).astimezone(timezone.utc)!=kickoff_utc(lock["kickoff_bj"]):
            reasons["KICKOFF_IDENTITY_MISMATCH"]=reasons.get("KICKOFF_IDENTITY_MISMATCH",0)+1;continue
        status,pnl=realized(lock,verified["h"],verified["a"])
        row={"model_identity":lock["model_identity"],
             "fixture_id":lock["fixture_id"],"market":lock["market"],
             "lock_observation_id":lock["observation_id"],
             "state":status,"pnl_u":str(pnl),
             "home_goals":verified["h"],"away_goals":verified["a"],
             "verified_ft_sha256":verified["hash"],
             "settled_at":now.isoformat(),"telegram_write":False}
        staged.append(row)
        keys.add(k)
    return staged,reasons

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--ledger-folder",required=True)
    p.add_argument("--verified-formal-ledger",required=True)
    p.add_argument("--key-env",default="M2_LEDGER_SECRET")
    opts=p.parse_args()
    import os
    secret=os.environ.get(opts.key_env)
    if not secret: raise ValueError("M2 decrypt key missing")
    folder=Path(opts.ledger_folder)
    locks=load_locks(folder,secret)
    settle_dir=folder/"settlements"
    existing=[]
    for f in sorted(settle_dir.glob("*.enc.json")):
        record=decode(f.read_text(encoding="utf-8"),secret)
        if record.get("protocol")!="M2_V0_VERIFIED_SETTLEMENT_V1":
            raise ValueError("Unrecognized settlement record")
        existing.extend(record["settlements"])
    verified=json.loads(Path(opts.verified_formal_ledger).read_text(encoding="utf-8"))
    new,reasons=summarize(locks,existing,verified)
    if new:
        settle_dir.mkdir(parents=True,exist_ok=True)
        batchid=hashlib.sha256(json.dumps(new,sort_keys=True).encode()).hexdigest()[:24]
        target=settle_dir/(batchid+".enc.json")
        with target.open("x",encoding="utf-8") as f:
            f.write(encode({"protocol":"M2_V0_VERIFIED_SETTLEMENT_V1",
                "settlements":new},secret))
    all_settled=existing+new
    pnl=sum((Decimal(x["pnl_u"]) for x in all_settled),Decimal(0))
    print(json.dumps({
        "protocol":"M2_V0_BASELINE_SETTLEMENT_SUMMARY_V1",
        "baseline_locks":len(locks),"baseline_settled":len(all_settled),
        "baseline_pending":len(locks)-len(all_settled),
        "new_verified_settlements":len(new),
        "pending_reasons":reasons,
        "baseline_net_u":str(pnl),
        "baseline_roi":str(pnl/len(all_settled)) if all_settled else None,
        "m2_trained_model_roi":None,
        "tg_sent":False
    },ensure_ascii=False))

if __name__=="__main__":
    main()
