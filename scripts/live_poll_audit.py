"""Automatic, forecast-pinned coverage audit with independent affiliations intact."""
import json
import pandas as pd
import election_lab as lab

METHOD = ('D/Independent is the forecast side, not a party label. Independent candidates remain IND. '
          'For questions with multiple D/IND candidates, the input is the strongest individual '
          'candidate minus the Republican, never their combined votes. This is a scalar proxy, '
          'not a joint candidate-level win model. Independent winners count on the D/Independent '
          'chamber side by modeling assumption, not a verified caucus commitment. '
          'Reviewed supplements and exact candidate aliases are applied automatically. '
          'Conditional/reduced-ballot versions are kept separately from the preferred ballot. '
          'Partial ballots and inferred date bounds remain explicitly flagged. '
          'All source questions are retained in the audit. Obsolete matchups, incompatible questions, '
          'duplicate sample versions and observations unavailable at the cutoff do not contribute.')


def build_poll_audit(run):
    run=lab.verify_run(run)
    meta=json.loads((run/'run.json').read_text())
    snapshot=lab.dataset_for_run(meta)
    if lab.sha(snapshot/'manifest.json') != meta['dataset_manifest_sha256']:
        raise ValueError('Forecast input manifest changed')
    from compact_data import CompactDataset
    CompactDataset(snapshot)  # Verify each sealed input, including review provenance.
    polls=pd.read_parquet(snapshot/'tables/polls.parquet')
    polls=polls[polls.cycle.eq(2026)&polls.dataset.eq('senate')].copy()
    quality=pd.read_parquet(snapshot/'tables/poll_quality.parquet')
    audit=pd.read_parquet(run/'poll_audit.parquet')
    details=polls.merge(quality[['observation_id','review_reason']],on='observation_id',validate='one_to_one')
    details=details.merge(audit[['observation_id','baseline_status']],on='observation_id',how='left',validate='one_to_one')
    answers=pd.read_parquet(snapshot/'tables/answers.parquet')
    answers=answers[answers.observation_id.isin(details.observation_id)&~answers.exact_duplicate.fillna(False)]
    if 'canonical_candidate_name' in answers:
        answers['candidate_name']=answers.canonical_candidate_name.fillna(answers.candidate_name)
    candidates=answers.groupby('observation_id').apply(
        lambda x:'; '.join(f'{r.candidate_name} ({r.party})' for r in x.itertuples() if r.party in {'DEM','REP','IND'}),include_groups=False)
    details['Candidates']=details.observation_id.map(candidates)
    states=sorted(pd.read_parquet(run/'predictions.parquet').geography.unique())
    summary=[]
    for state in states:
        rows=details[details.geography.eq(state)]; used=rows[rows.baseline_status.eq('eligible')]
        ids=set(used.observation_id)
        independents=answers[answers.observation_id.isin(ids)&answers.party.eq('IND')]
        summary.append({'State':state,'Questions':len(rows),'Eligible':len(used),'Excluded':len(rows)-len(used),
                        'Independent candidates in eligible polls':', '.join(sorted(independents.candidate_name.unique())) or 'None'})
    details['Reason']=details.baseline_status.fillna('not_in_forecast')
    restricted=details.Reason.eq('source_or_matchup_restriction')
    details.loc[restricted,'Reason']=details.loc[restricted,'review_reason']
    reasons=details[~details.baseline_status.eq('eligible')].groupby(['geography','Reason'],dropna=False).size().reset_index(name='Questions').rename(columns={'geography':'State'})
    used=details[details.baseline_status.eq('eligible')]
    banned=['conditional_missing_ballot_contender','alternative_reduced_ballot_same_sample',
            'reviewed_informed_question','reviewed_conditional_question','reviewed_ambiguous_question','unreviewed_or_former_contender']
    checks=[{'Check':'Every source question has a forecast disposition','Passed':bool(details.baseline_status.notna().all())},
            {'Check':'All admitted questions have valid margins and sample sizes','Passed':bool(used.dem_rep_margin.notna().all() and used.sample_size.gt(0).all())},
            {'Check':'No rejected ballot/scenario enters the forecast','Passed':not used.quality_flags.fillna('').str.contains('|'.join(banned),regex=True).any()},
            {'Check':'No admitted fieldwork or known release is after cutoff','Passed':bool((pd.to_datetime(used.poll_end)<=pd.Timestamp(meta['as_of'])).all() and (pd.to_datetime(used.source_available_date)<=pd.Timestamp(meta['as_of'])).all())}]
    if not all(c['Passed'] for c in checks):raise ValueError('All-state poll audit failed: '+str(checks))
    flags=used[['geography','pollster','poll_end','quality_flags']].copy()
    flags=flags[flags.quality_flags.fillna('').str.contains('partial_ballot|publication_date_upper_bound|reviewed_candidate_alias|reviewed_missing_sample_size')]
    receipts_path=snapshot/'review/receipts.json'
    supplements=pd.DataFrame(json.loads(receipts_path.read_text())) if receipts_path.exists() else pd.DataFrame()
    return {'supplements':supplements,'summary':pd.DataFrame(summary),'details':details,'reasons':reasons,'checks':pd.DataFrame(checks),'flags':flags}



def save_poll_audit(run,out):
    from output_publication import markdown_table
    audit=build_poll_audit(run)
    for name,frame in audit.items():frame.to_parquet(out/f'poll_audit_{name}.parquet',index=False)
    (out/'poll_audit.md').write_text('# All-state polling audit\n\n'+METHOD+'\n\n'
        +'Counts are question versions, not independent samples. Recency affects weighting; older eligible polls are retained.\n\n'
        +markdown_table(audit['summary'])+'\n\n## Integrity checks\n\n'+markdown_table(audit['checks'])+'\n\n## Reviewed qualifications\n\n'+markdown_table(audit['flags'])+'\n\n## Exclusion reasons\n\n'+markdown_table(audit['reasons'])
        +'\n\n## Supplemental source receipts\n\n'+markdown_table(audit['supplements'],['state','status','publication_date','source_url'])+'\n\n[Every question, candidate affiliation and reason](poll_audit_details.parquet)\n')
    return audit
