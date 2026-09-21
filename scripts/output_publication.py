"""Publish only the latest useful results; keep execution history in local cache."""
from pathlib import Path
import json
import os
import shutil
import tempfile
import pandas as pd

INTERNAL = {'refresh', 'cutoff_forecasts'}
FORECAST = {'live', 'live_reports', 'control_history'}
TRAINING = {'training', 'student_refit'}
TITLES = {
    'reproduction': 'Frozen model reproduction', 'blend_weights': 'Blend-weight comparison',
    'scenarios': 'Wave and polling-error scenarios', 'matched_student': 'Matched Student-t comparison',
    'matched_student_review': 'Matched Student-t review', 'portfolio': 'All-model comparison and mixtures',
    'poll_weights': 'Poll-weight experiments', 'model_disagreement': 'Where the models disagree',
    'training': 'Historical training reproduction', 'student_refit': 'Student posterior rerun',
    'live': 'Latest forecast results', 'control_history': 'Cutoff history', 'live_reports': 'Forecast report',
}


def result_path(root, kind):
    group = 'forecast' if kind in FORECAST else 'training' if kind in TRAINING else 'experiments'
    return Path(root)/'outputs/results'/group/kind


def replace_directory(source, destination):
    """Stage a complete copy on the destination filesystem; rollback on failure."""
    destination=Path(destination);destination.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(dir=destination.parent,prefix='.publish-') as temp:
        staged=Path(temp)/'new';shutil.copytree(source,staged)
        previous=Path(temp)/'old'
        if destination.exists():destination.rename(previous)
        try:staged.rename(destination)
        except BaseException:
            if previous.exists():previous.rename(destination)
            raise


def markdown_table(frame, columns=None, floatfmt=".2f"):
    if columns is not None:frame=frame[[c for c in columns if c in frame]]
    frame=frame.copy()
    for c in frame:
        if pd.api.types.is_datetime64_any_dtype(frame[c]):frame[c]=frame[c].dt.strftime('%Y-%m-%d')
    if 'scenario' in frame:
        frame['scenario']=frame.scenario.replace({'matched_live':'Matched September','oct31':'October 31'})
    labels={'scenario':'Horizon','model':'Model','variant':'Poll weighting','geography':'State',
        'races':'Races','n':'Races','correct':'Correct calls','absolute_error_pp':'Margin MAE (pp)',
        'brier':'Brier score','point_D':'D seats (mean winners)','point_R':'R seats (mean winners)',
        'expected_D':'Expected D seats','D_control_pct':'D control %','R_control_pct':'R control %',
        'D_lo70':'D seats: 70% low','D_hi70':'D seats: 70% high','margin_spread':'Margin spread (pp)',
        'prob_spread_pct':'D win probability spread (pp)','contest':'Contest','latest_poll':'Latest poll',
        'recent_samples':'Recent samples','recent_firms':'Recent firms','stronger_coverage':'Stronger coverage',
        'width95_pp':'95% interval width (pp)','cutoff':'Cutoff'}
    return frame.rename(columns=labels).fillna('—').to_markdown(index=False,floatfmt=floatfmt)


def write_index(root):
    root=Path(root);out=root/'outputs';out.mkdir(exist_ok=True)
    lines=['# Results — start here','',
        'Only the latest published results live here. Each rerun replaces the corresponding report and result bundle; Git history preserves committed versions.','',
        '## Forecast','']
    if (out/'reports/forecast/report.md').exists():
        lines += ['- [Read the forecast](reports/forecast/report.md) — Markdown summary, state forecasts, source status and cutoff history.',
                  '- [Open the browser report](reports/forecast/report.html) — self-contained HTML (download/open locally).']
    else:lines+=['Run notebook 04 to publish the forecast report.']
    lines += ['', '## Comparisons and training', '']
    for p in sorted((out/'reports').glob('*/*.md')):
        if p.parent.name=='forecast':continue
        lines.append(f'- [{TITLES.get(p.stem,p.stem.replace("_"," ").title())}]({p.relative_to(out).as_posix()})')
    lines += ['', '## Validation', '',
        '- [Notebook execution status](validation/notebooks.md)',
        '- [Storage and rerun validation](validation/output_cleanup.md)', '',
        '## Supporting files', '',
        '- `results/forecast/`: latest forecast tables, joint arrays and cutoff history.',
        '- `results/experiments/`: latest tables and diagnostics for each comparison.',
        '- `results/training/`: latest explicit training/sampler reruns. The active model remains in `../assets/`.',
        '- Every result bundle includes `run.json` and `manifest.json`; keep bundles complete.', '',
        'Timestamped executions, intermediate forecasts, logs and older migrated outputs are local-only under `../cache/`. They are ignored by Git. Source-audit and migration documentation remain under `../reports/`.', '',
        'Rerun all notebooks: `python scripts/run_notebooks.py` from the project root.']
    (out/'README.md').write_text('\n'.join(lines)+'\n')


