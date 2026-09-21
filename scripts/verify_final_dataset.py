"""Independent verification of the final aligned bundle and its predictor/label boundary."""
import argparse
import json
from pathlib import Path
import numpy as np
import pandas as pd
from alignment_features import sha
from data_utils import LAB


def require(test,message):
    if not test:raise ValueError(message)


def verify_tables(t,as_of,polls_count,outcome_count,answer_count,features):
    as_of=pd.Timestamp(as_of);p=t['polls'];labels=t['labels'];l=t['feature_ledger']
    require(len(p)==polls_count and p.observation_id.is_unique,'Poll count/identity changed')
    require(len(t['answers'])==answer_count,'Answer rows lost')
    require(set(t['answers'].observation_id)<=set(p.observation_id),'Dangling candidate answers')
    require(len(labels)==outcome_count+36 and labels.target_id.is_unique,'Target accounting failed')
    future=labels[labels.cycle.eq(2026)]
    require(len(future)==36 and future[['dem_share','rep_share','dem_rep_margin']].isna().all().all(),'Future target leakage')
    for name in ['poll_inputs_reference','poll_inputs_observed']:
        x=t[name]
        require(len(x)==len(p) and x.observation_id.is_unique and set(x.observation_id)==set(p.observation_id),'Poll feature join expanded/lost rows')
        require(not {'poll_error','reference_margin','dem_share_result','result_margin','diagnostic_eligible','review_status'}&set(x),'Outcome field in predictor view')
        for col in ['dem_share','rep_share','dem_rep_margin','sample_size']:
            a=x.set_index('observation_id')[col].sort_index();b=p.set_index('observation_id')[col].sort_index()
            require(np.allclose(a,b,equal_nan=True),f'Poll {col} changed')
        known=x.prior_presidential_year.notna()
        require((x.loc[known,'prior_presidential_year']<pd.to_datetime(x.loc[known,'context_id']).dt.year).all(),'State prior leaks future election')
    for name in ['contest_inputs_reference','contest_inputs_observed']:
        x=t[name];require(len(x)==len(labels) and x.target_id.is_unique and set(x.target_id)==set(labels.target_id),'Missing unpolled/current target')
        require(not {'dem_share','rep_share','dem_rep_margin','status','diagnostic_eligible','poll_error'}&set(x),'Target label in contest predictors')
    s=t['state_cycle_inputs_reference'];require(not s.duplicated(['cycle','geography']).any(),'Duplicate state-cycle rows')
    require(s.groupby('cycle').geography.nunique().eq(50).all(),'Not all states covered')
    r=t['national_contexts_reference'];o=t['national_contexts_observed']
    require(r.context_id.is_unique and o.context_id.is_unique,'Duplicate national contexts')
    require(set(r.context_id)==set(o.context_id),'Reference/observed context mismatch')
    require(pd.to_datetime(r.context_id).le(as_of).all(),'Future feature context')
    for name,context in [('poll_inputs_reference',r),('poll_inputs_observed',o),
                         ('contest_inputs_reference',r),('contest_inputs_observed',o),('state_cycle_inputs_reference',r)]:
        x=t[name]
        expected=x[['context_id']].merge(context[['context_id',*features]],on='context_id',how='left',validate='many_to_one')
        require(np.allclose(x[features].to_numpy(dtype=float),expected[features].to_numpy(dtype=float),equal_nan=True),f'Incorrect dated feature join: {name}')
        known_prior=x.prior_presidential_year.notna()
        require((x.loc[known_prior,'prior_presidential_year']<pd.to_datetime(x.loc[known_prior,'context_id']).dt.year).all(),'State prior leaks future election')
    expected_dates=pd.to_datetime(p.poll_end.fillna(p.poll_date))
    expected_dates=expected_dates.dt.strftime('%Y-%m-%d').where(expected_dates.le(as_of))
    require(p.context_id.fillna('').tolist()==expected_dates.fillna('').tolist(),'Poll feature cutoff differs from field date')
    require(not l.duplicated(['context_id','feature']).any() and len(l)==len(r)*len(features),'Incomplete feature ledger')
    have=l.value_reference.notna();strict=l.value_observed_by_cutoff.notna()
    cutoff=pd.to_datetime(l.context_id);end=pd.to_datetime(l.reference_end);known=pd.to_datetime(l.known_by)
    require((end[have]<=cutoff[have]).all(),'Future reference period')
    require((known[strict]<=cutoff[strict]).all(),'Value not observed by forecast cutoff')
    require(np.allclose(l.loc[strict,'value_reference'],l.loc[strict,'value_observed_by_cutoff']),'Observed view changed numeric values')
    require(l.loc[l.status.isin(['restricted_source','stale_source','missing_required_period','outside_political_review','no_prior_observation']),'value_reference'].isna().all(),'Missing feature imputed')
    for frame,valuecol in [(r,'value_reference'),(o,'value_observed_by_cutoff')]:
        check=l.pivot(index='context_id',columns='feature',values=valuecol).reindex(frame.context_id)
        require(np.allclose(frame[features].to_numpy(dtype=float),check[features].to_numpy(dtype=float),equal_nan=True),'Feature matrix differs from ledger')
    current=t['contest_inputs_reference'].cycle.eq(2026)
    require(current.sum()==36,'Current contest coverage failed')
    require(len(t['seat_ledger'])==100 and t['seat_ledger'].seat_id.is_unique,'100-seat ledger failed')
    return dict(poll_rows_preserved=len(p),target_rows_preserved=len(labels),answer_rows_preserved=len(t['answers']),
                current_targets_blank=36,all_states_per_cycle=50,national_contexts=len(r),
                no_many_to_many_expansion=True,no_future_reference_values=True,observed_cutoffs_checked=True,
                prior_result_date_check=True,no_imputation=True)


