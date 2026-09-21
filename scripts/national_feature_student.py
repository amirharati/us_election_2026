"""Matched Student polling likelihood on frozen chronological feature priors."""
from pathlib import Path
from datetime import datetime, timezone
import json
import numpy as np
import pandas as pd
import simple_bayesian_polling as v1
import simple_national_model as normal
import student_polling_likelihood as student
import poll_timing_student as timing
import coverage_balance as scoring
import national_factor_review as national
import national_tails_waves as chamber

SOURCE='20260920T013619.322700Z'
FAMILIES=['none','momentum','approval','both']
DISTS={'gaussian':0,'student5':5,'student10':10}
CONFIG=dict(draws=30000,seed=197139,validation_cycles=3,df=[0,5,10],as_of='2026-09-17',half_life_days=30)


def predict(test,prior_mean,k,poll,df,**kwargs):
    # The existing likelihood API reads prior in fractional D-R units.
    shifted=test.assign(prior=np.asarray(prior_mean)/100)
    d=student.fit(shifted,k,poll,df=df,**kwargs)
    p=timing.student_summary(test,d)
    p['feature_shifted_prior_pp']=prior_mean
    p=p.drop(columns=[c for c in ['national_movement_pp','local_electoral_update_pp'] if c in p])
    return p,d


