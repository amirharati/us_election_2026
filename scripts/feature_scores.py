"""Fixed domain summaries. No labels, regressions or outcome-fitted score weights.

Normalization statistics are estimated from one row per earlier training cycle;
fixed directions and bounded group weights compress economic measurements
into two inputs. Fit this transformer inside each future model training fold.
"""
import json
from pathlib import Path
import numpy as np
import pandas as pd

CONFIG_PATH=Path(__file__).resolve().parents[1]/'config/fixed_feature_scores_v2.json'
MODEL_COLUMNS=['economy_conditions_wh','economy_momentum_wh','approval_wh','disruption_any']


class FixedFeatureScores:
    def __init__(self, config=None):
        self.config=json.loads(CONFIG_PATH.read_text()) if config is None else json.loads(json.dumps(config))
        if 'components' in self.config:
            self.specs=self.config['components']
        else:  # Replay the original fixed v1 recipe explicitly.
            levels=list(self.config['level_directions']);anchors=self.config['change_anchors']
            self.specs={c:dict(score='economy_conditions',group=c,
                direction=self.config['level_directions'][c],weight=1/len(levels),center='history_mean') for c in levels}
            self.specs.update({f'{c}__change_{a}':dict(score='economy_momentum',group=c,
                direction=self.config['level_directions'][c],weight=1/(len(levels)*len(anchors)),center='zero')
                for c in levels for a in anchors})
        self.levels=[c for c,s in self.specs.items() if s['score']=='economy_conditions']
        self.changes=[c for c,s in self.specs.items() if s['score']=='economy_momentum']
        for columns in [self.levels,self.changes]:
            if not columns or not np.isclose(sum(self.specs[c]['weight'] for c in columns),1):
                raise ValueError('Each score must have fixed weights summing to one')
        for spec in self.specs.values():
            if spec['weight']<=0 or spec['direction'] not in (-1,1) or spec['center'] not in ('zero','history_mean'):
                raise ValueError('Invalid component recipe')
        self.stats=None

    def fit(self, history):
        if history.cycle.duplicated().any():raise ValueError('Use exactly one row per training cycle and scenario')
        if 'scenario' in history and history.scenario.nunique()>1:raise ValueError('Do not mix calendar scenarios')
        self.training_cycles=sorted(map(int,history.cycle.unique()))
        self.scenario=history.scenario.iloc[0] if len(history) and 'scenario' in history else None
        self.max_cycle=max(self.training_cycles) if self.training_cycles else None
        self.stats={}
        for c in self.levels+self.changes:
            values=pd.to_numeric(history[c],errors='raise')
            if np.isinf(values).any():raise ValueError('Infinite feature input')
            known=values.dropna();n=len(known)
            sd=float(known.std(ddof=0)) if n else None
            status='ok' if n>=self.config['minimum_history_values'] and sd>1e-12 else ('insufficient_history' if n<self.config['minimum_history_values'] else 'constant_history')
            self.stats[c]=dict(n=n,mean=float(known.mean()) if n else None,scale=sd,
                status=status,center=0. if self.specs[c]['center']=='zero' else float(known.mean()) if n else None)
        return self

    def transform(self, frame, require_later=False):
        if self.stats is None:raise ValueError('Fit training-only normalization first')
        if frame.cycle.duplicated().any():raise ValueError('Use one row per cycle and scenario')
        if 'scenario' in frame and self.scenario is not None and not frame.scenario.eq(self.scenario).all():
            raise ValueError('Mismatched calendar scenario')
        if require_later and self.max_cycle is not None and not frame.cycle.gt(self.max_cycle).all():
            raise ValueError('Forecast must follow normalization training history')
        cap=self.config['clip_component_abs'];records=[];audit=[]
        for row in frame.to_dict('records'):
            cycle=int(row['cycle']);components={}
            for c in self.levels+self.changes:
                stat=self.stats[c];value=row.get(c,np.nan)
                if pd.notna(value) and not np.isfinite(value):raise ValueError('Infinite feature input')
                status='missing_input' if pd.isna(value) else stat['status']
                spec=self.specs[c];direction=spec['direction']
                raw=(value-stat['center'])/stat['scale'] if status=='ok' else np.nan
                value_score=direction*np.clip(raw,-cap,cap) if status=='ok' else np.nan
                components[c]=value_score
                audit.append(dict(cycle=cycle,scenario=row.get('scenario'),context_id=row.get('context_id'),
                    component=c,input_value=value,center=stat['center'],scale=stat['scale'],
                    history_n=stat['n'],direction=direction,unclipped_standardized=raw,
                    score=spec['score'],group=spec['group'],weight=spec['weight'],
                    contribution=spec['weight']*value_score,
                    component_score=value_score,clipped=bool(abs(raw)>cap) if pd.notna(raw) else False,
                    status=status,training_max_cycle=self.max_cycle))
            def strict_score(columns):
                return float(sum(components[c]*self.specs[c]['weight'] for c in columns)) if all(pd.notna(components[c]) for c in columns) else np.nan
            conditions=strict_score(self.levels);momentum=strict_score(self.changes)
            approval=row.get('approval_3m_pct',np.nan)
            if pd.notna(approval) and not 0<=approval<=100:raise ValueError('Approval must be percent in [0,100]')
            approval_score=float(np.clip((approval-self.config['approval_center_pct'])/self.config['approval_scale_pp'],-cap,cap)) if pd.notna(approval) else np.nan
            party=row.get('wh_dem',np.nan)
            if pd.notna(party) and party not in (0,1):raise ValueError('WH party must be binary or missing')
            sign=2*party-1 if pd.notna(party) else np.nan
            disruption=row.get(self.config['disruption_column'],np.nan)
            if pd.notna(disruption) and disruption not in (0,1):raise ValueError('Disruption must be 0,1 or missing')
            pending=row.get('scenario')=='oct31' and not bool(row.get('window_complete',True))
            result={k:row.get(k) for k in ['cycle','scenario','context_id','start_cutoff','previous_cutoff','desired_cutoff','window_complete']}
            result.update(wh_sign=sign,economy_conditions=conditions,economy_momentum=momentum,approval_score=approval_score,
                economy_conditions_wh=sign*conditions,economy_momentum_wh=sign*momentum,approval_wh=sign*approval_score,
                disruption_any=disruption,conditions_known=sum(pd.notna(components[c]) for c in self.levels),
                conditions_required=len(self.levels),momentum_known=sum(pd.notna(components[c]) for c in self.changes),
                momentum_required=len(self.changes),normalization_cycles=len(self.training_cycles),
                normalization_first_cycle=min(self.training_cycles) if self.training_cycles else np.nan,
                normalization_last_cycle=self.max_cycle,calendar_status='pending_cutoff' if pending else 'available_at_cutoff')
            # Preserve components for audits; do not issue an apparent future-October score.
            if pending:
                for c in MODEL_COLUMNS+['economy_conditions','economy_momentum','approval_score']:result[c]=np.nan
            for score,required in [('economy_conditions',self.levels),('economy_momentum',self.changes)]:
                result[score+'_missing_components']='|'.join(c for c in required if pd.isna(components[c]))
            result['model_inputs_complete']=all(pd.notna(result[c]) for c in MODEL_COLUMNS)
            records.append(result)
        return pd.DataFrame(records),pd.DataFrame(audit)

    def metadata(self):
        return dict(config=self.config,scenario=self.scenario,training_cycles=self.training_cycles,statistics=self.stats,
            fitted_electoral_weights=False,normalization='component-specific fixed zero or earlier-cycle mean center; earlier-cycle population SD; no imputation')


def build_score_panel(calendars, config=None):
    """As-of diagnostics: calibrate on strictly earlier cycles for each score row.

For future model fitting, use FixedFeatureScores.fit(inner_train) then transform
both inner_train and validation using that SAME transformer, not this diagnostic
panel's different normalizers as if they were one fitted feature matrix.
"""
    if calendars.duplicated(['scenario','cycle']).any():raise ValueError('Duplicate calendar cycle')
    rows=[];ledgers=[];normalizers=[]
    for scenario,source in calendars.groupby('scenario'):
        for year in sorted(source.cycle.unique()):
            train=source[source.cycle.lt(year)]
            transform=FixedFeatureScores(config).fit(train)
            scored,ledger=transform.transform(source[source.cycle.eq(year)],require_later=True)
            rows.append(scored);ledgers.append(ledger)
            normalizers.append(dict(target_cycle=int(year),scenario=scenario,**{k:v for k,v in transform.metadata().items() if k!='scenario'}))
    # Build once from records so early all-missing rows have stable numeric dtypes.
    return (pd.DataFrame.from_records([r for frame in rows for r in frame.to_dict('records')]),
            pd.DataFrame.from_records([r for frame in ledgers for r in frame.to_dict('records')]),normalizers)
