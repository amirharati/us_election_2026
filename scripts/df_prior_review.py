"""Student-t systematic error convolved with fixed Gaussian observation noise."""
from pathlib import Path
from datetime import datetime,timezone
import json
import numpy as np
import pandas as pd
from scipy.special import gammaln,logsumexp,ndtr
from scipy.stats import norm
from scipy.optimize import brentq
import simple_bayesian_polling as v1
import poll_update_review as review
import structured_poll_error as structured
import national_tails_waves as previous

from student_polling_likelihood import fit, summarize, joint_nll, sample, integration_check

SOURCE='20260919T212335.194601Z'
DFS=[0,2.5,3,4,5,6,8,10,20,30]
GRID=[(df,g) for df in DFS for g in [0.,2.]]
CONFIG=dict(df_choices=DFS,national_sd_pp=[0.,2.],nodes=257,log_scale_bound=16.,draws=30000,seed=197139,validation_cycles=3,as_of='2026-09-17')

def select(scores,year,g=None):
    allowed=GRID if g is None else [(df,g) for df in DFS if df]
    fallback=(0,0.) if g is None else (5,g)
    q=scores[scores.cycle.lt(year)&scores.key.isin(allowed)];years=sorted(q.cycle.unique())[-3:]
    if len(years)<3:return fallback,years,'early_fixed_fallback'
    q=q[q.cycle.isin(years)]
    if len(q)!=len(years)*len(allowed) or q.duplicated(['cycle','key']).any():raise ValueError('Incomplete past validation grid')
    vals=q.groupby('key').joint_nll.mean().to_dict()
    if not np.isfinite(list(vals.values())).all():raise ValueError('Nonfinite scores')
    key=min(vals,key=lambda x:(vals[x],DFS.index(x[0]),x[1]));return key,years,'last_three_past_cycles'


def integration_check(test,d,other):
    p=summarize(test,d,False);q=summarize(test,other,False);a=joint_nll(100*test.actual.to_numpy(),d);b=joint_nll(100*test.actual.to_numpy(),other)
    return dict(max_mean_difference_pp=float(np.max(abs(d['mean']-other['mean']))),max_probability_difference=float(np.max(abs(p.p_dem-q.p_dem))),
        relative_covariance_difference=float(np.max(abs(d['covariance']-other['covariance']))/max(1,np.max(abs(d['covariance'])))),joint_nll_difference=float(abs(a-b)) if np.isfinite(a) else 0.)


