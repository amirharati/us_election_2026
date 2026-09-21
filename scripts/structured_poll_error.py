"""Firm overlap, shared-cycle discrepancy and aggregate time-dependent discrepancy."""
from pathlib import Path
from datetime import datetime,timezone
from itertools import product
import json
import numpy as np
import pandas as pd
from scipy.stats import norm
import simple_bayesian_polling as v1
import poll_update_review as previous

SOURCE='20260919T181021.670795Z'
GRID=list(product([0.,2.,4.],[0.,.5,1.],[0.,2.,4.]))
CONFIG=dict(common_sd_pp=[0.,2.,4.],firm_rho=[0.,.5,1.],drift_sd_30d_pp=[0.,2.,4.],
            priors=previous.PRIORS,poll_half_life_days=30.,draws=20000,seed=192109,
            validation_cycles=3,selection_score='equal_cycle_mean_joint_gaussian_nll_per_state',as_of='2026-09-17')


def brownian_mass(weights,leads):
    """Exact w' min(lead_i,lead_j) w; no dense sample covariance allocation."""
    w=np.asarray(weights,float);t=np.asarray(leads,float)
    if len(w)!=len(t) or not np.isfinite(w).all() or not np.isfinite(t).all() or (w<0).any() or (t<0).any():
        raise ValueError('Invalid drift weights/times')
    order=np.argsort(t);w=w[order];t=t[order]
    later=np.cumsum(w[::-1])[::-1]-w
    return float(np.sum(t*w*(w+2*later)))


def information(test,samples):
    sample_groups=dict(tuple(samples[samples.target_id.isin(test.target_id)].groupby('target_id')))
    if samples.duplicated(['target_id','sample_key']).any():raise ValueError('Duplicate target/sample')
    rows=[];firm_rows=[];allfirms=set();mapping={}
    for i,t in enumerate(test.itertuples()):
        q=sample_groups.get(t.target_id);mass=0.;poll=np.nan;neff=0.;drift=0.;age=np.nan;fw={}
        if q is not None and len(q):
            if q.age_days.lt(0).any() or not np.isfinite(q[['age_days','margin']]).all().all():raise ValueError('Invalid poll age/margin')
            dates=pd.to_datetime(q.field_end);cutoffs=pd.to_datetime(q.cutoff)
            if (dates>cutoffs).any() or (pd.to_datetime(q.available_date)>cutoffs).any():raise ValueError('Future poll admitted')
            w=np.exp2(-q.age_days.to_numpy(float)/30.)/q.groupby('firm').firm.transform('size').to_numpy()
            mass=float(w.sum());u=w/mass;poll=float(100*np.dot(u,q.margin))
            keys=[str(x) if str(x).strip().lower() not in ['', 'unknown','nan','none','null'] else 'unknown:'+str(t.target_id) for x in q.firm]
            for k,a in zip(keys,w):fw[k]=fw.get(k,0.)+float(a)
            if max(fw.values())>1+1e-12:raise AssertionError('Firm mass exceeds one')
            fw={k:a/mass for k,a in fw.items()};allfirms.update(fw)
            neff=1/sum(v*v for v in fw.values())
            age=float(np.dot(u,q.age_days))
            leads=(pd.Timestamp(t.election_date)-dates).dt.total_seconds().to_numpy()/86400
            drift=brownian_mass(u,leads)/30.
            for k,a in fw.items():firm_rows.append(dict(target_id=t.target_id,geography=t.geography,firm=k,normalized_weight=a))
        mapping[i]=fw
        rows.append(dict(target_id=t.target_id,geography=t.geography,firm_mass=mass,q_pp=poll,
                         samples=0 if q is None else len(q),firms=len(fw),effective_firms=neff,
                         weighted_age_days=age,drift_mass_30d=drift))
    firms=sorted(allfirms);indices={k:i for i,k in enumerate(firms)};u=np.zeros((len(test),len(firms)))
    for i,fw in mapping.items():
        for k,w in fw.items():u[i,indices[k]]=w
    table=pd.DataFrame(rows)
    if not np.allclose(table.q_pp,test.q_pp,equal_nan=True,atol=1e-9) or not np.allclose(table.firm_mass,test.firm_mass,atol=1e-12):
        raise AssertionError('Original aggregate not reproduced')
    return dict(weights=u,firms=np.array(firms,str),drift_mass=table.drift_mass_30d.to_numpy(),table=table,firm_table=pd.DataFrame(firm_rows))


