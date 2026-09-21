"""Execute and independently audit the small score comparison for the notebook."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,shutil
import numpy as np
import pandas as pd
from momentum_approval_models import evaluate,FEATURES,HALF_LIFE,PREFERENCE
from score_baselines import ALPHAS
from audit_recency_states import reconstruct
from winner_classification import classification_report
from senate_summary import senate_report


def independent(train,test,cal,base,feature_set,alpha):
    mode='prior' if base=='prior' else 'polling'
    if base=='bias':train=train.assign(poll_baseline=train.bias_prediction);test=test.assign(poll_baseline=test.bias_prediction)
    if feature_set!='constant':
        prediction,beta,_,df=reconstruct(train,test,cal,mode,HALF_LIFE,alpha,None,FEATURES[feature_set],'shared')
        return prediction,beta,df
    col='prior' if base=='prior' else 'poll_baseline'
    errors=(train.actual-train[col]).groupby(train.cycle).mean().sort_index()
    weights=2.**(-(int(test.cycle.iloc[0])-errors.index.to_numpy())/HALF_LIFE)
    intercept=float(np.average(errors,weights=weights))
    return np.clip(test[col].to_numpy()+intercept,-1,1),{'intercept':intercept},1.


def run_experiment(lab,parent):
    lab,parent=Path(lab).resolve(),Path(parent).resolve()
    stack=max((parent/'bias_momentum_stack').glob('*/manifest.json')).parent
    sources=dict(history=stack/'prequential_bias_history.parquet',references=stack/'predictions.parquet',
        calendars=parent/'contextual/calendars.parquet',membership=parent/'cv/competitive/membership.parquet',
        data_inputs=parent/'poll_error_models/data_inputs.json')
    hashes={k:hashlib.sha256(p.read_bytes()).hexdigest() for k,p in sources.items()}
    h=pd.read_parquet(sources['history']);h=h[h.base.eq('fixed5_8')].copy()
    before=h.copy(deep=True);cal=pd.read_parquet(sources['calendars'])
    out=parent/'momentum_approval'/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ');out.mkdir(parents=True,exist_ok=False)
    print('Small-score experiment:',out,flush=True)
    predictions,folds,tuning,fits=evaluate(h,cal)
    calls,_,_,_=classification_report(predictions)
    calls,cycles,summary=senate_report(calls,pd.read_parquet(sources['membership']))
    # Independent full normalization and weighted ridge reconstruction, plus all tuning losses.
    audits=[]
    for f in fits:
        if f['model'].endswith('__selected'):continue
        source=h[h.scenario.eq(f['scenario'])];cal_s=cal[cal.scenario.eq(f['scenario'])]
        train=source[source.cycle.lt(f['cycle'])&source.actual.notna()];test=source[source.cycle.eq(f['cycle'])]
        if f['base']!='prior':train=train[train.n_samples.gt(0)];test=test[test.n_samples.gt(0)]
        if test.empty:test=source[source.cycle.eq(f['cycle'])].iloc[:1]
        expected,beta,df=independent(train,test,cal_s,f['base'],f['feature_set'],f['alpha'] or 1.)
        saved=predictions[predictions.scenario.eq(f['scenario'])&predictions.cycle.eq(f['cycle'])&predictions.model.eq(f['model'])]
        matched=test[['target_id']].merge(saved[['target_id','prediction']],on='target_id',validate='one_to_one')
        assert np.allclose(matched.prediction,expected,atol=1e-10)
        assert list(beta)==list(f['standardized_coefficients'])
        assert np.allclose(list(beta.values()),list(f['standardized_coefficients'].values()),atol=1e-10)
        assert np.isclose(df,f['effective_df'])
        inner=train[train.cycle.lt(f['cycle']-2)];valid=train[train.cycle.eq(f['cycle']-2)]
        grid=tuning[tuning.scenario.eq(f['scenario'])&tuning.cycle.eq(f['cycle'])&tuning.base.eq(f['base'])&tuning.feature_set.eq(f['feature_set'])]
        for row in grid.itertuples():
            vp,_,_=independent(inner,valid,cal_s,f['base'],f['feature_set'],row.alpha if pd.notna(row.alpha) else 1.)
            assert np.isclose(100*np.abs(vp-valid.actual.to_numpy()).mean(),row.validation_mae_pp,atol=1e-9)
        choice=min(grid.to_dict('records'),key=lambda r:(round(r['validation_mae_pp']/100,12),-(r['alpha'] if pd.notna(r['alpha']) else 0)))
        assert np.isclose(f['validation_mae_pp'],choice['validation_mae_pp'])
        if f['alpha'] is not None:assert f['alpha']==choice['alpha']
        audits.append(dict(scenario=f['scenario'],cycle=f['cycle'],model=f['model'],
            max_prediction_difference=float(np.max(np.abs(expected-matched.prediction))),inner_candidates=len(grid)))
    for f in fits:
        if not f['model'].endswith('__selected'):continue
        g=tuning[tuning.scenario.eq(f['scenario'])&tuning.cycle.eq(f['cycle'])&tuning.base.eq(f['base'])]
        chosen=min(g.to_dict('records'),key=lambda r:(round(r['validation_mae_pp']/100,12),PREFERENCE[r['feature_set']],-(r['alpha'] if pd.notna(r['alpha']) else 0)))
        assert chosen['feature_set']==f['selected_features']
        source_name=f['base'] if f['selected_features']=='none' else f['base']+'__'+f['selected_features']
        subset=predictions[predictions.scenario.eq(f['scenario'])&predictions.cycle.eq(f['cycle'])]
        a=subset[subset.model.eq(f['model'])].set_index('target_id').prediction
        b=subset[subset.model.eq(source_name)].set_index('target_id').prediction
        np.testing.assert_array_equal(a,b)
    refs=pd.read_parquet(sources['references']);parity={}
    mapping={'prior':'prior','polling':'polling','bias':'base_fixed5_8','polling__momentum':'momentum_shared__half8',
        'bias__momentum':'stack_fixed5_8__half8','bias__constant':'stack_fixed5_8__constant8'}
    for name,old_name in mapping.items():
        a=predictions[predictions.model.eq(name)][['scenario','target_id','prediction']]
        b=refs[refs.model.eq(old_name)][['scenario','target_id','prediction']]
        q=a.merge(b,on=['scenario','target_id'],validate='one_to_one',suffixes=('_a','_b'))
        assert len(q)==len(a) and np.allclose(q.prediction_a,q.prediction_b,atol=1e-11)
        parity[name]=len(q)
    no=predictions[predictions.base.ne('prior')&predictions.n_samples.eq(0)]
    np.testing.assert_array_equal(no.prediction,no.poll_baseline)
    pd.testing.assert_frame_equal(h,before)
    groups=[]
    for (scenario,model),g in calls[calls.classification_status.eq('cv_scored')&calls.cycle.ge(2016)].groupby(['scenario','model']):
        for label,q in [('all',g),('competitive',g[g.history_selection_10pp.eq('competitive')]),
                        ('not_selected',g[g.history_selection_10pp.eq('not_selected')]),('unknown_history',g[g.history_selection_10pp.eq('unknown_history')]),
                        ('polled',g[g.n_samples.gt(0)]),('no_polls',g[g.n_samples.eq(0)])]:
            if len(q):groups.append(dict(scenario=scenario,model=model,group=label,n=len(q),correct=int(q.correct.sum()),
                mae_pp=100*(q.prediction-q.actual).abs().groupby(q.cycle).mean().mean()))
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
    fit_table=pd.DataFrame([{k:f.get(k) for k in ['scenario','cycle','model','base','feature_set','selected_features','alpha',
        'nominal_parameters','effective_df','training_cycles','training_rows','effective_cycles','training_max_cycle',
        'applied_rows','unchanged_no_poll_rows','validation_mae_pp']} for f in fits])
    current=predictions[predictions.actual.isna()].pivot(index=['scenario','target_id','geography','n_samples'],columns='model',values='prediction')*100
    assert not predictions[predictions.actual.isna()].scenario.eq('oct31').any()
    # Paired changed calls against each model's own reference (recent cycles).
    changes=[]
    for (scenario,model),g in calls[calls.classification_status.eq('cv_scored')&calls.cycle.ge(2016)].groupby(['scenario','model']):
        if '__' not in model:continue
        base=model.split('__')[0]
        ref=calls[calls.scenario.eq(scenario)&calls.model.eq(base)][['target_id','prediction','correct']]
        q=g.merge(ref,on='target_id',validate='one_to_one',suffixes=('','_base'))
        changed=q[np.sign(q.prediction)!=np.sign(q.prediction_base)].copy()
        changed['change']=np.where(changed.correct,'repaired','spoiled')
        changes.append(changed[['scenario','cycle','target_id','geography','model','base','actual','prediction_base','prediction','change','history_selection_10pp']])
    frames=dict(predictions=predictions,folds=folds,tuning=tuning,state_calls=calls,cycle_metrics=cycles,summary=summary,groups=groups,
        fit_summary=fit_table,current_states=current.reset_index(),independent_audit=pd.DataFrame(audits),changed_calls=pd.concat(changes,ignore_index=True))
    for name,frame in frames.items():frame.to_parquet(out/(name+'.parquet'),index=False)
    (out/'fits.json').write_text(json.dumps(fits,indent=2,allow_nan=False)+'\n')
    settings=dict(version='momentum-approval-shared-comparison-v1',feature_sets=FEATURES,half_life_years=HALF_LIFE,alpha_grid=ALPHAS,
        best_base='prequential fixed last5-cycle/8-year state-bias polling; state shrinkage tuned on Y-2',
        optional_selection='Y-2 MAE over none/constant/momentum/approval/both, then refit',
        approval='fixed WH-signed overall approval LEVEL score; not whole raw approval family',
        independently_audited_fixed_final_fits=len(audits),independent_inner_candidates=int(sum(x['inner_candidates'] for x in audits)),
        reference_parity=parity,automatic_model_promotion=False,
        source_files={k:{'path':str(p),'sha256':hashes[k]} for k,p in sources.items()})
    (out/'settings.json').write_text(json.dumps(settings,indent=2)+'\n')
    for k,p in sources.items():assert hashlib.sha256(p.read_bytes()).hexdigest()==hashes[k]
    shutil.copy2(sources['data_inputs'],out/'source_data_inputs.json')
    for name in ['momentum_approval_models.py','run_momentum_approval.py','recency_state_baselines.py','audit_recency_states.py',
                 'feature_scores.py','poll_error_baselines.py','cycle_cv.py','winner_classification.py','senate_summary.py']:
        shutil.copy2(lab/'scripts'/name,out/name)
    shutil.copy2(lab/'config/fixed_feature_scores_v2.json',out/'fixed_feature_scores_v2.json')
    (out/'manifest.json').write_text(json.dumps({p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(out.iterdir())
        if p.is_file() and p.name!='manifest.json'},indent=2)+'\n')
    print('Verified',len(audits),'fixed final fits;',settings['independent_inner_candidates'],'inner candidates; reference parity:',parity,flush=True)
    return out,frames,fits

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--parent',type=Path,required=True);a=p.parse_args()
    run_experiment(Path(__file__).resolve().parents[1],a.parent)
