"""Bounded within-firm polling momentum with past-only bias/noise calibration."""
from pathlib import Path
from datetime import datetime,timezone
import json
import numpy as np
import pandas as pd
import poll_timing_student as timing
import simple_bayesian_polling as v1
import bayesian_revision2 as v2
import simple_national_model as normal
import national_feature_prior as features
import national_factor_review as national
import national_tails_waves as chamber
import coverage_balance as scoring
from final_baseline_experiments import cycle_metrics

FEATURE='20260920T013619.322700Z'
ORDER=['baseline','recent_level','momentum_half','momentum_full']
CONFIG=dict(window_days=30,min_date_gap_days=14,slope_cap_pp30=6.,matched_firm_shrinkage=3.,max_shift_pp=3.,max_projection_days=30.,seed=197139,draws=30000,as_of='2026-09-17')


def add_signatures(waves,metadata,identity,polls):
    d=metadata[['observation_id','population','estimate_basis','question_construct']].merge(identity[['observation_id','series_key']],on='observation_id',validate='one_to_one').set_index('observation_id')
    target=polls.set_index('observation_id').target_id;out=waves.copy();keys=[]
    for row in out.itertuples():
        ids=row.observation_ids.split('|')
        if not set(ids)<=set(d.index):raise ValueError('Missing sample metadata')
        if not target.reindex(ids).eq(row.target_id).all():raise ValueError('Observation/contest mismatch')
        q=d.loc[ids].fillna('unknown').astype(str)
        # Equal versions were already collapsed into one independent sample.
        # Match the complete set of chosen metadata signatures across periods.
        keys.append(json.dumps(sorted(set(tuple(x) for x in q.to_numpy())),separators=(',',':')))
    out['trend_signature']=keys
    return out


def aggregate(targets,waves):
    base=timing.aggregate(targets,waves,30);groups=dict(tuple(waves.groupby('target_id')));rows=[];pairrows=[]
    for t in targets.itertuples():
        w=groups.get(t.target_id,waves.iloc[:0]);recent=w[w.age_days.between(0,59)]
        slopes=[]
        for (firm,signature),g in recent.groupby(['firm','trend_signature']):
            new=g[g.age_days.lt(30)];old=g[g.age_days.ge(30)]
            if new.empty or old.empty:continue
            def average(q):
                a=np.exp2(-q.age_days.to_numpy()/30);return float(np.average(q.margin,weights=a)*100),float(np.average(q.age_days,weights=a))
            nm,na=average(new);om,oa=average(old);gap=oa-na
            if gap<CONFIG['min_date_gap_days']:continue
            raw=(nm-om)*30/gap;value=float(np.clip(raw,-CONFIG['slope_cap_pp30'],CONFIG['slope_cap_pp30']))
            slopes.append(dict(firm=firm,slope_pp30=value));pairrows.append(dict(target_id=t.target_id,firm=firm,signature=signature,new_margin_pp=nm,old_margin_pp=om,new_age_days=na,old_age_days=oa,date_gap_days=gap,raw_slope_pp30=raw,capped_slope_pp30=value,new_samples=len(new),old_samples=len(old)))
        byfirm=pd.DataFrame(slopes).groupby('firm').slope_pp30.median() if slopes else pd.Series(dtype=float);n=len(byfirm);raw=float(byfirm.median()) if n else 0.;gain=n/(n+CONFIG['matched_firm_shrinkage']);slope=raw*gain
        rows.append(dict(target_id=t.target_id,matched_firms=n,recent_firms=recent.firm.nunique(),firm_median_slope_pp30=raw,trend_shrinkage=gain,smoothed_slope_pp30=slope,trend_status='matched_recent_firms' if n else 'no_matched_trend_evidence',forecast_days_to_election=float(t.forecast_days_to_election)))
    a=base.merge(pd.DataFrame(rows),on='target_id',validate='one_to_one');a=a.rename(columns={'q_pp':'base_q_pp'});pairs=pd.DataFrame(pairrows)
    return a,pairs


