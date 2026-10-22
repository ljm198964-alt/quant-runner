"""Pre-register immutable M3 calibration candidates; compare only later independent fixtures.

Candidate V1 is a fixed 10% shrink of predicted 1X2 probability toward equal thirds.
This is a research challenger, not a strategy or production change.
"""
from __future__ import annotations
import argparse,datetime,hashlib,json,math
from pathlib import Path

UTC=datetime.timezone.utc
MODEL_NAMES=('poisson','dixon_coles','bivariate_poisson')
def probabilities(grid):
    mass=sum(sum(row) for row in grid)
    if not 0.999<=mass<=1.001:raise ValueError('invalid probability grid')
    h=sum(v for i,row in enumerate(grid) for j,v in enumerate(row) if i>j)/mass
    d=sum(row[i] for i,row in enumerate(grid) if i<len(row))/mass
    return (h,d,max(0.,1-h-d))
def scores(pred,home,away):
    index=0 if home>away else 1 if home==away else 2
    return (-math.log(max(pred[index],1e-12)),sum((v-int(i==index))**2 for i,v in enumerate(pred)))
def validate(events,registration):
    if registration.get('protocol')!='M3_CANDIDATE_REGISTRATION_V1':raise ValueError('invalid registration')
    cutoff=datetime.datetime.fromisoformat(registration['registered_at_utc'].replace('Z','+00:00'))
    forecasts={e['forecast_id']:e for e in events if e.get('protocol')=='M3_TOTALCORNER_FORWARD_FORECAST_V1'}
    fixtures={}
    for e in events:
        if e.get('protocol')!='M3_TOTALCORNER_FORWARD_SETTLEMENT_V1':continue
        f=forecasts.get(e.get('forecast_id'))
        if not f or f.get('model') not in MODEL_NAMES:continue
        if datetime.datetime.fromisoformat(f['forecasted_at_utc'].replace('Z','+00:00'))<=cutoff:continue
        key=(f.get('model'),f.get('fixture_identity_id'))
        if key not in fixtures or f['forecasted_at_utc']<fixtures[key][0]['forecasted_at_utc']:
            fixtures[key]=(f,e)
    outcome={}
    for name in MODEL_NAMES:
        pairs=[]
        for (model,_), (f,e) in fixtures.items():
            if model!=name:continue
            try:
                base=probabilities(f['score_probability_grid'])
                candidate=tuple(.9*p+.1/3 for p in base)
                a=scores(base,e['home_goals'],e['away_goals'])
                b=scores(candidate,e['home_goals'],e['away_goals'])
                pairs.append((f['source_fixture_date'],a,b))
            except (ValueError,KeyError,TypeError):continue
        pairs.sort(key=lambda x:x[0])
        # Two chronologically separated halves to reject transient improvements.
        n=len(pairs)
        halves=[pairs[:n//2],pairs[n//2:]]
        def diff(chunk,index):
            return sum(a[index]-b[index] for _,a,b in chunk)/len(chunk) if chunk else None
        improvements=[{'logloss':diff(x,0),'brier':diff(x,1)} for x in halves]
        pass_gate=(bool(pairs) and
                   all(v['logloss'] is not None and v['logloss']>=.01 and v['brier']>=.005 for v in improvements))
        outcome[name]={'settled_unique_fixtures_after_registration':n,'distinct_dates':len({x[0] for x in pairs}),
                       'chronological_half_improvements':improvements,
                       'candidate_status':'EVIDENCE_PASSED_REVIEW_ONLY' if pass_gate else 'HOLD_NOT_PROMOTED',
                       'promotion_authorized':False}
    return {'protocol':'M3_CHALLENGER_OOS_EVALUATION_V1','registration':registration,'models':outcome,
            'production_changed':False,'telegram_sent':False}
def main():
    p=argparse.ArgumentParser()
    p.add_argument('--ledger',type=Path,required=True)
    p.add_argument('--registration',type=Path,required=True)
    p.add_argument('--report',type=Path,required=True)
    a=p.parse_args()
    reg=json.loads(a.registration.read_text())
    events=[json.loads(x) for x in a.ledger.read_text().splitlines() if x.strip()]
    result=validate(events,reg)
    a.report.parent.mkdir(parents=True,exist_ok=True)
    a.report.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'protocol':result['protocol'],'summary':{k:v['candidate_status'] for k,v in result['models'].items()},'production_changed':False}))
if __name__=='__main__':main()
