from pathlib import Path
import sys,json,copy
import numpy as np,pandas as pd
lab=Path('/Users/amir/projects/labs/ml-foundations/prob_ml_course/labs/US_election_2026');sys.path.insert(0,str(lab/'scripts'))
from three_model_comparison import prepare_direct,independent_prediction
from recency_state_baselines import predict_problem
from state_score_baselines import solve_partial
out=lab/'reports/baselines/20260918T055206.305739Z/three_models/20260918T225135.051653Z'
settings=json.loads((Path(json.loads((out/'settings.json').read_text())['source'])/'settings.json').read_text())
h=pd.read_parquet(settings['sources']['history']['path']);h=h.query("base=='fixed5_8' and scenario=='matched_live'")
cal=pd.read_parquet(settings['sources']['calendars']['path']).query("scenario=='matched_live'")
train=h[h.cycle.lt(2026)&h.actual.notna()];test=h[h.cycle.eq(2026)];p=prepare_direct(train,test,cal)
pred,fit,_=predict_problem(p,.1,.1,True);expected=independent_prediction(p,.1,.1);assert np.allclose(pred,expected,atol=1e-10)
mask=train.geography.eq('TX').to_numpy();tx=train[mask].copy();z=p['z'][mask];w=p['weights'][mask];y=p['response'][mask]
scores=p['scores'].set_index('cycle');cc=cal.set_index('cycle')
for c in ['economy_momentum_wh','approval_wh']:tx[c]=scores.loc[tx.cycle,c].to_numpy()
tx['wh_party']=np.where(cc.loc[tx.cycle,'wh_dem'].to_numpy()==1,'D','R')
tx['economic_z']=z[:,1];tx['approval_z']=z[:,2];tx['weight_share']=w/w.sum();tx['actual_pp']=100*y
tx['poll_error_pp']=np.where(tx.n_samples.gt(0),100*(tx.actual-tx.poll_baseline),np.nan)
tx['state_fit_pp']=100*z@np.array(list(fit['states']['TX']['total'].values()))

def corr(x,y,w):
 x=x-np.average(x,weights=w);y=y-np.average(y,weights=w)
 return np.sum(w*x*y)/np.sqrt(np.sum(w*x*x)*np.sum(w*y*y))
print('TX inputs/outcomes:');print(tx[['cycle','wh_party','economy_momentum_wh','economic_z','approval_z','weight_share','actual_pp','n_samples','poll_error_pp']].round(4).to_string(index=False))
print('CORRELATIONS',dict(economy_actual=corr(z[:,1],y,w),approval_actual=corr(z[:,2],y,w),economy_approval=corr(z[:,1],z[:,2],w)))
shared=np.array(list(fit['shared_coefficients'].values()));total=np.linalg.solve(z.T@(w[:,None]*z)+.1*np.eye(3),z.T@(w*y)+.1*shared)
assert np.allclose(total,list(fit['states']['TX']['total'].values()))
# Exact local ridge-with-shared-anchor partial regression, including penalty pseudo-observations.
a=np.vstack([np.sqrt(w)[:,None]*z,np.sqrt(.1)*np.eye(3)]);b=np.r_[np.sqrt(w)*y,np.sqrt(.1)*shared]
other=a[:,[0,2]];xr=a[:,1]-other@np.linalg.lstsq(other,a[:,1],rcond=None)[0]
yr=b-other@np.linalg.lstsq(other,b,rcond=None)[0];influence=100*xr*yr/(xr@xr)
assert np.isclose(influence.sum(),100*total[1]);tx['economic_coefficient_contribution_pp_per_sd']=influence[:len(tx)]
print('Partial regression contributions:',tx[['cycle','economic_coefficient_contribution_pp_per_sd']].round(4).to_string(index=False));print('Shared-anchor pseudo contribution:',influence[len(tx):].sum())
rows=[]
for year in tx.cycle:
 keep=~((train.geography=='TX')&(train.cycle==year)).to_numpy()
 # Hold preprocessing, per-row weights and selected penalties fixed to isolate a row's influence.
 sh,de,comp=solve_partial(p['z'][keep],p['response'][keep],p['weights'][keep],train.geography.to_numpy()[keep],.1,.1,'state_partial')
 beta=sh+de['TX'];rows.append(dict(removed_tx_cycle=int(year),economic_slope_pp_per_sd=100*beta[1],approval_slope_pp_per_sd=100*beta[2]))
loo=pd.DataFrame(rows);print('Leave one TX cycle, frozen design:',loo.round(4).to_string(index=False))
rows=[]
for a1 in [.1,1.,10.,100.]:
 for sp in [.1,1.,10.,100.]:
  _,f,_=predict_problem(p,a1,sp,True)
  rows.append(dict(alpha=a1,state_penalty=sp,economic_slope_pp_per_sd=100*f['states']['TX']['total']['economy_momentum_wh']))
sens=pd.DataFrame(rows);print('PENALTY',sens.round(4).to_string(index=False))
# Remove approval only, retaining the existing score scaling and same penalties.
r=copy.copy(p);r['z']=p['z'][:,:2];r['future']=p['future'][:,:2]
sh,de,_=solve_partial(r['z'],r['response'],r['weights'],train.geography.to_numpy(),.1,.1,'state_partial')
print('WITHOUT_APPROVAL_TX_ECON',100*(sh+de['TX'])[1])
diagnostic_dir=lab/'reports/diagnostics/texas_economic_slope_20260918'
diagnostic_dir.mkdir(parents=True,exist_ok=True)
tx.to_parquet(diagnostic_dir/'history.parquet',index=False);loo.to_parquet(diagnostic_dir/'leave_one_out.parquet',index=False);sens.to_parquet(diagnostic_dir/'penalties.parquet',index=False)

import hashlib
summary=dict(target='actual final D-R margin, not polling error',source=str(out),training_texas_rows=len(tx),no_poll_texas_rows=int(tx.n_samples.eq(0).sum()),
    effective_texas_cycles=fit['states']['TX']['effective_cycles'],weighted_corr_economy_outcome=corr(z[:,1],y,w),weighted_corr_approval_outcome=corr(z[:,2],y,w),weighted_corr_economy_approval=corr(z[:,1],z[:,2],w),
    full_economic_slope_pp_per_sd=100*total[1],without_approval_slope_pp_per_sd=100*(sh+de['TX'])[1],
    independent_prediction_max_difference=float(np.max(np.abs(pred-expected))),
    sources={k:v for k,v in settings['sources'].items() if k in ['history','calendars']})
(diagnostic_dir/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
(diagnostic_dir/'diagnose_texas_economic_slope.py').write_bytes(Path(__file__).read_bytes())
(diagnostic_dir/'manifest.json').write_text(json.dumps({p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in diagnostic_dir.iterdir() if p.is_file() and p.name!='manifest.json'},indent=2)+'\n')
print('Saved diagnostic:',diagnostic_dir)
