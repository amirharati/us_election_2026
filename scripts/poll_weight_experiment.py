"""Controlled poll-weight sensitivity; frozen Gaussian priors/variance budgets.

Ratings use only the immediately previous cycle at the same horizon. A second
arm refits historical bias under each rule; it does not retune variances.
"""
from pathlib import Path
import json,hashlib
import numpy as np
import pandas as pd
from scipy.stats import norm
import election_lab as lab
from coverage_balance import score_rows,seat_scores
from simple_baselines import prepare_inputs

RULES={
 'Firm balanced (reference)':('firm',30.,0.),
 'Equal polls, 30d':('equal',30.,0.),
 'Respondent n, 30d':('n',30.,0.),
 'Firm balanced + within-firm n':('firm_n',30.,0.),
 'Firm + last-cycle rating mild':('firm',30.,.5),
 'Firm + last-cycle rating strong':('firm',30.,1.),
 'Equal polls, no decay':('equal',None,0.),
}
REFERENCE=next(iter(RULES))
CONFIG=dict(rules=RULES,rating_window_days=30,rating_shrink_contests=3.,rating_scale_pp=3.,
            rating_min_multiplier=.5,rating_max_multiplier=2.,missing_n_fallback=1000.,
            calibration=['Frozen bias','Refit bias'],variance='Frozen original P, B and 16/firm_mass; no respondent-count precision',
            prior='Frozen final Gaussian prior for each fold',promotion=False)


def last_cycle_ratings(targets,waves,year):
    """One equal-weight contribution per firm/contest, compared to contest peers."""
    previous=targets[targets.cycle.eq(year-2)&targets.actual.notna()]
    w=waves[waves.target_id.isin(previous.target_id)&waves.age_days.between(0,CONFIG['rating_window_days'])].copy()
    columns=['firm','contests','excess_mae_pp','reliability','source_cycle']
    if w.empty:return pd.DataFrame(columns=columns)
    if 'unknown' in w.firm.values:w=w[~w.firm.eq('unknown')].copy()
    w['weight']=np.exp2(-w.age_days/30);w['weighted_margin']=100*w.margin*w.weight
    a=w.groupby(['target_id','firm']).agg(total=('weight','sum'),weighted=('weighted_margin','sum')).reset_index()
    a['poll_pp']=a.weighted/a.total
    a=a.merge(previous[['target_id','actual']],on='target_id',validate='many_to_one')
    a['error_pp']=abs(a.poll_pp-100*a.actual)
    peers=a.groupby('target_id').firm.transform('size');a=a[peers.ge(2)].copy()
    a['excess']=a.error_pp-a.groupby('target_id').error_pp.transform('median')
    result=a.groupby('firm').agg(contests=('target_id','nunique'),excess_mae_pp=('excess','mean')).reset_index()
    result['reliability']=result.contests/(result.contests+CONFIG['rating_shrink_contests']);result['source_cycle']=year-2
    return result[columns]


def rating_multiplier(ratings,strength):
    if ratings.empty:return {}
    exponent=-strength*ratings.reliability*ratings.excess_mae_pp/CONFIG['rating_scale_pp']
    multiplier=np.exp(exponent.clip(np.log(.5),np.log(2.)))
    return dict(zip(ratings.firm,multiplier))


def aggregate(targets,waves,rule,ratings,fill_n):
    """Change mean weights only. Preserve baseline evidence mass for uncertainty."""
    mode,half_life,strength=RULES[rule];multipliers=rating_multiplier(ratings,strength)
    baseline=lab.gaussian.aggregate(targets,waves);groups=dict(tuple(waves.groupby('target_id')))
    rows=[];ledger=[]
    for r in baseline.itertuples():
        row=r._asdict();row.pop('Index',None);w=groups.get(r.target_id)
        if w is not None and len(w):
            w=w.copy();reported=pd.to_numeric(w.reported_n,errors='coerce')
            missing=~(np.isfinite(reported)&reported.gt(0));n=reported.mask(missing,fill_n)
            counts=w.groupby('firm').firm.transform('size')
            decay=np.ones(len(w)) if half_life is None else np.exp2(-w.age_days.to_numpy()/half_life)
            if mode=='firm':weight=decay/counts
            elif mode=='equal':weight=decay
            elif mode=='n':weight=decay*n
            elif mode=='firm_n':weight=decay*n/n.groupby(w.firm).transform('sum')
            else:raise ValueError(mode)
            multiplier=w.firm.map(multipliers).fillna(1.)
            weight=np.asarray(weight*multiplier,float);weight/=weight.sum()
            row['q_pp']=float(weight@(100*w.margin.to_numpy()))
            audit=w[['target_id','sample_key','firm','age_days','reported_n','margin']].copy()
            audit['normalized_weight']=weight;audit['rating_multiplier']=multiplier.to_numpy();audit['imputed_n']=missing.to_numpy();audit['n_used']=n.to_numpy()
            audit['n_affects_weight']=mode in {'n','firm_n'};audit['variant']=rule;ledger.append(audit)
        rows.append(row)
    return pd.DataFrame(rows),pd.concat(ledger,ignore_index=True) if ledger else pd.DataFrame()


