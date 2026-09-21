"""Controlled covariance-scale/tail study, national-error tuning, conditional waves."""
from pathlib import Path
from datetime import datetime, timezone
import json
import numpy as np
import pandas as pd
from scipy.stats import norm, t, multivariate_normal, multivariate_t, chi2
import simple_bayesian_polling as v1
import poll_update_review as review
import structured_poll_error as structured

SOURCE='20260919T205021.002455Z'
FAMILIES=['gaussian','scale4','scale10','scale30','t5_matched']
GS=[0.,2.,4.,6.]
GRID=[(f,g) for f in FAMILIES for g in GS]
CONFIG=dict(families=FAMILIES,national_sd_pp=GS,draws=30000,seed=196019,validation_cycles=3,as_of='2026-09-17',prior_model='control_state')


def distribution(test,k,poll,info,family,g):
    if family not in FAMILIES or not np.isfinite(g) or g<0:raise ValueError('Invalid model')
    obs,so,r=structured.observation_covariance(test,poll,info,(g,0.,0.))
    mu=100*test.prior.to_numpy();values=test.q_pp.to_numpy()[obs]-poll['bias_mean'][so]
    mean,v,_=v1.normal_update(mu,k,obs,values,r)
    a=k[np.ix_(obs,obs)]+r;res=values-mu[obs]
    solved=np.linalg.solve(a,res) if len(obs) else np.array([])
    h=float(res@solved);n=len(obs);df=np.inf;factor=1.;scale=v.copy()
    if family.startswith('scale'):
        nu=int(family[5:]);df=float(nu+n);factor=(nu-2+h)/(nu+n-2);scale=v*(nu-2+h)/(nu+n)
    elif family=='t5_matched':df=5.;scale=v*3/5
    umean=float(g*g*solved.sum());uv=g*g-g**4*float(np.linalg.solve(a,np.ones(n)).sum()) if n else g*g
    return dict(mean=mean,scale=scale,covariance=scale if np.isinf(df) else scale*df/(df-2),df=df,
                scale_mean=factor,innovation_mahal=h,observed=n,national_error_mean_pp=umean,
                national_error_sd_pp=float(np.sqrt(max(0,uv)*factor)),family=family,g=g)


def summarize(test,dist,delta=0.):
    if not np.isfinite(delta):raise ValueError('Finite wave shift required')
    p=test.copy();mean=dist['mean']+delta;sd=np.sqrt(np.diag(dist['scale']));df=dist['df']
    rv=norm if np.isinf(df) else t(df)
    p['prediction_pp']=mean;p['prediction']=mean/100;p['posterior_sd_pp']=np.sqrt(np.diag(dist['covariance']))
    p['p_dem']=rv.cdf(mean/sd);p['log_predictive_density']=rv.logpdf((100*p.actual-mean)/sd)-np.log(sd)
    for level in [50,70,80,95]:
        width=rv.ppf((1+level/100)/2)*sd;p[f'lo{level}_pp']=mean-width;p[f'hi{level}_pp']=mean+width
    return p


def joint_nll(actual,dist):
    ids=np.flatnonzero(np.isfinite(actual))
    if not len(ids):return np.nan
    mean=dist['mean'][ids];scale=dist['scale'][np.ix_(ids,ids)];y=np.asarray(actual)[ids]
    logp=multivariate_normal.logpdf(y,mean=mean,cov=scale) if np.isinf(dist['df']) else multivariate_t.logpdf(y,loc=mean,shape=scale,df=dist['df'])
    return float(-logp/len(ids))


def sample(dist,z,uniforms):
    centered=z@np.linalg.cholesky(dist['scale']).T
    if np.isfinite(dist['df']):centered*=np.sqrt(dist['df']/chi2.ppf(uniforms,dist['df']))[:,None]
    return dist['mean']+centered


def select(scores,year,scope):
    allowed=GRID if scope=='all' else [(f,g) for f,g in GRID if (f.startswith('scale') if scope=='scale' else f==scope)]
    fallback=('gaussian',0.) if scope=='all' else ('scale10',0.) if scope=='scale' else (scope,0.)
    past=scores[scores.cycle.lt(year)&scores.key.isin(allowed)];years=sorted(past.cycle.unique())[-3:]
    if len(years)<3:return fallback,years,'early_fixed_fallback'
    past=past[past.cycle.isin(years)]
    if len(past)!=len(years)*len(allowed) or past.duplicated(['cycle','key']).any():raise ValueError('Incomplete tuning grid')
    vals=past.groupby('key').joint_nll.mean().to_dict()
    if not np.isfinite(list(vals.values())).all():raise ValueError('Nonfinite validation objective')
    key=min(vals,key=lambda x:(vals[x],FAMILIES.index(x[0]),x[1]))
    return key,years,'last_three_past_cycles'


