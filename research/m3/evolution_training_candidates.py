"""Train independent rolling-history M3 challengers; evidence only, no promotion."""
from __future__ import annotations
import argparse,datetime,hashlib,json
from pathlib import Path
import pandas as pd
from research.m3.openfootball_shadow import read_openfootball,MODELS,_serialize_score_probability_grid

def run(root,out,asof):
    data,fixtures,_,_=read_openfootball(root)
    cutoff=pd.Timestamp(asof,tz='UTC')
    targets=[f for f in fixtures if f['source_date']>=asof][:12]
    records=[]
    registered=datetime.datetime.now(datetime.timezone.utc).isoformat()
    for league in sorted({f['league'] for f in targets}):
        matches=data.loc[(data.league==league)&(data.match_date_utc<cutoff)]
        for model_name,cls in MODELS.items():
            for years in (2,4):
                training=matches.loc[matches.match_date_utc>=cutoff-pd.Timedelta(days=years*365)]
                if training.empty:continue
                model=cls(training.home_goals,training.away_goals,training.home_team,training.away_team)
                model.fit()
                version=hashlib.sha256(json.dumps([league,model_name,years,asof,model.get_params()],sort_keys=True).encode()).hexdigest()
                known=set(map(str,model.teams))
                for f in targets:
                    if f['league']!=league or f['home_team'] not in known or f['away_team'] not in known:continue
                    records.append({'model':model_name,'train_years':years,'version':version,
                        'fixture_id':f['fixture_identity_id'],'source_date':f['source_date'],
                        'score_grid':_serialize_score_probability_grid(model.predict(f['home_team'],f['away_team'])),
                        'registered_at_utc':registered, 'training_cutoff_utc':cutoff.isoformat(),
                        'shadow_only':True,'promoted':False})
    out.parent.mkdir(parents=True,exist_ok=True)
    existing=set()
    if out.exists():
        for line in out.read_text().splitlines():
            if line.strip():
                old=json.loads(line)
                existing.add((old['model'],old['train_years'],old['version'],old['fixture_id']))
    new=[r for r in records if (r['model'],r['train_years'],r['version'],r['fixture_id']) not in existing]
    with out.open('a') as f:
        for r in new:f.write(json.dumps(r,sort_keys=True)+'\n')
    print(json.dumps({'candidate_predictions':len(records),'new_records':len(new),'no_production_change':True}))
if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--input-root',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--asof',default=datetime.datetime.now(datetime.timezone.utc).date().isoformat())
    a=p.parse_args();run(a.input_root,a.output,a.asof)
