"""Normalize archived public 2026 forecasts; preserve date/party/basis limitations."""
from pathlib import Path
import json,re
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from compare_current_forecasts import race_rows,NAMES,ABBR,RACE_URL,SILVER_URL
import simple_bayesian_polling as v1
FEATURE='20260920T013619.322700Z'
PROXY_STATES={'ID','MT','NE','SD'}

def flight_text(html):
    parts=[]
    for script in BeautifulSoup(html,'html.parser').find_all('script'):
        text=script.string or ''
        if text.startswith('self.__next_f.push('):
            value=json.loads(text[len('self.__next_f.push('):-1])
            if len(value)>1 and isinstance(value[1],str):parts.append(value[1])
    return ''.join(parts)

def ddhq_forecast(html):
    text=flight_text(html);matches=list(re.finditer(r'"forecast":',text));decoded=[]
    for m in matches:
        try:value,_=json.JSONDecoder().raw_decode(text[m.end():].lstrip())
        except json.JSONDecodeError:continue
        if isinstance(value,dict) and 'parties' in value:decoded.append(value)
    unique={json.dumps(x,sort_keys=True):x for x in decoded}
    if len(unique)!=1:raise ValueError(f'Expected unique published race forecast, found {len(unique)}')
    return next(iter(unique.values()))

def build(out,lab):
    out,lab=Path(out),Path(lab)
    if (out/'manifest.json').exists():raise FileExistsError('Use a new raw archive; do not mutate a completed review')
    raw=out/'raw';src=lab/'reports/national_feature_prior'/FEATURE
    rp=json.loads((raw/'rttwh_live.json').read_text());r,candidates=race_rows(rp);rows=[];update=rp['data'][3][0][0]
    for x in r.itertuples():
        rows.append(dict(publisher='Race to the WH',state=x.state,p_dem=x.race_D_probability/100,p_rep=x.race_R_probability/100,p_ind=x.race_I_probability/100,margin_pp=x.race_margin_DR_pp,updated=update,source_url=RACE_URL,compatible=x.state not in PROXY_STATES,margin_basis=x.race_margin_basis))
    for path in raw.glob('ddhq_*.html'):
        state=next(s for s,name in NAMES.items() if path.name.startswith('ddhq_'+name.lower().replace(' ','-')+'-us-senate'))
        d=ddhq_forecast(path.read_text());parties={x['shortAbbrev']:x for x in d['parties']};dem=parties.get('D',{});rep=parties.get('R',{});ind=parties.get('I',{});url='https://votes.decisiondeskhq.com/races/2026-11-03/'+path.stem.removeprefix('ddhq_')+'/forecast'
        rows.append(dict(publisher='DDHQ',state=state,p_dem=dem.get('winProbability',np.nan),p_rep=rep.get('winProbability',np.nan),p_ind=ind.get('winProbability',np.nan),margin_pp=dem.get('margin',np.nan) if state not in PROXY_STATES else np.nan,updated=d['updatedAt'],source_url=url,compatible=state not in PROXY_STATES,margin_basis='publisher_projected_margin_not_harmonized',candidates=json.dumps({k:[y['firstName']+' '+y['lastName'] for y in x['candidates']] for k,x in parties.items()})))
    pub=pd.DataFrame(rows);pub['margin_pp']=pd.to_numeric(pub.margin_pp.map(lambda x:-0.0 if x=='$-0' else x),errors='raise');assert len(pub)==70 and not pub.duplicated(['publisher','state']).any()
    q=pd.read_parquet(src/'predictions.parquet');q=q[q.cycle.eq(2026)&q.model.isin(['none','both'])].rename(columns={'geography':'state'})
    cmp=q[['state','target_id','model','prediction_pp','p_dem','q_pp','historical_bias_pp','prior','posterior_sd_pp']].merge(pub,on='state',suffixes=('_lab','_publisher'),validate='many_to_many')
    cmp['probability_difference_pp']=100*(cmp.p_dem_lab-cmp.p_dem_publisher);cmp.loc[~cmp.compatible,'probability_difference_pp']=np.nan
    cmp['margin_difference_pp']=cmp.prediction_pp-cmp.margin_pp;cmp['call_disagrees']=np.where(cmp.compatible,cmp.p_dem_lab.gt(.5).ne(cmp.p_dem_publisher.gt(.5)),np.nan)
    cmp['lab_as_of']='2026-09-17';cmp['comparison_note']=np.where(cmp.compatible,'Different dates and model definitions; margins descriptive, not exactly harmonized','Independent/ballot proxy: D-vs-R model output is not a literal Democratic candidate win probability')
    silver=BeautifulSoup((raw/'silver.html').read_text(),'html.parser').get_text(' ',strip=True)
    m=re.search(r'chances of retaking the Senate are up to (\d+) percent',silver);assert m
    ddtext=BeautifulSoup((raw/'ddhq.html').read_text(),'html.parser').get_text(' ',strip=True)
    dm=re.search(r'Democrats (\d+)% Probability',ddtext);assert dm
    top=[dict(model='Race to the WH',p_D_control=float(rp['data'][0][1][1].split('%')[0])/100,expected_D=float(rp['data'][1][1][1].split()[0]),updated=update,url=RACE_URL,scope='publisher full chamber'),dict(model='DDHQ',p_D_control=int(dm[1])/100,expected_D=np.nan,updated='2026-09-18, 2:41 PM',url='https://votes.decisiondeskhq.com/forecast/2026/senate',scope='publisher full chamber; displayed51/49 map is not assumed to be expectation'),dict(model='Silver Bulletin Deluxe',p_D_control=int(m[1])/100,expected_D=np.nan,updated='2026-09-19',url=SILVER_URL,scope='public topline only; state forecasts subscriber-only')]
    seats=pd.read_parquet(src/'seats.parquet');folds=pd.read_parquet(src/'folds.parquet')
    for model in ['none','both']:
        s=seats[seats.cycle.eq(2026)&seats.model.eq(model)].iloc[0];f=folds[folds.cycle.eq(2026)&folds.model.eq(model)].iloc[0];freq=np.load(src/f.forecast_path)['seat_count_frequency'];top.append(dict(model='Lab_'+model,p_D_control=freq[51:].sum()/freq.sum(),expected_D=s.expected_D_exact,updated='2026-09-17 inputs',url=str(src),scope='lab conditional caucus/ballot proxies retained'))
    for name,table in dict(published_states=pub,current_comparison=cmp,rttwh_candidates=candidates,current_topline=pd.DataFrame(top)).items():table.to_parquet(out/f'{name}.parquet',index=False)
    print(pd.DataFrame(top).to_string(index=False));print(cmp[cmp.model.eq('both')&cmp.compatible].sort_values('probability_difference_pp')[['state','publisher','p_dem_lab','p_dem_publisher','probability_difference_pp','prediction_pp','margin_pp']].round(3).to_string(index=False))
    return cmp

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('out',type=Path);a=p.parse_args();build(a.out,Path(__file__).resolve().parents[1])