def build(lab):
    lab=Path(lab).resolve();source=lab/'reports/student_polling_likelihood'/SOURCE;sha=v1.verify(source);s=json.loads((source/'settings.json').read_text());prior=Path(s['prior_source']);upstream=Path(s['upstream']);v1.verify(prior);v1.verify(upstream)
    old=pd.read_parquet(prior/'predictions.parquet');sf=pd.read_parquet(prior/'folds.parquet');sf=sf[sf.model.eq('control_state')];roster=pd.read_parquet(upstream/'full_seat_ledger.parquet')
    out=lab/'reports/df_prior_review'/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ');out.mkdir(parents=True);(out/'forecasts').mkdir();(out/'recipe').mkdir();print('OUTPUT',out,flush=True)
    settings=dict(config=CONFIG,source=str(source),source_sha256=sha,prior_source=str(prior),prior_source_sha256=v1.verify(prior),upstream=str(upstream),upstream_sha256=v1.verify(upstream),
        old_notebook_hashes={p.name:v1.sha(p) for p in lab.glob('*.ipynb') if p.name!='DF_PRIOR_REVIEW.ipynb'},promotion=False,polling_refreshed=False)
    v1.json_write(out/'settings.json',settings);roster.to_parquet(out/'full_seat_ledger.parquet',index=False)
    predictions=[];candidates=[];scores=[];folds=[];seats=[];checks=[];tuning=[]
    for sc,group in sf.groupby('scenario'):
        for row in group.sort_values('cycle').itertuples():
            year=int(row.cycle);test=old[old.scenario.eq(sc)&old.cycle.eq(year)&old.model.eq('control_state')].sort_values('target_id').reset_index(drop=True)
            zold=np.load(prior/row.forecast_path);assert np.array_equal(zold['target_ids'],test.target_id.to_numpy(str));k=zold['prior_covariance'];poll=dict(np.load(prior/row.poll_path));bank={}
            for df,g in GRID:
                d=fit(test,k,poll,df,g);pred=summarize(test,d);bank[(df,g)]=(d,pred)
                candidates.append(pred.assign(df=df,national_sd=g,model=f'df{df}_g{g}'))
                if df:
                    high=fit(test,k,poll,df,g,nodes=513);checks.append(dict(scenario=sc,cycle=year,df=df,national_sd=g,check='double_nodes',edge_mass=d['edge_mass'],**integration_check(test,d,high)))
                    if df in [2.5,5]:
                        wider=fit(test,k,poll,df,g,nodes=321,bound=20);checks.append(dict(scenario=sc,cycle=year,df=df,national_sd=g,check='wider_domain',edge_mass=d['edge_mass'],**integration_check(test,d,wider)))
            past=pd.DataFrame([r for r in scores if r['scenario']==sc],columns=['scenario','cycle','key','joint_nll'])
            choices={'reference':((0,0.),[],'fixed'),'common2':((0,2.),[],'fixed'),'student5_g0':((5,0.),[],'fixed'),'student5_g2':((5,2.),[],'fixed')}
            for name,g in [('df_selected_g0',0.),('df_selected_g2',2.),('all_selected',None)]:
                choices[name]=select(past,year,g);key,years,status=choices[name]
                for r in past[past.cycle.isin(years)].to_dict('records'):
                    df,gg=r.pop('key');tuning.append(dict(**r,df=df,national_sd=gg,forecast_cycle=year,selector=name,selected_df=key[0],selected_g=key[1],status=status))
            for key,(d,pred) in bank.items():
                if year<2026:scores.append(dict(scenario=sc,cycle=year,key=key,joint_nll=joint_nll(100*test.actual.to_numpy(),d)))
            rng=np.random.default_rng(CONFIG['seed']+year+10000*(sc=='oct31'));z=rng.standard_normal((CONFIG['draws'],len(test)));u=rng.random(CONFIG['draws']);rr=roster[roster.scenario.eq(sc)&roster.cycle.eq(year)]
            for model,(key,years,status) in choices.items():
                d,pred=bank[key];pred=pred.assign(model=model,prior_model='control_state',df=key[0],national_sd=key[1]);predictions.append(pred)
                draws=sample(d,z,u);seat,counts=previous.seat_summary(rr,test,pred,draws);seats.append(dict(scenario=sc,cycle=year,model=model,**seat));path=f'forecasts/{sc}_{year}_{model}.npz'
                saved=dict(target_ids=test.target_id.to_numpy(str),mean=d['mean'],covariance=d['covariance'],prior_covariance=k,scales=d['scales'],weights=d['weights'],seat_count_frequency=np.bincount(counts,minlength=101))
                if year==2026:saved.update(component_means=d['means'],component_covariances=d['covs'])
                np.savez_compressed(out/path,**saved)
                folds.append(dict(scenario=sc,cycle=year,model=model,df=key[0],national_sd=key[1],scale_mean=d['scale_mean'],p_scale_gt1=d['p_scale_gt1'],log_evidence=d['log_evidence'],edge_mass=d['edge_mass'],prior_grid_mass=d['prior_grid_mass'],
                    validation_cycles=','.join(map(str,years)),status=status,training_max_cycle=row.training_max_cycle,source_forecast=row.forecast_path,source_poll=row.poll_path,forecast_path=path,joint_nll=joint_nll(100*test.actual.to_numpy(),d)))
            print(sc,year,'selected',choices['all_selected'][0],flush=True)
    p=pd.concat(predictions,ignore_index=True);ss=pd.DataFrame([{**{k:v for k,v in r.items() if k!='key'},'df':r['key'][0],'national_sd':r['key'][1]} for r in scores])
    for name,table in dict(predictions=p,candidate_predictions=pd.concat(candidates,ignore_index=True),folds=pd.DataFrame(folds),seats=pd.DataFrame(seats),scores=ss,tuning=pd.DataFrame(tuning),integration_checks=pd.DataFrame(checks),calibration=review.metrics(p)).items():table.to_parquet(out/(name+'.parquet'),index=False)
    for src in (lab/'scripts').glob('*.py'):(out/'recipe'/src.name).write_bytes(src.read_bytes())
    (out/'DF_PRIOR_REVIEW.md').write_bytes((lab/'DF_PRIOR_REVIEW.md').read_bytes());v1.manifest(out);audit(out,lab);report(out,lab);influence_review(out,lab);v1.json_write(out.parent/'latest.json',dict(artifact=out.name,manifest_sha256=v1.sha(out/'manifest.json')));return out


