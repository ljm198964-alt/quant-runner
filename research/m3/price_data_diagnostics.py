"""Audit M3 source event coverage without exposing or rewriting the ledger."""
import argparse,collections,json
from pathlib import Path
from research.m3.price_dislocation_prediction import build
def audit(events):
    c=collections.Counter(e.get("protocol") for e in events)
    forecasts={e.get("forecast_id"):e for e in events if e.get("protocol")=="M3_TOTALCORNER_FORWARD_FORECAST_V1"}
    reasons=collections.Counter()
    quotes=[e for e in events if e.get("protocol")=="M3_TOTALCORNER_FORWARD_EV_V1"]
    from research.m3.price_dislocation_prediction import utc
    for q in quotes:
        f=forecasts.get(q.get("forecast_id"))
        if not f:
            reasons["no_matching_forecast"]+=1;continue
        if not q.get("bookmaker") or not q.get("quote_snapshot_recorded_utc"):
            reasons["missing_bookmaker_or_timestamp"]+=1;continue
        if not f.get("kickoff_utc_verified") or not f.get("forecasted_at_utc"):
            reasons["missing_forecast_timestamps"]+=1;continue
        try:
            if utc(f["kickoff_utc_verified"])<=max(utc(f["forecasted_at_utc"]),utc(q["quote_snapshot_recorded_utc"])):
                reasons["kickoff_not_future"]+=1;continue
        except (TypeError,ValueError):
            reasons["invalid_timestamps"]+=1;continue
        reasons["eligible_time_join"]+=1
    rows=build(events)
    return {"event_counts":dict(c),"quote_diagnostics":dict(reasons),
            "paired_feature_rows":len(rows),
            "observed_labels":{str(h):sum(r["labels"][str(h)]["status"]=="OBSERVED" for r in rows) for h in (5,15,30,45)}}
def main():
    p=argparse.ArgumentParser();p.add_argument("--ledger",required=True,type=Path);p.add_argument("--output",required=True,type=Path);a=p.parse_args()
    result=audit([json.loads(s) for s in a.ledger.open() if s.strip()])
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps(result,ensure_ascii=False))
if __name__=="__main__":main()
