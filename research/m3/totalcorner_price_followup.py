"""Capture genuine follow-up TotalCorner default odds for future M3 fixtures.

Operational request budget only; does not filter or modify model orders.
"""
import argparse,datetime,json,os,time
from pathlib import Path
from research.m3.totalcorner_forward_ev import get_latest,hash_id
from research.m3.totalcorner_shadow_ev import fetch
UTC=datetime.timezone.utc
def parse(s):
    return datetime.datetime.fromisoformat(s.replace("Z","+00:00")).astimezone(UTC)
def capture(events,token,limit=25,delay=2.2):
    now=datetime.datetime.now(UTC)
    fixtures={}
    for e in events:
        if e.get("protocol")!="M3_TOTALCORNER_FORWARD_FORECAST_V1":continue
        mid=str(e.get("totalcorner_match_id") or "")
        if not mid:
            # Older forecasts intentionally omit match ID; resolve via linked quotes.
            continue
        try:kickoff=parse(e["kickoff_utc_verified"])
        except (KeyError,TypeError,ValueError):continue
        if kickoff>now:fixtures[mid]=kickoff
    for e in events:
        if e.get("protocol")!="M3_TOTALCORNER_FORWARD_EV_V1":continue
        mid=str(e.get("totalcorner_match_id") or "")
        try:kickoff=parse(e["kickoff_utc_verified"])
        except (KeyError,TypeError,ValueError):
            continue
        if mid and kickoff>now:fixtures[mid]=kickoff
    last={}
    for e in events:
        if e.get("protocol")!="M3_TOTALCORNER_PRICE_SNAPSHOT_V1":continue
        mid=str(e.get("totalcorner_match_id"))
        try:t=parse(e["captured_at_utc"])
        except (KeyError,TypeError,ValueError):continue
        if mid not in last or t>last[mid]:last[mid]=t
    ordered=sorted(fixtures,key=lambda mid:(last.get(mid,datetime.datetime.min.replace(tzinfo=UTC)),mid))
    rows=[];errors=[]
    for mid in ordered[:limit]:
        try:
            match=fetch(mid,token)
            captured=datetime.datetime.now(UTC).isoformat()
            for market,field,sides in (("AH","asian_list",("home","away")),("OU","goal_list",("over","under"))):
                quote=get_latest(match.get(field))
                if quote is None:continue
                _,line,a,b=quote
                for side,odd in zip(sides,(a,b)):
                    event={"protocol":"M3_TOTALCORNER_PRICE_SNAPSHOT_V1",
                           "totalcorner_match_id":mid,"provider":"TotalCorner",
                           "bookmaker":"totalcorner_default_NOT_CROWN",
                           "market":market,"line":line,"side":side,
                           "decimal_odd":odd,"captured_at_utc":captured,
                           "kickoff_utc":fixtures[mid],"research_only":True}
                    event["kickoff_utc"]=fixtures[mid].isoformat()
                    event["event_id"]=hash_id(["M3_PRICE_SNAPSHOT_V1",mid,market,line,side,captured])
                    rows.append(event)
        except Exception as exc:
            errors.append({"match_id":mid,"error_type":type(exc).__name__})
        time.sleep(delay)
    return rows,{"eligible_fixtures":len(ordered),"attempted_fixtures":min(limit,len(ordered)),
                 "deferred_due_request_budget":max(0,len(ordered)-limit),
                 "snapshot_events":len(rows),"errors":errors}
def main():
    p=argparse.ArgumentParser();p.add_argument("--ledger",type=Path,required=True)
    p.add_argument("--max-matches",type=int,default=25);a=p.parse_args()
    events=[json.loads(s) for s in a.ledger.open() if s.strip()]
    rows,stats=capture(events,os.environ["TOTALCORNER_TOKEN"],a.max_matches)
    with a.ledger.open("a") as out:
        for e in rows:out.write(json.dumps(e,ensure_ascii=False,sort_keys=True)+"\n")
    print(json.dumps(stats))
if __name__=="__main__":main()
