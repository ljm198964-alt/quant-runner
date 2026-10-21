"""Fresh M3 forward snapshots with true current TotalCorner default odds and source-labelled EV.

New records only; never backfills older recorded forecasts. Research shadow, no Telegram.
"""
from __future__ import annotations
import argparse,datetime,hashlib,json,math,os,time
from pathlib import Path
import pandas as pd
from research.m3.openfootball_shadow import read_openfootball,MODELS,_serialize_score_probability_grid
from research.m3.totalcorner_schedule_discovery import get_schedule
from research.m3.totalcorner_auto_shadow import match_one
from research.m3.totalcorner_shadow_ev import fetch
from research.m3.probabilities import settle_score

UTC=datetime.timezone.utc
def hash_id(values):
    return hashlib.sha256(json.dumps(values,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
def money(line_raw):
    parts=[float(x) for x in str(line_raw).split(',')]
    if not (1<=len(parts)<=2 and all(math.isfinite(x) for x in parts)):raise ValueError('invalid Asian line')
    line=sum(parts)/len(parts)
    if abs(line*4-round(line*4))>1e-7:raise ValueError('non-quarter Asian line')
    return line
def get_latest(rows):
    valid=[]
    for r in rows or []:
        if not isinstance(r,list) or len(r) not in (7,8) or r[0] not in (None,0,'0',''):continue
        if len(r)==8 and r[7] not in (None,0,'0',False):continue
        try:
            line=money(r[1]);a=float(r[2]);b=float(r[3])
            if not(math.isfinite(a) and math.isfinite(b) and a>1 and b>1):continue
            valid.append((str(r[4]),line,a,b))
        except (TypeError,ValueError):continue
    if not valid:return None
    valid.sort(key=lambda x:x[0])
    last=valid[-1]
    if any(x[0]==last[0] and x[1:]!=last[1:] for x in valid):return None
    return last
def calculate(matrix,market,line,side,decimal):
    mass=0.0;ev=0.0
    for h,row in enumerate(matrix):
        for a,prob in enumerate(row):
            _,profit=settle_score(market,line,side,h,a,decimal)
            mass+=prob;ev+=prob*profit
    if not math.isclose(mass,1,abs_tol=1e-7):raise ValueError('score grid invalid')
    return ev/mass
def run(root,output,max_dates,run_id):
    now=datetime.datetime.now(UTC)
    data,fixtures,_,_=read_openfootball(root)
    # All model training is limited strictly to past calendar dates.
    train=data.loc[data.match_date_utc.lt(pd.Timestamp(now.date().isoformat(),tz='UTC'))]
    # At least 3 calendar days out avoids pretending an unqualified provider
    # wall-clock start is a verified UTC kickoff time.
    next_days=sorted({f['source_date'] for f in fixtures if
        now.date()+datetime.timedelta(days=3)<=datetime.date.fromisoformat(f['source_date'])<=
        now.date()+datetime.timedelta(days=5)})[:max_dates]
    matched_by_league={}
    pages=0
    for day in next_days:
        schedule,count=get_schedule(day,os.environ['TOTALCORNER_TOKEN']);pages+=count
        for fixture in fixtures:
            if fixture['source_date']!=day:continue
            source=match_one(fixture,schedule)
            if source:matched_by_league.setdefault(fixture['league'],[]).append((fixture,source))
    existing=set()
    if output.exists():
        for line in output.read_text().splitlines():
            if line.strip():existing.add(json.loads(line)['event_id'])
    rows=[];forecast_count=0;quote_count=0
    for league,pairs in matched_by_league.items():
        league_train=train.loc[train.league.eq(league)]
        if league_train.empty:continue
        market_cache={}
        for fixture,src in pairs:
            sid=str(src['id'])
            if sid not in market_cache:
                market_cache[sid]=(fetch(sid,os.environ['TOTALCORNER_TOKEN']),datetime.datetime.now(UTC).isoformat())
                time.sleep(2.2)
        for model_name,cls in MODELS.items():
            model=cls(league_train.home_goals,league_train.away_goals,league_train.home_team,league_train.away_team)
            model.fit()
            known=set(map(str,model.teams))
            for fixture,src in pairs:
                if fixture['home_team'] not in known or fixture['away_team'] not in known:continue
                forecasted_at=datetime.datetime.now(UTC).isoformat()
                distribution=model.predict(fixture['home_team'],fixture['away_team'])
                matrix=_serialize_score_probability_grid(distribution)
                forecast_id=hash_id(['M3_FRESH_FORWARD_V1',run_id,fixture['fixture_identity_id'],model_name,forecasted_at])
                forecast_count+=1
                match,market_captured_at=market_cache[str(src['id'])]
                # Market request was made before the forecast computation; this is
                # a valid current comparison snapshot, not an execution quote.
                for market,field,sides in [('AH','asian_list',('home','away')),('OU','goal_list',('over','under'))]:
                    quote=get_latest(match.get(field))
                    if quote is None:continue
                    _,line,a,b=quote
                    quote_count+=1
                    for side,decimal in zip(sides,(a,b)):
                        result={'protocol':'M3_TOTALCORNER_FORWARD_EV_V1','forecast_id':forecast_id,
                            'forecast_protocol':'NEW_FORWARD_RESEARCH_SNAPSHOT','forecasted_at_utc':forecasted_at,
                            'model':model_name,'fixture_identity_id':fixture['fixture_identity_id'],
                            'source_fixture_date':fixture['source_date'],'home_team':fixture['home_team'],
                            'away_team':fixture['away_team'],'totalcorner_match_id':str(src['id']),
                            'provider':'TotalCorner','bookmaker':'default_unspecified_NOT_CROWN',
                            'market':market,'line':line,'side':side,'decimal_odd':decimal,
                            'expected_unit_return':calculate(matrix,market,line,side,decimal),
                            'quote_snapshot_recorded_utc':market_captured_at,
                            'source_wall_clock_timezone_verified':False,
                            'kickoff_utc_verified':False,'formal_order':False,'telegram_sent':False,
                            'settled':False,'roi':None,'run_id':run_id}
                        result['event_id']=hash_id(['M3_EV',forecast_id,market,line,side])
                        if result['event_id'] not in existing:rows.append(result);existing.add(result['event_id'])
    output.parent.mkdir(parents=True,exist_ok=True)
    with output.open('a') as file:
        for row in rows:file.write(json.dumps(row,ensure_ascii=False,sort_keys=True)+'\n')
    print(json.dumps({'status':'COMPLETED','date_count':len(next_days),'schedule_pages':pages,
        'matched_fixtures':sum(len(x) for x in matched_by_league.values()),
        'fresh_forecast_snapshots':forecast_count,'markets_quoted':quote_count,
        'ev_rows_appended':len(rows),'output':str(output),
        'telegram_sent':False,'settlements':0}))
def main():
    p=argparse.ArgumentParser()
    p.add_argument('--input-root',required=True,type=Path)
    p.add_argument('--output',required=True,type=Path)
    p.add_argument('--max-dates',default=2,type=int)
    p.add_argument('--run-id',required=True)
    a=p.parse_args()
    run(a.input_root,a.output,a.max_dates,a.run_id)
if __name__=='__main__':main()