def audit(out,lab):
    out,lab=Path(out),Path(lab);v1.verify(out);s=json.loads((out/'settings.json').read_text());prior=Path(s['prior_source']);old=pd.read_parquet(prior/'predictions.parquet')
    p=pd.read_parquet(out/'predictions.parquet');cp=pd.read_parquet(out/'candidate_predictions.parquet');f=pd.read_parquet(out/'folds.parquet');ss=pd.read_parquet(out/'scores.parquet');ss['key']=list(zip(ss.df,ss.national_sd));seats=pd.read_parquet(out/'seats.parquet');integ=pd.read_parquet(out/'integration_checks.parquet');trace=pd.read_parquet(out/'tuning.parquet')
    c={name+'_unchanged':v1.verify(s[name])==s[name+'_sha256'] for name in ['source','prior_source','upstream']}
    c.update(old_notebooks_preserved=all(v1.sha(lab/n)==h for n,h in s['old_notebook_hashes'].items()),past_training=bool(f.training_max_cycle.lt(f.cycle).all()),past_tuning=bool(trace.cycle.lt(trace.forecast_cycle).all()),future_labels_blank=bool(p[p.cycle.eq(2026)].actual.isna().all() and cp[cp.cycle.eq(2026)].actual.isna().all()),unique_forecasts=not p.duplicated(['scenario','model','target_id']).any(),equal_cases=all(g.groupby('model').target_id.apply(frozenset).nunique()==1 for _,g in p.groupby(['scenario','cycle'])),
        complete_candidates=bool(cp.groupby(['scenario','target_id']).size().eq(len(GRID)).all() and not cp.duplicated(['scenario','target_id','df','national_sd']).any()),integration_convergence=bool(integ.max_mean_difference_pp.lt(1e-5).all() and integ.max_probability_difference.lt(1e-7).all() and integ.relative_covariance_difference.lt(1e-6).all() and integ.joint_nll_difference.lt(1e-7).all()),negligible_edge_mass=bool(integ.edge_mass.lt(1e-8).all()),finite_probabilities=bool(np.isfinite(p[['prediction_pp','posterior_sd_pp','p_dem']]).all().all() and p.p_dem.between(0,1).all()))
    reconstructed=[];ref=[];frozen=[];selected=[];candidateok=[];seatok=[];mixtureok=[]
    cols=['prediction_pp','posterior_sd_pp','p_dem','lo70_pp','hi70_pp','lo95_pp','hi95_pp'];scopes={'df_selected_g0':0.,'df_selected_g2':2.,'all_selected':None}
    for (sc,year),group in f.groupby(['scenario','cycle']):
        row=group.iloc[0];test=old[old.scenario.eq(sc)&old.cycle.eq(year)&old.model.eq('control_state')].sort_values('target_id').reset_index(drop=True);k=np.load(prior/row.source_forecast)['prior_covariance'];poll=dict(np.load(prior/row.source_poll));bank={}
        for key in GRID:
            d=fit(test,k,poll,*key);expected=summarize(test,d);bank[key]=(d,expected)
            q=cp[cp.scenario.eq(sc)&cp.cycle.eq(year)&cp.df.eq(key[0])&cp.national_sd.eq(key[1])].sort_values('target_id');ok=np.allclose(expected[cols],q[cols],atol=1e-9)
            if year<2026:
                sr=ss[ss.scenario.eq(sc)&ss.cycle.eq(year)&ss.df.eq(key[0])&ss.national_sd.eq(key[1])].iloc[0];ok=ok and abs(sr.joint_nll-joint_nll(100*test.actual.to_numpy(),d))<1e-9
            candidateok.append(ok);mixtureok.append(abs(d['weights'].sum()-1)<1e-10 and np.linalg.eigvalsh(d['covariance']).min()>0 and abs(d['prior_grid_mass']-1)<1e-8)
        for r in group.itertuples():
            d,expected=bank[(r.df,r.national_sd)];q=p[p.scenario.eq(sc)&p.cycle.eq(year)&p.model.eq(r.model)].sort_values('target_id');z=np.load(out/r.forecast_path)
            reconstructed.append(np.allclose(q[cols],expected[cols],atol=1e-9) and np.allclose(z['covariance'],d['covariance']) and np.allclose(z['weights'],d['weights']))
            frozen.append(np.array_equal(k,z['prior_covariance']) and np.array_equal(test.prior,q.prior))
            if r.model=='reference':ref.append(np.allclose(q[cols],test[cols],atol=1e-9))
            if r.model in scopes:
                key,years,status=select(ss[ss.scenario.eq(sc)],year,scopes[r.model]);selected.append(key==(r.df,r.national_sd) and ','.join(map(str,years))==r.validation_cycles and status==r.status)
            seat=seats[seats.scenario.eq(sc)&seats.cycle.eq(year)&seats.model.eq(r.model)].iloc[0]
            seatok.append(z['seat_count_frequency'].sum()==CONFIG['draws'] and abs(seat.expected_D_exact-seat.fixed_D-q.p_dem.sum())<1e-9 and seat.point_D==seat.fixed_D+(q.prediction_pp>0).sum() and seat.probability_call_D==seat.fixed_D+(q.p_dem>.5).sum())
    c.update(candidates_and_joint_scores_reconstructed=all(candidateok),reported_forecasts_reconstructed=all(reconstructed),gaussian_reference_reproduces=all(ref),historical_prior_frozen=all(frozen),selectors_reconstructed=all(selected),joint_seat_accounting=all(seatok),mixture_mass_and_covariance_valid=all(mixtureok))
    result=dict(passed=all(c.values()),checks=c,forecast_rows=len(p),candidate_rows=len(cp),integration_comparisons=len(integ));v1.json_write(out/'completion_audit.json',result)
    if not result['passed']:raise AssertionError([k for k,v in c.items() if not v])
    v1.manifest(out);return result


