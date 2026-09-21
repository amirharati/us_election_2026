"""Chronological interval-score selection and controlled cross-state diagnostics.

Uses immutable forecasts from the df/prior review; no poll/data refresh.
"""
from pathlib import Path
from datetime import datetime, timezone
import json
import numpy as np
import pandas as pd
from scipy.special import ndtr
from scipy.optimize import brentq
import simple_bayesian_polling as v1
import student_polling_likelihood as student
import national_tails_waves as chamber
import df_prior_review as previous

SOURCE = '20260919T214629.957686Z'
LEVELS = (50, 70, 80, 95)
FAMILIES = {'gaussian': ['reference', 'reference_K2', 'reference_K4'],
            'student': ['df_selected_g2', 'df_selected_g2_K2', 'df_selected_g2_K4']}
DIAGNOSTICS = ('no_error_links', 'no_movement_links', 'diagonal_both')
CONFIG = dict(levels=LEVELS, validation_cycles=3, draws=30000,
              seed=197139, as_of='2026-09-17', prior_multipliers=[1, 2, 4],
              diagnostic_K_multiplier=2, diagnostic_df='frozen earlier-cycle selector')


def interval_score(y, lo, hi, alpha):
    """Central (1-alpha) interval score in the same units as y; lower is better."""
    if not 0 < alpha < 1:
        raise ValueError('alpha must lie strictly between zero and one')
    y, lo, hi = np.broadcast_arrays(np.asarray(y, float), lo, hi)
    if np.any(lo > hi):
        raise ValueError('Reversed interval')
    return hi-lo + 2/alpha*np.maximum(lo-y, 0) + 2/alpha*np.maximum(y-hi, 0)


def score_rows(p):
    p = p.copy(); y = 100*p.actual
    p['absolute_error_pp'] = abs(p.prediction_pp-y)
    p['correct'] = np.where(y.notna(), (p.prediction_pp > 0) == (y > 0), np.nan)
    p['brier'] = np.where(y.notna(), (p.p_dem-(y > 0))**2, np.nan)
    p['wis_pp'] = .5*abs(y-p.median_pp)
    p['wis_width_pp'] = 0.
    p['wis_miss_pp'] = 0.
    for level in LEVELS:
        alpha = 1-level/100
        lo, hi = p[f'lo{level}_pp'], p[f'hi{level}_pp']
        width = hi-lo
        score = interval_score(y, lo, hi, alpha)
        p[f'width{level}_pp'] = width
        p[f'coverage{level}'] = np.where(y.notna(), y.between(lo, hi), np.nan)
        p[f'interval_score{level}_pp'] = score
        p['wis_pp'] += alpha/2*score
        p['wis_width_pp'] += alpha/2*width
        p['wis_miss_pp'] += alpha/2*(score-width)
    for name in ['wis_pp', 'wis_width_pp', 'wis_miss_pp']:
        p[name] /= len(LEVELS)+.5
    return p


def median(d):
    means = d['means']; sd = np.sqrt(np.diagonal(d['covs'], axis1=1, axis2=2))
    return np.array([brentq(lambda x: d['weights']@ndtr((x-means[:,j])/sd[:,j])-.5,
                           (means[:,j]-12*sd[:,j]).min(),
                           (means[:,j]+12*sd[:,j]).max()) for j in range(len(d['mean']))])


def choose(scores, cycle, models):
    """Only earlier out-of-sample cycle scores; ties retain simpler K."""
    q = scores[scores.cycle.lt(cycle) & scores.model.isin(models)]
    years = sorted(q.cycle.unique())[-3:]
    if len(years) < 3:
        return models[0], years, 'early_fixed_fallback'
    q = q[q.cycle.isin(years)]
    if len(q) != 3*len(models) or q.duplicated(['cycle', 'model']).any():
        raise ValueError('Incomplete past validation grid')
    values = q.groupby('model').wis_pp.mean()
    if not np.isfinite(values).all():
        raise ValueError('Nonfinite validation score')
    return min(models, key=lambda m: (values[m], models.index(m))), years, 'last_three_past_cycles'


