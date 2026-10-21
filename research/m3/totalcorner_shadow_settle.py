"""Append research-only FT outcome marks for M3 forward quote candidates; no claimed betting ROI."""
import argparse,datetime,hashlib,json
from pathlib import Path
from research.m3.openfootball_shadow import read_openfootball
from research.m3.probabilities import settle_score

def main():
    p=argparse.ArgumentParser();p.add_argument('--input-root',required=True,type=Path);p.add_argument('--ledger',required=True,type=Path);a=p.parse_args()
    if not a.ledger.exists():
        print(json.dumps({'status':'NO_FORWARD_QUOTE_LEDGER','settlements_added':0}));return
    events=[json.loads(x) for x in a.ledger.read_text().splitlines() if x.strip()]
    existing={x.get('event_id') for x in events}
    results,_,_,_=read_openfootball(a.input_root)
    finished={r['fixture_identity_id']:r for r in results.to_dict('records')}
    new=[]
    for e in events:
        if e.get('protocol')!='M3_TOTALCORNER_FORWARD_EV_V1':continue
        result=finished.get(e['fixture_identity_id'])
        if result is None:continue
        # No result before fixture calendar date; no event before its forecast.
        if result['match_date_utc'].strftime('%Y-%m-%d')<e['source_fixture_date']:continue
        if datetime.date.fromisoformat(e['source_fixture_date']) >= datetime.datetime.now(datetime.timezone.utc).date():continue
        h,a_goals=int(result['home_goals']),int(result['away_goals'])
        state,unit=settle_score(e['market'],e['line'],e['side'],h,a_goals,e['decimal_odd'])
        event_id=hashlib.sha256(('M3_RESULT_OBSERVED_V1:'+e['event_id']).encode()).hexdigest()
        if event_id in existing:continue
        new.append({'event_id':event_id,'protocol':'M3_TOTALCORNER_FORWARD_SETTLEMENT_V1',
            'candidate_event_id':e['event_id'],'forecast_id':e['forecast_id'],
            'fixture_identity_id':e['fixture_identity_id'],'home_goals':h,'away_goals':a_goals,
            'market':e['market'],'side':e['side'],'line':e['line'],
            'hypothetical_unit_return':unit,'settlement_state':state,
            'actual_bet_placed':False,'formal_order':False,'telegram_sent':False,
            'result_source':'openfootball/football.json','observed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()})
        existing.add(event_id)
    with a.ledger.open('a') as out:
        for e in new:out.write(json.dumps(e,sort_keys=True,ensure_ascii=False)+'\n')
    print(json.dumps({'status':'COMPLETED','settlements_added':len(new),'formal_bets':0,'realized_formal_roi':None}))
if __name__=='__main__':main()
