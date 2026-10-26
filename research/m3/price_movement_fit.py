"""Time-ordered, strictly out-of-sample M3 odds-shortening baseline.

Fit only on past observed labels; missing outcomes never count as losses.
No new production gate and no Telegram output.
"""
import argparse
import collections
import json
import math
from datetime import datetime
from pathlib import Path

HORIZONS=(5,15,30,45)
def timestamp(s):
    return datetime.fromisoformat(s.replace("Z","+00:00"))

def features(r):
    return (float(r["model_expected_unit_return"]),
            float(r["minutes_to_kickoff"]),
            float(r["decimal_odd"]))

def predict(train,x):
    # Transparent Laplace-smoothed empirical prior with nearest-neighbor
    # adjustment; does not claim a calibrated probability without validation.
    ranked=sorted(train,key=lambda z:
        abs(z[0][0]-x[0])/0.2+
        abs(z[0][1]-x[1])/120+
        abs(z[0][2]-x[2])/0.2)
    nearest=ranked[:min(50,len(ranked))]
    p=(1+sum(y for _,y,_ in nearest))/(2+len(nearest))
    change=sum(delta for _,_,delta in nearest)/len(nearest)
    return p,change,len(nearest)

def evaluate(data,min_train=20):
    ordered=sorted(data,key=lambda r:timestamp(r["observed_at_utc"]))
    results=[]
    for horizon in HORIZONS:
        training=[]
        predictions=[]
        # Group timestamps: no same-time label can train on another
        # prediction from that instant.
        groups=collections.defaultdict(list)
        for r in ordered:
            groups[r["observed_at_utc"]].append(r)
        for t,items in sorted(groups.items(),key=lambda kv:timestamp(kv[0])):
            now=timestamp(t)
            eligible=[z for z in training if z[3]<now]
            for r in items:
                label=r["labels"][str(horizon)]
                if label["status"]!="OBSERVED":
                    continue
                x=features(r)
                subset=[(z[0],z[1],z[2]) for z in eligible
                        if z[4]==r["model"] and z[5]==r["market"]]
                if len(subset)<min_train:
                    continue
                prob,delta,n=predict(subset,x)
                predictions.append({
                    "forecast_id":r["forecast_id"],"model":r["model"],
                    "match_id":r["match_id"],"market":r["market"],"side":r["side"],
                    "quote_event_id":r["quote_event_id"],
                    "observed_at_utc":t,"horizon_minutes":horizon,
                    "probability_shortening":round(prob,6),
                    "predicted_odds_change":round(delta,6),
                    "actual_odds_change":label["odds_change"],
                    "actual_shortening":label["odds_shortened"],
                    "train_rows":n,"research_only":True
                })
            for r in items:
                label=r["labels"][str(horizon)]
                if label["status"]=="OBSERVED":
                    training.append((*features(r),))
                    # Store target availability time to prevent future-label leakage.
                    training[-1]=(features(r),int(label["odds_shortened"]),
                                  float(label["odds_change"]),
                                  timestamp(label["future_quote_utc"]),r["model"],r["market"])
        n=len(predictions)
        results.append({
            "horizon_minutes":horizon,"evaluated_predictions":n,
            "brier_score":round(sum((z["probability_shortening"]-int(z["actual_shortening"]))**2 for z in predictions)/n,6) if n else None,
            "baseline_brier_score":round(sum((0.5-int(z["actual_shortening"]))**2 for z in predictions)/n,6) if n else None,
            "mean_absolute_odds_error":round(sum(abs(z["predicted_odds_change"]-z["actual_odds_change"]) for z in predictions)/n,6) if n else None,
            "predictions":predictions
        })
    return results

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--dataset",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    p.add_argument("--min-train",type=int,default=20)
    a=p.parse_args()
    data=json.loads(a.dataset.read_text())["data"]
    report=evaluate(data,a.min_train)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps({
        "protocol":"M3_PRICE_MOVEMENT_WALK_FORWARD_V1",
        "method":"past-label-only nearest historical analog; grouped by model and market",
        "minimum_training_rows":a.min_train,
        "horizons":[{"horizon_minutes":x["horizon_minutes"],
                     "evaluated_predictions":x["evaluated_predictions"],
                     "brier_score":x["brier_score"],
                     "baseline_brier_score":x["baseline_brier_score"],
                     "mean_absolute_odds_error":x["mean_absolute_odds_error"]}
                    for x in report],
        "predictions":[z for x in report for z in x["predictions"]]
    },ensure_ascii=False,indent=2)+"\n")
    print(json.dumps([{"horizon":x["horizon_minutes"],"evaluated":x["evaluated_predictions"],
                       "brier":x["brier_score"]} for x in report]))
if __name__=="__main__":
    main()
