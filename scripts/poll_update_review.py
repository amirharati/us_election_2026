"""Frozen-prior polling likelihood sensitivity; no downloads or prior refitting."""
from pathlib import Path
from datetime import datetime, timezone
import json
import numpy as np
import pandas as pd
from scipy.stats import norm
import simple_bayesian_polling as v1
import bayesian_revision2 as v2

SOURCE = '20260919T181021.670795Z'
PRIORS = ['control_state', 'history4_state', 'shrink1_state']
SCALES = [1., 2., 4.]  # covariance multipliers, not standard-deviation multipliers
CONFIG = dict(scales=SCALES, priors=PRIORS, validation_cycles=3,
              minimum_validation_cycles=3, draws=50000, seed=193721,
              objective='equal_cycle_mean_marginal_negative_log_density',
              insufficient_history_scale=1., as_of='2026-09-17')


def update(test, prior_cov, poll, scale=1.):
    """Integrate saved bias uncertainty and scale the entire likelihood covariance."""
    if not np.isfinite(scale) or scale <= 0:
        raise ValueError('Positive finite variance scale required')
    si = np.array([v2.STATES.index(s) for s in test.geography], int)
    obs = np.flatnonzero(test.q_pp.notna().to_numpy())
    so = si[obs]
    prior = 100 * test.prior.to_numpy()
    r = poll['covariance'][np.ix_(so, so)] + poll['bias_covariance'][np.ix_(so, so)]
    r = scale * (r + np.diag(16. / test.firm_mass.to_numpy()[obs]))
    values = test.q_pp.to_numpy()[obs] - poll['bias_mean'][so]
    if len(obs):
        mean, cov, _ = v1.normal_update(prior, prior_cov, obs, values, r)
        gain = np.linalg.solve(prior_cov[np.ix_(obs, obs)] + r, prior_cov[obs, :]).T
    else:
        mean, cov = prior.copy(), prior_cov.copy()
        gain = np.zeros((len(test), 0))
    sd = np.sqrt(np.diag(cov))
    pred = test.copy()
    pred['prediction_pp'] = mean
    pred['prediction'] = mean / 100
    pred['posterior_sd_pp'] = sd
    pred['p_dem'] = norm.cdf(mean / sd)
    pred['log_predictive_density'] = norm.logpdf(100 * pred.actual, mean, sd)
    for level in [50, 70, 80, 95]:
        z = norm.ppf((1 + level / 100) / 2)
        pred[f'lo{level}_pp'] = mean - z * sd
        pred[f'hi{level}_pp'] = mean + z * sd
    own = np.zeros(len(test))
    own[obs] = gain[obs, np.arange(len(obs))] * (values - prior[obs])
    diag = test[['target_id', 'cycle', 'scenario', 'geography', 'actual', 'q_pp', 'firm_mass', 'history_selection_10pp']].copy()
    diag['prior_pp'] = prior
    diag['prior_sd_pp'] = np.sqrt(np.diag(prior_cov))
    diag['bias_pp'] = poll['bias_mean'][si]
    diag['corrected_poll_pp'] = test.q_pp.to_numpy() - poll['bias_mean'][si]
    diag['likelihood_sd_pp'] = np.nan
    diag.loc[obs, 'likelihood_sd_pp'] = np.sqrt(np.diag(r))
    diag['posterior_pp'] = mean
    diag['posterior_sd_pp'] = sd
    diag['sd_ratio'] = sd / diag.prior_sd_pp
    diag['own_poll_shift_pp'] = own
    diag['other_poll_shift_pp'] = mean - prior - own
    diag['own_gain'] = np.nan
    diag.loc[obs, 'own_gain'] = gain[obs, np.arange(len(obs))]
    # Exact additive decomposition; gain weights can be signed and need not sum to one.
    return pred, cov, diag


