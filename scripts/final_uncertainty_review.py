"""Bounded final diagnostics on frozen election forecasts, not another model search."""
from pathlib import Path
from datetime import datetime, timezone
import json
import argparse
import shutil
import numpy as np
import pandas as pd
from scipy.stats import norm, qmc
from scipy.special import xlogy
from numpy.polynomial.legendre import leggauss

import simple_bayesian_polling as v1
import simple_national_model as national
from simple_baselines import poll_predict
from calibrate_margin_uncertainty import sha, finalize
from plain_polling_blend import verify

BAYES = 'reports/signed_state_factor/20260920T052241.012596Z'
MEAN = 'reports/mean_only_polling_blend/20260920T064738.332296Z'
PLAIN = 'reports/plain_polling_blend/20260920T062747.520500Z'
UPSTREAM = 'reports/official_repair_review/20260919T172552.860612Z'
FINAL = 'data/final/snapshots/20260919T172852.916455Z'
POLL = 'reports/simple_national_model/20260920T000314.601869Z'
PUBLIC = 'reports/current_published_scenarios/20260920T034345.798141Z'
PROXIES = ['ID','MT','NE','SD']
METRICS = ['mae_pp','brier','coverage70','width70_pp','coverage95','width95_pp']
EVENTS = ['health_disruption_4y','financial_disruption_4y','security_disruption_4y','extraordinary_event_any_4y']


def scored(mean, sd, actual):
    mean,sd,actual = np.asarray(mean),np.asarray(sd),np.asarray(actual)
    p=norm.cdf(mean/sd)
    return dict(mean_pp=mean,sd_pp=sd,p_dem=p,mae_pp=abs(mean-actual),
        correct=(mean>0)==(actual>0),brier=(p-(actual>0))**2,
        coverage70=abs(actual-mean)<=norm.ppf(.85)*sd,width70_pp=2*norm.ppf(.85)*sd,
        coverage95=abs(actual-mean)<=norm.ppf(.975)*sd,width95_pp=2*norm.ppf(.975)*sd)


def recent_firm(waves):
    """Choose by latest available receipt date, field end, then firm name; no outcomes."""
    if waves.empty:return waves.copy(),None
    firm=(waves.groupby('firm').agg(available=('available_date','max'),end=('field_end','max'))
          .reset_index().sort_values(['available','end','firm'],ascending=[False,False,True]).iloc[0].firm)
    return waves[waves.firm.eq(firm)].copy(),firm


def update(prior_mean, prior_cov, q, mass, state_indices, poll):
    obs=np.flatnonzero(np.isfinite(q))
    ids=state_indices[obs]
    if np.any(np.asarray(mass)[obs]<=0):raise ValueError('Observed polls require positive information mass')
    R=poll['covariance'][np.ix_(ids,ids)]+poll['bias_covariance'][np.ix_(ids,ids)]+np.diag(16/np.asarray(mass)[obs])
    return v1.normal_update(prior_mean,prior_cov,obs,np.asarray(q)[obs]-poll['bias_mean'][ids],R)[:2]


def summarize(frame, keys):
    cycles=frame.groupby(keys+['cycle'])[METRICS].mean().reset_index()
    result=cycles.groupby(keys)[METRICS].mean().reset_index()
    counts=frame.groupby(keys).agg(n=('target_id','size'),cycles=('cycle','nunique'),correct=('correct','sum')).reset_index()
    return result.merge(counts,on=keys,validate='one_to_one')


