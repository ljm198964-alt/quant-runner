"""M3 independent walk-forward performance gate. No autonomous deployment or wagers."""
from __future__ import annotations
import argparse,collections,datetime,hashlib,json,math
from pathlib import Path

MIN_DISTINCT_FIXTURES=100
MIN_BETTER_LOGLOSS=0.01
MIN_BETTER_BRIER=0.005
MODEL_NAMES=('poisson','dixon_coles','bivariate_poisson')
def evaluate(events):
    forecasts={e['forecast_id']:e for e in events if e.get('protocol')=='M3_TOTALCORNER_FORWARD_FORECAST_V1'}
    settled=set()
    for e in events:
        if e.get('protocol')=='M3_TOTALCORNER_FORWARD_SETTLEMENT_V1':
            settled.add(e['forecast_id'])
    group=collections.defaultdict(dict)
    for fid in settled:
        f=forecasts.get(fid)
        if not f or f.get('model') not in MODEL_NAMES or not f.get('score_probability_grid'):continue
        key=(f.get('source_fixture_date'),f.get('fixture_identity_id'))
        group[f['model']][key]=f
    result={}
    for name in MODEL_NAMES:
        candidates=group[name]
        dates={k[0] for k in candidates}
        count=len(candidates)
        result[name]={'distinct_settled_fixtures':count,'distinct_fixture_dates':len(dates),
            'status':'INSUFFICIENT_OUT_OF_SAMPLE_RESULTS' if count<MIN_DISTINCT_FIXTURES else 'ELIGIBLE_FOR_SCORING',
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
