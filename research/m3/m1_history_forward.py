"""Additional M3 shadow predictions trained on existing read-only M1 full-time league cache.

This is separate from the existing OpenFootball baseline. No Telegram orders.
"""
import argparse, collections, datetime, json, os, time
from pathlib import Path
import pandas as pd
from research.m3.totalcorner_schedule_discovery import get_schedule
from research.m3.kickoff_gate import totalcorner_shanghai_kickoff,gate
from research.m3.openfootball_shadow import MODELS,_serialize_score_probability_grid
from research.m3.totalcorner_forward_ev import hash_id,get_latest,calculate
from research.m3.totalcorner_shadow_ev import fetch
from research.m3.m1_mr1_scope_audit import classify, MR1_PATH

UTC=datetime.timezone.utc
def load_history(cache_dir,now):
    grouped={};counts=collections.Counter()
    for file in sorted(cache_dir.glob('*.json')):
        try: data=json.loads(file.read_text())
        except (ValueError,OSError):
            counts['unreadable_cache']+=1;continue
        lid=str(data.get('league_id',''))
        arr=[]
        for r in data.get('rows',[]):
            if r.get('status')!='full':continue
            try:
                ts=datetime.datetime.fromisoformat(str(r['start']).replace(' ','T')).replace(tzinfo=datetime.timezone(datetime.timedelta(hours=8))).astimezone(UTC)
                h,a=str(r['h_id']),str(r['a_id']);gh,ga=int(r['hg']),int(r['ag'])
                if ts>=now or not h.isdigit() or not a.isdigit() or h==a or min(gh,ga)<0:continue
            except (ValueError,TypeError,KeyError):continue
            arr.append((str(r['id']),ts,h,a,gh,ga))
        unique={r[0]:r for r in arr}
        if not lid.isdigit():continue
        grouped[lid]=list(unique.values())
        counts['finished_training_rows']+=len(unique)
        counts['cache_leagues']+=1
    return grouped,dict(counts)

