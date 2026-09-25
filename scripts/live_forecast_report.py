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
from model_labels import model_label, label_frame, MODEL_GUIDE

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
        ('Gaussian: shifts toward empirical baseline', [m for m in table.model.unique() if m.startswith('Corrected ')]),
        ('Four-model mixture and mean shifts', [m for m in table.model.unique() if m.startswith('Mixture +') or m=='Four-model mixture']),
    ]
    groups = [(title, names) for title,names in groups if names]
    fig, axes = plt.subplots(len(groups), 2, figsize=(15, 4*len(groups)), squeeze=False, sharex=True, sharey=True)
    for row,(title,names) in enumerate(groups):
        for col,(party,field) in enumerate([('Democratic','D_control_pct'),('Republican','R_control_pct')]):
            ax = axes[row,col]
            for name in names:
                part = table[table.model.eq(name)].sort_values('cutoff')
                ax.plot(part.cutoff,part[field],label=model_label(name),marker='.',linewidth=1.4)
            ax.axhline(50,color='gray',linestyle='--',linewidth=.7)
            ax.set(title=f'{title}\n{party} control',ylim=(0,100),ylabel='Probability (%)')
            ax.grid(alpha=.2);ax.legend(fontsize=7,loc='best');ax.tick_params(axis='x',rotation=30)
    fig.suptitle(f'2026 cutoff replay through {pd.Timestamp(table.cutoff.max()).date()} — fixed trained models, dated evidence\nLines connect evaluated cutoffs; early-year forecasts use September calibration.',fontsize=12)
    fig.tight_layout(rect=(0,0,1,.95))
    return fig


def recent_table(table, last_days=3):
    end = table.cutoff.max()
    recent = table[table.cutoff.ge(end-pd.Timedelta(days=last_days-1))].copy()
    recent['date'] = recent.cutoff.dt.strftime('%Y-%m-%d')
    return recent.pivot(index='model',columns='date',values=['D_control_pct','R_control_pct']).round(2)


