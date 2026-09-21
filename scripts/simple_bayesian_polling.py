"""Small, exact grid/Normal polling update. See SIMPLE_BAYESIAN_POLLING_MODEL.md.

No MCMC, no regression slopes, no inferred per-state covariance loadings.
All internal margins/scales are percentage points. Historical relevance is a
power likelihood, explicitly including normalization in grid evidence.
"""
from pathlib import Path
from datetime import datetime, timezone
from itertools import product
import hashlib
import json
import numpy as np
import pandas as pd
from scipy.special import logsumexp, ndtr
from scipy.stats import norm
from scipy.optimize import brentq

STATES = 'AL AK AZ AR CA CO CT DE FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS MO MT NE NV NH NJ NM NY NC ND OH OK OR PA RI SC SD TN TX UT VT VA WA WV WI WY'.split()
HISTORY_SDS = [10., 20., 30.]
POLL_SDS = [3., 6., 9.]
RHOS = [0., .1, .3]
CONFIG = dict(poll_half_life_days=30., history_half_life_years=8., other_type_weight=.5,
              bias_prior_sd_pp=3., shared_poll_sd_pp=2., fresh_firm_sd_pp=4.,
              grid_history_sd_pp=HISTORY_SDS, grid_poll_sd_pp=POLL_SDS, grid_rho=RHOS,
              seed=190926, draws=20000)
LABELS = {'linked':'New linked polling', 'local':'New local polling control',
          'raw30':'Raw 30-day polling / history fallback',
          'gaussian':'Previous Gaussian', 'student5':'Previous Student-t',
          'nonbayes_bias':'Previous corrected polling',
          'nonbayes_momentum':'Previous corrected polling + momentum'}


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def json_write(path, value):
    Path(path).write_text(json.dumps(value, indent=2, default=str, allow_nan=False)+'\n')


def manifest(out):
    out = Path(out)
    json_write(out/'manifest.json', {str(p.relative_to(out)):sha(p) for p in sorted(out.rglob('*'))
                                   if p.is_file() and p.name != 'manifest.json'})


def verify(out):
    out = Path(out)
    for p, digest in json.loads((out/'manifest.json').read_text()).items():
        if sha(out/p) != digest:
            raise ValueError('Artifact checksum mismatch: '+p)
    return sha(out/'manifest.json')


def normal_update(mean, cov, observed, values, observation_cov):
    """Normal conditioning plus log marginal evidence; accepts sparse observations."""
    mean, cov = np.asarray(mean, float), np.asarray(cov, float)
    obs = np.asarray(observed, int)
    if not len(obs):
        return mean.copy(), cov.copy(), 0.
    r = np.asarray(values)-mean[obs]
    v = cov[np.ix_(obs, obs)]+observation_cov
    chol = np.linalg.cholesky(v)
    z = np.linalg.solve(chol, r)
    a = np.linalg.solve(chol, cov[obs, :])
    m = mean+a.T@z
    c = cov-a.T@a
    ll = -.5*(len(obs)*np.log(2*np.pi)+2*np.log(np.diag(chol)).sum()+z@z)
    return m, (c+c.T)/2, float(ll)


def relevance(cycle, year):
    return 2.**(-(year-cycle)/CONFIG['history_half_life_years'])*(1. if cycle%4 == year%4 else CONFIG['other_type_weight'])