def observation_covariance(test,poll,info,params):
    g,rho,d=params
    if g<0 or d<0 or not 0<=rho<=1:raise ValueError('Invalid structured parameters')
    si=np.array([v1.STATES.index(x) for x in test.geography]);obs=np.flatnonzero(test.q_pp.notna());so=si[obs]
    u=info['weights'][obs];overlap=u@u.T;diagonal=1/test.firm_mass.to_numpy()[obs]
    if (diagonal-np.diag(overlap)<-1e-10).any():raise ValueError('Invalid firm covariance remainder')
    fresh=16*(np.diag(diagonal)+rho*(overlap-np.diag(np.diag(overlap))))
    r=poll['covariance'][np.ix_(so,so)]+poll['bias_covariance'][np.ix_(so,so)]+fresh
    r+=g*g*np.ones((len(obs),len(obs)))+np.diag(d*d*info['drift_mass'][obs])
    return obs,so,r


def predict(test,k,poll,info,params):
    obs,so,r=observation_covariance(test,poll,info,params)
    mu=100*test.prior.to_numpy();values=test.q_pp.to_numpy()[obs]-poll['bias_mean'][so]
    mean,cov,_=v1.normal_update(mu,k,obs,values,r);sd=np.sqrt(np.diag(cov))
    p=test.copy();p['prediction_pp']=mean;p['prediction']=mean/100;p['posterior_sd_pp']=sd;p['p_dem']=norm.cdf(mean/sd)
    p['log_predictive_density']=norm.logpdf(100*p.actual,mean,sd)
    for level in [50,70,80,95]:
        z=norm.ppf((1+level/100)/2);p[f'lo{level}_pp']=mean-z*sd;p[f'hi{level}_pp']=mean+z*sd
    return p,cov


def joint_score(actual,mean,cov):
    actual=np.asarray(actual);obs=np.flatnonzero(np.isfinite(actual))
    if not len(obs):return np.nan
    c=cov[np.ix_(obs,obs)];e=actual[obs]-np.asarray(mean)[obs];l=np.linalg.cholesky(c);z=np.linalg.solve(l,e)
    return float(.5*(len(obs)*np.log(2*np.pi)+2*np.log(np.diag(l)).sum()+z@z)/len(obs))


def allowed(family):
    if family=='joint':return GRID
    index=['common','firm','drift'].index(family)
    return [p for p in GRID if all(p[i]==0 for i in range(3) if i!=index)]


def select(scores,year,family):
    choices=allowed(family)
    s=scores[(scores.cycle<year)&scores.params.isin(choices)]
    years=sorted(s.cycle.unique())[-3:]
    if len(years)<3:return (0.,0.,0.),years,'fallback_fewer_than_three_saved_cycles'
    s=s[s.cycle.isin(years)]
    if len(s)!=len(years)*len(choices) or s.duplicated(['cycle','params']).any():raise ValueError('Incomplete selection grid')
    values=s.groupby('params').joint_nll.mean().to_dict()
    if not np.isfinite(list(values.values())).all():raise ValueError('Invalid selection scores')
    p=min(values,key=lambda p:(values[p],sum(x!=0 for x in p),p))
    return tuple(p),years,'last_three_past_joint_scores'


