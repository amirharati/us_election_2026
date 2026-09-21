"""Rebuild pinned eligible polls, run and audit within-cycle decay comparisons."""
from pathlib import Path
from datetime import datetime,timezone
from collections import Counter
import json,hashlib,shutil
import numpy as np
import pandas as pd
from load_final_dataset import open_run_dataset
from simple_baselines import prepare_inputs
from poll_error_baselines import build_poll_history
from poll_age_decay import evaluate,HALVES,MODES,PREFERENCE
from audit_state_poll_bias import reconstruct
from winner_classification import classification_report
from senate_summary import senate_report


def replay_waves(parent,raw,cal):
    data=open_run_dataset(parent/'poll_error_models/data_inputs.json')
    original=data.load_table('contest_inputs_reference');waves={};parity={}
    for scenario in sorted(raw.scenario.unique()):
        c=cal[cal.scenario.eq(scenario)];replace=[k for k in c if k in original and k!='cycle']
        inputs=original.drop(columns=replace).merge(c,on='cycle',validate='many_to_one')
        election=pd.to_datetime(inputs.election_date);cutoff=pd.to_datetime(inputs.context_id)
        inputs['historical_horizon_comparable']=inputs.historical_horizon_comparable&election.gt(cutoff)
        inputs['forecast_days_to_election']=(election-cutoff).dt.days
        ts,ws,_,_=prepare_inputs(data,inputs)
        h,_=build_poll_history(ts,ws,scenario)
        q=raw[raw.scenario.eq(scenario)].merge(h[['target_id','poll_baseline','n_samples']],on='target_id',validate='one_to_one',suffixes=('_old','_new'))
        assert len(q)==len(h) and np.array_equal(q.n_samples_old,q.n_samples_new)
        assert np.allclose(q.poll_baseline_old,q.poll_baseline_new,atol=1e-12)
        ids=set(raw.loc[raw.scenario.eq(scenario),'target_id']);waves[scenario]=ws[ws.target_id.isin(ids)].copy()
        assert waves[scenario].age_days.ge(0).all()
        parity[scenario]=len(q)
    return waves,parity


