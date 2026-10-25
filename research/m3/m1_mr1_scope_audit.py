"""Report M3 fixture research scope from saved production M1 and MR1 rule snapshots.

Scope is not model training suitability and does not imply a bet.
"""
import argparse, collections, hashlib, json
from pathlib import Path
from research.m3.reference.m1_runtime_policy import scope_status

MR1_PATH = Path(__file__).with_name('reference') / 'mr1_competition_scope.json'

def mr1_status(league: str, spec: dict):
    text = str(league or '').lower()
    if any(str(t).lower() in text for t in spec['exclude_competition_tokens']):
        return False
    return any(str(t).lower() in text for t in spec['include_country_tokens'])

def classify(league, home, away, spec):
    m1 = scope_status(league,home=home,away=away)['status']=='IN'
    mr1 = mr1_status(league,spec)
    return m1,mr1, ('M1_AND_MR1' if m1 and mr1 else 'M1' if m1 else 'MR1' if mr1 else 'OUT_OF_EXISTING_SCOPE')

def main():
    p=argparse.ArgumentParser();p.add_argument('--ledger',type=Path,required=True);p.add_argument('--run-id',required=True);a=p.parse_args()
    spec=json.loads(MR1_PATH.read_text())
    events=[json.loads(line) for line in a.ledger.open() if line.strip()]
    present={e.get('event_id') for e in events}
    rows=[];counts=collections.Counter()
    for e in events:
        if e.get('protocol')!='M3_TOTALCORNER_FUTURE_INVENTORY_V1' or e.get('run_id')!=a.run_id:continue
        m1,mr1,group=classify(e['league_source'],e['home_source'],e['away_source'],spec)
        event_id=hashlib.sha256(json.dumps(['M3_M1_MR1_SCOPE_V1',e['event_id']],separators=(',',':')).encode()).hexdigest()
        if event_id in present:continue
        rows.append({'protocol':'M3_M1_MR1_SCOPE_V1','event_id':event_id,'inventory_event_id':e['event_id'],
          'totalcorner_match_id':e['totalcorner_match_id'],'run_id':a.run_id,'m1_in_scope':m1,
          'mr1_in_scope':mr1,'research_scope':group,'formal_order':False,'telegram_sent':False})
        counts[group]+=1
        if e['timing_state']=='TIME_QUALIFIED':counts['TIME_'+group]+=1
    with a.ledger.open('a') as out:
        for row in rows:out.write(json.dumps(row,ensure_ascii=False,sort_keys=True)+'\n')
    print(json.dumps({'status':'COMPLETED','added':len(rows),'scope_counts':dict(counts)}))
if __name__=='__main__':main()
