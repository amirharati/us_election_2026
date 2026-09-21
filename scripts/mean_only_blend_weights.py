"""Fixed 20/50/70% mean translations; retain each Bayesian joint covariance."""
from pathlib import Path
from datetime import datetime, timezone
import json
import shutil
import numpy as np
import pandas as pd
from model_labels import label_frame
from scipy.stats import norm
from calibrate_margin_uncertainty import sha, finalize
from plain_polling_blend import verify, BAYES_SOURCE
from mean_only_polling_blend import SOURCE, SEED, DRAWS, rescore, translate_draws

PREVIOUS = 'reports/mean_only_polling_blend/20260920T064738.332296Z'
VARIANTS = [('Bayesian', 'bayesian_pp', 0.)] + [
    (f'{label} {int(w*100)}%', col, w)
    for label, col in [('Plain', 'plain_pp'), ('Corrected', 'nonbayesian_pp')]
    for w in [.2, .5, .7]]
METRICS = ['absolute_error_pp', 'brier', 'coverage70', 'coverage95',
           'width70_pp', 'interval_score70_pp']


def blend_mean(bayesian, other, weight):
    if not np.isfinite(weight) or not 0 <= weight <= 1:
        raise ValueError('Weight must be finite and between zero and one')
    a, b = np.asarray(bayesian, float), np.asarray(other, float)
    if a.shape != b.shape or not np.isfinite(a).all() or not np.isfinite(b).all():
        raise ValueError('Finite aligned component means required')
    return (1-weight)*a + weight*b


