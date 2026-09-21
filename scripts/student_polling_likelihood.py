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

SOURCE='20260919T210836.001457Z'
DFS=[0,5,10,30] # 0 = Gaussian, no latent scale.
GRID=[(df,g) for df in DFS for g in [0.,2.]]
CONFIG=dict(df_choices=DFS,national_sd_pp=[0.,2.],nodes=257,log_scale_bound=16.,draws=30000,seed=197139,validation_cycles=3,as_of='2026-09-17')


def fit(test,k,poll,df=5,g=0.,nodes=257,bound=16.):
    if df!=0 and df<=2:raise ValueError('Student df must exceed two')
    if not np.isfinite(g) or g<0:raise ValueError('Invalid national SD')
    obs=np.flatnonzero(test.q_pp.notna());si=np.array([v1.STATES.index(x) for x in test.geography]);so=si[obs]
    mu=100*test.prior.to_numpy();values=test.q_pp.to_numpy()[obs]-poll['bias_mean'][so]
    systematic=poll['covariance'][np.ix_(so,so)]+g*g*np.ones((len(obs),len(obs)))
    fixed=poll['bias_covariance'][np.ix_(so,so)]+np.diag(16/test.firm_mass.to_numpy()[obs])
    if df==0 or not len(obs):scales=np.array([1.]);logs=np.array([0.]);prior_mass=1.
    else:
        z=np.linspace(-bound,bound,nodes);scales=np.exp(z);a=df/2;b=(df-2)/2
        logs=a*np.log(b)-gammaln(a)-a*z-b/scales+np.log(z[1]-z[0]);logs[[0,-1]]-=np.log(2)
        prior_mass=float(np.exp(logsumexp(logs)))
    means=[];covs=[];evidence=[]
    for scale in scales:
        mean,cov,ll=v1.normal_update(mu,k,obs,values,fixed+scale*systematic)
        means.append(mean);covs.append(cov);evidence.append(ll)
    means=np.array(means);covs=np.array(covs);lw=logs+evidence;log_evidence=float(logsumexp(lw));w=np.exp(lw-log_evidence)
    mean=w@means;centered=means-mean;cov=np.einsum('k,kij->ij',w,covs)+np.einsum('k,ki,kj->ij',w,centered,centered)
    return dict(means=means,covs=covs,weights=w,scales=scales,mean=mean,covariance=cov,log_evidence=log_evidence,scale_mean=float(w@scales),
        p_scale_gt1=float(w[scales>1].sum()+(.5*w[scales==1].sum() if len(w)>1 else 0.)),edge_mass=float(w[:3].sum()+w[-3:].sum()) if len(w)>6 else 0.,prior_grid_mass=prior_mass,df=df,g=g)


def summarize(test,d,intervals=True):
    p=test.copy();means=d['means'];sd=np.sqrt(np.diagonal(d['covs'],axis1=1,axis2=2));w=d['weights'];mean=d['mean']
    p['prediction_pp']=mean;p['prediction']=mean/100;p['posterior_sd_pp']=np.sqrt(np.diag(d['covariance']));p['p_dem']=w@ndtr(means/sd)
    with np.errstate(divide='ignore'):lw=np.log(w)
    p['log_predictive_density']=logsumexp(lw[:,None]+norm.logpdf(100*p.actual.to_numpy()[None,:],means,sd),axis=0)
    if intervals:
        for level in [50,70,80,95]:
            for side,prob in [('lo',(1-level/100)/2),('hi',(1+level/100)/2)]:
                p[f'{side}{level}_pp']=[brentq(lambda x:np.dot(w,ndtr((x-means[:,j])/sd[:,j]))-prob,float((means[:,j]-12*sd[:,j]).min()),float((means[:,j]+12*sd[:,j]).max()),xtol=1e-10) for j in range(len(test))]
    return p


def joint_nll(actual,d):
    ids=np.flatnonzero(np.isfinite(actual))
    if not len(ids):return np.nan
    logs=[]
    for mean,cov in zip(d['means'],d['covs']):
        l=np.linalg.cholesky(cov[np.ix_(ids,ids)]);e=np.linalg.solve(l,np.asarray(actual)[ids]-mean[ids]);logs.append(-.5*(len(ids)*np.log(2*np.pi)+2*np.log(np.diag(l)).sum()+e@e))
    with np.errstate(divide='ignore'):lw=np.log(d['weights'])
    return float(-logsumexp(lw+logs)/len(ids))


def sample(d,z,u):
    ids=np.minimum(np.searchsorted(np.cumsum(d['weights']),u),len(d['weights'])-1);draws=np.empty_like(z)
    for i in np.unique(ids):
        sel=ids==i;draws[sel]=d['means'][i]+z[sel]@np.linalg.cholesky(d['covs'][i]).T
    return draws


