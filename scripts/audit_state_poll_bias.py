"""Independent scalar reconstruction of historical state polling offsets."""
import math
from collections import defaultdict
import numpy as np


def reconstruct(train,test,lookback,half_life,architecture,shrinkage):
    year=int(test.cycle.iloc[0]);by_cycle=defaultdict(list);by_state_cycle=defaultdict(list)
    allowed=set(range(year-2*lookback,year,2)) if lookback is not None else None
    for row in train.itertuples():
        if row.cycle>=year:raise ValueError('Future training row')
        if row.n_samples<=0 or not math.isfinite(row.actual):continue
        if allowed is not None and row.cycle not in allowed:continue
        error=float(row.actual-row.poll_baseline)
        by_cycle[int(row.cycle)].append(error)
        by_state_cycle[(row.geography,int(row.cycle))].append(error)
    weight=lambda cycle:1. if half_life is None else 2.**(-((year-2)-cycle)/half_life)
    mass=sum(weight(y) for y in by_cycle)
    shared=sum(weight(y)*sum(e)/len(e) for y,e in by_cycle.items())/mass if mass else 0.
    states={}
    for state in set(test.geography)|{s for s,_ in by_state_cycle}:
        rows=[(year_,sum(e)/len(e)) for (s,year_),e in by_state_cycle.items() if s==state]
        local_mass=sum(weight(y) for y,_ in rows)
        numerator=sum(weight(y)*error for y,error in rows)
        bias=shared if architecture=='shared' or not local_mass else (numerator+shrinkage*shared)/(local_mass+shrinkage)
        states[state]=dict(bias=bias,local_cycles=len(rows),weight_mass=local_mass)
    predictions=[]
    for row in test.itertuples():
        predictions.append(max(-1.,min(1.,row.poll_baseline+states[row.geography]['bias']))
                           if row.n_samples>0 else row.poll_baseline)
    return np.array(predictions),shared,states
