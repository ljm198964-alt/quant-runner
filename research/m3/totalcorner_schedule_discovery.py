"""Live TotalCorner schedule discovery against saved M3 predictions; no wagers or odds persistence."""
import argparse, collections, datetime, difflib, json, os, time, urllib.parse, urllib.request
from pathlib import Path

def get_schedule(day, token):
    page=1; rows=[]
    while True:
        params=urllib.parse.urlencode({'token':token,'date':day.replace('-',''),'page':page})
        req=urllib.request.Request('https://api.totalcorner.com/v1/match/schedule?'+params,headers={'Accept':'application/json'})
        with urllib.request.urlopen(req,timeout=25) as response:
            payload=json.load(response)
        if payload.get('success') != 1:
            raise RuntimeError('TotalCorner schedule API unsuccessful: '+str(payload.get('error','unspecified')))
        if not isinstance(payload.get('data'),list):
            raise RuntimeError('Unexpected schedule response shape')
        rows.extend(payload['data'])
        p=payload.get('pagination') or {}
        if not p.get('next'):
            break
        page += 1
        time.sleep(2.2)
    return rows,page

def normalize(value):
    import unicodedata,re
    value=''.join(c for c in unicodedata.normalize('NFKD',str(value or '').lower()) if not unicodedata.combining(c))
    return ' '.join(re.findall('[a-z0-9]+',value) )

def main():
    p=argparse.ArgumentParser();p.add_argument('--ledger',type=Path,required=True);p.add_argument('--date',required=True);a=p.parse_args()
    token=os.environ.get('TOTALCORNER_TOKEN')
    if not token: raise RuntimeError('TOTALCORNER_TOKEN missing')
    ledger=[json.loads(x) for x in a.ledger.open() if x.strip()]
    forecasts={r['fixture_identity_id']:r for r in ledger if r.get('event_type')=='FORECAST' and r.get('source_fixture_date')==a.date}
    matches,pages=get_schedule(a.date,token)
    output=[]
    for f in forecasts.values():
        scored=[]
        for m in matches:
            h=difflib.SequenceMatcher(None,normalize(f['home_team']),normalize(m.get('h'))).ratio()
            v=difflib.SequenceMatcher(None,normalize(f['away_team']),normalize(m.get('a'))).ratio()
            scored.append((round((h+v)/2,3),m))
        scored.sort(key=lambda t:t[0],reverse=True)
        best=scored[:3]
        output.append({'league':f['league'],'home':f['home_team'],'away':f['away_team'], 'candidates':[{'id':str(m.get('id')),'home':m.get('h'),'away':m.get('a'),'league':m.get('l'),'start_source_local':m.get('start'),'similarity':score} for score,m in best]})
    print(json.dumps({'date':a.date,'schedule_rows':len(matches),'pages':pages,'forecast_fixtures':len(forecasts),'candidate_matches':output,'crown_quotes':0,'telegram':False},ensure_ascii=False))
if __name__=='__main__': main()