def build(lab, information=True):
    lab=Path(lab).resolve()
    for source in [MEAN,PLAIN]:verify(lab/source)
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')
    out=lab/'reports/final_uncertainty_review'/stamp;out.mkdir(parents=True)
    print('OUTPUT',out,flush=True)
    hashes={};old_notebooks={p.name:sha(p) for p in lab.glob('*.ipynb')}
    def read(source,name):
        path=lab/source/(name+'.parquet');hashes[str(path.relative_to(lab))]=sha(path)
        return pd.read_parquet(path)
    def arrays(path):
        hashes[str(path.relative_to(lab))]=sha(path);return dict(np.load(path))
    def save(name,table):table.to_parquet(out/(name+'.parquet'),index=False)
    working_hash=sha(lab/'WORKING_MODEL.json')
    base=read(BAYES,'predictions').query('model == "repaired_both__selected"').copy()
    folds=read(BAYES,'folds').query('model == "repaired_both__selected"')
    seats=read(BAYES,'seats').query('model == "repaired_both__selected"')
    blend=read(MEAN,'predictions').query('model == "Mean-only blend"')
    history=read(UPSTREAM,'history');waves=read(UPSTREAM,'samples')
    ledger=read(UPSTREAM,'full_seat_ledger').query('model == "polling"')
    current_roster=read(FINAL+'/tables','current_contests')
    external=read(PUBLIC,'current_comparison')
    plain=read(PLAIN,'paired_inputs')
    feature_status=read(FINAL+'/tables','feature_source_selection')
    save('feature_source_status',feature_status)
    save('model_contract',pd.DataFrame([
        dict(role='Designated working candidate',model='no_U_K1',source=POLL,uncertainty='Gaussian joint',promoted=True),
        dict(role='Frozen diagnostic reference',model='repaired_both__selected',source=BAYES,uncertainty='Gaussian joint',promoted=False),
        dict(role='Mean-only sensitivity',model='Mean-only blend',source=MEAN,uncertainty='Same Bayesian covariance',promoted=False),
        dict(role='Point benchmarks',model='polling / bias',source=UPSTREAM,uncertainty='See separate pooled calibration; not used here',promoted=False),
        dict(role='Previously tested tail sensitivities',model='combined / local / national Student',source='reports/combined_student_model/20260920T025147.349063Z',uncertainty='Existing archived distributions; not refitted',promoted=False)]))
    # Roster identity is separate from candidate/caucus interpretation.
    current=base[base.cycle.eq(2026)].sort_values('target_id').reset_index(drop=True)
    roster=ledger[ledger.cycle.eq(2026)].copy()
    assert len(roster)==100 and roster.seat_id.nunique()==100
    assert roster.contested.sum()==35 and len(current)==35
    assert set(roster.loc[roster.contested,'target_id'])==set(current.target_id)
    assert set(current_roster.contest_id)==set(current.target_id)
    for x in current_roster.itertuples():
        t=current[current.target_id.eq(x.contest_id)].iloc[0]
        assert t.geography==x.state and bool(t.special)==bool(x.special)
    save('current_roster',current_roster)
    candidates=external[external.publisher.eq('DDHQ')].drop_duplicates('state')
    exceptions=candidates[candidates.state.isin(PROXIES)][['state','candidates','source_url','updated','comparison_note']].copy()
    exceptions['distribution_status']='No validated local candidate-specific distribution; use allocation bounds only'
    save('candidate_exceptions',exceptions)
    completion=seats[['scenario','cycle','fixed_D','unmodeled_contested','point_D','actual_D']].copy()
    completion['modeled_contests']=[len(base[base.scenario.eq(r.scenario)&base.cycle.eq(r.cycle)]) for r in completion.itertuples()]
    save('historical_completion',completion)
    # Joint draws exactly reconstruct the latest Bayesian and mean-only baselines.
    fold_cache={};mask_rows=[];natural=[];surprises=[];reproduction=[];coverage_rows=[];chamber=[]
    for f in folds.itertuples():
        a=arrays(lab/BAYES/f.forecast_path)
        q=base[base.scenario.eq(f.scenario)&base.cycle.eq(f.cycle)].set_index('target_id').loc[a['target_ids'].astype(str)].reset_index()
        hh=history[history.scenario.eq(f.scenario)].set_index('target_id').loc[q.target_id].reset_index()
        bb=blend[blend.scenario.eq(f.scenario)&blend.cycle.eq(f.cycle)].set_index('target_id').loc[q.target_id]
        source_fit=arrays(lab/BAYES/f.fit_path)
        assert set(source_fit['terms'].astype(str)) <= {'economy_momentum_wh','approval_wh'}, 'Review state-poll feature dependencies before masking'
        assert max(source_fit['years'])<f.cycle
        pf=arrays(lab/POLL/f'fits/{f.scenario}_{f.cycle}_poll.npz')
        poll=national.fixed_common(pf['training_values'],pf['training_noise'],pf['training_weights'],pf['budget'],0.,9.)
        si=np.array([v1.STATES.index(s) for s in q.geography])
        mean,cov=update(a['prior_mean'],a['prior_covariance'],q.q_pp.to_numpy(),q.firm_mass.to_numpy(),si,poll)
        np.testing.assert_allclose(mean,a['mean'],atol=1e-8);np.testing.assert_allclose(cov,a['covariance'],atol=1e-8)
        wf=waves[waves.scenario.eq(f.scenario)&waves.target_id.isin(q.target_id)].copy()
        agg=v1.aggregate(q,wf).set_index('target_id').loc[q.target_id]
        assert np.allclose(agg.q_pp,q.q_pp,equal_nan=True) and np.allclose(agg.firm_mass,q.firm_mass)
        assert pd.to_datetime(wf.available_date).le(pd.to_datetime(wf.cutoff)).all()
        seed=197139+f.cycle+10000*(f.scenario=='oct31')
        noise=np.random.default_rng(seed).standard_normal((30000,len(q)))@np.linalg.cholesky(cov).T
        ref=seats[seats.scenario.eq(f.scenario)&seats.cycle.eq(f.cycle)].iloc[0]
        assert np.array_equal(np.bincount(int(ref.fixed_D)+(mean+noise>0).sum(1),minlength=101),a['seat_count_frequency'])
        fold_cache[(f.scenario,f.cycle)]=(q,mean,cov,bb.margin_pp.to_numpy(),noise,poll,si)
        for name,mu in [('Bayesian',mean),('Mean-only blend',bb.margin_pp.to_numpy())]:
            counts=int(ref.fixed_D)+(noise+mu>0).sum(1)
            freq=np.bincount(counts,minlength=101)/len(counts);cdf=freq.cumsum()
            actual=ref.actual_D
            lo,hi=np.quantile(counts,[.15,.85],method='inverted_cdf')
            expected=float(ref.fixed_D+norm.cdf(mu/np.sqrt(np.diag(cov))).sum())
            chamber.append(dict(scenario=f.scenario,cycle=f.cycle,model=name,
                point_D=int(ref.fixed_D+(mu>0).sum()),expected_D=expected,actual_D=actual,
                p_D_at_least_51=float((counts>=51).mean()),D_lo70=lo,D_hi70=hi,
                expected_seat_absolute_error=abs(expected-actual) if np.isfinite(actual) else np.nan,
                seat_crps=float(abs(counts-actual).mean()-(cdf*(1-cdf)).sum()) if np.isfinite(actual) else np.nan,
                coverage70=bool(lo<=actual<=hi) if np.isfinite(actual) else None,
                unmodeled_contested=int(ref.unmodeled_contested)))
        reproduction.append(dict(scenario=f.scenario,cycle=f.cycle,posterior_reproduced=True,seat_draws_reproduced=True,
                                 prior_training_max=int(max(source_fit['years'])),poll_feature_dependency='none; momentum/approval only'))
        for i,r in q.iterrows():
            rec=dict(scenario=f.scenario,cycle=f.cycle,target_id=r.target_id,state=r.geography,
                     sample_count=int(r.sample_count),firm_count=int(r.firm_count),prior_sd_pp=r.prior_sd_pp,
                     mean_pp=mean[i],sd_pp=np.sqrt(cov[i,i]),p_dem=norm.cdf(mean[i]/np.sqrt(cov[i,i])))
            coverage_rows.append(rec)
            if f.cycle==2026:continue
            if pd.isna(r.q_pp):
                for name,m in [('Bayesian',mean[i]),('Mean-only blend',bb.margin_pp.iloc[i])]:
                    natural.append(dict(scenario=f.scenario,cycle=f.cycle,target_id=r.target_id,state=r.geography,model=name,
                                        **{k:np.asarray(v).item() for k,v in scored(m,np.sqrt(cov[i,i]),100*r.actual).items()}))
                continue
            w=wf[wf.target_id.eq(r.target_id)]
            only,firm=recent_firm(w)
            # The original plain prior differs from the repaired Bayesian prior: retain each one's own recipe.
            target=hh.iloc[[i]]
            plain_full=poll_predict(target,w,float(target.poll_half_life.iloc[0]),float(target.poll_prior_strength.iloc[0])).prediction.iloc[0]*100
            expected_plain=plain[plain.scenario.eq(f.scenario)&plain.target_id.eq(r.target_id)].plain_pp.iloc[0]
            assert np.isclose(plain_full,expected_plain)
            for mask,kept in [('full',w),('no_polls',w.iloc[:0]),('one_firm',only)]:
                aa=v1.aggregate(q.iloc[[i]],kept).iloc[0]
                values=q.q_pp.to_numpy().copy();mass=q.firm_mass.to_numpy().copy()
                values[i]=aa.q_pp;mass[i]=aa.firm_mass
                mm,cc=update(a['prior_mean'],a['prior_covariance'],values,mass,si,poll)
                pp=100*poll_predict(target,kept,float(target.poll_half_life.iloc[0]),float(target.poll_prior_strength.iloc[0])).prediction.iloc[0]
                if mask=='full':assert np.allclose(mm,mean) and np.allclose(cc,cov)
                if mask=='no_polls':
                    assert np.isnan(values[i]) and mass[i]==0 and np.isclose(pp,100*target.prior.iloc[0])
                    assert cc[i,i]>=cov[i,i]-1e-8
                for name,m in [('Bayesian',mm[i]),('Mean-only blend',.5*(mm[i]+pp))]:
                    mask_rows.append(dict(scenario=f.scenario,cycle=f.cycle,target_id=r.target_id,state=r.geography,
                        model=name,mask=mask,kept_firm=firm if mask=='one_firm' else None,kept_samples=len(kept),
                        original_samples=len(w),plain_component_pp=pp,prior_component_pp=100*target.prior.iloc[0],
                        mean_other_state_shift_pp=float(np.delete(mm-mean,i).mean()),
                        **{k:np.asarray(v).item() for k,v in scored(m,np.sqrt(cc[i,i]),100*r.actual).items()}))
        if f.cycle<2026:
            for name,m in [('Bayesian',mean),('Mean-only blend',bb.margin_pp.to_numpy())]:
                z=(100*q.actual.to_numpy()-m)/np.sqrt(np.diag(cov))
                simz=noise/np.sqrt(np.diag(cov))
                observed={'mean_error_pp':float((100*q.actual-m).mean()),'median_abs_z':float(np.median(abs(z))),
                    'fraction_abs_z_gt2':float((abs(z)>2).mean()),'fraction_abs_z_gt3':float((abs(z)>3).mean()),
                    'same_direction_fraction':float(max((z>0).mean(),(z<0).mean()))}
                sims={'mean_error_pp':noise.mean(1),'median_abs_z':np.median(abs(simz),axis=1),
                    'fraction_abs_z_gt2':(abs(simz)>2).mean(1),'fraction_abs_z_gt3':(abs(simz)>3).mean(1),
                    'same_direction_fraction':np.maximum((simz>0).mean(1),(simz<0).mean(1))}
                for metric,val in observed.items():
                    sim=sims[metric];lo,hi=np.quantile(sim,[.025,.975])
                    surprises.append(dict(scenario=f.scenario,cycle=f.cycle,model=name,n=len(q),metric=metric,value=val,
                        simulated_lo95=lo,simulated_hi95=hi,simulated_percentile=float((sim<=val).mean())))
        print('Reviewed fold',f.scenario,f.cycle,flush=True)
    save('reproduction',pd.DataFrame(reproduction));save('coverage',pd.DataFrame(coverage_rows))
    save('chamber_scores',pd.DataFrame(chamber))
    mask=pd.DataFrame(mask_rows);save('masked_predictions',mask)
    save('masked_summary',summarize(mask[mask.cycle.ge(2016)],['scenario','model','mask']))
    save('masked_older_summary',summarize(mask,['scenario','model','mask']))
    save('masked_by_cycle',mask.groupby(['scenario','cycle','model','mask'])[METRICS].mean().reset_index())
    save('masked_by_state',summarize(mask[mask.cycle.ge(2016)],['scenario','model','mask','state']))
    natural=pd.DataFrame(natural);save('naturally_unpolled',natural)
    save('naturally_unpolled_summary',summarize(natural[natural.cycle.ge(2016)],['scenario','model']))
    save('surprise_metrics',pd.DataFrame(surprises))
    print('MASKING AND ACCOUNTING COMPLETE',flush=True)
    # Original and blended scores, including 95% marginal coverage, no unpaired partial periods.
    score=[]
    for (sc,year),(q,m,C,bm,noise,poll,si) in fold_cache.items():
        if year==2026:continue
        for name,mu in [('Bayesian',m),('Mean-only blend',bm)]:
            rr=pd.DataFrame(scored(mu,np.sqrt(np.diag(C)),100*q.actual.to_numpy()))
            rr['target_id']=q.target_id.to_numpy();rr['cycle']=year;rr['scenario']=sc;rr['model']=name;score.append(rr)
    scores=pd.concat(score);save('scores',scores);save('score_summary',summarize(scores[scores.cycle.ge(2016)],['scenario','model']))
    accounting(out,fold_cache,roster)
    events(out,history,pd.DataFrame(surprises),read)
    if information:information_review(out,fold_cache)
    settings=dict(data_as_of='2026-09-17',sources=hashes,old_notebooks=old_notebooks,working_sha256=working_hash,
        no_refresh=True,no_promotion=True,refits='No model tuning; fixed historical poll-error posterior reconstructed from saved training arrays',
        uncertainty_note='Masking reruns the joint update from saved prior; mean-only variant inherits each masked Bayesian covariance',
        information_method='Independent-noise auxiliary observation of final margin, not literal new-poll likelihood; averaged conditional joint simulations',
        scope='One-firm means all eligible samples from the most recently available firm, chosen without outcomes')
    assert all(sha(lab/p)==h for p,h in hashes.items())
    assert all(sha(lab/p)==h for p,h in old_notebooks.items()) and sha(lab/'WORKING_MODEL.json')==working_hash
    (out/'settings.json').write_text(json.dumps(settings,indent=2)+'\n')
    (out/'audit.json').write_text(json.dumps(dict(passed=True,folds=len(fold_cache),masked_rows=len(mask),
        current_contests=35,preserved_notebooks=len(old_notebooks),checks=['Pinned source manifests','35 contests and100 unique physical seats',
        '15 posterior and joint-seat reproductions','Past-only parameter fits','Full raw aggregates and plain means reproduce',
        'No-poll plain fallback replaces hidden polls','No state polls in momentum/approval inputs','Covariance expands when observations removed',
        'Current outcomes not evaluated','Input and old notebook preservation']),indent=2)+'\n')
    shutil.copy2(__file__,out/Path(__file__).name)
    for name in ['final_information_value.py','simple_bayesian_polling.py','simple_national_model.py','simple_baselines.py',
                 'bayesian_revision2.py','calibrate_margin_uncertainty.py','plain_polling_blend.py']:
        shutil.copy2(lab/'scripts'/name,out/name)
    if information:write_report(out)
    finalize(out)
    return out