def markdown_report(out, meta, seats, predictions, watchlist, history_run=None, surprise=None, published=None):
    """Readable GitHub report, with full numerical bundles linked separately."""
    from output_publication import markdown_table
    main=seats[seats.model.eq('Bayesian')].iloc[0]
    lines=[f'# 2026 Senate forecast — {meta["as_of"]}', '',
        '[All outputs](../../README.md) · [HTML report](report.html) · [Supporting tables](../../results/forecast/live_reports/)', '',
        '## At a glance', '',
        f'- **D/Independent control: {main.D_control_pct:.1f}%** under the reference Gaussian model.',
        f'- **Expected D/Independent seats: {main.expected_D:.1f}**; central 70% range: **{int(main.D_lo70)}–{int(main.D_hi70)}**.',
        f'- Predicted winners by mean margin: **{int(main.point_D)} D/IND / {int(main.point_R)} R**.',
        f'- Trained through **{meta["trained_through"]}**. Live evidence updates predictions; trained parameters are fixed.', '',
        'Margins are D/Independent minus Republican percentage points. Positive margins favor the D/Independent side. D control requires 51 seats; R control includes a 50–50 chamber under the retained vice-presidential tie-break assumption.', '',
        '## Poll coverage and candidate affiliations', '',
        '[All-state polling audit](poll_audit.md). Independents retain their IND affiliation. For multiple D/IND candidates, the strongest individual candidate is used, never their summed votes. Independent chamber alignment is an explicit modeling assumption.', '',
        '## Data freshness', '']
    sources=meta.get('freshness',{}).get('sources',[])
    statuses={'fresh_check_cache':'Recent successful check reused','checked_online':'Checked online this run',
              'offline_cache':'Offline: saved evidence','stale_cache_after_failure':'STALE: source check failed; saved evidence used'}
    if sources:
        frame=pd.DataFrame([{'Source':r['source'],'Status':statuses.get(r.get('acquisition_status'),r.get('acquisition_status','Unknown')),
                             'Last successful check':r.get('checked_at') or 'Not recorded'} for r in sources])
        lines += [markdown_table(frame),'']
    lines += [f'Political context is reviewed through **{meta["political_reference_reviewed_through"]}**. '+
              ('It is carried forward as an explicit assumption.' if meta['political_context_carried_forward'] else 'No carry-forward is needed.'), '',
              'The forecast cutoff does not mean every source has observations through that date. Missing evidence is not replaced with a zero.', '',
              '## Chamber forecast across models', '']
    chamber=seats[['model','expected_D','D_control_pct','R_control_pct','D_lo70','D_hi70']].rename(columns={
        'model':'Model','expected_D':'Expected D seats','D_control_pct':'D control %','R_control_pct':'R control %',
        'D_lo70':'D seats: 70% low','D_hi70':'D seats: 70% high'})
    lines += [markdown_table(chamber),'', MODEL_GUIDE+' Mixtures and mean shifts are comparisons, not automatically selected replacements for the reference model.', '',
              '## State forecasts — reference model','']
    state=predictions[predictions.model.eq('Bayesian')][['geography','special','margin_pp','p_dem','lo95_pp','hi95_pp']].copy()
    state['Contest']=state.geography+state.special.map(lambda x:' (special)' if x else '')
    state['D/IND win %']=100*state.p_dem
    state=state.rename(columns={'margin_pp':'D/IND−R margin','lo95_pp':'95% low','hi95_pp':'95% high'})
    lines += [markdown_table(state,['Contest','D/IND−R margin','D/IND win %','95% low','95% high']), '',
              '## Recently polled races with broad uncertainty', '']
    broad=watchlist['broad'].query("model == 'Bayesian'")
    if broad.empty:lines+=['No reference-model contests meet the configured recency and interval-width thresholds.','']
    else:
        lines += [markdown_table(broad,['contest','latest_poll','recent_samples','recent_firms','stronger_coverage','width95_pp']), '']
    settings=watchlist.get('parameters',{})
    lines += ['Watchlist settings: '+', '.join(f'{k}={v}' for k,v in settings.items())+'.','']
    if surprise is not None:
        from live_surprise_watchlist import display_table, METHOD
        lines += ['## Races to watch — room for a different outcome', '', METHOD, '',
                  'Coverage: at least '+str(surprise['parameters']['min_samples'])+' independent eligible samples from '+
                  str(surprise['parameters']['min_firms'])+' firms in the past '+str(surprise['parameters']['recent_days'])+' days.', '',
                  'Available core models: '+', '.join(map(model_label, surprise['parameters']['available_models']))+'.', '']
        for key,title in [('polled','Adequately polled races'),('thin','Thinly polled or no recent polls')]:
            lines += ['### '+title, '', markdown_table(display_table(surprise[key])) if not surprise[key].empty else 'No qualifying races.', '']
        lines += ['[All races and numerical scores](../../results/forecast/live_reports/surprise_all.parquet) · '
                  '[Watchlist settings and provenance](../../results/forecast/live_reports/surprise_parameters.json)', '']
    if history_run is not None:
        hm=json.loads((history_run/'run.json').read_text());history=pd.read_parquet(history_run/'control_history.parquet')
        lines += ['## Control probability over cutoff dates','',
            '**This is a retrospective reconstruction, not a record of forecasts issued on those dates.** The current roster, revised historical features and September-calibrated model are reused at earlier cutoffs.', '',
            '![Control probabilities across cutoff dates](control_history.png)', '',
            '### Recent reference-model cutoffs','']
        recent=history[history.model.eq('Bayesian')].sort_values('cutoff').tail(hm['last_days'])
        lines += [markdown_table(recent,['cutoff','D_control_pct','R_control_pct','expected_D','D_lo70','D_hi70']), '',
            f'History mode: **{hm["feature_mode"]}**; regular spacing: **{hm["every_days"]} days**. Small differences can include Monte Carlo variation. All models and cutoff rows are in the HTML and supporting Parquet tables.','']
    else:lines+=['## Cutoff history','','This current-only report does not yet include cutoff history. Run notebook 04 to publish the full history.','']
    if published is not None:
        from live_published_comparison import sections, method
        lines += ['## Comparison with published forecasts', '', method(published), '']
        for title, frame in sections(published):
            lines += ['### '+title, '', markdown_table(frame) if not frame.empty else 'No rows qualify or the source is unavailable. Check source status above.', '']
        lines += ['[All matched state comparisons](../../results/forecast/live_reports/published_all_states.parquet) · '
                  '[Publisher snapshots and provenance](../../results/forecast/live_reports/published_sources.json) · '
                  '[Comparison settings](../../results/forecast/live_reports/published_parameters.json)', '']
    images=sorted(out.glob('share_*.png'))
    if images:
        lines += ['## Shareable images', '', 'The tables above remain available. These PNGs are generated from the same saved results on every run.', '']
        for picture in images:
            lines += [f'![{picture.stem.removeprefix("share_").replace("_"," ")}]({picture.name})', '']
        lines += ['[Image manifest](../../results/forecast/live_reports/share_images.json)', '']
    lines += ['## Provenance and interpretation','',
        '- [Forecast settings, input hash and source receipts](../../results/forecast/live_reports/forecast_metadata.json)',
        '- [Complete state predictions](../../results/forecast/live_reports/predictions.parquet)',
        '- [Chamber results](../../results/forecast/live_reports/seats.parquet)', '',
        'The model retains its candidate, caucus, election-rule, historical-vintage and small-sample limitations. Probabilities are model estimates. An unchanged fitted checkpoint can produce different forecasts when polls, feature observations or the cutoff change.', '']
    (out/'report.md').write_text('\n'.join(lines))


