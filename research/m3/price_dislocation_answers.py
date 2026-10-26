"""Produce actionable research-only M3 answers from contemporaneous model/quote data.

This is a baseline candidate generator, not a trained odds-movement forecaster.
Every eligible model/market pair yields one answer; no EV threshold is applied.
"""
import argparse
import collections
import json
from pathlib import Path

def build(dataset):
    rows=dataset["data"]
    by_group=collections.defaultdict(list)
    for r in rows:
        key=(r["forecast_id"],r["market"])
        by_group[key].append(r)
    answers=[]
    for (fid,market),candidates in sorted(by_group.items()):
        sides={"home","away"} if market=="AH" else {"over","under"}
        if {r["side"] for r in candidates}!=sides or len(candidates)!=2:
            continue
        # This is an existing model-price dislocation baseline, NOT an
        # empirically fitted probability of future shortening.
        chosen=max(candidates,key=lambda r:(r["model_expected_unit_return"],r["side"]))
        answers.append({
            "protocol":"M3_PRICE_DISLOCATION_RESEARCH_ANSWER_V1",
            "forecast_id":fid,"model":chosen["model"],
            "fixture_identity_id":chosen["fixture_identity_id"],
            "match_id":chosen["match_id"],
            "market":market,"side":chosen["side"],"line":chosen["line"],
            "current_decimal_odd":chosen["decimal_odd"],
            "observed_at_utc":chosen["observed_at_utc"],
            "kickoff_utc":chosen["kickoff_utc"],
            "bookmaker":chosen["bookmaker"],
            "model_expected_unit_return":chosen["model_expected_unit_return"],
            "model_fair_decimal_odd_if_linear":chosen["model_fair_decimal_odd_if_linear"],
            "forecast_future_odds_shortening_probability":None,
            "forecast_future_odds_change":None,
            "prediction_status":"BASELINE_CANDIDATE_NOT_TRAINED",
            "basis":"MODEL_PRICE_DISLOCATION_NO_EV_GATE",
            "research_only":True,"formal_order":False,"telegram_sent":False
        })
    return answers

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--dataset",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()
    answers=build(json.loads(a.dataset.read_text()))
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps({
        "protocol":"M3_PRICE_DISLOCATION_ANSWERS_V1",
        "note":"Candidate directions, NOT trained price forecasts or formal orders",
        "count":len(answers),"answers":answers
    },ensure_ascii=False,indent=2)+"\n")
    print(json.dumps({"research_candidates":len(answers)}))
if __name__=="__main__":
    main()