def build(lab):
    lab=Path(lab).resolve();source=lab/'reports/national_feature_prior'/SOURCE
    st=json.loads((source/'settings.json').read_text());working=Path(st['source']);up=Path(st['upstream'])
    out=lab/'reports/national_feature_student'/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')
    for sub in ['forecasts','recipe']:(out/sub).mkdir(parents=True,exist_ok=True)
    settings=dict(config=CONFIG,source=str(source),working=str(working),upstream=str(up),sources={str(x):v1.verify(x) for x in [source,working,up]},working_sha256=v1.sha(lab/'WORKING_MODEL.json'),old_notebook_hashes={x.name:v1.sha(x) for x in lab.glob('*.ipynb') if x.name!='NATIONAL_FEATURE_STUDENT.ipynb'},data_refreshed=False,promotion=False)
    v1.json_write(out/'settings.json',settings)
    orig=pd.read_parquet(source/'predictions.parquet');fold=pd.read_parquet(source/'folds.parquet');roster=pd.read_parquet(up/'full_seat_ledger.parquet')
    predictions=[];seats=[];folds=[];checks=[];reproductions=[]
    print('OUTPUT',out,flush=True)
    for (sc,year),ff in fold.groupby(['scenario','cycle']):
        pf=np.load(working/f'fits/{sc}_{year}_poll.npz');poll=normal.fixed_common(pf['training_values'],pf['training_noise'],pf['training_weights'],pf['budget'],0.,9.)
        for r in ff.itertuples():
            family=r.model;test=orig[orig.scenario.eq(sc)&orig.cycle.eq(year)&orig.model.eq(family)].sort_values('target_id').reset_index(drop=True)
            prior=np.load(source/r.forecast_path);mu=prior['prior_mean'];k=prior['prior_covariance']
            rng=np.random.default_rng(CONFIG['seed']+year+10000*(sc=='oct31'));z=rng.standard_normal((CONFIG['draws'],len(test)));u=rng.random(CONFIG['draws'])
            for dist,df in DISTS.items():
                p,d=predict(test,mu,k,poll,df);name=f'{family}_{dist}';p=p.assign(model=name,family=family,distribution=dist,df=df);predictions.append(p)
                if not df:
                    cols=['prediction_pp','p_dem','lo70_pp','hi95_pp'];reproductions.append(bool(np.allclose(p[cols],test[cols],atol=1e-8) and np.allclose(d['covariance'],prior['covariance'])))
                else:
                    for label,nodes,bound in [('double_nodes',513,16.),('wider_domain',321,20.)]:
                        shifted=test.assign(prior=mu/100);other=student.fit(shifted,k,poll,df=df,nodes=nodes,bound=bound)
                        checks.append(dict(scenario=sc,cycle=year,model=name,check=label,edge_mass=d['edge_mass'],prior_grid_mass=d['prior_grid_mass'],**student.integration_check(test,d,other)))
                draws=student.sample(d,z,u);ss,counts=chamber.seat_summary(roster[roster.scenario.eq(sc)&roster.cycle.eq(year)],test,p,draws);freq=np.bincount(counts,minlength=101)
                if not df:reproductions.append(bool(np.array_equal(freq,prior['seat_count_frequency'])))
                seats.append(scoring.seat_scores(dict(ss,scenario=sc,cycle=year,model=name,family=family,distribution=dist,df=df),freq))
                path=f'forecasts/{sc}_{year}_{name}.npz'
                np.savez_compressed(out/path,target_ids=test.target_id.to_numpy(str),prior_mean=mu,prior_covariance=k,seat_count_frequency=freq,**{x:d[x] for x in ['mean','covariance','means','covs','weights','scales']})
                folds.append(dict(scenario=sc,cycle=year,model=name,family=family,distribution=dist,df=df,feature_tau=r.tau,source_fit_path=r.fit_path,source_forecast_path=r.forecast_path,forecast_path=path,scale_mean=d['scale_mean'],p_scale_gt1=d['p_scale_gt1'],log_evidence=d['log_evidence']))
        print(sc,year,'four families x three distributions complete',flush=True)
    p=pd.concat(predictions,ignore_index=True);s=pd.DataFrame(seats);f=pd.DataFrame(folds);trace=[];pp=[];ss=[];ff=[]
    for (sc,year,family),group in p.groupby(['scenario','cycle','family']):
        order=[f'{family}_{x}' for x in DISTS];chosen,years,status=timing.choose(s[s.scenario.eq(sc)],year,order)
        for table,dest in [(p,pp),(s,ss),(f,ff)]:dest.append(table[table.scenario.eq(sc)&table.cycle.eq(year)&table.model.eq(chosen)].assign(model=f'{family}_selected',selected_model=chosen))
        for candidate in order:
            q=s[s.scenario.eq(sc)&s.cycle.isin(years)&s.model.eq(candidate)];trace.append(dict(scenario=sc,forecast_cycle=year,family=family,candidate=candidate,selected_model=chosen,validation_cycles=','.join(map(str,years)),status=status,validation_crps=q.seat_crps.mean()))
    p=pd.concat([p,*pp],ignore_index=True);s=pd.concat([s,*ss],ignore_index=True);f=pd.concat([f,*ff],ignore_index=True)
    cyc=p[p.actual.notna()].groupby(['scenario','cycle','model'],as_index=False).agg(n=('actual','size'),correct=('correct','sum'),mae_pp=('absolute_error_pp','mean'),wis_pp=('wis_pp','mean'),brier=('brier','mean'))
    tables=dict(predictions=p,seats=s,folds=f,tuning=pd.DataFrame(trace),integration_checks=pd.DataFrame(checks),summary=scoring.summarize_scores(p),chamber_summary=national.chamber_summary(s),cycle_scores=cyc)
    for name,table in tables.items():table.to_parquet(out/f'{name}.parquet',index=False)
    v1.json_write(out/'reproduction.json',dict(passed=all(reproductions),checks=len(reproductions)))
    for path in (lab/'scripts').glob('*.py'):(out/'recipe'/path.name).write_bytes(path.read_bytes())
    (out/'NATIONAL_FEATURE_STUDENT.md').write_bytes((lab/'NATIONAL_FEATURE_STUDENT.md').read_bytes())
    v1.manifest(out);audit(out,lab);report(out,lab);v1.manifest(out)
    v1.json_write(out.parent/'latest.json',dict(artifact=out.name,manifest_sha256=v1.verify(out)))
    print('COMPLETE',out,flush=True);return out


