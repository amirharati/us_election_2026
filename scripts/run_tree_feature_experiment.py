"""Reproducible tree experiment runner used by the baseline notebook."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,shutil
import pandas as pd
import numpy as np
import sklearn
from tree_feature_models import evaluate,DEPTHS,N_TREES,RAW_GROUPS,SEED
from winner_classification import classification_report
from senate_summary import senate_report


def run_experiment(lab,parent,n_trees=N_TREES):
    lab,parent=Path(lab).resolve(),Path(parent).resolve()
    out=parent/'tree_feature_models'/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')
    out.mkdir(parents=True,exist_ok=False)
    bias=max((parent/'state_poll_bias').glob('*/manifest.json')).parent
    sources=dict(history=parent/'poll_error_models/poll_history.parquet',calendars=parent/'contextual/calendars.parquet',
        membership=parent/'cv/competitive/membership.parquet',regression=parent/'recency_direct_models/predictions.parquet',
        bias=bias/'state_calls.parquet',data_inputs=parent/'poll_error_models/data_inputs.json')
    hashes={k:hashlib.sha256(p.read_bytes()).hexdigest() for k,p in sources.items()}
    history=pd.read_parquet(sources['history']);cal=pd.read_parquet(sources['calendars'])
    print('Tree experiment:',out,flush=True)
    def progress(message):
        print(message,flush=True);(out/'progress.txt').write_text(message+'\n')
    pred,folds,tuning,fits,importance,ablation=evaluate(history,cal,n_trees=n_trees,progress=progress)
    keys=['scenario','target_id'];meta=['cycle','kind','geography','actual','n_samples','prior','prior_basis','poll_baseline','status']
    refs=[]
    for name,model,file in [('linear_direct','direct_all__selected','regression'),
                            ('linear_prior','prior_all__selected','regression'),
                            ('polling_bias','bias_state__last5_half8','bias')]:
        old=pd.read_parquet(sources[file]);old=old[old.model.eq(model)]
        base=pred[pred.model.eq('prior')][keys+meta]
        q=base.merge(old[keys+['actual','prediction']],on=keys,how='left',validate='one_to_one',suffixes=('','_reference'))
        if q.prediction.isna().any():raise ValueError('Missing comparison forecast')
        if not (q.actual.eq(q.actual_reference)|(q.actual.isna()&q.actual_reference.isna())).all():raise ValueError('Reference outcome mismatch')
        refs.append(q.drop(columns='actual_reference').assign(model=name))
    pred=pd.concat([pred,*refs],ignore_index=True)
    calls,_,_,_=classification_report(pred)
    calls,cycles,summary=senate_report(calls,pd.read_parquet(sources['membership']))
    groups=[]
    for (scenario,model),g in calls[calls.classification_status.eq('cv_scored')&calls.cycle.ge(2016)].groupby(['scenario','model']):
        for label,q in [('all',g),('competitive',g[g.history_selection_10pp.eq('competitive')]),
                        ('not_selected',g[g.history_selection_10pp.eq('not_selected')]),
                        ('unknown_history',g[g.history_selection_10pp.eq('unknown_history')]),
                        ('polled',g[g.n_samples.gt(0)]),('no_polls',g[g.n_samples.eq(0)])]:
            if len(q):groups.append(dict(scenario=scenario,model=model,group=label,n=len(q),correct=int(q.correct.sum()),
                mae_pp=100*(q.prediction-q.actual).abs().groupby(q.cycle).mean().mean()))
    groups=pd.DataFrame(groups)
    fit_table=pd.DataFrame([{k:f[k] for k in ['scenario','cycle','model','depth','training_rows','features','trees',
        'mean_leaves','minimum_distinct_cycles_per_leaf','validation_mae_pp']}|{'training_cycles':len(f['training_cycles'])} for f in fits])
    imp_summary=importance[importance.cycle.between(2016,2024)].groupby(['scenario','model','feature','group']).agg(
        mean_impurity=('impurity_importance','mean'),cycles=('cycle','nunique'),used_cycles=('impurity_importance',lambda s:int(s.gt(0).sum()))).reset_index()
    ab_summary=ablation.groupby(['scenario','model','group']).agg(mean_removal_cost_pp=('removal_cost_pp','mean'),
        median_removal_cost_pp=('removal_cost_pp','median'),helpful_cycles=('removal_cost_pp',lambda s:int(s.gt(0).sum())),
        cycles=('cycle','nunique'),minimum=('removal_cost_pp','min'),maximum=('removal_cost_pp','max')).reset_index()
    for f in fits:
        assert f['training_max_cycle']<f['cycle'] and f['validation_cycle']==f['cycle']-2
        grid=tuning[tuning.scenario.eq(f['scenario'])&tuning.cycle.eq(f['cycle'])&tuning.model.eq(f['model'])]
        choice=min(grid.to_dict('records'),key=lambda x:(round(x['mae_pp']/100,12),x['depth']))
        assert choice['depth']==f['depth'] and np.isclose(choice['mae_pp'],f['validation_mae_pp'])
        for counts in f['cycle_bootstrap_counts']:
            assert sum(counts.values())==len(f['training_cycles']) and max(counts)<f['cycle']
    for row in summary.itertuples():
        q=calls[calls.classification_status.eq('cv_scored')&calls.scenario.eq(row.scenario)&calls.model.eq(row.model)]
        if row.period=='2016_onward':q=q[q.cycle.ge(2016)]
        if row.scope=='with_polls':q=q[q.n_samples.gt(0)]
        if row.subset!='all_admitted':q=q[q['history_selection_'+('5pp' if row.subset.endswith('_5pp') else '10pp')].eq('competitive')]
        assert len(q)==row.contests and int(q.correct.sum())==row.correct
        assert np.isclose(100*(q.prediction-q.actual).abs().groupby(q.cycle).mean().mean(),row.mean_state_mae_pp)
    for _,g in groups.groupby(['scenario','model']):
        q=g.set_index('group');assert q.loc[['competitive','not_selected','unknown_history'],'correct'].sum()==q.loc['all','correct']
    assert not pred[pred.actual.isna()].scenario.eq('oct31').any()
    assert all(hashlib.sha256(p.read_bytes()).hexdigest()==hashes[k] for k,p in sources.items())
    frames=dict(predictions=pred,folds=folds,tuning=tuning,state_calls=calls,cycle_metrics=cycles,summary=summary,
                groups=groups,fit_summary=fit_table,impurity_importance=importance,importance_summary=imp_summary,
                group_ablation=ablation,ablation_summary=ab_summary)
    current=pred[pred.actual.isna()].pivot(index=['scenario','target_id','geography','n_samples'],columns='model',values='prediction')*100
    frames['current_states']=current.reset_index()
    for name,frame in frames.items():frame.to_parquet(out/(name+'.parquet'),index=False)
    (out/'fits.json').write_text(json.dumps(fits,indent=2,allow_nan=False)+'\n')
    settings=dict(version='cycle-bootstrap-feature-trees-v1',depths=DEPTHS,forest_trees=n_trees,random_seed=SEED,
        sklearn_version=sklearn.__version__,min_distinct_rows_leaf=5,min_weight_fraction_leaf=.01,max_features_forest=.7,
        cycle_bootstrap=True,cycle_balanced_weights=True,training_decay=None,raw_groups=RAW_GROUPS,
        raw_exclusions=['arbitrary-base CPI/gasoline levels','absolute real GDP/income levels','calendar dates/year as predictors',
                        'poll inputs','prior/latest outcome as direct predictors'],
        diagnostic_importance_not_used_for_selection=True,automatic_model_promotion=False,
        source_files={k:{'path':str(p),'sha256':hashes[k]} for k,p in sources.items()})
    (out/'settings.json').write_text(json.dumps(settings,indent=2)+'\n')
    shutil.copy2(sources['data_inputs'],out/'source_data_inputs.json')
    for name in ['tree_feature_models.py','run_tree_feature_experiment.py','feature_scores.py','winner_classification.py','senate_summary.py']:
        shutil.copy2(lab/'scripts'/name,out/name)
    shutil.copy2(lab/'config/fixed_feature_scores_v2.json',out/'fixed_feature_scores_v2.json')
    (out/'manifest.json').write_text(json.dumps({p.name:hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted(out.iterdir()) if p.is_file() and p.name!='manifest.json'},indent=2)+'\n')
    return out,frames,fits

if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('--parent',type=Path,required=True)
    args=parser.parse_args();run_experiment(Path(__file__).resolve().parents[1],args.parent)