def transform(k, poll, g, variant):
    """Remove links while preserving K, B, and total systematic T diagonals."""
    if variant not in DIAGNOSTICS:
        raise ValueError('Unknown diagnostic')
    kk = k.copy(); pp = {name: np.array(value, copy=True) for name, value in poll.items()}
    if variant in ('no_movement_links', 'diagonal_both'):
        kk = np.diag(np.diag(kk))
    if variant in ('no_error_links', 'diagonal_both'):
        pp['covariance'] = np.diag(np.diag(pp['covariance'])+g*g)
        pp['bias_covariance'] = np.diag(np.diag(pp['bias_covariance']))
        g = 0.
    return kk, pp, g


def seat_scores(row, frequency):
    """Discrete CRPS and WIS from the saved JOINT seat distribution."""
    p = np.asarray(frequency, float); p /= p.sum(); cdf = p.cumsum()
    result = dict(row)
    def quantile(prob):
        return int(min(np.searchsorted(cdf, prob), len(p)-1))
    result['D_median'] = quantile(.5)
    y = result['actual_D'] if pd.notna(result['actual_D']) else np.nan
    result['actual_D'] = y
    result['seat_wis'] = .5*abs(y-result['D_median']) if pd.notna(y) else np.nan
    for level in LEVELS:
        alpha = 1-level/100; lo = quantile(alpha/2); hi = quantile(1-alpha/2)
        result[f'D_lo{level}'] = lo; result[f'D_hi{level}'] = hi
        result[f'width{level}'] = hi-lo
        result[f'coverage{level}'] = float(lo <= y <= hi) if pd.notna(y) else np.nan
        result['seat_wis'] += alpha/2*float(interval_score(y, lo, hi, alpha))
    result['seat_wis'] /= len(LEVELS)+.5
    result['seat_crps'] = float(np.sum((cdf[:-1]-(np.arange(len(p)-1) >= y))**2)) if pd.notna(y) else np.nan
    result['expected_seat_error'] = abs(result['expected_D_exact']-y)
    return result


def summarize_scores(p):
    rows = []
    for period, first in [('recent_2016_2024', 2016), ('tuned_2018_2024', 2018), ('all_2012_2024', 2012)]:
        for (sc, model), q0 in p[p.cycle.between(first, 2024)].groupby(['scenario', 'model']):
            for group, mask in [('all', np.ones(len(q0), bool)),
                                ('competitive', q0.history_selection_10pp.eq('competitive')),
                                ('polled', q0.q_pp.notna()), ('no_polls', q0.q_pp.isna())]:
                q = q0[mask]
                if not len(q): continue
                averaged = q.groupby('cycle')[['wis_pp', 'absolute_error_pp', 'brier',
                    'wis_width_pp', 'wis_miss_pp', 'width70_pp', 'width95_pp']].mean().mean()
                rows.append(dict(period=period, scenario=sc, model=model, group=group,
                    n=len(q), cycles=q.cycle.nunique(), correct=int(q.correct.sum()),
                    accuracy=float(q.correct.mean()), **averaged.to_dict(),
                    **{f'coverage{x}': float(q[f'coverage{x}'].mean()) for x in LEVELS}))
    return pd.DataFrame(rows)