def select(scores,year,g=None):
    allowed=GRID if g is None else [(df,g) for df in [5,10,30]]
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
    lab=Path(lab).resolve();source=lab/'reports/national_tails_waves'/SOURCE;sha=v1.verify(source);s=json.loads((source/'settings.json').read_text());prior=Path(s['prior_source']);upstream=Path(s['upstream']);v1.verify(prior);v1.verify(upstream)
    old=pd.read_parquet(prior/'predictions.parquet');sf=pd.read_parquet(prior/'folds.parquet');sf=sf[sf.model.eq('control_state')];roster=pd.read_parquet(upstream/'full_seat_ledger.parquet')
    out=lab/'reports/student_polling_likelihood'/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ');out.mkdir(parents=True);(out/'forecasts').mkdir();(out/'recipe').mkdir();print('OUTPUT',out,flush=True)
    settings=dict(config=CONFIG,source=str(source),source_sha256=sha,prior_source=str(prior),prior_source_sha256=v1.verify(prior),upstream=str(upstream),upstream_sha256=v1.verify(upstream),
        old_notebook_hashes={p.name:v1.sha(p) for p in lab.glob('*.ipynb') if p.name!='STUDENT_POLLING_LIKELIHOOD.ipynb'},promotion=False,polling_refreshed=False)
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
                    if df==5:
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
    (out/'STUDENT_POLLING_LIKELIHOOD.md').write_bytes((lab/'STUDENT_POLLING_LIKELIHOOD.md').read_bytes());v1.manifest(out);audit(out,lab);report(out,lab);v1.json_write(out.parent/'latest.json',dict(artifact=out.name,manifest_sha256=v1.sha(out/'manifest.json')));return out


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
    text='# Student-t polling likelihood — results\n\nFrozen September17,2026 inputs. Gaussian historical prior unchanged; Student-t systematic polling error convolved with unchanged Gaussian bias/fresh noise. This is a likelihood update, not a post-fit t replacement. One scale per cycle links all systematic errors; not independent poll/state outlier weights. No automatic promotion.\n\n'
    text+='## Review finding\n\nThe fixed nu5/g2 likelihood slightly improves MAE versus matched Gaussian g2:6.909→6.897pp earlier and5.218→5.162pp late. Joint density and Brier scores also improve at both horizons, but marginal density and coverage worsen. Winner calls fall129→128 earlier and133→131 late. Late95%coverage falls92.1→90.0%;70%coverage69.3→64.3%. The lost late calls are FL2018 and NC2020, near-zero Gaussian wins that the t update reverses. Earlier it loses NC2020. These are tradeoffs, not universal improvement.\n\nAtg0, nu5 improves lateMAE5.250→5.207 and expected-seatMAE1.288→1.211 with131calls unchanged, but95%coverage falls92.1→90.7%. Atg2, late expected-seatMAE improves1.479→1.384 but remains worse than reference1.288. Earlier expected-seat error worsens under fixednu5 at either g. Selection remains mixed; keep existing references for review.\n\nCurrent nu5/g2 gives48Dpoint/48.446expected/70%47–50/95%45–52, versus Gaussian g2 47Dpoint/48.105expected. AK movesR+0.236→D+0.473; MI movesR+0.425→R+0.112. The unchanged Gaussian g0 reference is49Dpoint/48.481expected. Current posterior systematic variance multiplier averages0.749, allowing more polling information on average; heavy tails do not automatically increase variance or always downweight polls. No2026outcomes were used.\n\nAll120integration comparisons pass, with maximum mean discrepancy below6e-13pp. Seat probabilities/ranges use30,000joint draws with shared random inputs within this experiment. Integer quantile endpoints near a probability boundary can differ across earlier experiments using other seeds; do not interpret those as model changes.\n\n'
    for period in ['recent_2016_2024','tuned_2018_2024','all_2012_2024']:text+='## '+period+'\n\n'+summary[summary.period.eq(period)][cols].round(4).to_markdown(index=False)+'\n\n'
    text+='## Per-cycle outcomes\n\n'+cycle.round(4).to_markdown(index=False)+'\n\n'
    text+='## Selection and systematic-error scale\n\nScale is a variance multiplier. Values below1 permit more polling influence, values above1 less, conditional on the same prior. Historical priors and baseline covariance shape remain fixed.\n\n'+f[['scenario','cycle','model','df','national_sd','scale_mean','p_scale_gt1','validation_cycles','status']].round(4).to_markdown(index=False)+'\n\n'
    text+='## Recent chamber results\n\nFive cycles per horizon; existing continuing/unmodeled-seat completion assumptions remain.\n\n'+chamber.round(4).to_markdown(index=False)+'\n\n'
    text+='## Current forecasts\n\nPoint seats use posterior-mean signs; probability_call_D uses P(D)>0.5. Mixtures may distinguish them.\n\n'+seats[seats.cycle.eq(2026)][['model','point_D','point_R','probability_call_D','expected_D_exact','D_lo70','D_hi70','D_lo95','D_hi95','p_D_at_least_51','p_D_exactly_50']].round(4).to_markdown(index=False)+'\n\n'
    text+='## Current state margins\n\n'+p[p.cycle.eq(2026)].pivot(index='geography',columns='model',values='prediction_pp').round(3).to_markdown()+'\n\n'
    text+='## Numerical integration\n\n'+integ.groupby('check')[['max_mean_difference_pp','max_probability_difference','relative_covariance_difference','joint_nll_difference','edge_mass']].max().to_markdown()+'\n\n'
    text+='## Limits\n\nOne common scale provides correlated heavy errors but cannot isolate individual-state outliers. Prior/correlation/bias parameters remain estimated as before, with their estimation uncertainty largely omitted. Historical selection is chronological but extensive prior exploration makes results exploratory. Posterior scale can decrease, narrowing central intervals despite heavier tails. No conclusions should be based on current partisan direction. Review results before choosing inclusion.\n'
    (lab/'STUDENT_POLLING_LIKELIHOOD_RESULTS.md').write_text(text);(out/'STUDENT_POLLING_LIKELIHOOD_RESULTS.md').write_text(text);v1.manifest(out)


if __name__=='__main__':build(Path(__file__).resolve().parents[1])
