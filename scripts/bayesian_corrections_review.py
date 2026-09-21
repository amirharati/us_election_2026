"""Paired review of Bayesian bias ablations and shared feature surprises."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from bayesian_corrections import LABELS,PRIMARY,FEATURES
from bayesian_gaussian_review import manifest
from bayesian_gaussian import verify_manifest


def load(out):
    out=Path(out);verify_manifest(out);f={p.stem:pd.read_parquet(p) for p in out.glob('*.parquet')}
    f['fits']=pd.DataFrame(json.loads((out/'fits.json').read_text()));return f


def performance(f,group='all',controls=False):
    models=list(LABELS) if controls else PRIMARY;rows=[]
    for m in models:
        row={'Model':LABELS[m]}
        for s,name in [('matched_live','Sep17'),('oct31','Oct31')]:
            r=f['metrics'].query("scenario==@s and model==@m and period=='recent_2016_2024' and group==@group").iloc[0]
            row[name+' calls']=f'{r.correct}/{r.n}';row[name+' MAE pp']=round(r.mae_pp,3);row[name+' Brier']=round(r.brier,4);row[name+' 95% coverage']=round(100*r.coverage95,1)
        rows.append(row)
    return pd.DataFrame(rows)


def bias_table(f,year=2026,scenario='matched_live'):
    q=f['components'].query("cycle==@year and scenario==@scenario and model=='original'").copy()
    return q[['state','n_samples','raw_poll_pp','legacy_regularization_pull_pp','legacy_bias_correction_pp','legacy_corrected_poll_pp','history_bayesian_bias_correction_pp','updated_bayesian_bias_correction_pp']].round(3).sort_values('state')


def states(f,year=2026,scenario='matched_live'):
    p=f['predictions'].query('cycle==@year and scenario==@scenario');m=p.pivot(index='target_id',columns='model',values='prediction_pp');prob=p.pivot(index='target_id',columns='model',values='p_dem')
    b=p[p.model.eq('original')].set_index('target_id');rows=[]
    for target,r in b.iterrows():
        row={'State':r.geography+(' special' if '-special-' in target else ''),'Poll samples':int(r.n_samples),'Prior pp':100*r.prior,'Raw poll pp':100*r.poll_mean,'Actual pp':100*r.actual}
        for model in ['original','bias_off_refit','features']:
            row[LABELS[model]+' pp']=m.loc[target,model];row[LABELS[model]+' D%']=100*prob.loc[target,model]
        rows.append(row)
    return pd.DataFrame(rows).round(2).sort_values('State')


def cycles(f):
    rows=[]
    for (scenario,year),p in f['predictions'][f['predictions'].actual.notna()].groupby(['scenario','cycle']):
        row={'Horizon':scenario,'Cycle':year}
        for model in PRIMARY:
            q=p[p.model.eq(model)];row[LABELS[model]+' calls']=f'{int(((q.p_dem>.5)==(q.actual>0)).sum())}/{len(q)}';row[LABELS[model]+' MAE pp']=round((q.prediction_pp-100*q.actual).abs().mean(),3)
        rows.append(row)
    return pd.DataFrame(rows)


def effects(f):
    p=f['predictions'];rows=[]
    for scenario,q in p[p.cycle.between(2016,2024)].groupby('scenario'):
        for on,off,title in [('original','bias_off_fixed','Persistent bias, fixed scales'),('original','bias_off_refit','Persistent bias versus no-bias refit'),('features','original','Joint feature model versus original'),('features','features_off','Feature term within same joint fit')]:
            a=q[q.model.eq(on)].set_index('target_id');b=q[q.model.eq(off)].set_index('target_id').loc[a.index]
            err_on=(a.prediction_pp-100*a.actual).abs();err_off=(b.prediction_pp-100*b.actual).abs()
            rows.append(dict(Horizon=scenario,Comparison=title,correct_call_change=int(((a.p_dem>.5)==(a.actual>0)).sum()-((b.p_dem>.5)==(b.actual>0)).sum()),MAE_improvement_pp=float((err_off-err_on).groupby(a.cycle).mean().mean()),Brier_improvement=float(((b.p_dem-(b.actual>0))**2-(a.p_dem-(a.actual>0))**2).groupby(a.cycle).mean().mean())))
    return pd.DataFrame(rows).round(4)


def feature_effects(f):
    cols=['history_momentum_surprise_pp','history_approval_surprise_pp','updated_momentum_surprise_pp','updated_approval_surprise_pp']
    q=f['components'].query("model=='features'").groupby(['scenario','cycle'])[cols].first().reset_index()
    q['updated_total_surprise_pp']=q.updated_momentum_surprise_pp+q.updated_approval_surprise_pp
    return q.round(4)


def plot(f,out):
    out=Path(out);paths=[]
    q=f['components'].query("cycle==2026 and model=='original' and n_samples>0")
    fig,ax=plt.subplots(figsize=(7,5));ax.scatter(q.legacy_bias_correction_pp,q.history_bayesian_bias_correction_pp,color='#436e9c')
    for r in q.itertuples():
        if r.state in ['AK','MI','NC','TX','OH']:ax.annotate(r.state,(r.legacy_bias_correction_pp,r.history_bayesian_bias_correction_pp),xytext={'AK':(5,-14),'TX':(5,7),'NC':(-19,9)}.get(r.state,(5,6)),textcoords='offset points')
    lim=max(abs(q.legacy_bias_correction_pp).max(),abs(q.history_bayesian_bias_correction_pp).max())+1
    ax.plot([-lim,lim],[-lim,lim],'k--',lw=.8);ax.axvline(0,color='gray',lw=.7);ax.axhline(0,color='gray',lw=.7)
    ax.set_xlim(q.legacy_bias_correction_pp.min()-1,q.legacy_bias_correction_pp.max()+1)
    ax.set_ylim(q.history_bayesian_bias_correction_pp.min()-.6,q.history_bayesian_bias_correction_pp.max()+.6)
    ax.set(xlabel='Old correction to prior-weighted polling (pp)',ylabel='Bayesian correction to raw polling (pp)',title='2026 history-trained bias adjustments\nDifferent input bases; not an equality test');fig.tight_layout();p=out/'bias_comparison.png';fig.savefig(p,dpi=150);plt.close(fig);paths.append(p)
    fig,axes=plt.subplots(1,2,figsize=(11,4),sharey=True)
    q=feature_effects(f)
    for ax,scenario in zip(axes,['matched_live','oct31']):
        g=q[q.scenario.eq(scenario)];x=np.arange(len(g))
        ax.bar(x-.18,g.updated_momentum_surprise_pp,.36,label='Economic momentum',color='#437fa8');ax.bar(x+.18,g.updated_approval_surprise_pp,.36,label='Approval',color='#d49a45');ax.plot(x,g.updated_total_surprise_pp,'ko',ms=4,label='Total')
        ax.axhline(0,color='gray',lw=.8);ax.set_xticks(x,g.cycle,rotation=45);ax.set_title(scenario);ax.set_ylabel('Equivalent polling adjustment, D−R pp')
    axes[0].legend(fontsize=8);fig.suptitle('Shared feature surprise after forecast-poll parameter update');fig.tight_layout();p=out/'shared_feature_surprises.png';fig.savefig(p,dpi=150);plt.close(fig);paths.append(p)
    fig,axes=plt.subplots(1,2,figsize=(11,4.5),sharey=True)
    colors={'original':'#4a6f96','bias_off_refit':'#999999','features':'#b0693c'}
    for ax,scenario in zip(axes,['matched_live','oct31']):
        for model in colors:
            r=f['metrics'].query("scenario==@scenario and model==@model and period=='recent_2016_2024' and group=='all'").iloc[0]
            ax.plot([50,80,95],100*np.array([r.coverage50,r.coverage80,r.coverage95]),'o-',label=LABELS[model],color=colors[model])
        ax.plot([30,100],[30,100],'k--',alpha=.4);ax.set(xlabel='Nominal coverage (%)',title=scenario,xlim=(45,100),ylim=(25,100))
    axes[0].set_ylabel('Observed coverage (%)');axes[0].legend(fontsize=7);fig.suptitle('2016–2024: Gaussian uncertainty remains a separate acceptance check');fig.tight_layout();p=out/'correction_calibration.png';fig.savefig(p,dpi=150);plt.close(fig);paths.append(p)
    return paths

METHOD='''# Bayesian polling corrections: bias ablations and shared features

Notebook Sections9–12 append to BAYESIAN_GAUSSIAN.ipynb; earlier sections and baseline notebooks remain unchanged. Same frozen September17,2026 inputs, same2012–2024folds at two horizons, main2016–2024evaluation.

## Models and comparisons

- Original Bayesian covariance-off and covariance-on forecasts are retained exactly.
- Bias off, fixed scales: set persistent state/shared-mean bias b_s to zero at forecast time. Historical fitted scales stay fixed. This is a sensitivity, not a refit.
- Bias off, refitted scales: fit the historical polling likelihood with b_s=0. The mean-zero cycle polling error remains, and its scales and race-error scales are re-estimated.
- Joint feature model: `poll = final + b_s - beta_economy*x_economy - beta_approval*x_approval + B_cycle + R_race + noise`. Positive beta·x means positive actual-minus-poll surprise (Democratic improvement). Two shared coefficients have N(0,2²) priors in pp per training-score SD. They are jointly estimated with persistent bias and error scales; no extra feature intercept, state feature slopes or old external correction.
- Features off, same joint fit: suppress beta·x only at forecast time while retaining the joint fit's bias/scales. This separates the feature term from changes in other fitted parameters; it is a sensitivity, not a separately fitted model.

The two fixed score recipes include White House party orientation, economic changes from January1and previousOctober31, and approval. All ingredient normalization, median filling and score standardization use one row per earlier **polled** cycle; no forecast/current data or labels fit preprocessing. Cycles have equal weight in preprocessing; the Bayesian likelihood retains the first model's older/recent and midterm/presidential error scales. No new hyperparameter selection based on held-out accuracy. All earlier eligible polls inform the correction, not just the last cycle. Identical national inputs do not become independent contexts by appearing in many state rows; the common cycle polling error represents their shared uncertainty.

Historical final outcomes are observed, so the state-movement and polling-error parameter posteriors factorize under this model. We reuse the first model's saved movement posterior and independently fit the new polling posterior, avoiding redundant movement fits. Reusing draws does not increase movement effective sample size. The polling Gibbs step jointly updates the two coefficients and cycle errors using a collapsed Gaussian calculation. Current polling updates parameters through marginal-likelihood importance weights before joint outcome draws, as in the first model.

No-poll states have no direct feature-adjusted polling observation. Their final forecasts may still change indirectly through state covariance and parameter learning. The displayed `beta·x` is an equivalent raw-poll adjustment, NOT the final posterior-margin change after prior weighting and correlated updating.

## Old versus Bayesian correction semantics

The old correction is learned for a **prior-weighted polling baseline**, whereas Bayesian b_s measures raw-poll-minus-final error. We show old prior pull and old error correction separately. Negating b_s aligns its sign with the old added correction, but does not make the input bases identical. History-trained bias estimates and bias estimates updated with forecast-date polls are separate columns. We do not stack the old correction into the Bayesian likelihood.
'''


def report(lab,out):
    lab,out=Path(lab),Path(out);f=load(out);paths=plot(f,out)
    text=METHOD+'\n## Recent performance\n\n'+performance(f).to_markdown(index=False)+'\n\n## All controls\n\n'+performance(f,controls=True).to_markdown(index=False)+'\n\n## Competitive states\n\n'+performance(f,'competitive').to_markdown(index=False)+'\n\n## Component comparisons (positive improvement is better)\n\n'+effects(f).to_markdown(index=False)+'\n\n## Per-cycle calls and margins\n\n'+cycles(f).to_markdown(index=False)+'\n\n## Current old/Bayesian bias comparison\n\n'+bias_table(f).to_markdown(index=False)+'\n\n## Shared coefficients: historical posterior\n\n'+f['coefficients'].round(4).to_markdown(index=False)+'\n\n## Shared surprise contributions\n\n'+feature_effects(f).to_markdown(index=False)+'\n\n## Current state predictions\n\n'+states(f).to_markdown(index=False)+'\n\n## Full chamber distributions and historical actuals\n\n'+f['seat_distributions'].round(4).to_markdown(index=False)+'\n\n## Diagnostics\n\n'+f['diagnostics'].groupby(['scenario','cycle','model']).agg(max_Rhat=('rhat','max'),min_bulk_ESS=('bulk_ess','min'),min_tail_ESS=('tail_ess','min')).round(3).to_markdown()+'\n\nImportance updates:\n\n'+f['forecast_diagnostics'].round(4).to_markdown(index=False)+'''

Existing ballot/independent/caucus/RCV/runoff and source-availability restrictions remain. Seat distributions are conditional scalar D/R scenarios. Historical missing contests use explicit incumbent-caucus completion, excluded from model accuracy. Point seats count individual >50% calls; expected seats average joint outcomes. Gaussian calibration must be assessed separately from margin/call improvements. Small differences are exploratory, especially with few independent cycles and concentrated importance weights. No automatic model promotion; Student-t and disruption-scale experiments remain future work.
'''
    text+='\n## Earlier point-model references\n\n'+legacy_reference(out).to_markdown(index=False)+'\n\n## Historical winner calls changed from the original Bayesian model\n\n'+changed_calls(f).round(4).to_markdown(index=False)+'''

## Interpretation

Against the original covariance-on Bayesian model, the joint feature model improves September calls from 124 to 125 of 138, with October unchanged at 129. Equal-cycle MAE slightly worsens (7.643 to 7.673 pp; 5.697 to 5.712 pp), as does Brier score. Removing persistent bias and refitting improves September calls to 126 but worsens October margin error. No variant wins consistently. The older corrected-polling reference remains stronger on October point performance (132/138, MAE 5.230 pp).

Feature-model 95% interval coverage is 92.0% in September and 87.7% in October; Gaussian undercoverage remains. Its predictive density improves slightly, but this does not establish calibration. Both current feature coefficient 95% credible intervals include zero. The current feature surprise after polling updates is about +1.16 pp Democratic, before posterior prior/covariance weighting. Original, no-bias refit and joint-feature models all call 49 D / 51 R; expected D seats are 48.17, 48.55 and 48.79. The covariance-off reference still calls 48 D / 52 R.

All 30 new four-chain polling fits meet Rhat <1.01 and bulk/tail ESS >=400. These diagnostics do not replace those of the reused movement posterior. Forecast importance ESS is a separate measure; its minimum is about 400 in an auxiliary features-off control. Small Monte Carlo differences should not determine model selection. All comparisons reuse exploratory historical folds, not a new untouched holdout.
'''
    (lab/'BAYESIAN_CORRECTIONS_RESULTS.md').write_text(text);(out/'BAYESIAN_CORRECTIONS_RESULTS.md').write_text(text);(out/Path(__file__).name).write_bytes(Path(__file__).read_bytes());manifest(out);return f,paths

def legacy_reference(out):
    settings=json.loads((Path(out)/'settings.json').read_text());h=pd.read_parquet(settings['source_inputs']['history']['path']);h=h[h.base.eq('fixed5_8')&h.cycle.between(2016,2024)];rows=[]
    for s,g in h.groupby('scenario'):
        for col,label in [('poll_baseline','Old polling before error correction'),('bias_prediction','Old corrected polling')]:
            rows.append(dict(Horizon=s,Model=label,Correct=f'{int(((g[col]>0)==(g.actual>0)).sum())}/{len(g)}',MAE_pp=round(100*(g[col]-g.actual).abs().groupby(g.cycle).mean().mean(),3)))
    return pd.DataFrame(rows)


def changed_calls(f):
    p=f['predictions'];q=p[p.actual.notna()];a=q[q.model.eq('original')]
    parts=[]
    for model in ['bias_off_fixed','bias_off_refit','features','features_off']:
        b=q[q.model.eq(model)];z=a.merge(b,on=['scenario','cycle','target_id'],suffixes=('_original','_new'),validate='one_to_one')
        z=z[(z.p_dem_original>.5)!=(z.p_dem_new>.5)].copy();z['model']=model
        parts.append(z[['scenario','cycle','geography_original','model','actual_original','p_dem_original','p_dem_new','prediction_pp_original','prediction_pp_new']])
    return pd.concat(parts,ignore_index=True).rename(columns={'geography_original':'state','actual_original':'actual_margin'})