def seat_summary(roster,test,pred,draws):
    result=v1.seat_counts(roster,test,pred,draws);counts=result['fixed_D']+(draws>0).sum(axis=1)
    result['expected_D_exact']=float(result['fixed_D']+pred.p_dem.sum())
    for level in [70,95]:
        a=(1-level/100)/2;lo,hi=np.quantile(counts,[a,1-a],method='inverted_cdf');result[f'D_lo{level}']=int(lo);result[f'D_hi{level}']=int(hi)
    return result,counts


def wave(out,model='reference',delta=0.):
    """Conditional 2026 shift; never modifies fitted artifacts or their inputs."""
    out=Path(out);folds=pd.read_parquet(out/'folds.parquet');r=folds[folds.cycle.eq(2026)&folds.model.eq(model)].iloc[0]
    z=np.load(out/r.forecast_path);dist=dict(mean=z['mean'],scale=z['scale'],covariance=z['covariance'],df=float(z['df']))
    p=pd.read_parquet(out/'predictions.parquet');p=p[p.cycle.eq(2026)&p.model.eq(model)].sort_values('target_id').reset_index(drop=True)
    if not np.array_equal(p.target_id.to_numpy(str),z['target_ids']):raise ValueError('Target order mismatch')
    pred=summarize(p,dist,delta);draws=z['draws_pp']+delta
    roster=pd.read_parquet(out/'full_seat_ledger.parquet');roster=roster[roster.cycle.eq(2026)&roster.scenario.eq(r.scenario)]
    seats,_=seat_summary(roster,p,pred,draws)
    return pred,dict(model=model,wave_pp=float(delta),**seats)


def custom_current(out,family='gaussian',national_sd_pp=2.,wave_pp=0.):
    """Refit current likelihood with user settings; no writes or model promotion."""
    out=Path(out);settings=json.loads((out/'settings.json').read_text());prior=Path(settings['prior_source']);source=Path(settings['source'])
    v1.verify(prior);v1.verify(source)
    f=pd.read_parquet(out/'folds.parquet');r=f[f.cycle.eq(2026)&f.model.eq('reference')].iloc[0]
    p=pd.read_parquet(out/'predictions.parquet');test=p[p.cycle.eq(2026)&p.model.eq('reference')].sort_values('target_id').reset_index(drop=True)
    k=np.load(prior/r.source_forecast)['prior_covariance'];poll=dict(np.load(prior/r.source_poll));info=dict(np.load(source/f'information/{r.scenario}_2026.npz'))
    d=distribution(test,k,poll,info,family,national_sd_pp);pred=summarize(test,d,wave_pp)
    rng=np.random.default_rng(CONFIG['seed']+2026);z=rng.standard_normal((CONFIG['draws'],len(test)));u=np.clip(rng.random(CONFIG['draws']),1e-10,1-1e-10)
    draws=sample(d,z,u)+wave_pp;roster=pd.read_parquet(out/'full_seat_ledger.parquet');rr=roster[roster.cycle.eq(2026)&roster.scenario.eq(r.scenario)]
    seat,_=seat_summary(rr,test,pred,draws)
    return pred,dict(family=family,national_sd_pp=national_sd_pp,wave_pp=wave_pp,**seat),d


