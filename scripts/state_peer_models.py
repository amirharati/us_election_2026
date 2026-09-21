"""Past-only interstate prediction using other states' observable polling shifts.

State correlations alone cannot reveal an unobserved current polling error.
Predict actual-minus-prior (or remaining polling/bias error) from *other states'*
current poll-minus-prior signals. Missing Senate races/polls are not zero swings.
Ridge on a mean-filled design has a PSD Gram matrix, unlike naive inversion of
a sparse pairwise covariance matrix. Every state-cycle is one training unit.
"""
import numpy as np
import pandas as pd
from poll_error_baselines import correction_folds

BASES={'prior':'prior','polling':'poll_baseline','bias':'bias_prediction'}
ALPHAS=[1.,10.,100.]
WINDOWS=[10,5]
ARCHITECTURES=['constant','one','all']
HALF_LIFE=8.
MIN_PAIRS=3
INTERCEPT_MASS=3.
BLEND_SCALES=[0.,1.,3.,10.,float('inf')]


def weighted_corr(x,y,w):
    x,y,w=map(lambda a:np.asarray(a,float),(x,y,w))
    x=x-np.average(x,weights=w);y=y-np.average(y,weights=w)
    denom=np.sqrt(np.dot(w,x*x)*np.dot(w,y*y))
    return float(np.dot(w,x*y)/denom) if denom>1e-15 else np.nan


def panel(frame):
    """Aggregate simultaneous regular/special contests without pseudo-replication."""
    f=frame.copy()
    f['signal']=(f.poll_baseline-f.prior).where(f.n_samples.gt(0))
    return f.groupby(['cycle','geography']).signal.mean().unstack('geography')


def fit_peer(train,test,base='prior',architecture='all',alpha=10.,lookback=10):
    if base not in BASES or architecture not in ARCHITECTURES:
        raise ValueError('Unknown base or architecture')
    if test.empty or test.cycle.nunique()!=1 or not test.kind.eq('senate').all():
        raise ValueError('One nonempty Senate test cycle required')
    year=int(test.cycle.iloc[0]);col=BASES[base]
    if not train.kind.eq('senate').all() or not train.cycle.lt(year).all():
        raise ValueError('Training must contain only earlier Senate cycles')
    if train.target_id.duplicated().any() or test.target_id.duplicated().any():
        raise ValueError('Duplicate contest')
    if alpha<=0 or not np.isfinite(alpha) or lookback<1:
        raise ValueError('Positive regularization and calendar window required')
    if not np.isfinite(test[['prior','poll_baseline',col]]).all().all():
        raise ValueError('Finite test predictors required')
    tr=train[train.cycle.ge(year-2*lookback)].copy()
    xpast=panel(tr);xnow=panel(test).loc[year].dropna()
    labels=tr[tr.actual.notna()]
    if base!='prior':labels=labels[labels.n_samples.gt(0)]
    labels=labels.assign(response=labels.actual-labels[col])
    responses=labels.groupby(['geography','cycle']).response.mean()
    prediction=test[col].to_numpy().copy();fits=[];edges=[]
    for state in sorted(test.geography.unique()):
        positions=np.flatnonzero(test.geography.eq(state).to_numpy())
        y=responses.loc[state] if state in responses.index.get_level_values(0) else pd.Series(dtype=float)
        years=y.index.to_numpy(int);w=np.exp2(-((year-2)-years)/HALF_LIFE)
        mass=float(w.sum());eff=float(mass**2/(w@w)) if mass else 0.
        info=dict(geography=state,forecast_cycle=year,base=base,architecture=architecture,
                  alpha=float(alpha),lookback=lookback,training_cycles=len(y),effective_cycles=eff,
                  training_max_cycle=int(years.max()) if len(y) else None,training_years=years.tolist(),
                  intercept=0.,peer_adjustment=0.,total_adjustment=0.,donors=[],
                  coefficients={},means={},scales={},current_signals={},
                  status='insufficient_target_history',effective_df=0.)
        if len(y)<MIN_PAIRS:
            fits.append(info);continue
        ym=float(np.average(y,weights=w));intercept=ym*mass/(mass+INTERCEPT_MASS)
        candidates=[]
        if architecture!='constant':
            for donor in sorted(set(xpast.columns)&set(xnow.index)-{state}):
                x=xpast[donor].reindex(years).to_numpy();known=np.isfinite(x)
                if known.sum()<MIN_PAIRS:continue
                ww=w[known];xx=x[known];yy=y.to_numpy()[known]
                mean=float(np.average(xx,weights=ww));sd=float(np.sqrt(np.average((xx-mean)**2,weights=ww)))
                if sd<1e-8:continue
                corr=weighted_corr(xx,yy,ww);neff=float(ww.sum()**2/(ww@ww))
                score=abs(corr)*neff/(neff+5.) if np.isfinite(corr) else 0.
                # Missing historical races/polls use this training-only donor mean.
                z=np.where(known,(x-mean)/sd,0.)
                candidates.append(dict(donor=donor,overlap_cycles=int(known.sum()),effective_overlap=neff,
                    correlation=corr,ranking_score=score,mean=mean,sd=sd,z=z,
                    current=float(xnow[donor]),overlap_years=years[known].tolist()))
        candidates.sort(key=lambda a:(-a['ranking_score'],-a['overlap_cycles'],a['donor']))
        active=candidates[:1] if architecture=='one' else candidates
        z=np.column_stack([a['z'] for a in active]) if active else np.empty((len(y),0))
        # Gram covariance is PSD by construction. SVD is efficient when states > cycles.
        xw=z*np.sqrt(w)[:,None]
        if active:
            u,s,vt=np.linalg.svd(xw,full_matrices=False)
            beta=vt.T@((s/(s*s+alpha))*(u.T@((y.to_numpy()-ym)*np.sqrt(w))))
            current=np.array([(a['current']-a['mean'])/a['sd'] for a in active])
            peer=float(current@beta);df=float(np.sum(s*s/(s*s+alpha)))
        else:beta=np.array([]);peer=0.;df=0.
        applied=positions if base=='prior' else positions[test.iloc[positions].n_samples.gt(0).to_numpy()]
        prediction[applied]=np.clip(prediction[applied]+intercept+peer,-1,1)
        info.update(intercept=intercept,peer_adjustment=peer,total_adjustment=intercept+peer,
            donors=[a['donor'] for a in active],coefficients=dict(zip([a['donor'] for a in active],map(float,beta))),
            means={a['donor']:a['mean'] for a in active},scales={a['donor']:a['sd'] for a in active},
            current_signals={a['donor']:a['current'] for a in active},
            status='fitted_peers' if active else 'intercept_only_no_eligible_peer',
            effective_df=df+mass/(mass+INTERCEPT_MASS))
        fits.append(info)
        for a,b in zip(active,beta):
            edges.append(dict(geography=state,donor=a['donor'],overlap_cycles=a['overlap_cycles'],
                effective_overlap=a['effective_overlap'],correlation=a['correlation'],ranking_score=a['ranking_score'],
                standardized_slope=float(b),current_signal_pp=100*a['current'],
                contribution_pp=100*b*(a['current']-a['mean'])/a['sd'],overlap_years=','.join(map(str,a['overlap_years']))))
    return prediction,fits,pd.DataFrame(edges)