def select_scale(scores, forecast_cycle):
    earlier = scores[scores.cycle < forecast_cycle]
    years = sorted(earlier.cycle.unique())[-3:]
    if len(years) < 3:
        return 1., years, 'fallback_insufficient_saved_validation_cycles'
    means = earlier[earlier.cycle.isin(years)].groupby('variance_scale').marginal_nll.mean()
    if set(means.index) != set(SCALES) or not np.isfinite(means).all():
        raise ValueError('Incomplete validation scale grid')
    return float(min(means.index, key=lambda x: (means.loc[x], x))), years, 'last_three_saved_past_folds'


def metrics(p):
    rows = []
    for period, first in [('recent_2016_2024', 2016), ('tuned_2018_2024', 2018), ('all_2012_2024', 2012)]:
        for (sc, prior, model), g in p[p.cycle.between(first, 2024)].groupby(['scenario', 'prior_model', 'model']):
            masks = dict(all=np.ones(len(g), bool), polled=g.q_pp.notna(), no_polls=g.q_pp.isna(),
                         competitive=g.history_selection_10pp.eq('competitive'),
                         noncompetitive=g.history_selection_10pp.eq('not_selected'),
                         unknown_history=g.history_selection_10pp.eq('unknown_history'))
            for group, mask in masks.items():
                q = g[mask]
                error = 100 * q.actual - q.prediction_pp
                row = dict(period=period, scenario=sc, prior_model=prior, model=model, group=group,
                           n=len(q), cycles=q.cycle.nunique(), correct=int(((q.prediction_pp > 0) == (q.actual > 0)).sum()),
                           mae_pp=float(error.abs().groupby(q.cycle).mean().mean()),
                           signed_error_pp=float(error.groupby(q.cycle).mean().mean()),
                           marginal_nll=float((-q.log_predictive_density).groupby(q.cycle).mean().mean()),
                           brier=float(((q.p_dem - (q.actual > 0)) ** 2).mean()),
                           mean_sd_pp=float(q.posterior_sd_pp.mean()))
                for n in [50, 70, 80, 95]:
                    row['coverage'+str(n)] = float(((100*q.actual >= q[f'lo{n}_pp']) & (100*q.actual <= q[f'hi{n}_pp'])).mean())
                rows.append(row)
    return pd.DataFrame(rows)


