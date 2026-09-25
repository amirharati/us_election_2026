"""Event probabilities from saved Gaussian parameters and full joint draws.

Loading and evaluating a forecast never fits a model or accesses the network.
Mixtures reuse component draws; shifts translate the whole joint vector.
"""
from pathlib import Path
import json
import numpy as np
import pandas as pd
from scipy.stats import norm


class PredictiveDistributions:
    def __init__(self, run):
        run=Path(run)
        self.pred=pd.read_parquet(run/'predictions.parquet').query('cycle == 2026')
        self.config=json.loads((run/'run.json').read_text()).get('ensemble') or {}
        self.arrays={}
        for path in [run/'main_joint.npz',*sorted((run/'model_forecasts').glob('*.npz'))]:
            with np.load(path,allow_pickle=False) as a:
                name=str(a['model']) if 'model' in a else 'Bayesian'
                if name in self.arrays:raise ValueError('Duplicate predictive model: '+name)
                self.arrays[name]={k:a[k] for k in a.files}
            a=self.arrays[name]
            rows=self.pred[self.pred.model.eq(name)].set_index('target_id')
            ids=a['target_ids'].astype(str).tolist()
            if len(ids)!=len(set(ids)) or set(ids)!=set(rows.index):raise ValueError('Predictive target mapping differs: '+name)
            a['geographies']=rows.loc[ids,'geography'].tolist()
            if len(set(a['geographies']))!=len(ids):raise ValueError('Ambiguous predictive geography')
            if 'samples' in a:
                if a['samples'].ndim!=2 or a['samples'].shape[1]!=len(ids) or not len(a['samples']) or not np.isfinite(a['samples']).all():
                    raise ValueError('Invalid predictive samples: '+name)

    def _components(self, model, state):
        if model in ('Four-model mixture','Mixture + polling 10%'):
            weights=self.config.get('component_weights',{})
            if not weights or any(w<0 for w in weights.values()) or not np.isclose(sum(weights.values()),1):
                raise ValueError('Missing or invalid saved mixture weights')
            mix=self.pred[self.pred.model.eq('Four-model mixture')].set_index('geography')
            selected=self.pred[self.pred.model.eq(model)].set_index('geography')
            delta=float(selected.loc[state,'margin_pp']-mix.loc[state,'margin_pp'])
        else:weights={model:1.};delta=0.
        for name,weight in weights.items():
            a=self.arrays.get(name,{})
            if 'samples' not in a:
                raise ValueError('Full predictive samples missing for '+name+'. Run notebook 04 or export_predictive_distributions.py once; market scans never rerun inference.')
            yield weight,a['samples'][:,a['geographies'].index(state)]+delta

    def margin_probability(self, model, state, lower, upper, lower_closed=True, upper_closed=False):
        """P(lower <= M < upper), with explicit endpoints for reflected R bands."""
        if np.isnan(lower) or np.isnan(upper) or lower>upper:raise ValueError('Invalid margin interval')
        if model=='Bayesian':
            a=self.arrays[model];i=a['geographies'].index(state)
            mu=float(a['mean'][i]);sd=float(np.sqrt(a['covariance'][i,i]))
            if not np.isfinite(mu) or not np.isfinite(sd) or sd<=0:raise ValueError('Invalid Gaussian parameters')
            zlo=(lower-mu)/sd;zhi=(upper-mu)/sd
            # Survival function avoids cancellation in the positive tail.
            p=norm.sf(zlo)-norm.sf(zhi) if zlo>=0 else norm.cdf(zhi)-norm.cdf(zlo)
            return dict(probability=float(p),probability_kind='Analytic Gaussian CDF',simulation_draws=0)
        p=0.;count=0
        for weight,x in self._components(model,state):
            mask=(x>=lower if lower_closed else x>lower)&(x<=upper if upper_closed else x<upper)
            p+=weight*float(mask.mean());count+=len(x)
        return dict(probability=float(np.clip(p,0,1)),probability_kind='Full weighted joint simulations' if model.startswith(('Four-model','Mixture')) else 'Full posterior simulations',simulation_draws=count)


FORMULAS = '''The code maps supported contract types to explicit events. It does not hardcode a probability for each market.

| Contract | Yes probability |
|---|---|
| Democratic winner | P(D minus R margin > 0) |
| Republican winner | 1 minus P(D minus R margin > 0) |
| Democratic margin from a to b | P(a <= margin < b) |
| Republican margin from a to b | P(-b < margin <= -a) |
| Democratic Senate control | P(D/Independent seats >= 51) |
| Republican Senate control | P(D/Independent seats <= 50) |
| Republican seat total | Sum of saved seat probabilities satisfying the stated exact/at-least/at-most condition |
| Buy No | 1 minus the corresponding Yes probability |

Gaussian state events use its analytic CDF. Student-t and mixture state events count matching full simulations, with saved component weights for mixtures. Chamber events use saved joint seat frequencies, preserving state dependence. Simulation estimates have Monte Carlo error; zero observed events does not prove impossibility. No quantile interpolation or Gaussian approximation of the Student-t/mixture is used. Unrecognized or incompatible settlement rules remain unpriced.
'''