def accounting(out,cache,roster):
    q,mean,C,blend,noise,_,_=cache[('matched_live',2026)]
    fixed=int(((~roster.contested)&roster.caucus.eq('D')).sum());assert fixed==34
    rows=[]
    for model,mu in [('Bayesian',mean),('Mean-only blend',blend)]:
        wins=mu+noise>0;counts=fixed+wins.sum(1)
        for group in [[s] for s in PROXIES]+[PROXIES]:
            ids=np.flatnonzero(q.geography.isin(group));rest=counts-wins[:,ids].sum(1)
            for allocated in [0,len(ids)]:
                s=rest+allocated
                rows.append(dict(model=model,affected_states=','.join(group),allocated_D=allocated,
                    expected_D=float(s.mean()),p_D_control=float((s>=51).mean()),D_lo70=float(np.quantile(s,.15)),D_hi70=float(np.quantile(s,.85)),
                    baseline_expected_D=float(counts.mean()),baseline_p_D_control=float((counts>=51).mean()),
                    interpretation='Allocation-only bound; other races held fixed, not conditioning on a win'))
    pd.DataFrame(rows).to_parquet(out/'accounting_bounds.parquet',index=False)


def events(out,history,surprises,read):
    cols=EVENTS+['vix_3m','gpr_3m']
    assert history.groupby(['scenario','cycle'])[cols].nunique(dropna=False).le(1).all().all()
    events=history.groupby(['scenario','cycle'])[cols].first().reset_index()
    counts=history.groupby(['scenario','cycle']).agg(admitted_contests=('target_id','size'),
        polled_contests=('q_pp','count'),actual_outcomes=('actual','count')).reset_index()
    events=events.merge(counts);events['event_status']=events.extraordinary_event_any_4y.map({0.:'unflagged',1.:'flagged'}).fillna('unknown')
    events['known_components']=events[EVENTS[:3]].notna().sum(axis=1)
    events['vintage_status']='Reference-vintage proxies; historical real-time availability not certified'
    events['window_definition']='January of cycle-4 through last closed month; fixed rolling95th-percentile proxy flags'
    events.to_parquet(out/'event_support.parquet',index=False)
    raw=[]
    h=history[history.actual.notna()&history.q_pp.notna()]
    for (sc,year),g in h.groupby(['scenario','cycle']):
        err=100*g.actual-g.q_pp
        raw.append(dict(scenario=sc,cycle=year,n=len(g),mean_error_pp=err.mean(),mae_pp=err.abs().mean(),
                        same_direction_fraction=max(err.gt(0).mean(),err.lt(0).mean())))
    pd.DataFrame(raw).merge(events,on=['scenario','cycle']).to_parquet(out/'raw_poll_error_cycles.parquet',index=False)
    wide=surprises.pivot(index=['scenario','cycle','model'],columns='metric',values='value').reset_index().merge(events,on=['scenario','cycle'])
    correlations=[]
    for first in [2012,2016]:
        for (sc,model),g in wide[wide.cycle.ge(first)].groupby(['scenario','model']):
            for proxy in ['vix_3m','gpr_3m']:
                for outcome in ['median_abs_z','same_direction_fraction']:
                    f=g[['cycle',proxy,outcome]].dropna()
                    estimates=[]
                    for dropped in [None,*list(f.cycle)]:
                        v=f if dropped is None else f[f.cycle.ne(dropped)]
                        r=v[proxy].corr(v[outcome]) if len(v)>=3 and v[proxy].nunique()>1 and v[outcome].nunique()>1 else np.nan
                        estimates.append(dict(first_cycle=first,scenario=sc,model=model,proxy=proxy,outcome=outcome,
                                              omitted_cycle=dropped,n=len(v),pearson_r=r))
                    correlations.extend(estimates)
    pd.DataFrame(correlations).to_parquet(out/'stress_correlations.parquet',index=False)
    # Audit the counterintuitive 2008 negative flag directly from frozen source thresholds.
    threshold=read(FINAL+'/tables','disruption_thresholds')
    threshold[threshold.month.astype(str).str.startswith('2008')].to_parquet(out/'event_2008_threshold_audit.parquet',index=False)


