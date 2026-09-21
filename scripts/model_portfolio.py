"""Four Bayesian alternatives and a predictive mixture, with mean-only polling shifts.

A component is selected for the whole state vector, never independently by state.
Each model sees the same evidence; these are alternatives, not independent data.
"""
from pathlib import Path
import json
import numpy as np
import pandas as pd
from scipy.stats import norm
import election_lab as lab
from coverage_balance import score_rows,seat_scores
from release_alternatives import older_pair,matched_tail,OLD_GAUSSIAN,OLD_STUDENT,MATCHED_STUDENT

CONFIG_PATH=lab.ROOT/'config/ensemble_v1.json'


def configuration():
    c=json.loads(CONFIG_PATH.read_text());w=c['component_weights']
    if set(w)!={'Bayesian',MATCHED_STUDENT,OLD_GAUSSIAN,OLD_STUDENT}:raise ValueError('Expected four named Bayesian components')
    if any(x<0 for x in w.values()) or not np.isclose(sum(w.values()),1.):raise ValueError('Mixture weights must sum to one')
    if any(not 0<a<=1 for a in c['mean_shift_weights']):raise ValueError('Invalid polling mean-shift weight')
    return c


def mixture_moments(means,covariances,weights):
    means=np.asarray(means);weights=np.asarray(weights)
    center=weights@means;d=means-center
    covariance=np.einsum('m,mij->ij',weights,np.asarray(covariances))+np.einsum('m,mi,mj->ij',weights,d,d)
    return center,covariance


def weighted_quantiles(values,weights,probabilities):
    values=np.asarray(values);weights=np.asarray(weights,float);p=np.asarray(probabilities,float)
    if values.ndim==1:values=values[:,None]
    result=np.empty((len(p),values.shape[1]))
    for j in range(values.shape[1]):
        order=np.argsort(values[:,j]);cdf=np.cumsum(weights[order]);cdf/=cdf[-1]
        result[:,j]=values[order[np.minimum(np.searchsorted(cdf,p),len(order)-1)],j]
    return result


def make_mixture(components,config):
    names=list(config['component_weights']);weights=np.array([config['component_weights'][n] for n in names])
    first=components[names[0]]['predictions']
    for n in names:
        if list(components[n]['predictions'].target_id)!=list(first.target_id):raise ValueError('Model contest order differs')
    means=np.array([components[n]['predictions'].margin_pp.to_numpy() for n in names])
    mean,cov=mixture_moments(means,[components[n]['covariance'] for n in names],weights)
    samples=np.concatenate([components[n]['draws'] for n in names])
    draw_weights=np.concatenate([np.full(len(components[n]['draws']),w/len(components[n]['draws'])) for n,w in zip(names,weights)])
    np.testing.assert_allclose(draw_weights.sum(),1.,atol=1e-12)
    levels=[.025,.10,.15,.25,.5,.75,.85,.90,.975]
    quantiles=weighted_quantiles(samples,draw_weights,levels)
    return dict(mean=mean,covariance=cov,samples=samples,weights=draw_weights,quantiles=quantiles,
                component_names=names,component_weights=weights)


def distribution_rows(template,mixture,delta,label):
    """Translate the empirical mixture without changing its centered joint draws."""
    mean=mixture['mean']+delta;draws=mixture['samples']+delta
    weights=mixture['weights'];quantiles=mixture['quantiles']+delta
    p=template[['scenario','cycle','target_id','geography','special','actual','q_pp','firm_mass','history_selection_10pp']].copy()
    for c in ['as_of','outcome_type']:
        if c in template:p[c]=template[c].to_numpy()
    p['model']=label;p['prediction_pp']=mean;p['prediction']=mean/100;p['margin_pp']=mean
    p['posterior_sd_pp']=np.sqrt(np.diag(mixture['covariance']));p['sigma_pp']=p.posterior_sd_pp
    p['median_pp']=quantiles[4];p['p_dem']=weights@(draws>0)
    for level,lo,hi in [(95,0,8),(80,1,7),(70,2,6),(50,3,5)]:p[f'lo{level}_pp']=quantiles[lo];p[f'hi{level}_pp']=quantiles[hi]
    p=score_rows(p);p['actual_pp']=100*p.actual
    return p,draws