def build(lab):
    lab = Path(lab).resolve(); source = lab/'reports/df_prior_review'/SOURCE
    source_sha = v1.verify(source); s = json.loads((source/'settings.json').read_text())
    prior = Path(s['prior_source']); upstream = Path(s['upstream'])
    old = pd.read_parquet(prior/'predictions.parquet')
    sf = pd.read_parquet(source/'folds.parquet')
    cached = pd.concat([pd.read_parquet(source/'predictions.parquet'),
                        pd.read_parquet(source/'prior_ablations.parquet')], ignore_index=True)
    cached_seats = pd.concat([pd.read_parquet(source/'seats.parquet'),
                             pd.read_parquet(source/'prior_ablation_seats.parquet')], ignore_index=True)
    saved_folds = pd.concat([sf, pd.read_parquet(source/'prior_ablation_folds.parquet')], ignore_index=True)
    roster = pd.read_parquet(source/'full_seat_ledger.parquet')
    out = lab/'reports/coverage_balance'/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')
    out.mkdir(parents=True); (out/'forecasts').mkdir(); (out/'recipe').mkdir()
    print('OUTPUT', out, flush=True)
    settings = dict(config=CONFIG, source=str(source), source_sha256=source_sha,
        prior_source=str(prior), prior_source_sha256=v1.verify(prior),
        upstream=str(upstream), upstream_sha256=v1.verify(upstream), promotion=False, polling_refreshed=False,
        old_notebook_hashes={p.name:v1.sha(p) for p in lab.glob('*.ipynb') if p.name != 'COVERAGE_BALANCE.ipynb'})
    v1.json_write(out/'settings.json', settings)
    all_predictions=[]; all_seats=[]; all_folds=[]; numerical=[]; mi=[]; checks=[]
    for (sc, year), folds in sf.groupby(['scenario', 'cycle'], sort=True):
        row = folds.iloc[0]
        test = old[old.scenario.eq(sc)&old.cycle.eq(year)&old.model.eq('control_state')].sort_values('target_id').reset_index(drop=True)
        saved = np.load(prior/row.source_forecast); k = saved['prior_covariance']
        assert np.array_equal(saved['target_ids'], test.target_id.to_numpy(str))
        poll = dict(np.load(prior/row.source_poll)); sr = folds[folds.model.eq('df_selected_g2')].iloc[0]
        bank = {}
        configurations = [(m, mult, base, None) for base, models in FAMILIES.items() for m, mult in zip(models,[1,2,4])]
        configurations += [('common2', 1, 'common2', None)]
        configurations += [('student_K2_'+v, 2, 'student', v) for v in DIAGNOSTICS]
        rng = np.random.default_rng(CONFIG['seed']+int(year)+10000*(sc=='oct31'))
        z = rng.standard_normal((CONFIG['draws'], len(test))); u = rng.random(CONFIG['draws'])
        for model, mult, family, variant in configurations:
            df, g = (sr.df, sr.national_sd) if family == 'student' else (0, 2. if family == 'common2' else 0.)
            kk, pp = mult*k, poll
            if variant: kk, pp, g = transform(kk, poll, g, variant)
            d = student.fit(test, kk, pp, df, g)
            pred = student.summarize(test, d).assign(model=model, median_pp=median(d))
            pred = score_rows(pred); bank[model] = (d, pred, kk, pp, g)
            if not variant:
                q = cached[cached.scenario.eq(sc)&cached.cycle.eq(year)&cached.model.eq(model)].sort_values('target_id')
                cols = ['prediction_pp','p_dem','posterior_sd_pp']+[f'{side}{level}_pp' for level in LEVELS for side in ['lo','hi']]
                checks.append(np.array_equal(q.target_id.to_numpy(),pred.target_id.to_numpy()) and np.allclose(q[cols],pred[cols],atol=1e-8))
                ss = cached_seats[cached_seats.scenario.eq(sc)&cached_seats.cycle.eq(year)&cached_seats.model.eq(model)].iloc[0].to_dict()
                ff = saved_folds[saved_folds.scenario.eq(sc)&saved_folds.cycle.eq(year)&saved_folds.model.eq(model)].iloc[0]
                frequency = np.load(source/ff.forecast_path)['seat_count_frequency']
            else:
                rr = roster[roster.scenario.eq(sc)&roster.cycle.eq(year)]
                ss, counts = chamber.seat_summary(rr,test,pred,student.sample(d,z,u))
                ss.update(scenario=sc,cycle=year,model=model)
                frequency = np.bincount(counts,minlength=101)
                high = student.fit(test,kk,pp,df,g,nodes=513)
                numerical.append(dict(scenario=sc,cycle=year,model=model,
                    **previous.integration_check(test,d,high)))
            all_predictions.append(pred); all_seats.append(seat_scores(ss,frequency))
            path=f'forecasts/{sc}_{year}_{model}.npz'
            np.savez_compressed(out/path,target_ids=test.target_id.to_numpy(str),mean=d['mean'],
                covariance=d['covariance'],prior_covariance=kk,weights=d['weights'],scales=d['scales'],
                seat_count_frequency=frequency)
            all_folds.append(dict(scenario=sc,cycle=year,model=model,K_multiplier=mult,df=df,
                g=g,variant=variant or 'full',scale_mean=d['scale_mean'],forecast_path=path,
                source_forecast=row.source_forecast,source_poll=row.source_poll,training_max_cycle=row.training_max_cycle))
        if year == 2026:
            for model,(d,pred,kk,pp,g) in bank.items():
                idx = int(np.flatnonzero(test.geography.eq('MI'))[0]); obs=np.flatnonzero(test.q_pp.notna())
                so=np.array([v1.STATES.index(x) for x in test.geography.iloc[obs]])
                values=test.q_pp.to_numpy()[obs]-pp['bias_mean'][so]; mu=100*test.prior.to_numpy()
                fixed=pp['bias_covariance'][np.ix_(so,so)]+np.diag(16/test.firm_mass.to_numpy()[obs])
                t=pp['covariance'][np.ix_(so,so)]+g*g*np.ones((len(obs),len(obs)))
                gain=sum(w*np.linalg.solve(kk[np.ix_(obs,obs)]+fixed+s*t,kk[obs,:]).T for w,s in zip(d['weights'],d['scales']) if w>1e-18)
                contributions=gain[idx]*(values-mu[obs])
                np.testing.assert_allclose(mu[idx]+contributions.sum(),d['mean'][idx],atol=1e-9)
                for j,other in enumerate(obs):
                    mi.append(dict(model=model,state=test.geography.iloc[other],gain=gain[idx,j],innovation_pp=values[j]-mu[other],contribution_pp=contributions[j],mi_prior_pp=mu[idx],mi_posterior_pp=d['mean'][idx]))
            for mult in [1,2,4]:
                idx=int(np.flatnonzero(test.geography.eq('MI'))[0]); one=test.iloc[[idx]].copy()
                d=student.fit(one,k[np.ix_([idx],[idx])]*mult,poll,sr.df,sr.national_sd)
                pred=student.summarize(one,d).assign(model=f'MI_own_poll_only_K{mult}',median_pp=median(d))
                pred.to_parquet(out/f'mi_own_only_K{mult}.parquet',index=False)
        print(sc,year,'scored',len(configurations),'models',flush=True)
    p=pd.concat(all_predictions,ignore_index=True); seats=pd.DataFrame(all_seats); folds=pd.DataFrame(all_folds)
    cycle=p[p.actual.notna()].groupby(['scenario','cycle','model'],as_index=False).agg(
        wis_pp=('wis_pp','mean'),mae_pp=('absolute_error_pp','mean'),brier=('brier','mean'),n=('target_id','size'))
    trace=[]; selected=[]; selected_seats=[]
    for sc,group in p.groupby('scenario'):
        for year in sorted(group.cycle.unique()):
            for family,models in FAMILIES.items():
                chosen,years,status=choose(cycle[cycle.scenario.eq(sc)],year,models)
                name=family+'_wis_selected'
                selected.append(group[group.cycle.eq(year)&group.model.eq(chosen)].assign(model=name,selected_model=chosen))
                selected_seats.append(seats[seats.scenario.eq(sc)&seats.cycle.eq(year)&seats.model.eq(chosen)].assign(model=name,selected_model=chosen))
                for candidate in models:
                    hist=cycle[cycle.scenario.eq(sc)&cycle.cycle.isin(years)&cycle.model.eq(candidate)]
                    trace.append(dict(scenario=sc,forecast_cycle=year,selector=name,selected_model=chosen,candidate=candidate,
                        validation_cycles=','.join(map(str,years)),validation_max_cycle=max(years) if years else np.nan,
                        mean_validation_wis=hist.wis_pp.mean(),status=status))
    p=pd.concat([p,*selected],ignore_index=True); seats=pd.concat([seats,*selected_seats],ignore_index=True)
    summary=summarize_scores(p); chamber_rows=[]
    for period,first in [('recent_2016_2024',2016),('tuned_2018_2024',2018),('all_2012_2024',2012)]:
        for (sc,model),q in seats[seats.cycle.between(first,2024)].groupby(['scenario','model']):
            chamber_rows.append(dict(period=period,scenario=sc,model=model,cycles=len(q),
                **q[['seat_wis','seat_crps','expected_seat_error','coverage70','coverage95','width70','width95']].mean().to_dict()))
    tables=dict(predictions=p,seats=seats,folds=folds,cycle_scores=cycle,summary=summary,
                chamber_summary=pd.DataFrame(chamber_rows),tuning=pd.DataFrame(trace),
                mi_contributions=pd.DataFrame(mi),integration_checks=pd.DataFrame(numerical))
    for name,table in tables.items():table.to_parquet(out/(name+'.parquet'),index=False)
    v1.json_write(out/'reproduction_checks.json',dict(passed=all(checks),comparisons=len(checks)))
    for path in (lab/'scripts').glob('*.py'):
        (out/'recipe'/path.name).write_bytes(path.read_bytes())
    (out/'COVERAGE_BALANCE.md').write_bytes((lab/'COVERAGE_BALANCE.md').read_bytes())
    v1.manifest(out); audit(out,lab); report(out,lab)
    v1.json_write(out.parent/'latest.json',dict(artifact=out.name,manifest_sha256=v1.sha(out/'manifest.json')))
    return out