def aggregate(targets, waves):
    """One row per sample, fixed cutoff; no cumulative double update."""
    if targets.target_id.duplicated().any():
        raise ValueError('Duplicate target')
    if waves.duplicated(['target_id', 'sample_key']).any():
        raise ValueError('Duplicate underlying sample: clean or replace before update')
    if len(waves) and ((waves.age_days < 0).any() or not np.isfinite(waves[['margin','age_days']]).all().all()):
        raise ValueError('Invalid or future poll')
    groups = dict(tuple(waves.groupby('target_id')))
    records = []
    for t in targets.itertuples():
        w = groups.get(t.target_id)
        r = dict(target_id=t.target_id, q_pp=np.nan, firm_mass=0., sample_count=0,
                 firm_count=0, reported_n_total=0., unknown_release_count=0)
        if w is not None and len(w):
            a = np.exp2(-w.age_days.to_numpy(float)/CONFIG['poll_half_life_days'])
            a /= w.groupby('firm').firm.transform('size').to_numpy()
            mass = a.sum()
            r.update(q_pp=float(np.dot(a, w.margin)*100/mass), firm_mass=float(mass),
                     sample_count=len(w), firm_count=w.firm.nunique(),
                     reported_n_total=float(w.reported_n.sum()),
                     unknown_release_count=int(w.publication_unknown.sum()))
        records.append(r)
    return pd.DataFrame(records)


def covariance(n, history_sd, rho):
    return history_sd**2*((1-rho)*np.eye(n)+rho*np.ones((n,n)))


def fit(history, year):
    """Exact Gaussian integration over biases, finite-grid integration over scales."""
    tr = history[history.cycle.lt(year)&history.actual.notna()&history.prior_latest_cycle.notna()&history.prior_latest_cycle.lt(history.cycle)].copy()
    pol = tr[tr.q_pp.notna()]
    if tr.cycle.nunique() < 4 or pol.cycle.nunique() < 3:
        raise ValueError('Need four earlier outcome cycles and three earlier polled cycles')
    prior_logs = {}
    for sd, rho in product(HISTORY_SDS, RHOS):
        ll = 0.
        for cycle, g in tr.groupby('cycle'):
            e = 100*(g.actual-g.prior).to_numpy()
            _, _, val = normal_update(np.zeros(len(g)), np.zeros((len(g),len(g))),
                                     np.arange(len(g)), e, covariance(len(g),sd,rho))
            ll += relevance(cycle,year)*val
        prior_logs[(sd,rho)] = ll
    bias_fits = {}
    for sd in POLL_SDS:
        p = np.eye(50)/CONFIG['bias_prior_sd_pp']**2
        h = np.zeros(50)
        constant = 0.
        for cycle, g in pol.groupby('cycle'):
            si = np.array([STATES.index(s) for s in g.geography])
            H = np.eye(50)[si]
            e = g.q_pp.to_numpy()-100*g.actual.to_numpy()
            r = np.diag(sd**2+CONFIG['fresh_firm_sd_pp']**2/g.firm_mass.to_numpy())
            r += CONFIG['shared_poll_sd_pp']**2
            ch = np.linalg.cholesky(r)
            z = np.linalg.solve(ch,e); a = np.linalg.solve(ch,H)
            w = relevance(cycle,year)
            p += w*(a.T@a); h += w*(a.T@z)
            constant -= .5*w*(len(g)*np.log(2*np.pi)+2*np.log(np.diag(ch)).sum()+z@z)
        c = np.linalg.solve(p,np.eye(50)); m = c@h
        logz = constant-.5*50*np.log(CONFIG['bias_prior_sd_pp']**2)-.5*np.linalg.slogdet(p)[1]+.5*h@m
        bias_fits[sd] = (m,c,logz)
    combinations = []
    probabilities = [[.25,.5,.25],[.25,.5,.25],[.5,.35,.15]]
    for i,j,k in product(range(3),repeat=3):
        hs,ps,rho = HISTORY_SDS[i],POLL_SDS[j],RHOS[k]
        b,c,ll = bias_fits[ps]
        combinations.append(dict(history_sd=hs,poll_sd=ps,rho=rho,bias_mean=b,bias_cov=c,
                                 logweight=np.log(probabilities[0][i]*probabilities[1][j]*probabilities[2][k])+prior_logs[(hs,rho)]+ll))
    logs = np.array([g['logweight'] for g in combinations]); logs -= logsumexp(logs)
    for g,l in zip(combinations,logs):g['logweight'] = float(l)
    metadata = dict(cycle=int(year), training_first_cycle=int(tr.cycle.min()), training_max_cycle=int(tr.cycle.max()),
                    training_cycles=int(tr.cycle.nunique()), training_contests=len(tr),
                    polled_training_cycles=int(pol.cycle.nunique()), polled_training_contests=len(pol),
                    current_election_type='presidential' if year%4==0 else 'midterm',
                    uncertain_global_settings=3, bias_variables=50, grid_combinations=27,
                    historical_effective_cycle_mass=float(sum(relevance(c,year) for c in tr.cycle.unique())))
    return combinations, metadata


