"""Automated M3 research-only fixture discovery, source-labeled quote EV and persistent ledger."""
import argparse,datetime,difflib,hashlib,json,os,time
from pathlib import Path
from research.m3.totalcorner_schedule_discovery import get_schedule,normalize
from research.m3.totalcorner_shadow_ev import fetch,stamp,prices,value

LEAGUES={'D1':'Germany Bundesliga I','E0':'England Premier League','F1':'France Ligue 1','I1':'Italy Serie A','SP1':'Spain La Liga'}
ALIASES={'1 fsv mainz 05':'mainz','sv werder bremen':'werder bremen','aston villa fc':'aston villa','manchester city fc':'man city','arsenal fc':'arsenal','everton fc':'everton','rb leipzig':'rb leipzig','sv 07 elversberg':'elversberg','fc augsburg':'augsburg','1 fc union berlin':'union berlin','cagliari calcio':'cagliari','bologna fc 1909':'bologna','como 1907':'como','us sassuolo calcio':'sassuolo','coventry city fc':'coventry','fulham fc':'fulham','toulouse fc':'toulouse','es troyes ac':'troyes'}
def match_one(f,rows):
    a,b=normalize(f['home_team']),normalize(f['away_team'])
    a,b=ALIASES.get(a,a),ALIASES.get(b,b)
    expected=LEAGUES.get(f['league'])
    scored=[]
    for row in rows:
        if row.get('l')!=expected:continue
        home,away=normalize(row.get('h')),normalize(row.get('a'))
        if not home or not away:continue
        h=difflib.SequenceMatcher(None,a,home).ratio()
        v=difflib.SequenceMatcher(None,b,away).ratio()
        scored.append((min(h,v),row))
    scored.sort(key=lambda x:x[0],reverse=True)
    if not scored or scored[0][0]<0.86 or (len(scored)>1 and scored[0][0]-scored[1][0]<0.12):return None
    return scored[0][1]
def choose(events):
    superseded={e.get('superseded_forecast_id') for e in events if e.get('event_type')=='FORECAST_DUPLICATE_SUPERSEDED'}
    selected={}
    for e in events:
        if e.get('event_type')!='FORECAST' or e.get('forecast_id') in superseded or e.get('forecast_status')!='PREDICTED_NO_MARKET':continue
        k=(e['fixture_identity_id'],e['model'])
        if k not in selected or (bool(e.get('score_probability_grid')) and not selected[k].get('score_probability_grid')):selected[k]=e
    return list(selected.values())
def main():
    p=argparse.ArgumentParser();p.add_argument('--ledger',required=True,type=Path);p.add_argument('--output',required=True,type=Path);p.add_argument('--max-dates',type=int,default=3);args=p.parse_args()
    events=[json.loads(line) for line in args.ledger.read_text().splitlines() if line.strip()]
    now=datetime.datetime.now(datetime.timezone.utc)
    forecasts=[f for f in choose(events) if now.date()<=datetime.date.fromisoformat(f['source_fixture_date'])<now.date()+datetime.timedelta(days=4)]
    dates=sorted(set(f['source_fixture_date'] for f in forecasts))[:args.max_dates]
    existing={}
    if args.output.exists():
        for line in args.output.read_text().splitlines():
            if line.strip():
                e=json.loads(line);existing[e['event_id']]=e
    added=[]; matched=0; skipped=0; dates_read=0
    for day in dates:
        fixtures,_=get_schedule(day,os.environ['TOTALCORNER_TOKEN']);dates_read+=1
        ids={}
        for f in forecasts:
            if f['source_fixture_date']!=day:continue
            m=match_one(f,fixtures)
            if m:ids.setdefault(str(m['id']),[]).append(f)
            else:skipped+=1
        for mid,fs in ids.items():
            m=fetch(mid,os.environ['TOTALCORNER_TOKEN'])
            # Provider clock unqualified: no independently verified UTC => no tradable EV.
            # Keep matching receipts separately; do not invent precise execution timestamps.
            matched+=len(fs)
            for f in fs:
                event={'protocol':'M3_TOTALCORNER_DEFAULT_MATCH_V1','forecast_id':f['forecast_id'],'fixture_identity_id':f['fixture_identity_id'],'totalcorner_match_id':mid,'model':f['model'],'provider':'TotalCorner','bookmaker':'default_unspecified_NOT_CROWN','source_fixture_date':day,'market_ah_history_rows':len(m.get('asian_list') or []),'market_ou_history_rows':len(m.get('goal_list') or []),'status':'MATCHED_TIMEZONE_UNVERIFIED','ev':None,'roi':None,'formal_order':False,'telegram_sent':False}
                event['event_id']=hashlib.sha256(json.dumps([event['forecast_id'],mid,'MATCH'],separators=(',',':')).encode()).hexdigest()
                if event['event_id'] not in existing:added.append(event);existing[event['event_id']]=event
            time.sleep(2.2)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    if added:
        with args.output.open('a') as fp:
            for item in added:fp.write(json.dumps(item,sort_keys=True)+'\n')
    print(json.dumps({'status':'COMPLETED','dates':dates_read,'forecast_rows':len(forecasts),'matched':matched,'unmatched':skipped,'records_added':len(added),'ev_rows':0,'blocker':'source timezone evidence not established and prior forecasts have no grids','output':str(args.output)}))
if __name__=='__main__': main()
