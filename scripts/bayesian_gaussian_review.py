"""Readable summaries, plots and audit for the first Gaussian Bayesian notebook."""
from pathlib import Path
import json,hashlib
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from bayesian_gaussian import STATES,verify_manifest

MODEL_LABELS={'learned_covariance':'Learned state covariance','covariance_off_control':'State covariance off (control)'}

def manifest(out):
    files={str(p.relative_to(out)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(out.rglob('*')) if p.is_file() and p.name!='manifest.json'}
    (out/'manifest.json').write_text(json.dumps(files,indent=2)+'\n')

def load(out):
    out=Path(out);verify_manifest(out)
    f={p.stem:pd.read_parquet(p) for p in out.glob('*.parquet')};f['fits']=pd.DataFrame(json.loads((out/'fits.json').read_text()));return f

def performance(f,group='all'):
    q=f['metrics'].query("period=='recent_2016_2024' and group==@group").copy()
    q['Model']=q.model.map(MODEL_LABELS);q['Correct']=q.correct.astype(str)+'/'+q.n.astype(str)
    for level in [50,80,95]:q[f'{level}% interval coverage']=100*q['coverage'+str(level)]
    return q[['scenario','Model','Correct','mae_pp','brier','negative_log_density','50% interval coverage','80% interval coverage','95% interval coverage','mean_95_width_pp']].round(3)

def states(f,year=2026,scenario='matched_live'):
    q=f['predictions'].query('cycle==@year and scenario==@scenario').copy()
    base=q.query("model=='learned_covariance'").copy();control=q.query("model=='covariance_off_control'").set_index('target_id')
    return pd.DataFrame({'State':base.geography+np.where(base.target_id.str.contains('-special-'),' special',''),'Poll samples':base.n_samples.astype(int),'Prior D−R pp':100*base.prior,'Raw poll D−R pp':100*base.poll_mean,'Posterior D−R pp':base.prediction_pp,'Without covariance pp':base.target_id.map(control.prediction_pp),'D win %':100*base.p_dem,'95% low pp':base.lo95_pp,'95% high pp':base.hi95_pp,'Actual D−R pp':100*base.actual}).round(2).sort_values('State')

def cycle_scores(f):
    rows=[]
    for (s,y,m),q in f['predictions'][f['predictions'].actual.notna()].groupby(['scenario','cycle','model']):
        rows.append(dict(Horizon=s,Cycle=y,Model=MODEL_LABELS[m],Correct=f'{int(((q.p_dem>.5)==(q.actual>0)).sum())}/{len(q)}',MAE_pp=round((q.prediction_pp-100*q.actual).abs().mean(),3),Brier=round(((q.p_dem-(q.actual>0))**2).mean(),4),coverage95_pct=round(100*((100*q.actual>=q.lo95_pp)&(100*q.actual<=q.hi95_pp)).mean(),1)))
    return pd.DataFrame(rows)

def mask_scores(f):
    rows=[]
    q=f['masked_predictions'];q=q[q.actual.notna()]
    for (s,y,m),g in q.groupby(['scenario','cycle','model']):
        rows.append(dict(Horizon=s,Cycle=y,Model=MODEL_LABELS[m],States=g.geography.nunique(),Correct=f'{int(((g.p_dem>.5)==(g.actual>0)).sum())}/{len(g)}',MAE_pp=float((g.prediction_pp-100*g.actual).abs().mean()),Brier=float(((g.p_dem-(g.actual>0))**2).mean()),minimum_update_ESS=float(g.mask_importance_ess.min())))
    return pd.DataFrame(rows).round(3)

def covariance_support(f,out):
    settings=json.loads((Path(out)/'settings.json').read_text());h=pd.read_parquet(settings['source_inputs']['history']['path']);h=h[(h.base=='fixed5_8')&(h.scenario=='matched_live')&(h.cycle<2026)&h.actual.notna()&h.prior_latest_cycle.notna()]
    years={s:set(g.cycle) for s,g in h.groupby('geography')}
    q=f['correlations'].query("cycle==2026 and target_a<target_b").copy()
    q['shared_historical_cycles']=[len(years.get(s,set())&years.get(t,set())) for s,t in zip(q.state_a,q.state_b)]
    q['shared_recent_cycles']=[len((years.get(s,set())&years.get(t,set()))&set(range(2016,2026,2))) for s,t in zip(q.state_a,q.state_b)]
    return q.sort_values('prior_correlation',ascending=False).head(15)[['state_a','state_b','prior_correlation','posterior_correlation','shared_historical_cycles','shared_recent_cycles']].round(3)

def current_parameters(out):
    z=np.load(Path(out)/'chains/matched_live_2026.npz')['chains'];flat=z.reshape(-1,z.shape[-1]);n=len(STATES)
    records=[]
    for j,s in enumerate(STATES):
        l=flat[:,j];b=flat[:,n+j]
        records.append(dict(State=s,loading_mean_pp=l.mean(),loading_lo95=np.quantile(l,.025),loading_hi95=np.quantile(l,.975),poll_bias_mean_pp=b.mean(),bias_lo95=np.quantile(b,.025),bias_hi95=np.quantile(b,.975)))
    return pd.DataFrame(records).round(3)

def plot(f,out):
    out=Path(out);paths=[]
    fig,ax=plt.subplots(figsize=(7,4.5))
    for r in f['metrics'].query("period=='recent_2016_2024' and group=='all'").itertuples():
        ax.plot([50,80,95],100*np.array([r.coverage50,r.coverage80,r.coverage95]),marker='o',label=f'{r.scenario}: {MODEL_LABELS[r.model]}')
    ax.plot([45,100],[45,100],'k--',alpha=.4);ax.set(xlabel='Nominal interval coverage (%)',ylabel='Observed coverage (%)',title='Historical interval calibration: 2016–2024',xlim=(45,100),ylim=(40,102));ax.legend(fontsize=8);fig.tight_layout();p=out/'interval_calibration.png';fig.savefig(p,dpi=150);plt.close(fig);paths.append(p)
    q=f['predictions'].query("cycle==2026 and model=='learned_covariance'").sort_values('prediction_pp')
    fig,ax=plt.subplots(figsize=(8,11));y=np.arange(len(q));ax.hlines(y,q.lo95_pp,q.hi95_pp,color='#a9bacd',lw=2,label='95% interval');ax.hlines(y,q.lo50_pp,q.hi50_pp,color='#425b76',lw=5,label='50% interval');ax.scatter(q.prediction_pp,y,c=np.where(q.p_dem>.5,'#2463a8','#b34846'),s=20,zorder=3);ax.axvline(0,color='black',lw=.8);ax.set_yticks(y,q.geography);ax.set(xlabel='Final D−R margin (percentage points)',title='2026 Gaussian posterior — snapshot September 17\nConditional scalar D/R outcomes');ax.legend(loc='lower right');fig.tight_layout();p=out/'current_intervals.png';fig.savefig(p,dpi=150);plt.close(fig);paths.append(p)
    sel=['AK','CO','GA','IA','ME','MI','NC','NH','OH','TX','VA','WV'];c=f['correlations'].query('cycle==2026');fig,axes=plt.subplots(1,2,figsize=(12,5))
    for ax,col,title in zip(axes,['prior_correlation','posterior_correlation'],['Learned movement correlation','Final-margin posterior correlation']):
        mat=c.pivot(index='state_a',columns='state_b',values=col).reindex(index=sel,columns=sel);im=ax.imshow(mat,vmin=-1,vmax=1,cmap='RdBu_r');ax.set_xticks(range(len(sel)),sel,rotation=90);ax.set_yticks(range(len(sel)),sel);ax.set_title(title)
    fig.subplots_adjust(bottom=.12,top=.90,wspace=.3,right=.86);cax=fig.add_axes([.90,.20,.018,.60]);fig.colorbar(im,cax=cax,label='Correlation');p=out/'current_correlations.png';fig.savefig(p,dpi=150);plt.close(fig);paths.append(p)
    fig,ax=plt.subplots(figsize=(8,4.5))
    for model,color in [('covariance_off_control','#9a9a9a'),('learned_covariance','#326da8')]:
        d=np.load(out/'draws'/f'matched_live_2026_{model}.npz');seats=(d['margins_pp']>0).sum(axis=1)
        r=f['seat_distributions'].query('cycle==2026 and model==@model').iloc[0];fixed=round(r.expected_D-seats.mean());counts=fixed+seats
        ax.hist(counts,bins=np.arange(29.5,65.5),density=True,histtype='step',lw=2,label=MODEL_LABELS[model],color=color)
    ax.axvline(50.5,color='black',ls='--',lw=.8);ax.set(xlabel='Democratic-caucus seats, full chamber',ylabel='Probability mass',title='2026 conditional seat distribution\nBallot/caucus assumptions remain; not a certified control forecast',xlim=(37,62));ax.legend(fontsize=9);fig.tight_layout();p=out/'current_seats.png';fig.savefig(p,dpi=150);plt.close(fig);paths.append(p)
    z=np.load(out/'chains/matched_live_2026.npz')['chains'];n=len(STATES);fig,axes=plt.subplots(3,1,figsize=(9,6),sharex=True)
    for ax,j,label in zip(axes,[2*n,2*n+1,2*n+5],['Shared movement loading (pp)','Shared polling bias (pp)','Recent midterm state variance']):
        for k in range(z.shape[0]):ax.plot(np.arange(0,z.shape[1],10),z[k,::10,j],alpha=.55,lw=.65,label=f'Chain {k+1}')
        ax.set_ylabel(label,fontsize=8)
    axes[0].legend(ncol=4,fontsize=8);axes[-1].set_xlabel('Saved iteration (every tenth shown)');fig.suptitle('Current fit: posterior chain traces');fig.tight_layout();p=out/'chain_traces.png';fig.savefig(p,dpi=150);plt.close(fig);paths.append(p)
    return paths

MODEL_TEXT='''This is the first Bayesian Gaussian model, with no economic/approval inputs yet. Let p be a lagged state-result prior, theta the final D−R margin, q the **unblended** poll average, s a state and t a cycle. All inference units are percentage points.

    theta_st = p_st + lambda_s F_t + eta_st
    q_st = theta_st + b_s + B_t + R_st + epsilon_st

F_t ~ N(0,1); lambda_s ~ N(ell,2.5²); ell ~ HalfNormal(5). This fixes the factor scale and softly anchors its orientation; loadings may be negative. eta_st ~ N(0,sigma_g²). Biases b_s ~ N(mu_b,tau_b²), mu_b ~ N(0,5²). B_t ~ N(0,tau_N,g²), R_st ~ N(0,tau_R,g²). epsilon variance is 3² / max(saved effective fresh-firm weight,0.25). This is an explicit working aggregation-noise convention, NOT a claimed design-correct sampling SE. Multiple question versions are already collapsed upstream; unknown respondent overlap remains a limitation. R and B provide errors that do not vanish with more polls.

The group g crosses midterm/presidential cycles with older/recent data. At each forecast, recent means the five previous two-year cycles (last ten years). Current scales use the recent group. All older eligible outcomes remain in training; older and recent observations share loadings and state biases, but have separate noise scales. Older high-variance observations consequently carry less precision when estimating shared relationships. There is no likelihood power or arbitrary replication of sparse-state records. This assumes stable relationships across eras; it does not establish that older history improves forecasts.

Variance priors are InverseGamma(shape=3, scale): sigma² scale=200 (prior mean100), tau_N² scale=18 (mean9), tau_R² scale=32 (mean16), tau_b² scale=8 (mean4). These are regularizing modeling choices, not data-derived certainties. Known historical margins separate real movement from polling error. First neutral priors without any earlier result are excluded from movement calibration. States without local training history use the hierarchical distribution. Missing contests are unobserved, never zero.

The covariance shortcut is lambda lambda' + diagonal(sigma²). This provides a valid covariance with many fewer assumptions than an unrestricted 50-state covariance matrix, and propagates loading uncertainty. It cannot discover arbitrary regional clusters; a second factor would be a later extension. Pairs without shared history mostly borrow through the factor structure, not direct evidence.

Four conjugate Gibbs chains fit earlier cycles only. An additional joint location update improves mixing of polling biases and common shocks. Historical parameters are then updated by the marginal likelihood of forecast-date polls using importance weights, followed by exact Gaussian conditioning and joint posterior draws. This preserves feedback from observed current polls; held-out final results never enter fitting or conditioning. Rank-normalized folded split R-hat and bulk/tail ESS are reported, along with importance-weight ESS. Conditional errors are Gaussian; integrating uncertain variances yields a Gaussian mixture, not a single exactly Normal posterior.

The **covariance-off control** removes off-diagonal state-movement covariance at forecast time while preserving each draw's marginal prior variance and the common polling-error term. It uses the same historical fit; it is a controlled forecast sensitivity, NOT an independently fitted independent-state model. Covariance can change posterior means as well as uncertainty. Existing corrected-polling forecasts remain frozen benchmarks, not inputs to the new likelihood.

Historical poll averages retain upstream chronology-selected recency settings. Priors may use the explicitly labeled lagged-presidential fallback when admitted Senate history is absent. The notebook is pinned to September17,2026 inputs; it does not silently fetch a newer source. Data availability/vintage and candidate mapping limitations remain. Results from repeatedly explored historical cycles are retrospective, not untouched validation.
'''

def report(lab,out):
    lab,out=Path(lab),Path(out);f=load(out);paths=plot(f,out)
    diag=f['diagnostics'].groupby(['scenario','cycle']).agg(max_Rhat=('rhat','max'),min_bulk_ESS=('bulk_ess','min'),min_tail_ESS=('tail_ess','min')).reset_index()
    text='# First Bayesian Gaussian Senate model\n\n'+MODEL_TEXT+'\n## Recent out-of-cycle evaluation\n\n'+performance(f).to_markdown(index=False)+'\n\n## Competitive states\n\n'+performance(f,'competitive').to_markdown(index=False)+'\n\n## Fit diagnostics\n\n'+diag.round(3).to_markdown(index=False)+'\n\n## Training support\n\n'+f['fits'][['scenario','cycle','training_first_cycle','training_max_cycle','training_cycles','training_rows','polled_training_cycles','polled_training_rows']].to_markdown(index=False)+'\n\n## Current state forecasts\n\n'+states(f).to_markdown(index=False)+'\n\n## Conditional full-chamber distributions\n\n'+f['seat_distributions'].round(3).to_markdown(index=False)+'\n\n## Poll-withholding stress test\n\nAll polls for each tested state are removed together, while other states remain observed. This uses every polled state in2020,2024and2026 at available horizons. Historical actuals only score the resulting prediction. The masked diagnostics use every fifth saved MCMC draw; lower importance ESS must remain visible. This does not reproduce why real states lack polls.\n\n'+mask_scores(f).to_markdown(index=False)+'\n\n## Strongest current factor relationships, with overlap support\n\n'+covariance_support(f,out).to_markdown(index=False)+'\n\n## Limits and next steps\n\nThe current seat distributions are conditional on the scalar D/R, independent-caucus, RCV/runoff and missing-contest completion assumptions. They are not certified control probabilities. Historical unmodeled contests retain the explicit incumbent-caucus completion; accuracy scores exclude them. Report D>=51 separately from exactly50. Joint covariance uncertainty is included; election-rule uncertainty is not. Prior/noise-scale sensitivity, stationarity, possible extra movement factors, economic/approval inputs and disruption-dependent scale remain extensions. No automatic model promotion.\n\nDiagnostic references: [Stan MCMC diagnostics](https://mc-stan.org/learn-stan/diagnostics-warnings.html) and [prior/posterior predictive checks](https://mc-stan.org/docs/2_29/stan-users-guide/ppcs.html). The implementation uses NumPy/SciPy/Numba, not Stan.\n'
    (lab/'BAYESIAN_GAUSSIAN_RESULTS.md').write_text(text);(out/'BAYESIAN_GAUSSIAN_RESULTS.md').write_text(text)
    (out/Path(__file__).name).write_bytes(Path(__file__).read_bytes());manifest(out);return f,paths

def baseline_performance(out):
    settings=json.loads((Path(out)/'settings.json').read_text());q=pd.read_parquet(Path(settings['source'])/'predictions.parquet')
    q=q.query("model=='polling' and cycle>=2016 and cycle<=2024")
    return pd.DataFrame([dict(Horizon=s,Model='Frozen corrected-polling reference',Correct=f'{int(((g.prediction>0)==(g.actual>0)).sum())}/{len(g)}',MAE_pp=round(100*(g.prediction-g.actual).abs().groupby(g.cycle).mean().mean(),3)) for s,g in q.groupby('scenario')])

def prior_predictive(out):
    from scipy.stats import invgamma
    out=Path(out);q=pd.read_parquet(out/'predictions.parquet').query("cycle==2026 and model=='learned_covariance'");rng=np.random.default_rng(23019);n=len(q);d=10000
    ell=np.abs(rng.normal(0,5,d));lam=ell[:,None]+rng.normal(0,2.5,(d,n));factor=rng.normal(size=d)
    sigma=invgamma.rvs(3,scale=200,size=d,random_state=rng)
    margins=100*q.prior.to_numpy()[None,:]+lam*factor[:,None]+np.sqrt(sigma)[:,None]*rng.normal(size=(d,n))
    summary=pd.DataFrame(dict(State=q.geography,prior_center_pp=100*q.prior,prior_predictive_lo95_pp=np.quantile(margins,.025,axis=0),prior_predictive_hi95_pp=np.quantile(margins,.975,axis=0),outside_bounds_probability=np.mean(np.abs(margins)>100,axis=0)))
    summary.to_parquet(out/'prior_predictive.parquet',index=False)
    np.savez_compressed(out/'draws/prior_predictive.npz',margins_pp=margins,target_ids=q.target_id.to_numpy(str));return summary