def predict_components(test, fitted, local=False, observe_ids=None):
    """Integrate history bias analytically; return Gaussian mixture components."""
    n = len(test); means=[]; covs=[]; logs=[]; info=[]
    si = np.array([STATES.index(s) for s in test.geography])
    obs = np.flatnonzero(test.q_pp.notna().to_numpy())
    if observe_ids is not None:
        obs = np.array([i for i in obs if test.target_id.iloc[i] in observe_ids],int)
    prior = 100*test.prior.to_numpy()
    for g in fitted:
        if local and g['rho'] != 0:continue
        k = covariance(n,g['history_sd'],0 if local else g['rho'])
        if len(obs):
            b = g['bias_mean'][si[obs]]
            r = g['bias_cov'][np.ix_(si[obs],si[obs])].copy()
            if local:r = np.diag(np.diag(r))
            else:r += CONFIG['shared_poll_sd_pp']**2
            r += np.diag(g['poll_sd']**2+CONFIG['fresh_firm_sd_pp']**2/test.firm_mass.to_numpy()[obs])
            m,c,ll = normal_update(prior,k,obs,test.q_pp.to_numpy()[obs]-b,r)
        else:m,c,ll = prior,k,0.
        means.append(m);covs.append(c);logs.append(g['logweight']+ll)
        info.append({a:g[a] for a in ['history_sd','poll_sd','rho']})
    logs = np.asarray(logs); weights = np.exp(logs-logsumexp(logs))
    return np.array(means),np.array(covs),weights,pd.DataFrame(info).assign(weight=weights)


def mixture_summary(means,covs,weights,actual=None):
    sd = np.sqrt(np.diagonal(covs,axis1=1,axis2=2))
    mean = weights@means
    variance = weights@(sd**2+means**2)-mean**2
    p = weights@ndtr(means/sd)
    rows = dict(prediction_pp=mean,prediction=mean/100,posterior_sd_pp=np.sqrt(np.maximum(variance,0)),p_dem=p)
    for level in [50,80,95]:
        alpha=(1-level/100)/2
        for side,prob in [('lo',alpha),('hi',1-alpha)]:
            rows[f'{side}{level}_pp'] = [brentq(lambda x:np.dot(weights,ndtr((x-means[:,j])/sd[:,j]))-prob,
                                             float((means[:,j]-12*sd[:,j]).min()),float((means[:,j]+12*sd[:,j]).max())) for j in range(means.shape[1])]
    rows['outside_margin_bounds_probability'] = weights@(ndtr((-100-means)/sd)+ndtr((means-100)/sd))
    if actual is not None:
        rows['log_predictive_density'] = logsumexp(np.log(weights)[:,None]+norm.logpdf(np.asarray(actual)[None,:]*100,means,sd),axis=0)
    return pd.DataFrame(rows)


def mixture_draws(means,covs,weights,rng,count):
    result=np.empty((count,means.shape[1]));selected=rng.choice(len(weights),count,p=weights)
    for k in np.unique(selected):
        ids=np.flatnonzero(selected==k)
        result[ids]=means[k]+rng.standard_normal((len(ids),means.shape[1]))@np.linalg.cholesky(covs[k]).T
    return result


