"""Small exact Gaussian conditional and frozen-parameter 2026 scenarios."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
from scipy.stats import norm,truncnorm
from scipy.integrate import quad
import simple_bayesian_polling as v1
import national_feature_prior as features
import simple_national_model as normal
import national_tails_waves as chamber
from current_published_review import FEATURE
DRAW_COUNT=200000
SEED=198273

def sqrt_psd(cov):
    e,Q=np.linalg.eigh((cov+cov.T)/2)
    if e.min() < -1e-8:raise ValueError('Non-positive covariance')
    return Q@np.diag(np.sqrt(np.maximum(e,0)))

def gaussian_prob(mean,cov):
    sd=np.sqrt(np.maximum(np.diag(cov),0));p=np.empty(len(mean));known=sd<1e-10
    p[~known]=norm.cdf(mean[~known]/sd[~known]);p[known]=(mean[known]>0).astype(float)
    if np.any(known&(mean==0)):raise ValueError('Exact tied election has no winner convention')
    return p

def condition_scalar(mean,cov,cross,scalar_mean,scalar_variance,value):
    if scalar_variance<=0:raise ValueError('Positive conditioning variance required')
    return mean+cross/scalar_variance*(value-scalar_mean),cov-np.outer(cross,cross)/scalar_variance

def texas_condition(mean,cov,index,direction,z,u):
    """Exact sign-event moments and quadrature probabilities; joint truncated draws."""
    mu=mean[index];var=cov[index,index];sd=np.sqrt(var);cut=-mu/sd
    lower,upper=(cut,np.inf) if direction=='D' else (-np.inf,cut)
    event=float(norm.sf(cut) if direction=='D' else norm.cdf(cut))
    if event<1e-8:raise ValueError('Conditioning event too rare for this integration')
    txmean,txvar=truncnorm.stats(lower,upper,loc=mu,scale=sd,moments='mv');cross=cov[:,index];gain=cross/var
    conditional=cov-np.outer(cross,cross)/var
    m=mean+gain*(txmean-mu);C=conditional+np.outer(gain,gain)*txvar
    xs=truncnorm.ppf(u,lower,upper,loc=mu,scale=sd)
    draws=mean+(xs-mu)[:,None]*gain+z@sqrt_psd(conditional).T;draws[:,index]=xs
    p=np.empty(len(mean))
    for j in range(len(mean)):
        if j==index:p[j]=float(direction=='D');continue
        residual_sd=np.sqrt(max(conditional[j,j],0))
        if residual_sd<1e-10:raise ValueError('Degenerate other-state conditional distribution')
        integrand=lambda t:norm.pdf(t)*norm.cdf((mean[j]+gain[j]*sd*t)/residual_sd)/event
        p[j]=quad(integrand,lower,upper,epsabs=2e-10)[0]
    return m,C,p,draws,event

def price_shock(calendar,cpi_pct=0.,gas_pct=0.):
    out=calendar.copy(deep=True)
    # Every ratio has the same unchanged historical denominator as baseline.
    for level,change,ratios in [('cpi_level',cpi_pct,['inflation_yoy_pct','cpi_24m_pct','cpi_level__pct_change_jan01','cpi_level__pct_change_previous_oct31']),('gasoline_cpi_level',gas_pct,['gasoline_yoy_pct','gasoline_cpi_level__pct_change_jan01','gasoline_cpi_level__pct_change_previous_oct31'])]:
        factor=1+change/100
        if factor<=0:raise ValueError('Positive price level required')
        out[level]=calendar[level]*factor
        for col in ratios:out[col]=100*((1+calendar[col]/100)*factor-1)
    for anchor in ['jan01','previous_oct31']:
        base='inflation_yoy_pct__start_jan01' if anchor=='jan01' else 'inflation_yoy_pct__previous_oct31'
        out['inflation_yoy_pct__change_'+anchor]=out.inflation_yoy_pct-out[base]
    return out

def build(out,lab):
    out,lab=Path(out),Path(lab)
    if (out/'scenario_seats.parquet').exists():raise FileExistsError('Use a new raw archive; do not overwrite completed scenarios')
    src=lab/'reports/national_feature_prior'/FEATURE;st=json.loads((src/'settings.json').read_text());work=Path(st['source']);up=Path(st['upstream'])
    settings=dict(source=str(src),working=str(work),upstream=str(up),sources={str(x):v1.verify(x) for x in [src,work,up]},old_notebooks={p.name:v1.sha(p) for p in lab.glob('*.ipynb') if p.name!='CURRENT_COMPARISON_AND_SCENARIOS.ipynb'},working_sha256=v1.sha(lab/'WORKING_MODEL.json'),score_config_sha256=v1.sha(features.CONFIG_PATH),draw_count=DRAW_COUNT,seed=SEED,data_as_of='2026-09-17',no_promotion=True,scenarios_are_not_new_forecasts=True)
    v1.json_write(out/'settings.json',settings);(out/'forecasts').mkdir(exist_ok=True)
    original=pd.read_parquet(src/'predictions.parquet');folds=pd.read_parquet(src/'folds.parquet');cal=pd.read_parquet(up/'calendars.parquet');roster=pd.read_parquet(up/'full_seat_ledger.parquet');roster=roster[roster.cycle.eq(2026)&roster.scenario.eq('matched_live')]
    states=[];seats=[];diagnostics=[];features_log=[];price_inputs=[];bias_log=[];checks=[]
    for family in ['none','both']:
        f=folds[folds.cycle.eq(2026)&folds.model.eq(family)].iloc[0];test=original[original.cycle.eq(2026)&original.model.eq(family)].sort_values('target_id').reset_index(drop=True)
        fit=dict(np.load(src/f.fit_path));fit['a']=float(fit['a']);V=fit['budget'];pf=dict(np.load(work/'fits/matched_live_2026_poll.npz'));poll=normal.fixed_common(pf['training_values'],pf['training_noise'],pf['training_weights'],pf['budget'],0.,9.)
        p,C,stats,meta=features.predict(test,V,poll,fit,fit['z']);m=p.prediction_pp.to_numpy();saved=np.load(src/f.forecast_path)
        checks.append(dict(name=family+'_baseline_exact',passed=bool(np.allclose(m,saved['mean'],atol=1e-9)&np.allclose(C,saved['covariance'],atol=1e-9))))
        rng=np.random.default_rng(SEED);z=rng.standard_normal((DRAW_COUNT,len(test)));u=rng.uniform(1e-12,1-1e-12,DRAW_COUNT);j=int(np.flatnonzero(test.geography.eq('TX'))[0]);cache={}
        def save(name,mean,cov,prob=None,draws=None,**extra):
            if prob is None:prob=gaussian_prob(mean,cov)
            if draws is None:draws=mean+z@sqrt_psd(cov).T
            q=test[['target_id','geography','cycle']].copy();q['model']=family;q['scenario']=name;q['prediction_pp']=mean;q['p_dem']=prob;q['sd_pp']=np.sqrt(np.maximum(np.diag(cov),0));q['actual']=np.nan
            for level in [70,95]:
                a=(1-level/100)/2;qq=np.quantile(draws,[a,1-a],axis=0);q[f'lo{level}_pp']=qq[0];q[f'hi{level}_pp']=qq[1]
            q['mean_change_pp']=mean-m;q['probability_change_pp']=100*(prob-p.p_dem.to_numpy());q['correct']=np.nan
            ss,counts=chamber.seat_summary(roster,test,q,draws);freq=np.bincount(counts,minlength=101)
            ss.update(model=family,scenario=name,p_D_control=float(np.mean(counts>=51)),D_control_mc_se=float(np.sqrt(np.mean(counts>=51)*(1-np.mean(counts>=51))/len(counts))),point_D_probability=int(ss['fixed_D']+np.sum(prob>.5)),**extra)
            states.append(q);seats.append(ss);cache[name]=(mean,cov,prob)
            err=abs(np.mean(draws>0,axis=0)-prob);se=np.sqrt(prob*(1-prob)/len(draws));checks.append(dict(name=family+'_'+name+'_marginal_MC',passed=bool(np.all(err<6*se+0.00015))))
            np.savez_compressed(out/'forecasts'/f'{family}_{name}.npz',target_ids=test.target_id.to_numpy(str),mean=mean,covariance=cov,p_dem=prob,seat_count_frequency=freq)
        save('baseline',m,C)
        for direction in ['D','R']:
            mm,cc,prob,draws,event=texas_condition(m,C,j,direction,z,u);save('texas_wins_'+direction,mm,cc,prob,draws,condition_probability=event)
        for value in [-3.,3.]:
            mm,cc=condition_scalar(m,C,C[:,j],m[j],C[j,j],value);cc[j,:]=0;cc[:,j]=0;mm[j]=value;save('texas_margin_'+str(int(value)),mm,cc,condition_margin_pp=value)
        d=cache['texas_wins_D'];r=cache['texas_wins_R'];a=p.p_dem.iloc[j]
        checks.append(dict(name=family+'_total_probability',passed=bool(np.allclose(a*d[2]+(1-a)*r[2],p.p_dem,atol=1e-8))))
        checks.append(dict(name=family+'_total_expectation',passed=bool(np.allclose(a*d[0]+(1-a)*r[0],m,atol=1e-8))))
        recovered=a*(d[1]+np.outer(d[0]-m,d[0]-m))+(1-a)*(r[1]+np.outer(r[0]-m,r[0]-m))
        checks.append(dict(name=family+'_total_covariance',passed=bool(np.allclose(recovered,C,atol=1e-7))))
        obs=np.flatnonzero(test.q_pp.notna());g=stats['N_prior_variance'];K=meta['prior_covariance'];R=meta['observation_covariance'];S=K[np.ix_(obs,obs)]+R
        cross=g*np.ones(len(test))-K[:,obs]@np.linalg.solve(S,g*np.ones(len(obs)));nv=stats['N_sd_pp']**2
        diagnostics.extend([dict(model=family,state=row.geography,national_posterior_mean_pp=stats['N_mean_pp'],national_posterior_sd_pp=stats['N_sd_pp'],national_condition_gain=cross[i]/nv,texas_condition_gain=C[i,j]/C[j,j],posterior_sd_pp=np.sqrt(C[i,i]),prior_sd_pp=np.sqrt(K[i,i]),raw_poll_pp=row.q_pp,historical_prior_pp=100*row.prior,historical_bias_pp=poll['bias_mean'][v1.STATES.index(row.geography)]) for i,row in enumerate(test.itertuples())])
        for delta in [-4.,-2.,0.,2.,4.]:
            if delta:save('wave_shift_'+str(int(delta)),m+delta,C,wave_pp=delta)
            value=stats['N_mean_pp']+delta;mm,cc=condition_scalar(m,C,cross,stats['N_mean_pp'],nv,value);save('national_known_'+str(int(delta)),mm,cc,national_offset_pp=delta,national_value_pp=value)
        for horizon in ['matched_live','oct31']:
            # Current horizon fit contains all historical residuals; October historical source is its2024 fit's source prior block, located below.
            if horizon=='matched_live':errors=pf['training_values'][np.flatnonzero(pf['years']==2024)[0]]
            else:
                #2024 observations are held-out rows, with raw aggregated poll-minus-final error at October31.
                hist=original[original.cycle.eq(2024)&original.scenario.eq('oct31')&original.model.eq('none')]
                errors=np.full(len(v1.STATES),np.nan)
                for row in hist[hist.q_pp.notna()].itertuples():errors[v1.STATES.index(row.geography)]=row.q_pp-100*row.actual
            known=np.isfinite(errors);extra=errors-poll['bias_mean'];common=float(np.nanmedian(extra));rawmedian=float(np.nanmedian(errors))
            for i in np.flatnonzero(known):bias_log.append(dict(model=family,horizon=horizon,state=v1.STATES[i],poll_minus_result_2024_pp=errors[i],already_corrected_bias_pp=poll['bias_mean'][i],remaining_2024_error_pp=extra[i],median_remaining_pp=common))
            for strength in [.5,1.]:
                scenario='error2024_'+horizon+'_'+str(strength);newpoll=dict(poll,bias_mean=poll['bias_mean']+strength*common);pp,cc,_,_=features.predict(test,V,newpoll,fit,fit['z']);save(scenario,pp.prediction_pp.to_numpy(),cc,extra_poll_bias_pp=strength*common,error_2024_raw_median_pp=rawmedian,error_reference_states=int(known.sum()))
            if horizon=='matched_live':
                increment=np.where(known,extra,common);newpoll=dict(poll,bias_mean=poll['bias_mean']+increment);pp,cc,_,_=features.predict(test,V,newpoll,fit,fit['z']);save('error2024_state_pattern',pp.prediction_pp.to_numpy(),cc,extra_poll_bias_pp=common,error_reference_states=int(known.sum()))
        design,xx,zz,_,_,_=features.prepare_design(cal[cal.scenario.eq('matched_live')],fit['years'],fit['training_weights'],2026);ids=[design.active.index(term) for term in fit['terms']]
        checks.append(dict(name=family+'_frozen_design_reproduces',passed=bool(np.allclose(zz[ids],fit['z']))));calendar=cal[cal.scenario.eq('matched_live')&cal.cycle.eq(2026)].copy()
        frozen=json.dumps(design.metadata(),sort_keys=True,default=str)
        for name,cp,gp in [('zero',0.,0.),('cpi1',1.,0.),('gas10',0.,10.),('moderate',1.,10.),('severe',2.,20.)]:
            future=price_shock(calendar,cp,gp);newX,scores=design.transform(future,require_later=True);newz=newX[0,ids];pp,cc,newstats,_=features.predict(test,V,poll,fit,newz)
            save('prices_'+name,pp.prediction_pp.to_numpy(),cc,cpi_index_increase_pct=cp,gas_index_increase_pct=gp,feature_prior_mean_pp=newstats['feature_mean_pp'],national_posterior_mean_pp=newstats['N_mean_pp'])
            if name=='zero' or family=='none':checks.append(dict(name=family+'_prices_'+name+'_identity',passed=bool(np.allclose(pp.prediction_pp,m,atol=1e-9)&np.allclose(cc,C,atol=1e-9))))
            for term,value,beta in zip(fit['terms'],newz,fit['beta_mean']):features_log.append(dict(model=family,scenario='prices_'+name,term=term,standardized_score=value,raw_score=float(scores[term].iloc[0]),coefficient_mean_pp=beta,contribution_pp=value*beta))
            for col in calendar:
                if col in design.summary.specs or col in ['cpi_level','gasoline_cpi_level','approval_3m_pct']:
                    price_inputs.append(dict(model=family,scenario='prices_'+name,component=col,before=float(calendar[col].iloc[0]),after=float(future[col].iloc[0])))
        checks.append(dict(name=family+'_normalizer_unchanged',passed=frozen==json.dumps(design.metadata(),sort_keys=True,default=str)))
        print(family,'scenarios complete',flush=True)
    for name,table in dict(scenario_states=pd.concat(states,ignore_index=True),scenario_seats=pd.DataFrame(seats),mechanics=pd.DataFrame(diagnostics),price_score_contributions=pd.DataFrame(features_log),price_inputs=pd.DataFrame(price_inputs),error2024_inputs=pd.DataFrame(bias_log),numerical_checks=pd.DataFrame(checks)).items():table.to_parquet(out/f'{name}.parquet',index=False)
    if not all(x['passed'] for x in checks):raise AssertionError([x for x in checks if not x['passed']])
    v1.manifest(out);audit(out,lab);v1.manifest(out);v1.json_write(out.parent/'latest.json',dict(artifact=out.name,manifest_sha256=v1.verify(out)));return out

def audit(out,lab):
    out,lab=Path(out),Path(lab);v1.verify(out);st=json.loads((out/'settings.json').read_text());p=pd.read_parquet(out/'scenario_states.parquet');s=pd.read_parquet(out/'scenario_seats.parquet');pub=pd.read_parquet(out/'published_states.parquet');cmp=pd.read_parquet(out/'current_comparison.parquet')
    checks=dict(source_hashes=all(v1.verify(path)==h for path,h in st['sources'].items()) and v1.sha(features.CONFIG_PATH)==st['score_config_sha256'],previous_notebooks=all(v1.sha(lab/n)==h for n,h in st['old_notebooks'].items()),working_designation=v1.sha(lab/'WORKING_MODEL.json')==st['working_sha256'],numerical_checks=bool(pd.read_parquet(out/'numerical_checks.parquet').passed.all()),unique_state_scenarios=not p.duplicated(['model','scenario','target_id']).any(),current_labels_missing=bool(p.actual.isna().all()),valid_probabilities=bool(p.p_dem.between(0,1).all()),publisher_coverage=pub.groupby('publisher').state.nunique().eq(35).all(),independent_flags=bool(cmp[~cmp.compatible].probability_difference_pp.isna().all()),raw_hashes=all(v1.sha(out/'raw'/x['file'])==x['sha256'] for x in json.loads((out/'raw/download_log.json').read_text())))
    accounting=[];covariance=[]
    for r in s.itertuples():
        q=p[p.model.eq(r.model)&p.scenario.eq(r.scenario)];a=np.load(out/'forecasts'/f'{r.model}_{r.scenario}.npz');freq=a['seat_count_frequency'];accounting.append(abs(r.expected_D_exact-r.fixed_D-q.p_dem.sum())<1e-8 and freq.sum()==DRAW_COUNT and abs(r.p_D_control-freq[51:].sum()/DRAW_COUNT)<1e-10 and r.point_D+r.point_R==100);covariance.append(np.linalg.eigvalsh(a['covariance']).min()>-1e-8)
    checks.update(seat_accounting=all(accounting),positive_semidefinite_covariance=all(covariance),publisher_probabilities=bool(pub[['p_dem','p_rep','p_ind']].sum(axis=1).sub(1).abs().lt(1e-8).all() and pub[['p_dem','p_rep','p_ind']].stack().between(0,1).all()),unique_comparisons=not cmp.duplicated(['model','publisher','state']).any());result=dict(passed=bool(all(checks.values())),checks={k:bool(x) for k,x in checks.items()},scenarios=len(s),state_rows=len(p),old_notebooks=len(st['old_notebooks']),numerical_checks=len(pd.read_parquet(out/'numerical_checks.parquet')));v1.json_write(out/'audit.json',result)
    if not result['passed']:raise AssertionError(checks)
    return result

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('out',type=Path);a=p.parse_args();build(a.out,Path(__file__).resolve().parents[1])