def build(lab):
    lab = Path(lab).resolve()
    source = lab/'reports/prior_sensitivity'/SOURCE
    source_sha = v1.verify(source)
    settings = json.loads((source/'settings.json').read_text())
    upstream = Path(settings['source'])
    upstream_sha = v1.verify(upstream)
    oldhashes = {p.name: v1.sha(p) for p in lab.glob('*.ipynb') if p.name != 'POLLING_UPDATE_REVIEW.ipynb'}
    out = lab/'reports/poll_update_review'/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')
    (out/'forecasts').mkdir(parents=True)
    print('OUTPUT', out, flush=True)
    source_p = pd.read_parquet(source/'predictions.parquet')
    source_f = pd.read_parquet(source/'folds.parquet')
    roster = pd.read_parquet(upstream/'full_seat_ledger.parquet')
    predictions, diagnostics, seats, folds, scores, tuning, checks = [], [], [], [], [], [], []
    for (sc, prior_model), group in source_f[source_f.model.isin(PRIORS)].groupby(['scenario', 'model']):
        for row in group.sort_values('cycle').itertuples():
            test = source_p[source_p.model.eq(prior_model) & source_p.scenario.eq(sc) & source_p.cycle.eq(row.cycle)].sort_values('target_id').reset_index(drop=True)
            saved = np.load(source/row.forecast_path)
            assert np.array_equal(test.target_id.to_numpy(str), saved['target_ids'])
            k = saved['prior_covariance']
            poll = dict(np.load(source/row.poll_path))
            variants = {scale: update(test, k, poll, scale) for scale in SCALES}
            control, cov, diag = variants[1.]
            checks.append(bool(np.allclose(control.prediction_pp, test.prediction_pp, atol=1e-10) and np.allclose(cov, saved['posterior_covariance'], atol=1e-10)))
            past = pd.DataFrame([r for r in scores if r['scenario'] == sc and r['prior_model'] == prior_model], columns=['scenario','prior_model','cycle','variance_scale','marginal_nll'])
            selected, years, status = select_scale(past, row.cycle)
            for rec in past[past.cycle.isin(years)].to_dict('records'):
                tuning.append(dict(**rec, forecast_cycle=row.cycle, validation_cycle=rec['cycle'], selected_scale=selected, status=status))
            for scale, (pred, _, _) in variants.items():
                if row.cycle < 2026:
                    scores.append(dict(scenario=sc, prior_model=prior_model, cycle=row.cycle, variance_scale=scale,
                                       marginal_nll=float(-pred.log_predictive_density.mean())))
            for model, scale in [('R1', 1.), ('R2', 2.), ('R4', 4.), ('R_selected', selected)]:
                pred, cov, diag = variants[scale]
                pred = pred.assign(prior_model=prior_model, model=model, variance_scale=scale)
                predictions.append(pred)
                if model == 'R1':
                    diagnostics.append(diag.assign(prior_model=prior_model))
                rng = np.random.default_rng(CONFIG['seed'] + row.cycle + 10000*(sc == 'oct31'))
                draws = pred.prediction_pp.to_numpy() + rng.standard_normal((CONFIG['draws'], len(test))) @ np.linalg.cholesky(cov).T
                rr = roster[roster.scenario.eq(sc) & roster.cycle.eq(row.cycle)]
                seat = v1.seat_counts(rr, test, pred, draws)
                counts = seat['fixed_D'] + (draws > 0).sum(axis=1)
                lo, hi = np.quantile(counts, [.15, .85], method='inverted_cdf')
                seats.append(dict(scenario=sc, cycle=row.cycle, prior_model=prior_model, model=model,
                                  variance_scale=scale, **seat, expected_D_exact=float(seat['fixed_D']+pred.p_dem.sum()), D_lo70=int(lo), D_hi70=int(hi)))
                path = f'forecasts/{sc}_{row.cycle}_{prior_model}_{model}.npz'
                np.savez_compressed(out/path, target_ids=test.target_id.to_numpy(str), prior_covariance=k,
                                    posterior_covariance=cov, means_pp=pred.prediction_pp.to_numpy(),
                                    seat_count_frequency=np.bincount(counts, minlength=101))
                folds.append(dict(scenario=sc, cycle=row.cycle, prior_model=prior_model, model=model, variance_scale=scale,
                                  source_forecast=row.forecast_path, source_poll=row.poll_path, forecast_path=path,
                                  validation_cycles=','.join(map(str, years)) if model == 'R_selected' else '',
                                  tuning_status=status if model == 'R_selected' else 'fixed_sensitivity'))
    p = pd.concat(predictions, ignore_index=True)
    d = pd.concat(diagnostics, ignore_index=True)
    cal = metrics(p)
    cycle = p[p.actual.notna()].groupby(['scenario','cycle','prior_model','model']).apply(
        lambda q: pd.Series(dict(n=len(q), correct=int(((q.prediction_pp>0)==(q.actual>0)).sum()),
                                 mae_pp=float((100*q.actual-q.prediction_pp).abs().mean()),
                                 marginal_nll=float(-q.log_predictive_density.mean()))), include_groups=False).reset_index()
    stages = []
    for (sc, pm), g in d[d.cycle.between(2016,2024) & d.q_pp.notna()].groupby(['scenario','prior_model']):
        for stage, center, sd in [('prior','prior_pp','prior_sd_pp'), ('raw_poll','q_pp','likelihood_sd_pp'),
                                   ('corrected_poll','corrected_poll_pp','likelihood_sd_pp'), ('posterior','posterior_pp','posterior_sd_pp')]:
            error = 100*g.actual-g[center]
            z = error/g[sd]
            stages.append(dict(scenario=sc, prior_model=pm, stage=stage, n=len(g),
                               mae_pp=float(error.abs().groupby(g.cycle).mean().mean()),
                               signed_error_pp=float(error.groupby(g.cycle).mean().mean()), rms_z=float(np.sqrt((z*z).mean())),
                               coverage70=float((z.abs()<=norm.ppf(.85)).mean()), coverage95=float((z.abs()<=norm.ppf(.975)).mean())))
    tables = dict(predictions=p, diagnostics=d, seats=pd.DataFrame(seats), folds=pd.DataFrame(folds),
                  validation_scores=pd.DataFrame(scores), tuning=pd.DataFrame(tuning), calibration=cal,
                  cycle_scores=cycle, polled_stage_diagnostics=pd.DataFrame(stages))
    for name, table in tables.items():
        table.to_parquet(out/(name+'.parquet'), index=False)
    audit = dict(control_reproduces=all(checks), unique_predictions=not p.duplicated(['scenario','prior_model','model','target_id']).any(),
                 future_labels_blank=bool(p[p.cycle.eq(2026)].actual.isna().all()),
                 tuning_past_only=bool(tables['tuning'].validation_cycle.lt(tables['tuning'].forecast_cycle).all()),
                 decomposition_exact=bool(np.allclose(d.posterior_pp, d.prior_pp+d.own_poll_shift_pp+d.other_poll_shift_pp)),
                 source_unchanged=v1.verify(source)==source_sha, upstream_unchanged=v1.verify(upstream)==upstream_sha,
                 old_notebooks_unchanged=all(v1.sha(lab/n)==h for n,h in oldhashes.items()),
                 finite_forecasts=bool(np.isfinite(p[['prediction_pp','posterior_sd_pp','p_dem']]).all().all()),
                 valid_probabilities=bool(p.p_dem.between(0,1).all()))
    for r in tables['folds'].itertuples():
        z = np.load(out/r.forecast_path)
        old = np.load(source/r.source_forecast)
        assert np.array_equal(z['prior_covariance'], old['prior_covariance'])
        assert np.linalg.eigvalsh(z['posterior_covariance']).min()>0
        assert z['seat_count_frequency'].sum()==CONFIG['draws']
    audit.update(all_prior_covariances_frozen=True, positive_posterior_covariances=True, seat_draw_totals=True)
    v1.json_write(out/'completion_audit.json', dict(passed=all(audit.values()), checks=audit))
    assert all(audit.values()), audit
    v1.json_write(out/'settings.json', dict(config=CONFIG, source=str(source), source_sha256=source_sha,
                  upstream=str(upstream), upstream_sha256=upstream_sha, old_notebook_hashes=oldhashes,
                  selection_note='Validation uses saved past-only outer forecasts; three required, so first tuned forecast is 2018. No refitting prior means, strengths, covariance, polling bias or polling covariance.',
                  promotion=False, polling_refreshed=False))
    (out/'recipe').mkdir()
    for script in (lab/'scripts').glob('*.py'):
        (out/'recipe'/script.name).write_bytes(script.read_bytes())
    v1.manifest(out)
    v1.json_write(out.parent/'latest.json', dict(artifact=out.name, manifest_sha256=v1.sha(out/'manifest.json')))
    review(out, lab)
    return out


