#!/usr/bin/env python3
"""M2 independent two-sided Crown market sample builder and historical evidence audit.

Reads saved production scans and strictly verified M1 FT results. Research only.
Never writes Telegram, paper orders, or predictions to public files.
"""
from __future__ import annotations
from collections import Counter
from datetime import datetime, timezone, timedelta
from pathlib import Path
import argparse
import json
import math

def utc(s):
    if not s: return None
    d=datetime.fromisoformat(str(s).replace("Z","+00:00").replace(" ","T"))
    if d.tzinfo is None: d=d.replace(tzinfo=timezone(timedelta(hours=8)))
    return d.astimezone(timezone.utc)

def val(x):
    try:
        y=float(x)
        return y if math.isfinite(y) else None
    except (ValueError,TypeError): return None

def two_sided(match,market,asof,max_quote_minutes=None):
    raw=match.get("market_raw_evidence") or {}
    if not isinstance(raw,dict):
        return None,"UNSUPPORTED_LEGACY_RAW_EVIDENCE"
    if raw.get("source_bookmaker")!="crown" or raw.get("source_bookmaker_verified") is not True:
        return None,"NOT_CROWN"
    quotes=raw.get("asian_list" if market=="AH" else "goal_list") or []
    best=None
    for q in quotes:
        if not isinstance(q,list) or len(q)<5: continue
        line,p1,p2=val(q[1]),val(q[2]),val(q[3])
        observed=utc(q[4])
        if line is None or p1 is None or p2 is None or p1<=1 or p2<=1 or not observed: continue
        age=(asof-observed).total_seconds()/60
        if age < 0:continue
        if best is None or observed>best["observed"]:
            best={"line":line,"p1":p1,"p2":p2,"observed":observed,"quote_age_min":age}
    if not best:return None,"NO_FRESH_TWO_SIDED_CROWN"
    x,y=1/best["p1"],1/best["p2"]
    best["no_vig_first"]=x/(x+y)
    best["no_vig_second"]=y/(x+y)
    best["overround"]=x+y
    best["market"]=market
    return best,None

def build(saved,formal):
    # Only results from verified FT source, not implied from outcome in scan.
    evidence={}
    for k,revs in (formal.get("results") or {}).items():
        fid=k.split("|")[0]
        for r in revs if isinstance(revs,list) else []:
            if r.get("source")!="TotalCorner API /match/view" or not r.get("raw_sha256"):continue
            if str(r.get("fixture_id"))!=fid:continue
            h,a=val(r.get("home_goals")),val(r.get("away_goals"))
            if h is None or a is None:continue
            proof=(int(h),int(a),utc(r.get("observed_at")))
            if fid in evidence and evidence[fid][:2]!=proof[:2]:evidence[fid]=None
            elif fid not in evidence:evidence[fid]=proof
    counts=Counter()
    output=[]
    first_seen=set()
    for f in sorted(Path(saved).glob("M1_*.json")):
        try:scan=json.loads(f.read_text(encoding="utf-8"))
        except (ValueError,OSError):
            counts["UNREADABLE_RUN"]+=1;continue
        if scan.get("scan_status")!="COMPLETE":
            counts["PARTIAL_SCAN"]+=1;continue
        asof=utc(scan.get("finished_at"))
        if asof is None:continue
        for m in scan.get("matches") or []:
            if not isinstance(m,dict):
                counts["UNSUPPORTED_LEGACY_MATCH"]+=1;continue
            fid=str(m.get("fixture_id") or "")
            if not fid or m.get("scope",{}).get("status")!="IN":continue
            kickoff=utc(m.get("kickoff_bj"))
            if not kickoff or not 8 <= (kickoff-asof).total_seconds()/3600 <=24:
                counts["OUTSIDE_PREMATCH_WINDOW"]+=1;continue
            for market in ("AH","OU"):
                counts["SCOPED_MARKET_OBSERVATIONS"]+=1
                key=(fid,market)
                if key in first_seen:continue
                quote,reason=two_sided(m,market,asof)
                if reason:
                    counts[reason]+=1
                    counts[f"{market}_{reason}"]+=1
                    continue
                counts[f"{market}_FRESH_TWO_SIDED_CROWN"]+=1
                first_seen.add(key)
                final=evidence.get(fid)
                if not final or final[2] is None or final[2]<=asof:
                    counts["NOT_YET_VERIFIED_FT"]+=1
                    counts[f"{market}_NOT_YET_VERIFIED_FT"]+=1
                    continue
                features=m.get("distilled_teacher_concept_proxies") or {}
                row={
                  "fixture_id":fid,"market":market,
                  "asof":asof.isoformat(),"kickoff":kickoff.isoformat(),
                  "market_line":quote["line"],
                  "crown_price_first":quote["p1"],
                  "crown_price_second":quote["p2"],
                  "crown_no_vig_first":quote["no_vig_first"],
                  "crown_overround":quote["overround"],
                  "quote_age_minutes":quote["quote_age_min"],
                  "quote_timestamp":quote["observed"].isoformat(),
                  "scan_completed_at":asof.isoformat(),
                  "last_successful_fetch_at":None,
                  "last_price_change_at":None,
                  "timestamp_semantics":"SOURCE_TIMESTAMP_UNVERIFIED_FETCH_OR_CHANGE",
                  "ft_home":final[0],"ft_away":final[1],
                  "m1_goal_total":val(features.get("model_expected_total")),
                  "m1_goal_diff":val(features.get("model_expected_goal_difference")),
                  "form_diff_home5":val(features.get("home_form_goal_diff_5")),
                  "form_diff_away5":val(features.get("away_form_goal_diff_5")),
                  "form_diff_home20":val(features.get("home_form_goal_diff_20")),
                  "form_diff_away20":val(features.get("away_form_goal_diff_20")),
                }
                output.append(row)
                counts[f"{market}_AUDITED_VERIFIED_SAMPLES"]+=1
    # Ensure one market per fixture and no after-result samples; do not output raw rows in public CI.
    assert len({(r["fixture_id"],r["market"]) for r in output})==len(output)
    for row in output:
        assert utc(row["asof"])<utc(row["kickoff"])
    counts["AUDITED_VERIFIED_SAMPLES"]=len(output)
    counts["AUDITED_UNIQUE_MATCHES"]=len({r["fixture_id"] for r in output})
    return output,dict(counts)

def main():
    a=argparse.ArgumentParser()
    a.add_argument("--runs",required=True)
    a.add_argument("--ledger",required=True)
    a.add_argument("--out",required=True)
    p=a.parse_args()
    rows,counts=build(p.runs,json.loads(Path(p.ledger).read_text(encoding="utf-8")))
    target=Path(p.out);target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(json.dumps({"protocol":"M2_VERIFIED_CROWN_TWO_SIDED_DATASET_V1",
        "rows":rows,"counts":counts},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"protocol":"M2_VERIFIED_CROWN_TWO_SIDED_AUDIT_V1",
        "counts":counts,"sufficient_for_training":len(rows)>=200},ensure_ascii=False))

if __name__=="__main__":main()