def entropy(p):
    p=np.clip(np.asarray(p),0,1)
    return -(xlogy(p,p)+xlogy(1-p,1-p))/np.log(2)


def information_review(out,cache):
    # Defined below: kept separate so contract/masking can be reviewed independently.
    from final_information_value import run
    run(out,cache)


def write_report(out):
    read=lambda name:pd.read_parquet(out/(name+'.parquet'))
    score=read('score_summary');mask=read('masked_summary');natural=read('naturally_unpolled_summary')
    seats=read('chamber_scores');info=read('information_value');repeat=read('information_repeat')
    event=read('event_support');bounds=read('accounting_bounds');surprise=read('surprise_metrics')
    top=info[info.measurement.eq('calibrated_error_floor')].sort_values(['model','rank']).groupby('model').head(10).copy()
    top['control_entropy_reduction_pct']=100*top.information_bits/top.control_entropy_before
    correlations=read('stress_correlations')
    full=correlations[correlations.omitted_cycle.isna()].copy()
    keys=['first_cycle','scenario','model','proxy','outcome']
    ranges=correlations[correlations.omitted_cycle.notna()].groupby(keys).pearson_r.agg(omit_one_min='min',omit_one_max='max').reset_index()
    correlation_table=full.merge(ranges,on=keys);correlation_table.to_parquet(out/'correlation_stability.parquet',index=False)
    stability=info.merge(repeat,on=['model','state','measurement'],suffixes=('','_repeat'))
    stability['information_difference']=stability.information_bits_repeat-stability.information_bits
    stability.to_parquet(out/'information_stability.parquet',index=False)
    report='''# Final uncertainty review — results

Executed on frozen September 17, 2026 inputs. No new polling, model selection, weight search or promotion. The reference here is `repaired_both__selected`; the 50/50 mean-only polling blend inherits its covariance. The older formally designated `no_U_K1` is preserved and explicitly distinguished in the model contract.

## Main findings

1. **Missing-poll behavior is conservative, not overconfident in this test.** Hiding historical current-cycle polls worsens accuracy while widening intervals. One recently available firm recovers much of the accuracy. Masking is not random natural missingness, and this does not prove every no-poll prior is well centered.
2. **The disruption flag is not an adequate indicator of known extraordinary events.** All five recent cycles are flagged. Across 1998–2024, only 2008 and 2014 are unflagged; 2008's financial crisis is missed at these cutoffs by the strict monthly-threshold/completed-month construction. No causal or crisis-specific fat-tail conclusion is supported by this flag.
3. **Shared forecast misses and isolated large misses both occur.** In 2020 and 2024, roughly85–89% of admitted states miss in the same direction. September2022 has two standardized errors beyond3SD (Vermont and South Dakota); both winner calls are correct. These are errors relative to our forecasts, not proof of a wave relative to the preceding election, or proof of an event cause. A biased mean or too-small shared covariance can also explain coherent misses.
4. **Where more information helps depends on the model.** At the fixed effective-error benchmark, Bayesian ranking starts Alaska/Ohio/Iowa/Texas; the mean-only blend starts Colorado/West Virginia/Alaska/Iowa. The latter two unpolled-state priorities expose prior/fallback sensitivity. Close ranking differences are not precise distinctions.
5. **Four candidate-proxy cases remain unresolved.** Idaho, Montana, Nebraska and South Dakota lack validated local independent-candidate distributions. Allocation bounds quantify their effect; they are not estimates of those candidates' election chances.

## Fixed current forecasts

Expected seats use exact marginals; control and ranges use the original30,000 paired joint draws. D needs51, R controls a50–50 tie under the saved ledger convention. These numbers retain the stated candidate-proxy assumptions.

'''+seats[seats.cycle.eq(2026)].round(4).to_markdown(index=False)
    report+='\n\n## Historical reference comparison, 2016–2024\n\n140 contests per horizon. Error metrics average cycles equally; counts/correct calls pool contests. `matched_live` is September17; `oct31` is October31. Positive margin means D−R; Brier and MAE are lower-is-better. Widths are percentage points. The mean-only blend does not beat Bayesian alone on these scores.\n\n'+score.round(4).to_markdown(index=False)
    report+='\n\n## Masking historical state polls\n\nSame originally polled targets in all three rows per model/horizon:102 earlier and125 late contests over2016–2024. Each masking case removes or thins one state at a time, retains other states, and redoes the Bayesian update from its prior. Prior/historical parameter fits are fixed. The plain component uses its original historical-prior fallback when masked, never its hidden polled forecast. One firm means all eligible samples from the most recently available firm; selection uses receipt/field dates and a fixed alphabetical tie rule, not outcomes. Existing unknown-publication-date proxies are retained. National features are momentum/approval, with no hidden state-poll dependency.\n\n'+mask.round(4).to_markdown(index=False)
    report+='\n\nNaturally unpolled contests are a separate, small population (38 earlier/15 late). Their results must not be interpreted as a randomized masking experiment.\n\n'+natural.round(4).to_markdown(index=False)
    report+='\n\n## Event support and source limitation\n\nThe OR flag uses elevated health-news/VIX/GPR proxies above a past120-month95th percentile, requiring60 prior values, with January(cycle−4) through the last closed month. This is the existing inclusive calendar-year convention, not a strict48-month interval. Unknown components remain unknown unless another component is1. Historical reference vintages are not certified as available in real time.\n\n'+event[event.cycle.ge(1998)].round(3).to_markdown(index=False)
    report+='\n\nIn2008, September VIX monthly mean30.24 was below its33.76 threshold. October mean61.18 exceeded32.77, but October is not a completed reference month at the October31 forecast cutoff. The stored2008 flag therefore remains0. This is a definition/timing limitation, not proof that2008 was an ordinary election environment. Existing event flags were not changed after seeing errors.\n'
    s=surprise[surprise.model.eq('Bayesian')&surprise.cycle.ge(2016)]
    report+='\n\n## Cycle-level surprise patterns\n\nErrors are actual minus forecast. Negative signed errors mean outcomes were more Republican than our forecast. Standardization uses the original forecast SD. Simulation reference bands use the same joint covariance and admitted states for each cycle. They are exploratory diagnostics, not multiple-testing-adjusted significance results.\n\n'+s.pivot(index=['scenario','cycle'],columns='metric',values='value').round(4).to_markdown()
    report+='\n\nVIX has a positive descriptive association with typical standardized error, particularly at October31; geopolitical risk has no consistent direction across models/horizons. Only5 recent or7 full backtest cycles support these correlations. Omission ranges show instability. They do not establish a causal event effect or justify new feature weights.\n\n'+correlation_table[correlation_table.first_cycle.eq(2012)&correlation_table.model.eq('Bayesian')].round(4).to_markdown(index=False)
    report+='\n\nOlder raw-poll error comparisons are saved separately in `raw_poll_error_cycles.parquet`; they are not additional model-backtest folds.\n'
    report+='\n\n## Candidate/caucus sensitivity\n\nThe100-seat ledger and35 current physical contests reconcile; candidate identity and caucus interpretation are different checks. The exception table uses already captured public source evidence, not a fresh candidate certification. None of these four proxies supplies a validated candidate-specific probability. The bounds below remove the model allocation for the named seat(s), set them to D or R, and leave the other simulated races unchanged. This is neither conditioning on a surprising win nor assuming a national wave. Extreme all-four allocations are logical bounds, not plausible-scenario probabilities. Expected seats here are Monte Carlo means and can differ slightly from exact marginal sums.\n\n'+read('candidate_exceptions').to_markdown(index=False)
    report+='\n\n'+bounds.round(4).to_markdown(index=False)
    report+='\n\nHistorical full-chamber totals retain explicit fixed completion for2–9 unmodeled contests per cycle. State accuracy excludes those contests. The completion counts and conditional chamber CRPS/seat errors are saved in `historical_completion.parquet` and `chamber_scores.parquet`.\n'
    report+='\n\n## Value of more information\n\nThis is an auxiliary noisy observation of the final margin with independent measurement noise. It is **not** a literal new-poll likelihood: shared future polling errors and future vote drift are not explicitly modeled here. The effective SD floor is8.887pp, anchored to the median current systematic/bias uncertainty plus one fresh firm; the second quality doubles it to17.774pp. Perfect-final-margin information is the ideal limiting benchmark, numerically integrated, not something a poll can provide.\n\nWe average over both favorable and unfavorable observations. The primary criterion is expected reduction in binary Senate-control entropy; secondary is reduction in seat-count variance. A1% entropy reduction does not mean a1-point change in Democratic control odds. On average, expected seats/control odds recover the starting forecast.\n\n'+top[['model','state','rank','polled','structural_proxy','p_dem','information_bits','control_entropy_reduction_pct','seat_variance_reduction']].round(4).to_markdown(index=False)
    report+=f'\n\nAll35 states, three information qualities, two model means;8,192 scrambled quasi-Monte Carlo conditional draws and48 quadrature nodes. Top-five union repeated with independent16,384 draws and64 nodes. Maximum mean-recovery error={info.mean_recovery_error.abs().max():.6f} seats; maximum control-recovery error={100*info.control_recovery_error.abs().max():.3f} percentage points. Tiny negative information estimates near zero are numerical error and retained rather than hidden. Rankings are model-dependent; small adjacent differences are not decision-grade.\n'
    report+='\n\n## Closeout\n\nThe bounded review is complete. Keep the Bayesian reference, bias-corrected polling point benchmark, mean-only blend sensitivity and existing Student sensitivities explicitly named. No model is promoted. Remaining substantive limits are candidate/proxy interpretation, the event flag\'s meaning and timing, sparse state priors, historical feature vintages and repeated exploration of a small number of cycles.\n\nThe existing `refresh_2026.py` can acquire/prepare/align a new dataset. The recent model experiment scripts pin old artifacts; rerunning them does not automatically consume that refreshed dataset. A versioned orchestration step through the selected modeling dependencies is still needed before calling this an end-to-end live forecast refresh. This review performs no download or refresh.\n'
    (out/'RESULTS.md').write_text(report)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--lab',type=Path,default=Path(__file__).resolve().parents[1])
    p.add_argument('--skip-information',action='store_true')
    args=p.parse_args();build(args.lab,not args.skip_information)
