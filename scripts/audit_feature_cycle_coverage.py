"""Audit every accepted cycle against separate feature streams; no predictor joins.

Periods measure reference-data presence, NOT publication availability or complete
within-month sampling. Daily/weekly/irregular sources are audited by month presence.
"""
from pathlib import Path
import json
import pandas as pd
import numpy as np
from data_utils import LAB,Snapshot,csv_bytes,digest

FEATURES='20260917T051031.539083Z'
ACCEPTED='20260917T031058.249642Z'
AS_OF=pd.Timestamp('2026-09-17')
FEATURE_NAMES={'F01':'Economic sentiment','F02':'Personal finances / expectations','F03':'Prices / inflation inputs',
 'F04':'Real income','F05':'Employment','F06':'Real GDP','F07':'Overall / issue approval','F08':'Approval by respondent party',
 'F09':'Market returns / levels','F10':'Volatility / financial stress','F11':'Geopolitical risk / conflict',
 'F12':'Issue salience','F13':'Health disruption / proxies','F14':'Policy / social disruption','F15':'Policy uncertainty'}


def cycle_windows(polls,outcomes,calendar):
    years=sorted(set(calendar.cycle)|set(polls.cycle)|set(outcomes.cycle))
    result=[]
    for y in years:
        p=polls[polls.cycle==y];o=outcomes[outcomes.cycle==y]
        dates=pd.concat([pd.to_datetime(p[c]) for c in ['poll_start','poll_end','poll_date']]).dropna()
        start=pd.Timestamp(y-1,1,1);end=min(pd.Timestamp(y,12,31),AS_OF)
        first=dates.min() if len(dates) else pd.NaT;last=dates.max() if len(dates) else pd.NaT
        a=min(start,first) if pd.notna(first) else start;z=max(end,last) if pd.notna(last) else end
        z=min(z,AS_OF)
        result.append(dict(cycle=int(y),standard_start=start,standard_end=end,audit_start=a,audit_end=z,
                           first_poll_date=first,last_poll_date=last,poll_rows=len(p),outcome_rows=len(o),
                           recent_priority=int(y>=2016),odd_special_cycle=int(y%2==1),
                           expanded_for_poll_dates=bool(a<start or z>end)))
    return pd.DataFrame(result)


def period_coverage(dates,valid,windows,freq='M',kind='series',covid_specific=False):
    dates=pd.to_datetime(dates,errors='raise'); observed=dates[valid].dropna()
    earliest=observed.min();latest=observed.max()
    observed_bins=set(observed.dt.to_period(freq).astype(str))
    rows=[]
    for w in windows.to_dict('records'):
        start,end=w['audit_start'],w['audit_end']
        expected=pd.period_range(start,end,freq=freq)
        # The unfinished terminal reference period is reported, not called a gap.
        expected=[p for p in expected if p.end_time.normalize()<=end]
        keys={str(p) for p in expected};have=keys&observed_bins
        in_window=dates.between(start,end);n=int((in_window&valid).sum())
        if n:
            status='observed_irregular' if kind in ('survey','event','document') else 'all_reference_bins_present' if len(have)==len(keys) else 'partial_reference_bins'
        elif covid_specific and end<pd.Timestamp('2020-01-01'):status='not_applicable_pre_covid'
        elif pd.isna(earliest):status='no_numeric_observations_in_download'
        elif end<earliest:status='before_observed_history'
        elif start>latest:status='after_last_observation'
        else:status='gap_within_observed_history'
        rows.append(dict(cycle=w['cycle'],recent_priority=w['recent_priority'],audit_start=start,audit_end=end,
                         status=status,observed_rows=n,missing_numeric_rows=int((in_window&~valid).sum()),
                         observed_dates=int(dates[in_window&valid].nunique()),reference_bin=freq,
                         expected_closed_bins=len(keys),bins_with_values=len(have),missing_bins='|'.join(sorted(keys-have)),
                         presence_fraction=len(have)/len(keys) if keys else np.nan,
                         first_observed=earliest,last_observed=latest,kind=kind,
                         completeness_note='Irregular observations do not establish exhaustive coverage' if kind in ('survey','event','document') else
                                           'Daily/weekly sources: month presence only; not daily completeness or as-of availability'))
    return rows


def family(table,series='',group=''):
    source=table.split('/')[0]
    if source in ('fred','bea','bls','oecd'):
        return {'CPIAUCSL':'F03','CUSR0000SA0':'F03','PCEPI':'F03','A229RX0':'F04','UNRATE':'F05','LNS14000000':'F05',
                'GDPC1':'F06','NASDAQCOM':'F09','STLFSI4':'F10','USACSCICP02STSAM':'F01'}[series]
    if source=='michigan':return 'F01' if table.endswith(('1a','5b')) else 'F02'
    if source=='ucsb':return 'F07' if group=='all' else 'F08'
    return {'silver_bulletin':'F07','cboe':'F10','french':'F09','gpr':'F11','ucdp':'F11','epu':'F15',
            'infectious_emv':'F13','cdc':'F13','cdc_nhsn':'F13','who':'F13','owid':'F13','oxcgrt':'F14',
            'policy_agendas':'F12','yougov':'F12'}[source]


