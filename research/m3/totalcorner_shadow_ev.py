"""Calculate M3 EV with genuine TotalCorner default AH/OU lines, never represent them as Crown."""
import argparse,datetime,hashlib,json,os,time,urllib.parse,urllib.request,difflib
from research.m3.totalcorner_schedule_discovery import get_schedule,normalize
from pathlib import Path
from research.m3.probabilities import settle_score

LEAGUES={'D1':'Germany Bundesliga I','E0':'England Premier League','I1':'Italy Serie A','F1':'France Ligue 1','SP1':'Spain La Liga'}
ALIASES={'1. FSV Mainz 05':'Mainz','SV Werder Bremen':'Werder Bremen','Aston Villa FC':'Aston Villa','Manchester City FC':'Man City','Arsenal FC':'Arsenal','Everton FC':'Everton','RB Leipzig':'RB Leipzig','SV 07 Elversberg':'Elversberg','FC Augsburg':'Augsburg','1. FC Union Berlin':'Union Berlin','Cagliari Calcio':'Cagliari','Bologna FC 1909':'Bologna','Como 1907':'Como','US Sassuolo Calcio':'Sassuolo'}
def fixture_matches(f,m):
    if m.get('l')!=LEAGUES.get(f.get('league')):return False
    return normalize(ALIASES.get(f['home_team'],f['home_team']))==normalize(m.get('h')) and normalize(ALIASES.get(f['away_team'],f['away_team']))==normalize(m.get('a'))
def discover(events,token):
    today=datetime.datetime.now(datetime.timezone.utc).date()
    dates=sorted({r.get('source_fixture_date') for r in events if r.get('event_type')=='FORECAST' and r.get('forecast_status')=='PREDICTED_NO_MARKET' and r.get('source_fixture_date') and today<=datetime.date.fromisoformat(r['source_fixture_date'])<=today+datetime.timedelta(days=5)})
    fixtures=[]
    for day in dates:
        schedule,_=get_schedule(day,token)
        for f in (r for r in events if r.get('event_type')=='FORECAST' and r.get('source_fixture_date')==day):
            eligible=[m for m in schedule if fixture_matches(f,m)]
            if len(eligible)==1: fixtures.append((f,eligible[0]))
        time.sleep(2.5)
    return fixtures
def fetch(mid,token):
    url='https://api.totalcorner.com/v1/match/odds/'+mid+'?'+urllib.parse.urlencode({'token':token,'columns':'asianList,goalList'})
    for i in range(7):
        with urllib.request.urlopen(urllib.request.Request(url,headers={'Accept':'application/json'}),timeout=30) as resp: data=json.load(resp)
        if data.get('success')==1: return next(x for x in data.get('data',[]) if str(x.get('id'))==mid)
        if (data.get('error') or {}).get('code')!='TOO_MANY_REQUEST' or i==6: raise ValueError('source response failed')
        time.sleep(11)
def stamp(raw):
    raw=str(raw).replace(' ','T')
    if not raw.endswith('Z') and '+' not in raw: raw+='+08:00'
    return datetime.datetime.fromisoformat(raw.replace('Z','+00:00')).astimezone(datetime.timezone.utc)
def prices(row,market,forecast_at,kickoff):
    if not isinstance(row,list) or len(row)<8 or row[0] is not None or row[7] not in (0,'0',False):return None
    observed=stamp(row[4])
    if not forecast_at<=observed<kickoff:return None
    rawline=str(row[1]).split(',')
    line=sum(float(x) for x in rawline)/len(rawline)
    first,second=float(row[2]),float(row[3])
    if first<=1 or second<=1:return None
    return (observed,market,line,first,second)
