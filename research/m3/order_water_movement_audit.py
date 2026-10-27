"""Read-only order-level M3 water movement audit using recorded TotalCorner prices."""
import argparse,collections,datetime,json
from pathlib import Path

def timestamp(value):
    d=datetime.datetime.fromisoformat(value.replace("Z","+00:00"))
    if d.tzinfo is None:raise ValueError("missing timezone")
    return d.astimezone(datetime.timezone.utc)

def audit(events):
    orders=[e for e in events if e.get("protocol")=="M3_SHADOW_ORDER_V1"]
    quotes=collections.defaultdict(list)
    for e in events:
        if e.get("protocol")=="M3_TOTALCORNER_PRICE_SNAPSHOT_V1":
            if e.get("provider")=="TotalCorner" and e.get("bookmaker")=="totalcorner_default_NOT_CROWN":
                quotes[(str(e.get("totalcorner_match_id")),e.get("market"),e.get("side"))].append(e)
    for rows in quotes.values():rows.sort(key=lambda e:e.get("captured_at_utc",""))
    results={}
    for model in ("poisson","dixon_coles","bivariate_poisson"):
        results[model]={}
        for market in ("AH","OU"):
            selected=[o for o in orders if o.get("model")==model and o.get("market")==market]
            counts=collections.Counter();changes=[];examples=[]
            for o in selected:
                try:
                    start=timestamp(o["quote_snapshot_recorded_utc"])
                    decision=max(start,timestamp(o["forecasted_at_utc"]))
                    kickoff=timestamp(o["kickoff_utc_verified"])
                    opening=float(o["decimal_odd"])
                except (KeyError,TypeError,ValueError):
                    counts["INVALID_ORIGINAL_QUOTE"]+=1;continue
                if decision>=kickoff or opening<=1:
                    counts["INVALID_ORDER_TIME"]+=1;continue
                subsequent=[]
                moved_line=False
                for q in quotes[(str(o.get("totalcorner_match_id")),market,o.get("side"))]:
                    try:
                        t=timestamp(q["captured_at_utc"])
                        if not decision<t<kickoff:continue
                        if abs(float(q["line"])-float(o["line"]))>1e-8:
                            moved_line=True;continue
                        odd=float(q["decimal_odd"])
                        if odd>1:subsequent.append((t,odd))
                    except (ValueError,TypeError,KeyError):continue
                if not subsequent:
                    counts["LINE_CHANGED_NO_COMPARABLE_QUOTE" if moved_line else "NO_LATER_COMPARABLE_QUOTE"]+=1
                    continue
                t,latest=max(subsequent)
                delta=round(latest-opening,6)
                state="SHORTENED" if delta< -1e-9 else "DRIFTED" if delta>1e-9 else "UNCHANGED"
                counts[state]+=1;changes.append(delta)
                if len(examples)<3:examples.append({"order_event_id":o["event_id"],"opening_odd":opening,"latest_odd":latest,"change":delta,"latest_utc":t.isoformat()})
            n=len(changes)
            results[model][market]={"orders":len(selected),"counts":dict(counts),
                "comparable_orders":n,"shortening_rate_percent":round(100*counts["SHORTENED"]/n,4) if n else None,
                "average_odds_change":round(sum(changes)/n,6) if n else None,
                "sample_audit_examples":examples}
    return {"protocol":"M3_ORDER_WATER_MOVEMENT_AUDIT_V1","scope":"SHADOW ONLY, TotalCorner default NOT Crown",
        "definition":"Latest recorded same-side same-line quote after decision and before kickoff; no snapshot is not unchanged; line moves are excluded",
        "note":"Repeated models and forecasts may share one market observation; do not treat all orders as independent prices. Sparse snapshots may miss intermediate changes.",
        "models":results}
def main():
    p=argparse.ArgumentParser();p.add_argument("--ledger",type=Path,required=True);p.add_argument("--output",type=Path,required=True);a=p.parse_args()
    result=audit([json.loads(s) for s in a.ledger.open() if s.strip()])
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps(result["models"],ensure_ascii=False))
if __name__=="__main__":main()