def audit(out,lab):
    out,lab=Path(out),Path(lab);v1.verify(out);st=json.loads((out/'settings.json').read_text());src=Path(st['source']);working=Path(st['working'])
    p=pd.read_parquet(out/'predictions.parquet');s=pd.read_parquet(out/'seats.parquet');f=pd.read_parquet(out/'folds.parquet');t=pd.read_parquet(out/'tuning.parquet');i=pd.read_parquet(out/'integration_checks.parquet');orig=pd.read_parquet(src/'predictions.parquet')
    c=dict(sources_unchanged=all(v1.verify(x)==h for x,h in st['sources'].items()),old_notebooks_preserved=all(v1.sha(lab/x)==h for x,h in st['old_notebook_hashes'].items()),working_unchanged=v1.sha(lab/'WORKING_MODEL.json')==st['working_sha256'],gaussian_reproduces=json.loads((out/'reproduction.json').read_text())['passed'],unique_forecasts=not p.duplicated(['scenario','target_id','model']).any(),current_labels_missing=bool(p[p.cycle.eq(2026)][['actual','wis_pp','brier']].isna().all().all() and s[s.cycle.eq(2026)][['actual_D','seat_crps']].isna().all().all()),integration_converged=bool(i.max_mean_difference_pp.lt(1e-5).all() and i.max_probability_difference.lt(1e-7).all() and i.relative_covariance_difference.lt(1e-6).all() and i.joint_nll_difference.lt(1e-7).all()),integration_mass=bool(i.edge_mass.lt(1e-8).all() and (i.prior_grid_mass-1).abs().lt(1e-8).all()),zero_shared_error=bool(p.national_poll_error_pp.eq(0).all()))
    recon=[];frozen=[];seatok=[];mass=[];chrono=[];selection=[];pollcache={}
    for r in f[~f.model.str.endswith('_selected')].itertuples():
        q=p[p.scenario.eq(r.scenario)&p.cycle.eq(r.cycle)&p.model.eq(r.model)].sort_values('target_id').reset_index(drop=True);old=orig[orig.scenario.eq(r.scenario)&orig.cycle.eq(r.cycle)&orig.model.eq(r.family)].sort_values('target_id').reset_index(drop=True);z=np.load(out/r.forecast_path);g=np.load(src/r.source_forecast_path);fit=np.load(src/r.source_fit_path)
        chrono.append(fit['years'].max()<r.cycle)
        key=(r.scenario,r.cycle)
        if key not in pollcache:
            pf=np.load(working/f'fits/{r.scenario}_{r.cycle}_poll.npz');pollcache[key]=normal.fixed_common(pf['training_values'],pf['training_noise'],pf['training_weights'],pf['budget'],0.,9.)
        expected,d=predict(old,g['prior_mean'],g['prior_covariance'],pollcache[key],r.df)
        cols=['prediction_pp','p_dem','lo70_pp','hi95_pp'];recon.append(np.allclose(q[cols],expected[cols],atol=1e-9) and np.allclose(z['covariance'],d['covariance']))
        frozen.append(np.array_equal(g['prior_mean'],z['prior_mean']) and np.array_equal(g['prior_covariance'],z['prior_covariance']) and all(np.array_equal(q[x],old[x],equal_nan=True) for x in ['prior','q_pp','actual','historical_bias_pp','firm_mass']))
        mass.append(abs(z['weights'].sum()-1)<1e-10 and np.linalg.eigvalsh(z['covariance']).min()>0)
        sr=s[s.scenario.eq(r.scenario)&s.cycle.eq(r.cycle)&s.model.eq(r.model)].iloc[0];seatok.append(z['seat_count_frequency'].sum()==CONFIG['draws'] and abs(sr.expected_D_exact-sr.fixed_D-q.p_dem.sum())<1e-9 and sr.point_D==sr.fixed_D+q.prediction_pp.gt(0).sum())
    for r in t.drop_duplicates(['scenario','forecast_cycle','family']).itertuples():
        chosen,years,status=timing.choose(s[s.scenario.eq(r.scenario)],r.forecast_cycle,[f'{r.family}_{x}' for x in DISTS]);qa=p[p.scenario.eq(r.scenario)&p.cycle.eq(r.forecast_cycle)&p.model.eq(f'{r.family}_selected')].sort_values('target_id');qb=p[p.scenario.eq(r.scenario)&p.cycle.eq(r.forecast_cycle)&p.model.eq(chosen)].sort_values('target_id')
        selection.append(chosen==r.selected_model and ','.join(map(str,years))==r.validation_cycles and status==r.status and np.allclose(qa.prediction_pp,qb.prediction_pp))
    c.update(predictions_reconstructed=all(recon),feature_priors_polls_labels_preserved=all(frozen),valid_mixture_covariance=all(mass),training_past_only=all(chrono),seat_accounting=all(seatok),past_only_selection_reconstructed=all(selection))
    result=dict(passed=all(c.values()),checks=c,forecast_rows=len(p),fixed_fits=len(recon),integration_comparisons=len(i));v1.json_write(out/'audit.json',result)
    if not result['passed']:raise AssertionError([k for k,v in c.items() if not v])
    v1.manifest(out);return result