def n_default(targets,waves,year):
    older=set(targets.loc[targets.cycle.lt(year),'target_id']);n=pd.to_numeric(waves.loc[waves.target_id.isin(older),'reported_n'],errors='coerce')
    n=n[np.isfinite(n)&n.gt(0)]
    return float(n.median()) if len(n) else CONFIG['missing_n_fallback']


def histories(targets,waves):
    agg=[];ratings=[];weights=[]
    for year,g in targets.groupby('cycle'):
        rating=last_cycle_ratings(targets,waves,int(year));ratings.append(rating.assign(cycle=year))
        fill=n_default(targets,waves,year);wg=waves[waves.target_id.isin(g.target_id)]
        for rule in RULES:
            a,w=aggregate(g,wg,rule,rating,fill);a['variant']=rule;a['cycle']=year;agg.append(a)
            if len(w):weights.append(w.assign(cycle=year,n_fallback=fill))
    return pd.concat(agg,ignore_index=True),pd.concat([r for r in ratings if len(r)],ignore_index=True),pd.concat(weights,ignore_index=True)


def refit_bias(sc,year,variant,aggregates,history):
    """Same variance budget, dates and relevance weights; only errors change."""
    saved=np.load(lab.ASSETS/'poll'/f'{sc}_{year}.npz')
    h=history[history.scenario.eq(sc)&history.cycle.lt(year)].copy()
    a=aggregates[aggregates.scenario.eq(sc)&aggregates.variant.eq(variant)][['target_id','q_pp']]
    h=h.drop(columns='q_pp').merge(a,on='target_id',validate='one_to_one')
    # Use precisely the originally eligible chronology; no new labels/contests.
    h=h[h.actual.notna()&h.prior_latest_cycle.notna()&h.prior_latest_cycle.lt(h.cycle)&h.q_pp.notna()&h.firm_mass.gt(0)]
    h['residual']=h.q_pp-100*h.actual
    values=h.pivot(index='cycle',columns='geography',values='residual').reindex(index=saved['years'],columns=lab.gaussian.STATES).to_numpy()
    assert np.array_equal(np.isfinite(values),np.isfinite(saved['training_values']))
    assert saved['years'].max()<year
    if variant==REFERENCE:np.testing.assert_allclose(values,saved['training_values'],atol=1e-10,equal_nan=True)
    result=lab.national.fixed_common(values,saved['training_noise'],saved['training_weights'],saved['budget'],0.,9.)
    if variant==REFERENCE:
        original=lab.load_poll(sc,year)
        np.testing.assert_allclose(result['bias_mean'],original['bias_mean'],atol=1e-10)
    return result


def predict(template,prior,aggregate_rows,poll,label):
    q=template.copy();a=aggregate_rows.set_index('target_id').loc[q.target_id]
    q['q_pp']=a.q_pp.to_numpy();obs=np.flatnonzero(q.q_pp.notna());ids=np.array([lab.gaussian.STATES.index(s) for s in q.geography]);oi=ids[obs]
    # Keep original confidence to avoid interpreting n or repeated firm polls as independent precision.
    np.testing.assert_allclose(a.firm_mass,q.firm_mass,atol=1e-10)
    R=poll['covariance'][np.ix_(oi,oi)]+poll['bias_covariance'][np.ix_(oi,oi)]+np.diag(16/q.firm_mass.to_numpy()[obs])
    y=q.q_pp.to_numpy()[obs]-poll['bias_mean'][oi]
    mean,cov,_=lab.gaussian.normal_update(prior['prior_mean'],prior['prior_covariance'],obs,y,R)
    p=q[['scenario','cycle','target_id','geography','special','actual','q_pp','firm_mass','history_selection_10pp']].copy()
    p['model']=label;p['prediction_pp']=mean;p['prediction']=mean/100;p['margin_pp']=mean;p['median_pp']=mean
    sd=np.sqrt(np.diag(cov));p['sigma_pp']=sd;p['posterior_sd_pp']=sd;p['p_dem']=norm.cdf(mean/sd)
    p['historical_bias_pp']=poll['bias_mean'][ids];p['corrected_poll_pp']=p.q_pp-p.historical_bias_pp
    for level in [50,70,80,95]:
        width=norm.ppf((1+level/100)/2)*sd;p[f'lo{level}_pp']=mean-width;p[f'hi{level}_pp']=mean+width
    p=score_rows(p);p['actual_pp']=100*p.actual
    return p,cov