def forecast(test,fitted,model='linked',draws=20000,seed=0):
    rng=np.random.default_rng(seed)
    if model=='linked':
        m,c,w,grid=predict_components(test,fitted)
        pred=mixture_summary(m,c,w,test.actual.to_numpy())
        samples=mixture_draws(m,c,w,rng,draws)
        mean=w@m
        final_cov=np.einsum('k,kij->ij',w,c)+np.einsum('k,ki,kj->ij',w,m,m)-np.outer(mean,mean)
    elif model=='local':
        frames=[];samplelist=[];grids=[]
        for i in range(len(test)):
            t=test.iloc[[i]]
            m,c,w,g=predict_components(t,fitted,local=True)
            frames.append(mixture_summary(m,c,w,t.actual.to_numpy()))
            samplelist.append(mixture_draws(m,c,w,rng,draws)[:,0])
            grids.append(g.assign(target_id=t.target_id.iloc[0]))
        pred=pd.concat(frames,ignore_index=True); samples=np.column_stack(samplelist);grid=pd.concat(grids,ignore_index=True)
        final_cov=np.diag(pred.posterior_sd_pp.to_numpy()**2)
    else:raise ValueError(model)
    pred=pd.concat([test.reset_index(drop=True),pred],axis=1)
    pred['model']=model
    return pred,samples,grid,final_cov


def prepare(lab):
    """Pinned inputs, each horizon's full raw sample catalog, exact roster checks."""
    from load_final_dataset import open_dataset
    from simple_baselines import prepare_inputs, poll_predict
    from bayesian_gaussian import verify_manifest
    lab=Path(lab).resolve()
    root=lab/'reports/baselines/20260918T055206.305739Z'
    source=lab/'reports/bayesian/20260919T015548.653455Z'
    tails=lab/'reports/bayesian_tails/20260919T025118.460583Z'
    verify_manifest(source);verify_manifest(tails)
    settings=json.loads((source/'settings.json').read_text())
    paths={k:Path(v['path']) for k,v in settings['source_inputs'].items()}
    for k,v in settings['source_inputs'].items():
        if sha(v['path'])!=v['sha256']:raise ValueError('Changed input '+k)
    record=json.loads((root/'data_inputs.json').read_text())
    snapshot=Path(record['dataset']['snapshot'])
    if sha(snapshot/'manifest.json')!=record['dataset']['manifest_sha256']:raise ValueError('Changed final snapshot')
    data=open_dataset(snapshot=snapshot)
    history=pd.read_parquet(paths['history']).query("base=='fixed5_8' and kind=='senate'").copy()
    old=pd.read_parquet(tails/'predictions.parquet')
    roster=pd.read_parquet(Path(settings['source'])/'full_seat_ledger.parquet').query("model=='polling'")
    allwaves=[];histories=[];audits=[];checks=[]
    original=data.load_table('contest_inputs_reference')
    for scenario,h in history.groupby('scenario'):
        # Saved model context dates are the actual comparison cutoffs. Do not infer them from scenario names.
        cut=h[['target_id','context_id']]
        if cut.target_id.duplicated().any():raise ValueError('Duplicate saved history target')
        inp=original.drop(columns='context_id').merge(cut,on='target_id',validate='one_to_one')
        _,waves,audit,_=prepare_inputs(data,inp)
        waves=waves[waves.target_id.isin(h.target_id)].copy()
        release=audit.set_index('observation_id').release
        def dates(row):
            values=release.reindex(row.observation_ids.split('|'))
            return max(row.field_end,values.max()) if values.notna().any() else row.field_end
        waves['available_date']=[dates(r) for r in waves.itertuples()]
        if waves.available_date.gt(waves.cutoff).any():raise ValueError('Future publication admitted')
        # Verify original sample inventory and old raw means independently before changing weights.
        for half,t in h.groupby('poll_half_life'):
            p=poll_predict(t,waves,float(half),0).set_index('target_id')
            t=t.set_index('target_id')
            if not (p.n_samples==t.n_samples).all():raise ValueError('Sample roster changed at '+scenario)
            if not np.allclose(p.poll_mean,t.poll_mean,equal_nan=True,atol=1e-12):raise ValueError('Saved raw polling mismatch')
        a=aggregate(h,waves)
        h=h.merge(a,on='target_id',validate='one_to_one')
        histories.append(h);allwaves.append(waves.assign(scenario=scenario));audits.append(audit.assign(scenario=scenario))
        checks.append(dict(scenario=scenario,samples=len(waves),unknown_release=int(waves.publication_unknown.sum()),
                           original_raw_averages_reproduced=True,original_sample_counts_reproduced=True))
    input_paths=list(paths.values())+[source/'manifest.json',tails/'manifest.json',tails/'predictions.parquet',
                Path(settings['source'])/'full_seat_ledger.parquet',root/'data_inputs.json',snapshot/'manifest.json']
    provenance={str(p):sha(p) for p in input_paths}
    return pd.concat(histories,ignore_index=True),pd.concat(allwaves,ignore_index=True),pd.concat(audits,ignore_index=True),old,roster,dict(paths=provenance,dataset=data.metadata(),sample_checks=checks)