def audit(out,lab):
    out,lab=Path(out),Path(lab);v1.verify(out);s=json.loads((out/'settings.json').read_text())
    p=pd.read_parquet(out/'predictions.parquet');t=pd.read_parquet(out/'tuning.parquet');f=pd.read_parquet(out/'folds.parquet')
    seats=pd.read_parquet(out/'seats.parquet');cycle=pd.read_parquet(out/'cycle_scores.parquet');integ=pd.read_parquet(out/'integration_checks.parquet')
    y=100*p.actual.to_numpy();pinball=np.zeros(len(p));probs=[.5];quantiles=[p.median_pp.to_numpy()]
    for level in LEVELS:
        probs += [(1-level/100)/2,(1+level/100)/2]
        quantiles += [p[f'lo{level}_pp'].to_numpy(),p[f'hi{level}_pp'].to_numpy()]
    for prob,q in zip(probs,quantiles):
        e=y-q;pinball+=2*np.maximum(prob*e,(prob-1)*e)/len(probs)
    c={name+'_unchanged':v1.verify(s[name])==s[name+'_sha256'] for name in ['source','prior_source','upstream']}
    c.update(old_notebooks_unchanged=all(v1.sha(lab/n)==h for n,h in s['old_notebook_hashes'].items()),
        cached_forecasts_reproduced=json.loads((out/'reproduction_checks.json').read_text())['passed'],
        past_only_training=bool(f.training_max_cycle.lt(f.cycle).all()),past_only_selection=bool((t.validation_max_cycle.isna()|t.validation_max_cycle.lt(t.forecast_cycle)).all()),
        wis_matches_quantile_score=bool(np.allclose(pinball,p.wis_pp,equal_nan=True,atol=1e-10)),
        no_2026_labels_or_errors=bool(p[p.cycle.eq(2026)][['actual','wis_pp','brier','correct']].isna().all().all()),
        no_2026_seat_scores=bool(seats[seats.cycle.eq(2026)][['actual_D','seat_wis','seat_crps']].isna().all().all()),
        unique_forecasts=not p.duplicated(['scenario','model','target_id']).any(),
        same_target_sets=all(q.groupby('model').target_id.apply(frozenset).nunique()==1 for _,q in p.groupby(['scenario','cycle'])),
        finite_forecasts=bool(np.isfinite(p[['prediction_pp','p_dem','median_pp','lo95_pp','hi95_pp']]).all().all()),
        integration_converged=bool(integ.max_mean_difference_pp.lt(1e-6).all()&integ.max_probability_difference.lt(1e-7).all()&integ.relative_covariance_difference.lt(1e-6).all()))
    ok=[];seatok=[];diag=[]
    for r in t.drop_duplicates(['scenario','forecast_cycle','selector']).itertuples():
        chosen,years,status=choose(cycle[cycle.scenario.eq(r.scenario)],r.forecast_cycle,FAMILIES[r.selector.split('_')[0]])
        q=p[p.scenario.eq(r.scenario)&p.cycle.eq(r.forecast_cycle)]
        a=q[q.model.eq(r.selector)].sort_values('target_id');b=q[q.model.eq(chosen)].sort_values('target_id')
        ok.append(chosen==r.selected_model and status==r.status and ','.join(map(str,years))==r.validation_cycles and np.array_equal(a.target_id,b.target_id) and np.allclose(a.wis_pp,b.wis_pp,equal_nan=True) and np.allclose(a.prediction_pp,b.prediction_pp))
    for r in f.itertuples():
        z=np.load(out/r.forecast_path);q=p[p.scenario.eq(r.scenario)&p.cycle.eq(r.cycle)&p.model.eq(r.model)].sort_values('target_id')
        ss=seats[seats.scenario.eq(r.scenario)&seats.cycle.eq(r.cycle)&seats.model.eq(r.model)].iloc[0]
        seatok.append(z['seat_count_frequency'].sum()==CONFIG['draws'] and abs(ss.expected_D_exact-ss.fixed_D-q.p_dem.sum())<1e-9)
        if r.variant!='full':
            baseline=np.load(out/f'forecasts/{r.scenario}_{r.cycle}_df_selected_g2_K2.npz')
            diag.append(np.allclose(np.diag(z['prior_covariance']),np.diag(baseline['prior_covariance'])))
    c.update(selectors_reconstructed=all(ok),joint_seat_accounting=all(seatok),diagnostic_prior_variances_preserved=all(diag))
    result=dict(passed=all(c.values()),checks=c,forecast_rows=len(p),integration_comparisons=len(integ))
    v1.json_write(out/'audit.json',result)
    if not result['passed']:raise AssertionError([name for name,value in c.items() if not value])
    v1.manifest(out);return result