def candidate(row,now,spec,hist):
    m1,mr1,scope=classify(row.get('l'),row.get('h'),row.get('a'),spec)
    if not (m1 or mr1):return 'OUT_OF_M1_MR1_SCOPE',None
    start=totalcorner_shanghai_kickoff(row)
    ok,_,reason=gate({'kickoff_utc_verified':start},now)
    if not ok:return reason,None
    lid=str(row.get('l_id') or '')
    h,a=str(row.get('h_id') or ''),str(row.get('a_id') or '')
    if not lid.isdigit() or not h.isdigit() or not a.isdigit():return 'MISSING_TOTALCORNER_IDS',None
    league=hist.get(lid,[])
    teams={t for r in league for t in r[2:4]}
    if h not in teams or a not in teams:return 'MISSING_TEAM_HISTORY',None
    if len(league)<2:return 'INSUFFICIENT_LEAGUE_RESULTS',None
    return 'READY',(lid,h,a,start,league)

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--cache-dir',type=Path,required=True);p.add_argument('--ledger',type=Path,required=True)
    p.add_argument('--run-id',required=True);p.add_argument('--max-dates',type=int,default=2)
    args=p.parse_args()
    now=datetime.datetime.now(UTC)
    history,coverage=load_history(args.cache_dir,now)
    spec=json.loads(MR1_PATH.read_text())
    bj=now.astimezone(datetime.timezone(datetime.timedelta(hours=8))).date()
    found={};counts=collections.Counter();pages=0
    for delta in range(args.max_dates):
        day=(bj+datetime.timedelta(days=delta)).isoformat()
        sched,n=get_schedule(day,os.environ['TOTALCORNER_TOKEN']);pages+=n
        for r in sched:
            counts['source_rows']+=1
            reason,info=candidate(r,now,spec,history);counts[reason]+=1
            if info:found[str(r['id'])]=(r,info)
    # Historical shadow orders remain immutable. Avoid fitting/predicting a fixture
    # whose model already has both AH and OU shadow orders in any earlier run.
    prior=set()
    completed_orders=set()
    with args.ledger.open() as stream:
        for line in stream:
            if not line.strip():continue
            record=json.loads(line)
            prior.add(record['event_id'])
            if record.get('protocol')=='M3_SHADOW_ORDER_V1':
                completed_orders.add((str(record['fixture_identity_id']),record['model'],record['market']))
    rows=[];forecast_count=0;ev_count=0
    by_league=collections.defaultdict(list)
    for mid,(source,info) in found.items():by_league[info[0]].append((mid,source,info))
    for lid,fixtures in by_league.items():
        train=fixtures[0][2][4]
        frame=pd.DataFrame([{'home_team':x[2],'away_team':x[3],'home_goals':x[4],'away_goals':x[5]} for x in train])
        for model_name,cls in MODELS.items():
            try:
                model=cls(frame.home_goals,frame.away_goals,frame.home_team,frame.away_team);model.fit()
            except Exception:
                counts['MODEL_FIT_FAILED_'+model_name]+=1;continue
            for mid,src,(_,h,a,start,_) in fixtures:
                fixture_key=hash_id(['M3_TOTALCORNER_FIXTURE_V1',mid])
                if all((fixture_key,model_name,market) in completed_orders for market in ('AH','OU')):
                    counts['ALREADY_HAS_BOTH_MARKET_ORDERS']+=1
                    continue
                forecast_at=datetime.datetime.now(UTC)
                if not gate({'kickoff_utc_verified':start},forecast_at)[0]:
                    counts['TIMING_EXPIRED_DURING_FIT']+=1
                    continue
                try: matrix=_serialize_score_probability_grid(model.predict(h,a))
                except Exception:
                    counts['MODEL_PREDICT_FAILED_'+model_name]+=1;continue
                fid=hash_id(['M3_M1_CACHE_FORWARD_V1',args.run_id,mid,model_name,forecast_at.isoformat()])
                fixture_id=hash_id(['M3_TOTALCORNER_FIXTURE_V1',mid])
                ev={'protocol':'M3_TOTALCORNER_FORWARD_FORECAST_V1','forecast_id':fid,
                    'fixture_identity_id':fixture_id,'model':model_name,'source_fixture_date':str(src.get('start',''))[:10],
                    'totalcorner_match_id':mid,'home_team':str(src.get('h')),'away_team':str(src.get('a')),
                    'home_team_id':h,'away_team_id':a,'league_id':lid,
                    'training_source':'M1_READ_ONLY_CACHE','model_semantic_version':'m3-m1-id-goal-v1',
                    'training_rows':len(train),'score_grid_sha256':hash_id(matrix),
                    'training_cutoff_utc':forecast_at.isoformat(),'forecasted_at_utc':forecast_at.isoformat(),
                    'kickoff_utc_verified':start,'score_probability_grid':matrix,
                    'formal_order':False,'telegram_sent':False,'run_id':args.run_id}
                ev['event_id']=hash_id(['M3_M1_CACHE_EVENT_V1',fid])
                if ev['event_id'] not in prior:rows.append(ev);prior.add(ev['event_id'])
                forecast_count+=1
                # Read source prices strictly after the forecast matrix exists.
                # Never call them Crown or a tradable execution quote.
                if len(found[mid]) == 2:
                    try:found[mid]=(src,info,fetch(mid,os.environ['TOTALCORNER_TOKEN']),datetime.datetime.now(UTC).isoformat())
                    except Exception:
                        counts['QUOTE_FETCH_FAILED']+=1
                        found[mid]=(src,info,{},datetime.datetime.now(UTC).isoformat())
                    time.sleep(2.2)
                quote_data=found[mid][2];captured=found[mid][3]
                for market,field,sides in [('AH','asian_list',('home','away')),('OU','goal_list',('over','under'))]:
                    quote=get_latest(quote_data.get(field))
                    if not quote:continue
                    _,line,odd1,odd2=quote
                    for side,odd in zip(sides,(odd1,odd2)):
                        record={'protocol':'M3_TOTALCORNER_FORWARD_EV_V1','forecast_id':fid,'model':model_name,
                           'fixture_identity_id':fixture_id,'source_fixture_date':ev['source_fixture_date'],
                           'home_team':ev['home_team'],'away_team':ev['away_team'],
                           'totalcorner_match_id':mid,'provider':'TotalCorner',
                           'bookmaker':'totalcorner_default_NOT_CROWN','market':market,
                           'line':line,'side':side,'decimal_odd':odd,
                           'expected_unit_return':calculate(matrix,market,line,side,odd),
                           'quote_snapshot_recorded_utc':captured,
                           'forecasted_at_utc':forecast_at.isoformat(),'formal_order':False,
                           'telegram_sent':False,'settled':False,'run_id':args.run_id}
                        record['event_id']=hash_id(['M3_EV',fid,market,line,side])
                        if record['event_id'] not in prior:rows.append(record);prior.add(record['event_id']);ev_count+=1
    with args.ledger.open('a') as out:
        for x in rows:out.write(json.dumps(x,ensure_ascii=False,sort_keys=True)+'\n')
    print(json.dumps({'status':'COMPLETED','pages':pages,'cache_coverage':coverage,'reasons':dict(counts),
          'distinct_predicted_fixtures':len({x['fixture_identity_id'] for x in rows if x['protocol']=='M3_TOTALCORNER_FORWARD_FORECAST_V1'}),
          'forecast_count':forecast_count,'ev_count':ev_count,'events_added':len(rows)}))
if __name__=='__main__':main()