def weighted_seats(pred,draws,weights,reference):
    fixed=int(reference.fixed_D);counts=fixed+(draws>0).sum(axis=1)
    frequency=np.bincount(counts,weights=weights,minlength=101)
    lo,hi=weighted_quantiles(counts,weights,[.15,.85])[:,0]
    point=fixed+int(pred.margin_pp.gt(0).sum());expected=fixed+pred.p_dem.sum()
    np.testing.assert_allclose(expected,counts@weights,atol=1e-9)
    row=dict(scenario=pred.scenario.iloc[0],cycle=int(pred.cycle.iloc[0]),model=pred.model.iloc[0],
             fixed_D=fixed,unmodeled_contested=int(reference.unmodeled_contested),actual_D=float(reference.actual_D),
             point_D=point,point_R=100-point,expected_D=float(expected),expected_D_exact=float(expected),expected_R=float(100-expected),
             p_D_control=float(weights@(counts>=51)),D_lo70=int(lo),D_hi70=int(hi),method='Whole-vector predictive mixture; weighted joint draws')
    return seat_scores(row,frequency),frequency


def additions(main_rows,main_fit,lam,calendar,main_draws,main_covariance,polling_rows,reference,include_student=True):
    """Extra rows for one historical/live case; reference rows are never changed."""
    alternatives,diagnostics=older_pair(main_rows,calendar,include_student)
    rows=[];seats=[];moments={};checks=[]
    components={'Bayesian':dict(predictions=main_rows,draws=main_draws,covariance=main_covariance),**alternatives}
    if include_student:
        matched,diag=matched_tail(main_rows,main_fit,lam,main_covariance)
        components[MATCHED_STUDENT]=matched;diagnostics.append(diag)
    for name,comp in components.items():
        if name=='Bayesian':continue
        pred=comp['predictions'];rows.append(pred)
        seat,freq=lab.seat_row(pred,comp['draws'],name,reference,'Joint Gaussian' if name==OLD_GAUSSIAN else 'Joint Student MCMC')
        seat['expected_D_exact']=seat['expected_D'];seats.append(seat_scores(seat,freq))
        moments[name]=dict(mean=pred.margin_pp.to_numpy(),covariance=comp['covariance'],seat_count_frequency=freq)
    if include_student:
        config=configuration();mix=make_mixture(components,config)
        if list(polling_rows.target_id)!=list(main_rows.target_id):raise ValueError('Polling helper contest mapping differs')
        for alpha in [0.,*config['mean_shift_weights']]:
            delta=alpha*(polling_rows.margin_pp.to_numpy()-mix['mean'])
            label=config['mixture_label'] if alpha==0 else f'Mixture + polling {100*alpha:g}%'
            pred,draws=distribution_rows(main_rows,mix,delta,label)
            # Translation must preserve full dependence, not just marginal widths.
            np.testing.assert_allclose(draws-pred.margin_pp.to_numpy(),mix['samples']-mix['mean'],atol=1e-12)
            np.testing.assert_allclose(pred.hi70_pp-pred.lo70_pp,mix['quantiles'][6]-mix['quantiles'][2],atol=1e-12)
            seat,freq=weighted_seats(pred,draws,mix['weights'],reference)
            rows.append(pred);seats.append(seat)
            moments[label]=dict(mean=pred.margin_pp.to_numpy(),covariance=mix['covariance'],seat_count_frequency=freq)
            checks.append(dict(model=label,mean_shift_weight=alpha,covariance_preserved=True,component_weights=config['component_weights']))
        # At zero translation, chamber mixture probability is the weighted component probability.
        expected=sum(config['component_weights'][n]*np.mean(int(reference.fixed_D)+(components[n]['draws']>0).sum(axis=1)>=51) for n in components)
        actual=next(s['p_D_control'] for s in seats if s['model']==config['mixture_label'])
        np.testing.assert_allclose(actual,expected,atol=1e-12)
    return dict(predictions=rows,seats=seats,diagnostics=diagnostics,moments=moments,checks=checks)


def nonbayesian(q,scenario,year):
    from state_poll_bias import fit_bias
    from calibrate_margin_uncertainty import fit_scale
    h=pd.read_parquet(lab.ASSETS/'training/history.parquet');h=h[h.scenario.eq(scenario)]
    current=h[h.cycle.eq(year)].set_index('target_id').loc[q.target_id].reset_index()
    mean,*_=fit_bias(h[h.cycle.lt(year)],current,5,8.,'state',float(current.bias_shrinkage.iloc[0]))
    np.testing.assert_allclose(mean,current.bias_prediction,atol=1e-12)
    reference=pd.read_parquet(lab.ASSETS/'reference_blends/predictions.parquet').query('model=="Bayesian"')
    sigma=fit_scale(reference,scenario,year,'nonbayesian_pp')['sigma_pp']
    p=q.copy();p['model']='Non-Bayesian corrected';p['prediction_pp']=100*mean;p['prediction']=mean;p['median_pp']=100*mean
    p['posterior_sd_pp']=sigma;p['p_dem']=norm.cdf(p.prediction_pp/sigma)
    for level in [50,70,80,95]:
        width=norm.ppf((1+level/100)/2)*sigma;p[f'lo{level}_pp']=p.prediction_pp-width;p[f'hi{level}_pp']=p.prediction_pp+width
    p=score_rows(p);p['margin_pp']=p.prediction_pp;p['sigma_pp']=sigma;p['actual_pp']=100*p.actual
    # An unavailable interval is not an observed coverage failure.
    for level in [50,70,80,95]:
        p.loc[p[f'lo{level}_pp'].isna()|p[f'hi{level}_pp'].isna(),f'coverage{level}']=np.nan
    return p


