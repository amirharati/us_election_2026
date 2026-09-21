"""Date/contest-matched historical Senate benchmarks from publisher archives."""
from pathlib import Path
from datetime import datetime,timezone
import json
import numpy as np
import pandas as pd
import simple_bayesian_polling as v1
import coverage_balance as scoring
from compare_current_forecasts import NAMES as STATE_NAMES

SOURCE='20260920T013619.322700Z'
FILES={2018:'538_2018_state_archive.csv',2020:'538_2020_archive.csv',2022:'538_2022_archive_late.csv'}
NATIONAL={2018:'538_2018_national_archive.csv',2020:'538_2020_national_archive.csv',2022:'538_2022_national_archive.csv'}
SOURCES={2018:'https://github.com/fivethirtyeight/data/tree/master/senate-forecast-2018',2020:'https://github.com/fivethirtyeight/data/tree/master/election-forecasts-2020',2022:'https://github.com/fivethirtyeight/data/tree/master/election-forecasts-2022',2024:'https://www.racetothewh.com/senate/24'}

def dates_2024(labels):
    # Publisher omits year; anchor the final Nov5 point to election2024 and walk backward.
    md=[datetime.strptime(x+' 2024','%b %d %Y') for x in labels];year=2024;out=[];prev=None
    for x in md[::-1]:
        if prev is not None and (x.month,x.day)>(prev.month,prev.day):year-=1
        out.append(pd.Timestamp(year,x.month,x.day));prev=x
    return out[::-1]

def latest(q,date,max_age=0):
    q=q[q.forecast_date.le(pd.Timestamp(date))]
    if q.empty:return q
    chosen=q.forecast_date.max()
    return q[q.forecast_date.eq(chosen)] if (pd.Timestamp(date)-chosen).days<=max_age else q.iloc[:0]

