#!/usr/bin/env python3
"""Opponent team recurrence versus archived M1 opportunity pool.

Conservative exact names only; never equate missing source coverage with a non-pick.
No model or formal policy changes.
"""
import argparse, json
from collections import Counter
from datetime import datetime, timezone, timedelta
from pathlib import Path
def dt(s, beijing=False):
    try:
        d=datetime.fromisoformat(str(s).replace("Z","+00:00").replace(" ","T"))
        if d.tzinfo is None: d=d.replace(tzinfo=timezone(timedelta(hours=8 if beijing else 0)))
        return d.astimezone(timezone.utc)
    except (ValueError,TypeError):return None
def norm(s):
    return " ".join(str(s or "").strip().lower().split())
def key(date,league,home,away):
    return (date,norm(league),norm(home),norm(away))
def audit(root):
    opp={}
    for p in sorted((root/"data/opponent").glob("opponent_picks_*.json")):
        try: rows=json.loads(p.read_text())["records"]
        except (ValueError,OSError,KeyError):continue
        for r in rows:
            if r.get("market") in ("AH","OU") and r.get("gmail_id"):opp[r["gmail_id"]]=r
    picked={}
    for r in opp.values():
        k=dt(r.get("kickoff_bj"),True)
        mail=dt(r.get("email_ts"))
        if not k or not mail:continue
        ident=key(k.isoformat(),r.get("league_cn"),r.get("home_cn"),r.get("away_cn"))
        if not all(ident):continue
        if ident not in picked or mail<picked[ident]["mail"]:
            picked[ident]={"mail":mail,"teams":(ident[2],ident[3]),"league":ident[1],"kickoff":k}
    chosen=sorted(picked.values(),key=lambda x:x["mail"])
    # At each pick, only earlier, actually observed opponent messages can create familiarity.
    seen=set()
    familiar_at_pick={}
    for x in chosen:
        familiar_at_pick[(x["kickoff"].isoformat(),x["league"],*x["teams"])]=any(t in seen for t in x["teams"])
        seen.update(x["teams"])
    pool={}
    scan_count=0
    for p in (root/"results/runs").glob("M1_*.json"):
        try: scan=json.loads(p.read_text())
        except (OSError,ValueError):continue
        if scan.get("scan_status")!="COMPLETE":continue
        asof=dt(scan.get("finished_at"))
        if asof is None:continue
        scan_count+=1
        for m in scan.get("matches") or []:
            if not isinstance(m,dict) or (m.get("scope") or {}).get("status")!="IN":continue
            kick=dt(m.get("kickoff_bj"),True)
            if kick is None or not 8 <= (kick-asof).total_seconds()/3600 <=24:continue
            ident=key(kick.isoformat(),m.get("league"),m.get("home"),m.get("away"))
            if not all(ident):continue
            pool[ident]=True
    matches=set(pool).intersection(familiar_at_pick)
    same_window=[k for k in familiar_at_pick if k in pool]
    return {"protocol":"OPPONENT_FAMILIARITY_POOL_COVERAGE_V1",
      "unique_opponent_matches":len(chosen),"complete_scans":scan_count,
      "unique_scoped_opportunities":len(pool),
      "exact_fixture_name_matches":len(matches),
      "exact_match_rate":round(len(matches)/len(chosen),4) if chosen else None,
      "opponent_previously_seen_team_share":round(sum(familiar_at_pick.values())/len(chosen),4) if chosen else None,
      "matched_opponent_previously_seen_count":sum(familiar_at_pick[k] for k in matches),
      "unmatched_opponent_count":len(chosen)-len(matches),
      "selection_lift_vs_available_pool":None,
      "reason_no_lift":"No verified cross-provider fixture identity and full same-time tradable opportunity coverage; exact matched subset insufficient to assume unbiased control.",
      "notes":"Exact fixture matching only; M1 in-scope scan is not entire available market; no claim of opponent preference/ROI."}
def main():
    a=argparse.ArgumentParser();a.add_argument("--source",required=True);p=a.parse_args()
    print(json.dumps(audit(Path(p.source)),ensure_ascii=False))
if __name__=="__main__":main()
