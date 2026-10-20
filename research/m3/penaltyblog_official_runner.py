"""M3 independent penaltyblog model runner using original documented model API.

Input: independent M3 CSV with Date, HomeTeam, AwayTeam, FTHG, FTAG.
No M1/M2/MR1 imports; no Crown substitution; no Telegram or signal gates.
"""
import argparse
import json
from pathlib import Path
import pandas as pd
from penaltyblog.models import PoissonGoalsModel, DixonColesGoalModel

def fit_and_predict(csv_path, home, away, model_name):
    df=pd.read_csv(csv_path)
    missing=[c for c in ("HomeTeam","AwayTeam","FTHG","FTAG") if c not in df]
    if missing:raise ValueError("Missing original match columns: "+",".join(missing))
    df=df.dropna(subset=("HomeTeam","AwayTeam","FTHG","FTAG"))
    cls={"poisson":PoissonGoalsModel,"dixon-coles":DixonColesGoalModel}[model_name]
    model=cls(df["FTHG"],df["FTAG"],df["HomeTeam"],df["AwayTeam"])
    model.fit()
    pred=model.predict(home,away)
    return {
       "protocol":"M3_UPSTREAM_PENALTYBLOG_MODEL_V1",
       "model_identity":"M3", "model_type":model_name,
       "source":"penaltyblog official fit/predict API",
       "training_rows":len(df),
       "fixture":{"home":home,"away":away},
       "home_draw_away":[float(x) for x in pred.home_draw_away],
       "ah_home_minus_0_5":float(pred.asian_handicap("home",-0.5)),
       "ou_over_2_5":float(pred.total_goals("over",2.5)),
       "research_only":True,"telegram_write":False,
       "crown_market_prices_provided":False,"roi":None}
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--csv",required=True)
    p.add_argument("--home",required=True)
    p.add_argument("--away",required=True)
    p.add_argument("--model",choices=("poisson","dixon-coles"),required=True)
    p.add_argument("--output",required=True)
    args=p.parse_args()
    result=fit_and_predict(Path(args.csv),args.home,args.away,args.model)
    out=Path(args.output);out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps(result,ensure_ascii=False))
if __name__=="__main__":main()
