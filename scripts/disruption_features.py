"""A simple OR of elevated health, financial and security proxies, preserving NaNs."""
import numpy as np
import pandas as pd


def nullable_or(frame):
    """1 if any known input is 1; 0 only if every input is known and 0."""
    if frame.shape[1] == 0:
        raise ValueError('OR needs at least one input')
    if not frame.isin([0, 1]).where(frame.notna(), True).all().all():
        raise ValueError('OR inputs must be 0, 1 or missing')
    return pd.Series(np.where(frame.eq(1).any(axis=1), 1.0,
                             np.where(frame.notna().all(axis=1), 0.0, np.nan)), index=frame.index)


def monthly_disruption(inputs, as_of, quantile=.95, lookback=120, min_months=60):
    """Monthly value > prior 120-month 95th percentile, needing 60 prior values.

    Parameters are fixed descriptive choices, not selected using election outcomes.
    Only closed reference months enter. Historical publication vintages are not certified.
    """
    if not inputs or not 0 < quantile < 1 or not 1 <= min_months <= lookback:
        raise ValueError('Invalid inputs or threshold configuration')
    series = {}
    for name, value in inputs.items():
        if not isinstance(value.index, pd.PeriodIndex) or value.index.freqstr != 'M' or value.index.has_duplicates:
            raise ValueError('Each input must have a unique monthly PeriodIndex')
        s = value.astype(float).sort_index()
        if np.isinf(s).any():
            raise ValueError('Infinite values are not valid measurements')
        series[name] = s
    end = pd.Timestamp(as_of).to_period('M') - 1
    months = pd.period_range(min(s.index.min() for s in series.values()), end, freq='M')
    flags = pd.DataFrame(index=months)
    ledger = []
    for name, s in series.items():
        values = s.reindex(months)
        past = values.shift(1)
        threshold = past.rolling(lookback, min_periods=min_months).quantile(quantile)
        count = past.rolling(lookback, min_periods=0).count().fillna(0).astype(int)
        known = values.notna() & threshold.notna()
        flag = (values > threshold).astype(float).where(known)
        flags[name] = flag
        ledger.append(pd.DataFrame({'month': months.astype(str), 'component': name,
                      'value': values.to_numpy(), 'threshold': threshold.to_numpy(),
                      'prior_observed_months': count.to_numpy(), 'flag': flag.to_numpy(),
                      'status': np.where(values.isna(), 'missing_source_value',
                                np.where(threshold.isna(), 'insufficient_prior_history', 'observed'))}))
    flags['extraordinary_event_any'] = nullable_or(flags)
    flags.index.name = 'month'
    return flags, pd.concat(ledger, ignore_index=True)


def cycle_disruption(flags, years, as_of):
    """Inclusive four-calendar-year lookback, preserving the user's 2020→2024 rule.

    For cycle Y, include January of Y-4 through its September cutoff (or last
    closed month for a live earlier cutoff). This includes the current year and
    four prior calendar years; it is explicitly NOT a rolling 48-month window.
    Also retain the ordinary two-year cycle flag for comparison.
    """
    if 'extraordinary_event_any' not in flags:
        raise ValueError('Missing monthly combined flag')
    requested = sorted(set(years))
    if not requested or any(y % 2 for y in requested):
        raise ValueError('Use regular even election cycles')
    if max(requested) > pd.Timestamp(as_of).year:
        raise ValueError('Cannot build a future election cycle')
    last_closed = pd.Timestamp(as_of).to_period('M') - 1
    rows = []
    for year in requested:
        cutoff = min(pd.Timestamp(year, 9, 30), pd.Timestamp(as_of))
        end = min(cutoff.to_period('M'), last_closed)
        recent = pd.period_range(f'{year-1}-01', end, freq='M')
        extended = pd.period_range(f'{year-4}-01', end, freq='M')
        base = nullable_or(flags.reindex(recent).T)
        memory = nullable_or(flags.reindex(extended).T)
        rows.append(dict(cycle=year, window_start=str(recent.min()), window_end=str(end),
                         lookback_start=str(extended.min()), cutoff=cutoff.date().isoformat(),
                         expected_months=len(extended),
                         **{col: base[col] for col in flags.columns},
                         **{col+'_4y': memory[col] for col in flags.columns},
                         contributing_months='|'.join(str(m) for m in extended
                             if m in flags.index and flags.loc[m,'extraordinary_event_any']==1)))
    return pd.DataFrame(rows)
