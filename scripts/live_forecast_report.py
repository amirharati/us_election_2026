"""Portable HTML reports and cached, fixed-model 2026 cutoff replays.

Replay is retrospective: the current roster, source screening, data revisions
and trained checkpoint are held fixed. It is not a record of issued forecasts.
"""
import base64
import hashlib
import html
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import election_lab as lab


def cutoff_schedule(start, end, every_days=30, last_days=3):
    """Include start/end and the last N calendar days, with no duplicate dates."""
    start, end = pd.Timestamp(start).normalize(), pd.Timestamp(end).normalize()
    if start > end or start.year != 2026 or end.year != 2026:
        raise ValueError('Use an ordered date range inside2026')
    if every_days < 1 or last_days < 1:
        raise ValueError('Step and recent-day count must be positive integers')
    if int(every_days) != every_days or int(last_days) != last_days:
        raise ValueError('Step and recent-day count must be integers')
    regular = pd.date_range(start, end, freq=f'{int(every_days)}D')
    daily = pd.date_range(max(start, end-pd.Timedelta(days=int(last_days)-1)), end)
    return sorted(set(regular) | set(daily) | {end})


def _model_hash():
    files = [lab.ROOT/'election_lab.py', *sorted((lab.ROOT/'scripts').glob('*.py')),
             *sorted(p for p in (lab.ROOT/'config').glob('*') if p.is_file()),
             *sorted(p for p in lab.ASSETS.rglob('*') if p.is_file())]
    return hashlib.sha256(json.dumps({str(p.relative_to(lab.ROOT)):lab.sha(p)
                                     for p in files}, sort_keys=True).encode()).hexdigest()


def _evidence_hash(evidence, model_hash, include_student, weights):
    """Reuse a cutoff after refresh when its actual model inputs are unchanged.

    New source row IDs alone do not invalidate inference. Date, values, sample
    multiplicity, firm identity, missingness and trained code/assets all matter.
    """
    h = hashlib.sha256(json.dumps(dict(model_hash=model_hash,
        include_student=include_student, weights=weights,
        feature_mode=evidence['feature_mode']), sort_keys=True).encode())
    frames = [evidence['q'], evidence['targets'], evidence['cal']]
    waves = evidence['waves']
    frames.append(waves[[c for c in ['target_id','margin','field_end','cutoff','firm',
                                     'reported_n','publication_unknown','age_days'] if c in waves]])
    for frame in frames:
        # Preserve row multiplicity but ignore arbitrary source/export ordering.
        values = pd.util.hash_pandas_object(frame, index=False).to_numpy()
        h.update('|'.join(frame.columns).encode())
        h.update(np.sort(values).tobytes())
    return h.hexdigest()


def _seat_history_row(run):
    seats = pd.read_parquet(run/'seats.parquet').copy()
    # The retained convention counts caucusing independents with Democrats;
    # Republicans control a50/50 Senate under the assumed GOP VP tie-break.
    seats['p_R_control'] = 1-seats.p_D_control
    seats['D_control_pct'] = 100*seats.p_D_control
    seats['R_control_pct'] = 100*seats.p_R_control
    return seats


