#!/usr/bin/env python3
"""M2 market-plus-form calibration: strict chronological research gate.

AH and OU are audited separately. No model is promoted or traded when sample
support is inadequate. Pure Crown market is the mandatory baseline. No use of
post-event features or future quotes in a prediction row.

The narrow initial target is directional win-vs-loss for non-push Asian contracts.
This is NOT a full Asian five-state pricing model; quarter-lines, pushes and ROI
are explicitly not certified by this preliminary experiment.
"""
from __future__ import annotations
import argparse
import json
import math
from pathlib import Path

MIN_TRAIN = 160
MIN_TEST = 80
MIN_UNIQUE_FIXTURES = 150
MAX_MISSING_RATE = 0.25
FEATURES = ("m1_goal_total","m1_goal_diff","form_diff_home5","form_diff_away5",
            "form_diff_home20","form_diff_away20")

def sigmoid(x):
    if x>=0:
        z=math.exp(-min(x,700))
        return 1/(1+z)
    z=math.exp(max(x,-700))
    return z/(1+z)

def logit(p):
    x=max(1e-5,min(1-1e-5,float(p)))
    return math.log(x/(1-x))

def target(row):
    """Exclude unresolved quarter-ball outcomes and pushes from binary diagnostic."""
    if row["market"]=="AH":
        # first Asian quote corresponds to home team with line applying to home
        m=int(row["ft_home"])-int(row["ft_away"])
        v=m+float(row["market_line"])
    elif row["market"]=="OU":
        v=int(row["ft_home"])+int(row["ft_away"])-float(row["market_line"])
    else:return None
    if abs(v)<=1e-9:return None
    # Asian quarter split can yield half-result. Discard such examples here.
    q=round(4*float(row["market_line"]))
    if abs(q/4-float(row["market_line"]))>1e-9:return None
    if q%2!=0 and abs(v)<=0.25+1e-9:return None
    return int(v>0)

def bce(p,y):
    p=max(1e-7,min(1-1e-7,p))
    return -y*math.log(p)-(1-y)*math.log(1-p)

def diagnostics(rows):
    by_market={}
    for market in ("AH","OU"):
        sample=sorted((r for r in rows if r.get("market")==market),key=lambda r:r["asof"])
        unique=len({r["fixture_id"] for r in sample})
        labeled=[(r,target(r)) for r in sample]
        labeled=[(r,y) for r,y in labeled if y is not None]
        with_features=[(r,y) for r,y in labeled
                       if all(isinstance(r.get(f),(int,float)) and math.isfinite(float(r[f])) for f in FEATURES)]
        status="INSUFFICIENT_PREDECLARED_SAMPLE"
        if len(with_features)>=MIN_TRAIN+MIN_TEST and unique>=MIN_UNIQUE_FIXTURES:
            status="FUTURE_WALK_FORWARD_READY_NOT_PROMOTED"
        base_bce=sum(bce(r["crown_no_vig_first"],y) for r,y in labeled)/len(labeled) if labeled else None
        by_market[market]={
          "raw_rows":len(sample),"unique_fixtures":unique,
          "binary_labeled_after_push_quarter_exclusions":len(labeled),
          "complete_fundamentals":len(with_features),
          "binary_crown_market_log_loss_descriptive":base_bce,
          "status":status,
          "minimum_train":MIN_TRAIN,"minimum_future_test":MIN_TEST,
          "minimum_unique_fixtures":MIN_UNIQUE_FIXTURES,
          "caveat":"Binary directional diagnostic, not Asian-payoff EV, ROI, or trained M2."
        }
    return by_market

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--audited-dataset",required=True)
    args=p.parse_args()
    d=json.loads(Path(args.audited_dataset).read_text(encoding="utf-8"))
    if d.get("protocol")!="M2_VERIFIED_CROWN_TWO_SIDED_DATASET_V1":
        raise ValueError("Unsupported audited dataset")
    result={"protocol":"M2_FUSION_RESEARCH_GATE_V1",
      "dataset_rows":len(d["rows"]),"market_diagnostics":diagnostics(d["rows"]),
      "trained_model_saved":False,"forward_m2_orders":0,
      "roi_claim":None,
      "limitations":["No threshold optimization on holdout",
          "Asian quarter and push payout model remains untrained",
          "Historical feature missingness and team/league shift require audit"]}
    print(json.dumps(result,ensure_ascii=False))

if __name__=="__main__":main()