def summary_tables(predictions):
    hist=predictions[predictions.evidence.eq('frozen')&predictions.actual.notna()&predictions.cycle.le(2024)].copy()
    metrics=['absolute_error_pp','brier','wis_pp','width70_pp','width95_pp']
    cyc=hist.groupby(['scenario','cycle','model'])[metrics].mean().reset_index()
    counts=hist.groupby(['scenario','cycle','model']).agg(n=('target_id','size'),correct=('correct','sum'),probability_n=('brier','count'),coverage70=('coverage70','mean'),coverage95=('coverage95','mean')).reset_index()
    cyc=cyc.merge(counts,on=['scenario','cycle','model'])
    rows=[]
    for first in [2012,2016,2018]:
        for (sc,model),g in hist[hist.cycle.ge(first)].groupby(['scenario','model']):
            by=g.groupby('cycle')[metrics].mean()
            rows.append(dict(first_cycle=first,scenario=sc,model=model,n=len(g),cycles=g.cycle.nunique(),correct=int(g.correct.sum()),accuracy_pct=100*g.correct.mean(),
                             probability_n=g.brier.count(),coverage70=100*g.coverage70.mean(),coverage95=100*g.coverage95.mean(),**by.mean().to_dict()))
    return cyc,pd.DataFrame(rows)


