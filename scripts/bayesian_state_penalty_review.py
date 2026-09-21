"""Review tables, figures and provenance/forecast audits for state prior penalties."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
from scipy.stats import norm
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import bayesian_state_penalty as model
import simple_bayesian_polling as v1


def load(out):
    v1.verify(out);return {p.stem:pd.read_parquet(p) for p in Path(out).glob('*.parquet')}


def performance(f,group='all',period='recent_2016_2024'):
    g=f['metrics'].query('group==@group and period==@period').copy()
    g['Model']=g.model.map(model.LABELS);g['Correct']=g.correct.astype(str)+'/'+g.n.astype(str);g['Coverage95_pct']=100*g.coverage95
    return g[['scenario','Model','Correct','mae_pp','brier','Coverage95_pct','mean95_width_pp']].round(3)


def cycles(f):
    rows=[]
    for (s,y,m),g in f['predictions'].query('cycle<2026').groupby(['scenario','cycle','model']):
        rows.append(dict(Horizon=s,Cycle=y,Model=model.LABELS[m],N=len(g),Correct=int(((g.prediction_pp>0)==(g.actual>0)).sum()),
                         MAE_pp=float(abs(g.prediction_pp-100*g.actual).mean()),Marginal_NLPD=float(-g.log_predictive_density.mean()) if g.log_predictive_density.notna().all() else np.nan))
    return pd.DataFrame(rows).round(3)


def states(f,family='decay',year=2026,scenario='matched_live'):
    q=f['predictions'].query('cycle==@year and scenario==@scenario');base=q[q.model.eq(f'v4_{family}_state')].set_index('target_id')
    z=f['state_penalties'].query('cycle==@year and scenario==@scenario and family==@family').set_index('state')
    t=pd.DataFrame(dict(State=base.geography+np.where(base.special,' special',''),Actual_pp=100*base.actual,Prior_pp=100*base.prior,
                        Raw_poll_pp=base.q_pp,State_penalty_pp=base.prediction_pp,D_probability=base.p_dem,
                        Low95_pp=base.lo95_pp,High95_pp=base.hi95_pp,Variance_multiplier=base.variance_multiplier,
                        Penalty_strength=base.prior_penalty_strength))
    for mode in ['fixed','tuned']:
        t[f'{mode}_pp']=q[q.model.eq(f'v3_{family}_{mode}')].set_index('target_id').prediction_pp
    t['Recent_validation_n']=base.geography.map(z.validation_n);t['Shared_fallback']=base.geography.map(z.validation_n).eq(0)
    return t.reset_index().sort_values('State').round(3)


def seats(f,out):
    settings=json.loads((Path(out)/'settings.json').read_text());old=pd.read_parquet(Path(settings['source'])/'seat_comparison.parquet')
    q=f['seats'];t=pd.DataFrame(dict(Horizon=q.scenario,Cycle=q.cycle,Model=q.model.map(model.LABELS),D=q.point_D,R=q.point_R,
                                   Actual_D=q.actual_D,Expected_D=q.expected_D_exact,D_low70=q.D_lo70,D_high70=q.D_hi70,
                                   D_low95=q.D_lo95,D_high95=q.D_hi95,D_at_least_51=q.p_D_at_least_51,
                                   Unmodeled_contest_completions=q.unmodeled_contested))
    return pd.concat([t,old],ignore_index=True).round(3)


def withholding(f,out):
    source=Path(json.loads((Path(out)/'settings.json').read_text())['source']);old=pd.read_parquet(source/'masked_predictions.parquet')
    q=pd.concat([f['masked_predictions'],old],ignore_index=True);rows=[]
    for (s,y,m),g in q.query('cycle<2026').groupby(['scenario','cycle','model']):
        rows.append(dict(Horizon=s,Cycle=y,Model=model.LABELS[m],N=len(g),MAE_pp=float(abs(g.prediction_pp-100*g.actual).mean()),Correct=int(((g.prediction_pp>0)==(g.actual>0)).sum())))
    return pd.DataFrame(rows).round(3)


def audit(f,out,lab):
    out,lab=Path(out),Path(lab);settings=json.loads((out/'settings.json').read_text());source=Path(settings['source']);checks={}
    checks['frozen_revision3_unchanged']=v1.verify(source)==settings['source_manifest_sha256']
    checks['original_inputs_unchanged']=all(v1.sha(p)==s for p,s in settings['provenance']['paths'].items())
    checks['previous_notebooks_unchanged']=all(v1.sha(lab/p)==s for p,s in settings['old_notebook_hashes'].items())
    checks['used_frozen_components_unchanged']=all(v1.sha(source/r.path)==r.sha256 for r in f['used_components'].itertuples())
    u=f['used_components'];checks['component_fits_past_only']=bool((u.training_max_cycle<u.cycle).all())
    folds=f['folds'];checks['outer_fits_past_only']=bool((folds.training_max_cycle<folds.cycle).all())
    t=f['local_tuning'];checks['local_tuning_past_only']=bool(((t.fit_max_cycle<t.validation_cycle)&(t.validation_cycle<t.forecast_cycle)).all())
    grouped=['scenario','forecast_cycle','family'];last=t.groupby(grouped).validation_cycle.transform('max')
    checks['recent_weights_reconstructed']=bool(np.allclose(t.weight,np.exp2(-(last-t.validation_cycle)/model.CONFIG['recent_half_life_years'])))
    checks['marginal_log_scores_reconstructed']=bool(np.allclose(t.nld,-norm.logpdf(t.actual_pp,t.prediction_pp,t.sd_pp)))
    profile=f['state_penalties'];checks['fallback_exact']=bool((profile.loc[profile.validation_n.eq(0),'variance_multiplier']==profile.loc[profile.validation_n.eq(0),'shared_multiplier']).all())
    lower=profile[['shared_multiplier','raw_multiplier']].min(axis=1);upper=profile[['shared_multiplier','raw_multiplier']].max(axis=1)
    checks['state_scales_shrink_toward_shared']=bool(((profile.variance_multiplier>=lower-1e-12)&(profile.variance_multiplier<=upper+1e-12)&profile.local_fraction.between(0,1,inclusive='left')).all())
    checks['penalty_is_inverse_variance_multiplier']=bool(np.allclose(profile.penalty_strength,1/profile.variance_multiplier))
    reconstructed=[]
    for (s,y,family),g in profile.groupby(['scenario','cycle','family']):
        surf=t[t.scenario.eq(s)&t.forecast_cycle.eq(y)&t.family.eq(family)]
        _,p=model.shrink_state_scores(surf,float(g.shared_multiplier.iloc[0]),int(y))
        reconstructed.append(np.allclose(p.set_index('state').sort_index().variance_multiplier,g.set_index('state').sort_index().variance_multiplier))
    checks['all_state_selections_reconstructed']=all(reconstructed)
    checks['shared_scalar_control_exact']=bool((folds.shared_control_max_error_pp<1e-9).all())
    pred=f['predictions'];new=pred[pred.model.isin(model.MODELS)];old=pd.read_parquet(source/'predictions.parquet')
    retained=pred[pred.model.isin(old.model.unique())];keys=['scenario','cycle','model','target_id']
    pd.testing.assert_frame_equal(retained[old.columns].sort_values(keys).reset_index(drop=True),old.sort_values(keys).reset_index(drop=True),check_dtype=False)
    checks['all_frozen_predictions_retained_exactly']=True
    checks['same_comparison_cases']=all(len({tuple(sorted(g.target_id)) for _,g in block.groupby('model')})==1 for _,block in pred.groupby(['scenario','cycle']))
    checks['finite_predictions_and_probabilities']=bool(np.isfinite(new[['prediction_pp','posterior_sd_pp','p_dem','lo95_pp','hi95_pp']]).all().all() and new.p_dem.between(0,1).all())
    covchecks=[];predchecks=[];mc=[];scales=[];corrs=[];sameinputs=[]
    for row in folds.itertuples():
        s,y,family=row.scenario,row.cycle,row.family;m=f'v4_{family}_state';g=new[new.scenario.eq(s)&new.cycle.eq(y)&new.model.eq(m)]
        z=np.load(out/'draws'/f'{s}_{y}_{m}.npz');g=g.set_index('target_id').loc[z['target_ids']].reset_index()
        mov=np.load(source/row.movement_path);poll=np.load(source/row.poll_path)
        p,c,meta=model.state_predict(g,dict(covariance=mov['covariance']),dict(covariance=poll['covariance'],bias_mean=poll['bias_mean'],bias_covariance=poll['bias_covariance']),z['multipliers_all_states'])
        predchecks.append(np.allclose(p.prediction_pp,g.prediction_pp,atol=1e-10) and np.allclose(c,z['covariance_pp2']))
        covchecks.append(np.linalg.eigvalsh(c).min()>0 and np.linalg.eigvalsh(meta['prior_covariance']).min()>0)
        ix=[model.v2.STATES.index(x) for x in g.geography];raw=mov['covariance'][np.ix_(ix,ix)];scaled=z['prior_covariance_pp2'];a=z['multipliers_all_states'][ix]
        scales.append(np.allclose(scaled,raw*np.sqrt(np.outer(a,a))))
        corrs.append(np.allclose(raw/np.sqrt(np.outer(np.diag(raw),np.diag(raw))),scaled/np.sqrt(np.outer(np.diag(scaled),np.diag(scaled)))))
        se=g.posterior_sd_pp.to_numpy()/np.sqrt(len(z['margins_pp']));mc.append(np.all(abs(z['margins_pp'].mean(axis=0)-g.prediction_pp.to_numpy())<6*se+.02))
        control=old[old.scenario.eq(s)&old.cycle.eq(y)&old.model.eq(f'v3_{family}_fixed')].set_index('target_id').loc[g.target_id]
        sameinputs.append(np.allclose(g[['prior','actual','q_pp','firm_mass','sample_count']],control[['prior','actual','q_pp','firm_mass','sample_count']],equal_nan=True))
    checks['all_forecasts_reconstructed']=all(predchecks);checks['positive_prior_and_posterior_covariances']=all(covchecks)
    checks['diagonal_congruence_scaling_correct']=all(scales);checks['prior_correlations_preserved']=all(corrs)
    checks['joint_draws_match_analytic_means']=all(mc);checks['means_outcomes_polls_unchanged']=all(sameinputs)
    result=dict(passed=all(checks.values()),checks=checks,new_forecasts=len(new),outer_folds=len(folds)//3,state_profiles=len(profile),
                local_candidate_scores=len(t),reused_component_fits=len(u),new_covariance_fits=0,
                max_outside_bounds_historical=float(new[new.cycle.lt(2026)].outside_margin_bounds_probability.max()),
                max_outside_bounds_current=float(new[new.cycle.eq(2026)].outside_margin_bounds_probability.max()),selection_uncertainty_included=False)
    v1.json_write(out/'completion_audit.json',result)
    if not result['passed']:raise AssertionError(result)
    return result


def plots(f,out):
    out=Path(out);paths=[];q=f['metrics'].query('period=="recent_2016_2024" and group=="all"')
    fig,axes=plt.subplots(1,2,figsize=(13,5));colors=['#9ab1bc','#438096','#bd8253']
    for ax,scenario in zip(axes,['matched_live','oct31']):
        for j,(mode,color) in enumerate(zip(['fixed','tuned','state'],colors)):
            keys=[f'v4_{family}_state' if mode=='state' else f'v3_{family}_{mode}' for family in model.FAMILIES]
            g=q[q.scenario.eq(scenario)].set_index('model').loc[keys]
            ax.bar(np.arange(3)+(j-1)*.23,g.mae_pp,width=.23,label={'fixed':'Fixed','tuned':'Shared','state':'State + fallback'}[mode],color=color)
        ax.set_xticks(range(3),model.FAMILIES);ax.set(title=scenario,ylabel='MAE (pp), equal cycle weight');ax.legend(fontsize=8)
    fig.suptitle('2016–2024: does state-specific prior strength help?');fig.tight_layout();paths.append(out/'performance.png');fig.savefig(paths[-1],dpi=145);plt.close(fig)
    q=f['state_penalties'].query('cycle==2026 and family=="decay"').sort_values('variance_multiplier')
    fig,ax=plt.subplots(figsize=(10,10));y=np.arange(len(q));ax.scatter(q.raw_multiplier,y,marker='x',color='#b58c60',label='Raw state preference');ax.scatter(q.variance_multiplier,y,color='#26758e',label='Shrunk state multiplier');ax.axvline(q.shared_multiplier.iloc[0],color='black',ls=':',label='Shared fallback')
    ax.set_xscale('log',base=2);ax.set_xticks(model.CONFIG['variance_candidates'],model.CONFIG['variance_candidates']);ax.set_yticks(y,q.state);ax.tick_params(axis='y',labelsize=8);ax.set(xlabel='Prior variance multiplier; smaller means stronger prior',title='2026 decay prior: state preferences shrink toward shared strength');ax.legend(fontsize=8);fig.tight_layout();paths.append(out/'current_state_penalties.png');fig.savefig(paths[-1],dpi=145);plt.close(fig)
    q=f['state_penalties'].query('cycle==2026 and family=="decay"');fig,ax=plt.subplots(figsize=(8,4.5));ax.scatter(q.recent_mass,q.local_fraction,color='#327e96');xx=np.linspace(0,2.5,100);ax.plot(xx,xx/(xx+model.CONFIG['shrinkage_mass']),color='#a08467',label='m / (m + 2)');ax.set(xlabel='Available recent validation weight',ylabel='Fraction of local log-scale estimate retained',title='Sparse evidence stays close to the shared fallback');ax.legend();fig.tight_layout();paths.append(out/'shrinkage.png');fig.savefig(paths[-1],dpi=145);plt.close(fig)
    q=f['predictions'].query('cycle==2026 and model=="v4_decay_state"').sort_values('prediction_pp');fig,ax=plt.subplots(figsize=(10,10));y=np.arange(len(q));ax.hlines(y,q.lo95_pp,q.hi95_pp,color='#abc2cd',lw=2);ax.hlines(y,q.lo70_pp,q.hi70_pp,color='#2b7791',lw=4);ax.scatter(q.prediction_pp,y,s=18,color='#1d3c4f');ax.axvline(0,color='black',lw=.7);ax.set_yticks(y,q.geography+np.where(q.special,' special',''));ax.set(xlabel='D−R margin (pp); 70% and 95% intervals',title='2026 decay prior with state-specific strength — frozen September 17');fig.tight_layout();paths.append(out/'current_ranges.png');fig.savefig(paths[-1],dpi=145);plt.close(fig)
    return paths


def report(lab,out):
    lab,out=Path(lab),Path(out);f=load(out);a=audit(f,out,lab);paths=plots(f,out)
    chamber=seats(f,out);chamber.to_parquet(out/'seat_comparison.parquet',index=False);cycles(f).to_parquet(out/'cycle_scores.parquet',index=False)
    frames=[]
    for family in model.FAMILIES:
        for s,y in f['folds'][['scenario','cycle']].drop_duplicates().itertuples(index=False,name=None):frames.append(states(f,family,int(y),s).assign(Family=family,Cycle=y,Horizon=s))
    pd.concat(frames,ignore_index=True).to_parquet(out/'all_state_tables.parquet',index=False)
    text='# State-specific prior strength — results\n\n'
    text+='Notebook: `BAYESIAN_STATE_PENALTY.ipynb`. Design: `BAYESIAN_STATE_PENALTY.md`. Three new state-shrunk variants reuse exact Revision 3 prior means, fitted covariance/poll-error components and frozen September 17, 2026 data. No new downloads or covariance fits. Smaller variance multiplier means stronger prior; precision strength is its reciprocal.\n\n'
    text+='The shared fallback is learned from the last three earlier cycles. State preferences use the same cycles, with four-year recency weighting, then shrink on log scale with two pseudo-results. This is two-stage tuning, not a posterior over 50 parameters or a joint optimum. Covariance is scaled by D C D, retaining correlations.\n\n'
    for title,group in [('Recent performance','all'),('Competitive states','competitive'),('Noncompetitive states','noncompetitive')]:
        text+=f'## {title}\n\n2016–2024. MAE averages cycles equally; correct calls pool the same contests.\n\n'+performance(f,group).to_markdown(index=False)+'\n\n'
    text+='## Recent evidence and state penalties for 2026\n\nA zero evidence count means exact shared fallback. Local fraction is the weight on the raw state log multiplier; the remaining fraction stays shared. These training scores are not held-out performance estimates.\n\n'+f['state_penalties'].query('cycle==2026').round(4).to_markdown(index=False)+'\n\n'
    text+='## By historical cycle\n\n'+cycles(f).to_markdown(index=False)+'\n\n'
    for family in model.FAMILIES:text+=f'## Current states: {family} prior\n\n'+states(f,family).to_markdown(index=False)+'\n\n'
    text+='## Full chamber totals\n\nD includes mapped Democratic-caucusing independents. Point totals count margin signs; expected totals sum probabilities. Existing unmodeled-contest completion and ballot assumptions remain.\n\n'+chamber.to_markdown(index=False)+'\n\n'
    text+='## Withheld-state polling stress test\n\n'+withholding(f,out).to_markdown(index=False)+'\n\n'
    text+='## Audit\n\n'+pd.DataFrame([dict(Check=k,Passed=v) for k,v in a['checks'].items()]).to_markdown(index=False)+'\n\n'
    text+=f'## Limits\n\nNo automatic model promotion. Covariance and penalty-selection uncertainty are excluded from intervals. Maximum Gaussian mass beyond physical margin bounds: {100*a["max_outside_bounds_historical"]:.2f}% historically, {100*a["max_outside_bounds_current"]:.2f}% currently across the new variants. Sparse race histories, existing outcome-admission exclusions and candidate/seat changes remain. Examine horizon, cycle and competitive-state results before treating a retrospective gain as general.\n'
    (lab/'BAYESIAN_STATE_PENALTY_RESULTS.md').write_text(text);(out/'BAYESIAN_STATE_PENALTY_RESULTS.md').write_text(text)
    (out/Path(__file__).name).write_bytes(Path(__file__).read_bytes());v1.manifest(out)
    v1.json_write(out.parent/'latest.json',dict(artifact=out.name,manifest_sha256=v1.sha(out/'manifest.json')))
    return f,paths,a


if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('out',type=Path);p.add_argument('--lab',type=Path,default=Path(__file__).resolve().parents[1]);a=p.parse_args();report(a.lab,a.out)
