"""Build the versioned polling + feature dataset without fitting or imputing."""
import argparse
import calendar
from datetime import date,timedelta
import json
from pathlib import Path
import numpy as np
import pandas as pd
from data_utils import LAB,Snapshot,digest
from audit_refresh_2026 import verified
from alignment_features import FeatureStore,sha


def regular_election_day(year):
    first=date(year,11,1)
    monday=first+timedelta(days=(0-first.weekday())%7)
    return monday+timedelta(days=1)


def state_lean_rows(rows,history):
    """Never expose a presidential result before the following calendar year."""
    source=history[['state','prior_presidential_year','prior_state_pres_margin','prior_national_pres_margin','prior_state_lean']].drop_duplicates()
    if source.duplicated(['state','prior_presidential_year']).any():raise ValueError('Conflicting lagged state results')
    result=[]
    for r in rows.itertuples(index=False):
        cutoff=pd.to_datetime(r.context_id) if pd.notna(r.context_id) else pd.NaT
        q=source[(source.state==r.geography)&(source.prior_presidential_year<cutoff.year)] if pd.notna(cutoff) else source.iloc[:0]
        values={k:np.nan for k in ['prior_presidential_year','prior_state_pres_margin','prior_national_pres_margin','prior_state_lean']}
        if len(q):values.update(q.sort_values('prior_presidential_year').iloc[-1].drop('state').to_dict())
        result.append(values)
    return pd.DataFrame(result,index=rows.index)