def scores(predictions):
    rows=[];p=predictions[predictions.actual.notna()]
    for period,select in [('all_2012_2024',p.cycle.between(2012,2024)),('recent_2016_2024',p.cycle.between(2016,2024))]:
        for group in ['all','competitive','noncompetitive','polled','no_polls']:
            q=p[select]
            if group=='competitive':q=q[q.history_selection_10pp=='competitive']
            if group=='noncompetitive':q=q[q.history_selection_10pp=='not_selected']
            if group=='polled':q=q[q.n_samples>0]
            if group=='no_polls':q=q[q.n_samples==0]
            for (scenario,model),g in q.groupby(['scenario','model']):
                errors=abs(g.prediction_pp-100*g.actual)
                r=dict(period=period,group=group,scenario=scenario,model=model,n=len(g),cycles=g.cycle.nunique(),
                       correct=int(((g.prediction_pp>0)==(g.actual>0)).sum()),
                       accuracy=float(((g.prediction_pp>0)==(g.actual>0)).mean()),
                       mae_pp=float(errors.groupby(g.cycle).mean().mean()))
                if g.p_dem.notna().all():
                    r['brier']=float(((g.p_dem-(g.actual>0))**2).mean())
                    for level in [50,80,95]:r['coverage'+str(level)]=float(((100*g.actual>=g['lo'+str(level)+'_pp'])&(100*g.actual<=g['hi'+str(level)+'_pp'])).mean())
                    r['mean95_width_pp']=float((g.hi95_pp-g.lo95_pp).mean())
                rows.append(r)
    return pd.DataFrame(rows)


def seat_counts(roster,test,pred,draws):
    fixed=roster[~roster.target_id.isin(test.target_id)]
    if len(roster)!=100 or len(fixed)+len(test)!=100:raise ValueError('Seat roster mismatch')
    fixed_d=int((fixed.caucus=='D').sum())
    counts=fixed_d+(draws>0).sum(axis=1)
    lo,hi=np.quantile(counts,[.025,.975])
    return dict(point_D=int(fixed_d+(pred.prediction_pp>0).sum()),point_R=int(100-fixed_d-(pred.prediction_pp>0).sum()),
                probability_call_D=int(fixed_d+(pred.p_dem>.5).sum()),expected_D=float(counts.mean()),
                D_lo95=int(lo),D_hi95=int(hi),p_D_at_least_51=float((counts>=51).mean()),
                p_D_exactly_50=float((counts==50).mean()),fixed_D=fixed_d,
                actual_D=int((roster.actual_caucus=='D').sum()) if test.cycle.iloc[0]<2026 else None,
                unmodeled_contested=int((fixed.contested).sum()))