def build():
    snap=LAB/'data/features_prepared/snapshots'/FEATURES
    accepted=LAB/'data/accepted/snapshots'/ACCEPTED
    catalog=json.loads((snap/'catalog.json').read_text());manifest=json.loads((snap/'manifest.json').read_text())
    for e in catalog.values():assert digest((snap/e['path']).read_bytes())==manifest['files'][e['path']]['sha256']
    polls=pd.read_csv(accepted/'tables/observations.csv',usecols=['cycle','poll_start','poll_end','poll_date'])
    outcomes=pd.read_csv(accepted/'tables/outcomes.csv',usecols=['cycle'])
    calendar=pd.read_csv(accepted/'tables/state_calendar.csv',usecols=['cycle'])
    windows=cycle_windows(polls,outcomes,calendar)
    records=[];inventory=[];geographies=[]
    def add(table,series,group,df,value='value',freq='M',kind='series',unit='',covid=False,restriction=''):
        ident=f'{table}::{series}::{group}'
        fid=family(table,series,group)
        valid=df[value].notna() if value else pd.Series(True,index=df.index)
        dates=df['date'];rs=period_coverage(dates,valid,windows,freq,kind,covid)
        inventory.append(dict(stream_id=ident,feature_id=fid,feature_name=FEATURE_NAMES[fid],table=table,series=series,
                              group=group,unit=unit,scope='national or explicitly named subgroup; global for conflict/news risk',
                              restriction=restriction))
        for r in rs:r.update(stream_id=ident,feature_id=fid,table=table,series=series,group=group,unit=unit,restriction=restriction)
        records.extend(rs)
    for table,meta in catalog.items():
        source=table.split('/')[0]
        if source=='congress':continue # entity attributes/terms; new political daily table audited separately
        # Read only required UCDP columns, to keep the event audit quick and bounded.
        cols=['date_end','id','country','archive_kind','best'] if source=='ucdp' else None
        df=pd.read_csv(snap/meta['path'],usecols=cols,low_memory=False)
        date_col=next(c for c in ['date','end_date','date_end'] if c in df)
        df['date']=pd.to_datetime(df[date_col])
        if source=='ucdp':
            for group,q in df.groupby('archive_kind'):add(table,'event_best_fatalities',group,q,'best',kind='event',unit='deaths',restriction='Global event occurrence, not absence-of-war certification; provisional and finalized separate')
            continue
        if source=='ucsb':
            for (measure,party),q in df.groupby(['measure','respondent_party']):
                add(table,measure,party,q,kind='survey',unit='fraction',restriction='Changing presidents/methods; party interpolation/subgroup N unresolved')
            continue
        if source=='silver_bulletin':
            for (sub,pop),q in df.groupby(['subgroup','population'],dropna=False):
                for metric in ['approve_fraction','disapprove_fraction','net_fraction','adjusted_approve_fraction','adjusted_disapprove_fraction','adjusted_net_fraction']:
                    add(table,metric,f'{sub}/{pop}',q,metric,kind='survey',unit='fraction',restriction='No pooling across subgroup types; shared samples unresolved')
            continue
        if source=='yougov':
            add(table,'scalar_topline_candidates','all_questions_review_only',df,kind='document',unit='fraction',restriction='Not certified feature coverage; question/party/crosstab mapping pending')
            continue
        if source=='gpr' and table.endswith('event_annotations'):
            add(table,'publisher_annotations','global',df,None,kind='event',restriction='Selected annotations, not exhaustive event history');continue
        if 'series' in df and 'value' in df:
            grouping=['series']+(['group'] if 'group' in df else [])
            for key,q in df.groupby(grouping,dropna=False):
                key=key if isinstance(key,tuple) else (key,)
                series=key[0];group=str(key[1]) if len(key)>1 else 'all'
                precision=q.date_precision.iloc[0];freq={'quarter':'Q','year':'Y'}.get(precision,'M')
                kind='survey' if source=='michigan' else 'series'
                restriction=('MIP raw annual totals fail unity in some years; no renormalization' if source=='policy_agendas' else
                             'Publisher basis/series definitions remain separate; no vintage certification')
                add(table,series,group,q,freq=freq,kind=kind,unit=q.unit.iloc[0],restriction=restriction)
            continue
        numeric=[c for c,v in meta.get('source_columns',{}).items() if v['type']=='number']
        if source in ('cdc','cdc_nhsn','oxcgrt','owid','who'):
            geo=next((c for c in ['geographic_aggregation','state','regioncode','country_code','country'] if c in df),None)
            if geo:
                for group,q in df.groupby(geo,dropna=False):
                    geographies.append(dict(table=table,geography=str(group),rows=len(q),first=q.date.min(),last=q.date.max(),
                                            note='Row-date inventory only; metric presence may differ; no state coverage inferred from national'))
            if source=='cdc':df=df[df.state=='United States']
            elif source=='cdc_nhsn':df=df[df.geographic_aggregation=='USA']
            elif source=='oxcgrt':df=df[df.regioncode.isna() & df.jurisdiction.eq('NAT_TOTAL')]
            assert len(df),f'No explicit national rows in {table}'
        groups=['type','outcome'] if source=='cdc' else []
        iterator=df.groupby(groups,dropna=False) if groups else [('US' if source!='cboe' else 'market',df)]
        for group,q in iterator:
            for metric in numeric:
                u=meta['source_columns'][metric].get('unit','source_unit')
                covid=(source in ('who','oxcgrt') or source=='owid' and any(k in metric for k in ('cases','deaths','vaccin','hosp','icu','test')))
                add(table,metric,str(group),q,metric,unit=u,covid=covid,
                    restriction='National only; state/geography inventory separate. Absence is not zero; release dates unknown')
    # Political context is complete day-granular coverage, not inferred from legislature row counts.
    root=LAB/'data/political_context/prepared';pp=root/json.loads((root/'latest.json').read_text())['snapshot']
    political=pd.read_csv(pp/'daily_context.csv',parse_dates=['date'])
    control=[]
    for w in windows.to_dict('records'):
        q=political[political.date.between(w['audit_start'],w['audit_end'])]
        days=(w['audit_end']-w['audit_start']).days+1
        assert len(q)==days,('Political gap',w['cycle'])
        row={**w,'control_days':len(q),'control_complete':True,'reference_only_not_forecast_input':True}
        for col in ['wh_party','house_party','senate_party']:
            row[col+'_at_start']=q[col].iloc[0];row[col+'_at_cutoff']=q[col].iloc[-1]
            row[col+'_dem_day_fraction']=q[col].eq('DEM').mean();row[col+'_rep_day_fraction']=q[col].eq('REP').mean()
            row[col+'_changes']=int(q[col].ne(q[col].shift()).sum()-1)
        row['unified_day_fraction']=q.unified_government.mean();row['presidential_election_cycle']=int(w['cycle']%4==0)
        row['midterm_cycle']=int(w['cycle']%4==2);control.append(row)
    coverage=pd.DataFrame(records);streams=pd.DataFrame(inventory)
    assert not coverage.duplicated(['stream_id','cycle']).any()
    assert len(coverage)==len(streams)*len(windows)
    families=[]
    for fid,title in FEATURE_NAMES.items():
        for w in windows.to_dict('records'):
            q=coverage[(coverage.feature_id==fid)&(coverage.cycle==w['cycle'])]
            present=q[q.observed_rows>0]
            families.append(dict(feature_id=fid,feature_name=title,cycle=w['cycle'],recent_priority=w['recent_priority'],
                                 streams=len(q),streams_with_values=len(present),sources_with_values='|'.join(sorted(set(present.table.str.split('/').str[0]))),
                                 presence='some_observations_not_full_certification' if len(present) else 'no_observations',
                                 absent_statuses='|'.join(sorted(set(q.loc[q.observed_rows==0,'status'])))))
    # Alternative providers are explicitly absent across all cycles, not silently forgotten.
    sys_sources={'ipsos':['F02','F07','F08','F12'],'ap_norc':['F02','F07','F08','F12'],'gallup':['F01','F07','F08','F12'],
                 'conference_board':['F01'],'roper':['F07','F08','F12'],'gtd':['F11'],'acled':['F14'],'fivethirtyeight':['F07']}
    unavailable=[dict(source=s,feature_ids='|'.join(fs),cycle=int(y),status='not_acquired',not_zero=True) for s,fs in sys_sources.items() for y in windows.cycle]
    with Snapshot(LAB/'data/feature_cycle_coverage','feature_cycle_coverage') as out:
        for name,data in [('cycle_windows',windows),('stream_inventory',streams),('stream_cycle_coverage',coverage),
                          ('family_cycle_presence',pd.DataFrame(families)),('geography_inventory',pd.DataFrame(geographies)),
                          ('political_cycle_reference',pd.DataFrame(control)),('unacquired_source_cycles',pd.DataFrame(unavailable))]:
            out.add(name+'.csv',data.to_csv(index=False,date_format='%Y-%m-%d').encode())
        out.add('recipe.py',Path(__file__).read_bytes())
        out.write_json('inputs.json',{'feature_snapshot':FEATURES,'accepted_snapshot':ACCEPTED,'as_of':str(AS_OF.date()),
                                    'feature_manifest_sha256':digest((snap/'manifest.json').read_bytes()),
                                    'accepted_manifest_sha256':digest((accepted/'manifest.json').read_bytes()),
                                    'political_snapshot':str(pp.relative_to(LAB))})
        return out.finish({'cycles':len(windows),'first_cycle':int(windows.cycle.min()),'last_cycle':int(windows.cycle.max()),
                           'streams':len(streams),'stream_cycle_rows':len(coverage),'feature_families':len(FEATURE_NAMES),
                           'political_days':len(political),'political_cycles_complete':len(control),
                           'older_cycles_retained':True,'aligned_to_polls':False})

if __name__=='__main__':build()
