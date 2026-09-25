from pathlib import Path
import sys,unittest
from unittest.mock import patch
import numpy as np
import pandas as pd
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import election_lab
from model_portfolio import make_mixture,configuration,distribution_rows
from live_share_images import state_chart_data,state_images

class MixtureChartTests(unittest.TestCase):
    def test_intervals_use_weighted_mixture_quantiles_not_sd(self):
        config=configuration();components={}
        for name,values in zip(config['component_weights'],[[-30,-20],[-10,0],[1,2],[3,60]]):
            components[name]=dict(predictions=pd.DataFrame({'target_id':['a'],'margin_pp':[np.mean(values)]}),
                draws=np.array(values,dtype=float)[:,None],covariance=np.array([[np.var(values)]]))
        mix=make_mixture(components,config)
        np.testing.assert_array_equal(mix['quantiles68'][:,0],[-20,3])
        np.testing.assert_array_equal(mix['quantiles'][[0,8],0],[-30,60])
        template=pd.DataFrame(dict(scenario=['live'],cycle=[2026],target_id=['a'],geography=['AA'],special=[False],actual=[np.nan],q_pp=[0],firm_mass=[1],history_selection_10pp=[False]))
        with patch('model_portfolio.score_rows',side_effect=lambda x:x):
            p,_=distribution_rows(template,mix,np.array([4.]),'Four-model mixture')
        self.assertEqual((p.lo68_pp.iloc[0],p.hi68_pp.iloc[0]),(-16,7))
        self.assertEqual((p.lo95_pp.iloc[0],p.hi95_pp.iloc[0]),(-26,64))

    def test_chart_uses_mixture_intervals_and_only_four_components(self):
        names=list(configuration()['component_weights'])
        margins=pd.DataFrame({**{n:[v] for n,v in zip(names,[0,2,4,6])},'Non-Bayesian corrected':[999]},index=['AA'])
        predictions=pd.DataFrame(dict(State=['AA'],model=['Four-model mixture'],margin_pp=[3],lo95_pp=[-20],hi95_pp=[30],lo68_pp=[-5],hi68_pp=[8],p_dem=[.6]))
        tables=dict(margins=margins,predictions=predictions)
        q=state_chart_data(tables)
        self.assertAlmostEqual(q.disagreement_pp.iloc[0],20/6)
        with patch('live_share_images.finish',side_effect=lambda fig,*args:fig):
            figures=state_images(tables,names,'.','2026-09-23')
        ax=figures[0].axes[0]
        self.assertEqual(ax.collections[0].get_segments()[0].tolist(),[[-20.,0.],[30.,0.]])
        self.assertEqual(ax.collections[1].get_segments()[0].tolist(),[[-5.,0.],[8.,0.]])
        self.assertTrue(all(g.get_visible() for g in ax.get_ygridlines()))
        self.assertEqual(len(figures[1].axes[0].collections),1)
        import matplotlib.pyplot as plt
        for fig in figures:plt.close(fig)

    def test_polling_colors_use_samples_and_firms_and_preserve_race_order(self):
        from live_share_images import interval_coverage,COVERAGE_COLORS
        rows=pd.DataFrame(dict(target_id=['a','b','c','d'],model=['Four-model mixture']*4,
            recent_samples=[3,2,0,5],recent_firms=[2,2,0,1]))
        coverage=dict(all_contests=rows,parameters=dict(min_samples=3,min_firms=2))
        q=pd.DataFrame(dict(target_id=['c','a','d','b']))
        self.assertEqual(interval_coverage(q,coverage),[COVERAGE_COLORS[k] for k in ['none','adequate','thin','thin']])
        with self.assertRaisesRegex(ValueError,'Missing polling coverage'):
            interval_coverage(pd.DataFrame(dict(target_id=['missing'])),coverage)
