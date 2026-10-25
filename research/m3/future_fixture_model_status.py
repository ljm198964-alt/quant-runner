"""Append per-fixture screening disposition without classifying unscored matches invalid."""
import argparse, collections, hashlib, json
from pathlib import Path

LEAGUE_NAMES={'Germany Bundesliga I','England Premier League','France Ligue 1',
              'Italy Serie A','Spain La Liga'}
def fixture_id(mid):
    return hashlib.sha256(json.dumps(['M3_TOTALCORNER_FIXTURE_V1',str(mid)],ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def generate(events,run_id):
    seen={e['event_id'] for e in events}
    forecast_ids={e['fixture_identity_id'] for e in events
                  if e.get('protocol')=='M3_TOTALCORNER_FORWARD_FORECAST_V1' and e.get('run_id')==run_id}
    results=[];counts=collections.Counter()
    for i in events:
        if i.get('protocol')!='M3_TOTALCORNER_FUTURE_INVENTORY_V1' or i.get('run_id')!=run_id:continue
        if i['timing_state']!='TIME_QUALIFIED':reason='NOT_TIME_QUALIFIED'
        elif i['league_source'] not in LEAGUE_NAMES:reason='NO_HISTORICAL_TRAINING_LEAGUE'
        elif fixture_id(i['totalcorner_match_id']) not in forecast_ids:reason='NO_MODEL_FORECAST_HISTORICAL_TEAM_OR_FIT'
        else:reason='MODEL_FORECAST_RECORDED'
        rid=hashlib.sha256(json.dumps(['M3_FUTURE_MODEL_STATUS_V1',i['event_id']],separators=(',',':')).encode()).hexdigest()
        if rid in seen:continue
        results.append({'event_id':rid,'protocol':'M3_FUTURE_MODEL_STATUS_V1','inventory_event_id':i['event_id'],
                        'totalcorner_match_id':i['totalcorner_match_id'],'run_id':run_id,'model_stage':reason,
                        'formal_order':False,'telegram_sent':False})
        counts[reason]+=1
    return results,dict(counts)

def main():
    p=argparse.ArgumentParser();p.add_argument('--ledger',type=Path,required=True);p.add_argument('--run-id',required=True);a=p.parse_args()
    rows=[json.loads(x) for x in a.ledger.read_text().splitlines() if x.strip()]
    fresh,counts=generate(rows,a.run_id)
    with a.ledger.open('a') as f:
        for e in fresh:f.write(json.dumps(e,ensure_ascii=False,sort_keys=True)+'\n')
    print(json.dumps({'status':'COMPLETED','added':len(fresh),'model_stage_counts':counts}))
if __name__=='__main__':main()