def build(lab):
    lab=Path(lab).resolve();source=lab/'reports/prior_sensitivity'/SOURCE;source_sha=v1.verify(source)
    source_settings=json.loads((source/'settings.json').read_text());upstream=Path(source_settings['source']);upstream_sha=v1.verify(upstream)
    oldp=pd.read_parquet(source/'predictions.parquet');sf=pd.read_parquet(source/'folds.parquet');sf=sf[sf.model.isin(previous.PRIORS)]
    samples=pd.read_parquet(upstream/'samples.parquet');roster=pd.read_parquet(upstream/'full_seat_ledger.parquet')
    out=lab/'reports/structured_poll_error'/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')
    for n in ['information','forecasts','recipe']:(out/n).mkdir(parents=True,exist_ok=True)
    print('OUTPUT',out,flush=True)
    oldhash={p.name:v1.sha(p) for p in lab.glob('*.ipynb') if p.name!='STRUCTURED_POLL_ERROR.ipynb'}
    predictions=[];candidates=[];scores=[];tuning=[];folds=[];seats=[];info_rows=[];firm_rows=[];info_cache={}
    cols=['target_id','cycle','geography','actual','prior','q_pp','firm_mass','history_selection_10pp','scenario','election_date','n_samples','prior_history_n','prior_source_max_cycle']
    for (sc,pm),group in sf.groupby(['scenario','model']):
        for row in group.sort_values('cycle').itertuples():
            year=int(row.cycle);test=oldp[oldp.scenario.eq(sc)&oldp.cycle.eq(year)&oldp.model.eq(pm)][cols].sort_values('target_id').reset_index(drop=True)
            oldz=np.load(source/row.forecast_path);assert np.array_equal(oldz['target_ids'],test.target_id.to_numpy(str));k=oldz['prior_covariance']
            poll=dict(np.load(source/row.poll_path))
            if (sc,year) not in info_cache:
                info=information(test,samples[samples.scenario.eq(sc)]);info_cache[(sc,year)]=info
                info_rows.append(info['table'].assign(scenario=sc,cycle=year));firm_rows.append(info['firm_table'].assign(scenario=sc,cycle=year))
                np.savez_compressed(out/f'information/{sc}_{year}.npz',weights=info['weights'],firms=info['firms'],drift_mass=info['drift_mass'],target_ids=test.target_id.to_numpy(str))
            info=info_cache[(sc,year)];bank={}
            for params in GRID:
                pred,cov=predict(test,k,poll,info,params);bank[params]=(pred,cov)
                candidates.append(pred.assign(prior_model=pm,common_sd=params[0],firm_rho=params[1],drift_sd=params[2]))
            past=pd.DataFrame([r for r in scores if r['scenario']==sc and r['prior_model']==pm],columns=['scenario','prior_model','cycle','params','joint_nll','marginal_nll'])
            choices={'reference':((0.,0.,0.),[],'fixed'),'common_fixed2':((2.,0.,0.),[],'fixed'),
                     'firm_fixed_half':((0.,.5,0.),[],'fixed'),'drift_fixed2':((0.,0.,2.),[],'fixed')}
            for family in ['common','firm','drift','joint']:
                params,years,status=select(past,year,family);choices[family+'_selected']=(params,years,status)
                for r in past[past.cycle.isin(years)&past.params.isin(allowed(family))].to_dict('records'):
                    par=r.pop('params');tuning.append(dict(**r,common_sd=par[0],firm_rho=par[1],drift_sd=par[2],forecast_cycle=year,validation_cycle=r['cycle'],family=family,
                        selected_common=params[0],selected_firm=params[1],selected_drift=params[2],status=status))
            for params,(pred,cov) in bank.items():
                if year<2026:scores.append(dict(scenario=sc,prior_model=pm,cycle=year,params=params,joint_nll=joint_score(100*test.actual,pred.prediction_pp,cov),marginal_nll=float(-pred.log_predictive_density.mean())))
            normal=np.random.default_rng(CONFIG['seed']+year+10000*(sc=='oct31')).standard_normal((CONFIG['draws'],len(test)))
            for model,(params,years,status) in choices.items():
                pred,cov=bank[params];pred=pred.assign(prior_model=pm,model=model,common_sd=params[0],firm_rho=params[1],drift_sd=params[2]);predictions.append(pred)
                draws=pred.prediction_pp.to_numpy()+normal@np.linalg.cholesky(cov).T
                rr=roster[roster.scenario.eq(sc)&roster.cycle.eq(year)];seat=v1.seat_counts(rr,test,pred,draws);counts=seat['fixed_D']+(draws>0).sum(axis=1)
                lo,hi=np.quantile(counts,[.15,.85],method='inverted_cdf')
                seats.append(dict(scenario=sc,cycle=year,prior_model=pm,model=model,**seat,expected_D_exact=float(seat['fixed_D']+pred.p_dem.sum()),D_lo70=int(lo),D_hi70=int(hi)))
                path=f'forecasts/{sc}_{year}_{pm}_{model}.npz'
                np.savez_compressed(out/path,target_ids=test.target_id.to_numpy(str),means_pp=pred.prediction_pp.to_numpy(),posterior_covariance=cov,prior_covariance=k,seat_count_frequency=np.bincount(counts,minlength=101))
                folds.append(dict(scenario=sc,cycle=year,prior_model=pm,model=model,common_sd=params[0],firm_rho=params[1],drift_sd=params[2],validation_cycles=','.join(map(str,years)),status=status,
                    source_forecast=row.forecast_path,source_poll=row.poll_path,forecast_path=path,training_max_cycle=row.training_max_cycle,
                    joint_nll=joint_score(100*test.actual,pred.prediction_pp,cov)))
            print(sc,pm,year,'selected',choices['joint_selected'][0],flush=True)
    p=pd.concat(predictions,ignore_index=True);score_table=pd.DataFrame([{**{k:v for k,v in r.items() if k!='params'},'common_sd':r['params'][0],'firm_rho':r['params'][1],'drift_sd':r['params'][2]} for r in scores])
    tables=dict(predictions=p,candidate_predictions=pd.concat(candidates,ignore_index=True),calibration=previous.metrics(p),
        scores=score_table,tuning=pd.DataFrame(tuning),folds=pd.DataFrame(folds),seats=pd.DataFrame(seats),information=pd.concat(info_rows,ignore_index=True),firm_weights=pd.concat(firm_rows,ignore_index=True))
    for name,t in tables.items():t.to_parquet(out/(name+'.parquet'),index=False)
    v1.json_write(out/'settings.json',dict(config=CONFIG,source=str(source),source_sha256=source_sha,upstream=str(upstream),upstream_sha256=upstream_sha,
        old_notebook_hashes=oldhash,promotion=False,polling_refreshed=False,interpretation='Optional predictive discrepancy terms; not separately identified true shock/drift variances.'))
    for f in (lab/'scripts').glob('*.py'):(out/'recipe'/f.name).write_bytes(f.read_bytes())
    (out/'STRUCTURED_POLL_ERROR.md').write_bytes((lab/'STRUCTURED_POLL_ERROR.md').read_bytes());v1.manifest(out)
    audit(out,lab);report(out,lab);v1.json_write(out.parent/'latest.json',dict(artifact=out.name,manifest_sha256=v1.sha(out/'manifest.json')))
    return out


