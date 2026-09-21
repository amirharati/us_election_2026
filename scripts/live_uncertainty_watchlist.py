"""Describe wide margin intervals with recent, admitted polling evidence.

This is a reporting filter, not a model selection or fat-tail diagnostic.
Read the forecast's own snapshot and cutoff, never a newer dataset pointer.
"""
import json
from pathlib import Path

import pandas as pd

import election_lab as lab


def build_watchlist(run, models, recent_days=30, min_width_pp=25.,
                    min_samples=3, min_firms=2):
    """Return recent-state detail, broad-state detail and per-model summaries.

    Recency uses field-end age in [0, recent_days], inclusive. Poll screening
    comes from the saved audit. Tied questions from one sample count once;
    unknown firm identities do not count toward the distinct-firm threshold.
    """
    if recent_days < 0 or min_width_pp <= 0 or min_samples < 1 or min_firms < 1:
        raise ValueError('Use nonnegative recency, positive width and counts >= 1')
    run = lab.verify_run(Path(run))
    meta = json.loads((run/'run.json').read_text())
    cutoff = pd.Timestamp(meta['as_of']).normalize()
    snapshot = lab.dataset_for_run(meta)
    if not snapshot.is_relative_to(lab.ROOT):
        raise ValueError('Dataset must be inside the standalone package')
    if lab.sha(snapshot/'manifest.json') != meta['dataset_manifest_sha256']:
        raise ValueError('Forecast dataset manifest has changed')
    manifest = json.loads((snapshot/'manifest.json').read_text())['files']

    def read_table(name):
        rel = f'tables/{name}.parquet'
        if lab.sha(snapshot/rel) != manifest[rel]['sha256']:
            raise ValueError('Changed dataset table: '+name)
        return pd.read_parquet(snapshot/rel)

    polls = read_table('polls')
    identity = read_table('poll_identity')[['observation_id', 'canonical_firm']]
    polls = polls.merge(identity, on='observation_id', validate='one_to_one')
    polls['sample_key'] = (polls.canonical_sample_group_id
                           .fillna(polls.sample_group_id).fillna(polls.observation_id))
    polls['firm'] = polls.canonical_firm.fillna(polls.pollster)
    polls['firm'] = polls.firm.replace({'unknown': None, '': None})
    pred = pd.read_parquet(run/'predictions.parquet')
    pred = pred[pred.model.isin(models)].copy()
    audit = pd.read_parquet(run/'poll_audit.parquet')
    eligible = audit[audit.baseline_status.eq('eligible') &
                     audit.target_id.isin(pred.target_id)].merge(
        polls[['observation_id', 'sample_key', 'firm']],
        on='observation_id', validate='one_to_one')
    # Mirrors the model's one-contribution-per-target/sample grouping.
    samples = eligible.groupby(['target_id', 'sample_key']).agg(
        field_end=('field_end', 'max'), firm=('firm', 'first')).reset_index()
    samples['age_days'] = (cutoff-pd.to_datetime(samples.field_end)).dt.days
    recent = samples[samples.age_days.between(0, recent_days)]
    coverage = recent.groupby('target_id').agg(
        latest_poll=('field_end', 'max'), recent_samples=('sample_key', 'size'),
        recent_firms=('firm', 'nunique')).reset_index()
    detail = pred.merge(coverage, on='target_id', how='left', validate='many_to_one')
    detail[['recent_samples','recent_firms']] = detail[['recent_samples','recent_firms']].fillna(0).astype(int)
    detail['contest'] = detail.geography + detail.special.fillna(False).map(
        {True: ' special', False: ''})
    detail['width95_pp'] = detail.hi95_pp-detail.lo95_pp
    detail['broad'] = detail.width95_pp.ge(min_width_pp)
    detail['stronger_coverage'] = (detail.recent_samples.ge(min_samples) &
                                 detail.recent_firms.ge(min_firms))
    detail['latest_poll'] = pd.to_datetime(detail.latest_poll).dt.strftime('%Y-%m-%d')
    columns = ['model', 'target_id', 'contest', 'latest_poll', 'recent_samples',
               'recent_firms', 'stronger_coverage', 'prediction_pp', 'lo95_pp',
               'hi95_pp', 'width95_pp', 'p_dem', 'broad']
    detail = detail[columns].sort_values(['model', 'width95_pp'], ascending=[True, False])
    all_contests = detail.copy()
    detail = detail[detail.recent_samples.gt(0)].copy()
    broad = detail[detail.broad].copy()
    summaries = []
    for model in models:
        if model not in pred.model.values:
            continue  # The live notebook can run without Student inference.
        rows = broad[broad.model.eq(model)]
        summaries.append(dict(
            model=model, recent_contests=int(detail.model.eq(model).sum()),
            broad_contests=len(rows), states=', '.join(rows.contest) or 'None',
            stronger_coverage_states=', '.join(rows.loc[rows.stronger_coverage, 'contest']) or 'None'))
    return dict(as_of=str(cutoff.date()), recent=detail, broad=broad, all_contests=all_contests,
                parameters=dict(recent_days=recent_days,min_width_pp=min_width_pp,
                                min_samples=min_samples,min_firms=min_firms),
                summary=pd.DataFrame(summaries))
