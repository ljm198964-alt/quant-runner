"""Locked M3 policy: one AH and one OU shadow order per forecast with both quotes.

Select the side by model-only expected settlement at neutral decimal odds 2.0.
Actual quoted EV is recorded for evaluation, NEVER used as a gate or direction selector.
"""
import argparse, collections, datetime, json
from pathlib import Path
from research.m3.totalcorner_forward_ev import calculate, hash_id

POLICY='M3_TWO_MARKET_MODEL_DIRECTION_V1'

def slot_for(timestamp):
    """Assign retries to the most recent Beijing 06:00 or 12:00 slot."""
    dt=datetime.datetime.fromisoformat(str(timestamp).replace('Z','+00:00'))
    if dt.tzinfo is None:
        raise ValueError('naive forecast timestamp')
    local=dt.astimezone(datetime.timezone(datetime.timedelta(hours=8)))
    if local.hour>=12:
        day,hour=local.date(),12
    elif local.hour>=6:
        day,hour=local.date(),6
    else:
        day,hour=local.date()-datetime.timedelta(days=1),12
    return f'{day.isoformat()}T{hour:02d}:00+08:00'

def order_identity(event):
    if event.get('protocol')!='M3_SHADOW_ORDER_V1':
        return None
    return (slot_for(event['forecasted_at_utc']),
            str(event['fixture_identity_id']),event['model'],event['market'])


def choose(forecast, market, quotes):
    matrix=forecast['score_probability_grid']
    line=quotes[0]['line']
    assert all(q['line']==line for q in quotes)
    sides=('home','away') if market=='AH' else ('over','under')
    scores={side:calculate(matrix,market,line,side,2.0) for side in sides}
    selected=max(sides,key=lambda side:(scores[side],-sides.index(side)))
    return next(q for q in quotes if q['side']==selected),scores

def build(events,run_id=None):
    forecasts={e['forecast_id']:e for e in events if e.get('protocol')=='M3_TOTALCORNER_FORWARD_FORECAST_V1' and (run_id is None or e.get('run_id')==run_id)}
    quotes=collections.defaultdict(list)
    for e in events:
        if e.get('protocol')=='M3_TOTALCORNER_FORWARD_EV_V1' and e.get('forecast_id') in forecasts:
            quotes[(e['forecast_id'],e['market'])].append(e)
    existing={e.get('event_id') for e in events}
    existing_orders={order_identity(e) for e in events if e.get('protocol')=='M3_SHADOW_ORDER_V1'}
    added=[];missing=collections.Counter()
    for fid,f in forecasts.items():
        for market in ('AH','OU'):
            qs=quotes.get((fid,market),[])
            if len(qs)!=2 or {q['side'] for q in qs}!=({'home','away'} if market=='AH' else {'over','under'}):
                missing[market]+=1;continue
            selected,scores=choose(f,market,qs)
            eid=hash_id([POLICY,fid,market])
            identity=(slot_for(f['forecasted_at_utc']),str(f['fixture_identity_id']),f['model'],market)
            if eid in existing or identity in existing_orders:continue
            added.append({'protocol':'M3_SHADOW_ORDER_V1','policy_version':POLICY,'event_id':eid,
                'run_id':f['run_id'],'forecast_id':fid,'fixture_identity_id':f['fixture_identity_id'],
                'totalcorner_match_id':selected['totalcorner_match_id'],'home_team':f['home_team'],'away_team':f['away_team'],
                'kickoff_utc_verified':f['kickoff_utc_verified'],'model':f['model'],
                'market':market,'side':selected['side'],'line':selected['line'],
                'decimal_odd':selected['decimal_odd'],'expected_unit_return':selected['expected_unit_return'],
                'model_direction_scores_neutral_odds':scores,'quote_snapshot_recorded_utc':selected['quote_snapshot_recorded_utc'],
                'forecasted_at_utc':f['forecasted_at_utc'],'selection_basis':'MODEL_ONLY_NEUTRAL_ODDS_2_NO_EV_GATE',
                'selection_provenance':'RETROSPECTIVE_RECONSTRUCTION' if run_id is None else 'RUN_SCOPED_AFTER_FORECAST',
                'formal_order':False,'telegram_sent':False,'settled':False})
            existing.add(eid)
            existing_orders.add(identity)
    return added,dict(missing),len(forecasts)

def main():
    p=argparse.ArgumentParser();p.add_argument('--ledger',required=True,type=Path);p.add_argument('--run-id');p.add_argument('--historical-backfill',action='store_true');a=p.parse_args()
    if not a.run_id and not a.historical_backfill:p.error('supply --run-id or --historical-backfill')
    events=[json.loads(s) for s in a.ledger.read_text().splitlines() if s.strip()]
    new,missing,n=build(events,None if a.historical_backfill else a.run_id)
    with a.ledger.open('a') as out:
        for e in new:out.write(json.dumps(e,ensure_ascii=False,sort_keys=True)+'\n')
    print(json.dumps({'policy':POLICY,'forecast_count':n,'new_shadow_orders':len(new),'missing_market_quotes':missing,'historical_backfill':a.historical_backfill,'idempotency':'BEIJING_SLOT_FIXTURE_MODEL_MARKET'}))
if __name__=='__main__':main()
