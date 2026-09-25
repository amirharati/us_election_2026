"""Latest-only publication, clone fallback, and complete report links."""
from pathlib import Path
import json
import sys
import tempfile
import unittest
from unittest.mock import patch
import pandas as pd
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import election_lab as lab
from output_publication import result_path


class PublicationTests(unittest.TestCase):
    def test_latest_replaces_old_files_and_is_usable_without_cache(self):
        with tempfile.TemporaryDirectory() as temp,patch.object(lab,'ROOT',Path(temp)):
            a=lab.new_run('training');(a/'old.txt').write_text('old');lab.finish(a,dict(cycle=2026))
            b=lab.new_run('training');(b/'fit.npz').write_bytes(b'latest-fit');lab.finish(b,dict(cycle=2026))
            public=result_path(lab.ROOT,'training')
            self.assertFalse((public/'old.txt').exists())
            self.assertEqual((public/'fit.npz').read_bytes(),b'latest-fit')
            import shutil
            shutil.rmtree(lab.ROOT/'cache')
            self.assertEqual(lab.latest_run('training'),public)
            self.assertTrue((lab.ROOT/'outputs/reports/training/training.md').exists())

    def test_dated_reports_preserve_other_days_and_freeze_links(self):
        with tempfile.TemporaryDirectory() as temp,patch.object(lab,'ROOT',Path(temp)):
            from output_publication import publish
            for stamp,value in [('20260920T100000.000000Z',1),('20260921T100000.000000Z',2),('20260921T110000.000000Z',3)]:
                run=lab.ROOT/'cache/runs/live_reports'/stamp;run.mkdir(parents=True)
                (run/'report.md').write_text(f'# Value {value}\n![Chart](control_history.png)\n[Settings](forecast_metadata.json)')
                (run/'control_history.png').write_bytes(bytes([value]))
                (run/'forecast_metadata.json').write_text(json.dumps({'value':value}))
                (run/'run.json').write_text(json.dumps({'as_of':'2026-09-01'}))
                publish(lab.ROOT,run)
            base=lab.ROOT/'outputs/reports/history'
            for date,value in [('2026-09-20',1),('2026-09-21',3)]:
                saved=base/date/'live_reports'
                self.assertIn(f'# Value {value}',(saved/f'forecast-{date}.md').read_text())
                self.assertEqual((saved/'control_history.png').read_bytes(),bytes([value]))
                self.assertEqual(json.loads((saved/'forecast_metadata.json').read_text())['value'],value)
            self.assertEqual(len(list(base.glob('*/live_reports/forecast-*.md'))),2)
            index=(base/'README.md').read_text()
            self.assertIn('2026-09-20/live_reports/forecast-2026-09-20.md',index)
            self.assertIn('2026-09-21/live_reports/forecast-2026-09-21.md',index)

    def test_notebook_portfolio_reviews_do_not_overwrite_each_other(self):
        with tempfile.TemporaryDirectory() as temp,patch.object(lab,'ROOT',Path(temp)):
            from model_portfolio import publish_review
            source=lab.new_run('portfolio')
            frame=pd.DataFrame({'model':['Bayesian','Older Gaussian','Four-model mixture'], 'cycle':[2026]*3})
            for name in ['predictions','seats','summary','cycle_scores','diagnostics','checks']:
                frame.to_parquet(source/(name+'.parquet'),index=False)
            lab.finish(source,{},publish=False)
            original=lab.sha(source/'manifest.json')
            a=publish_review(source,'older_alternatives',['Bayesian','Older Gaussian'])
            before=(result_path(lab.ROOT,'older_alternatives')/'manifest.json').read_bytes()
            publish_review(source,'all_model_mixture')
            self.assertEqual(before,(result_path(lab.ROOT,'older_alternatives')/'manifest.json').read_bytes())
            self.assertEqual(lab.sha(source/'manifest.json'),original)
            self.assertEqual(set(pd.read_parquet(a/'predictions.parquet').model),{'Bayesian','Older Gaussian'})
            self.assertEqual(len(list((lab.ROOT/'outputs/reports/history').glob('*/*/report.md'))),2)

    def test_publication_strips_only_samples_and_preserves_local_run(self):
        import numpy as np
        from output_publication import replace_directory
        with tempfile.TemporaryDirectory() as temp,patch.object(lab,'ROOT',Path(temp)):
            run=lab.new_run('live')
            np.savez_compressed(run/'main_joint.npz',samples=np.ones((4,2)),mean=np.array([1.,2.]),covariance=np.eye(2),seat_count_frequency=np.array([.2,.8]))
            lab.finish(run,{'kind':'live'},publish=False);original=lab.sha(run/'manifest.json')
            lab.publish_run(run);public=result_path(lab.ROOT,'live');lab.verify_run(public)
            with np.load(public/'main_joint.npz') as a:
                self.assertNotIn('samples',a.files);np.testing.assert_array_equal(a['mean'],[1.,2.])
                np.testing.assert_array_equal(a['seat_count_frequency'],[.2,.8])
            with np.load(run/'main_joint.npz') as a:self.assertIn('samples',a.files)
            self.assertEqual(lab.sha(run/'manifest.json'),original)

    def test_html_uses_existing_png_and_reseals_copy(self):
        import base64
        from output_publication import replace_directory
        with tempfile.TemporaryDirectory() as temp,patch.object(lab,'ROOT',Path(temp)):
            run=lab.new_run('live_reports');raw=b'png-example'
            (run/'chart.png').write_bytes(raw)
            (run/'report.html').write_text('<img src="data:image/png;base64,'+base64.b64encode(raw).decode()+'">')
            lab.finish(run,{},publish=False);original=lab.sha(run/'manifest.json')
            target=Path(temp)/'published';replace_directory(run,target);lab.verify_run(target)
            self.assertEqual((target/'report.html').read_text(),'<img src="chart.png">')
            self.assertEqual(len(list(target.glob('*.png'))),1)
            self.assertEqual(lab.sha(run/'manifest.json'),original)

    def test_internal_runs_are_never_published(self):
        with tempfile.TemporaryDirectory() as temp,patch.object(lab,'ROOT',Path(temp)):
            run=lab.new_run('cutoff_forecasts');lab.finish(run,dict(as_of='2026-09-21'))
            self.assertFalse((lab.ROOT/'outputs').exists())

    def test_deferred_live_run_is_not_published_before_commit(self):
        with tempfile.TemporaryDirectory() as temp,patch.object(lab,'ROOT',Path(temp)):
            run=lab.new_run('live');lab.finish(run,dict(as_of='2026-09-21'),publish=False)
            self.assertFalse(result_path(lab.ROOT,'live').exists())
            lab.publish_run(run)
            self.assertTrue(result_path(lab.ROOT,'live').exists())

if __name__=='__main__':unittest.main()