def build_final(accepted,features,political,as_of,output,run_inputs=None):
    accepted,features,political=map(Path,[accepted,features,political]);as_of=pd.Timestamp(as_of).normalize()
    for p in [accepted,features,political]:verified(p)
    def read(name):return pd.read_csv(accepted/'tables'/f'{name}.csv',low_memory=False)
    observations=read('observations');answers=read('answers');outcomes=read('outcomes')
    quality=read('dispositions');meta=read('metadata');state_history=read('state_features');cal=read('state_calendar')
    current=read('current_contests');seats=read('seat_ledger')
    if observations.observation_id.duplicated().any():raise ValueError('Duplicate poll ID')
    polls=observations.copy()
    polls['alignment_date']=pd.to_datetime(polls.poll_end.fillna(polls.poll_date),errors='raise')
    valid=polls.alignment_date.notna()&polls.alignment_date.le(as_of)
    polls['context_id']=polls.alignment_date.dt.strftime('%Y-%m-%d').where(valid)
    polls['alignment_status']=np.where(polls.alignment_date.isna(),'missing_poll_date',np.where(valid,'dated','after_dataset_cutoff'))
    polls['target_id']=polls.outcome_id
    current_map=current.set_index('state').contest_id.to_dict()
    mask=polls.cycle.eq(2026)
    polls.loc[mask,'target_id']=polls.loc[mask].geography.map(current_map)
    polls.loc[mask&polls.dataset.eq('generic_ballot'),'target_id']='2026-US-house-popular-vote-future'
    # Labels live separately, including explicit missing future labels.
    labels=outcomes.rename(columns={'outcome_id':'target_id'}).copy()
    future=[]
    for c in current.itertuples():
        future.append(dict(target_id=c.contest_id,cycle=2026,geography=c.state,outcome_type='senate_contest_stage',
             stage='general',special=c.special,election_date=c.election_date,status='future_outcome_unavailable',
             diagnostic_eligible=False,dem_share=np.nan,rep_share=np.nan,dem_rep_margin=np.nan))
    future.append(dict(target_id='2026-US-house-popular-vote-future',cycle=2026,geography='US',
         outcome_type='national_house_popular_vote',stage='general',special=False,election_date='2026-11-03',
         status='future_outcome_unavailable',diagnostic_eligible=False,dem_share=np.nan,rep_share=np.nan,dem_rep_margin=np.nan))
    labels=pd.concat([labels,pd.DataFrame(future)],ignore_index=True)
    if labels.target_id.duplicated().any():raise ValueError('Duplicate target')
    if not set(polls.target_id.dropna())<=set(labels.target_id):raise ValueError('Dangling poll target')
    # Match the live forecast horizon for historical contests when their election date is known.
    horizon=max(1,(pd.Timestamp('2026-11-03')-as_of).days)
    dates=observations.dropna(subset=['outcome_id','election_date']).groupby('outcome_id').election_date.agg(lambda s:sorted(set(s)))
    contests=[]
    for r in labels.itertuples():
        election=pd.to_datetime(r.election_date) if pd.notna(r.election_date) else pd.NaT
        basis='outcome_or_current_manifest'
        if pd.isna(election):
            ds=dates.get(r.target_id,[])
            if len(ds)==1:election=pd.Timestamp(ds[0]);basis='linked_poll_election_date'
            elif r.stage in ['gen','general'] and (not bool(r.special) or r.outcome_type=='national_house_popular_vote'):
                election=pd.Timestamp(regular_election_day(r.cycle));basis='regular_federal_calendar'
            else:basis='unknown_or_ambiguous_date'
        if r.cycle==2026:cutoff=as_of
        elif pd.notna(election):cutoff=election-pd.Timedelta(days=horizon)
        else:cutoff=pd.Timestamp(r.cycle,as_of.month,min(as_of.day,calendar.monthrange(r.cycle,as_of.month)[1]))
        contests.append(dict(target_id=r.target_id,cycle=r.cycle,geography=r.geography,outcome_type=r.outcome_type,
            stage=r.stage,special=r.special,election_date=election,context_id=str(cutoff.date()),
            election_date_basis=basis,forecast_days_to_election=(election-cutoff).days if pd.notna(election) else np.nan,
            historical_horizon_comparable=pd.notna(election),is_presidential_cycle=int(r.cycle%4==0),is_midterm_cycle=int(r.cycle%4==2)))
    contests=pd.DataFrame(contests)
    # Preserve all 50 states, including states without a Senate contest in a cycle.
    state_context=cal.rename(columns={'state':'geography'}).copy()
    state_context['context_id']=[str((as_of if y==2026 else pd.Timestamp(regular_election_day(y))-pd.Timedelta(days=horizon)).date()) for y in state_context.cycle]
    all_dates=sorted(set(polls.context_id.dropna())|set(contests.context_id)|set(state_context.context_id))
    store=FeatureStore(features,json.loads((political/'config.json').read_text()),as_of)
    contexts=[];observed=[]
    for i,cutoff in enumerate(all_dates):
        a,z=store.at(cutoff);contexts.append(a);observed.append(z)
        if (i+1)%500==0:print(f'Aligned {i+1}/{len(all_dates)} dated contexts',flush=True)
    reference=pd.DataFrame(contexts);strict=pd.DataFrame(observed)
    ledger=pd.DataFrame(store.ledger)
    for table in [polls,contests,state_context]:
        lean=state_lean_rows(table,state_history)
        for name in lean:table[name]=lean[name]
    # Exact source predictor allowlist: no outcomes/errors/eligibility conclusions become features.
    from build_accepted_data import PREDICTORS
    predictor_fields=[k for k in PREDICTORS if k in polls]+['context_id','target_id','alignment_status',
        'prior_presidential_year','prior_state_pres_margin','prior_national_pres_margin','prior_state_lean']
    inputs=polls[predictor_fields].copy()
    inputs['is_presidential_cycle']=inputs.cycle.mod(4).eq(0).astype(int)
    inputs['is_midterm_cycle']=inputs.cycle.mod(4).eq(2).astype(int)
    poll_reference=inputs.merge(reference,on='context_id',how='left',validate='many_to_one')
    poll_observed=inputs.merge(strict,on='context_id',how='left',validate='many_to_one')
    contest_reference=contests.merge(reference,on='context_id',how='left',validate='many_to_one')
    contest_observed=contests.merge(strict,on='context_id',how='left',validate='many_to_one')
    state_reference=state_context.merge(reference,on='context_id',how='left',validate='many_to_one')
    # Poll availability and contest coverage are metadata, not imputation or sample selection.
    quality=quality.rename(columns={'status':'review_status','reason':'review_reason'})
    quality=quality.merge(polls[['observation_id','context_id','target_id','alignment_status']],on='observation_id',validate='one_to_one')
    availability=meta[['observation_id','documented_release_date','availability_status','archive_created_date']].copy()
    # Rebuilding labels does not make unchanged polls newly observed. Use each
    # observation's original reviewed/refresh source receipt, not this build date.
    accepted_config=json.loads((accepted/'config.json').read_text())
    source_dates={name:pd.Timestamp(json.loads((LAB/accepted_config['snapshots'][name]['path']/'manifest.json').read_text())['retrieved_at']).tz_localize(None).normalize()
                  for name in ['reviewed','refresh']}
    availability['snapshot_observed_date']=availability.observation_id.map(polls.set_index('observation_id').origin_bundle).map(source_dates)
    if availability.snapshot_observed_date.isna().any():raise ValueError('Missing poll source receipt')
    availability=availability.merge(polls[['observation_id','context_id']],on='observation_id',validate='one_to_one')
    cutoffs=pd.to_datetime(availability.context_id);release=pd.to_datetime(availability.documented_release_date,errors='coerce')
    availability['poll_known_by_context_date']=pd.Series(pd.NA,index=availability.index,dtype='boolean')
    availability.loc[release.gt(cutoffs),'poll_known_by_context_date']=False
    availability.loc[release.le(cutoffs)|cutoffs.ge(availability.snapshot_observed_date),'poll_known_by_context_date']=True
    polls_by_target={k:g for k,g in polls.groupby('target_id')};q_by_id=quality.set_index('observation_id')
    coverage=[]
    for r in contests.itertuples():
        pool=polls_by_target.get(r.target_id,polls.iloc[:0]);eligible=pool[pool.alignment_date.le(pd.Timestamp(r.context_id))]
        cutoff=pd.Timestamp(r.context_id)
        statuses=q_by_id.reindex(eligible.observation_id).review_status
        usable=eligible.loc[statuses.isin(['usable_retrospective','provisional','current_screened']).to_numpy()]
        # Publication evidence is stricter than field dates; snapshot retrieval proves only current availability.
        m=availability.set_index('observation_id').reindex(usable.observation_id)
        documented=pd.to_datetime(m.documented_release_date,errors='coerce').le(cutoff)
        retrieved=m.snapshot_observed_date.le(cutoff)
        known=(documented|retrieved).to_numpy()
        coverage.append(dict(target_id=r.target_id,context_id=r.context_id,stored_versions=len(pool),
              versions_by_field_date=len(eligible),screened_versions_by_field_date=len(usable),
              publication_confirmed_screened_versions=int(known.sum()),
              screened_versions_last_14_days=int(usable.alignment_date.ge(cutoff-pd.Timedelta(days=14)).sum()),
              status='no_source_poll' if not len(pool) else 'no_screened_poll_by_cutoff' if not len(usable) else 'polls_available_with_review_flags'))
    feature_catalog=[]
    for k in store.columns:
        units=ledger.loc[ledger.feature.eq(k)&ledger.unit.ne(''),'unit'].dropna().unique()
        if len(units)>1:raise ValueError(f'Conflicting feature units: {k}')
        feature_catalog.append(dict(feature=k,unit=units[0] if len(units) else 'not_admitted',
             representation='reference / observed_by_cutoff',missing_preserved=True,
             role='candidate_mean_scale_tail_or_skew_input' if 'disruption' in k or k=='extraordinary_event_any_4y' else 'candidate_predictor'))
    policy=dict(version='final-alignment-v1',as_of=str(as_of.date()),historical_horizon_days=horizon,
       history='1976 onward; all accepted versions/outcomes retained; 2016+ priority is not a cutoff',
       reference_view='Latest-revised source observations whose full reference periods end by the row cutoff; no publication guarantee',
       observed_view='Feature values masked unless observation by cutoff is supported; this does not certify poll availability (see poll_availability). Retrieval proves only availability on retrieval day or later',
       feature_window='Latest eligible closed month (or quarter); 3 consecutive months for means; exact 12-month endpoints for growth, 24 months for cpi_24m_pct',
       staleness_days={'monthly_or_daily_aggregates':120,'GDP':200},missing='NaN; no imputation',
       political='Official effective-date reference within reviewed range; outside range missing',
       state_prior='Latest retained presidential result with result year strictly before context year',
       disruption='OR of health/VIX/GPR high-stress proxies; Jan(cutoff_year-4)..last closed month; original source/threshold limitations retained',
       polls='All versions preserved; screened counts are not independent samples. Quality/source restrictions remain separate.',
       selected_national_features=len(store.columns),restricted_feature='MIP/PDF mapping not admitted; all prepared source tables retained via pinned source catalog',
       not_forecast_ready_reasons=['complete_ballot_and_seat_mapping_restrictions','historical_publication_and_vintage_gaps','sample_version_and_model_likelihood_policy_pending'])
    frames={'polls':polls,'answers':answers,'labels':labels,'poll_quality':quality,'poll_availability':availability,
       'poll_inputs_reference':poll_reference,'poll_inputs_observed':poll_observed,
       'contest_inputs_reference':contest_reference,'contest_inputs_observed':contest_observed,
       'state_cycle_inputs_reference':state_reference,'national_contexts_reference':reference,'national_contexts_observed':strict,
       'feature_ledger':ledger,'contest_coverage':pd.DataFrame(coverage),'feature_catalog':pd.DataFrame(feature_catalog),
       'feature_source_selection':pd.DataFrame(store.selection),'feature_monthly_inputs':pd.DataFrame(store.monthly_rows),
       'disruption_monthly':store.disruption.reset_index(),'disruption_thresholds':store.disruption_ledger,
       'seat_ledger':seats,'current_contests':current,'poll_identity':read('identity'),
       'poll_metadata':meta,'historical_poll_errors':read('errors'),'result_restrictions':read('result_restrictions')}
    if (accepted/'tables/official_result_review_audit.csv').exists():
        frames['official_result_review_audit']=read('official_result_review_audit')
    from verify_final_dataset import verify_tables
    checks=verify_tables(frames,as_of,len(observations),len(outcomes),len(answers),store.columns)
    summary=dict(as_of=str(as_of.date()),status='aligned_for_analysis_with_explicit_restrictions',seat_forecast_ready=False,
       counts={k:len(v) for k,v in frames.items()},checks=checks,national_feature_count=len(store.columns),
       historical_poll_rows=int(polls.cycle.lt(2026).sum()),current_poll_rows=int(polls.cycle.eq(2026).sum()),
       future_labels_blank=True,imputed_values=0,unverified_feature_values=int((ledger.value_reference.notna()&ledger.value_observed_by_cutoff.isna()).sum()),
       current_political_review_through=store.political['reviewed_through'],source_catalog_tables=len(store.catalog))
    provenance=dict(accepted_snapshot=str(accepted.resolve()),prepared_feature_snapshot=str(features.resolve()),political_snapshot=str(political.resolve()),
       manifests={str(p.resolve()):sha(p/'manifest.json') for p in [accepted,features,political]},run=run_inputs or {},
       feature_source_catalog=store.catalog,all_prepared_sources_retained=True)
    with Snapshot(output,'final_aligned_election_dataset') as snap:
        for name,d in frames.items():
            d=d.copy()
            for col in d:
                if isinstance(d[col].dtype,pd.PeriodDtype):d[col]=d[col].astype(str)
            dest=snap.stage/'tables'/f'{name}.parquet';dest.parent.mkdir(exist_ok=True)
            d.to_parquet(dest,index=False)
        for name in ['contest_coverage','feature_catalog','feature_source_selection']:
            frames[name].to_csv(snap.stage/f'{name}.csv',index=False)
        snap.write_json('policy.json',policy);snap.write_json('summary.json',summary);snap.write_json('provenance.json',provenance)
        for name in ['build_final_dataset.py','alignment_features.py','verify_final_dataset.py','disruption_features.py','final_pipeline.py']:
            snap.add('recipe/'+name,(LAB/'scripts'/name).read_bytes())
        for p in snap.stage.rglob('*'):
            if p.is_file():snap.files[str(p.relative_to(snap.stage))]=dict(bytes=p.stat().st_size,sha256=sha(p))
        # Reload serialized tables before publishing the dataset pointer.
        from verify_final_dataset import verify
        verify(snap.stage,manifest_required=False)
        return snap.finish(summary)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--accepted',type=Path,required=True);p.add_argument('--features',type=Path,required=True)
    p.add_argument('--political',type=Path,required=True);p.add_argument('--as-of',type=date.fromisoformat,default=date.today())
    p.add_argument('--output',type=Path,default=LAB/'data/final');a=p.parse_args()
    build_final(a.accepted,a.features,a.political,a.as_of,a.output)