def report(out,lab):
    out,lab=Path(out),Path(lab);su=pd.read_parquet(out/'summary.parquet');ch=pd.read_parquet(out/'chamber_summary.parquet');seats=pd.read_parquet(out/'seats.parquet');folds=pd.read_parquet(out/'folds.parquet')
    text='# Feature priors with Student-t: results\n\nFrozen September 17 inputs. Gaussian feature fits and 30-day polling fixed; only systematic polling likelihood tails change. Lower MAE/WIS/Brier/CRPS is better.\n\n'
    for title,tab in [('Recent state metrics',su[su.period.eq('recent_2016_2024')&su.group.eq('all')][['scenario','model','n','correct','absolute_error_pp','wis_pp','brier','coverage70','coverage95']]),('Recent chamber metrics',ch[ch.period.eq('recent_2016_2024')]),('Current seats',seats[seats.cycle.eq(2026)][['model','point_D','expected_D_exact','D_lo70','D_hi70','D_lo95','D_hi95']]),('Current inferred polling scale',folds[folds.cycle.eq(2026)][['model','feature_tau','df','scale_mean','p_scale_gt1']])]:
        text+='## '+title+'\n\n'+tab.round(4).to_markdown(index=False)+'\n\n'
    (out/'NATIONAL_FEATURE_STUDENT_RESULTS.md').write_text(text);(lab/'NATIONAL_FEATURE_STUDENT_RESULTS.md').write_text(text)
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,axes=plt.subplots(1,2,figsize=(12,4.5),layout='constrained')
    for ax,sc in zip(axes,['matched_live','oct31']):
        q=ch[ch.period.eq('recent_2016_2024')&ch.scenario.eq(sc)].copy();q['family']=q.model.str.rsplit('_',n=1).str[0];q['distribution']=q.model.str.rsplit('_',n=1).str[1]
        q.pivot(index='family',columns='distribution',values='seat_crps').reindex(FAMILIES)[list(DISTS)].plot.bar(ax=ax,rot=0);ax.set_title('September' if sc=='matched_live' else 'October 31');ax.set_ylabel('Chamber CRPS (lower is better)');ax.set_xlabel('Feature family')
    for ax in axes:
        ax.legend(loc='upper center',ncol=3,title=None,fontsize=8);ax.set_ylim(0,1.05)
    fig.savefig(out/'chamber_comparison.png',dpi=150);plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(12,4.5),layout='constrained')
    for ax,sc in zip(axes,['matched_live','oct31']):
        q=su[su.period.eq('recent_2016_2024')&su.group.eq('all')&su.scenario.eq(sc)].copy();q['family']=q.model.str.rsplit('_',n=1).str[0];q['distribution']=q.model.str.rsplit('_',n=1).str[1]
        q.pivot(index='family',columns='distribution',values='coverage70').reindex(FAMILIES)[list(DISTS)].plot.bar(ax=ax,rot=0);ax.axhline(.7,color='black',ls='--');ax.set_ylim(.5,.9);ax.set_ylabel('Observed 70% interval coverage');ax.set_title('September' if sc=='matched_live' else 'October 31');ax.set_xlabel('Feature family')
    for ax in axes:
        ax.legend(loc='upper center',ncol=3,title=None,fontsize=8);ax.set_ylim(0,1.05)
    fig.savefig(out/'coverage_comparison.png',dpi=150);plt.close(fig)


def load(lab):
    lab=Path(lab);root=lab/'reports/national_feature_student';ptr=json.loads((root/'latest.json').read_text());out=root/ptr['artifact'];assert v1.verify(out)==ptr['manifest_sha256'];return out,{x.stem:pd.read_parquet(x) for x in out.glob('*.parquet')}

if __name__=='__main__':build(Path(__file__).resolve().parents[1])
