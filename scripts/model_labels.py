"""Readable model names, without changing persisted identifiers or calculations."""
import pandas as pd


def model_label(value):
    return 'Gaussian Bayesian' if isinstance(value, str) and value == 'Bayesian' else value


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