def value(f,market,line,side,odd):
    grid=f.get('score_probability_grid')
    if grid:
        outcome=0.0
        coverage=0.0
        for home_goals,row in enumerate(grid):
            for away_goals,probability in enumerate(row):
                _,net=settle_score(market,line,side,home_goals,away_goals,odd)
                outcome+=net*probability
                coverage+=probability
        return outcome/coverage
    # Old M3 forecasts have AH0 and OU2.5 probabilities only.
    if market=='AH' and line==0:
        p=[f['ah_home_0_p_win'],f['ah_home_0_p_push'],f['ah_home_0_p_lose']]
        if side=='away':p=p[::-1]
        return p[0]*(odd-1)-p[2]
    if market=='OU' and line==2.5:
        p=f['ou_p_over_2_5'] if side=='over' else 1-f['ou_p_over_2_5']
        return p*(odd-1)-(1-p)
    return None
def main():
    p=argparse.ArgumentParser();p.add_argument('--ledger',type=Path,required=True);p.add_argument('--private-output',type=Path,required=True);a=p.parse_args()
    token=os.environ['TOTALCORNER_TOKEN']
    events=[json.loads(x) for x in a.ledger.open() if x.strip()]
    records=[]
    discovered=discover(events,token)
    by_match={}
    for f,m in discovered: by_match.setdefault(str(m['id']),[]).append(f)
    print(json.dumps({'discovered_fixture_ids':len(by_match),'matched_forecasts':len(discovered)}))
    for mid,forecasts in by_match.items():
        match=fetch(mid,token)
        if not match.get('h') or not match.get('a'):raise ValueError('missing TotalCorner match names')
        kickoff=stamp(match['start'])
        print(json.dumps({'match_id':mid,'quote_diagnostics':{m:{'rows':len(match.get(k,[])),'lines':sorted(set(str(row[1]) for row in match.get(k,[]) if isinstance(row,list) and len(row)>4))} for m,k in [('AH','asian_list'),('OU','goal_list')]},'forecast_rows':len(forecasts)}))
        for f in forecasts:
            predicted=stamp(f['forecasted_at_utc'])
            if predicted>=kickoff:continue
            for market,field,sides in [('AH','asian_list',('home','away')),('OU','goal_list',('over','under'))]:
                eligible=[r for raw in match.get(field,[]) if (r:=prices(raw,market,predicted,kickoff))]
                if not eligible:continue
                observed,_,line,first,second=max(eligible,key=lambda x:x[0])
                for side,odd in zip(sides,(first,second)):
                    ev=value(f,market,line,side,odd)
                    if ev is None:continue
                    records.append({'protocol':'M3_TOTALCORNER_DEFAULT_SHADOW_EV_V1','forecast_id':f['forecast_id'],'model':f['model'],'fixture_identity_id':f['fixture_identity_id'],'totalcorner_match_id':mid,'provider':'TotalCorner','bookmaker':'default_unspecified_NOT_CROWN','market':market,'line':line,'side':side,'decimal_odd':odd,'observed_at_utc':observed.isoformat(),'forecasted_at_utc':f['forecasted_at_utc'],'kickoff_at_utc':kickoff.isoformat(),'expected_unit_return':ev,'telegram_sent':False,'formal_order':False,'settled':False})
        time.sleep(2.2)
    a.private_output.parent.mkdir(parents=True,exist_ok=True)
    # Idempotent append: re-running the shadow scan must not double-count quotes.
    existing=set()
    if a.private_output.exists():
        for line in a.private_output.read_text().splitlines():
            if line.strip():
                old=json.loads(line)
                existing.add((old['forecast_id'],old['totalcorner_match_id'],old['market'],old['line'],old['side'],old['observed_at_utc']))
    new=[]
    for r in records:
        key=(r['forecast_id'],r['totalcorner_match_id'],r['market'],r['line'],r['side'],r['observed_at_utc'])
        if key not in existing:
            new.append(r);existing.add(key)
    with a.private_output.open('a') as file:
        for r in new:file.write(json.dumps(r,ensure_ascii=False)+'\n')
    print(json.dumps({'status':'COMPLETED','source':'TotalCorner default NOT Crown','ev_rows_appended':len(new),'forecast_ids':len(set(r['forecast_id'] for r in records)),'private_path':str(a.private_output),'telegram_sent':False,'formal_order':False}))
if __name__=='__main__':main()