def report(out,lab):
    out,lab=Path(out),Path(lab);summary=pd.read_parquet(out/'summary.parquet');seats=pd.read_parquet(out/'seats.parquet');cs=pd.read_parquet(out/'chamber_summary.parquet');p=pd.read_parquet(out/'predictions.parquet')
    trace=pd.read_parquet(out/'tuning.parquet');mi=pd.read_parquet(out/'mi_contributions.parquet')
    current=p[p.cycle.eq(2026)&p.geography.eq('MI')][['model','prediction_pp','p_dem','lo70_pp','hi70_pp']]
    own=pd.concat([pd.read_parquet(out/f'mi_own_only_K{k}.parquet') for k in [1,2,4]])
    current=pd.concat([current,own[current.columns]],ignore_index=True);current.to_parquet(out/'mi_comparison.parquet',index=False)
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,axes=plt.subplots(1,2,figsize=(11,4.5))
    for ax,sc in zip(axes,['matched_live','oct31']):
        q=summary[summary.period.eq('recent_2016_2024')&summary.group.eq('all')&summary.scenario.eq(sc)].set_index('model')
        for family,models in FAMILIES.items():
            for model in models:
                ax.plot([50,70,80,95],[100*q.loc[model,f'coverage{x}'] for x in LEVELS],marker='o',label=model.replace('df_selected_g2','Student').replace('reference','Gaussian'))
        ax.plot([50,95],[50,95],'k--');ax.set(title=sc,xlabel='Nominal interval (%)',ylabel='Observed state coverage (%)');ax.legend(fontsize=7)
    fig.tight_layout();fig.savefig(out/'coverage.png',dpi=145);plt.close(fig)
    fig,ax=plt.subplots(figsize=(10,5))
    q=current[~current.model.str.contains('wis_selected|reference|common2')].iloc[::-1]
    yy=np.arange(len(q));ax.errorbar(q.prediction_pp,yy,xerr=[q.prediction_pp-q.lo70_pp,q.hi70_pp-q.prediction_pp],fmt='o',capsize=3)
    ax.set_yticks(yy,q.model);ax.axvline(0,color='black',linestyle='--');ax.set(xlabel='Michigan D−R margin (pp); 70% intervals',title='Current Michigan: covariance diagnostics and own-poll-only refits')
    fig.tight_layout();fig.savefig(out/'michigan.png',dpi=145);plt.close(fig)
    text='# Coverage balance and cross-state review\n\nFrozen September17 inputs. All forecasts use only earlier results; no promotion. WIS uses median and central50/70/80/95 intervals, lower is better. Scores/MAE/Brier average cycles equally; coverage and calls pool contests. Brier differs slightly from previous pooled-state tables because of this explicit cycle weighting.\n\n'
    text+='## Main findings\n\nAcross2016–2024, weakening Student K1→K2 improves95%coverage90.7→94.3% in September and90.0→92.1% in October, but state WIS worsens4.118→4.359 and2.981→3.106. Average95%width increases35.54→44.52pp earlier and25.53→29.38pp late. Some improved coverage is purchased with excessive width under this score. K4 worsens state WIS further. September competitive-state WIS slightly improves3.635→3.615 underK2, but late competitive WIS worsens2.598→2.623.\n\nThe rolling K selectors retainK1 for every completed historical cycle. For2026 both families selectK2 using2020/22/24: Student WIS4.1437→4.1167 and Gaussian4.0977→4.0686, shallow improvements below1%. Thus the chronological selected-model historical rows equalK1; they do not demonstrate a historical adaptive-K improvement. Current StudentK2 gives50D/50R point seats,49.382expectedD,70%47–52,95%45–54. GaussianK2 gives50D/50R,49.177expectedD,70%47–51,95%45–54.\n\nThe chamber objective differs: StudentK2 improves recent late seat CRPS0.957→0.856 and expected-seat MAE1.418→1.264. K4 improves these further to0.789 and1.185. Therefore state-marginal WIS does not choose the best aggregate seat distribution in this small sample. Only five recent elections support these chamber comparisons.\n\nMichigan cross-state influence is real within the model. AtK2, own-poll-only refitD+3.097→fullD+0.562, a2.536pp Republican shift; Democratic probability68.6→54.6%. Removing error links givesD+1.502; removing historical movement links givesD+1.602; diagonalizing both givesD+3.033. Diagonal_both still shares the Student scale. AtK1 the full meanR+0.024 is effectively a tie and its mixture Democratic probability is50.24%, so describing it as confidently Republican would be wrong.\n\nRemoving error links is not a universal historical fix: versus fullK2, late state MAE5.198→5.508 and calls131→130, though chamber CRPS0.856→0.717 improves. Removing movement links yields late MAE5.149 and133calls, but state WIS worsens3.106→3.183 and chamber CRPS0.856→0.887. These mixed results support reviewing covariance estimation, not mechanically deleting all links. Retain the old reference and this moderate-K challenger; no automatic promotion.\n\n'
    cols=['scenario','model','n','correct','absolute_error_pp','wis_pp','brier','coverage70','coverage95','width95_pp']
    for period in ['recent_2016_2024','tuned_2018_2024','all_2012_2024']:
        text+='## '+period+'\n\n'+summary[summary.period.eq(period)&summary.group.eq('all')][cols].round(4).to_markdown(index=False)+'\n\n'
    text+='## Recent total-seat evaluation\n\nFive cycles; discrete intervals and fixed continuing/completion seats. CRPS evaluates the entire simulated seat distribution.\n\n'+cs[cs.period.eq('recent_2016_2024')].round(4).to_markdown(index=False)+'\n\n'
    text+='## Prior strength selection\n\n'+trace.drop_duplicates(['scenario','forecast_cycle','selector'])[['scenario','forecast_cycle','selector','selected_model','validation_cycles','status']].to_markdown(index=False)+'\n\n'
    text+='## Current full chamber\n\nPoint seats use posterior-mean signs; expected seats sum win probabilities.\n\n'+seats[seats.cycle.eq(2026)][['model','point_D','point_R','expected_D_exact','D_lo70','D_hi70','D_lo95','D_hi95']].round(3).to_markdown(index=False)+'\n\n'
    text+='## Michigan diagnostic\n\nThe three link-removal variants use K×2 and retain each state variance. Removing error links diagonalizes both systematic error (including national g²) and bias covariance. Removing movement links diagonalizes K. Student scale remains shared, so diagonal_both still learns scale from all states. MI_own_poll_only refits use only Michigan current polls and integrate its scale independently; all historical parameters and df remain fixed. Fitted gain decomposition is not a causal effect or a leave-one-state-out refit.\n\n'+current.round(4).to_markdown(index=False)+'\n\n'
    text+='## Current state margins\n\n'+p[p.cycle.eq(2026)].pivot(index='geography',columns='model',values='prediction_pp').round(3).to_markdown()+'\n\n'
    text+='## Limits\n\nK tuning uses last3 earlier held-out cycles. Student df remains the previously selected chronological value for each fold; no joint df/K grid is fitted. Cross-state variants are fixed diagnostics, not tuned winners. Removing either covariance type changes conditional gains and the posterior scale, so effects are not additive. Gaussian reference uses g0; Student uses g2; common2 is the matched g2 Gaussian control. State labels in the same cycle are correlated. Only five recent elections support chamber coverage; many exploratory comparisons have been made. No economy/approval inputs and no live refresh.\n'
    (lab/'COVERAGE_BALANCE_RESULTS.md').write_text(text);(out/'COVERAGE_BALANCE_RESULTS.md').write_text(text);v1.manifest(out)


if __name__ == '__main__':
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('--lab',type=Path,default=Path(__file__).resolve().parents[1]);args=parser.parse_args()
    build(args.lab)
