"""Dated national feature contexts, with separate reference and observed-by-cutoff views."""
from pathlib import Path
import hashlib
import json
import numpy as np
import pandas as pd
from disruption_features import monthly_disruption, nullable_or
from build_political_context import state_on

# One transparent alignment rule, not model/validation tuning.
SPEC = {
 'sentiment':('michigan/RB_1a','consumer_sentiment','all','value','date',1,'index_points'),
 'finances':('michigan/RB_6','better_off','all','value','date',100,'percent'),
 'cpi':('fred/observations','CPIAUCSL','all','value','date',1,'index_1982_84_100_SA'),
 'gasoline':('fred/observations','CUSR0000SETB01','all','value','date',1,'index_1982_84_100_SA'),
 'income':('fred/observations','A229RX0','all','value','date',1,'chained_2017_USD_per_capita_SAAR'),
 'unemployment':('fred/observations','UNRATE','all','value','date',100,'percent'),
 'gdp':('fred/observations','GDPC1','all','value','date',1,'billions_chained_2017_USD_SAAR'),
 'approval_all':('ucsb/approval_observations','approve','all','value','end_date',100,'percent'),
 'approval_dem':('ucsb/approval_observations','approve','DEM','value','end_date',100,'percent'),
 'approval_rep':('ucsb/approval_observations','approve','REP','value','end_date',100,'percent'),
 'market_return':('french/factors_month','Mkt_RF',None,'value','date',100,'percent_excess_return'),
 'vix':('cboe/vix_daily',None,None,'close','date',1,'index_points'),
 'gpr':('gpr/data_gpr_export','GPRH','all','value','date',1,'index_points'),
 'epu':('epu/US_Policy_Uncertainty_Data_main_news_index','News_Based_Policy_Uncert_Index','all','value','date',1,'index_points'),
 'infectious_news':('infectious_emv/infectious_emv','daily_infect_emv_index','all','value','date',1,'index_points'),
 'covid_policy':('oxcgrt/OxCGRT_compact_national_v1',None,None,'stringencyindex_average','date',1,'index_points'),
}
MEANS={'consumer_sentiment_3m':'sentiment','personal_finances_better_3m_pct':'finances',
       'approval_3m_pct':'approval_all','approval_dem_3m_pct':'approval_dem','approval_rep_3m_pct':'approval_rep',
       'market_excess_return_3m_pct':'market_return','vix_3m':'vix','gpr_3m':'gpr','epu_3m':'epu',
       'infectious_news_3m':'infectious_news','covid_stringency_3m':'covid_policy'}
LEVELS={'cpi_level':'cpi','real_income_per_capita':'income','unemployment_pct':'unemployment','real_gdp_level':'gdp'}
GROWTH={'inflation_yoy_pct':'cpi','real_income_yoy_pct':'income','real_gdp_yoy_pct':'gdp'}
LEVELS['gasoline_cpi_level']='gasoline'
GROWTH.update({'gasoline_yoy_pct':'gasoline','cpi_24m_pct':'cpi'})
GROWTH_MONTHS={'cpi_24m_pct':24}  # Other growth features use exact 12-month endpoints.
POLITICAL=['wh_dem','house_dem','senate_dem','unified_government','split_congress',
           'wh_matches_house','wh_matches_senate','president_days_in_office','wh_party_days_in_power']

def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()


def digest_text(value):
    return hashlib.sha256(str(value).encode()).hexdigest()[:24]


def empty_monthly():
    return pd.DataFrame(columns=['value','reference_end','known_by','n','monthly_id'], index=pd.PeriodIndex([],freq='M',name='month'))