def build(lab):
    lab=Path(lab).resolve();source=lab/'reports/structured_poll_error'/SOURCE;source_sha=v1.verify(source)
    oldsettings=json.loads((source/'settings.json').read_text());prior=Path(oldsettings['source']);prior_sha=v1.verify(prior);upstream=Path(oldsettings['upstream']);upstream_sha=v1.verify(upstream)
    old=pd.read_parquet(prior/'predictions.parquet');sf=pd.read_parquet(prior/'folds.parquet');sf=sf[sf.model.eq('control_state')]
    roster=pd.read_parquet(upstream/'full_seat_ledger.parquet')
    out=lab/'reports/national_tails_waves'/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ');out.mkdir(parents=True);(out/'forecasts').mkdir();(out/'recipe').mkdir()
    print('OUTPUT',out,flush=True);settings=dict(config=CONFIG,source=str(source),source_sha256=source_sha,prior_source=str(prior),prior_source_sha256=prior_sha,upstream=str(upstream),upstream_sha256=upstream_sha,
        old_notebook_hashes={p.name:v1.sha(p) for p in lab.glob('*.ipynb') if p.name!='NATIONAL_TAILS_WAVES.ipynb'},promotion=False,polling_refreshed=False)
    v1.json_write(out/'settings.json',settings);roster.to_parquet(out/'full_seat_ledger.parquet',index=False)
    predictions=[];candidates=[];scores=[];folds=[];seats=[];trace=[]
    for sc,group in sf.groupby('scenario'):
        for row in group.sort_values('cycle').itertuples():
            year=int(row.cycle);test=old[old.scenario.eq(sc)&old.cycle.eq(year)&old.model.eq('control_state')].sort_values('target_id').reset_index(drop=True)
            base=np.load(prior/row.forecast_path);assert np.array_equal(base['target_ids'],test.target_id.to_numpy(str));k=base['prior_covariance'];poll=dict(np.load(prior/row.poll_path));info=dict(np.load(source/f'information/{sc}_{year}.npz'))
            bank={}
            for family,g in GRID:
                dist=distribution(test,k,poll,info,family,g);pred=summarize(test,dist);bank[(family,g)]=(dist,pred)
                candidates.append(pred.assign(family=family,national_sd=g,model=family+'_g'+str(g)))
            past=pd.DataFrame([s for s in scores if s['scenario']==sc],columns=['scenario','cycle','key','joint_nll'])
            choices={'reference':(('gaussian',0.),[],'fixed'),'common2':(('gaussian',2.),[],'fixed'),
                     'scale10_g0':(('scale10',0.),[],'fixed'),'scale10_g2':(('scale10',2.),[],'fixed'),
                     't5_g0':(('t5_matched',0.),[],'fixed'),'t5_g2':(('t5_matched',2.),[],'fixed')}
            for name,scope in [('national_selected','gaussian'),('scale_selected','scale'),('t5_national_selected','t5_matched'),('all_selected','all')]:
                choices[name]=select(past,year,scope);key,years,status=choices[name]
                for rr in past[past.cycle.isin(years)].to_dict('records'):
                    ff,gg=rr.pop('key');trace.append(dict(**rr,family=ff,national_sd=gg,forecast_cycle=year,scope=scope,selected_family=key[0],selected_g=key[1],status=status))
            for key,(dist,pred) in bank.items():
                if year<2026:scores.append(dict(scenario=sc,cycle=year,key=key,joint_nll=joint_nll(100*test.actual.to_numpy(),dist)))
            rng=np.random.default_rng(CONFIG['seed']+year+10000*(sc=='oct31'));z=rng.standard_normal((CONFIG['draws'],len(test)));u=np.clip(rng.random(CONFIG['draws']),1e-10,1-1e-10)
            rr=roster[roster.scenario.eq(sc)&roster.cycle.eq(year)]
            for model,(key,years,status) in choices.items():
                dist,pred=bank[key];pred=pred.assign(model=model,prior_model='control_state',family=key[0],national_sd=key[1]);predictions.append(pred)
                draws=sample(dist,z,u);seat,counts=seat_summary(rr,test,pred,draws);seats.append(dict(scenario=sc,cycle=year,model=model,**seat))
                path=f'forecasts/{sc}_{year}_{model}.npz';saved=dict(target_ids=test.target_id.to_numpy(str),mean=dist['mean'],scale=dist['scale'],covariance=dist['covariance'],df=dist['df'],prior_covariance=k,seat_count_frequency=np.bincount(counts,minlength=101))
                if year==2026:saved['draws_pp']=draws
                np.savez_compressed(out/path,**saved)
                folds.append(dict(scenario=sc,cycle=year,model=model,family=key[0],national_sd=key[1],df=dist['df'],scale_mean=dist['scale_mean'],innovation_mahal=dist['innovation_mahal'],observed=dist['observed'],
                    national_error_mean_pp=dist['national_error_mean_pp'],national_error_sd_pp=dist['national_error_sd_pp'],validation_cycles=','.join(map(str,years)),status=status,training_max_cycle=row.training_max_cycle,
                    source_forecast=row.forecast_path,source_poll=row.poll_path,forecast_path=path,joint_nll=joint_nll(100*test.actual.to_numpy(),dist)))
            print(sc,year,'national',choices['national_selected'][0],'all',choices['all_selected'][0],flush=True)
    p=pd.concat(predictions,ignore_index=True);f=pd.DataFrame(folds);ss=pd.DataFrame([{**{k:v for k,v in s.items() if k!='key'},'family':s['key'][0],'national_sd':s['key'][1]} for s in scores])
    for name,table in dict(predictions=p,candidate_predictions=pd.concat(candidates,ignore_index=True),folds=f,scores=ss,tuning=pd.DataFrame(trace),seats=pd.DataFrame(seats),calibration=review.metrics(p)).items():table.to_parquet(out/(name+'.parquet'),index=False)
    waves=[];statewaves=[]
    for model in f[f.cycle.eq(2026)].model:
        for delta in [-6.,-4.,-2.,0.,2.,4.,6.]:
            pp,seat=wave(out,model,delta);waves.append(seat);statewaves.append(pp.assign(wave_pp=delta))
    pd.DataFrame(waves).to_parquet(out/'waves.parquet',index=False);pd.concat(statewaves,ignore_index=True).to_parquet(out/'wave_states.parquet',index=False)
    for src in (lab/'scripts').glob('*.py'):(out/'recipe'/src.name).write_bytes(src.read_bytes())
    (out/'NATIONAL_TAILS_WAVES.md').write_bytes((lab/'NATIONAL_TAILS_WAVES.md').read_bytes());v1.manifest(out)
    audit(out,lab);report(out,lab);v1.json_write(out.parent/'latest.json',dict(artifact=out.name,manifest_sha256=v1.sha(out/'manifest.json')));return out