def experiment_report(root, run, kind):
    meta=json.loads((run/'run.json').read_text())
    group='training' if kind in TRAINING else 'experiments'
    destination=Path(root)/'outputs/reports'/group/(kind+'.md');destination.parent.mkdir(parents=True,exist_ok=True)
    result=result_path(root,kind)
    link=Path(os.path.relpath(result,destination.parent)).as_posix()
    lines=[f'# {TITLES.get(kind,kind.replace("_"," ").title())}', '',
        f'[Complete supporting results]({link}/) · [Run settings]({link}/run.json)', '',
        f'Latest execution: `{run.name}`. Forecast cutoff: **{meta.get("as_of","frozen historical/reference inputs")}**.', '',
        'Margins are Democratic minus Republican percentage points. Experiments do not replace the active model or automatically select blend weights.','']
    for name,title in [('historical_summary.csv','Historical comparison'),('summary.parquet','Historical comparison'),
                       ('current_seats.csv','Current chamber forecast'),('seats.parquet','Chamber results'),
                       ('state_ranges.parquet','Largest current disagreements')]:
        p=run/name
        if not p.exists():continue
        frame=pd.read_parquet(p) if p.suffix=='.parquet' else pd.read_csv(p)
        if 'first_cycle' in frame:frame=frame[frame.first_cycle.eq(2016)]
        if 'calibration' in frame:frame=frame[frame.calibration.eq('Refit bias')]
        if 'evidence' in frame and frame.evidence.eq('live').any():frame=frame[frame.evidence.eq('live')]
        if name=='seats.parquet' and 'cycle' in frame and frame.cycle.eq(2026).any():frame=frame[frame.cycle.eq(2026)]
        if kind=='scenarios' and 'random_mode' in frame:
            frame=frame[frame.random_mode.eq('none')&frame.wave_pp.eq(0)&frame.poll_error_pp.eq(0)]
            title='Baseline before scenario stress'
        if 'prob_spread' in frame:
            frame=frame[frame.scope.eq('five core')].sort_values('prob_spread',ascending=False).head(10).copy()
            frame['prob_spread_pct']=100*frame.prob_spread
        if 'p_D_control' in frame:frame=frame.assign(D_control_pct=100*frame.p_D_control)
        columns=['scenario','model','variant','geography','races','n','correct','absolute_error_pp','brier',
                 'point_D','point_R','expected_D','D_control_pct','D_lo70','D_hi70','margin_spread','prob_spread_pct']
        selected=[c for c in columns if c in frame]
        if not selected or frame.empty:continue
        lines += ['## '+title,'',markdown_table(frame.head(40),selected,floatfmt=".3f"),'']
        if len(frame)>40:lines += [f'Showing 40 of {len(frame)} rows; the complete table is in [{name}]({link}/{name}).','']
    for picture in sorted(run.glob('*.png')):
        lines += [f'![{picture.stem.replace("_"," ")}]({link}/{picture.name})','']
    if kind in TRAINING:
        lines += ['## Fit settings','',markdown_table(pd.DataFrame([{'Setting':k,'Value':str(v)} for k,v in meta.items()])), '',
                  'This is a reproduction/posterior rerun. The saved active model in `assets/` is unchanged.','']
    lines += [f'For all scenarios, per-state tables, sampler diagnostics and exact provenance, see the [complete result bundle]({link}/).','']
    destination.write_text('\n'.join(lines))


def publish(root, run):
    run=Path(run);kind=run.parent.name
    if kind in INTERNAL:return
    replace_directory(run,result_path(root,kind))
    if kind=='live_reports':
        with tempfile.TemporaryDirectory() as temp:
            stage=Path(temp)
            for name in ['report.md','report.html','control_history.png']:
                if (run/name).exists():shutil.copyfile(run/name,stage/name)
            replace_directory(stage,Path(root)/'outputs/reports/forecast')
    elif kind not in FORECAST:experiment_report(root,run,kind)
    write_index(root)