def save_report(live_run, watchlist, history_run=None, surprise=None, published=None):
    """Save Markdown and self-contained HTML reports, plus supporting tables."""
    live_run = lab.verify_run(live_run)
    meta = json.loads((live_run/'run.json').read_text())
    from live_published_comparison import build_published_comparison, save_comparison, render_comparison
    if published is None:
        published = build_published_comparison(live_run, offline=True)
    if published['parameters']['source_manifest_sha256'] != lab.sha(live_run/'manifest.json'):
        raise ValueError('Published comparison and report use different forecasts')
    out = lab.new_run('live_reports')
    save_comparison(published, out)
    from live_poll_audit import save_poll_audit, METHOD as POLL_SIDE_METHOD
    poll_coverage = save_poll_audit(live_run, out)
    lab.write_json(out/'forecast_metadata.json',meta)
    from live_surprise_watchlist import build_surprise_watchlist, display_table, METHOD
    if surprise is None:
        settings = watchlist.get('parameters',{})
        surprise = build_surprise_watchlist(live_run, **{k:settings[k] for k in
            ['recent_days','min_samples','min_firms'] if k in settings})
    if surprise['parameters']['source_manifest_sha256'] != lab.sha(live_run/'manifest.json'):
        raise ValueError('Surprise watchlist and report use different forecasts')
    for name in ['all','polled','thin']:
        surprise[name].to_parquet(out/f'surprise_{name}.parquet',index=False)
    lab.write_json(out/'surprise_parameters.json',surprise['parameters'])
    seats = _seat_history_row(live_run)
    pred = pd.read_parquet(live_run/'predictions.parquet')
    seats.to_parquet(out/'seats.parquet',index=False)
    pred.to_parquet(out/'predictions.parquet',index=False)
    for name in ['recent','broad','summary']:
        watchlist[name].to_parquet(out/f'watchlist_{name}.parquet',index=False)
    def table(frame):return label_frame(frame).to_html(index=False,float_format=lambda x:f'{x:.2f}',na_rep='—',escape=True)
    parts = [f'<h1>2026 Senate forecast — {html.escape(meta["as_of"])}</h1>',
        '<p>Positive margins favor D/Independent. Probabilities are model estimates, not certified outcomes. '
        'D/Independent control requires 51 seats; Republican control includes a50–50 Senate with the assumed GOP vice-presidential tie-break.</p>',
        '<h2>Current chamber forecast — all models</h2>',
        '<p>'+html.escape(MODEL_GUIDE)+'</p>',
        table(seats[['model','point_D','point_R','expected_D','expected_R','D_control_pct','R_control_pct','D_lo70','D_hi70']]),
        '<h2>Recently polled states with broad uncertainty</h2>',
        '<p>Wide intervals are not themselves evidence of fat tails. The stronger-coverage flag distinguishes multiple recent samples/firms from a single recent poll.</p>',
        '<p>Watchlist settings: '+html.escape(json.dumps(watchlist.get('parameters',{})))+'</p>',
        table(watchlist['summary']),table(watchlist['broad'].query("model == 'Bayesian'")),
        '<h2>State margins, probabilities and95% ranges — all models</h2>']
    # Keep the new watchlist beside the existing uncertainty summary.
    parts.pop()  # Move the all-model state-details heading below the watchlist.
    parts += ['<h2>Races to watch — room for a different outcome</h2>',
              '<p>'+html.escape(METHOD)+'</p>',
              '<p>Settings: '+html.escape(json.dumps(surprise['parameters']))+'</p>']
    for key,title in [('polled','Adequately polled races'),('thin','Thinly polled or no recent polls')]:
        parts += ['<h3>'+title+'</h3>',table(display_table(surprise[key])) if not surprise[key].empty else '<p>No qualifying races.</p>']
    parts += ['<h2>Poll coverage and independent candidates</h2>', '<p>'+html.escape(POLL_SIDE_METHOD)+'</p>', table(poll_coverage['summary']), '<h2>State margins, probabilities and 95% ranges — all models</h2>']
    state = pred[['model','geography','special','margin_pp','p_dem','lo95_pp','hi95_pp']].copy()
    state['D_win_pct'] = 100*state.pop('p_dem')
    for model,frame in state.groupby('model',sort=False):
        parts.extend([f'<details><summary>{html.escape(model_label(model))}</summary>',table(frame.drop(columns='model')),'</details>'])
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
            '<h3>Recent daily probabilities (%)</h3>',label_frame(recent_table(history,hmeta['last_days'])).to_html(),
            '<details><summary>All cutoff results and changes</summary>',table(history),'</details>',
            '<details><summary>Polling evidence by cutoff</summary>',table(evidence),'</details>'])
    parts.extend(['<h2>Comparison with published forecasts</h2>', render_comparison(published).data])
    from live_share_images import build_share_images
    share_images=build_share_images(out,live_run,watchlist,surprise,published)
    parts += ['<h2>Shareable images</h2>', '<p>These PNGs are generated from the same results. The original tables remain above.</p>']
    for picture in share_images:
        encoded=base64.b64encode(picture.read_bytes()).decode()
        label=html.escape(picture.stem.removeprefix('share_').replace('_',' '))
        parts += [f'<details><summary>{label}</summary><img alt="{label}" src="data:image/png;base64,{encoded}"></details>']
    parts.extend(['<h2>Freshness and provenance</h2>',
        '<pre>'+html.escape(json.dumps(meta,indent=2))+'</pre>'])
    page='<!doctype html><html><head><meta charset="utf-8"><title>2026 Senate forecast report</title><style>body{font-family:system-ui,sans-serif;margin:32px;line-height:1.45}table{border-collapse:collapse;font-size:13px;margin:16px 0}th,td{padding:6px 10px;border:1px solid #ddd;text-align:right}th{background:#eef2f6}details{margin:16px 0}pre{white-space:pre-wrap;overflow-wrap:anywhere}img{max-width:100%}</style></head><body>'+''.join(parts)+'</body></html>'
    (out/'report.html').write_text(page)
    markdown_report(out,meta,seats,pred,watchlist,history_run,surprise,published)
    return lab.finish(out,dict(kind='live_report',as_of=meta['as_of'],
        live_run=str(live_run.relative_to(lab.ROOT)),live_manifest_sha256=lab.sha(live_run/'manifest.json'),
        published_parameters=published['parameters'],
        watchlist_parameters=watchlist.get('parameters',{}),surprise_parameters=surprise['parameters'],
        history_run=str(history_run.relative_to(lab.ROOT)) if history_run else None,
        history_manifest_sha256=lab.sha(history_run/'manifest.json') if history_run else None))