def review(out, lab):
    """Reconstruct predictions, add explanatory tables and publish the review."""
    out, lab = Path(out), Path(lab)
    v1.verify(out)
    settings = json.loads((out/'settings.json').read_text())
    source = Path(settings['source'])
    p = pd.read_parquet(out/'predictions.parquet')
    old = pd.read_parquet(source/'predictions.parquet')
    folds = pd.read_parquet(out/'folds.parquet')
    scores = pd.read_parquet(out/'validation_scores.parquet')
    seats = pd.read_parquet(out/'seats.parquet')
    reconstruct, choices, means, accounting, monotone = [], [], [], [], []
    for row in folds.itertuples():
        test = old[old.scenario.eq(row.scenario) & old.cycle.eq(row.cycle) & old.model.eq(row.prior_model)].sort_values('target_id').reset_index(drop=True)
        z = np.load(source/row.source_forecast)
        pred, cov, _ = update(test, z['prior_covariance'], dict(np.load(source/row.source_poll)), row.variance_scale)
        saved = np.load(out/row.forecast_path)
        q = p[p.scenario.eq(row.scenario) & p.cycle.eq(row.cycle) & p.prior_model.eq(row.prior_model) & p.model.eq(row.model)].sort_values('target_id')
        cols = ['prediction_pp','posterior_sd_pp','p_dem','lo70_pp','hi70_pp','lo95_pp','hi95_pp']
        reconstruct.append(np.allclose(pred[cols], q[cols], atol=1e-10) and np.allclose(cov, saved['posterior_covariance'], atol=1e-10))
        means.append(np.array_equal(test.prior.to_numpy(), q.prior.to_numpy()))
        seat = seats[seats.scenario.eq(row.scenario) & seats.cycle.eq(row.cycle) & seats.prior_model.eq(row.prior_model) & seats.model.eq(row.model)].iloc[0]
        accounting.append(abs(seat.expected_D_exact-seat.fixed_D-q.p_dem.sum())<1e-10 and seat.point_D==seat.fixed_D+(q.prediction_pp>0).sum())
        monotone.append(np.linalg.eigvalsh(cov-z['posterior_covariance']).min() > -1e-8)
        if row.model == 'R_selected':
            candidate = scores[scores.scenario.eq(row.scenario) & scores.prior_model.eq(row.prior_model)]
            scale, years, status = select_scale(candidate, row.cycle)
            choices.append(scale==row.variance_scale and ','.join(map(str,years))==row.validation_cycles and status==row.tuning_status)
    audit = json.loads((out/'completion_audit.json').read_text())
    audit['checks'].update(all_forecasts_reconstructed=bool(all(reconstruct)), all_prior_means_frozen=bool(all(means)),
                           scale_selection_reconstructed=bool(all(choices)), exact_seat_accounting=bool(all(accounting)),
                           inflation_never_reduces_covariance=bool(all(monotone)))
    audit['passed'] = all(audit['checks'].values())
    assert audit['passed'], audit
    v1.json_write(out/'completion_audit.json', audit)
    d = pd.read_parquet(out/'diagnostics.parquet')
    polled = d[d.cycle.between(2016,2024) & d.q_pp.notna()].copy()
    for name, center in [('prior','prior_pp'), ('poll','corrected_poll_pp'), ('posterior','posterior_pp')]:
        polled[name+'_error_pp'] = 100*polled.actual-polled[center]
    dep = []
    for (sc, pm), g in polled.groupby(['scenario','prior_model']):
        a,b = g.prior_error_pp,g.poll_error_pp
        ac = a-g.groupby('cycle').prior_error_pp.transform('mean')
        bc = b-g.groupby('cycle').poll_error_pp.transform('mean')
        dep.append(dict(scenario=sc, prior_model=pm, n=len(g), cycles=g.cycle.nunique(),
                        prior_poll_error_correlation=float(a.corr(b)), within_cycle_centered_correlation=float(ac.corr(bc)),
                        same_error_sign_fraction=float((a*b>0).mean()), median_posterior_prior_sd_ratio=float(g.sd_ratio.median())))
    dependence = pd.DataFrame(dep)
    cycle_bias = polled.groupby(['scenario','prior_model','cycle']).agg(n=('geography','size'),
                    prior_error_pp=('prior_error_pp','mean'), poll_error_pp=('poll_error_pp','mean'), posterior_error_pp=('posterior_error_pp','mean')).reset_index()
    misses = d[d.cycle.eq(2024)&d.scenario.eq('oct31')&d.prior_model.eq('control_state')].copy()
    misses['actual_pp'] = 100*misses.actual
    misses['error_pp'] = misses.actual_pp-misses.posterior_pp
    misses = misses.sort_values('error_pp', key=abs, ascending=False)
    for name, table in [('error_dependence',dependence),('cycle_bias',cycle_bias),('late2024_decomposition',misses)]:
        table.to_parquet(out/(name+'.parquet'), index=False)
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    cal = pd.read_parquet(out/'calibration.parquet')
    fig, axes = plt.subplots(1,2,figsize=(12,4.5))
    for ax, sc in zip(axes,['matched_live','oct31']):
        q = cal.query('period=="recent_2016_2024" and group=="all" and prior_model=="control_state"')
        for row in q[q.scenario.eq(sc)].itertuples():
            ax.plot([50,70,80,95],[100*getattr(row,'coverage'+str(n)) for n in [50,70,80,95]],marker='o',label=row.model)
        ax.plot([50,95],[50,95],'k--',label='nominal')
        ax.set(title=sc,xlabel='Nominal interval (%)',ylabel='Observed coverage (%)');ax.legend()
    fig.tight_layout();fig.savefig(out/'coverage.png',dpi=140);plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(12,4.5))
    for ax,sc in zip(axes,['matched_live','oct31']):
        g=polled[polled.scenario.eq(sc)&polled.prior_model.eq('control_state')]
        for y,q in g.groupby('cycle'):ax.scatter(q.prior_error_pp,q.poll_error_pp,label=str(y),alpha=.75)
        ax.axhline(0,color='gray',lw=.6);ax.axvline(0,color='gray',lw=.6)
        ax.set(title=sc,xlabel='Actual − prior (pp)',ylabel='Actual − corrected poll (pp)');ax.legend()
    fig.tight_layout();fig.savefig(out/'error_dependence.png',dpi=140);plt.close(fig)
    cols=['scenario','prior_model','model','n','correct','mae_pp','marginal_nll','coverage70','coverage95']
    text='# Polling update review — frozen priors\n\n'
    text+='The three prior recipes, their saved means/scaled covariance, polling aggregates, bias and fitted error covariance are fixed. Only total likelihood variance is multiplied by1,2or4 (SD by1,√2or2). This changes both mean weights and uncertainty; it is not merely widening reported intervals. No new data or model promotion. Polls remain frozen September17,2026.\n\n'
    text+='## Findings and decision\n\nKeep the existing reference and prior challengers. Doubling likelihood variance improves interval coverage but slightly worsens margin MAE; fourfold inflation is generally too broad. The chronological selector does not consistently improve predictive density or calls. Thus this is a calibration tradeoff, not a demonstrated new best model.\n\n'
    text+='On the same polled cases, the original model shrinks median prior SD to48.8% at the September-matched horizon and33.4% at October31. Prior and corrected-poll errors have descriptive correlations0.31/0.53 (0.31/0.49 after within-cycle centering). Both often miss in the same direction. This motivates checking dependence/shared error and fitted covariance uncertainty. It does not prove conditional independence is wrong: forecasts share outcomes, states repeat and only five recent cycles are available. No p-values or causal conclusions are assigned.\n\n'
    text+='## Evaluation contract\n\nMargins and MAE are D−R percentage points; positive signed error means actual results were more Democratic. MAE and marginal negative log density average cycles equally; calls and interval coverage pool contests. Lower MAE/NLL/Brier is better; interval coverage should match its nominal rate. This is marginal state calibration, not calibration of the joint Senate-seat distribution.\n\nR_selected chooses from1/2/4 using mean marginal negative log density in the last three saved earlier forecast cycles, equally weighted. Every saved validation forecast was constructed using only its earlier labels. It falls back to1 in2012/2014/2016 and first tunes in2018. This separate likelihood selection uses a marginal scoring objective; earlier prior-strength fitting used joint scores. Historical cycles have been repeatedly explored, so these are exploratory comparisons, not a new untouched test set.\n\n'
    for period in ['recent_2016_2024','tuned_2018_2024','all_2012_2024']:
        text+='## '+period+'\n\n'+cal[cal.period.eq(period)&cal.group.eq('all')][cols].round(4).to_markdown(index=False)+'\n\n'
    text+='## Same polled cases: where error and uncertainty change\n\nThe raw-poll standardized diagnostic reuses the corrected likelihood SD only as a scale comparison; it is not a separately fitted raw-poll probability forecast. No-poll states are excluded here and reported below.\n\n'+pd.read_parquet(out/'polled_stage_diagnostics.parquet').query('prior_model=="control_state"').round(4).to_markdown(index=False)+'\n\n'
    text+='## Dependence diagnostics\n\n'+dependence.round(4).to_markdown(index=False)+'\n\n'+cycle_bias.query('prior_model=="control_state"').round(3).to_markdown(index=False)+'\n\n'
    text+='## Reference-prior subgroups\n\n'+cal.query('period=="recent_2016_2024" and prior_model=="control_state" and group!="all"')[['scenario','group','model','n','correct','mae_pp','coverage95']].round(4).to_markdown(index=False)+'\n\n'
    text+='## October2024 state decomposition\n\nPosterior = prior + own-poll contribution + other-poll contributions. These contributions use the full gain matrix; they are signed, not convex mixture weights. Bias is subtracted from raw polls. ND and FL show polls already missing Republican strength, with the cross-state contribution adding to that miss; WV also has a stale/candidate-sensitive prior. This decomposition alone does not establish a source-data defect or a causal explanation.\n\n'+misses[['geography','actual_pp','prior_pp','q_pp','bias_pp','corrected_poll_pp','own_poll_shift_pp','other_poll_shift_pp','posterior_pp','posterior_sd_pp','error_pp']].round(3).to_markdown(index=False)+'\n\n'
    text+='## Scale choices\n\n'+folds.query('model=="R_selected"')[['scenario','cycle','prior_model','variance_scale','validation_cycles','tuning_status']].to_markdown(index=False)+'\n\n'
    text+='## Current full Senate scenarios\n\nReference remains49D/51R by state calls, expected48.48D and70% D range47–50. The selected-scale experiment is48D/52R, expected47.83D and70% D range46–50; it is not promoted. D includes Democratic-caucusing independents. Existing roster, unmodeled-seat completions and scalar ballot/runoff assumptions remain. No future October2026 forecast is invented.\n\n'+seats.query('cycle==2026')[['prior_model','model','variance_scale','point_D','point_R','expected_D_exact','D_lo70','D_hi70','D_lo95','D_hi95']].round(3).to_markdown(index=False)+'\n\n'
    text+='## Next directions, in order\n\n1. Polling evidence and common errors: separate fresh sampling noise from persistent pollster/state/cycle errors; audit effective firm mass and shared evidence. Avoid fitting a free state-by-state dependence matrix from five cycles.\n2. Time to election: test poll-age/election-day drift uncertainty, then decay, using matched historical horizons. The current comparison only rescales the existing aggregate likelihood.\n3. Probability uncertainty: integrate covariance/bias/hyperparameter uncertainty or try a tightly controlled heavy-tail residual model, holding the mean recipe fixed. Validate probabilities and joint seat ranges as well as calls.\n4. Context and surprises: reintroduce economic momentum/approval as a small separate correction; test disruption flags as possible variance/tail predictors. Few cycles mean strong pooling and one experiment at a time.\n5. Election structure: candidate/open-seat/special-election effects, exceptional ballots and sparse-history withholding validation. Preserve explicit chamber completion assumptions.\n\nThe next focused step should be1. Priors are sufficiently developed for this stage, with the reference plus two named challengers retained. Candidate context and sparse-history uncertainty remain limitations rather than reasons for another broad prior search. Use a frozen evaluation protocol and prospective2026 scoring to limit repeated historical selection.\n'
    (out/'POLLING_UPDATE_REVIEW_RESULTS.md').write_text(text)
    (lab/'POLLING_UPDATE_REVIEW_RESULTS.md').write_text(text)
    (out/'recipe'/Path(__file__).name).write_bytes(Path(__file__).read_bytes())
    v1.manifest(out)
    v1.json_write(out.parent/'latest.json',dict(artifact=out.name,manifest_sha256=v1.sha(out/'manifest.json')))
    return out


if __name__ == '__main__':
    build(Path(__file__).resolve().parents[1])