def normalize_538(raw,year):
    out=[]
    if year==2018:
        for (date,state,cl,special,model),q in raw.groupby(['forecastdate','state','class','special','model']):
            d=q[q.party.eq('D')];r=q[q.party.eq('R')]
            if len(d)!=1 or len(r)!=1:continue
            out.append(dict(cycle=year,forecast_date=pd.Timestamp(date),geography=state,seat_class=int(cl),special=bool(special),model='538_'+model,p_dem=float(d.win_probability.iloc[0]),prediction_pp=float(d.voteshare.iloc[0]-r.voteshare.iloc[0]),lo80_pp=np.nan,hi80_pp=np.nan))
    else:
        q=raw.copy();q['forecast_date']=pd.to_datetime(q.forecastdate,format='%m/%d/%y');q['geography']=q.district.str[:2];q['seat_class']=q.district.str.extract(r'S(\d)')[0].astype(int)
        for r in q.itertuples():
            # Compatible target is exactly one D versus one R. Exclude independent contenders.
            if pd.isna(r.name_D1) or pd.isna(r.name_R1) or pd.notna(r.name_D2) or pd.notna(r.name_R2) or r.winner_I1>.001:continue
            margin=r.voteshare_mean_D1-r.voteshare_mean_R1
            if abs(margin-r.mean_netpartymargin)>.002:continue
            out.append(dict(cycle=year,forecast_date=r.forecast_date,geography=r.geography,seat_class=r.seat_class,special=r.seat_class!=((year-2)%6//2+1),model='538'+r.expression,p_dem=r.winner_Dparty,prediction_pp=margin,lo80_pp=r.p10_netpartymargin,hi80_pp=r.p90_netpartymargin))
    return pd.DataFrame(out)

def rttwh_history(path,name_to_code):
    data=json.loads(Path(path).read_text());rows=[]
    for state,sheet in zip(data['sheetNames'],data['data']):
        if state not in name_to_code or state in ['Maine','Vermont','Nebraska','Wyoming']:continue # Independent or no D contender; NE special has separate name.
        dates=dates_2024([r[0] for r in sheet[1:]])
        for date,r in zip(dates,sheet[1:]):
            rows.append(dict(cycle=2024,forecast_date=date,geography=name_to_code[state],seat_class=1,special=False,model='RacetotheWH',p_dem=float(r[1].strip('%'))/100,prediction_pp=np.nan,lo80_pp=np.nan,hi80_pp=np.nan,candidate_D=sheet[0][1],candidate_R=sheet[0][2]))
    return pd.DataFrame(rows)

def score(q):
    q=q.copy();q['actual_pp']=100*q.actual;q['absolute_error_pp']=abs(q.prediction_pp-q.actual_pp);q['brier']=(q.p_dem-q.actual.gt(0))**2
    # Classify by published win probability for all sources; keep mean-sign metric separate.
    q['correct']=q.p_dem.gt(.5).eq(q.actual.gt(0)).astype(float);q.loc[q.p_dem.eq(.5)|q.p_dem.isna(),'correct']=np.nan
    q['mean_sign_correct']=np.where(q.prediction_pp.notna(),q.prediction_pp.gt(0).eq(q.actual.gt(0)),np.nan)
    q['coverage80']=np.where(q.lo80_pp.notna()&q.hi80_pp.notna(),q.actual_pp.between(q.lo80_pp,q.hi80_pp),np.nan)
    q['interval_score80']=scoring.interval_score(q.actual_pp,q.lo80_pp,q.hi80_pp,.2)
    return q

def aggregate(q,keys):
    return q.groupby(keys,as_index=False).agg(n=('target_id','size'),expected_D_in_matched_contests=('p_dem',lambda x:x.sum(min_count=1)),actual_D_in_matched_contests=('actual',lambda x:x.gt(0).sum()),correct=('correct','sum'),classified=('correct','count'),accuracy=('correct','mean'),mean_sign_correct=('mean_sign_correct','sum'),mae_pp=('absolute_error_pp','mean'),brier=('brier','mean'),interval_n=('coverage80','count'),coverage80=('coverage80','mean'),interval_score80=('interval_score80','mean'))

def build(lab):
    lab=Path(lab).resolve();root=lab/'reports/published_forecasts';raw=root/'raw';src=lab/'reports/national_feature_prior'/SOURCE;up=Path(json.loads((src/'settings.json').read_text())['upstream']);out=root/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ');out.mkdir(parents=True)
    local=pd.read_parquet(src/'predictions.parquet');local=local[local.model.isin(['none','both'])];seats=pd.read_parquet(src/'seats.parquet');nb=pd.read_parquet(up/'nonbayesian_predictions.parquet');nb=nb[nb.model.eq('bias')]
    # Existing project STATE_NAMES maps postal codes to full names.
    name_to_code={v:k for k,v in STATE_NAMES.items()}
    ext=pd.concat([*[normalize_538(pd.read_csv(raw/name),year) for year,name in FILES.items()],rttwh_history(raw/'rttwh_2024_trend.json',name_to_code)],ignore_index=True)
    ext['source_url']=ext.cycle.map(SOURCES);ext.to_parquet(out/'publisher_history.parquet',index=False)
    pairs=[];admissions=[];nats=[]
    for (sc,year),loc in local[local.cycle.isin([2018,2020,2022,2024])].groupby(['scenario','cycle']):
        base=loc[loc.model.eq('both')].sort_values('target_id');date=pd.Timestamp(base.as_of.iloc[0]);regular=((year-2)%6//2+1)
        for publisher,allq in ext[ext.cycle.eq(year)].groupby('model'):
            q=latest(allq,date,6 if year==2024 else 0);q=q[q.seat_class.eq(regular)&~q.special]
            if q.geography.duplicated().any():raise ValueError('Ambiguous publisher contest mapping')
            joined=base[['target_id','geography','actual','history_selection_10pp']].merge(q,on='geography',validate='one_to_one');key=f'{year}_{sc}_{publisher}'
            for r in base.itertuples():admissions.append(dict(comparison=key,scenario=sc,cycle=year,publisher=publisher,target_id=r.target_id,geography=r.geography,included=r.target_id in set(joined.target_id),reason='matched_regular_D_R' if r.target_id in set(joined.target_id) else 'no_compatible_date_contest_or_party'))
            if joined.empty:continue
            joined=joined.assign(scenario=sc,comparison=key,requested_cutoff=str(date.date()),comparison_date=str(q.forecast_date.iloc[0].date()),date_gap_days=(date-q.forecast_date.iloc[0]).days,provenance='publisher_retrospective_history' if year==2024 else 'archived_publisher_download')
            pairs.append(score(joined))
            for family in ['none','both']:
                z=loc[loc.model.eq(family)&loc.target_id.isin(joined.target_id)].copy();z=z.assign(model='Lab_'+family,comparison=key,requested_cutoff=str(date.date()),comparison_date=str(q.forecast_date.iloc[0].date()),date_gap_days=(date-q.forecast_date.iloc[0]).days,forecast_date=date,source_url=str(src),provenance='retrospective_lab_backtest');pairs.append(score(z))
            n=nb[nb.scenario.eq(sc)&nb.cycle.eq(year)&nb.target_id.isin(joined.target_id)].copy();n['prediction_pp']=100*n.prediction;n['p_dem']=np.nan;n['lo80_pp']=np.nan;n['hi80_pp']=np.nan;n=n.assign(model='Lab_nonbayesian_bias',comparison=key,forecast_date=date,source_url=str(up),comparison_date=str(q.forecast_date.iloc[0].date()),date_gap_days=(date-q.forecast_date.iloc[0]).days);n=score(n);n['correct']=n.mean_sign_correct;n['brier']=np.nan;pairs.append(n)
        if year in NATIONAL:
            nn=pd.read_csv(raw/NATIONAL[year]);nn['forecast_date']=pd.to_datetime(nn.forecastdate,format='%Y-%m-%d' if year==2018 else '%m/%d/%y');nn=latest(nn,date)
            for er in nn.itertuples():
                if year==2018 and er.party!='D':continue
                model='538_'+er.model if year==2018 else '538'+er.expression;expected=er.mean_seats if year==2018 else er.mean_seats_Dparty;lo=er.p10_seats if year==2018 else er.p10_seats_Dparty;hi=er.p90_seats if year==2018 else er.p90_seats_Dparty
                actual=seats[seats.scenario.eq(sc)&seats.cycle.eq(year)&seats.model.eq('both')].actual_D.iloc[0]
                nats.append(dict(scenario=sc,cycle=year,model=model,forecast_date=str(date.date()),expected_D=expected,actual_D=actual,expected_seat_error=abs(expected-actual),lo80_D=lo,hi80_D=hi,scope='publisher_full_chamber',source_url=SOURCES[year]))
        else:
            d=json.loads((raw/'rttwh_2024_national_trend.json').read_text());sheet=d['data'][d['sheetNames'].index('Projected Seats')];qq=pd.DataFrame(sheet[1:],columns=sheet[0]);qq['forecast_date']=dates_2024(qq.iloc[:,0].tolist());qq=latest(qq,date,6)
            er=qq.iloc[0];val=float(er.iloc[1]);actual=47
            nats.append(dict(scenario=sc,cycle=year,model='RacetotheWH',forecast_date=str(er.forecast_date.date()),expected_D=val,actual_D=actual,expected_seat_error=abs(val-actual),lo80_D=np.nan,hi80_D=np.nan,scope='publisher_retrospective_full_chamber',source_url=SOURCES[year]))
        for family in ['none','both']:
            sr=seats[seats.scenario.eq(sc)&seats.cycle.eq(year)&seats.model.eq(family)].iloc[0]
            fr=pd.read_parquet(src/'folds.parquet');fr=fr[fr.scenario.eq(sc)&fr.cycle.eq(year)&fr.model.eq(family)].iloc[0];freq=np.load(src/fr.forecast_path)['seat_count_frequency'];cdf=np.cumsum(freq)/freq.sum();lo=int(np.searchsorted(cdf,.1));hi=int(np.searchsorted(cdf,.9))
            nats.append(dict(scenario=sc,cycle=year,model='Lab_'+family,forecast_date=str(date.date()),expected_D=sr.expected_D_exact,actual_D=sr.actual_D,expected_seat_error=sr.expected_seat_error,lo80_D=lo,hi80_D=hi,scope='lab_chamber_with_fixed_excluded_contest_completion',source_url=str(src)))
    p=pd.concat(pairs,ignore_index=True);a=pd.DataFrame(admissions);national=pd.DataFrame(nats)
    # Economist: released Oct31 correction; only contemporaneous last row, not corrected back-history.
    eco=[]
    for state in ['AZ','GA','NV','PA']:
        e=pd.read_csv(raw/f'economist_2022_{state.lower()}.csv');e['forecast_date']=pd.to_datetime(e.date);e=latest(e,'2022-10-31',1);loc=local[local.cycle.eq(2022)&local.scenario.eq('oct31')&local.geography.eq(state)]
        if e.empty or loc.empty:continue
        er=e.iloc[0];base=loc[loc.model.eq('both')].iloc[0]
        for label,prob in [('Economist_corrected',er.new_dem_win_prob),('Lab_both',base.p_dem),('Lab_none',loc[loc.model.eq('none')].p_dem.iloc[0])]:eco.append(dict(cycle=2022,geography=state,target_id=base.target_id,model=label,p_dem=float(prob),actual=base.actual,prediction_pp=np.nan,lo80_pp=np.nan,hi80_pp=np.nan,forecast_date='2022-10-30' if label.startswith('Economist') else '2022-10-31',published_model_change_date='2022-10-31',source_url='https://github.com/TheEconomist/us-midterms-2022-change-data',note='Corrected back-history before Oct31 excluded; explicit two-party vote margins not compared to full-vote lab margins'))
    eco=score(pd.DataFrame(eco)) if eco else pd.DataFrame()
    for name,table in dict(matched_predictions=p,admissions=a,state_summary=aggregate(p,['comparison','scenario','cycle','model']),competitive_summary=aggregate(p[p.history_selection_10pp.eq(True)],['comparison','scenario','cycle','model']),national_comparison=national,economist_matched=eco,economist_summary=aggregate(eco,['cycle','model'])).items():table.to_parquet(out/f'{name}.parquet',index=False)
    used=[*FILES.values(),*NATIONAL.values(),'rttwh_2024_trend.json','rttwh_2024_national_trend.json',*[f'economist_2022_{s}.csv' for s in ['az','ga','nv','pa']]]
    st=dict(source=str(src),source_manifest=v1.verify(src),upstream=str(up),upstream_manifest=v1.verify(up),raw_directory=str(raw),raw_sha256={n:v1.sha(raw/n) for n in used},date_rule='latest <= lab cutoff; exact for538, max6days for RTTWH five-day history',election_year_assignment='RTTWH month/day dates anchored final Nov5 to2024, reverse chronological wrap to2023',no_promotion=True)
    v1.json_write(out/'settings.json',st);v1.manifest(out);audit(out);v1.manifest(out);v1.json_write(root/'latest.json',dict(artifact=out.name,manifest_sha256=v1.verify(out)));print('COMPLETE',out,flush=True);return out

def audit(out):
    out=Path(out);v1.verify(out);st=json.loads((out/'settings.json').read_text());p=pd.read_parquet(out/'matched_predictions.parquet');q=p[~p.model.str.startswith('Lab')];counts=p.groupby(['comparison','model']).target_id.apply(frozenset).groupby('comparison').nunique()
    c=dict(sources_preserved=v1.verify(st['source'])==st['source_manifest'] and v1.verify(st['upstream'])==st['upstream_manifest'],raw_preserved=all(v1.sha(Path(st['raw_directory'])/n)==h for n,h in st['raw_sha256'].items()),same_targets=bool(counts.eq(1).all()),unique_predictions=not p.duplicated(['comparison','model','target_id']).any(),past_publication=bool(q.forecast_date.le(pd.to_datetime(q.requested_cutoff)).all()),bounded_staleness=bool(q.date_gap_days.le(6).all()),finite_probability=bool(q.p_dem.between(0,1).all()),valid_labels=bool(p.actual.notna().all()),probability_scores=bool(np.allclose(q.brier,(q.p_dem-q.actual.gt(0))**2)),no_synthetic_nonbayesian_probabilities=bool(p[p.model.eq('Lab_nonbayesian_bias')].p_dem.isna().all()))
    result=dict(passed=all(c.values()),checks=c,matched_rows=len(p),comparisons=p.comparison.nunique());v1.json_write(out/'audit.json',result)
    if not result['passed']:raise AssertionError(c)
    return result

if __name__=='__main__':build(Path(__file__).resolve().parents[1])