def run(include_live=True,force=False):
    """Paired historical portfolio plus latest all-model live rows, cached by content."""
    live=lab.latest_run('live') if include_live else None
    if live:
        current=pd.read_parquet(live/'predictions.parquet')
        if not set(configuration()['component_weights']).issubset(current.model):raise ValueError('Run the updated live command/notebook04 first to include all four models')
    inputs=[lab.ROOT/'election_lab.py',*sorted((lab.ROOT/'scripts').glob('*.py')),*sorted(p for p in (lab.ROOT/'config').glob('*') if p.is_file()),*sorted(p for p in lab.ASSETS.rglob('*') if p.is_file())]
    if live:inputs.append(live/'manifest.json')
    hashes={str(p.relative_to(lab.ROOT)):lab.sha(p) for p in inputs}
    key=__import__('hashlib').sha256(json.dumps(hashes,sort_keys=True).encode()).hexdigest();index=lab.ROOT/'cache/portfolio'/f'{key}.json'
    if index.exists() and not force:
        c=json.loads(index.read_text());out=lab.ROOT/c['run']
        if lab.sha(out/'manifest.json')!=c['manifest_sha256']:raise ValueError('Portfolio cache changed')
        print('Verified cached portfolio',out.name,flush=True);return lab.verify_run(out)
    out=lab.new_run('portfolio');(out/'forecasts').mkdir();preds=[];seats=[];diags=[];checks=[]
    folds=pd.read_parquet(lab.ASSETS/'main/folds.parquet');base=pd.read_parquet(lab.ASSETS/'main/predictions.parquet');refs=pd.read_parquet(lab.ASSETS/'main/seats.parquet')
    for r in folds.itertuples():
        sc=r.scenario;year=int(r.cycle)
        q=base[base.scenario.eq(sc)&base.cycle.eq(year)].sort_values('target_id').reset_index(drop=True)
        gp=lab.scored(q,'Bayesian');fit=dict(np.load(lab.ASSETS/'main'/r.fit_path));fit['a']=float(fit['a'])
        joint=np.load(lab.ASSETS/'main'/r.forecast_path);np.testing.assert_allclose(joint['mean'],gp.margin_pp,atol=1e-10)
        lab.verify_selection(sc,year);assert fit['years'].max()<year
        seed=lab.SEED+year+10000*(sc=='oct31');draws=joint['mean']+np.random.default_rng(seed).standard_normal((lab.DRAWS,len(q)))@np.linalg.cholesky(joint['covariance']).T
        ref=refs[refs.scenario.eq(sc)&refs.cycle.eq(year)].iloc[0]
        row,freq=lab.seat_row(gp,draws,'Bayesian',ref);row['expected_D_exact']=row['expected_D'];row=seat_scores(row,freq)
        nb=nonbayesian(q,sc,year)
        nbseat=dict(scenario=sc,cycle=year,model='Non-Bayesian corrected',evidence='frozen',
                    fixed_D=int(ref.fixed_D),actual_D=float(ref.actual_D),unmodeled_contested=int(ref.unmodeled_contested),
                    point_D=int(ref.fixed_D)+int(nb.margin_pp.gt(0).sum()),method='Independent-state approximation; missing if insufficient calibration history')
        nbseat['point_R']=100-nbseat['point_D']
        if nb.p_dem.notna().all():
            from plain_polling_blend import independent_seats
            summary,frequency=independent_seats(nb.p_dem.to_numpy(),int(ref.fixed_D))
            full=np.zeros(101);full[int(ref.fixed_D):int(ref.fixed_D)+len(frequency)]=frequency
            nbseat.update(summary);nbseat['expected_D_exact']=summary['expected_D'];nbseat=seat_scores(nbseat,full)
        seats.append(nbseat)
        extra=additions(gp,fit,float(r.lambda_value),None,draws,joint['covariance'],nb,ref)
        for p in [gp,nb,*extra['predictions']]:preds.append(p.assign(evidence='frozen'))
        seats.extend([dict(row,evidence='frozen'),*[dict(s,evidence='frozen') for s in extra['seats']]])
        diags.extend(d.assign(evidence='frozen',scenario=sc,cycle=year) for d in extra['diagnostics'])
        checks.extend(dict(c,scenario=sc,cycle=year) for c in extra['checks'])
        for i,(name,m) in enumerate(extra['moments'].items()):
            np.savez_compressed(out/'forecasts'/f'{sc}_{year}_{i}.npz',model=name,target_ids=q.target_id.to_numpy(str),**m)
        print('Portfolio',sc,year,'complete',flush=True)
    if live:
        names={*configuration()['component_weights'],configuration()['mixture_label'],'Non-Bayesian corrected',*[f'Mixture + polling {100*a:g}%' for a in configuration()['mean_shift_weights']]}
        preds.append(current[current.model.isin(names)].assign(evidence='live'))
        ls=pd.read_parquet(live/'seats.parquet');seats.extend(ls[ls.model.isin(names)].assign(evidence='live').to_dict('records'))
        if (live/'all_model_diagnostics.parquet').exists():diags.append(pd.read_parquet(live/'all_model_diagnostics.parquet').assign(evidence='live',scenario='matched_live',cycle=2026))
    p=pd.concat(preds,ignore_index=True);s=pd.DataFrame(seats);cyc,summary=summary_tables(p)
    assert not p.duplicated(['evidence','scenario','cycle','model','target_id']).any()
    assert p[p.cycle.eq(2026)].actual.isna().all()
    for name,t in dict(predictions=p,seats=s,cycle_scores=cyc,summary=summary,diagnostics=pd.concat(diags),checks=pd.DataFrame(checks)).items():t.to_parquet(out/(name+'.parquet'),index=False)
    lab.finish(out,dict(kind='all_model_portfolio',source_hashes=hashes,configuration=configuration(),source_live=str(live.relative_to(lab.ROOT)) if live else None,
                       validation='Rolling-origin earlier-cycle fits/tuning; architecture exploration reused evaluation years; not untouched holdout',
                       ensemble_weights_learned=False,mean_shift_weights_learned=False,promotion=False))
    lab.write_json(index,dict(run=str(out.relative_to(lab.ROOT)),manifest_sha256=lab.sha(out/'manifest.json')))
    return out


def publish_review(source, kind, models=None):
    """Publish a notebook-specific view without mutating the shared portfolio."""
    if kind not in {'older_alternatives', 'all_model_mixture'}:
        raise ValueError('Unknown portfolio review: '+kind)
    source = lab.verify_run(source)
    out = lab.new_run(kind)
    for name in ['predictions', 'seats', 'summary', 'cycle_scores', 'diagnostics', 'checks']:
        frame = pd.read_parquet(source/(name+'.parquet'))
        if models is not None and 'model' in frame:
            frame = frame[frame.model.isin(models)]
        frame.to_parquet(out/(name+'.parquet'), index=False)
    meta = json.loads((source/'run.json').read_text())
    return lab.finish(out, dict(meta, kind=kind, selected_models=models,
        source_portfolio=str(source.relative_to(lab.ROOT)),
        source_portfolio_manifest_sha256=lab.sha(source/'manifest.json')))