def run_history(live_run, start='2026-01-01', every_days=30, last_days=3,
                feature_mode='dated', force=False):
    """Replay all models present in live_run, caching complete inference per cutoff.

    No download or fitting occurs here. Student models use their actual sampler
    and convergence checks, never substitute Gaussian tails to speed the replay.
    """
    live_run = lab.verify_run(live_run)
    meta = json.loads((live_run/'run.json').read_text())
    snapshot = lab.dataset_for_run(meta)
    if lab.sha(snapshot/'manifest.json') != meta['dataset_manifest_sha256']:
        raise ValueError('Live dataset manifest changed')
    models = pd.read_parquet(live_run/'seats.parquet').model.tolist()
    include_student = 'Matched Student-t (df5)' in models
    weights = meta['weights']
    dates = cutoff_schedule(start, meta['as_of'], every_days, last_days)
    model_hash = _model_hash()
    records, evidence_rows, sources, diagnostics = [], [], [], []
    for i, cutoff in enumerate(dates, 1):
        date = str(cutoff.date())
        if date == meta['as_of']:
            # Exact endpoint equality to the notebook's current forecast.
            run, status = live_run, 'current_live_run'
            fingerprint = None
        else:
            e = lab.prepare_live_evidence(snapshot, date, feature_mode)
            fingerprint = _evidence_hash(e, model_hash, include_student, weights)
            cache = lab.ROOT/'cache/cutoff_history'/f'{fingerprint}.json'
            if cache.exists() and not force:
                cached = json.loads(cache.read_text())
                run = lab.ROOT/cached['run']
                if lab.sha(run/'manifest.json') != cached['manifest_sha256']:
                    raise ValueError('Changed cached cutoff manifest')
                lab.verify_run(run)
                status = 'verified_cache'
            else:
                run = lab.live_forecast(snapshot, include_student=include_student,
                    weights=weights, as_of=date, feature_mode=feature_mode,
                    output_kind='cutoff_forecasts', prepared=e)
                lab.write_json(cache, dict(run=str(run.relative_to(lab.ROOT)),
                    manifest_sha256=lab.sha(run/'manifest.json'), input_fingerprint=fingerprint))
                status = 'computed'
        print(f'Cutoff {i}/{len(dates)}: {date} — {status}', flush=True)
        seats = _seat_history_row(run)
        if set(seats.model) != set(models):
            raise ValueError('Cutoff model roster differs from current forecast')
        seats['cutoff'] = cutoff
        records.append(seats)
        audit = pd.read_parquet(run/'poll_audit.parquet')
        admitted = audit[audit.baseline_status.eq('eligible')]
        if (pd.to_datetime(admitted.field_end) > cutoff).any():
            raise ValueError('Future poll entered a cutoff')
        if (pd.to_datetime(admitted.release).dropna() > cutoff).any():
            raise ValueError('Known future release entered a cutoff')
        pred = pd.read_parquet(run/'predictions.parquet')
        main = pred[pred.model.eq('Bayesian')]
        evidence_rows.append(dict(cutoff=cutoff, polled_contests=int(main.sample_count.gt(0).sum()),
            admitted_samples=int(main.sample_count.sum()),
            latest_poll_end=admitted.field_end.max(),
            eligible_question_versions=len(admitted),
            unknown_release_versions=int(admitted.release.isna().sum())))
        sources.append(dict(cutoff=date, run=str(run.relative_to(lab.ROOT)),
            manifest_sha256=lab.sha(run/'manifest.json'), status=status,
            input_fingerprint=fingerprint))
        if (run/'all_model_diagnostics.parquet').exists():
            diagnostics.append(pd.read_parquet(run/'all_model_diagnostics.parquet').assign(cutoff=cutoff))
    table = pd.concat(records, ignore_index=True).sort_values(['model','cutoff'])
    table['delta_D_pp'] = table.groupby('model').D_control_pct.diff()
    table['delta_R_pp'] = table.groupby('model').R_control_pct.diff()
    table['days_since_previous'] = table.groupby('model').cutoff.diff().dt.days
    np.testing.assert_allclose(table.D_control_pct+table.R_control_pct, 100.)
    if table.duplicated(['model','cutoff']).any():raise ValueError('Duplicate timeline point')
    out = lab.new_run('control_history')
    table.to_parquet(out/'control_history.parquet', index=False)
    pd.DataFrame(evidence_rows).to_parquet(out/'evidence.parquet', index=False)
    if diagnostics:pd.concat(diagnostics, ignore_index=True).to_parquet(out/'diagnostics.parquet', index=False)
    return lab.finish(out, dict(kind='control_history', as_of=meta['as_of'],
        live_run=str(live_run.relative_to(lab.ROOT)), start=start, every_days=every_days,
        last_days=last_days, feature_mode=feature_mode, models=models,
        source_manifest_sha256=lab.sha(live_run/'manifest.json'), model_hash=model_hash,
        cutoff_sources=sources, trained_through=2024,
        interpretation='Retrospective fixed-model, current-roster replay; not archived issued forecasts.',
        availability='Poll field-end and known release cutoffs; unknown releases use field end. Dated features use latest-revised reference periods, not publication vintages.',
        horizon='September-calibrated checkpoints reused from January onward; early-year probabilities are exploratory.',
        control_rule='D>=51; R<=50 D seats, including GOP VP tie-break; caucusing independents grouped with their bloc.'))


