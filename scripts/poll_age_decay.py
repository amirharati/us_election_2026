"""Controlled within-cycle poll-age decay, with freshly learned bias per rule.

Fixed_blend changes only the poll mean. Native_mass retains the existing coupling
between decayed poll evidence and the historical prior. Both freeze the existing
chronological prior-strength choices; no joint prior-strength grid expansion.
"""
import numpy as np
import pandas as pd
from state_poll_bias import fit_bias,SHRINKAGES
from poll_error_baselines import correction_folds

HALVES={'flat':None,'d90':90.,'d60':60.,'d30':30.,'d14':14.,'d07':7.}
MODES=['fixed_blend','native_mass']
# Prefer less aggressive decay when previous-cycle errors tie.
PREFERENCE={name:i for i,name in enumerate(HALVES)}


def aggregate_polls(targets,waves,half_life,mode):
    if mode not in MODES:raise ValueError('Unknown blend mode')
    if half_life is not None and (not np.isfinite(half_life) or half_life<=0):raise ValueError('Positive half-life required')
    if targets.target_id.duplicated().any() or waves.duplicated(['target_id','sample_key']).any():raise ValueError('Duplicate target/sample')
    if waves.age_days.lt(0).any() or not np.isfinite(waves[['age_days','margin']]).all().all():raise ValueError('Invalid eligible poll')
    groups={k:g for k,g in waves.groupby('target_id')};rows=[]
    for row in targets.itertuples():
        w=groups.get(row.target_id)
        if w is None or w.empty:
            rows.append(dict(target_id=row.target_id,poll_baseline=row.prior,n_samples=0,n_firms=0,
                poll_mean=np.nan,prior_fraction=1.,decayed_firm_mass=0.,weighted_age_days=np.nan,
                share_weight_last14=np.nan,share_weight_last30=np.nan,weight_equivalent_samples=0.,weight_equivalent_firms=0.))
            continue
        age=w.age_days.to_numpy(float)
        time_weight=np.ones(len(w)) if half_life is None else np.exp2(-age/half_life)
        weights=time_weight/w.groupby('firm').firm.transform('size').to_numpy()
        mass=float(weights.sum());mean=float(np.dot(weights,w.margin)/mass)
        if mode=='fixed_blend':prior_fraction=float(row.prior_fraction)
        else:prior_fraction=float(row.poll_prior_strength/(mass+row.poll_prior_strength))
        pred=(1-prior_fraction)*mean+prior_fraction*row.prior
        firm_weights=pd.Series(weights,index=w.firm).groupby(level=0).sum().to_numpy()
        rows.append(dict(target_id=row.target_id,poll_baseline=pred,n_samples=len(w),n_firms=w.firm.nunique(),poll_mean=mean,
            prior_fraction=prior_fraction,decayed_firm_mass=mass,weighted_age_days=float(np.dot(weights,age)/mass),
            share_weight_last14=float(weights[age<=14].sum()/mass),share_weight_last30=float(weights[age<=30].sum()/mass),
            weight_equivalent_samples=float(mass*mass/(weights@weights)),weight_equivalent_firms=float(mass*mass/(firm_weights@firm_weights))))
    return pd.DataFrame(rows)


def rebuild_bias(history):
    """Same last5/8-year bias rule, relearned using this poll rule's own residuals."""
    parts=[];fits=[];grids=[]
    for year in sorted(history.cycle.unique()):
        year=int(year);test=history[history.cycle.eq(year)]
        past=history[history.cycle.lt(year)&history.actual.notna()]
        inner=past[past.cycle.lt(year-2)];valid=past[past.cycle.eq(year-2)&past.n_samples.gt(0)]
        candidates=[]
        if len(valid) and inner.n_samples.gt(0).any():
            for k in SHRINKAGES:
                vp,_,_=fit_bias(inner,valid,5,8.,'state',k)
                loss=float(np.abs(vp-valid.actual.to_numpy()).mean());candidates.append((loss,k))
                grids.append(dict(cycle=year,validation_cycle=year-2,training_max_cycle=int(inner.loc[inner.n_samples.gt(0),'cycle'].max()),
                    shrinkage=k,validation_mae_pp=100*loss))
        if candidates:loss,k=min(candidates,key=lambda t:(round(t[0],12),-t[1]));status='previous_cycle_tuned'
        else:loss=None;k=3.;status='early_default_k3'
        pp,f,_=fit_bias(past,test,5,8.,'state',k)
        f.update(cycle=year,validation_cycle=year-2,tuning_status=status,validation_mae_pp=None if loss is None else 100*loss)
        fits.append(f)
        parts.append(test.assign(bias_prediction=pp,bias_shrinkage=k,bias_training_max_cycle=f['training_max_cycle'],
            bias_tuning_status=status,bias_adjustment_pp=100*(pp-test.poll_baseline.to_numpy())))
    return pd.concat(parts,ignore_index=True),pd.DataFrame(grids),fits


