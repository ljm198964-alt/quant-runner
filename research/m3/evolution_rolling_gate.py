"""Paired, chronology-locked OOS evaluation and shadow-only selection of rolling challengers."""
from __future__ import annotations
import argparse,collections,datetime,json
from pathlib import Path
from research.m3.evolution_candidates import probabilities,scores,MODEL_NAMES

def evaluate(forward,challengers,previous=None):
    base={}
    by_id={e['forecast_id']:e for e in forward if e.get('protocol')=='M3_TOTALCORNER_FORWARD_FORECAST_V1'}
    scores_by_fixture={}
    for e in forward:
        if e.get('protocol')!='M3_TOTALCORNER_FORWARD_SETTLEMENT_V1':continue
        f=by_id.get(e.get('forecast_id'))
        if not f:continue
        key=(f['model'],f['fixture_identity_id'])
        if key not in base or f['forecasted_at_utc']<base[key]['forecasted_at_utc']:
            base[key]=f
            scores_by_fixture[key]=(int(e['home_goals']),int(e['away_goals']))
    earliest={}
    for c in challengers:
        if c.get('model') not in MODEL_NAMES or c.get('train_years') not in (2,4):continue
        key=(c['model'],c['train_years'],c['fixture_id'])
        if key not in earliest or c['registered_at_utc']<earliest[key]['registered_at_utc']:earliest[key]=c
    states={}
    for model in MODEL_NAMES:
        groups={}
        for years in (2,4):
            rows=[]
            for (name,y,fixture_id),c in earliest.items():
                if name!=model or y!=years:continue
                key=(model,fixture_id)
                f=base.get(key);score=scores_by_fixture.get(key)
                if f is None or score is None or c['source_date']!=f['source_fixture_date']:continue
                # The candidate must be recorded before its fixture date and
                # the scored fixture must have occurred after registration.
                if c['source_date']<=c['registered_at_utc'][:10]:continue
                if f['forecasted_at_utc'][:10]>c['source_date']:continue
                try:
                    b=scores(probabilities(f['score_probability_grid']),*score)
                    a=scores(probabilities(c['score_grid']),*score)
                except (ValueError,IndexError,KeyError,TypeError,ZeroDivisionError):continue
                rows.append((c['source_date'],b,a))
            rows.sort(key=lambda r:r[0])
            diff={'logloss':sum(r[1][0]-r[2][0] for r in rows)/len(rows) if rows else None,
                  'brier':sum(r[1][1]-r[2][1] for r in rows)/len(rows) if rows else None}
            passed=bool(rows) and diff['logloss']>=0.01 and diff['brier']>=0.005
            groups['rolling_'+str(years)+'y']={'paired_unique_fixtures':len(rows),
                'distinct_dates':len({r[0] for r in rows}),'overall_improvement':diff,'passed':passed}
        prior=((previous or {}).get('models') or {}).get(model,{})
        current=prior.get('rolling_shadow_active','baseline')
        eligible=[k for k,v in groups.items() if v['passed']]
        if current=='baseline' and eligible:
            selected=max(eligible,key=lambda k:groups[k]['overall_improvement']['logloss'])
            decision='PROMOTE_SHADOW_ONLY'
        else:
            selected=current;decision='HOLD'
        states[model]={'rolling_shadow_active':selected,'previous_rolling_shadow_active':current,
                      'decision':decision,'candidates':groups}
    return {'protocol':'M3_ROLLING_TRAINING_OOS_REGISTRY_V1','generated_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'models':states,'production_changed':False,'telegram_sent':False}
def main():
    p=argparse.ArgumentParser()
    p.add_argument('--forward',required=True,type=Path)
    p.add_argument('--challengers',required=True,type=Path)
    p.add_argument('--registry',required=True,type=Path)
    a=p.parse_args()
    forward=[json.loads(x) for x in a.forward.read_text().splitlines() if x.strip()]
    challengers=[json.loads(x) for x in a.challengers.read_text().splitlines() if x.strip()] if a.challengers.exists() else []
    previous=json.loads(a.registry.read_text()) if a.registry.exists() else {}
    result=evaluate(forward,challengers,previous)
    a.registry.parent.mkdir(parents=True,exist_ok=True)
    a.registry.write_text(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+'\n')
    print(json.dumps({'models':{k:v['decision'] for k,v in result['models'].items()},
                      'challengers_loaded':len(challengers),'production_changed':False}))
if __name__=='__main__':main()