def history_figure(table):
    """Show both blocs and every retained model without sixteen lines per panel."""
    groups = [
        ('Core models', [m for m in table.model.unique() if m in
         ['Bayesian','Matched Student-t (df5)','Older Gaussian','Student-t research helper','Non-Bayesian corrected']]),
        ('Gaussian + corrected-polling mean', [m for m in table.model.unique() if m.startswith('Corrected ')]),
        ('Four-model mixture and mean shifts', [m for m in table.model.unique() if m.startswith('Mixture +') or m=='Four-model mixture']),
    ]
    groups = [(title, names) for title,names in groups if names]
    fig, axes = plt.subplots(len(groups), 2, figsize=(15, 4*len(groups)), squeeze=False, sharex=True, sharey=True)
    for row,(title,names) in enumerate(groups):
        for col,(party,field) in enumerate([('Democratic','D_control_pct'),('Republican','R_control_pct')]):
            ax = axes[row,col]
            for name in names:
                part = table[table.model.eq(name)].sort_values('cutoff')
                ax.plot(part.cutoff,part[field],label=name,marker='.',linewidth=1.4)
            ax.axhline(50,color='gray',linestyle='--',linewidth=.7)
            ax.set(title=f'{title}\n{party} control',ylim=(0,100),ylabel='Probability (%)')
            ax.grid(alpha=.2);ax.legend(fontsize=7,loc='best');ax.tick_params(axis='x',rotation=30)
    fig.suptitle('2026 cutoff replay — fixed trained models, dated evidence\nLines connect evaluated cutoffs; early-year forecasts use September calibration.',fontsize=12)
    fig.tight_layout(rect=(0,0,1,.95))
    return fig


def recent_table(table, last_days=3):
    end = table.cutoff.max()
    recent = table[table.cutoff.ge(end-pd.Timedelta(days=last_days-1))].copy()
    recent['date'] = recent.cutoff.dt.strftime('%Y-%m-%d')
    return recent.pivot(index='model',columns='date',values=['D_control_pct','R_control_pct']).round(2)