def run_experiment(lab,parent):
    lab,parent=Path(lab).resolve(),Path(parent).resolve()
    bias=max((parent/'state_poll_bias').glob('*/manifest.json')).parent
    sources=dict(history=parent/'poll_error_models/poll_history.parquet',calendars=parent/'contextual/calendars.parquet',
        membership=parent/'cv/competitive/membership.parquet',old_bias=bias/'state_calls.parquet',data_inputs=parent/'poll_error_models/data_inputs.json')
    hashes={k:hashlib.sha256(p.read_bytes()).hexdigest() for k,p in sources.items()}
    raw=pd.read_parquet(sources['history']);before=raw.copy(deep=True);cal=pd.read_parquet(sources['calendars'])
    waves,parity=replay_waves(parent,raw,cal)
    out=parent/'poll_age_decay'/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ');out.mkdir(parents=True,exist_ok=False)
    print('Poll age experiment:',out,flush=True)
    def progress(message):print(message,flush=True)
    frames,fits=evaluate(raw,waves,progress=progress)
    pred=frames['predictions'];hist=frames['history'];reference_parts=[]
    key=pred[['scenario','target_id','status']].drop_duplicates()
    refs=raw.merge(key,on=['scenario','target_id'],validate='one_to_one')
    for name,col in [('prior','prior'),('baseline_polling','poll_baseline')]:reference_parts.append(refs.assign(model=name,prediction=refs[col]))
    old=pd.read_parquet(sources['old_bias']);old=old[old.model.eq('bias_state__last5_half8')]
    ref=refs.merge(old[['scenario','target_id','prediction']],on=['scenario','target_id'],how='left',validate='one_to_one')
    assert ref.prediction.notna().all();reference_parts.append(ref.assign(model='baseline_bias'))
    pred=pd.concat([pred,*reference_parts],ignore_index=True);frames['predictions']=pred
    calls,_,_,_=classification_report(pred);calls,cycles,summary=senate_report(calls,pd.read_parquet(sources['membership']))
    # Scalar audit of every recalculated poll forecast (all historical cycles).
    poll_audits=[]
    for scenario,source in raw.groupby('scenario'):
        groups={key:g for key,g in waves[scenario].groupby('target_id')}
        indexed=source.set_index('target_id')
        for (mode,profile),q in hist[hist.scenario.eq(scenario)].groupby(['mode','profile']):
            half=HALVES[profile];errors=[]
            for row in q.itertuples():
                oldrow=indexed.loc[row.target_id];g=groups.get(row.target_id)
                if g is None:
                    expected=float(oldrow.prior)
                else:
                    counts=Counter(g.firm);pairs=[((1. if half is None else 2.**(-float(p.age_days)/half))/counts[p.firm],float(p.margin)) for p in g.itertuples()]
                    mass=sum(w for w,_ in pairs);mean=sum(w*v for w,v in pairs)/mass
                    fraction=float(oldrow.prior_fraction) if mode=='fixed_blend' else oldrow.poll_prior_strength/(mass+oldrow.poll_prior_strength)
                    expected=(1-fraction)*mean+fraction*oldrow.prior
                    assert np.isclose(row.prior_fraction,fraction) and np.isclose(row.poll_mean,mean)
                    if mode=='fixed_blend':assert row.prior_fraction==oldrow.prior_fraction
                    if half==oldrow.poll_half_life:assert np.isclose(row.poll_baseline,oldrow.poll_baseline,atol=1e-11)
                errors.append(abs(expected-row.poll_baseline))
            assert max(errors)<1e-11
            poll_audits.append(dict(scenario=scenario,mode=mode,profile=profile,targets=len(q),max_difference=max(errors)))
    # Independently reconstruct final bias fits and all k-validation scores in scored/current folds.
    bias_audits=[]
    for f in fits:
        if f['cycle']<2012 or (f['scenario']=='oct31' and f['cycle']==2026):continue
        h=hist[hist.scenario.eq(f['scenario'])&hist['mode'].eq(f['mode'])&hist.profile.eq(f['profile'])]
        train=h[h.cycle.lt(f['cycle'])&h.actual.notna()];test=h[h.cycle.eq(f['cycle'])]
        expected,_,_=reconstruct(train,test,5,8.,'state',f['shrinkage'])
        assert np.allclose(expected,test.bias_prediction,atol=1e-11)
        inner=train[train.cycle.lt(f['cycle']-2)];valid=train[train.cycle.eq(f['cycle']-2)&train.n_samples.gt(0)]
        grid=frames['bias_tuning'];g=grid[grid.scenario.eq(f['scenario'])&grid['mode'].eq(f['mode'])&grid.profile.eq(f['profile'])&grid.cycle.eq(f['cycle'])]
        for row in g.itertuples():
            vp,_,_=reconstruct(inner,valid,5,8.,'state',row.shrinkage)
            assert np.isclose(100*np.abs(vp-valid.actual.to_numpy()).mean(),row.validation_mae_pp)
        chosen=min(g.to_dict('records'),key=lambda r:(round(r['validation_mae_pp']/100,12),-r['shrinkage']))
        assert chosen['shrinkage']==f['shrinkage']
        bias_audits.append(dict(scenario=f['scenario'],cycle=f['cycle'],mode=f['mode'],profile=f['profile'],max_difference=float(np.max(abs(expected-test.bias_prediction))),inner_candidates=len(g)))
    for row in frames['selections'].itertuples():
        g=frames['selection_tuning'];g=g[g.scenario.eq(row.scenario)&g['mode'].eq(row.mode)&g.architecture.eq(row.architecture)&g.cycle.eq(row.cycle)]
        for candidate in g.itertuples():
            h=hist[hist.scenario.eq(row.scenario)&hist['mode'].eq(row.mode)&hist.profile.eq(candidate.profile)&hist.cycle.eq(row.validation_cycle)&hist.n_samples.gt(0)]
            col='poll_baseline' if row.architecture=='polling' else 'bias_prediction'
            assert np.isclose(100*(h[col]-h.actual).abs().mean(),candidate.validation_mae_pp)
        best=min(g.to_dict('records'),key=lambda v:(round(v['validation_mae_pp']/100,12),PREFERENCE[v['profile']]))
        assert best['profile']==row.selected_profile
        q=pred[pred.scenario.eq(row.scenario)&pred.cycle.eq(row.cycle)]
        a=q[q.model.eq(row.model)].set_index('target_id').prediction
        b=q[q.model.eq(row.mode+'__'+row.selected_profile+'__'+row.architecture)].set_index('target_id').prediction
        np.testing.assert_array_equal(a,b)
    no=pred[pred.n_samples.eq(0)];np.testing.assert_array_equal(no.prediction,no.prior)
    assert not pred[pred.actual.isna()].scenario.eq('oct31').any()
    pd.testing.assert_frame_equal(raw,before)
    groups=[]
    for (scenario,model),g in calls[calls.classification_status.eq('cv_scored')&calls.cycle.ge(2016)].groupby(['scenario','model']):
        for label,q in [('all',g),('competitive',g[g.history_selection_10pp.eq('competitive')]),('not_selected',g[g.history_selection_10pp.eq('not_selected')]),
                        ('unknown_history',g[g.history_selection_10pp.eq('unknown_history')]),('polled',g[g.n_samples.gt(0)]),('no_polls',g[g.n_samples.eq(0)])]:
            if len(q):groups.append(dict(scenario=scenario,model=model,group=label,n=len(q),correct=int(q.correct.sum()),mae_pp=100*(q.prediction-q.actual).abs().groupby(q.cycle).mean().mean()))
    groups=pd.DataFrame(groups)
    for row in summary.itertuples():
        q=calls[calls.classification_status.eq('cv_scored')&calls.scenario.eq(row.scenario)&calls.model.eq(row.model)]
        if row.period=='2016_onward':q=q[q.cycle.ge(2016)]
        if row.scope=='with_polls':q=q[q.n_samples.gt(0)]
        if row.subset!='all_admitted':q=q[q['history_selection_'+('5pp' if row.subset.endswith('_5pp') else '10pp')].eq('competitive')]
        assert len(q)==row.contests and int(q.correct.sum())==row.correct
        assert np.isclose(100*(q.prediction-q.actual).abs().groupby(q.cycle).mean().mean(),row.mean_state_mae_pp)
    for _,g in groups.groupby(['scenario','model']):
        q=g.set_index('group');assert q.loc[['competitive','not_selected','unknown_history'],'correct'].sum()==q.loc['all','correct']
    current=pred[pred.actual.isna()].pivot(index=['scenario','target_id','geography','n_samples'],columns='model',values='prediction')*100
    frames.update(state_calls=calls,cycle_metrics=cycles,summary=summary,groups=groups,current_states=current.reset_index(),
                  independent_poll_audit=pd.DataFrame(poll_audits),independent_bias_audit=pd.DataFrame(bias_audits))
    for scenario,w in waves.items():w.assign(scenario=scenario).to_parquet(out/('eligible_samples_'+scenario+'.parquet'),index=False)
    for name,frame in frames.items():frame.to_parquet(out/(name+'.parquet'),index=False)
    (out/'bias_fits.json').write_text(json.dumps(fits,indent=2,allow_nan=False)+'\n')
    settings=dict(version='within-cycle-poll-age-v1',half_life_days=HALVES,blend_modes=MODES,
        half_life_selection='previous-cycle polled MAE; prefer longer/no decay on ties',
        prior_strength='unchanged original chronological 30/90-day,0/2-prior grid choice; no expanded joint tuning',
        bias_rule='relearn each rule prequentially: last5 cycles,8-year decay,k onY-2',
        prior_fraction_fixed_in_control=True,poll_age='forecast cutoff minus sample field end',
        eligibility='unchanged current two-year cycle pool; prior-year polls retained and aged',
        reconstructed_legacy_parity=parity,independent_bias_fits=len(bias_audits),automatic_model_promotion=False,
        source_files={k:{'path':str(p),'sha256':hashes[k]} for k,p in sources.items()})
    for k,p in sources.items():assert hashlib.sha256(p.read_bytes()).hexdigest()==hashes[k]
    (out/'settings.json').write_text(json.dumps(settings,indent=2)+'\n');shutil.copy2(sources['data_inputs'],out/'source_data_inputs.json')
    for name in ['poll_age_decay.py','run_poll_age_decay.py','simple_baselines.py','poll_error_baselines.py','state_poll_bias.py',
                 'audit_state_poll_bias.py','cycle_cv.py','winner_classification.py','senate_summary.py']:
        shutil.copy2(lab/'scripts'/name,out/name)
    (out/'manifest.json').write_text(json.dumps({p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(out.iterdir()) if p.is_file() and p.name!='manifest.json'},indent=2)+'\n')
    print('Verified',len(poll_audits),'poll-weight panels;',len(bias_audits),'final bias fits; legacy parity:',parity,flush=True)
    return out,frames,fits

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--parent',type=Path,required=True);args=p.parse_args()
    run_experiment(Path(__file__).resolve().parents[1],args.parent)