class FeatureStore:
    def __init__(self, snapshot, political_config, as_of, records_only=False):
        self.path=Path(snapshot);self.as_of=pd.Timestamp(as_of);self.political=political_config
        self.catalog=json.loads((self.path/'catalog.json').read_text())
        inputs=json.loads((self.path/'inputs.json').read_text())
        self.artifact_order={a['id']:max(pd.Timestamp(o['retrieved_at']).tz_localize(None)
                           for o in a['origins'] if o.get('retrieved_at')) for a in inputs['artifacts']}
        self.artifact_time={a['id']:min(pd.Timestamp(o['retrieved_at']).tz_localize(None).normalize() for o in a['origins'] if o.get('retrieved_at')) for a in inputs['artifacts']}
        self.monthly={};self.selection=[];self.monthly_rows=[];frames={};raw={}
        for key,(table,series,group,value,date,scale,unit) in SPEC.items():
            if table not in self.catalog:
                self.monthly[key]=empty_monthly()
                self.selection.append(dict(series=key,status='source_table_absent'));continue
            if table not in raw:raw[table]=pd.read_csv(self.path/self.catalog[table]['path'],low_memory=False)
            d=raw[table].copy()
            if table.startswith('ucsb'):
                d=d[d.measure.eq(series)&d.respondent_party.eq(group)].copy()
            else:
                if series is not None:d=d[d.series.eq(series)].copy()
                if group is not None:d=d[d.group.eq(group)].copy()
            if key=='covid_policy':d=d[d.regioncode.isna()&d.jurisdiction.eq('NAT_TOTAL')].copy()
            d['_date']=pd.to_datetime(d[date]);d['_end']=pd.to_datetime(d['period_end'] if 'period_end' in d else d[date])
            d['_value']=pd.to_numeric(d[value],errors='raise')*scale
            d['_known']=pd.to_datetime(d.artifact_id.map(self.artifact_time))
            d['_retrieved']=pd.to_datetime(d.artifact_id.map(self.artifact_order))
            frames[key]=d
        # Exact-row dedup can retain an older canonical artifact; track re-observation by newer artifacts.
        ids={r for d in frames.values() for r in d.record_id};reobserved={}
        duplicate=self.path/'audit/duplicate_rows.jsonl'
        if duplicate.exists():
            for line in duplicate.open():
                r=json.loads(line);rid=r['canonical_record_id']
                if rid in ids:
                    t=self.artifact_order[r['artifact_id']]
                    reobserved[rid]=max(reobserved.get(rid,t),t)
        self.records = []
        duplicates = {}
        if duplicate.exists():
            for line in duplicate.open():
                item = json.loads(line)
                duplicates.setdefault(item['canonical_record_id'], set()).add(item['artifact_id'])
        artifacts = {a['id']: a for a in inputs['artifacts']}
        for key, frame in frames.items():
            for row in frame.to_dict('records'):
                for aid in [row['artifact_id'], *sorted(duplicates.get(row['record_id'], set()))]:
                    a = artifacts[aid]
                    scope = 'current' if all('/current_2026/' in o['path'] for o in a['origins']) else 'historical'
                    self.records.append(dict(series_key=key, record_id=row['record_id'],
                        logical_key=row['logical_key'], artifact_id=aid, scope=scope,
                        source=a['source'], _date=row['_date'], _end=row['_end'],
                        _value=row['_value'], _known=self.artifact_time[aid],
                        _retrieved=self.artifact_order[aid], quality_flags=row['quality_flags']))
        if records_only: return
        for key,d in frames.items():
            d['_version']=pd.concat([d['_retrieved'],pd.to_datetime(d.record_id.map(reobserved))],axis=1).max(axis=1)
        self._aggregate(frames)

    @classmethod
    def from_records(cls, records, political_config, as_of):
        """Use normalized model series; no provider archive is needed at runtime."""
        self = cls.__new__(cls)
        self.as_of = pd.Timestamp(as_of); self.political = political_config
        self.catalog = {}; self.monthly = {}; self.selection = []; self.monthly_rows = []
        self.records = records.to_dict('records')
        frames = {}
        for key in SPEC:
            d = records[records.series_key.eq(key)].copy()
            if d.empty:
                self.monthly[key] = empty_monthly()
                self.selection.append(dict(series=key,status='source_table_absent'))
                continue
            # Exact duplicates retain canonical provenance/observation time and
            # latest re-observation time, matching the source normalizer.
            d['_version'] = d.groupby('record_id')._retrieved.transform('max')
            frames[key] = d.drop_duplicates('record_id', keep='first')
        self._aggregate(frames)
        return self

    def _aggregate(self, frames):
        for key,d in frames.items():
            initial=len(d)
            # Latest retrieved version wins within each logical key; conflicting same-date versions stay unknown.
            newest=d.groupby('logical_key')._version.transform('max')
            d=d[d._version.eq(newest)].copy();conflict=d.logical_key.duplicated(keep=False)
            flags=d.quality_flags.fillna('').ne('');invalid=~np.isfinite(d._value)
            self.selection.append(dict(series=key,status='selected',input_rows=initial,older_version_rows=initial-len(d),
                 conflicting_latest_rows=int(conflict.sum()),flagged_rows=int(flags.sum()),missing_rows=int(invalid.sum())))
            # Missing/flagged latest versions do not fall back to an older value.
            d=d[~(conflict|flags|invalid)].copy();d['month']=d._date.dt.to_period('M')
            rows=[]
            for month,q in d.groupby('month'):
                rid=digest_text((key,str(month),'|'.join(sorted(q.record_id))))
                end=max(month.end_time.normalize(),q._end.max())
                row=dict(series=key,month=month,monthly_id=rid,value=q._value.mean(),reference_end=end,
                         known_by=q._known.max(),n=len(q),record_ids='|'.join(sorted(q.record_id)),
                         artifact_ids='|'.join(sorted(set(q.artifact_id))),unit=SPEC[key][-1])
                rows.append(row);self.monthly_rows.append(row)
            self.monthly[key]=pd.DataFrame(rows).set_index('month') if rows else empty_monthly()
        self._finalize()

    @classmethod
    def from_monthly(cls, monthly, political_config, as_of):
        self = cls.__new__(cls)
        self.as_of = pd.Timestamp(as_of); self.political = political_config
        self.catalog = {}; self.selection = []; self.monthly_rows = monthly.to_dict('records')
        self.monthly = {}
        monthly = monthly.copy(); monthly['month'] = pd.PeriodIndex(monthly.month, freq='M')
        for key in SPEC:
            self.monthly[key] = monthly[monthly.series.eq(key)].set_index('month')
        self._finalize()
        return self

    def _finalize(self):
        self.disruption,self.disruption_ledger=monthly_disruption(
            {k:self.monthly[s]['value'] for k,s in [('health','infectious_news'),('financial','vix'),('security','gpr')]},self.as_of)
        self.disruption_known=pd.DataFrame(index=self.disruption.index)
        for component,series in [('health','infectious_news'),('financial','vix'),('security','gpr')]:
            times=self.monthly[series]['known_by'].reindex(self.disruption.index)
            numeric=times.astype('int64').astype(float).where(times.notna())
            self.disruption_known[component]=pd.to_datetime(numeric.rolling(121,min_periods=1).max())
        self.cache={};self.ledger=[]
        self.columns=list(MEANS)+list(LEVELS)+list(GROWTH)+['issue_salience_economy']+POLITICAL+[
            'health_disruption_4y','financial_disruption_4y','security_disruption_4y','extraordinary_event_any_4y']

    def at(self, cutoff):
        cutoff=pd.Timestamp(cutoff).normalize()
        if cutoff>self.as_of:raise ValueError('Context date after dataset cutoff')
        if cutoff in self.cache:return self.cache[cutoff]
        context_id=cutoff.date().isoformat();reference={'context_id':context_id,'as_of':context_id};strict=dict(reference)
        last_month=cutoff.to_period('M')-1
        def put(name,value=np.nan,status='missing',end=pd.NaT,known=pd.NaT,months='',n=0,unit='',note=''):
            age=(cutoff-end).days if pd.notna(end) else None
            available=pd.notna(value) and pd.notna(known) and known<=cutoff
            reference[name]=value;strict[name]=value if available else np.nan
            self.ledger.append(dict(context_id=context_id,feature=name,value_reference=value,
                value_observed_by_cutoff=value if available else np.nan,status=status,reference_end=end,
                known_by=known,age_days=age,input_monthly_ids=months,source_rows=n,unit=unit,note=note,
                availability='observed_by_cutoff' if available else 'unknown_historical_availability' if pd.notna(value) else status))
        for key in SPEC:
            m=self.monthly[key]
            eligible=m[(m.index<=last_month)&(m.reference_end<=cutoff)] if len(m) else m
            names=[(name,'mean') for name,s in MEANS.items() if s==key]+[(name,'level') for name,s in LEVELS.items() if s==key]+[(name,'growth') for name,s in GROWTH.items() if s==key]
            for name,kind in names:
                if not len(eligible):put(name,status='no_prior_observation');continue
                anchor=eligible.index.max();last=eligible.loc[anchor];age=(cutoff-last.reference_end).days
                max_age=200 if key=='gdp' else 120
                if age>max_age:put(name,status='stale_source',end=last.reference_end,known=last.known_by,note=f'max_age_days={max_age}');continue
                periods=pd.period_range(anchor-2,anchor,freq='M') if kind=='mean' else pd.PeriodIndex([anchor-GROWTH_MONTHS.get(name,12),anchor]) if kind=='growth' else pd.PeriodIndex([anchor])
                q=eligible.reindex(periods)
                if q.value.isna().any():put(name,status='missing_required_period',end=last.reference_end,note='|'.join(str(p) for p in periods[q.value.isna()]));continue
                if kind=='growth' and q.value.iloc[0]<=0:put(name,status='invalid_denominator');continue
                value=100*(q.value.iloc[-1]/q.value.iloc[0]-1) if kind=='growth' else q.value.mean()
                put(name,value,'observed_reference',q.reference_end.max(),q.known_by.max(),
                    '|'.join(q.monthly_id),int(q.n.sum()),'percent_change' if kind=='growth' else SPEC[key][-1],
                    'Latest eligible complete reference period; latest-revised history; no imputation')
        put('issue_salience_economy',status='restricted_source',note='MIP total/category and PDF mapping issues; source archive retained')
        reviewed=pd.Timestamp(self.political['reviewed_through'])
        if pd.Timestamp(self.political['coverage_start'])<=cutoff<=reviewed:
            p=state_on(self.political,str(cutoff.date()))
            values={'wh_dem':int(p['wh_party']=='DEM'),'house_dem':int(p['house_party']=='DEM'),'senate_dem':int(p['senate_party']=='DEM')}
            values.update({k:p[k] for k in POLITICAL if k not in values})
            for k,v in values.items():put(k,v,'official_dated_reference',cutoff,cutoff,unit='days' if 'days' in k else 'binary',note='Effective-date control; historical reference, not source publication reconstruction')
        else:
            for k in POLITICAL:put(k,status='outside_political_review',note='No extrapolation beyond official review cutoff')
        # Current year plus four prior calendar years, ending at last closed month.
        months=pd.period_range(f'{cutoff.year-4}-01',last_month,freq='M')
        dq=self.disruption.reindex(months)
        vals=nullable_or(dq.T)
        for source,name in [('health','health_disruption_4y'),('financial','financial_disruption_4y'),('security','security_disruption_4y'),('extraordinary_event_any','extraordinary_event_any_4y')]:
            # A sufficient positive signal can certify OR even when another component is unknown.
            components=['health','financial','security'] if source=='extraordinary_event_any' else [source]
            known_dates=self.disruption_known.reindex(months)[components]
            cert_flags=dq[components].where(known_dates.le(cutoff))
            certified=nullable_or(pd.DataFrame([cert_flags.to_numpy().ravel()])).iloc[0]
            v=vals[source];end=last_month.end_time.normalize();known=cutoff if pd.notna(certified) else pd.NaT
            put(name,v,'observed_reference' if pd.notna(v) else 'incomplete_event_support',end,known,
                unit='binary',note=f'OR; window={months.min()}..{last_month}; prior120m q95 min60; proxy not curated event labels')
        self.cache[cutoff]=(reference,strict)
        return reference,strict