def audit(out,lab):
    out,lab=Path(out),Path(lab);v1.verify(out);s=json.loads((out/'settings.json').read_text());source=Path(s['source']);upstream=Path(s['upstream'])
    p=pd.read_parquet(out/'predictions.parquet');cp=pd.read_parquet(out/'candidate_predictions.parquet');folds=pd.read_parquet(out/'folds.parquet');scores=pd.read_parquet(out/'scores.parquet')
    scores['params']=list(zip(scores.common_sd,scores.firm_rho,scores.drift_sd));t=pd.read_parquet(out/'tuning.parquet');seats=pd.read_parquet(out/'seats.parquet')
    oldp=pd.read_parquet(source/'predictions.parquet');samples=pd.read_parquet(upstream/'samples.parquet');cache={};infook=[];con=[];recon=[];frozen=[];chosen=[];seatok=[];pdok=[];scoreok=[]
    c=dict(source_unchanged=v1.verify(source)==s['source_sha256'],upstream_unchanged=v1.verify(upstream)==s['upstream_sha256'],
        old_notebooks_unchanged=all(v1.sha(lab/n)==h for n,h in s['old_notebook_hashes'].items()),
        unique_forecasts=not p.duplicated(['scenario','prior_model','model','target_id']).any(),
        future_labels_blank=bool(p[p.cycle.eq(2026)].actual.isna().all() and cp[cp.cycle.eq(2026)].actual.isna().all()),
        base_training_past_only=bool(folds.training_max_cycle.lt(folds.cycle).all()),tuning_past_only=bool(t.validation_cycle.lt(t.forecast_cycle).all()),
        finite_forecasts=bool(np.isfinite(p[['prediction_pp','posterior_sd_pp','p_dem']]).all().all() and p.p_dem.between(0,1).all()),
        equal_cases=all(g.groupby('model').target_id.apply(frozenset).nunique()==1 for _,g in p.groupby(['scenario','cycle','prior_model'])))
    c['complete_unique_candidate_grid']=bool(not cp.duplicated(['scenario','cycle','prior_model','target_id','common_sd','firm_rho','drift_sd']).any() and
        cp.groupby(['scenario','cycle','prior_model','target_id']).size().eq(len(GRID)).all())
    cols=['prediction_pp','posterior_sd_pp','p_dem','lo70_pp','hi70_pp','lo95_pp','hi95_pp']
    for r in folds.itertuples():
        test=oldp[oldp.scenario.eq(r.scenario)&oldp.cycle.eq(r.cycle)&oldp.model.eq(r.prior_model)].sort_values('target_id').reset_index(drop=True)
        if (r.scenario,r.cycle) not in cache:
            info=information(test,samples[samples.scenario.eq(r.scenario)]);cache[(r.scenario,r.cycle)]=info
            z=np.load(out/f'information/{r.scenario}_{r.cycle}.npz')
            infook.append(all(np.array_equal(z[k],info[k]) for k in ['weights','firms','drift_mass']))
        info=cache[(r.scenario,r.cycle)];base=np.load(source/r.source_forecast);poll=dict(np.load(source/r.source_poll));z=np.load(out/r.forecast_path)
        params=(r.common_sd,r.firm_rho,r.drift_sd);expected,cov=predict(test,base['prior_covariance'],poll,info,params)
        q=p[p.scenario.eq(r.scenario)&p.cycle.eq(r.cycle)&p.prior_model.eq(r.prior_model)&p.model.eq(r.model)].sort_values('target_id')
        recon.append(np.allclose(expected[cols],q[cols],atol=1e-10) and np.allclose(cov,z['posterior_covariance']))
        frozen.append(np.array_equal(q.prior.to_numpy(),test.prior.to_numpy()) and np.array_equal(z['prior_covariance'],base['prior_covariance']))
        if r.model=='reference':con.append(np.allclose(q[cols],test[cols],atol=1e-10))
        pdok.append(np.linalg.eigvalsh(cov).min()>0)
        if r.model.endswith('_selected'):
            selected,years,status=select(scores[scores.scenario.eq(r.scenario)&scores.prior_model.eq(r.prior_model)],r.cycle,r.model.removesuffix('_selected'))
            chosen.append((selected,','.join(map(str,years)),status)==(params,r.validation_cycles,r.status))
        seat=seats[seats.scenario.eq(r.scenario)&seats.cycle.eq(r.cycle)&seats.prior_model.eq(r.prior_model)&seats.model.eq(r.model)].iloc[0]
        seatok.append(z['seat_count_frequency'].sum()==CONFIG['draws'] and abs(seat.expected_D_exact-seat.fixed_D-q.p_dem.sum())<1e-10 and seat.point_D==seat.fixed_D+(q.prediction_pp>0).sum())
    # Reconstruct every candidate and the joint objective driving selection.
    for (sc,year,pm,g,rho,d),q in cp.groupby(['scenario','cycle','prior_model','common_sd','firm_rho','drift_sd']):
        q=q.sort_values('target_id').reset_index(drop=True);ref=folds[folds.scenario.eq(sc)&folds.cycle.eq(year)&folds.prior_model.eq(pm)].iloc[0]
        k=np.load(source/ref.source_forecast)['prior_covariance'];poll=dict(np.load(source/ref.source_poll))
        expected,cov=predict(q,k,poll,cache[(sc,year)],(g,rho,d));ok=np.allclose(expected[cols],q[cols],atol=1e-10)
        if year<2026:
            sr=scores[scores.scenario.eq(sc)&scores.cycle.eq(year)&scores.prior_model.eq(pm)&scores.common_sd.eq(g)&scores.firm_rho.eq(rho)&scores.drift_sd.eq(d)].iloc[0]
            ok=ok and abs(joint_score(100*q.actual,q.prediction_pp,cov)-sr.joint_nll)<1e-10 and abs(-q.log_predictive_density.mean()-sr.marginal_nll)<1e-10
        scoreok.append(ok)
    c.update(aggregate_and_firm_information_reconstructed=all(infook),reference_reproduces=all(con),all_forecasts_reconstructed=all(recon),
        election_priors_frozen=all(frozen),selection_reconstructed=all(chosen),joint_seat_accounting=all(seatok),positive_posterior_covariances=all(pdok),
        candidates_and_joint_scores_reconstructed=all(scoreok))
    result=dict(passed=all(c.values()),checks=c,forecast_rows=len(p),candidate_rows=len(cp));v1.json_write(out/'completion_audit.json',result)
    if not result['passed']:raise AssertionError([k for k,v in c.items() if not v])
    v1.manifest(out);return result


