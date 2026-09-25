"""Readable model names, without changing persisted identifiers or calculations."""
import re
import pandas as pd


MODEL_GUIDE = (
    'All forecasts shown here use polling evidence when available. '
    'The empirical baseline uses poll averages and historical polling-error patterns. '
    'A 20% shift moves the predicted margin one-fifth of the way toward that baseline while retaining the original model’s uncertainty distribution. '
    'It does not mean the other models omit polls or need correction.'
)


def model_label(value):
    if not isinstance(value,str):return value
    names={'Bayesian':'Gaussian Bayesian', 'Non-Bayesian corrected':'Empirical baseline'}
    if value in names:return names[value]
    for pattern,label in [(r'Mixture \+ polling (\d+(?:\.\d+)?)%', 'Mixture'),
                          (r'Corrected (\d+(?:\.\d+)?)%', 'Gaussian')]:
        match=re.fullmatch(pattern,value)
        if match:return f'{label}: {match.group(1)}% shift toward baseline'
    match=re.fullmatch(r'Plain (\d+(?:\.\d+)?)%',value)
    if match:return f'Gaussian: {match.group(1)}% shift toward poll average'
    return value


def _axis(axis):
    if isinstance(axis, pd.MultiIndex):
        return pd.MultiIndex.from_tuples(
            [tuple(model_label(v) for v in key) for key in axis], names=axis.names)
    return axis.map(model_label)


def label_frame(value):
    """Copy a displayed table; never relabel its underlying calculation inputs."""
    if isinstance(value, pd.DataFrame):
        result = value.copy()
        for col in result:
            if pd.api.types.is_object_dtype(result[col]) or isinstance(result[col].dtype, (pd.StringDtype, pd.CategoricalDtype)):
                result[col] = result[col].map(model_label)
        result.columns = _axis(result.columns)
        result.index = _axis(result.index)
        return result
    if isinstance(value, pd.Series):
        result = value.map(model_label)
        result.index = _axis(result.index)
        result.name = model_label(result.name)
        return result
    return value


def display(*objects, **kwargs):
    """IPython display with consistent labels for model tables."""
    from IPython.display import display as _display
    return _display(*(label_frame(value) for value in objects), **kwargs)
