"""Source-wide prospective fixture/quote inventory; never generates invented model picks."""
import argparse, collections, datetime, hashlib, json, os, time
from pathlib import Path
from research.m3.totalcorner_schedule_discovery import get_schedule
from research.m3.totalcorner_forward_ev import fetch_crown,get_latest
from research.m3.kickoff_gate import totalcorner_shanghai_kickoff,gate
UTC=datetime.timezone.utc
def process(schedules,now,quote_lookup,pace=lambda:None):
    records=[];counts=collections.Counter();seen=set()
    for day,rows in schedules:
        for row in rows:
            counts['source_rows']+=1
            mid=str(row.get('id',''))
            identity=(day,mid)
            if not mid.isdigit() or identity in seen:
                counts['invalid_or_duplicate']+=1;continue
            seen.add(identity)
            start=totalcorner_shanghai_kickoff(row)
            allowed,lead,reason=gate({'kickoff_utc_verified':start},now)
            status='TIME_QUALIFIED' if allowed else reason
            markets={'AH':'NOT_CHECKED_TIME','OU':'NOT_CHECKED_TIME'}
            snapshot=None
            if allowed:
                counts['time_qualified']+=1
                try:
                    quote_lookup_result=quote_lookup(mid)
                    snapshot=datetime.datetime.now(UTC).isoformat()
                    for market,field in [('AH','asian_list'),('OU','goal_list')]:
                        markets[market]='CROWN_AVAILABLE' if get_latest(quote_lookup_result.get(field)) else 'NO_CROWN_QUOTE'
                        counts[market+'_'+markets[market]]+=1
                except Exception:
                    markets={'AH':'QUOTE_QUERY_FAILED','OU':'QUOTE_QUERY_FAILED'}
                    counts['quote_query_failed']+=1
                pace()
            else:counts[reason]+=1
            item={'protocol':'M3_TOTALCORNER_FUTURE_INVENTORY_V1','source':'TotalCorner',
              'totalcorner_match_id':mid,'source_fixture_date':day,
              'league_source':str(row.get('l') or ''),'home_source':str(row.get('h') or ''),
              'away_source':str(row.get('a') or ''),'kickoff_utc_verified':start,
              'timing_state':status,'lead_minutes_at_scan':lead,'crown_market_status':markets,
              'quote_observed_utc':snapshot,'formal_order':False,'telegram_sent':False}
            records.append(item)
    return records,dict(counts)
def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True)
    p.add_argument('--run-id',required=True);p.add_argument('--max-dates',type=int,default=2)
    a=p.parse_args()
    now=datetime.datetime.now(UTC)
    bj=now.astimezone(datetime.timezone(datetime.timedelta(hours=8))).date()
    schedules=[];pages=0
    for offset in range(a.max_dates):
        day=(bj+datetime.timedelta(days=offset)).isoformat()
        rows,count=get_schedule(day,os.environ['TOTALCORNER_TOKEN'])
        schedules.append((day,rows));pages+=count
    records,counts=process(schedules,now,
        lambda mid:fetch_crown(mid,os.environ['TOTALCORNER_TOKEN']),
        lambda:time.sleep(2.2))
    a.output.parent.mkdir(parents=True,exist_ok=True)
    with a.output.open('a') as out:
        for r in records:
            r['run_id']=a.run_id
            r['event_id']=hashlib.sha256(json.dumps(['M3_FUTURE_INVENTORY_V1',a.run_id,r['source_fixture_date'],r['totalcorner_match_id']],separators=(',',':')).encode()).hexdigest()
            out.write(json.dumps(r,ensure_ascii=False,sort_keys=True)+'\n')
    print(json.dumps({'status':'COMPLETED','source_pages':pages,'events_added':len(records),'counts':counts,'output':str(a.output)}))
if __name__=='__main__':main()