def report(out,lab):
    out,lab=Path(out),Path(lab);p=pd.read_parquet(out/'predictions.parquet');cal=pd.read_parquet(out/'calibration.parquet');folds=pd.read_parquet(out/'folds.parquet');seats=pd.read_parquet(out/'seats.parquet')
    rows=[]
    for (sc,y,pm,model),q in p[p.actual.notna()].groupby(['scenario','cycle','prior_model','model']):
        e=100*q.actual-q.prediction_pp;f=folds[folds.scenario.eq(sc)&folds.cycle.eq(y)&folds.prior_model.eq(pm)&folds.model.eq(model)].iloc[0]
        rows.append(dict(scenario=sc,cycle=y,prior_model=pm,model=model,n=len(q),correct=int(((q.prediction_pp>0)==(q.actual>0)).sum()),
            mae_pp=float(e.abs().mean()),marginal_nll=float(-q.log_predictive_density.mean()),joint_nll=f.joint_nll,
            coverage70=float((e.abs()<=1.0364333894937898*q.posterior_sd_pp).mean()),coverage95=float((e.abs()<=1.959963984540054*q.posterior_sd_pp).mean())))
    cycle=pd.DataFrame(rows);cycle.to_parquet(out/'cycle_scores.parquet',index=False)
    baseline=cycle[cycle.model.eq('reference')][['scenario','cycle','prior_model','mae_pp','correct','joint_nll','marginal_nll']]
    paired=cycle.merge(baseline,on=['scenario','cycle','prior_model'],suffixes=('','_reference'),validate='many_to_one')
    for name in ['mae_pp','correct','joint_nll','marginal_nll']:paired['delta_'+name]=paired[name]-paired[name+'_reference']
    paired.to_parquet(out/'paired_cycle_changes.parquet',index=False)
    base=p[p.model.eq('reference')][['scenario','prior_model','target_id','prediction_pp']]
    changed=p.merge(base,on=['scenario','prior_model','target_id'],suffixes=('','_reference'),validate='many_to_one')
    changed=changed[((changed.prediction_pp>0)!=(changed.prediction_pp_reference>0))&changed.actual.notna()].copy()
    changed['was_correct']=(changed.prediction_pp_reference>0)==(changed.actual>0);changed['now_correct']=(changed.prediction_pp>0)==(changed.actual>0)
    changed['actual_pp']=100*changed.actual
    changed[['scenario','cycle','geography','prior_model','model','actual_pp','prediction_pp_reference','prediction_pp','was_correct','now_correct']].to_parquet(out/'changed_calls.parquet',index=False)
    summary=[]
    for period,first in [('recent_2016_2024',2016),('tuned_2018_2024',2018),('all_2012_2024',2012)]:
        j=cycle[cycle.cycle.ge(first)].groupby(['scenario','prior_model','model']).joint_nll.mean().reset_index()
        summary.append(cal[cal.period.eq(period)&cal.group.eq('all')].merge(j,on=['scenario','prior_model','model'],validate='one_to_one'))
    summary=pd.concat(summary,ignore_index=True);summary.to_parquet(out/'summary.parquet',index=False)
    chamber=[]
    for (sc,pm,model),g in seats[seats.cycle.between(2016,2024)].groupby(['scenario','prior_model','model']):
        chamber.append(dict(scenario=sc,prior_model=pm,model=model,cycles=len(g),seat_count_mae=float((g.point_D-g.actual_D).abs().mean()),
            expected_seat_mae=float((g.expected_D_exact-g.actual_D).abs().mean()),coverage70=float(g.actual_D.between(g.D_lo70,g.D_hi70).mean()),coverage95=float(g.actual_D.between(g.D_lo95,g.D_hi95).mean())))
    chamber=pd.DataFrame(chamber);chamber.to_parquet(out/'chamber_scores.parquet',index=False)
    current=p[p.cycle.eq(2026)&p.prior_model.eq('control_state')];table=current.pivot(index='geography',columns='model',values='prediction_pp')
    table=table.join(current[current.model.eq('reference')].set_index('geography')[['q_pp','prior']]);table['prior_pp']=100*table.pop('prior');table.reset_index().to_parquet(out/'current_states.parquet',index=False)
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,axes=plt.subplots(1,2,figsize=(12,4.5))
    for ax,sc in zip(axes,['matched_live','oct31']):
        q=summary[summary.period.eq('recent_2016_2024')&summary.prior_model.eq('control_state')&summary.scenario.eq(sc)].set_index('model')
        for name in ['reference','common_selected','firm_selected','drift_selected','joint_selected']:
            ax.plot([50,70,80,95],[100*q.loc[name,'coverage'+str(n)] for n in [50,70,80,95]],marker='o',label=name)
        ax.plot([50,95],[50,95],'k--');ax.set(title=sc,xlabel='Nominal interval (%)',ylabel='Observed coverage (%)');ax.legend(fontsize=8)
    fig.tight_layout();fig.savefig(out/'coverage.png',dpi=145);plt.close(fig)
    info=pd.read_parquet(out/'information.parquet');q=info[info.cycle.eq(2026)&info.firm_mass.gt(0)].sort_values('effective_firms')
    overlaps=[]
    for (sc,year),group in info.groupby(['scenario','cycle']):
        z=np.load(out/f'information/{sc}_{year}.npz');u=z['weights'];dot=u@u.T
        table_info=group.set_index('target_id').loc[z['target_ids']]
        for i in range(len(u)):
            for j in range(i):
                if dot[i,j]>0:
                    overlaps.append(dict(scenario=sc,cycle=year,state_a=table_info.geography.iloc[i],state_b=table_info.geography.iloc[j],
                        shared_firms=int(((u[i]>0)&(u[j]>0)).sum()),overlap=float(dot[i,j]),
                        fresh_error_correlation_at_rho1=float(dot[i,j]*np.sqrt(table_info.firm_mass.iloc[i]*table_info.firm_mass.iloc[j]))))
    overlap_table=pd.DataFrame(overlaps);overlap_table.to_parquet(out/'firm_overlap.parquet',index=False)
    fig,ax=plt.subplots(figsize=(10,6));x=np.arange(len(q));ax.barh(x-.18,q.firm_mass,height=.35,label='age-decayed firm mass');ax.barh(x+.18,q.effective_firms,height=.35,label='Kish effective firms');ax.set_yticks(x,q.geography);ax.legend();ax.set(xlabel='Distinct information summaries, not sample size',title='2026 polling firm information');fig.tight_layout();fig.savefig(out/'firm_information.png',dpi=145);plt.close(fig)
    cols=['scenario','model','n','correct','mae_pp','brier','marginal_nll','joint_nll','coverage70','coverage95']
    text='# Structured polling error — results\n\nFrozen September17,2026 inputs. Election priors, aggregate polls, bias and baseline residual covariance unchanged. Test optional common-cycle discrepancy, cross-state firm links with unchanged fresh-noise marginals, and extra Brownian time discrepancy. Zero settings preserve the original model. No automatic promotion.\n\n'
    text+='Shared/time terms are additional predictive discrepancy, since baseline polling-to-final covariance already contains some shared and temporal error. They are not separately identified physical components. Firms are linked by existing normalized names, not verified shared panels. All changes update the likelihood and can move the mean toward or away from the historical prior.\n\n'
    text+='Selection uses the last three earlier saved cycles\' joint Gaussian NLL per state, equally averaged by cycle. First selected test2018; earlier tests use zero. This objective explicitly values cross-state dependence and differs from the earlier marginal penalty selector. Report both objectives.\n\n'
    text+='## Review conclusion\n\nA fixed2pp common discrepancy is a useful challenger, not an automatically promoted model. With the reference prior it improves recent September MAE6.9802→6.9090, keeps129/140calls, and improves95%coverage92.14→93.57%. October MAE improves5.2503→5.2177 and calls131→133;70%coverage improves65.71→69.29%,95%stays92.14%. Joint and marginal scores improve at both horizons. The extra late calls are FL2018 and NC2020, both close margins; earlier it loses NV2018 and gains NC2020. Across the two other frozen priors it also improves MAE/joint score at both horizons, but calls/coverage vary.\n\nSelecting larger common/time terms is less consistent. Joint selection improves earlier MAE to6.7863 and keeps129calls, but late MAE worsens to5.2798 despite133calls. Same-firm links have small effects; selected firm links slightly improve MAE/joint score, lose one earlier call and gain one late call. The added time term does not clearly improve the forecast. These are additional discrepancies beyond an existing historical polling-error covariance, so a weak time result is not evidence that voter movement is absent.\n\nFull chamber checks remain mixed: fixed common2 improves individual late calls but worsens expected-seat MAE1.288→1.479 across five cycles. All displayed95%chamber ranges cover all five recent outcomes under existing completion assumptions; that sample is far too small to establish calibration. Keep the reference and retain common2 as a bounded challenger rather than choosing the27-setting search winner.\n\nCurrent reference is49D/51R by calls,48.481expectedD,70%47–50D. Common2 gives47D/53R,48.105expectedD,70%46–50D: AK movesD+0.608→R+0.236 and MI D+0.018→R+0.425. These two near-zero crossings do not imply a confident two-seat difference. Current joint selection chooses(g=4,rho=1,d=4), with47Dpoint/47.657expected/70%46–50D; it remains experimental.\n\n'
    for period in ['recent_2016_2024','tuned_2018_2024','all_2012_2024']:
        text+='## '+period+' — reference prior\n\n'+summary[summary.period.eq(period)&summary.prior_model.eq('control_state')][cols].round(4).to_markdown(index=False)+'\n\n'
    text+='## Recent results under prior challengers\n\n'+summary[summary.period.eq('recent_2016_2024')][['prior_model']+cols].round(4).to_markdown(index=False)+'\n\n'
    text+='## Reference-prior subgroups\n\n'+cal[cal.period.eq('recent_2016_2024')&cal.prior_model.eq('control_state')&cal.group.ne('all')][['scenario','group','model','n','correct','mae_pp','marginal_nll','coverage95']].round(4).to_markdown(index=False)+'\n\n'
    text+='## Per-cycle scores\n\n'+cycle[cycle.prior_model.eq('control_state')].round(4).to_markdown(index=False)+'\n\n'
    text+='## Changed winner calls from the reference\n\n'+changed[changed.prior_model.eq('control_state')&changed.cycle.ge(2016)&changed.model.isin(['common_fixed2','firm_selected','joint_selected'])][['scenario','cycle','geography','model','actual_pp','prediction_pp_reference','prediction_pp','was_correct','now_correct']].round(3).to_markdown(index=False)+'\n\n'
    text+='## Selection trace\n\n'+folds[folds.prior_model.eq('control_state')][['scenario','cycle','model','common_sd','firm_rho','drift_sd','validation_cycles','status']].to_markdown(index=False)+'\n\n'
    text+='## Recent chamber checks\n\nOnly five cycles per horizon; horizons are not independent. Full-roster actual counts include outcomes of unmodeled contests whose forecasts retain prior completion assumptions. These few intervals cannot establish calibrated chamber-control probabilities.\n\n'+chamber[chamber.prior_model.eq('control_state')].round(4).to_markdown(index=False)+'\n\n'
    text+='## Current full chamber scenarios\n\nD includes Democratic-caucusing independents, continuing seats and existing completions; ballot/runoff assumptions remain.\n\n'+seats[seats.cycle.eq(2026)][['prior_model','model','point_D','point_R','expected_D_exact','D_lo70','D_hi70','D_lo95','D_hi95']].round(3).to_markdown(index=False)+'\n\n'
    text+='## Current states\n\n'+table.round(3).to_markdown()+'\n\n'
    text+='## Current firm and poll-age information\n\n'+info[info.cycle.eq(2026)].round(3).to_markdown(index=False)+'\n\n'
    text+='## Current firm overlap\n\nTop20pairs by implied correlation in the fresh-firm noise component at rho1. This is not the total polling-error correlation, and not a verified panel overlap measure.\n\n'+overlap_table[overlap_table.cycle.eq(2026)].sort_values('fresh_error_correlation_at_rho1',ascending=False).head(20).round(4).to_markdown(index=False)+'\n\n'
    text+='## Limits\n\nExisting covariance/bias estimation and selected-hyperparameter uncertainty remain omitted. Added common/temporal terms may overlap effects already in the baseline; zero is an explicit option. Fixed residual correlation patterns can be wrong. The firm-link model preserves within-state noise and only links observed states sharing named firms. The time term is a zero-mean discrepancy assumption, not an estimated direction of voter movement. No full longitudinal state-space model or election-day data refresh is performed. All historical model comparisons are exploratory.\n'
    (out/'STRUCTURED_POLL_ERROR_RESULTS.md').write_text(text);(lab/'STRUCTURED_POLL_ERROR_RESULTS.md').write_text(text)
    (out/'recipe'/Path(__file__).name).write_bytes(Path(__file__).read_bytes());v1.manifest(out);return out


if __name__=='__main__':build(Path(__file__).resolve().parents[1])