def build(lab):
    lab=Path(lab).resolve()
    original_hashes={p.name:sha(p) for p in lab.glob('*.ipynb') if p.name!='SIMPLE_BAYESIAN_POLLING.ipynb'}
    history,waves,audit,old,roster,provenance=prepare(lab)
    out=lab/'reports/simple_bayesian_polling'/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')
    out.mkdir(parents=True);(out/'draws').mkdir()
    history.to_parquet(out/'prepared_history.parquet',index=False)
    waves.to_parquet(out/'samples.parquet',index=False);audit.to_parquet(out/'sample_audit.parquet',index=False)
    records=[];grids=[];fits=[];seats=[];biases=[];decomp=[];masked=[];trace=[];correlations=[]
    refs=old[old.model.isin(['gaussian','student5','nonbayes_bias','nonbayes_momentum'])].copy()
    for (scenario,year),r in refs.query("model=='gaussian'").groupby(['scenario','cycle']):
        hist=history[history.scenario==scenario]
        test=hist[hist.cycle==year].merge(r[['target_id','history_selection_10pp']],on='target_id',validate='one_to_one').sort_values('target_id').reset_index(drop=True)
        if set(test.target_id)!=set(r.target_id):raise ValueError('Benchmark roster mismatch')
        fitted,meta=fit(hist,int(year));fits.append(dict(scenario=scenario,**meta))
        for i,g in enumerate(fitted):
            grids.append(dict(scenario=scenario,cycle=year,model='linked',stage='history',target_id='',
                              **{k:g[k] for k in ['history_sd','poll_sd','rho']},weight=float(np.exp(g['logweight']))))
        rr=roster[(roster.cycle==year)&(roster.scenario==scenario)]
        for model in ['linked','local']:
            pred,draw,g,cov=forecast(test,fitted,model,CONFIG['draws'],CONFIG['seed']+int(year)+(0 if model=='linked' else 111))
            records.append(pred)
            grids.extend(g.assign(scenario=scenario,cycle=year,model=model,stage='forecast').to_dict('records'))
            seats.append(dict(scenario=scenario,cycle=int(year),model=model,**seat_counts(rr,test,pred,draw)))
            np.savez_compressed(out/'draws'/f'{scenario}_{year}_{model}.npz',margins_pp=draw,target_ids=test.target_id.to_numpy(str),covariance_pp2=cov)
            if year==2026 and model=='linked':
                d=np.sqrt(np.diag(cov));corr=cov/np.outer(d,d)
                for i in range(len(test)):
                    for j in range(len(test)):
                        correlations.append(dict(target_a=test.target_id.iloc[i],target_b=test.target_id.iloc[j],state_a=test.geography.iloc[i],state_b=test.geography.iloc[j],posterior_correlation=float(corr[i,j])))
                for i,t in test.iterrows():
                    m,c,w,_=predict_components(test,fitted,observe_ids={t.target_id})
                    own=float((w@m)[i]);post=float(pred.prediction_pp.iloc[i])
                    # Historical mixture of state biases, before forecast feedback.
                    hw=np.exp([z['logweight'] for z in fitted]);si=STATES.index(t.geography)
                    bm=np.array([z['bias_mean'][si] for z in fitted]);bv=np.array([z['bias_cov'][si,si] for z in fitted])
                    biases.append(dict(geography=t.geography,target_id=t.target_id,bias_poll_minus_final_pp=float(hw@bm),
                                       bias_sd_pp=float(np.sqrt(hw@(bv+bm**2)-(hw@bm)**2))))
                    decomp.append(dict(target_id=t.target_id,geography=t.geography,prior_pp=100*t.prior,raw_poll_pp=t.q_pp,
                                       own_poll_update_pp=own-100*t.prior,other_poll_update_pp=post-own,posterior_pp=post,
                                       no_poll=bool(pd.isna(t.q_pp))))
        raw=test.copy();raw['model']='raw30';raw['prediction_pp']=raw.q_pp.fillna(100*raw.prior);raw['prediction']=raw.prediction_pp/100
        records.append(raw)
        # Complete-state withholding, exact mixture recomputation. Keep historical final only for scoring.
        if year in [2020,2024,2026]:
            for i,t in test[test.q_pp.notna()].iterrows():
                without=test.copy();without.loc[without.geography.eq(t.geography),'q_pp']=np.nan
                # When two seats share a state, withhold BOTH; score each held-out contest once.
                for model in ['linked','local']:
                    target=without if model=='linked' else without.iloc[[i]]
                    m,c,w,_=predict_components(target,fitted,local=model=='local')
                    j=i if model=='linked' else 0
                    s=mixture_summary(m[:,[j]],c[:,j:j+1,j:j+1],w,[t.actual]).iloc[0].to_dict()
                    masked.append(dict(scenario=scenario,cycle=int(year),target_id=t.target_id,geography=t.geography,model=model,actual=t.actual,prior_pp=100*t.prior,**s))
        if year==2026:
            # Fixed-cutoff arrival replay: availability order; no future clock or repeated posterior update.
            ws=waves[(waves.scenario==scenario)&waves.target_id.isin(test.target_id)].sort_values(['available_date','target_id','sample_key']).reset_index(drop=True)
            checkpoints=sorted(set([0,len(ws)]+list(range(1,len(ws)+1,10))))
            selected=['AK','MI','NH','TX']
            for count in checkpoints:
                part=ws.iloc[:count]
                a=aggregate(test,part)
                replay=test.drop(columns=a.columns.drop('target_id')).merge(a,on='target_id',validate='one_to_one')
                m,c,w,_=predict_components(replay,fitted)
                mean=w@m
                for i,t in replay.iterrows():
                    if t.geography in selected:
                        trace.append(dict(samples_seen=count,last_available_date=str(part.available_date.max()) if count else '',
                                          cutoff=t.context_id,geography=t.geography,mean_pp=float(mean[i]),
                                          own_samples=int(t.sample_count),arrival_date_proxy_count=int(part.publication_unknown.sum())))
        print(f'{scenario} {year}: {len(test)} contests; train {meta["training_cycles"]} cycles / {meta["polled_training_cycles"]} polled',flush=True)
    pred=pd.concat(records+[refs],ignore_index=True)
    for key,g in pred.groupby(['scenario','cycle']):
        sets=g.groupby('model').target_id.apply(set)
        if any(s!=sets.iloc[0] for s in sets):raise ValueError('Unequal comparison cases '+str(key))
    pred.to_parquet(out/'predictions.parquet',index=False)
    scores(pred).to_parquet(out/'metrics.parquet',index=False)
    for name,rows in [('grid_weights',grids),('fits',fits),('seats',seats),('current_bias',biases),('current_decomposition',decomp),('masked_predictions',masked),('arrival_trace',trace),('current_correlations',correlations)]:
        pd.DataFrame(rows).to_parquet(out/(name+'.parquet'),index=False)
    json_write(out/'settings.json',dict(config=CONFIG,as_of=provenance['dataset']['as_of'],provenance=provenance,
                                       old_notebook_hashes=original_hashes,model='Finite-grid generalized Bayesian Gaussian polling update',
                                       controls='Local marginal forecasts use only own polls to update scale probabilities; no interstate forecast dependence',
                                       future_features='none',promotion=False))
    for name in ['SIMPLE_BAYESIAN_POLLING_MODEL.md']:(out/name).write_bytes((lab/name).read_bytes())
    (out/Path(__file__).name).write_bytes(Path(__file__).read_bytes())
    changed=[name for name,digest in original_hashes.items() if sha(lab/name)!=digest]
    if changed:raise RuntimeError('Existing notebooks changed during run: '+str(changed))
    manifest(out)
    json_write(out.parent/'latest.json',dict(artifact=out.name,manifest_sha256=sha(out/'manifest.json')))
    return out


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--lab',type=Path,default=Path(__file__).resolve().parents[1])
    args=parser.parse_args()
    print(build(args.lab))
