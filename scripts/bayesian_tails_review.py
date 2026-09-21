"""Paired margin, winner and calibration review of Gaussian/t and point models."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import bayesian_tails as model
from bayesian_gaussian_review import manifest

ORDER=['nonbayes_bias','nonbayes_momentum','gaussian','gaussian_prior150','gaussian_poll150','gaussian_both150','student5']

def load(out):
    out=Path(out);model.base.verify_manifest(out)
    f={p.stem:pd.read_parquet(p) for p in out.glob('*.parquet')};f['fits']=pd.DataFrame(json.loads((out/'fits.json').read_text()));return f

def comparison(f,group='all',period='recent_2016_2024'):
    rows=[]
    for m in ORDER:
        row={'Model':model.LABELS[m]}
        for s,name in [('matched_live','Earlier'),('oct31','Oct31')]:
            q=f['point_metrics'].query('model==@m and scenario==@s and group==@group and period==@period')
            if len(q):
                r=q.iloc[0];row[name+' correct']=f'{r.correct}/{r.n}';row[name+' accuracy %']=100*r.accuracy;row[name+' MAE pp']=r.mae_pp
        rows.append(row)
    return pd.DataFrame(rows).round(3)

def calibration(f):
    q=f['probability_metrics'].query("period=='recent_2016_2024' and group=='all'").copy()
    q['Model']=q.model.map(model.LABELS);q['probability_call_accuracy_pct']=100*q.correct/q.n
    return q[['scenario','Model','probability_call_accuracy_pct','brier','negative_log_density','coverage50','coverage80','coverage95','mean_95_width_pp']].round(4)

def per_cycle(f):
    p=f['predictions'];rows=[]
    for (s,y),g in p[p.actual.notna()].groupby(['scenario','cycle']):
        fit=f['fits'].query('scenario==@s and cycle==@y').iloc[0]
        for m,q in g.groupby('model'):
            rows.append(dict(Horizon=s,Cycle=y,Model=model.LABELS[m],Bayesian_training_cycles=int(fit.training_cycles) if m.startswith(('gaussian','student')) else np.nan,Correct=f'{int(((q.prediction>0)==(q.actual>0)).sum())}/{len(q)}',Accuracy_pct=100*((q.prediction>0)==(q.actual>0)).mean(),MAE_pp=100*(q.prediction-q.actual).abs().mean()))
    return pd.DataFrame(rows).round(3)

def states(f,year=2026,scenario='matched_live'):
    p=f['predictions'].query('cycle==@year and scenario==@scenario');base=p[p.model.eq('gaussian')].set_index('target_id')
    q=base[['geography','actual','n_samples']].copy().rename(columns={'geography':'State','actual':'Actual pp','n_samples':'Poll samples'});q['Actual pp']*=100
    for m in ORDER:
        a=p[p.model.eq(m)].set_index('target_id');q[model.LABELS[m]+' pp']=a.prediction_pp
    q['Student-t D probability %']=100*p[p.model.eq('student5')].set_index('target_id').p_dem
    q.index.name='Contest';return q.reset_index().round(3).sort_values('State')

def chamber(f,out):
    s=json.loads((Path(out)/'settings.json').read_text());b=json.loads((Path(s['source'])/'settings.json').read_text());r=pd.read_parquet(Path(b['source'])/'full_seat_ledger.parquet').query("model=='polling'")
    rows=[]
    for (scenario,year,m),p in f['predictions'].groupby(['scenario','cycle','model']):
        roster=r[(r.scenario==scenario)&(r.cycle==year)];fixed=int(roster[~roster.target_id.isin(p.target_id)].caucus.eq('D').sum())
        row=dict(scenario=scenario,cycle=year,model=m,Model=model.LABELS[m],mean_margin_point_D=fixed+int((p.prediction>0).sum()),actual_D=int(roster.actual_caucus.eq('D').sum()) if year<2026 else np.nan)
        seat=f['seat_distributions'].query('scenario==@scenario and cycle==@year and model==@m')
        if len(seat):
            a=seat.iloc[0];row.update(probability_point_D=a.point_D,expected_D=a.expected_D,D_lo95=a.D_lo95,D_hi95=a.D_hi95)
        rows.append(row)
    return pd.DataFrame(rows)

def diagnostics_by_group(f):
    q=f['predictions'].query("model=='gaussian' and cycle>=2016 and cycle<=2024").copy()
    q['poll_group']=np.where(q.n_samples.gt(0),'Polled','No polls');q['z_error']=(100*q.actual-q.prediction_pp)/q.posterior_sd_pp
    q['miss95']=~((100*q.actual>=q.lo95_pp)&(100*q.actual<=q.hi95_pp))
    q['error_pp']=q.prediction_pp-100*q.actual
    return q.groupby(['scenario','poll_group']).agg(n=('target_id','size'),mean_signed_error_pp=('error_pp','mean'),mean_absolute_z=('z_error',lambda a:a.abs().mean()),fraction_outside95=('miss95','mean')).reset_index().round(3)

def plot(f,out):
    out=Path(out);paths=[];colors=['#444444','#8b667d','#477cac','#73a99c','#e1aa4c','#8e92aa','#b45f3c']
    fig,axes=plt.subplots(1,2,figsize=(12,5),sharey=True)
    for ax,s in zip(axes,['matched_live','oct31']):
        for m,col in zip(ORDER,colors):
            q=f['point_metrics'].query("scenario==@s and model==@m and group=='all' and period=='recent_2016_2024'").iloc[0]
            ax.scatter(q.mae_pp,100*q.accuracy,color=col,s=65,label=model.LABELS[m])
        ax.set(title='47 days before election' if s=='matched_live' else 'October 31',xlabel='Mean absolute margin error (pp; lower is better)');ax.grid(alpha=.15)
    axes[0].set_ylabel('Winner accuracy from mean margin (%)');fig.legend(*axes[0].get_legend_handles_labels(),loc='lower center',ncol=2,fontsize=8)
    fig.suptitle('2016–2024: identical contests, fixed model recipes');fig.tight_layout(rect=(0,.19,1,.95));p=out/'accuracy_mae.png';fig.savefig(p,dpi=150);plt.close(fig);paths.append(p)
    fig,axes=plt.subplots(1,2,figsize=(11,4.5),sharey=True)
    for ax,s in zip(axes,['matched_live','oct31']):
        for m,col in zip(ORDER,colors):
            if m.startswith('nonbayes'):continue
            r=f['probability_metrics'].query("scenario==@s and model==@m and group=='all' and period=='recent_2016_2024'").iloc[0]
            ax.plot([50,80,95],100*np.array([r.coverage50,r.coverage80,r.coverage95]),'o-',color=col,label=model.LABELS[m])
        ax.plot([35,100],[35,100],'k--',alpha=.3);ax.set(title='47 days before election' if s=='matched_live' else 'October 31',xlabel='Nominal coverage (%)',xlim=(45,100),ylim=(30,100))
    axes[0].set_ylabel('Observed coverage (%)');fig.legend(*axes[0].get_legend_handles_labels(),loc='lower center',ncol=2,fontsize=8);fig.tight_layout(rect=(0,.18,1,1));p=out/'tail_calibration.png';fig.savefig(p,dpi=150);plt.close(fig);paths.append(p)
    return paths

METHOD='''# Gaussian scale checks, Student-t and non-Bayesian comparisons

## Fixed design

The original Gaussian covariance-on model is retained exactly. Three **forecast-only sensitivity controls** multiply movement SD, polling-error SD (including aggregation), or both by 1.5. Their historical posterior stays fixed and forecast-poll likelihood weights are recomputed. They are not separately refitted or held-out-tuned models. They test whether relative uncertainty and excessive prior pull plausibly contribute to undercoverage.

The Student-t model refits all historical parameters with the same mean structure, priors, state loadings, input polls, admission rules and age/election-type variance groups. It replaces common movement F, individual movement eta, common polling error B, and individual polling error R by Student-t components with fixed df=5. Their scale squared is `(nu−2)/nu * component_variance`; variance-parameter priors are identical to the Gaussian model. Loading/bias priors and known aggregation noise stay Gaussian. This is a factor model of t components, not one unrestricted multivariate-t outcome distribution. It has no additional economic/approval effects; no disruption labels condition its tails.

Each t component uses latent precision `w ~ Gamma(nu/2, rate=nu/2)` and conditional Gaussian variance `V*(nu−2)/(nu*w)`. Historical Gibbs fitting updates these precisions and all parameters. New-cycle precisions are integrated jointly with forecast polls using importance weights, followed by exact conditional Gaussian outcome draws. Shared latent factors preserve joint state dependence. Forecast outcomes only score predictions; they never enter training or forecast weights. See [Stan's normal/gamma representation](https://mc-stan.org/docs/2_38/stan-users-guide/efficiency-tuning.html) and [Student-t parameterization](https://mc-stan.org/docs/2_29/functions-reference/student-t-distribution.html).

The 1.5 multiplier and df=5 are fixed comparisons, not settings chosen by evaluation scores. Sampling duration increases only for convergence. Independent predictive integration runs check Monte Carlo stability; latent-scale repetition does not manufacture independent MCMC parameter draws. Bayesian convergence is checked separately from predictive calibration.

## Non-Bayesian references and metrics

Two previously saved fixed references are included: state bias-corrected polling (last five calendar cycles, 8-year bias decay, previous-cycle-selected shrinkage), and that same model plus shared momentum. The former was strongest for October winner calls; the latter had better earlier results. They are retrospectively identified contenders, not a freshly selected universal best. We do not pick different models using each held-out cycle's result. No new probabilities or intervals are invented for these point models.

All seven models use identical contests/actuals. Main evaluation: 2016–2024, five cycles and 138 contests per horizon. Older-inclusive evaluation: 2012–2024; all earlier admitted training data retained. `matched_live` means 47 days before each election, not September 17 in every historical year. Current snapshot remains September 17, 2026; no data refresh occurred.

For direct model comparison, winner accuracy uses the sign of the **predicted mean D−R margin** for every model, and pools contest calls. MAE averages state absolute error within each cycle and then averages cycles equally, in percentage points. The separate probability table classifies Bayesian winners using P(D)>0.5, which can differ from mean-sign calls in skewed mixtures. Brier and negative log predictive density are lower-is-better; interval coverage pools contests and should match its nominal level. Larger intervals alone are not proof of a better predictive distribution. See [posterior predictive checks](https://mc-stan.org/docs/2_29/stan-users-guide/ppcs.html).

Competitive-state membership is frozen from earlier election results. National contexts are shared by states; these rows are not 138 independent economic environments. All comparisons remain exploratory after extensive retrospective work. Current and historical chamber totals retain the same scalar D/R ballot/caucus/independent/runoff assumptions and unmodeled-contest completion rules. D includes D-caucus independents. Probabilities are conditional on those assumptions.
'''

def report(lab,out):
    lab,out=Path(lab),Path(out);f=load(out);figures=plot(f,out);seats=chamber(f,out)
    text=METHOD
    for title,table in [('Recent all contests',comparison(f)),('Recent competitive contests',comparison(f,'competitive')),('Recent noncompetitive contests',comparison(f,'noncompetitive')),('All scored cycles',comparison(f,period='all_scored')),('Probability and interval calibration',calibration(f)),('Original Gaussian error by poll availability',diagnostics_by_group(f)),('Per-cycle point scores',per_cycle(f)),('Current states',states(f)),('Current chamber scenarios',seats[seats.cycle.eq(2026)]),('Predictive integration stability',f['integration_stability'].round(4)),('Forecast-weight diagnostics',f['forecast_diagnostics'].round(3))]:
        text+='\n## '+title+'\n\n'+table.to_markdown(index=False)+'\n'
    text+='''
## What this experiment supports

The Student-t model does not consistently improve on the original Gaussian: recent mean-sign calls are 125 versus 124 at the earlier horizon, but 128 versus 129 in October; MAE is 7.600 versus 7.643 pp and 5.789 versus 5.697 pp, respectively. These small changes do not beat the fixed non-Bayesian contenders. Corrected polling plus momentum leads earlier (126/138, 7.205 pp), while corrected polling leads October (132/138, 5.230 pp). These are two separate recipes, not one oracle that switches with test outcomes.

Increasing both Gaussian SD components by 1.5 brings nominal 95% coverage from 90.6% / 87.7% to 94.2% / 93.5% and improves mean log predictive density, but its 50% intervals overcover (63.0% / 58.0%). Student-t 95% coverage is 89.9% / 86.2%; its central intervals also undercover. Thus a heavier-tailed likelihood alone does not resolve this model's calibration problem. This result supports investigating scale and conditional-mean errors, but neither identifies their cause nor rules out other tail models. Some scale sensitivities have concentrated importance weights (ESS about 166–254), limiting fine comparisons.

Independent Student-t forecast integrations change no mean-sign or probability-majority winner calls in any of the 15 folds. The maximum absolute mean-margin change is about 0.29 pp and maximum probability change about 1.48 percentage points. Small MAE differences remain Monte Carlo-sensitive; these repeated integrations do not assess all MCMC error. Every historical Student-t fit passes the four-chain convergence gate.

Current Student-t and original Gaussian both call 49 D / 51 R (expected D 48.23 versus 48.17); corrected polling calls 50 D / 50 R. These remain frozen September 17, 2026 conditional scenarios. No model is automatically promoted. The next decision is whether to improve mean/bias/recency and scale modeling; extra changes are not included in this experiment.
'''
    (lab/'BAYESIAN_TAILS_RESULTS.md').write_text(text);(out/'BAYESIAN_TAILS_RESULTS.md').write_text(text);seats.to_parquet(out/'chamber_comparison.parquet',index=False)
    (out/Path(__file__).name).write_bytes(Path(__file__).read_bytes());manifest(out);return f,figures,seats
