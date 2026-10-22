"""M3 shadow-only version registry: pre-registered candidate family, chronological OOS gates, rollback.

Never changes production or Telegram. A decision is made only from post-registration
settlements. Evaluation is paired on the same distinct fixture and model.
"""
from __future__ import annotations
import argparse,datetime,json,math
from pathlib import Path
from research.m3.evolution_candidates import probabilities,scores,MODEL_NAMES

CANDIDATES={}
MIN_FIXTURES=100
MIN_DATES=20

def report(events,registered_at,prior=None):
    cutoff=datetime.datetime.fromisoformat(registered_at.replace("Z","+00:00"))
    forecasts={f["forecast_id"]:f for f in events if f.get("protocol")=="M3_TOTALCORNER_FORWARD_FORECAST_V1"}
    fixture_index={}
    for e in events:
        if e.get("protocol")!="M3_TOTALCORNER_FORWARD_SETTLEMENT_V1":continue
        f=forecasts.get(e.get("forecast_id"))
        if not f or f.get("model") not in MODEL_NAMES:continue
        at=datetime.datetime.fromisoformat(f["forecasted_at_utc"].replace("Z","+00:00"))
        if at<=cutoff:continue
        key=(f["model"],f["fixture_identity_id"])
        if key not in fixture_index or f["forecasted_at_utc"]<fixture_index[key][0]["forecasted_at_utc"]:
            fixture_index[key]=(f,e)
    state={}
    for model in MODEL_NAMES:
        observations=[]
        for (name,_),(f,e) in fixture_index.items():
            if name!=model:continue
            try:
                p=probabilities(f["score_probability_grid"])
                baseline=scores(p,int(e["home_goals"]),int(e["away_goals"]))
                variants={key:scores(tuple((1-shrink)*x+shrink/3 for x in p),int(e["home_goals"]),int(e["away_goals"])) for key,shrink in CANDIDATES.items()}
                observations.append((f["source_fixture_date"],baseline,variants))
            except (KeyError,ValueError,IndexError,TypeError,ZeroDivisionError):continue
        observations.sort(key=lambda x:x[0])
        count=len(observations);days=len({a[0] for a in observations})
        results={}
        for key in CANDIDATES:
            halves=[observations[:count//2],observations[count//2:]]
            improvements=[{"logloss":(sum(o[1][0]-o[2][key][0] for o in half)/len(half) if half else None),
                           "brier":(sum(o[1][1]-o[2][key][1] for o in half)/len(half) if half else None)} for half in halves]
            passed=count>=MIN_FIXTURES and days>=MIN_DATES and all(
                x["logloss"] is not None and x["logloss"]>=0.01 and x["brier"]>=0.005 for x in improvements)
            results[key]={"paired_fixtures":count,"dates":days,"half_improvements":improvements,"passed":passed}
        # Hold active baseline when no adequate evidence; shadow version state can be rolled back.
        previous=((prior or {}).get("models") or {}).get(model,{})
        current=previous.get("shadow_active","baseline")
        eligible=[k for k,v in results.items() if v["passed"]]
        if current!="baseline" and current not in eligible:
            selected="baseline";decision="ROLLBACK_TO_BASELINE"
        elif current=="baseline" and eligible:
            selected=max(eligible,key=lambda k:min(x["logloss"] for x in results[k]["half_improvements"]))
            decision="PROMOTE_SHADOW_ONLY"
        else:
            selected=current;decision="HOLD"
        state[model]={"observations":count,"distinct_dates":days,"candidates":results,
                      "shadow_active":selected,"previous_shadow_active":current,"decision":decision}
    return {"protocol":"M3_SHADOW_EVOLUTION_REGISTRY_V1","registered_at_utc":registered_at,
            "generated_at_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "models":state,"tg_changed":False,"production_changed":False,
            "scope":"shadow_calibration_selection_only"}
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--ledger",type=Path,required=True)
    p.add_argument("--registration",type=Path,required=True)
    p.add_argument("--state",type=Path,required=True)
    a=p.parse_args()
    reg=json.loads(a.registration.read_text())
    prior=json.loads(a.state.read_text()) if a.state.exists() else {}
    events=[json.loads(x) for x in a.ledger.read_text().splitlines() if x.strip()]
    result=report(events,reg["registered_at_utc"],prior)
    a.state.parent.mkdir(parents=True,exist_ok=True)
    a.state.write_text(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+"\n")
    print(json.dumps({"status":"COMPLETED","model_decisions":{k:(v["decision"],v["shadow_active"],v["observations"]) for k,v in result["models"].items()},"production_changed":False}))
if __name__=="__main__":main()
