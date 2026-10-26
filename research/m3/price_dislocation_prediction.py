"""Leakage-safe M3 model/market dislocation features and observed price labels.

Research only. No order selection, EV threshold, Telegram or Crown substitution.
"""
import argparse
import collections
import json
from datetime import datetime, timezone
from pathlib import Path

HORIZONS=(5,15,30,45)
def utc(value):
    d=datetime.fromisoformat(value.replace("Z","+00:00"))
    if d.tzinfo is None:
        raise ValueError("UTC timestamp must carry timezone")
    return d.astimezone(timezone.utc)

def build(events):
    forecasts={e["forecast_id"]:e for e in events if e.get("protocol")=="M3_TOTALCORNER_FORWARD_FORECAST_V1"}
    quotes=[e for e in events if e.get("protocol")=="M3_TOTALCORNER_FORWARD_EV_V1"
            and e.get("provider")=="TotalCorner" and e.get("bookmaker")
            and e.get("quote_snapshot_recorded_utc")]
    groups=collections.defaultdict(list)
    for q in quotes:
        key=(str(q.get("totalcorner_match_id")),q["bookmaker"],q.get("market"),str(q.get("line")),q.get("side"))
        groups[key].append(q)
    # Each unique market observation is independent of the number of model forecasts.
    times={}
    for key,items in groups.items():
        d={}
        for q in items:
            t=q["quote_snapshot_recorded_utc"]
            if t not in d:
                d[t]=q
        times[key]=sorted(d.values(),key=lambda q:utc(q["quote_snapshot_recorded_utc"]))
    out=[]
    for q in quotes:
        f=forecasts.get(q.get("forecast_id"))
        if not f or f.get("model") not in ("poisson","dixon_coles","bivariate_poisson"):
            continue
        try:
            t0=utc(q["quote_snapshot_recorded_utc"])
            ft=utc(f["forecasted_at_utc"])
            kickoff=utc(f["kickoff_utc_verified"])
            odd=float(q["decimal_odd"])
            ev=float(q["expected_unit_return"])
        except (KeyError,TypeError,ValueError):
            continue
        if odd<=1 or ft>t0 or kickoff<=t0:
            continue
        key=(str(q.get("totalcorner_match_id")),q["bookmaker"],q.get("market"),str(q.get("line")),q.get("side"))
        # The implied break-even probability and EV are calculated using
        # information available at the quote timestamp only.
        feature={
            "protocol":"M3_PRICE_DISLOCATION_PREDICTION_DATA_V1",
            "forecast_id":q["forecast_id"],"model":f["model"],
            "fixture_identity_id":f.get("fixture_identity_id"),
            "match_id":key[0],"bookmaker":key[1],"market":key[2],
            "line":key[3],"side":key[4],"quote_event_id":q.get("event_id"),
            "observed_at_utc":q["quote_snapshot_recorded_utc"],
            "kickoff_utc":f["kickoff_utc_verified"],
            "minutes_to_kickoff":round((kickoff-t0).total_seconds()/60,3),
            "decimal_odd":odd,"implied_break_even_probability":round(1/odd,8),
            "model_expected_unit_return":ev,
            "model_fair_decimal_odd_if_linear":round(odd/(1+ev),8) if 1+ev>0 else None,
            "forecast_score_grid_sha256":f.get("score_grid_sha256"),
            "research_only":True,
            "labels":{}
        }
        for horizon in HORIZONS:
            target=[]
            for later in times[key]:
                t1=utc(later["quote_snapshot_recorded_utc"])
                dt=(t1-t0).total_seconds()/60
                if horizon<=dt<=horizon+5 and t1<kickoff:
                    target.append((dt,later))
            if not target:
                feature["labels"][str(horizon)]={"status":"MISSING_OBSERVED_QUOTE"}
                continue
            dt,later=min(target,key=lambda x:x[0])
            try:
                after=float(later["decimal_odd"])
            except (ValueError,TypeError):
                feature["labels"][str(horizon)]={"status":"INVALID_OBSERVED_QUOTE"}
                continue
            feature["labels"][str(horizon)]={
                "status":"OBSERVED","future_quote_event_id":later.get("event_id"),
                "future_quote_utc":later["quote_snapshot_recorded_utc"],
                "elapsed_minutes":round(dt,3),
                "future_decimal_odd":after,
                "odds_change":round(after-odd,6),
                "odds_shortened":after<odd
            }
        out.append(feature)
    return out

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--ledger",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()
    rows=build(json.loads(s) for s in a.ledger.open() if s.strip())
    observed={str(h):sum(r["labels"][str(h)]["status"]=="OBSERVED" for r in rows) for h in HORIZONS}
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps({
        "protocol":"M3_PRICE_DISLOCATION_DATASET_V1",
        "note":"Research features and future labels, not fitted probabilities or trading signals",
        "rows":len(rows),"observed_labels_by_horizon":observed,"data":rows
    },ensure_ascii=False,indent=2)+"\n")
    print(json.dumps({"rows":len(rows),"observed_labels_by_horizon":observed}))
if __name__=="__main__":
    main()