def report(out,lab):
    out,lab=Path(out),Path(lab);p=pd.read_parquet(out/'predictions.parquet');f=pd.read_parquet(out/'folds.parquet');seats=pd.read_parquet(out/'seats.parquet');cal=pd.read_parquet(out/'calibration.parquet');integ=pd.read_parquet(out/'integration_checks.parquet')
    rows=[]
    for (sc,y,model),q in p[p.actual.notna()].groupby(['scenario','cycle','model']):
        r=f[f.scenario.eq(sc)&f.cycle.eq(y)&f.model.eq(model)].iloc[0]
        rows.append(dict(scenario=sc,cycle=y,model=model,n=len(q),correct=int(((q.prediction_pp>0)==(q.actual>0)).sum()),mae_pp=float((100*q.actual-q.prediction_pp).abs().mean()),joint_nll=r.joint_nll,marginal_nll=float(-q.log_predictive_density.mean()),coverage70=float((100*q.actual).between(q.lo70_pp,q.hi70_pp).mean()),coverage95=float((100*q.actual).between(q.lo95_pp,q.hi95_pp).mean())))
    cycle=pd.DataFrame(rows);cycle.to_parquet(out/'cycle_scores.parquet',index=False);summary=[]
    for period,first in [('recent_2016_2024',2016),('tuned_2018_2024',2018),('all_2012_2024',2012)]:
        joint=cycle[cycle.cycle.ge(first)].groupby(['scenario','model']).joint_nll.mean().reset_index();summary.append(cal[cal.period.eq(period)&cal.group.eq('all')].merge(joint,on=['scenario','model'],validate='one_to_one'))
    summary=pd.concat(summary,ignore_index=True);summary.to_parquet(out/'summary.parquet',index=False)
    chamber=[]
    for (sc,model),q in seats[seats.cycle.between(2016,2024)].groupby(['scenario','model']):
        chamber.append(dict(scenario=sc,model=model,cycles=len(q),point_seat_mae=float((q.point_D-q.actual_D).abs().mean()),expected_seat_mae=float((q.expected_D_exact-q.actual_D).abs().mean()),coverage70=float(q.actual_D.between(q.D_lo70,q.D_hi70).mean()),coverage95=float(q.actual_D.between(q.D_lo95,q.D_hi95).mean())))
    chamber=pd.DataFrame(chamber);chamber.to_parquet(out/'chamber_scores.parquet',index=False)
    baseline=p[p.model.eq('reference')][['scenario','target_id','prediction_pp','p_dem']];changes=p.merge(baseline,on=['scenario','target_id'],suffixes=('','_reference'),validate='many_to_one');changes['shift_pp']=changes.prediction_pp-changes.prediction_pp_reference;changes['call_changed']=(changes.prediction_pp>0)!=(changes.prediction_pp_reference>0)
    matched=p[p.model.isin(['reference','common2'])][['scenario','target_id','national_sd','prediction_pp']].rename(columns={'prediction_pp':'matched_gaussian_pp'})
    changes=changes.merge(matched,on=['scenario','target_id','national_sd'],validate='many_to_one');changes['student_shift_pp']=changes.prediction_pp-changes.matched_gaussian_pp;changes['matched_call_changed']=(changes.prediction_pp>0)!=(changes.matched_gaussian_pp>0);changes.to_parquet(out/'state_changes.parquet',index=False)
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    scores=pd.read_parquet(out/'scores.parquet');profiles=scores[scores.cycle.isin([2020,2022,2024])].groupby(['scenario','df','national_sd']).joint_nll.mean().reset_index()
    profiles.to_parquet(out/'current_df_validation_profile.parquet',index=False)
    fig,axes=plt.subplots(1,2,figsize=(11,4))
    for ax,sc in zip(axes,['matched_live','oct31']):
        for g in [0.,2.]:
            curve=profiles[profiles.scenario.eq(sc)&profiles.national_sd.eq(g)&profiles.df.gt(0)].sort_values('df');ax.plot(curve.df,curve.joint_nll,marker='o',label=f'national SD {g:g}pp')
        ax.set(xscale='log',xlabel='Student degrees of freedom',ylabel='Mean past-cycle joint NLL per state',title='2020/22/24 validation: '+sc);ax.set_xticks([2.5,4,6,10,20,30],['2.5','4','6','10','20','30']);ax.legend()
    fig.tight_layout();fig.savefig(out/'df_profile.png',dpi=145);plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(12,4.5))
    for ax,sc in zip(axes,['matched_live','oct31']):
        q=summary[summary.period.eq('recent_2016_2024')&summary.scenario.eq(sc)].set_index('model')
        for model in ['reference','common2','student5_g0','student5_g2','all_selected']:ax.plot([50,70,80,95],[100*q.loc[model,'coverage'+str(n)] for n in [50,70,80,95]],marker='o',label=model)
        ax.plot([50,95],[50,95],'k--');ax.set(title='September horizon' if sc=='matched_live' else 'October31',xlabel='Nominal interval (%)',ylabel='Observed coverage (%)');ax.legend(fontsize=8)
    fig.tight_layout();fig.savefig(out/'coverage.png',dpi=145);plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(12,4))
    for ax,sc in zip(axes,['matched_live','oct31']):
        for model in ['student5_g0','student5_g2','df_selected_g2']:
            q=f[f.scenario.eq(sc)&f.model.eq(model)].sort_values('cycle');ax.plot(q.cycle,q.scale_mean,marker='o',label=model)
        ax.axhline(1,color='black',linestyle='--');ax.set(title='September horizon' if sc=='matched_live' else 'October31',xlabel='Election cycle',ylabel='Posterior systematic variance multiplier');ax.legend(fontsize=8)
    fig.tight_layout();fig.savefig(out/'scale_updates.png',dpi=145);plt.close(fig)
    cols=['scenario','model','n','correct','mae_pp','brier','marginal_nll','joint_nll','coverage70','coverage95']
    text='# Refined Student df — results\n\nFrozen September17 inputs; refined df grid2.5/3/4/5/6/8/10/20/30 plus Gaussian, national SD0/2. Last3earlier-cycle joint-NLL selection. See DF_PRIOR_REVIEW.md for the design, and PRIOR_INFLUENCE_RESULTS.md for the matched non-Bayesian comparison. No promotion.\n\n'
    for period in ['recent_2016_2024','tuned_2018_2024','all_2012_2024']:text+='## '+period+'\n\n'+summary[summary.period.eq(period)][cols].round(4).to_markdown(index=False)+'\n\n'
    text+='## Per-cycle outcomes\n\n'+cycle.round(4).to_markdown(index=False)+'\n\n'
    text+='## Selection and systematic-error scale\n\nScale is a variance multiplier. Values below1 permit more polling influence, values above1 less, conditional on the same prior. Historical priors and baseline covariance shape remain fixed.\n\n'+f[['scenario','cycle','model','df','national_sd','scale_mean','p_scale_gt1','validation_cycles','status']].round(4).to_markdown(index=False)+'\n\n'
    text+='## Recent chamber results\n\nFive cycles per horizon; existing continuing/unmodeled-seat completion assumptions remain.\n\n'+chamber.round(4).to_markdown(index=False)+'\n\n'
    text+='## Current forecasts\n\nPoint seats use posterior-mean signs; probability_call_D uses P(D)>0.5. Mixtures may distinguish them.\n\n'+seats[seats.cycle.eq(2026)][['model','point_D','point_R','probability_call_D','expected_D_exact','D_lo70','D_hi70','D_lo95','D_hi95','p_D_at_least_51','p_D_exactly_50']].round(4).to_markdown(index=False)+'\n\n'
    text+='## Current state margins\n\n'+p[p.cycle.eq(2026)].pivot(index='geography',columns='model',values='prediction_pp').round(3).to_markdown()+'\n\n'
    text+='## Numerical integration\n\n'+integ.groupby('check')[['max_mean_difference_pp','max_probability_difference','relative_covariance_difference','joint_nll_difference','edge_mass']].max().to_markdown()+'\n\n'
    text+='## Limits\n\nOne common scale provides correlated heavy errors but cannot isolate individual-state outliers. Prior/correlation/bias parameters remain estimated as before, with their estimation uncertainty largely omitted. Historical selection is chronological but extensive prior exploration makes results exploratory. Posterior scale can decrease, narrowing central intervals despite heavier tails. No conclusions should be based on current partisan direction. Review results before choosing inclusion.\n'
    (lab/'DF_PRIOR_REVIEW_RESULTS.md').write_text(text);(out/'DF_PRIOR_REVIEW_RESULTS.md').write_text(text);v1.manifest(out)