def save_report(live_run, watchlist, history_run=None):
    """Save a self-contained HTML report, plus machine-readable result tables."""
    live_run = lab.verify_run(live_run)
    meta = json.loads((live_run/'run.json').read_text())
    out = lab.new_run('live_reports')
    seats = _seat_history_row(live_run)
    pred = pd.read_parquet(live_run/'predictions.parquet')
    seats.to_parquet(out/'seats.parquet',index=False)
    pred.to_parquet(out/'predictions.parquet',index=False)
    for name in ['recent','broad','summary']:
        watchlist[name].to_parquet(out/f'watchlist_{name}.parquet',index=False)
    def table(frame):return frame.to_html(index=False,float_format=lambda x:f'{x:.2f}',na_rep='—',escape=True)
    parts = [f'<h1>2026 Senate forecast — {html.escape(meta["as_of"])}</h1>',
        '<p>Positive margins favor Democrats. Probabilities are model estimates, not certified outcomes. '
        'Democratic control requires51 seats; Republican control includes a50–50 Senate with the assumed GOP vice-presidential tie-break.</p>',
        '<h2>Current chamber forecast — all models</h2>',
        table(seats[['model','point_D','point_R','expected_D','expected_R','D_control_pct','R_control_pct','D_lo70','D_hi70']]),
        '<h2>Recently polled states with broad uncertainty</h2>',
        '<p>Wide intervals are not themselves evidence of fat tails. The stronger-coverage flag distinguishes multiple recent samples/firms from a single recent poll.</p>',
        '<p>Watchlist settings: '+html.escape(json.dumps(watchlist.get('parameters',{})))+'</p>',
        table(watchlist['summary']),table(watchlist['broad'].query("model == 'Bayesian'")),
        '<h2>State margins, probabilities and95% ranges — all models</h2>']
    state = pred[['model','geography','special','margin_pp','p_dem','lo95_pp','hi95_pp']].copy()
    state['D_win_pct'] = 100*state.pop('p_dem')
    for model,frame in state.groupby('model',sort=False):
        parts.extend([f'<details><summary>{html.escape(model)}</summary>',table(frame.drop(columns='model')),'</details>'])
    if history_run is not None:
        history_run = lab.verify_run(history_run)
        hmeta = json.loads((history_run/'run.json').read_text())
        if hmeta['source_manifest_sha256'] != lab.sha(live_run/'manifest.json'):
            raise ValueError('Report and history use different current forecasts')
        history = pd.read_parquet(history_run/'control_history.parquet')
        history.to_parquet(out/'control_history.parquet',index=False)
        evidence = pd.read_parquet(history_run/'evidence.parquet')
        evidence.to_parquet(out/'history_evidence.parquet',index=False)
        figure = history_figure(history);figure.savefig(out/'control_history.png',dpi=140,bbox_inches='tight');plt.close(figure)
        encoded = base64.b64encode((out/'control_history.png').read_bytes()).decode()
        parts.extend(['<h2>Senate-control probabilities over cutoff dates</h2>',
            '<p>'+html.escape(hmeta['interpretation']+' '+hmeta['availability']+' '+hmeta['horizon'])+'</p>',
            f'<p>Feature mode: {html.escape(hmeta["feature_mode"])}. Scheduled spacing: {hmeta["every_days"]} days; '
            f'last {hmeta["last_days"]} days evaluated daily. Small changes may include Monte Carlo noise.</p>',
            f'<img alt="Senate-control history by model and party" src="data:image/png;base64,{encoded}">',
            '<h3>Recent daily probabilities (%)</h3>',recent_table(history,hmeta['last_days']).to_html(),
            '<details><summary>All cutoff results and changes</summary>',table(history),'</details>',
            '<details><summary>Polling evidence by cutoff</summary>',table(evidence),'</details>'])
    parts.extend(['<h2>Freshness and provenance</h2>',
        '<pre>'+html.escape(json.dumps(meta,indent=2))+'</pre>'])
    page='<!doctype html><html><head><meta charset="utf-8"><title>2026 Senate forecast report</title><style>body{font-family:system-ui,sans-serif;margin:32px;line-height:1.45}table{border-collapse:collapse;font-size:13px;margin:16px 0}th,td{padding:6px 10px;border:1px solid #ddd;text-align:right}th{background:#eef2f6}details{margin:16px 0}pre{white-space:pre-wrap;overflow-wrap:anywhere}img{max-width:100%}</style></head><body>'+''.join(parts)+'</body></html>'
    (out/'report.html').write_text(page)
    return lab.finish(out,dict(kind='live_report',as_of=meta['as_of'],
        live_run=str(live_run.relative_to(lab.ROOT)),live_manifest_sha256=lab.sha(live_run/'manifest.json'),
        watchlist_parameters=watchlist.get('parameters',{}),
        history_run=str(history_run.relative_to(lab.ROOT)) if history_run else None,
        history_manifest_sha256=lab.sha(history_run/'manifest.json') if history_run else None))
