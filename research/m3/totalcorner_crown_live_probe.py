"""Read actual Crown movement endpoint for selected source schedule IDs without emitting prices."""
import argparse,json,os,time,urllib.parse,urllib.request

def main():
    p=argparse.ArgumentParser();p.add_argument('--ids',nargs='+',required=True);a=p.parse_args()
    token=os.environ.get('TOTALCORNER_TOKEN')
    if not token: raise RuntimeError('TOTALCORNER_TOKEN is missing')
    for match_id in a.ids:
        url='https://api.totalcorner.com/v1/match/bookmaker_odds/'+urllib.parse.quote(match_id,safe='')+'?'+urllib.parse.urlencode({'token':token,'bookmaker':'crown','columns':'asianList,goalList'})
        for retry in range(7):
            with urllib.request.urlopen(urllib.request.Request(url,headers={'Accept':'application/json'}),timeout=30) as response:
                result=json.load(response)
            code=(result.get('error') or {}).get('code') if isinstance(result.get('error'),dict) else None
            if code=='TOO_MANY_REQUEST' and retry<6:
                time.sleep(11);continue
            break
        if result.get('success')!=1:
            print(json.dumps({'id':match_id,'status':'API_UNSUCCESSFUL','error_code':code}));continue
        matches=[m for m in result.get('data',[]) if str(m.get('id'))==match_id]
        crown=[b for m in matches for b in m.get('bookmakers',[]) if b.get('slug')=='crown']
        print(json.dumps({'id':match_id,'status':'CROWN_IDENTIFIED' if len(crown)==1 else 'CROWN_MISSING_OR_AMBIGUOUS','source_match_count':len(matches),'crown_bookmaker_count':len(crown),'bookmaker_keys':sorted(crown[0].keys()) if len(crown)==1 else [],'ah_movement_rows':len(crown[0].get('asian_list',[])) if len(crown)==1 else 0,'ou_movement_rows':len(crown[0].get('goal_list',[])) if len(crown)==1 else 0,'camel_ah_rows':len(crown[0].get('asianList',[])) if len(crown)==1 else 0,'camel_ou_rows':len(crown[0].get('goalList',[])) if len(crown)==1 else 0,'bet_placed':False,'telegram_sent':False}))
        # User-approved M3 fallback: inspect TotalCorner default odds when Crown rows are absent.
        if len(crown)!=1 or not crown[0].get('asian_list') or not crown[0].get('goal_list'):
            time.sleep(2.2)
            fallback_url='https://api.totalcorner.com/v1/match/odds/'+urllib.parse.quote(match_id,safe='')+'?'+urllib.parse.urlencode({'token':token,'columns':'asianList,goalList'})
            for retry in range(7):
                with urllib.request.urlopen(urllib.request.Request(fallback_url,headers={'Accept':'application/json'}),timeout=30) as response:
                    alternative=json.load(response)
                err=alternative.get('error')
                code=err.get('code') if isinstance(err,dict) else None
                if code=='TOO_MANY_REQUEST' and retry<6:
                    time.sleep(11);continue
                break
            alternative_matches=[m for m in alternative.get('data',[]) if isinstance(m,dict) and str(m.get('id'))==match_id] if alternative.get('success')==1 else []
            if len(alternative_matches)==1:
                record=alternative_matches[0]
                print(json.dumps({'id':match_id,'source':'TotalCorner match/odds default (NOT Crown)','status':'DEFAULT_ODDS_FOUND','ah_movement_rows':len(record.get('asian_list') or []),'ou_movement_rows':len(record.get('goal_list') or []),'available_keys':sorted(k for k in record.keys() if k in ('asian_list','goal_list','asian','goal')),'row_shapes':{market:{'lengths':sorted(set(len(x) for x in record.get(field,[]) if isinstance(x,list))),'minute_first_three':[str(x[0]) for x in record.get(field,[])[:3] if isinstance(x,list) and x],'closed_first_three':[str(x[7]) if len(x)>7 else 'absent' for x in record.get(field,[])[:3] if isinstance(x,list)],'prices_first_three':[[str(type(x[i]).__name__),str(x[i]>1) if isinstance(x[i],(int,float)) else 'not_numeric'] for x in record.get(field,[])[:1] if isinstance(x,list) for i in (2,3) if len(x)>i]} for market,field in [('AH','asian_list'),('OU','goal_list')]},'telegram_sent':False}))
            else:
                print(json.dumps({'id':match_id,'source':'TotalCorner match/odds default (NOT Crown)','status':'DEFAULT_ODDS_UNAVAILABLE','error_code':code,'telegram_sent':False}))
        time.sleep(2.2)
if __name__=='__main__': main()