def influence(test,k,poll,d,h):
    """Exact fitted-mixture algebra; gain is not a derivative of adaptive weights."""
    obs=np.flatnonzero(test.q_pp.notna());si=np.array([v1.STATES.index(x) for x in test.geography]);so=si[obs];mu=100*test.prior.to_numpy();bias=poll['bias_mean'][si]
    fixed=poll['bias_covariance'][np.ix_(so,so)]+np.diag(16/test.firm_mass.to_numpy()[obs]);t=poll['covariance'][np.ix_(so,so)]+d['g']**2*np.ones((len(obs),len(obs)))
    gain=np.zeros((len(test),len(obs)))
    for w,s in zip(d['weights'],d['scales']):
        if w>1e-18:gain+=w*np.linalg.solve(k[np.ix_(obs,obs)]+fixed+s*t,k[obs,:]).T
    y=test.q_pp.to_numpy()[obs]-bias[obs];innov=y-mu[obs];post=mu+gain@innov
    np.testing.assert_allclose(post,d['mean'],atol=1e-9)
    h=h.set_index('target_id').loc[test.target_id].reset_index();r=test[['scenario','cycle','target_id','geography','actual','q_pp','firm_mass','history_selection_10pp']].copy()
    r['bayes_prior_pp']=mu;r['nb_prior_pp']=100*h.prior.to_numpy();r['nb_prior_fraction']=h.prior_fraction.to_numpy();r['nb_half_life']=h.poll_half_life.to_numpy();r['nb_poll_mean_pp']=100*h.poll_mean.to_numpy();r['nb_polling_pp']=100*h.poll_baseline.to_numpy();r['nb_bias_pp']=100*h.bias_prediction.to_numpy();r['nb_bias_correction_pp']=100*(h.bias_prediction-h.poll_baseline).to_numpy()
    r['bayes_bias_correction_pp']=-bias;r['corrected_poll_pp']=test.q_pp.to_numpy()-bias;r['posterior_pp']=post;r['prior_sd_pp']=np.sqrt(np.diag(k));r['own_poll_gain']=np.nan;r['own_prior_pull_pp']=np.nan;r['other_states_shift_pp']=gain@innov
    if len(obs):
        own=gain[obs,np.arange(len(obs))];r.loc[obs,'own_poll_gain']=own;r.loc[obs,'own_prior_pull_pp']=(1-own)*(mu[obs]-y)
        r.loc[obs,'other_states_shift_pp']-=own*innov
    r['undo_nb_prior_pp']=r.nb_poll_mean_pp-r.nb_polling_pp;r['aggregation_change_pp']=r.q_pp-r.nb_poll_mean_pp;r['bias_change_pp']=r.bayes_bias_correction_pp-r.nb_bias_correction_pp;r['bayes_update_pp']=post-r.corrected_poll_pp;r['gap_vs_nb_bias_pp']=post-r.nb_bias_pp
    polled=r.q_pp.notna();r['bridge_sum_pp']=r.undo_nb_prior_pp+r.aggregation_change_pp+r.bias_change_pp+r.bayes_update_pp
    np.testing.assert_allclose(r.loc[polled,'bridge_sum_pp'],r.loc[polled,'gap_vs_nb_bias_pp'],atol=1e-9)
    np.testing.assert_allclose(r.loc[polled,'bayes_update_pp'],r.loc[polled,'own_prior_pull_pp']+r.loc[polled,'other_states_shift_pp'],atol=1e-9)
    return r


def point_metrics(p):
    rows=[]
    for period,first in [('recent_2016_2024',2016),('all_2012_2024',2012)]:
        for (sc,model),g in p[p.cycle.between(first,2024)&p.actual.notna()].groupby(['scenario','model']):
            for group,mask in dict(all=np.ones(len(g),bool),polled=g.q_pp.notna(),no_polls=g.q_pp.isna(),competitive=g.history_selection_10pp.eq('competitive'),noncompetitive=g.history_selection_10pp.eq('not_selected')).items():
                q=g[mask];rows.append(dict(period=period,scenario=sc,model=model,group=group,n=len(q),correct=int(((q.prediction_pp>0)==(q.actual>0)).sum()),mae_pp=float((q.prediction_pp-100*q.actual).abs().groupby(q.cycle).mean().mean())))
    return pd.DataFrame(rows)