def run(force=False):
    live=lab.latest_run('live');meta=json.loads((live/'run.json').read_text());snapshot=lab.dataset_for_run(meta)
    files=[lab.ROOT/'scripts/poll_weight_experiment.py',lab.ROOT/'scripts/simple_baselines.py',lab.ROOT/'scripts/simple_bayesian_polling.py',lab.ROOT/'scripts/simple_national_model.py',lab.ROOT/'scripts/bayesian_revision2.py',lab.ROOT/'election_lab.py',live/'manifest.json',snapshot/'manifest.json']
    files+=sorted((lab.ROOT/'scripts').glob('*.py'))
    files+=sorted(p for p in lab.ASSETS.rglob('*') if p.is_file())
    hashes={str(p.relative_to(lab.ROOT)):lab.sha(p) for p in files}
    key=hashlib.sha256(json.dumps(hashes,sort_keys=True).encode()).hexdigest();index=lab.ROOT/'cache/poll_weights'/f'{key}.json'
    if index.exists() and not force:
        info=json.loads(index.read_text());out=lab.ROOT/info['run']
        if lab.sha(out/'manifest.json')!=info['manifest_sha256']:raise ValueError('Cache mismatch')
        print('Verified poll-weight experiment cache',out.name,flush=True);return lab.verify_run(out)
    out=lab.new_run('poll_weights');history=pd.read_parquet(lab.ASSETS/'training/history.parquet');waves=pd.read_parquet(lab.ASSETS/'training/samples.parquet')
    aa=[];rr=[];ww=[]
    for sc,h in history.groupby('scenario'):
        a,r,w=histories(h,waves[waves.scenario.eq(sc)])
        old=a[a.variant.eq(REFERENCE)].set_index('target_id').loc[h.target_id]
        np.testing.assert_allclose(old.q_pp,h.q_pp,atol=1e-10,equal_nan=True);np.testing.assert_allclose(old.firm_mass,h.firm_mass,atol=1e-10)
        aa.append(a.assign(scenario=sc,evidence='frozen'));rr.append(r.assign(scenario=sc,evidence='frozen'));ww.append(w.assign(scenario=sc,evidence='frozen'))
    aggregates=pd.concat(aa,ignore_index=True)
    from load_final_dataset import open_dataset
    data=open_dataset(snapshot);targets,current_waves,_,_=prepare_inputs(data)
    targets=targets[targets.kind.eq('senate')&targets.cycle.eq(2026)].sort_values('target_id').reset_index(drop=True)
    current_waves=current_waves[current_waves.target_id.isin(targets.target_id)]
    previous=history[history.scenario.eq('matched_live')];previous_waves=waves[waves.scenario.eq('matched_live')]
    rating=last_cycle_ratings(previous,previous_waves,2026);rr.append(rating.assign(cycle=2026,scenario='matched_live',evidence='live'))
    live_agg=[]
    for rule in RULES:
        a,w=aggregate(targets,current_waves,rule,rating,n_default(previous,previous_waves,2026))
        live_agg.append(a.assign(variant=rule,cycle=2026,scenario='matched_live',evidence='live'))
        ww.append(w.assign(cycle=2026,scenario='matched_live',evidence='live'))
    live_agg=pd.concat(live_agg,ignore_index=True)
    folds=pd.read_parquet(lab.ASSETS/'main/folds.parquet');base=pd.read_parquet(lab.ASSETS/'main/predictions.parquet');refs=pd.read_parquet(lab.ASSETS/'main/seats.parquet')
    cases=[]
    for r in folds.itertuples():
        q=base[base.scenario.eq(r.scenario)&base.cycle.eq(r.cycle)].sort_values('target_id').reset_index(drop=True)
        cases.append(('frozen',r,q,dict(np.load(lab.ASSETS/'main'/r.forecast_path))))
    q=pd.read_parquet(live/'predictions.parquet').query('model=="Bayesian"').sort_values('target_id').reset_index(drop=True)
    r=next(r for r in folds.itertuples() if r.scenario=='matched_live' and r.cycle==2026)
    cases.append(('live',r,q,dict(np.load(live/'main_joint.npz'))))
    predictions=[];seats=[];checks=[];raw=[];biases=[];fit_cache={}
    for evidence,r,q,prior in cases:
        sc=r.scenario;year=int(r.cycle);ref=refs[refs.scenario.eq(sc)&refs.cycle.eq(year)].iloc[0]
        train_max=int(np.load(lab.ASSETS/'poll'/f'{sc}_{year}.npz')['years'].max());assert train_max<year
        pool=live_agg if evidence=='live' else aggregates
        seed=lab.SEED+year+10000*(sc=='oct31');standard=np.random.default_rng(seed).standard_normal((lab.DRAWS,len(q)))
        for rule in RULES:
            a=pool[pool.scenario.eq(sc)&pool.cycle.eq(year)&pool.variant.eq(rule)].set_index('target_id').loc[q.target_id].reset_index()
            polled=q[['target_id','cycle','scenario','geography','actual','history_selection_10pp']].copy();polled['q_pp']=a.q_pp.to_numpy()
            polled['absolute_error_pp']=abs(polled.q_pp-100*polled.actual);polled['correct']=np.where(polled.q_pp.notna()&polled.actual.notna(),polled.q_pp.gt(0).eq(polled.actual.gt(0)),np.nan)
            raw.append(polled.assign(variant=rule,evidence=evidence))
            for calibration in CONFIG['calibration']:
                ck=(sc,year,rule)
                if calibration=='Frozen bias':poll=lab.load_poll(sc,year)
                else:
                    if ck not in fit_cache:fit_cache[ck]=refit_bias(sc,year,rule,aggregates,history)
                    poll=fit_cache[ck]
                name=rule+' | '+calibration;p,cov=predict(q,prior,a,poll,name)
                if rule==REFERENCE:
                    np.testing.assert_allclose(p.prediction_pp,q.prediction_pp,atol=1e-9);np.testing.assert_allclose(cov,prior['covariance'],atol=1e-9)
                np.testing.assert_allclose(cov,prior['covariance'],atol=1e-9)
                draws=p.prediction_pp.to_numpy()+standard@np.linalg.cholesky(cov).T
                row,freq=lab.seat_row(p,draws,name,ref);row['expected_D_exact']=row['expected_D'];row=seat_scores(row,freq)
                predictions.append(p.assign(variant=rule,calibration=calibration,evidence=evidence))
                seats.append(dict(row,variant=rule,calibration=calibration,evidence=evidence))
                biases.append(pd.DataFrame(dict(geography=lab.gaussian.STATES,bias_pp=poll['bias_mean'])).assign(cycle=year,scenario=sc,variant=rule,calibration=calibration,evidence=evidence))
                checks.append(dict(cycle=year,scenario=sc,variant=rule,calibration=calibration,evidence=evidence,covariance_preserved=True,reference_reproduced=rule==REFERENCE,training_max_cycle=train_max))
        print('Poll weights',evidence,sc,year,'complete',flush=True)
    p=pd.concat(predictions,ignore_index=True);s=pd.DataFrame(seats);raw=pd.concat(raw,ignore_index=True)
    from model_portfolio import summary_tables
    cycles,summary=summary_tables(p)
    dimensions=p[['model','variant','calibration']].drop_duplicates()
    summary=summary.merge(dimensions,on='model',validate='many_to_one');cycles=cycles.merge(dimensions,on='model',validate='many_to_one')
    raw_summary=raw[raw.evidence.eq('frozen')&raw.cycle.between(2016,2024)&raw.q_pp.notna()].groupby(['scenario','variant']).agg(n=('actual','count'),mae_pp=('absolute_error_pp','mean'),correct=('correct','sum')).reset_index()
    ranks=pd.concat(rr,ignore_index=True);assert ranks.source_cycle.lt(ranks.cycle).all()
    assert not p.duplicated(['evidence','scenario','cycle','model','target_id']).any();assert p[p.cycle.eq(2026)].actual.isna().all()
    weights=pd.concat(ww,ignore_index=True)
    for name,t in dict(predictions=p,seats=s,cycle_scores=cycles,summary=summary,raw_polls=raw,raw_summary=raw_summary,ratings=ranks,sample_weights=weights,bias_estimates=pd.concat(biases),checks=pd.DataFrame(checks)).items():t.to_parquet(out/(name+'.parquet'),index=False)
    lab.finish(out,dict(kind='poll_weight_sensitivity',config=CONFIG,source_hashes=hashes,source_live=str(live.relative_to(lab.ROOT)),as_of=meta['as_of'],freshness=meta['freshness'],
                       limitations='Gaussian only; fixed prior and original polling variance budgets/precision; no full variance or hyperparameter retuning; exploratory historical architecture comparisons',promotion=False))
    lab.write_json(index,dict(run=str(out.relative_to(lab.ROOT)),manifest_sha256=lab.sha(out/'manifest.json')))
    return out