def verify(path,manifest_required=True):
    path=Path(path)
    if manifest_required:
        m=json.loads((path/'manifest.json').read_text())
        for name,info in m['files'].items():require(sha(path/name)==info['sha256'],f'Checksum mismatch: {name}')
    policy=json.loads((path/'policy.json').read_text());prov=json.loads((path/'provenance.json').read_text())
    for p,h in prov['manifests'].items():require(sha((LAB/Path(p))/'manifest.json')==h,'Source manifest changed')
    tables={p.stem:pd.read_parquet(p) for p in (path/'tables').glob('*.parquet')}
    accepted=LAB/Path(prov['accepted_snapshot'])
    original=pd.read_csv(accepted/'tables/observations.csv',low_memory=False)
    outcomes=pd.read_csv(accepted/'tables/outcomes.csv');answers=pd.read_csv(accepted/'tables/answers.csv',low_memory=False)
    features=tables['feature_catalog'].feature.tolist()
    checks=verify_tables(tables,policy['as_of'],len(original),len(outcomes),len(answers),features)
    original_labels=outcomes.rename(columns={'outcome_id':'target_id'}).set_index('target_id')
    actual_labels=tables['labels'].set_index('target_id').loc[original_labels.index]
    for col in ['dem_share','rep_share','dem_rep_margin']:
        require(np.allclose(original_labels[col],actual_labels[col],equal_nan=True),f'Historical label changed: {col}')
    # Independent source equality: no refresh records are silently dropped or normalized again.
    for col in ['observation_id','source','source_poll_id','source_question_id','cycle','geography','poll_date','poll_start','poll_end','election_date','dem_share','rep_share','dem_rep_margin','sample_size']:
        a=original.set_index('observation_id')[col] if col!='observation_id' else original.observation_id
        b=tables['polls'].set_index('observation_id')[col] if col!='observation_id' else tables['polls'].observation_id
        require(a.fillna('').astype(str).tolist()==b.fillna('').astype(str).tolist(),f'Source poll field changed: {col}')
    return checks


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('snapshot',type=Path)
    print(json.dumps(verify(p.parse_args().snapshot),indent=2))