def apply_variant(aggregates,name):
    if name not in ORDER:raise ValueError('Unknown trend variant')
    a=aggregates.copy();age=a.weighted_age_days.fillna(0).clip(0,30);future=a.forecast_days_to_election.clip(0,30)
    duration=age if name=='recent_level' else age+future
    strength=0. if name=='baseline' else .5 if name=='momentum_half' else 1.
    a['trend_shift_pp']=(strength*a.smoothed_slope_pp30*duration/30).clip(-3,3)
    a['q_pp']=(a.base_q_pp+a.trend_shift_pp).clip(-100,100);a['trend_shift_pp']=a.q_pp-a.base_q_pp
    a['variant']=name
    return a.drop(columns='forecast_days_to_election')


def build(lab):
    lab=Path(lab).resolve();src=lab/'reports/national_feature_prior'/FEATURE;fs=json.loads((src/'settings.json').read_text());work=Path(fs['source']);up=Path(fs['upstream']);prior=Path(json.loads((work/'settings.json').read_text())['prior_source'])
    h=pd.read_parquet(up/'history.parquet');waves=pd.read_parquet(up/'samples.parquet');roster=pd.read_parquet(up/'full_seat_ledger.parquet')
    snap=Path(json.loads((lab/'reports/baselines/20260918T055206.305739Z/data_inputs.json').read_text())['dataset']['snapshot']);paths={name:snap/'tables'/f'{name}.parquet' for name in ['polls','poll_metadata','poll_identity']}
    waves=add_signatures(waves,*[pd.read_parquet(paths[name]) for name in ['poll_metadata','poll_identity','polls']])
    out=lab/'reports/poll_trend_review'/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')
    for name in ['fits','forecasts','recipe']:(out/name).mkdir(parents=True,exist_ok=True)
    print('OUTPUT',out,flush=True)
    st=dict(config=CONFIG,source=str(src),working=str(work),upstream=str(up),prior=str(prior),sources={str(p):v1.verify(p) for p in [src,work,up,prior]},metadata_hashes={str(p):v1.sha(p) for p in paths.values()},old_notebooks={p.name:v1.sha(p) for p in lab.glob('*.ipynb') if p.name!='POLL_TREND_AND_SPARSE_REVIEW.ipynb'},working_sha256=v1.sha(lab/'WORKING_MODEL.json'),promotion=False,data_refreshed=False)
    v1.json_write(out/'settings.json',st);waves.to_parquet(out/'samples_with_signatures.parquet',index=False)
    aggregates=[];pairs=[];histories={};basechecks=[]
    for sc,hh in h.groupby('scenario'):
        a,pa=aggregate(hh,waves[waves.scenario.eq(sc)]);basechecks.append(np.allclose(a.base_q_pp,hh.q_pp,equal_nan=True)&np.allclose(a.firm_mass,hh.firm_mass));pairs.append(pa.assign(scenario=sc))
        for name in ORDER:
            aa=apply_variant(a,name);histories[(sc,name)]=timing.replace_aggregate(hh,aa);aggregates.append(aa.assign(scenario=sc))
    ag=pd.concat(aggregates,ignore_index=True);ag.to_parquet(out/'aggregates.parquet',index=False);pd.concat(pairs,ignore_index=True).to_parquet(out/'matched_pairs.parquet',index=False)
    print('Current matched trend support:',ag[ag.target_id.str.startswith('2026')&ag.variant.eq('baseline')][['target_id','matched_firms','smoothed_slope_pp30']].query('matched_firms>0').round(3).to_dict('records'),flush=True)
    old=pd.read_parquet(src/'predictions.parquet');folds0=pd.read_parquet(src/'folds.parquet');folds0=folds0[folds0.model.isin(['none','both'])];cache={x:{} for x in ORDER};predictions=[];seats=[];folds=[];fitdiag=[];trace=[];reproductions=[]
    for (sc,year),group in folds0.groupby(['scenario','cycle']):
        for name in ORDER:
            hist=histories[(sc,name)]
            if name=='baseline':
                pf=dict(np.load(work/f'fits/{sc}_{year}_poll.npz'));P=pf['budget'];x,noise,w,years,_=v2.blocks(hist,year,'poll');np.testing.assert_allclose(x,pf['training_values'],equal_nan=True);fit=None
            else:
                fit,tr=v2.choose_fit(hist,year,'poll',cache[name]);trace.extend(dict(**x,variant=name) for x in tr);x,noise,w,years,_=v2.blocks(hist,year,'poll');P=np.diag(fit['covariance'])+4.
            poll=normal.fixed_common(x,noise,w,P,0.,9.)
            path=f'fits/{sc}_{year}_{name}.npz';np.savez_compressed(out/path,**poll,training_values=x,training_noise=noise,training_weights=w,years=years)
            fitdiag.append(dict(scenario=sc,cycle=year,variant=name,training_max_cycle=int(years.max()),training_cycles=len(years),kappa=fit['kappa'] if fit else np.nan,converged=fit['converged'] if fit else True,poll_path=path))
            for sr in group.itertuples():
                family=sr.model;original=old[old.scenario.eq(sc)&old.cycle.eq(year)&old.model.eq(family)].sort_values('target_id').reset_index(drop=True);a=ag[ag.scenario.eq(sc)&ag.variant.eq(name)&ag.target_id.isin(original.target_id)].drop(columns='scenario');test=timing.replace_aggregate(original,a)
                ff=dict(np.load(src/sr.fit_path));ff['a']=float(ff['a']);p,C,stats,meta=features.predict(test,ff['budget'],poll,ff,ff['z']);model=family+'__'+name;p=p.assign(model=model,family=family,variant=name);predictions.append(p)
                rng=np.random.default_rng(CONFIG['seed']+year+10000*(sc=='oct31'));draws=p.prediction_pp.to_numpy()+rng.standard_normal((CONFIG['draws'],len(test)))@np.linalg.cholesky(C).T;ss,counts=chamber.seat_summary(roster[roster.scenario.eq(sc)&roster.cycle.eq(year)],test,p,draws);frequency=np.bincount(counts,minlength=101);seats.append(scoring.seat_scores(dict(ss,scenario=sc,cycle=year,model=model,family=family,variant=name),frequency))
                fp=f'forecasts/{sc}_{year}_{model}.npz';np.savez_compressed(out/fp,target_ids=test.target_id.to_numpy(str),mean=p.prediction_pp.to_numpy(),covariance=C,prior_covariance=meta['prior_covariance'],seat_count_frequency=frequency)
                folds.append(dict(scenario=sc,cycle=year,model=model,family=family,variant=name,poll_path=path,feature_fit_path=sr.fit_path,forecast_path=fp,**stats))
                if name=='baseline':
                    ref=np.load(src/sr.forecast_path);ok=np.allclose(p[['prediction_pp','p_dem','lo70_pp','hi95_pp']],original[['prediction_pp','p_dem','lo70_pp','hi95_pp']],atol=1e-8)&np.array_equal(frequency,ref['seat_count_frequency']);reproductions.append(bool(ok))
        print(sc,year,'all trend candidates complete',flush=True)
    p=pd.concat(predictions,ignore_index=True);s=pd.DataFrame(seats);f=pd.DataFrame(folds);tuning=[];pp=[];ss=[];ff=[]
    for (sc,year,family),g in p.groupby(['scenario','cycle','family']):
        order=[family+'__'+x for x in ORDER];chosen,yrs,status=timing.choose(s[s.scenario.eq(sc)],year,order)
        pp.append(g[g.model.eq(chosen)].assign(model=family+'__selected',selected_model=chosen));ss.append(s[s.scenario.eq(sc)&s.cycle.eq(year)&s.model.eq(chosen)].assign(model=family+'__selected',selected_model=chosen));ff.append(f[f.scenario.eq(sc)&f.cycle.eq(year)&f.model.eq(chosen)].assign(model=family+'__selected',selected_model=chosen))
        for model in order:tuning.append(dict(scenario=sc,forecast_cycle=year,family=family,candidate=model,selected_model=chosen,validation_cycles=','.join(map(str,yrs)),status=status,validation_crps=s[s.scenario.eq(sc)&s.cycle.isin(yrs)&s.model.eq(model)].seat_crps.mean()))
    p=pd.concat([p,*pp],ignore_index=True);s=pd.concat([s,*ss],ignore_index=True);f=pd.concat([f,*ff],ignore_index=True)
    p['coverage_group']=np.where(p.sample_count.eq(0),'no_polls',np.where(p.recent_firms.le(2),'low_recent_0_2_firms','recent_3plus_firms'))
    subgroup=[]
    for first in [2012,2016]:
        for (sc,model,group),q in p[p.cycle.between(first,2024)].groupby(['scenario','model','coverage_group']):
            metrics=q.groupby('cycle')[['absolute_error_pp','wis_pp','brier']].mean().mean().to_dict();subgroup.append(dict(first_cycle=first,scenario=sc,model=model,coverage_group=group,n=len(q),cycles=q.cycle.nunique(),correct=int(q.correct.sum()),coverage70=q.coverage70.mean(),coverage95=q.coverage95.mean(),mean_posterior_sd_pp=q.posterior_sd_pp.mean(),**metrics))
    for name,table in dict(predictions=p,seats=s,folds=f,calibration_fits=pd.DataFrame(fitdiag),calibration_selection=pd.DataFrame(trace),tuning=pd.DataFrame(tuning),summary=scoring.summarize_scores(p),chamber_summary=national.chamber_summary(s),cycle_scores=cycle_metrics(p),coverage_groups=pd.DataFrame(subgroup)).items():table.to_parquet(out/f'{name}.parquet',index=False)
    v1.json_write(out/'reproduction.json',dict(passed=bool(all(basechecks)&all(reproductions)),aggregate_checks=len(basechecks),forecasts=len(reproductions)))
    for name,c in cache.items():
        for (sc,year,kind,kappa),fit in c.items():
            np.savez_compressed(out/f'fits/calibration_{sc}_{year}_{name}_{kappa}.npz',**{k:v for k,v in fit.items() if isinstance(v,np.ndarray)})
    for path in (lab/'scripts').glob('*.py'):(out/'recipe'/path.name).write_bytes(path.read_bytes())
    (out/'POLL_TREND_AND_SPARSE_REVIEW.md').write_bytes((lab/'POLL_TREND_AND_SPARSE_REVIEW.md').read_bytes());v1.manifest(out);audit(out,lab);v1.manifest(out);v1.json_write(out.parent/'latest.json',dict(artifact=out.name,manifest_sha256=v1.verify(out)));print('COMPLETE',out,flush=True);return out


