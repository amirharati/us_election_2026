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
