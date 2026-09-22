"""Presentation labels must not change model identifiers or numeric results."""
from pathlib import Path
import sys
import unittest
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
from model_labels import label_frame
from output_publication import markdown_table


class ModelLabelTests(unittest.TestCase):
    def test_labels_leave_inputs_and_values_unchanged(self):
        source = pd.DataFrame({'model': ['Bayesian', 'Non-Bayesian corrected'], 'p_dem': [.6, .4]})
        before = source.copy(deep=True)
        shown = label_frame(source)
        pd.testing.assert_frame_equal(source, before)
        pd.testing.assert_series_equal(source.p_dem, shown.p_dem)
        self.assertEqual(shown.model.tolist(), ['Gaussian Bayesian', 'Non-Bayesian corrected'])
        self.assertIn('Gaussian Bayesian', markdown_table(source))

    def test_pivot_and_mixture_labels(self):
        frame = pd.DataFrame([[.7]], columns=pd.MultiIndex.from_tuples([('Bayesian', 'D')]))
        self.assertEqual(label_frame(frame).columns[0], ('Gaussian Bayesian', 'D'))
        weights = pd.Series([.25], index=['Bayesian'])
        self.assertEqual(label_frame(weights).index[0], 'Gaussian Bayesian')
        self.assertEqual(weights.index[0], 'Bayesian')