def blend(test,peer,base,scale):
    """No-poll rows use peer estimates; polled weight falls with firm count."""
    own=test[BASES[base]].to_numpy()
    if scale is None:return own.copy(),np.zeros(len(test))
    firms=test.n_firms.to_numpy(float)
    weight=np.ones(len(test)) if np.isinf(scale) else np.divide(scale,scale+firms,out=np.ones(len(test)),where=(scale+firms)>0)
    return (1-weight)*own+weight*peer,weight


def relationships(source,year=2026,lookback=10):
    """Descriptive pair correlations; no pairwise matrix is inverted or fit here."""
    h=source[source.cycle.lt(year)&source.cycle.ge(year-2*lookback)&source.actual.notna()].copy()
    h['margin']=h.actual;h['swing']=h.actual-h.prior
    h['poll_error']=(h.actual-h.poll_baseline).where(h.n_samples.gt(0))
    h['bias_error']=(h.actual-h.bias_prediction).where(h.n_samples.gt(0))
    rows=[]
    for kind in ['margin','swing','poll_error','bias_error']:
        matrix=h.groupby(['cycle','geography'])[kind].mean().unstack()
        states=sorted(matrix.columns)
        for i,a in enumerate(states):
            for b in states[i+1:]:
                q=matrix[[a,b]].dropna();w=np.exp2(-((year-2)-q.index.to_numpy())/HALF_LIFE)
                neff=float(w.sum()**2/(w@w)) if len(w) else 0.
                corr=weighted_corr(q[a],q[b],w) if len(q)>=MIN_PAIRS else np.nan
                rows.append(dict(kind=kind,state_a=a,state_b=b,lookback=lookback,as_of_cycle=year,
                    overlap_cycles=len(q),effective_overlap=neff,correlation=corr,
                    shrunk_correlation=corr*neff/(neff+5.),
                    difference_rmse_pp=float(100*np.sqrt(np.average((q[a]-q[b])**2,weights=w))) if len(q) else np.nan,
                    first_cycle=int(q.index.min()) if len(q) else None,last_cycle=int(q.index.max()) if len(q) else None))
    return pd.DataFrame(rows)


