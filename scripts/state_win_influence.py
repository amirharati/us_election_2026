"""Condition saved forecasts on TX/SC wins; separate rarity and covariance."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
from scipy.stats import norm
import simple_bayesian_polling as v1
import national_feature_prior as feat
import simple_national_model as normal
from current_conditional_scenarios import texas_condition


def national_cross(test,budget,poll,fit,z):
    si=np.array([v1.STATES.index(s) for s in test.geography]);obs=np.flatnonzero(test.q_pp.notna());so=si[obs];g=fit['a']+float(z@fit['beta_covariance']@z)
    K=np.diag(budget[si]-fit['a'])+g*np.ones((len(si),len(si)))
    R=poll['covariance'][np.ix_(so,so)]+poll['bias_covariance'][np.ix_(so,so)]+np.diag(16/test.firm_mass.to_numpy()[obs]);S=K[np.ix_(obs,obs)]+R
    return g*(np.ones(len(si))-K[:,obs]@np.linalg.solve(S,np.ones(len(obs))))


def build(out,lab,include_repaired=False):
    out,lab=Path(out),Path(lab);src=lab/'reports/national_feature_prior/20260920T013619.322700Z';work=lab/'reports/simple_national_model/20260920T000314.601869Z'
    runs=[];p=pd.read_parquet(src/'predictions.parquet');f=pd.read_parquet(src/'folds.parquet')
    for family in ['none','both']:
        r=f[f.cycle.eq(2026)&f.model.eq(family)].iloc[0];q=p[p.cycle.eq(2026)&p.model.eq(family)].sort_values('target_id').reset_index(drop=True);runs.append((family+'__baseline',q,dict(np.load(src/r.fit_path))))
    if include_repaired:
        p=pd.read_parquet(out/'predictions.parquet');f=pd.read_parquet(out/'folds.parquet')
        for family in ['none','both']:
            r=f[f.cycle.eq(2026)&f.model.eq(family+'__selected')].iloc[0];q=p[p.cycle.eq(2026)&p.model.eq(family+'__selected')].sort_values('target_id').reset_index(drop=True);runs.append((family+'__selected',q,dict(np.load(out/r.fit_path))))
    pf=np.load(work/'fits/matched_live_2026_poll.npz');poll=normal.fixed_common(pf['training_values'],pf['training_noise'],pf['training_weights'],pf['budget'],0.,9.);rows=[];summary=[];checks=[]
    for model,q,fit in runs:
        fit['a']=float(fit['a']);p,C,stats,_=feat.predict(q,fit['budget'],poll,fit,fit['z']);m=p.prediction_pp.to_numpy();prob=p.p_dem.to_numpy();cross=national_cross(q,fit['budget'],poll,fit,fit['z']);rng=np.random.default_rng(198273);z=rng.standard_normal((200000,len(q)));u=rng.uniform(1e-12,1-1e-12,len(z))
        joint=np.block([[C,cross[:,None]],[cross[None,:],np.array([[stats['N_sd_pp']**2]])]]);checks.append(dict(name=model+'_joint_covariance',passed=bool(np.linalg.eigvalsh(joint).min()>-1e-8)))
        for state in ['TX','SC']:
            j=int(np.flatnonzero(q.geography.eq(state))[0]);outcomes={}
            for party in ['D','R']:
                mm,cc,pr,draws,event=texas_condition(m,C,j,party,z,u);delta=mm[j]-m[j];Nshift=cross[j]/C[j,j]*delta;own=float(pr[j]-prob[j]);others=float((pr-prob).sum()-own)
                summary.append(dict(model=model,condition_state=state,winner=party,event_probability=event,baseline_margin_pp=m[j],baseline_sd_pp=np.sqrt(C[j,j]),conditioned_margin_pp=mm[j],margin_surprise_pp=delta,baseline_N_pp=stats['N_mean_pp'],N_sd_pp=stats['N_sd_pp'],national_covariance_pp2=cross[j],national_gain=cross[j]/C[j,j],national_shift_pp=Nshift,own_expected_seat_change=own,other_expected_seat_change=others,total_expected_seat_change=own+others,mean_other_margin_shift_pp=np.delete(mm-m,j).mean(),max_other_probability_shift_pp=np.max(abs(np.delete(100*(pr-prob),j)))))
                a=q[['target_id','geography']].copy();a=a.assign(model=model,condition_state=state,winner=party,baseline_margin_pp=m,conditional_margin_pp=mm,margin_shift_pp=mm-m,baseline_p_dem=prob,conditional_p_dem=pr,probability_shift_pp=100*(pr-prob),covariance_with_condition_pp2=C[:,j],regression_gain=C[:,j]/C[j,j],correlation_with_condition=C[:,j]/np.sqrt(np.diag(C)*C[j,j]));rows.append(a);outcomes[party]=(mm,cc,pr,event)
                se=np.sqrt(pr*(1-pr)/len(z));checks.append(dict(name=model+'_'+state+'_'+party+'_MC',passed=bool(np.all(abs((draws>0).mean(0)-pr)<6*se+.00015))))
            md,cd,pd_,a=outcomes['D'];mr,cr,pr_,b=outcomes['R'];cavg=a*(cd+np.outer(md-m,md-m))+b*(cr+np.outer(mr-m,mr-m));checks.append(dict(name=model+'_'+state+'_total_probability_moments',passed=bool(np.allclose(a*md+b*mr,m)&np.allclose(cavg,C)&np.allclose(a*pd_+b*pr_,prob,atol=1e-8))))
    for name,table in dict(influence_states=pd.concat(rows,ignore_index=True),influence_summary=pd.DataFrame(summary),influence_checks=pd.DataFrame(checks)).items():table.to_parquet(out/f'{name}.parquet',index=False)
    if not all(x['passed'] for x in checks):raise AssertionError(checks)
    print(pd.DataFrame(summary).round(5).to_string(index=False));return pd.DataFrame(summary)
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('artifact',type=Path);p.add_argument('--include-repaired',action='store_true');a=p.parse_args();build(a.artifact,Path(__file__).resolve().parents[1],a.include_repaired)
