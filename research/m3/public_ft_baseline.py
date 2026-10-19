"""M3 independent FT LightGBM research; never imports M1/M2/MR1 or sends TG."""
import argparse,io,json
from pathlib import Path
import pandas as pd,numpy as np
from lightgbm import LGBMRegressor
from sklearn.metrics import log_loss

def load(data,league):
    d=pd.read_csv(io.BytesIO(data),low_memory=False)
    req=['Date','HomeTeam','AwayTeam','FTHG','FTAG']
    if any(c not in d for c in req):raise ValueError('FT columns missing')
    d=d[req].copy();d['Date']=pd.to_datetime(d.Date,dayfirst=True,errors='coerce')
    for c in ('FTHG','FTAG'):d[c]=pd.to_numeric(d[c],errors='coerce')
    d=d.dropna(subset=req);d=d[(d.FTHG>=0)&(d.FTAG>=0)];d['league']=league
    return d

def feature_rows(d):
    history={};out=[]
    for day,group in d.sort_values('Date').groupby('Date',sort=True):
        updates=[]
        for r in group.itertuples(index=False):
            keys=((r.league,r.HomeTeam),(r.league,r.AwayTeam))
            xs=[history.get(k,[])[-10:] for k in keys]
            vals=[]
            for x in xs:vals += [len(x),np.mean([v[0] for v in x]) if x else 1.3,np.mean([v[1] for v in x]) if x else 1.3]
            out.append([day.year,*vals,int(r.FTHG),int(r.FTAG)])
            updates.append((keys,int(r.FTHG),int(r.FTAG)))
        for (hk,ak),h,a in updates:
            history.setdefault(hk,[]).append((h,a))
            history.setdefault(ak,[]).append((a,h))
    return pd.DataFrame(out,columns=['year','hn','hf','ha','an','af','aa','hg','ag'])

def poisson_cdf2(rate):
    return np.exp(-rate)*(1+rate+rate*rate/2)

def run(files):
    rows=[load(p.read_bytes(),p.stem.split('_')[0]) for p in files]
    if not rows:raise ValueError('No independent M3 CSV')
    f=feature_rows(pd.concat(rows,ignore_index=True))
    years=sorted(f.year.unique())
    if len(years)<3:raise ValueError('Insufficient chronological years')
    train=f[f.year<years[-1]];test=f[f.year==years[-1]]
    features=['hn','hf','ha','an','af','aa']
    estimates=[]
    for col in ('hg','ag'):
        model=LGBMRegressor(n_estimators=120,num_leaves=8,learning_rate=.04,min_child_samples=15,verbosity=-1,random_state=2026)
        model.fit(train[features],train[col])
        estimates.append(np.clip(model.predict(test[features]),.05,6))
    home,away=estimates
    over=np.clip(1-poisson_cdf2(home+away),1e-6,1-1e-6)
    from math import factorial
    k=np.arange(18);fact=np.array([factorial(int(i)) for i in k])
    ah=[]
    for h,a in zip(home,away):
        hp=np.exp(-h)*h**k/fact;ap=np.exp(-a)*a**k/fact
        ah.append(sum(hp[i]*sum(ap[:i]) for i in range(18)))
    ah=np.clip(ah,1e-6,1-1e-6)
    return {'protocol':'M3_INDEPENDENT_FT_LIGHTGBM_V1','model':'M3',
        'data_source':'independent public football-data.co.uk FT, not Crown odds',
        'train_rows':len(train),'test_rows':len(test),'test_year':int(years[-1]),
        'ou_over25_logloss':float(log_loss((test.hg+test.ag>2).astype(int),over,labels=[0,1])),
        'ah_home_win_logloss':float(log_loss((test.hg>test.ag).astype(int),ah,labels=[0,1])),
        'ah_note':'Home win diagnostic only, not Asian handicap ROI',
        'crown_verified':False,'asian_ah_roi':None,'asian_ou_roi':None,'telegram_sent':0}
def main():
    a=argparse.ArgumentParser();a.add_argument('--data-dir',required=True);a.add_argument('--output',required=True);opts=a.parse_args()
    paths=list(Path(opts.data_dir).glob('*.csv'))
    report=run(paths);out=Path(opts.output);out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
