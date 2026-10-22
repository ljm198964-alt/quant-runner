"""M3 independent walk-forward performance gate. No autonomous deployment or wagers."""
from __future__ import annotations
import argparse,collections,datetime,hashlib,json,math
from pathlib import Path

MIN_DISTINCT_FIXTURES=0
MIN_BETTER_LOGLOSS=0.01
MIN_BETTER_BRIER=0.005
MODEL_NAMES=('poisson','dixon_coles','bivariate_poisson')
def evaluate(events):
    forecasts={e['forecast_id']:e for e in events if e.get('protocol')=='M3_TOTALCORNER_FORWARD_FORECAST_V1'}
    settled={}
    for e in events:
        if e.get('protocol')=='M3_TOTALCORNER_FORWARD_SETTLEMENT_V1':
            settled.setdefault(e['forecast_id'],e)
    group=collections.defaultdict(dict)
    for fid,settlement in settled.items():
        f=forecasts.get(fid)
        if not f or f.get('model') not in MODEL_NAMES or not f.get('score_probability_grid'):continue
        key=(f.get('source_fixture_date'),f.get('fixture_identity_id'))
        if key not in group[f['model']]:group[f['model']][key]=(f,settlement)
    result={}
    for name in MODEL_NAMES:
        candidates=group[name]
        dates={k[0] for k in candidates}
        count=len(candidates)
        scored=[]
        for f,settlement in candidates.values():
            h,a=settlement.get('home_goals'),settlement.get('away_goals')
            matrix=f['score_probability_grid']
            if not isinstance(h,int) or not isinstance(a,int) or h<0 or a<0:continue
            probs=[sum(row) for row in matrix]
            p_exact=matrix[h][a] if h<len(matrix) and a<len(matrix[0]) else 0.
            p_home=sum(prob for i,row in enumerate(matrix) for j,prob in enumerate(row) if i>j)
            p_draw=sum(row[i] for i,row in enumerate(matrix) if i<len(row))
            p_away=max(0.,1.-p_home-p_draw)
            actual=(int(h>a),int(h==a),int(h<a))
            brier=sum((p-x)**2 for p,x in zip((p_home,p_draw,p_away),actual))
            categorical=(p_home,p_draw,p_away)[actual.index(1)]
            scored.append((min(20.,-math.log(max(categorical,1e-9))),brier))
        result[name]={'distinct_settled_fixtures':count,'distinct_fixture_dates':len(dates),
            'scored_fixtures':len(scored),
            'mean_1x2_logloss':round(sum(x[0] for x in scored)/len(scored),6) if scored else None,
            'mean_1x2_brier':round(sum(x[1] for x in scored)/len(scored),6) if scored else None,
            'status':'ELIGIBLE_FOR_SCORING' if scored else 'AWAITING_RESULTS',
            'automatic_promotion':False,'candidate_version':None}
    return {'protocol':'M3_CONTROLLED_EVOLUTION_V1','generated_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'minimum_independent_settled_fixtures':MIN_DISTINCT_FIXTURES,
        'required_logloss_improvement':MIN_BETTER_LOGLOSS,'required_brier_improvement':MIN_BETTER_BRIER,
        'policy':'NO_AUTO_PROMOTION_WITHOUT_PAIRED_CHRONOLOGICAL_OOS_COMPARISON',
        'models':result,'production_changes':False,'telegram_sent':False}
def main():
    p=argparse.ArgumentParser();p.add_argument('--ledger',type=Path,required=True);p.add_argument('--report',type=Path,required=True);a=p.parse_args()
    events=[json.loads(x) for x in a.ledger.read_text().splitlines() if x.strip()]
    result=evaluate(events)
    a.report.parent.mkdir(parents=True,exist_ok=True)
    a.report.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps(result,ensure_ascii=False))
if __name__=='__main__':main()