def audit(out,lab):
    out,lab=Path(out),Path(lab);v1.verify(out);s=json.loads((out/'settings.json').read_text());source=Path(s['source']);prior=Path(s['prior_source'])
    p=pd.read_parquet(out/'predictions.parquet');cp=pd.read_parquet(out/'candidate_predictions.parquet');f=pd.read_parquet(out/'folds.parquet');scores=pd.read_parquet(out/'scores.parquet');scores['key']=list(zip(scores.family,scores.national_sd));seats=pd.read_parquet(out/'seats.parquet');waves=pd.read_parquet(out/'waves.parquet')
    old=pd.read_parquet(prior/'predictions.parquet');c={name+'_unchanged':v1.verify(s[name])==s[name+'_sha256'] for name in ['source','prior_source','upstream']}
    c.update(old_notebooks_unchanged=all(v1.sha(lab/n)==h for n,h in s['old_notebook_hashes'].items()),future_labels_blank=bool(p[p.cycle.eq(2026)].actual.isna().all() and cp[cp.cycle.eq(2026)].actual.isna().all()),
        unique_forecasts=not p.duplicated(['scenario','model','target_id']).any(),past_base_training=bool(f.training_max_cycle.lt(f.cycle).all()),finite_forecasts=bool(np.isfinite(p[['prediction_pp','posterior_sd_pp','p_dem']]).all().all()),
        equal_cases=all(g.groupby('model').target_id.apply(frozenset).nunique()==1 for _,g in p.groupby(['scenario','cycle'])),complete_candidate_grid=bool(cp.groupby(['scenario','target_id']).size().eq(len(GRID)).all() and not cp.duplicated(['scenario','target_id','family','national_sd']).any()))
    cols=['prediction_pp','posterior_sd_pp','p_dem','lo70_pp','hi70_pp','lo95_pp','hi95_pp'];recon=[];frozen=[];reference=[];selection=[];seatcheck=[];candidatecheck=[];meancheck=[];positive=[];pastcheck=[]
    scopes={'national_selected':'gaussian','scale_selected':'scale','t5_national_selected':'t5_matched','all_selected':'all'}
    for (sc,year),group in f.groupby(['scenario','cycle']):
        row=group.iloc[0];test=old[old.scenario.eq(sc)&old.cycle.eq(year)&old.model.eq('control_state')].sort_values('target_id').reset_index(drop=True);k=np.load(prior/row.source_forecast)['prior_covariance'];poll=dict(np.load(prior/row.source_poll));info=dict(np.load(source/f'information/{sc}_{year}.npz'));bank={}
        for key in GRID:
            d=distribution(test,k,poll,info,*key);expected=summarize(test,d);bank[key]=(d,expected)
            q=cp[cp.scenario.eq(sc)&cp.cycle.eq(year)&cp.family.eq(key[0])&cp.national_sd.eq(key[1])].sort_values('target_id')
            ok=np.allclose(expected[cols],q[cols],atol=1e-10)
            if year<2026:
                r=scores[scores.scenario.eq(sc)&scores.cycle.eq(year)&scores.family.eq(key[0])&scores.national_sd.eq(key[1])].iloc[0];ok=ok and abs(r.joint_nll-joint_nll(100*test.actual.to_numpy(),d))<1e-10
            candidatecheck.append(ok);positive.append(np.linalg.eigvalsh(d['covariance']).min()>0)
        for g in GS:
            base=bank[('gaussian',g)][0]
            meancheck.append(all(np.array_equal(bank[(family,g)][0]['mean'],base['mean']) for family in FAMILIES))
            meancheck.append(np.allclose(bank[('t5_matched',g)][0]['covariance'],base['covariance']))
        for r in group.itertuples():
            d,expected=bank[(r.family,r.national_sd)];q=p[p.scenario.eq(sc)&p.cycle.eq(year)&p.model.eq(r.model)].sort_values('target_id');z=np.load(out/r.forecast_path)
            recon.append(np.allclose(expected[cols],q[cols],atol=1e-10) and np.allclose(d['covariance'],z['covariance']) and np.array_equal(z['target_ids'],q.target_id.to_numpy(str)))
            frozen.append(np.array_equal(k,z['prior_covariance']) and np.array_equal(test.prior,q.prior))
            if r.model=='reference':reference.append(np.allclose(q[cols],test[cols],atol=1e-10))
            if r.model in scopes:
                key,years,status=select(scores[scores.scenario.eq(sc)],year,scopes[r.model]);selection.append(key==(r.family,r.national_sd) and ','.join(map(str,years))==r.validation_cycles and status==r.status);pastcheck.append(all(y<year for y in years))
            seat=seats[seats.scenario.eq(sc)&seats.cycle.eq(year)&seats.model.eq(r.model)].iloc[0]
            seatcheck.append(z['seat_count_frequency'].sum()==CONFIG['draws'] and abs(seat.expected_D_exact-seat.fixed_D-q.p_dem.sum())<1e-10 and seat.point_D==seat.fixed_D+(q.prediction_pp>0).sum())
    zero=[];monotone=[];waverecon=[]
    for model,g in waves.groupby('model'):
        g=g.sort_values('wave_pp');monotone.append(all(g[col].diff().dropna().ge(-1e-12).all() for col in ['point_D','expected_D_exact','p_D_at_least_51','D_lo70','D_hi70']))
        for r in g.itertuples():
            pp,seat=wave(out,model,r.wave_pp);waverecon.append(all(np.isclose(seat[col],getattr(r,col)) for col in ['point_D','expected_D_exact','D_lo70','D_hi70','p_D_at_least_51']))
            if r.wave_pp==0:
                sr=seats[seats.cycle.eq(2026)&seats.model.eq(model)].iloc[0];zero.append(all(np.isclose(sr[col],seat[col]) for col in ['point_D','expected_D_exact','D_lo70','D_hi70']))
    customok=[]
    for model,family,g in [('reference','gaussian',0.),('common2','gaussian',2.),('t5_g2','t5_matched',2.)]:
        pp,seat,_=custom_current(out,family,g,2.);expected,es=wave(out,model,2.)
        customok.append(np.allclose(pp[cols],expected[cols],atol=1e-10) and abs(seat['expected_D_exact']-es['expected_D_exact'])<1e-10 and seat['p_D_at_least_51']==es['p_D_at_least_51'])
    c.update(all_candidates_and_scores_reconstructed=all(candidatecheck),all_reported_forecasts_reconstructed=all(recon),priors_frozen=all(frozen),reference_reproduced=all(reference),selectors_reconstructed=all(selection),past_only_selection=all(pastcheck),joint_seats_consistent=all(seatcheck),fixed_g_means_and_matched_t_covariance=all(meancheck),positive_covariance=all(positive),wave_zero_reproduces=all(zero),wave_monotonicity=all(monotone),waves_reconstructed=all(waverecon),custom_controls_reproduce_saved_scenarios=all(customok))
    result=dict(passed=all(c.values()),checks=c,forecast_rows=len(p),candidate_rows=len(cp));v1.json_write(out/'completion_audit.json',result)
    if not result['passed']:raise AssertionError([k for k,v in c.items() if not v])
    v1.manifest(out);return result


