"""Append-only, shadow-only M3 settlement using verified TotalCorner full-time results.

Never alters forecasts or orders. OpenFootball is independent corroboration when present.
"""
import argparse
import datetime
import hashlib
import json
import os
import time
import urllib.parse
import urllib.request
from pathlib import Path
from research.m3.kickoff_gate import totalcorner_shanghai_kickoff
from research.m3.probabilities import settle_score

UTC = datetime.timezone.utc
FT_STATUSES = {'full','finished','ft','complete','completed','ended','aet'}

def response_row(payload, match_id):
    if payload.get('success') != 1:
        raise ValueError('provider response not successful')
    data = payload.get('data')
    rows = data if isinstance(data,list) else [data] if isinstance(data,dict) else []
    found=[r for r in rows if isinstance(r,dict) and str(r.get('id'))==str(match_id)]
    if len(found)!=1: raise ValueError('provider match identity unresolved')
    return found[0]

def verified_final(payload, match_id, kickoff, now):
    row=response_row(payload,match_id)
    if str(row.get('status','')).strip().lower() not in FT_STATUSES:return None
    if not row.get('h') or not row.get('a') or not row.get('l_id'):raise ValueError('missing provider identity')
    stamp=totalcorner_shanghai_kickoff(row)
    if stamp is None or not kickoff or stamp != kickoff:
        raise ValueError('provider kickoff identity mismatch')
    if datetime.datetime.fromisoformat(kickoff).astimezone(UTC)>=now:return None
    def score(key):
        v=row.get(key)
        if isinstance(v,bool) or not str(v).isdigit():raise ValueError('invalid final score')
        return int(v)
    return score('hg'),score('ag'),hashlib.sha256(json.dumps(row,sort_keys=True,ensure_ascii=False).encode()).hexdigest()

def fetch_final(match_id,token):
    url='https://api.totalcorner.com/v1/match/view/'+urllib.parse.quote(str(match_id),safe='')+'?'+urllib.parse.urlencode({'token':token})
    for attempt in range(5):
        with urllib.request.urlopen(urllib.request.Request(url,headers={'Accept':'application/json'}),timeout=30) as response:
            payload=json.load(response)
        if payload.get('success')==1:return payload
        if (payload.get('error') or {}).get('code')!='TOO_MANY_REQUEST':return payload
        time.sleep(11)
    return payload

def reconcile(events,finished,lookup,now):
    forecasts={x['forecast_id']:x for x in events if x.get('protocol')=='M3_TOTALCORNER_FORWARD_FORECAST_V1'}
    existing={x.get('event_id') for x in events}
    candidates=[x for x in events if x.get('protocol')=='M3_TOTALCORNER_FORWARD_EV_V1']
    ids={}
    for e in candidates:
        f=forecasts.get(e.get('forecast_id'))
        if not f or not f.get('kickoff_utc_verified') or not e.get('totalcorner_match_id'):continue
        key=str(e['totalcorner_match_id'])
        ids.setdefault(key,set()).add((f['fixture_identity_id'],f['kickoff_utc_verified']))
    verified={};reasons={}
    for mid,identities in ids.items():
        if len(identities)!=1:
            reasons['CONFLICTING_FIXTURE_MAPPING']=reasons.get('CONFLICTING_FIXTURE_MAPPING',0)+1;continue
        fid,kickoff=next(iter(identities))
        if datetime.datetime.fromisoformat(kickoff).astimezone(UTC)>=now:continue
        try:
            payload=lookup(mid)
            outcome=verified_final(payload,mid,kickoff,now)
            if outcome is None:continue
            source_result=finished.get(fid)
            if source_result is not None and (int(source_result['home_goals']),int(source_result['away_goals']))!=outcome[:2]:
                reasons['OPENFOOTBALL_SCORE_CONFLICT']=reasons.get('OPENFOOTBALL_SCORE_CONFLICT',0)+1;continue
            verified[mid]=outcome
        except Exception:
            reasons['PROVIDER_OR_IDENTITY_UNVERIFIED']=reasons.get('PROVIDER_OR_IDENTITY_UNVERIFIED',0)+1
    new=[]
    for e in candidates:
        f=forecasts.get(e.get('forecast_id'))
        if not f or e.get('fixture_identity_id')!=f.get('fixture_identity_id'):continue
        outcome=verified.get(str(e.get('totalcorner_match_id')))
        if outcome is None:continue
        h,a,digest=outcome
        state,unit=settle_score(e['market'],e['line'],e['side'],h,a,e['decimal_odd'])
        event_id=hashlib.sha256(('M3_RESULT_OBSERVED_V1:'+e['event_id']).encode()).hexdigest()
        if event_id in existing:continue
        new.append({'event_id':event_id,'protocol':'M3_TOTALCORNER_FORWARD_SETTLEMENT_V1',
            'candidate_event_id':e['event_id'],'forecast_id':e['forecast_id'],
            'fixture_identity_id':e['fixture_identity_id'],'home_goals':h,'away_goals':a,
            'market':e['market'],'side':e['side'],'line':e['line'],
            'hypothetical_unit_return':unit,'settlement_state':state,
            'actual_bet_placed':False,'formal_order':False,'telegram_sent':False,
            'result_source':'TotalCorner verified /match/view','result_sha256':digest,
            'openfootball_crosscheck':'MATCHED' if e['fixture_identity_id'] in finished else 'NOT_AVAILABLE',
            'observed_utc':now.isoformat()})
        existing.add(event_id)
    return new, {'verified_fixtures':len(verified),'rejected':reasons,'candidates':len(candidates)}

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--input-root',required=True,type=Path)
    p.add_argument('--ledger',required=True,type=Path)
    args=p.parse_args()
    events=[json.loads(s) for s in args.ledger.read_text().splitlines() if s.strip()]
    from research.m3.openfootball_shadow import read_openfootball
    result,_,_,_=read_openfootball(args.input_root)
    finished={r['fixture_identity_id']:r for r in result.to_dict('records')}
    token=os.environ['TOTALCORNER_TOKEN'];now=datetime.datetime.now(UTC)
    new,stats=reconcile(events,finished,lambda mid:fetch_final(mid,token),now)
    with args.ledger.open('a') as out:
        for row in new:out.write(json.dumps(row,sort_keys=True,ensure_ascii=False)+'\n')
    print(json.dumps({'status':'COMPLETED','settlements_added':len(new),'formal_bets':0,'realized_formal_roi':None,**stats}))

if __name__=='__main__':main()