def audit(out,lab):
    out,lab=Path(out),Path(lab);v1.verify(out);st=json.loads((out/'settings.json').read_text());p=pd.read_parquet(out/'predictions.parquet');s=pd.read_parquet(out/'seats.parquet');f=pd.read_parquet(out/'folds.parquet');a=pd.read_parquet(out/'aggregates.parquet');tr=pd.read_parquet(out/'calibration_selection.parquet');fd=pd.read_parquet(out/'calibration_fits.parquet');t=pd.read_parquet(out/'tuning.parquet');old=pd.read_parquet(Path(st['source'])/'predictions.parquet')
    checks=dict(source_hashes=all(v1.verify(path)==h for path,h in st['sources'].items()),metadata_hashes=all(v1.sha(path)==h for path,h in st['metadata_hashes'].items()),old_notebooks=all(v1.sha(lab/n)==h for n,h in st['old_notebooks'].items()),working_designation=v1.sha(lab/'WORKING_MODEL.json')==st['working_sha256'],baseline_reproduction=json.loads((out/'reproduction.json').read_text())['passed'],past_calibration=bool(fd.training_max_cycle.lt(fd.cycle).all()&tr.fit_max_cycle.lt(tr.validation_cycle).all()&tr.validation_cycle.lt(tr.forecast_cycle).all()),converged=bool(fd.converged.all()),shift_bounded=bool(a.trend_shift_pp.dropna().abs().le(3.0000001).all()),sparse_fallback=bool(a[a.matched_firms.eq(0)].trend_shift_pp.fillna(0).eq(0).all()),no_polls_missing=bool(a[a.sample_count.eq(0)].q_pp.isna().all()),current_labels_missing=bool(p[p.cycle.eq(2026)][['actual','brier','wis_pp']].isna().all().all()),unique_forecasts=not p.duplicated(['scenario','model','target_id']).any(),probabilities=bool(p.p_dem.between(0,1).all()))
    raw=pd.read_parquet(Path(st['upstream'])/'samples.parquet');waves=pd.read_parquet(out/'samples_with_signatures.parquet');history=pd.read_parquet(Path(st['upstream'])/'history.parquet')
    checks['raw_samples_preserved']=bool(raw.equals(waves[raw.columns]))
    aggchecks=[]
    for sc,hh in history.groupby('scenario'):
        aa,_=aggregate(hh,waves[waves.scenario.eq(sc)])
        for name in ORDER:
            expected=apply_variant(aa,name).set_index('target_id').sort_index();observed=a[a.scenario.eq(sc)&a.variant.eq(name)].set_index('target_id').sort_index();cols=['q_pp','firm_mass','matched_firms','smoothed_slope_pp30','trend_shift_pp']
            aggchecks.append(np.allclose(expected[cols],observed[cols],equal_nan=True))
    checks['aggregate_reconstruction']=bool(all(aggchecks))
    recon=[];inputs=[];seats_ok=[];selection=[]
    for r in f.itertuples():
        q=p[p.scenario.eq(r.scenario)&p.cycle.eq(r.cycle)&p.model.eq(r.model)].sort_values('target_id').reset_index(drop=True);o=old[old.scenario.eq(r.scenario)&old.cycle.eq(r.cycle)&old.model.eq(r.family)].sort_values('target_id');fit=dict(np.load(Path(st['source'])/r.feature_fit_path));fit['a']=float(fit['a']);poll=dict(np.load(out/r.poll_path));expected,C,_,meta=features.predict(q,fit['budget'],poll,fit,fit['z']);saved=np.load(out/r.forecast_path);cols=['prediction_pp','p_dem','lo70_pp','hi95_pp'];recon.append(np.allclose(q[cols],expected[cols])&np.allclose(C,saved['covariance'])&np.allclose(meta['prior_covariance'],saved['prior_covariance']))
        inputs.append(np.array_equal(q.target_id,o.target_id)&np.array_equal(q.actual,o.actual,equal_nan=True)&np.array_equal(q.prior,o.prior)&np.allclose(q.firm_mass,o.firm_mass));seat=s[s.scenario.eq(r.scenario)&s.cycle.eq(r.cycle)&s.model.eq(r.model)].iloc[0];seats_ok.append(abs(seat.expected_D_exact-seat.fixed_D-q.p_dem.sum())<1e-8 and saved['seat_count_frequency'].sum()==CONFIG['draws'])
    for row in t.drop_duplicates(['scenario','forecast_cycle','family']).itertuples():
        chosen,years,status=timing.choose(s[s.scenario.eq(row.scenario)],row.forecast_cycle,[row.family+'__'+n for n in ORDER]);selection.append(chosen==row.selected_model and status==row.status and ','.join(map(str,years))==row.validation_cycles)
    checks.update(forecast_reconstruction=bool(all(recon)),unchanged_priors_information_labels=bool(all(inputs)),seat_accounting=bool(all(seats_ok)),past_selector_reconstruction=bool(all(selection)))
    result=dict(passed=bool(all(checks.values())),checks=checks,forecasts=len(f),calibration_fits=len(fd),rows=len(p),old_notebooks=len(st['old_notebooks']));v1.json_write(out/'audit.json',result)
    if not result['passed']:raise AssertionError(checks)
    return result

if __name__=='__main__':build(Path(__file__).resolve().parents[1])