def evaluate(raw_history,waves_by_scenario,start_cycle=2012,progress=None):
    histories=[];bias_fits=[];bias_grids=[];folds_all=[];predictions=[];selections=[];selection_grid=[]
    for scenario,raw in raw_history.groupby('scenario'):
        raw=raw[raw.kind.eq('senate')].copy()
        folds=correction_folds(raw,raw,scenario,start_cycle,6);folds_all.append(folds)
        eligible=set(folds.loc[folds.status.isin(['cv_scored','forecast_only_no_outcomes']),'cycle'])
        status_map=folds.set_index('cycle').status
        waves=waves_by_scenario[scenario];variants={}
        for mode in MODES:
            for profile,half in HALVES.items():
                pred=aggregate_polls(raw,waves,half,mode)
                cols=['target_id','cycle','kind','geography','actual','prior','prior_basis','context_id','window_complete','poll_prior_strength']
                source=raw[cols].merge(pred,on='target_id',validate='one_to_one')
                source['scenario']=scenario;source['mode']=mode;source['profile']=profile
                h,grid,fits=rebuild_bias(source);variants[(mode,profile)]=h
                histories.append(h)
                if len(grid):bias_grids.append(grid.assign(scenario=scenario,mode=mode,profile=profile))
                bias_fits += [dict(f,scenario=scenario,mode=mode,profile=profile) for f in fits]
                q=h[h.cycle.isin(eligible)].copy();q['status']=q.cycle.map(status_map)
                for architecture,col in [('polling','poll_baseline'),('bias','bias_prediction')]:
                    predictions.append(q.assign(model=mode+'__'+profile+'__'+architecture,architecture=architecture,prediction=q[col].to_numpy()))
                if progress:progress(f'{scenario} {mode}/{profile}: poll means and prequential bias rebuilt')
        for mode in MODES:
            for year in sorted(eligible):
                for architecture,col in [('polling','poll_baseline'),('bias','bias_prediction')]:
                    candidates=[]
                    for profile in HALVES:
                        h=variants[(mode,profile)]
                        valid=h[h.cycle.eq(year-2)&h.actual.notna()&h.n_samples.gt(0)]
                        if valid.empty:raise ValueError('No previous-cycle validation')
                        loss=float((valid[col]-valid.actual).abs().mean());candidates.append((loss,profile))
                        selection_grid.append(dict(scenario=scenario,cycle=int(year),mode=mode,architecture=architecture,
                            profile=profile,validation_cycle=int(year-2),validation_rows=len(valid),validation_mae_pp=100*loss))
                    loss,profile=min(candidates,key=lambda v:(round(v[0],12),PREFERENCE[v[1]]))
                    h=variants[(mode,profile)];q=h[h.cycle.eq(year)].copy();q['status']=status_map.loc[year]
                    model=mode+'__selected__'+architecture
                    predictions.append(q.assign(model=model,architecture=architecture,prediction=q[col].to_numpy()))
                    selections.append(dict(scenario=scenario,cycle=int(year),mode=mode,architecture=architecture,model=model,
                        selected_profile=profile,selected_half_life_days=HALVES[profile],validation_cycle=int(year-2),validation_mae_pp=100*loss))
    return dict(predictions=pd.concat(predictions,ignore_index=True),history=pd.concat(histories,ignore_index=True),
        folds=pd.concat(folds_all,ignore_index=True),bias_tuning=pd.concat(bias_grids,ignore_index=True),
        selection_tuning=pd.DataFrame(selection_grid),selections=pd.DataFrame(selections)),bias_fits