def build(lab):
    lab = Path(lab).resolve()
    source, bayes, previous = lab/SOURCE, lab/BAYES_SOURCE, lab/PREVIOUS
    for p in [source, previous]: verify(p)
    notebooks = {p.name: sha(p) for p in lab.glob('*.ipynb')}
    working = sha(lab/'WORKING_MODEL.json')
    paths = [source/'manifest.json', previous/'manifest.json',
             bayes/'folds.parquet', bayes/'seats.parquet', bayes/'tuning.parquet']
    hashes = {str(p.relative_to(lab)): sha(p) for p in paths}
    paired = pd.read_parquet(source/'paired_inputs.parquet')
    assert not paired.duplicated(['scenario', 'cycle', 'target_id']).any()
    frames = []
    for name, col, weight in VARIANTS:
        f = paired.copy()
        f['model'], f['nonbayesian_weight'], f['component'] = name, weight, col
        f['margin_pp'] = blend_mean(f.bayesian_pp, f[col], weight)
        f['sigma_pp'] = f.posterior_sd_pp
        f = rescore(f)
        f['lo95_pp'] = f.margin_pp-norm.ppf(.975)*f.sigma_pp
        f['hi95_pp'] = f.margin_pp+norm.ppf(.975)*f.sigma_pp
        f['coverage95'] = ((f.actual_pp >= f.lo95_pp) & (f.actual_pp <= f.hi95_pp)).astype(float).where(f.actual_pp.notna())
        frames.append(f)
    predictions = pd.concat(frames, ignore_index=True)
    old = pd.read_parquet(previous/'predictions.parquet').query('model == "Mean-only blend"')
    chk = predictions.query('model == "Plain 50%"').merge(old, on=['scenario','cycle','target_id'], suffixes=('', '_old'), validate='one_to_one')
    for col in ['margin_pp','p_dem','sigma_pp','width70_pp']:
        assert np.allclose(chk[col], chk[col+'_old'])
    folds = pd.read_parquet(bayes/'folds.parquet').query('model == "repaired_both__selected"')
    reference = pd.read_parquet(bayes/'seats.parquet').query('model == "repaired_both__selected"')
    tuning = pd.read_parquet(bayes/'tuning.parquet').query('base_model == "repaired_both"')
    for r in tuning.itertuples():
        assert all(int(y) < r.cycle for y in str(r.validation_years).split(',') if y and y != 'nan')
    out = lab/'reports/mean_only_blend_weights'/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')
    (out/'forecasts').mkdir(parents=True)
    seats, distributions, checks = [], [], []
    for fold in folds.itertuples():
        path = bayes/fold.forecast_path
        hashes[str(path.relative_to(lab))] = sha(path)
        a = dict(np.load(path)); ids = a['target_ids'].astype(str)
        mu, cov = a['mean'], a['covariance']
        seed = SEED+fold.cycle+10000*(fold.scenario == 'oct31')
        draws = mu+np.random.default_rng(seed).standard_normal((DRAWS,len(ids)))@np.linalg.cholesky(cov).T
        ref = reference[reference.scenario.eq(fold.scenario)&reference.cycle.eq(fold.cycle)].iloc[0]
        fixed = int(ref.fixed_D)
        for name, _, weight in VARIANTS:
            f = predictions[predictions.scenario.eq(fold.scenario)&predictions.cycle.eq(fold.cycle)&predictions.model.eq(name)].set_index('target_id').loc[ids]
            assert np.allclose(f.bayesian_pp,mu)
            assert np.allclose(f.sigma_pp,np.sqrt(np.diag(cov)))
            new_mu = f.margin_pp.to_numpy()
            shifted = translate_draws(draws,mu,new_mu)
            assert np.allclose(shifted-new_mu,draws-mu,atol=1e-12)
            assert np.allclose(np.cov(shifted,rowvar=False),np.cov(draws,rowvar=False),atol=1e-10)
            counts = fixed+(shifted>0).sum(axis=1)
            freq = np.bincount(counts,minlength=101)
            if name == 'Bayesian': assert np.array_equal(freq,a['seat_count_frequency'])
            if name == 'Plain 50%':
                old_a = np.load(previous/'forecasts'/f'{fold.scenario}_{fold.cycle}.npz')
                assert np.array_equal(freq,old_a['seat_count_frequency'])
            lo,hi = np.quantile(counts,[.15,.85],method='inverted_cdf')
            point = fixed+int(f.margin_pp.gt(0).sum())
            expected = fixed+f.p_dem.sum()
            actual = ref.actual_D
            crps = np.nan if pd.isna(actual) else float(np.square(np.cumsum(freq/DRAWS)-(np.arange(101)>=actual)).sum())
            seats.append(dict(scenario=fold.scenario,cycle=int(fold.cycle),model=name,nonbayesian_weight=weight,
                point_D=point,point_R=100-point,expected_D=expected,expected_R=100-expected,
                p_D_control=float((counts>=51).mean()),D_lo70=int(lo),D_hi70=int(hi),
                actual_D=actual,expected_seat_error=abs(expected-actual),seat_crps=crps,
                fixed_D=fixed,unmodeled_contested=int(ref.unmodeled_contested)))
            distributions.extend(dict(scenario=fold.scenario,cycle=int(fold.cycle),model=name,D_seats=i,probability=float(v/DRAWS)) for i,v in enumerate(freq) if v)
            np.savez_compressed(out/'forecasts'/f'{fold.scenario}_{fold.cycle}_{name.replace(" ","_").replace("%","")}.npz',
                target_ids=ids,mean=new_mu,covariance=cov,bayesian_mean=mu,seed=seed,draws=DRAWS,seat_count_frequency=freq)
        checks.append(dict(scenario=fold.scenario,cycle=int(fold.cycle),baseline_reproduced=True,
                           plain_50_reproduced=True,all_seven_covariances_unchanged=True))
    seats = pd.DataFrame(seats)
    history = predictions[predictions.actual_pp.notna()]
    cycles = history.groupby(['scenario','cycle','model'])[METRICS].mean().reset_index()
    cycles = cycles.merge(history.groupby(['scenario','cycle','model']).agg(n=('target_id','size'),correct=('correct','sum')).reset_index())
    summary = []
    for start in [2012,2016]:
        for (sc,name),g in cycles[cycles.cycle.ge(start)].groupby(['scenario','model']):
            chamber = seats[seats.scenario.eq(sc)&seats.model.eq(name)&seats.cycle.between(start,2024)]
            summary.append(dict(first_cycle=start,scenario=sc,model=name,cycles=len(g),n=int(g.n.sum()),correct=int(g.correct.sum()),
                **g[METRICS].mean().to_dict(),expected_seat_mae=chamber.expected_seat_error.mean(),seat_crps=chamber.seat_crps.mean()))
    summary = pd.DataFrame(summary)
    groups = []
    for (sc,name),g in history[history.cycle.ge(2016)].groupby(['scenario','model']):
        for label,f in {'competitive':g[g.history_selection_10pp.eq('competitive')],
                        'not_selected':g[g.history_selection_10pp.eq('not_selected')],
                        'unknown_history':g[g.history_selection_10pp.eq('unknown_history')],
                        'polled':g[g.q_pp.notna()], 'no_polls':g[g.q_pp.isna()]}.items():
            if len(f): groups.append(dict(scenario=sc,model=name,group=label,n=len(f),correct=int(f.correct.sum()),
                                          **f.groupby('cycle')[METRICS].mean().mean().to_dict()))
    current = predictions[predictions.cycle.eq(2026)].copy()
    assert current.actual_pp.isna().all() and current.brier.isna().all()
    assert len(current) == 35*7
    current['State'] = current.geography+np.where(current.special,' (special)','')
    current['P(D) %'] = 100*current.p_dem
    tables = dict(predictions=predictions,cycle_scores=cycles,summary=summary,subgroups=pd.DataFrame(groups),
                  seats=seats,seat_distributions=pd.DataFrame(distributions),current=current,
                  current_margins=current.pivot(index='State',columns='model',values='margin_pp').reset_index(),
                  current_probabilities=current.pivot(index='State',columns='model',values='P(D) %').reset_index())
    for name,table in tables.items(): table.to_parquet(out/(name+'.parquet'),index=False)
    assert all(sha(lab/k)==v for k,v in hashes.items())
    assert all(sha(lab/k)==v for k,v in notebooks.items())
    assert sha(lab/'WORKING_MODEL.json')==working
    settings = dict(bayesian_model='repaired_both__selected',source=SOURCE,bayesian_source=BAYES_SOURCE,
        previous=PREVIOUS,data_as_of='2026-09-17',variants=VARIANTS,draws=DRAWS,seed=SEED,
        rule='mu_new=(1-w)*mu_Bayesian+w*mu_component; covariance_new=covariance_Bayesian',
        corrected_component='Retained bias benchmark: local/shared historical polling-error correction, last 5 calendar cycles / 8-year decay',
        plain_component='Saved recency/firm weighted polling; historical tuning and no-poll prior fallback retained',
        no_refresh=True,no_refit=True,no_weight_selection=True,no_promotion=True,
        sources=hashes,old_notebooks=notebooks,working_sha256=working)
    (out/'settings.json').write_text(json.dumps(settings,indent=2)+'\n')
    (out/'audit.json').write_text(json.dumps(dict(passed=True,folds=checks,old_notebooks_preserved=len(notebooks),
        historical_contests_per_horizon=198,recent_contests_per_horizon=140,current_contests=35),indent=2)+'\n')
    report = '''# Mean-only blend weights: plain versus corrected polling

Weight is the non-Bayesian share: 20%, 50%, or 70%. Each state mean is `(1-w)*Bayesian + w*component`. Translate all original joint draws by that state's mean change. Full Bayesian margin covariance, correlations, SDs and interval widths stay unchanged. State probabilities use Gaussian marginals; chamber odds retain correlated joint draws (30,000 paired simulations). Seat-count variance can change because winning is a nonlinear threshold. This is an empirical hybrid, not a newly derived Bayesian posterior.

The Bayesian reference is `repaired_both__selected`; Corrected means the retained `bias` non-Bayesian benchmark, not every feature variant previously explored. Plain retains its original historical selection/fallback; no-poll races use its prior fallback. Inputs are frozen September 17, 2026. These user-specified weights are not fitted or selected; component forecasts use their saved earlier-cycle training/tuning. All baseline and previous 50% plain simulations reproduce exactly. No refresh or model promotion.

Positive margins favor Democrats, in percentage points. P(D) is state win probability. Point seats count positive means; expected seats sum win probabilities plus continuing seats. Control requires 51D under the current ledger convention. Historical chamber totals include fixed completion of unmodeled contests; current independent-candidate proxy conventions remain. Repeated earlier architecture exploration makes this an exploratory historical comparison, not untouched validation.

## Recent history, 2016–2024

Each horizon contains 140 contests across five cycles. MAE, Brier and coverage average cycles equally; correct calls pool contests. Lower MAE/Brier/CRPS is better; target coverage is 70% or 95%. Matched-live is the saved September horizon; oct31 is October 31.

'''+label_frame(summary.query('first_cycle == 2016').round(4)).to_markdown(index=False)
    for title,table in [('Current total seats',seats[seats.cycle.eq(2026)]),('All historical cycles',cycles),
                        ('Historical chamber totals and actuals',seats[seats.cycle.lt(2026)]),
                        ('Subgroups, 2016–2024',tables['subgroups']),('Current state margins',tables['current_margins']),
                        ('Current state P(D), percent',tables['current_probabilities'])]:
        report += '\n\n## '+title+'\n\n'+label_frame(table.round(4)).to_markdown(index=False)
    (out/'RESULTS.md').write_text(report)
    shutil.copy2(__file__,out/Path(__file__).name)
    finalize(out)
    print('OUTPUT',out)
    print(summary.query('first_cycle == 2016').round(4).to_string(index=False))
    print(seats[seats.cycle.eq(2026)].round(4).to_string(index=False))
    return out


if __name__ == '__main__':
    build(Path(__file__).resolve().parents[1])