def evaluate(history,progress=None):
    predictions=[];tuning=[];fits=[];edges=[];selections=[];folds=[]
    for scenario,h in history.groupby('scenario'):
        fold=correction_folds(h,h,scenario,2012,6);folds.append(fold)
        for row in fold.itertuples():
            if row.status not in ['cv_scored','forecast_only_no_outcomes']:continue
            year=int(row.cycle);test=h[h.cycle.eq(year)];past=h[h.cycle.lt(year)]
            inner=past[past.cycle.lt(year-2)];valid=past[past.cycle.eq(year-2)&past.actual.notna()]
            common=test[['target_id','cycle','kind','geography','actual','n_samples','n_firms','prior','prior_basis','poll_baseline','bias_prediction']].copy()
            def save(name,p,**extra):
                predictions.append(common.assign(scenario=scenario,status=row.status,model=name,prediction=p,**extra))
            for base,col in BASES.items():save(base,test[col].to_numpy())
            cache={};vcache={}
            for window in WINDOWS:
                for base in BASES:
                    for architecture in ARCHITECTURES:
                        name=f'{base}__peer_{architecture}__last{window}'
                        options=[]
                        for alpha in ([10.] if architecture=='constant' else ALPHAS):
                            vp,vf,ve=fit_peer(inner,valid,base,architecture,alpha,window)
                            cachekey=(window,base,architecture,alpha)
                            vcache[cachekey]=vp
                            p,f,e=fit_peer(past,test,base,architecture,alpha,window);cache[cachekey]=(p,f,e)
                            loss=float(np.abs(vp-valid.actual.to_numpy()).mean())
                            tuning.append(dict(scenario=scenario,cycle=year,model=name,alpha=alpha,scale='not_applicable',validation_cycle=year-2,validation_mae_pp=100*loss))
                            options.append((loss,alpha))
                        loss,alpha=min(options,key=lambda a:(round(a[0],12),-a[1]))
                        p,f,e=cache[(window,base,architecture,alpha)]
                        save(name,p)
                        fits.extend(dict(fit,scenario=scenario,cycle=year,model=name,selected_alpha=alpha) for fit in f)
                        if len(e):edges.append(e.assign(scenario=scenario,cycle=year,model=name))
                        selections.append(dict(scenario=scenario,cycle=year,model=name,alpha=alpha,scale='not_applicable',validation_mae_pp=100*loss))
                # Coverage-aware fusion: joint past-only choice of slope penalty and peer weight.
                for architecture in ['constant','one','all']:
                    for base in ['polling','bias']:
                        name=f'{base}__blend_{architecture}__last{window}'
                        options=[]
                        for alpha in ([10.] if architecture=='constant' else ALPHAS):
                            vp=vcache[(window,'prior',architecture,alpha)]
                            for scale in [None,*BLEND_SCALES]:
                                bp,_=blend(valid,vp,base,scale);loss=float(np.abs(bp-valid.actual.to_numpy()).mean())
                                label='none' if scale is None else 'all' if np.isinf(scale) else str(scale)
                                tuning.append(dict(scenario=scenario,cycle=year,model=name,alpha=alpha,scale=label,validation_cycle=year-2,validation_mae_pp=100*loss))
                                options.append((loss,scale,alpha,label))
                        loss,scale,alpha,label=min(options,key=lambda a:(round(a[0],12),-1 if a[1] is None else a[1],-a[2]))
                        p,_,_=cache[(window,'prior',architecture,alpha)];bp,bw=blend(test,p,base,scale)
                        save(name,bp,peer_weight=bw,peer_prediction=p)
                        selections.append(dict(scenario=scenario,cycle=year,model=name,alpha=alpha,scale=label,validation_mae_pp=100*loss))
                        # Save selected peer fit even when blend chooses a different alpha than standalone.
                        _,f,e=cache[(window,'prior',architecture,alpha)]
                        fits.extend(dict(fit,scenario=scenario,cycle=year,model=name,selected_alpha=alpha,blend_scale=label) for fit in f)
                        if len(e):edges.append(e.assign(scenario=scenario,cycle=year,model=name))
            if progress:progress(f'{scenario} {year}: peer-only, residual correction and coverage blends complete')
    return dict(predictions=pd.concat(predictions,ignore_index=True),tuning=pd.DataFrame(tuning),
                selections=pd.DataFrame(selections),folds=pd.concat(folds,ignore_index=True),
                peer_edges=pd.concat(edges,ignore_index=True)),fits
