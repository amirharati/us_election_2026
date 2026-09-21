"""Read-only comparison of retained current models and blends."""
import json
import numpy as np
import pandas as pd
import election_lab as lab

CORE=['Bayesian','Matched Student-t (df5)','Older Gaussian','Student-t research helper','Non-Bayesian corrected']
DISPLAY=CORE+['Four-model mixture','Mixture + polling 20%']


def state_ranges(p,scope):
    rows=[]
    for tid,g in p.groupby('target_id'):
        r=dict(target_id=tid,geography=g.geography.iloc[0],special=g.special.iloc[0],scope=scope)
        for col,short in [('margin_pp','margin'),('p_dem','prob'),('width70_pp','width70'),('width95_pp','width95')]:
            lo=g.loc[g[col].idxmin()];hi=g.loc[g[col].idxmax()]
            r.update({short+'_min':lo[col],short+'_max':hi[col],short+'_spread':hi[col]-lo[col],short+'_min_model':lo.model,short+'_max_model':hi.model})
        r['point_call_disagrees']=g.margin_pp.gt(0).nunique()>1;r['probability_call_disagrees']=g.p_dem.gt(.5).nunique()>1
        rows.append(r)
    return pd.DataFrame(rows)


def run():
    live=lab.latest_run('live');history=lab.latest_run('portfolio')
    meta=json.loads((live/'run.json').read_text())
    p=pd.read_parquet(live/'predictions.parquet');s=pd.read_parquet(live/'seats.parquet')
    main=p[p.model.eq('Bayesian')].sort_values('target_id')
    cols=['target_id','geography','special','model','margin_pp','p_dem','sigma_pp','lo70_pp','hi70_pp','lo95_pp','hi95_pp','q_pp','firm_mass']
    p=p[cols].copy().assign(family='retained')
    # Never trust inherited auxiliary width fields: derive them from endpoints.
    p['width70_pp']=p.hi70_pp-p.lo70_pp;p['width95_pp']=p.hi95_pp-p.lo95_pp
    p['central95_crosses_physical_bounds']=p.lo95_pp.lt(-100)|p.hi95_pp.gt(100)
    p['D_probability_pct']=100*p.p_dem
    s['D_control_pct']=100*s.p_D_control
    assert not p.duplicated(['target_id','model']).any();assert len(p)==35*16
    polls=main[['target_id','q_pp','firm_mass','sample_count']].rename(columns={'q_pp':'reference_poll_pp','firm_mass':'reference_firm_mass'})
    polls['admitted_poll']=polls.reference_poll_pp.notna()
    ranges=pd.concat([state_ranges(p[p.model.isin(CORE)],'five core'),state_ranges(p[p.model.isin(CORE[:4])],'four Bayesian'),state_ranges(p,'all retained/blends')],ignore_index=True).merge(polls,on='target_id',validate='many_to_one')
    pairs=[];pair_states=[]
    comparisons=[('Bayesian','Older Gaussian'),('Bayesian','Matched Student-t (df5)'),('Older Gaussian','Student-t research helper'),('Bayesian','Non-Bayesian corrected'),('Bayesian','Four-model mixture'),('Four-model mixture','Mixture + polling 20%')]
    for a,b in comparisons:
        left=p[p.model.eq(a)].set_index('target_id');right=p[p.model.eq(b)].set_index('target_id').loc[left.index]
        d=left[['geography','special']].copy();d['left']=a;d['right']=b
        for c in ['margin_pp','p_dem','width70_pp','width95_pp']:d['delta_'+c]=right[c]-left[c]
        d['admitted_poll']=left.q_pp.notna();pair_states.append(d.reset_index())
        pairs.append(dict(left=a,right=b,mean_abs_margin_difference_pp=abs(d.delta_margin_pp).mean(),max_abs_margin_difference_pp=abs(d.delta_margin_pp).max(),
                          mean_abs_probability_difference_pct=100*abs(d.delta_p_dem).mean(),mean_width70_change_pp=d.delta_width70_pp.mean(),mean_width95_change_pp=d.delta_width95_pp.mean(),
                          expected_D_change=d.delta_p_dem.sum(),unpolled_expected_D_change=d.loc[~d.admitted_poll,'delta_p_dem'].sum(),polled_expected_D_change=d.loc[d.admitted_poll,'delta_p_dem'].sum()))
    # Covariance and seat-tail summaries from saved joint forecasts.
    moments={'Bayesian':dict(np.load(live/'main_joint.npz'))}
    for f in sorted((live/'model_forecasts').glob('*.npz')):
        z=dict(np.load(f));moments[str(z['model'])]=z
    dependencies=[]
    for name,z in moments.items():
        C=z['covariance'];sd=np.sqrt(np.diag(C));corr=C/np.outer(sd,sd);off=corr[np.triu_indices(len(C),1)]
        freq=z['seat_count_frequency'].astype(float);freq/=freq.sum();counts=np.arange(len(freq));m=counts@freq
        dependencies.append(dict(model=name,mean_state_correlation=off.mean(),min_state_correlation=off.min(),max_state_correlation=off.max(),seat_sd=np.sqrt(((counts-m)**2)@freq),p_D_at_least_55=freq[counts>=55].sum(),p_D_45_or_fewer=freq[counts<=45].sum(),p_tie50=freq[50]))
    out=lab.new_run('model_disagreement');hist=pd.read_parquet(history/'summary.parquet')
    for name,t in dict(predictions=p,seats=s,state_ranges=ranges,pair_summary=pd.DataFrame(pairs),pair_states=pd.concat(pair_states),dependencies=pd.DataFrame(dependencies),historical_summary=hist).items():t.to_parquet(out/(name+'.parquet'),index=False)
    lab.finish(out,dict(kind='current_model_disagreement',as_of=meta['as_of'],core_models=CORE,display_models=DISPLAY,sources={str(x.relative_to(lab.ROOT)):lab.sha(x/'manifest.json') for x in [live,history]},
                       source_code_sha256=lab.sha(__file__),scope='16 retained current model/blend forecasts; poll-weight experiments excluded; no new fitted model',freshness=meta['freshness'],
                       caveats='Models/variants are dependent, not votes. Non-Bayesian chamber uncertainty assumes independence. No current accuracy labels. Historical architecture comparisons are exploratory.'))
    return out
