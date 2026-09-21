"""Additional factor source, stability and coverage checks."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
import simple_bayesian_polling as v1

def complete(out,lab):
    out,lab=Path(out),Path(lab)
    p=pd.read_parquet(out/'predictions.parquet');f=pd.read_parquet(out/'folds.parquet');ss=pd.read_parquet(out/'stability.parquet');starts=pd.read_parquet(out/'stability_starts.parquet');checks={};schecks=[]
    for r in ss.drop_duplicates(['base_model','omitted_cycle']).itertuples():
        z=np.load(out/r.fit_path);schecks.append(r.omitted_cycle not in z['years'] and z['years'].max()<2026 and abs(z['b'].sum())<1e-6 and np.max(abs(z['u']))<=.950001)
    checks['stability_fit_constraints']=all(schecks);checks['stability_optimizers_converged']=bool(starts.success.all())
    sourcechecks=[]
    for (sc,year,base),q in p.groupby(['scenario','cycle','base_model']):
        ref=q[q.lambda_value.eq(0)].drop_duplicates('target_id').set_index('target_id')
        for model,t in q.groupby('model'):
            t=t.set_index('target_id').loc[ref.index];sourcechecks.append(np.array_equal(t.actual,ref.actual,equal_nan=True) and np.array_equal(t.prior,ref.prior,equal_nan=True) and np.array_equal(t.q_pp,ref.q_pp,equal_nan=True) and np.allclose(t.firm_mass,ref.firm_mass))
    checks['all_lambda_inputs_labels_preserved']=all(sourcechecks)
    trend=lab/'reports/poll_trend_review/20260920T041249.965124Z';digest=v1.verify(trend);ag=pd.read_parquet(trend/'aggregates.parquet');ag=ag[ag.variant.eq('baseline')][['scenario','target_id','sample_count','recent_firms']].rename(columns={'sample_count':'admitted_samples'});pp=p.merge(ag,on=['scenario','target_id'],validate='many_to_one');assert pp.admitted_samples.notna().all();pp['coverage_group']=np.where(pp.admitted_samples.eq(0),'no_polls',np.where(pp.recent_firms.le(2),'low_recent_0_2_firms','recent_3plus_firms'));rows=[]
    for first in [2012,2016]:
     for (sc,model,group),q in pp[pp.cycle.between(first,2024)].groupby(['scenario','model','coverage_group']):
        metrics=q.groupby('cycle')[['absolute_error_pp','wis_pp','brier']].mean().mean().to_dict();rows.append(dict(first_cycle=first,scenario=sc,model=model,coverage_group=group,n=len(q),correct=int(q.correct.sum()),coverage70=q.coverage70.mean(),coverage95=q.coverage95.mean(),**metrics))
    pd.DataFrame(rows).to_parquet(out/'coverage_scores.parquet',index=False)
    rows=[]
    for r in f[f.cycle.eq(2026)].itertuples():
     q=p[p.cycle.eq(2026)&p.model.eq(r.model)].sort_values('target_id');z=np.load(out/r.forecast_path);C=z['covariance'];R=C/np.sqrt(np.outer(np.diag(C),np.diag(C)))
     for i in range(len(q)):
      for j in range(i+1,len(q)):rows.append(dict(model=r.model,state1=q.geography.iloc[i],state2=q.geography.iloc[j],rho=R[i,j]))
    pd.DataFrame(rows).to_parquet(out/'current_pair_correlations.parquet',index=False)
    checks['scenario_factor_decomposition']=bool(np.allclose(pd.read_parquet(out/'scenario_states.parquet').eval('national_shift_pp+pattern_shift_pp+local_shift_pp'),pd.read_parquet(out/'scenario_states.parquet').margin_change_pp))
    a=json.loads((out/'audit.json').read_text());a['checks'].update(checks);a['passed']=bool(all(a['checks'].values()));assert a['passed'];v1.json_write(out/'audit.json',a);v1.json_write(out/'review_sources.json',{str(trend):digest});v1.manifest(out);v1.json_write(out.parent/'latest.json',dict(artifact=out.name,manifest_sha256=v1.verify(out)));print(a)