def report(out,lab):
    out,lab=Path(out),Path(lab);p=pd.read_parquet(out/'predictions.parquet');f=pd.read_parquet(out/'folds.parquet');cal=pd.read_parquet(out/'calibration.parquet');seats=pd.read_parquet(out/'seats.parquet');waves=pd.read_parquet(out/'waves.parquet')
    rows=[]
    for (sc,y,model),q in p[p.actual.notna()].groupby(['scenario','cycle','model']):
        rr=f[f.scenario.eq(sc)&f.cycle.eq(y)&f.model.eq(model)].iloc[0];e=(100*q.actual-q.prediction_pp).abs()
        rows.append(dict(scenario=sc,cycle=y,model=model,n=len(q),correct=int(((q.actual>0)==(q.prediction_pp>0)).sum()),mae_pp=float(e.mean()),joint_nll=rr.joint_nll,marginal_nll=float(-q.log_predictive_density.mean()),coverage70=float((100*q.actual).between(q.lo70_pp,q.hi70_pp).mean()),coverage95=float((100*q.actual).between(q.lo95_pp,q.hi95_pp).mean())))
    cycle=pd.DataFrame(rows);cycle.to_parquet(out/'cycle_scores.parquet',index=False)
    summary=[]
    for period,first in [('recent_2016_2024',2016),('tuned_2018_2024',2018),('all_2012_2024',2012)]:
        j=cycle[cycle.cycle.ge(first)].groupby(['scenario','model']).joint_nll.mean().reset_index();summary.append(cal[cal.period.eq(period)&cal.group.eq('all')].merge(j,on=['scenario','model'],validate='one_to_one'))
    summary=pd.concat(summary,ignore_index=True);summary.to_parquet(out/'summary.parquet',index=False)
    chamber=[]
    for (sc,model),q in seats[seats.cycle.between(2016,2024)].groupby(['scenario','model']):
        chamber.append(dict(scenario=sc,model=model,cycles=len(q),point_seat_mae=float((q.point_D-q.actual_D).abs().mean()),expected_seat_mae=float((q.expected_D_exact-q.actual_D).abs().mean()),coverage70=float(q.actual_D.between(q.D_lo70,q.D_hi70).mean()),coverage95=float(q.actual_D.between(q.D_lo95,q.D_hi95).mean())))
    chamber=pd.DataFrame(chamber);chamber.to_parquet(out/'chamber_scores.parquet',index=False)
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,axes=plt.subplots(1,2,figsize=(12,4.5))
    for ax,sc in zip(axes,['matched_live','oct31']):
        q=summary[summary.period.eq('recent_2016_2024')&summary.scenario.eq(sc)].set_index('model')
        for model in ['reference','common2','scale10_g0','t5_g0','all_selected']:
            ax.plot([50,70,80,95],[100*q.loc[model,'coverage'+str(n)] for n in [50,70,80,95]],marker='o',label=model)
        ax.plot([50,95],[50,95],'k--');ax.set(title='September horizon' if sc=='matched_live' else 'October 31',xlabel='Nominal interval (%)',ylabel='Observed coverage (%)');ax.legend(fontsize=8)
    fig.tight_layout();fig.savefig(out/'coverage.png',dpi=145);plt.close(fig)
    fig,ax=plt.subplots(figsize=(9,5))
    for model in ['reference','common2','national_selected','all_selected']:
        q=waves[waves.model.eq(model)].sort_values('wave_pp');ax.plot(q.wave_pp,q.expected_D_exact,marker='o',label=model)
    q=waves[waves.model.eq('reference')].sort_values('wave_pp');ax.fill_between(q.wave_pp,q.D_lo70,q.D_hi70,alpha=.15,label='Reference 70% range');ax.axhline(50,color='gray',linestyle='--');ax.axvline(0,color='gray',linestyle=':');ax.set(xlabel='Conditional D−R margin shift (pp): red ← 0 → blue',ylabel='Democratic-caucus Senate seats',title='2026 wave scenarios — frozen September 17 inputs');ax.legend();fig.tight_layout();fig.savefig(out/'waves.png',dpi=145);plt.close(fig)
    cols=['scenario','model','n','correct','mae_pp','brier','marginal_nll','joint_nll','coverage70','coverage95']
    text='# National error, scale uncertainty and waves — results\n\nFrozen September17 inputs. No promotion. See [design](NATIONAL_TAILS_WAVES.md) for exact assumptions. Covariance uncertainty is one common scalar only; correlation shape is fixed. t5_matched is a covariance-preserving predictive sensitivity. The national SD tunes polling-error uncertainty; the wave delta is an external uniform shift in final margins, not a fitted forecast or a probability of a wave.\n\n'
    text+='## Review conclusion\n\nKeep the reference and fixed Gaussian common2 challenger. At g2, covariance-matched t5 improves recent joint NLL3.623→3.450 earlier and3.217→3.176 late, but70%coverage falls67.9→59.3% and69.3→60.7%. A heavy-tailed distribution with fixed variance can concentrate more mass centrally and in extremes. The scale10/g0 model instead lowers95%coverage92.1→85.0% earlier and92.1→78.6% late: the inferred global scale becomes too small for held-out outcomes. This is a failure of this restrictive scale recipe, not proof covariance uncertainty is irrelevant.\n\nGaussian national selection improves earlier MAE6.980→6.858 but worsens lateMAE5.250→5.313; late expected-seat MAE worsens1.288→1.925. Some older folds choose the maximum tested6pp SD, so the volatility estimate is not precise. Current Gaussian selection chooses4pp; the all-family selector chooses matched-t/g2. Current reference remains49Dpoint/48.481expected/70%47–50; matched-t/g2 has47Dpoint/48.099expected/46–50. No model is promoted.\n\nReference conditional wave shifts−2/0/+2 yield47.126/48.481/49.904expectedD seats, respectively. These scenarios receive no probability. The notebook includes separate editable national-error SD and final-margin wave controls, with per-state results.\n\n'
    for period in ['recent_2016_2024','tuned_2018_2024','all_2012_2024']:
        text+='## '+period+'\n\n'+summary[summary.period.eq(period)][cols].round(4).to_markdown(index=False)+'\n\n'
    text+='## Per-cycle results\n\n'+cycle.round(4).to_markdown(index=False)+'\n\n'
    text+='## Selection and scale diagnostics\n\nThe inferred national-error mean is positive for Democratic overpolling. For the matched-t predictive sensitivity its national-error diagnostic belongs to the underlying Gaussian fit, not a separately fitted latent t error.\n\n'+f[['scenario','cycle','model','family','national_sd','df','scale_mean','national_error_mean_pp','national_error_sd_pp','validation_cycles','status']].round(4).to_markdown(index=False)+'\n\n'
    text+='## Recent chamber performance\n\nFive cycles per horizon; intervals remain conditional on existing unmodeled-seat completions.\n\n'+chamber.round(4).to_markdown(index=False)+'\n\n'
    text+='## Current forecasts\n\n'+seats[seats.cycle.eq(2026)][['model','point_D','point_R','expected_D_exact','D_lo70','D_hi70','D_lo95','D_hi95','p_D_at_least_51','p_D_exactly_50']].round(4).to_markdown(index=False)+'\n\n'
    text+='## Conditional reference wave scenarios\n\nNo probability assigned to these scenarios. +2 means +2 margin points, not +2 Democratic vote-share points. Continuing seats and unmodeled completions fixed.\n\n'+waves[waves.model.eq('reference')][['wave_pp','point_D','point_R','expected_D_exact','D_lo70','D_hi70','D_lo95','D_hi95','p_D_at_least_51','p_D_exactly_50','unmodeled_contested']].round(4).to_markdown(index=False)+'\n\n'
    text+='## Boundaries\n\nOne shared scale cannot identify full covariance-estimation or selection uncertainty. Scaling prior and all observation errors together is restrictive. Means and winner calls are identical at fixed national SD, so heavier tails alone cannot fix mean bias. The national SD remains a predictive discrepancy, overlapping baseline error. Selection is strictly chronological but these extensively explored historical folds are not a pristine final test. Scenarios apply equal shifts to modeled contests and do not claim equal real-world state responses.\n'
    (lab/'NATIONAL_TAILS_WAVES_RESULTS.md').write_text(text);(out/'NATIONAL_TAILS_WAVES_RESULTS.md').write_text(text);v1.manifest(out)


if __name__=='__main__':build(Path(__file__).resolve().parents[1])