def influence_review(out,lab):
    out,lab=Path(out),Path(lab);settings=json.loads((out/'settings.json').read_text());prior=Path(settings['prior_source']);upstream=Path(settings['upstream']);f=pd.read_parquet(out/'folds.parquet');p=pd.read_parquet(out/'predictions.parquet');old=pd.read_parquet(prior/'predictions.parquet');h=pd.read_parquet(upstream/'history.parquet');nb=pd.read_parquet(upstream/'nonbayesian_predictions.parquet');roster=pd.read_parquet(out/'full_seat_ledger.parquet')
    ablations=[];decomp=[];seats=[];weakfolds=[];checks=[]
    for (sc,y),group in f.groupby(['scenario','cycle']):
        row=group.iloc[0];test=old[old.scenario.eq(sc)&old.cycle.eq(y)&old.model.eq('control_state')].sort_values('target_id').reset_index(drop=True);k=np.load(prior/row.source_forecast)['prior_covariance'];poll=dict(np.load(prior/row.source_poll));hh=h[h.scenario.eq(sc)&h.cycle.eq(y)]
        for base in ['reference','common2','df_selected_g2']:
            r=group[group.model.eq(base)].iloc[0];d=fit(test,k,poll,r.df,r.national_sd)
            decomp.append(influence(test,k,poll,d,hh).assign(model=base))
            if base=='common2':continue
            for scale in [2.,4.]:
                dd=fit(test,scale*k,poll,r.df,r.national_sd);pp=summarize(test,dd);name=f'{base}_K{int(scale)}';pp=pp.assign(model=name,prior_model='control_state');ablations.append(pp)
                rng=np.random.default_rng(CONFIG['seed']+y+10000*(sc=='oct31'));z=rng.standard_normal((CONFIG['draws'],len(test)));u=rng.random(CONFIG['draws']);draws=sample(dd,z,u);rr=roster[roster.scenario.eq(sc)&roster.cycle.eq(y)];seat,counts=previous.seat_summary(rr,test,pp,draws);seats.append(dict(scenario=sc,cycle=y,model=name,**seat));path=f'forecasts/{sc}_{y}_{name}.npz'
                np.savez_compressed(out/path,target_ids=test.target_id.to_numpy(str),mean=dd['mean'],covariance=dd['covariance'],prior_covariance=scale*k,seat_count_frequency=np.bincount(counts,minlength=101))
                weakfolds.append(dict(scenario=sc,cycle=y,model=name,base=base,df=r.df,national_sd=r.national_sd,K_multiplier=scale,scale_mean=dd['scale_mean'],joint_nll=joint_nll(100*test.actual.to_numpy(),dd),forecast_path=path))
                checks.append(np.array_equal(test.prior,pp.prior) and np.isfinite(pp.prediction_pp).all())
    ab=pd.concat(ablations,ignore_index=True);dec=pd.concat(decomp,ignore_index=True);extra=pd.DataFrame(seats)
    cols=['scenario','cycle','target_id','geography','actual','q_pp','n_samples','history_selection_10pp','prediction_pp','model']
    names=['prior','polling','bias','bias__momentum','bias__both','bias__selected'];n=nb[nb.model.isin(names)].copy();n['model']='nb_'+n.model
    # Exact target/label/aggregate agreement before comparison.
    base=p[p.model.eq('reference')][['scenario','target_id','actual','q_pp']];joined=n.merge(base,on=['scenario','target_id'],suffixes=('','_ref'),validate='many_to_one')
    assert len(joined)==len(n) and np.allclose(joined.actual,joined.actual_ref,equal_nan=True) and np.allclose(joined.q_pp,joined.q_pp_ref,equal_nan=True)
    pointonly=[]
    for label,col in [('same_poll_bias_only','corrected_poll_pp'),('raw30_history_fallback','q_pp')]:
        q=dec[dec.model.eq('reference')].copy();q['prediction_pp']=q[col].fillna(q.bayes_prior_pp);q['model']=label;q['n_samples']=np.nan;pointonly.append(q[cols])
    comp=pd.concat([p[cols],ab[cols],n[cols]]+pointonly,ignore_index=True);metrics=point_metrics(comp)
    det=[]
    for (sc,y,model),q in comp.groupby(['scenario','cycle','model']):
        rr=roster[roster.scenario.eq(sc)&roster.cycle.eq(y)];fixed=rr[~rr.target_id.isin(q.target_id)];assert len(fixed)+len(q)==100
        fixed_d=int(fixed.caucus.eq('D').sum());det.append(dict(scenario=sc,cycle=y,model=model,point_D=fixed_d+int(q.prediction_pp.gt(0).sum()),actual_D=int(rr.actual_caucus.eq('D').sum()) if y<2026 else np.nan))
    det=pd.DataFrame(det);ch=det[det.cycle.between(2016,2024)].assign(error=lambda x:(x.point_D-x.actual_D).abs()).groupby(['scenario','model']).agg(point_seat_mae=('error','mean'),cycles=('cycle','nunique')).reset_index()
    cyc=[]
    for (sc,y,model),q in comp[comp.actual.notna()].groupby(['scenario','cycle','model']):cyc.append(dict(scenario=sc,cycle=y,model=model,n=len(q),correct=int((q.prediction_pp.gt(0)==q.actual.gt(0)).sum()),mae_pp=float((q.prediction_pp-100*q.actual).abs().mean())))
    for name,table in dict(prior_ablations=ab,prior_ablation_folds=pd.DataFrame(weakfolds),prior_ablation_seats=extra,prior_ablation_calibration=review.metrics(ab),influence=dec,comparison_predictions=comp,comparison_metrics=metrics,comparison_seats=det,comparison_chamber_scores=ch,comparison_cycles=pd.DataFrame(cyc)).items():table.to_parquet(out/(name+'.parquet'),index=False)
    diag=dict(passed=all(checks),same_nonbayes_targets_labels_and_polls=True,exact_gap_bridge=True,exact_prior_and_other_state_split=True,ablations_preserve_centers=True,ablation_rows=len(ab))
    if not diag['passed']:raise AssertionError('Influence audit failed')
    v1.json_write(out/'influence_audit.json',diag)
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    q=dec[dec.cycle.eq(2026)&dec.model.eq('df_selected_g2')&dec.geography.isin(['AK','MI','NC','OH','TX'])].set_index('geography')
    plot=q[['undo_nb_prior_pp','aggregation_change_pp','bias_change_pp','own_prior_pull_pp','other_states_shift_pp']].rename(columns={'undo_nb_prior_pp':'Remove NB prior','aggregation_change_pp':'Poll averaging','bias_change_pp':'Bias correction difference','own_prior_pull_pp':'Own prior contrast','other_states_shift_pp':'Other states'})
    fig,ax=plt.subplots(figsize=(11,5));plot.plot.bar(ax=ax);ax.axhline(0,color='black',linewidth=.8);ax.set(ylabel='Contribution to Bayesian − non-Bayesian bias forecast (pp)',xlabel='State',title='Current forecast gap: fitted algebra, not causal attribution');ax.legend(fontsize=8);fig.tight_layout();fig.savefig(out/'gap_components.png',dpi=145);plt.close(fig)
    text='# Prior influence and non-Bayesian comparison\n\nFrozen September17 inputs, same targets/labels/polls. This isolates our model recipes; it does not verify alignment with current external forecasts. Non-Bayesian point forecasts have no calibrated intervals here. No model promotion.\n\n'
    text+='## Review findings\n\nThe refined selector choosesdf4/g2 for2026. Past2020/22/24 September validation scores atg2 are3.6157(df3),3.6136(df4),3.6156(df5): this is a shallow optimum, not a precisely estimated tail parameter. Recent per-g2 selection hasMAE6.872earlier/5.146late,128/132calls; old coarse selection was6.882/5.157,128/132. Optimization adds little. Currentdf4/g2 yields48Dpoint/48.544expected/70%47–50/95%45–52.\n\nPrior influence is substantial, but differs by state. All21currently polled states have zero explicit prior weight in the tuned non-Bayesian polling baseline; its raw mean equals the Bayesian30day mean in this cycle. Bias estimators and the Bayesian prior/cross-state update therefore drive the polled-state gap. NBbias predictsNC D+5.27/TX D+0.67/MI R+3.78; Bayesian df4/g2 predictsNC R+0.78/TX R+2.82/MI R+0.02. It is false that the Bayesian is uniformly more Republican.\n\nForNC, priorR+3.08 versus Bayesian corrected pollD+8.16 yields own-prior contrast−7.92pp and other-state shift−1.03pp, finalR+0.78. The saved prior SD is4.90pp; fitted own-poll gain0.296. ForMI, priorD+5.02 contributes+0.77pp relative to corrected pollD+2.76, while other states contribute−3.55pp; the prior center itself is not pulling Michigan Republican. NBbias is more Republican there because its correction is−6.34pp versus Bayesian+0.20pp. Gains are fitted algebra, not independent causal percentages.\n\nWeaker-prior tests confirm influence but not universal over-weighting. For refined Student/g2, multiplying K by4 moves current point seats48→52 and expected48.544→50.175; recent lateMAE worsens5.146→5.331, calls132→131, Brier worsens, while95%coverage improves90.0→93.6%. EarlierMAE worsens6.872→6.971, but95%coverage improves90.7→96.4%. Doubling K is a milder tradeoff. The Gaussian controls show the same broad pattern. More poll-driven current predictions alone do not justify a weaker prior.\n\nOn the matched recent historical cases, NBbias has lateMAE5.220/calls133 versus refined Student5.146/132; earlier NBbias7.472/127 versus Student6.872/128. Pure NBpolling is52Dpoint currently; NBbias49D; momentum or momentum+approval variants47D. Our best historical bias-corrected non-Bayesian model is not identical to the raw polling forecast. Features are excluded from these Bayesian fits.\n\n'
    text+='## Recent same-case margin and winner comparison\n\n'+metrics[metrics.period.eq('recent_2016_2024')&metrics.group.eq('all')].round(4).to_markdown(index=False)+'\n\n'
    text+='## Current state-by-state predictions\n\n'+comp[comp.cycle.eq(2026)].pivot(index='geography',columns='model',values='prediction_pp').round(3).to_markdown()+'\n\n'
    text+='## Current polled-state gap components\n\nEach contribution is in D−R margin points. Exact identity: Bayesian−NBbias = undo NBprior + change poll averaging + change bias correction + own-prior contrast + other-state update. Own gain is a fitted-mixture coefficient, not a universal prior percentage or causal derivative.\n\n'+dec[dec.cycle.eq(2026)&dec.model.eq('df_selected_g2')&dec.q_pp.notna()][['geography','nb_polling_pp','nb_bias_pp','bayes_prior_pp','bayes_bias_correction_pp','corrected_poll_pp','posterior_pp','nb_prior_fraction','own_poll_gain','undo_nb_prior_pp','aggregation_change_pp','bias_change_pp','own_prior_pull_pp','other_states_shift_pp','gap_vs_nb_bias_pp']].round(4).to_markdown(index=False)+'\n\n'
    text+='## Weaker-prior historical sensitivities\n\nK2/K4 multiply prior covariance, not its SD: prior precision is divided by2/4. Prior centers, likelihood and selected df stay fixed; Student scale weights are recomputed. These are diagnostics, not newly tuned settings.\n\n'+pd.concat([review.metrics(p),review.metrics(ab)]).query('period=="recent_2016_2024" and group=="all"')[['scenario','model','correct','mae_pp','brier','marginal_nll','coverage70','coverage95']].round(4).to_markdown(index=False)+'\n\n'
    text+='## Current point-seat totals\n\n'+det[det.cycle.eq(2026)].to_markdown(index=False)+'\n\n'
    text+='## Recent point-seat error\n\n'+ch.round(4).to_markdown(index=False)+'\n\n'
    text+='## Important distinctions\n\nNon-Bayesian polling tunes decay and an explicit prior weight; its bias model adds an empirical historical final-minus-baseline residual. Bayesian uses fixed30day aggregates, a different bias estimator, a probabilistic historical prior and cross-state updates. Priors may differ in centers as well as strength. Features are absent from the Bayesian model in this study; optional non-Bayesian momentum/approval are separate comparisons. A closer current match to conventional expectations is not validation. No-poll states still require a historical fallback or model.\n'
    (lab/'PRIOR_INFLUENCE_RESULTS.md').write_text(text);(out/'PRIOR_INFLUENCE_RESULTS.md').write_text(text);v1.manifest(out)
    audit_influence(out)


def audit_influence(out):
    out=Path(out);s=json.loads((out/'settings.json').read_text());prior=Path(s['prior_source']);base=pd.read_parquet(out/'folds.parquet');weak=pd.read_parquet(out/'prior_ablation_folds.parquet');p=pd.read_parquet(out/'prior_ablations.parquet');old=pd.read_parquet(prior/'predictions.parquet');dec=pd.read_parquet(out/'influence.parquet');seats=pd.read_parquet(out/'prior_ablation_seats.parquet')
    reconstructed=[];frozen=[];seatok=[]
    for r in weak.itertuples():
        sr=base[base.scenario.eq(r.scenario)&base.cycle.eq(r.cycle)&base.model.eq(r.base)].iloc[0];test=old[old.scenario.eq(r.scenario)&old.cycle.eq(r.cycle)&old.model.eq('control_state')].sort_values('target_id').reset_index(drop=True);k=np.load(prior/sr.source_forecast)['prior_covariance'];poll=dict(np.load(prior/sr.source_poll));d=fit(test,r.K_multiplier*k,poll,r.df,r.national_sd);expected=summarize(test,d)
        q=p[p.scenario.eq(r.scenario)&p.cycle.eq(r.cycle)&p.model.eq(r.model)].sort_values('target_id');z=np.load(out/r.forecast_path);cols=['prediction_pp','p_dem','posterior_sd_pp','lo70_pp','hi95_pp']
        reconstructed.append(np.allclose(q[cols],expected[cols],atol=1e-9) and np.allclose(z['covariance'],d['covariance']))
        frozen.append(np.array_equal(k*r.K_multiplier,z['prior_covariance']) and np.array_equal(q.prior,test.prior) and r.df==sr.df and r.national_sd==sr.national_sd)
        seat=seats[seats.scenario.eq(r.scenario)&seats.cycle.eq(r.cycle)&seats.model.eq(r.model)].iloc[0];seatok.append(abs(seat.expected_D_exact-seat.fixed_D-q.p_dem.sum())<1e-9 and z['seat_count_frequency'].sum()==CONFIG['draws'])
    pol=dec[dec.q_pp.notna()]
    c=dict(ablations_reconstructed=all(reconstructed),only_prior_covariance_changed=all(frozen),joint_seat_accounting=all(seatok),future_labels_blank=bool(p[p.cycle.eq(2026)].actual.isna().all()),exact_gap_bridge=bool(np.allclose(pol.bridge_sum_pp,pol.gap_vs_nb_bias_pp,atol=1e-9)),exact_prior_other_state_split=bool(np.allclose(pol.bayes_update_pp,pol.own_prior_pull_pp+pol.other_states_shift_pp,atol=1e-9)))
    nb=pd.read_parquet(Path(s['upstream'])/'nonbayesian_predictions.parquet');nb=nb[nb.model.eq('bias')]
    ref=old[old.model.eq('control_state')][['scenario','target_id','actual','q_pp']]
    joined=nb.merge(ref,on=['scenario','target_id'],suffixes=('','_ref'),validate='one_to_one')
    c['same_nonbayes_targets_labels_and_polls']=bool(len(joined)==len(nb) and np.allclose(joined.actual,joined.actual_ref,equal_nan=True) and np.allclose(joined.q_pp,joined.q_pp_ref,equal_nan=True))
    result=dict(passed=all(c.values()),checks=c,ablation_rows=len(p));v1.json_write(out/'influence_audit.json',result)
    if not result['passed']:raise AssertionError(c)
    v1.manifest(out);return result


if __name__=='__main__':build(Path(__file__).resolve().parents[1])
