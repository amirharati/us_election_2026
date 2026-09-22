from pathlib import Path
import sys,tempfile,unittest
import pandas as pd
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import election_lab
from live_share_images import uncertainty_images
from output_publication import publish


class ShareImageTests(unittest.TestCase):
    def test_uncertainty_chart_preserves_intervals_and_input(self):
        import matplotlib.pyplot as plt
        from matplotlib.table import Table
        frame=pd.DataFrame(dict(contest=['AA','BB'],recent_samples=[4,5],recent_firms=[2,3],
            prediction_pp=[2,-3],lo95_pp=[-8,-9],hi95_pp=[12,3],width95_pp=[20,12]))
        before=frame.copy(deep=True)
        with patch('live_share_images.finish',side_effect=lambda fig,*args:fig):
            fig=uncertainty_images(frame,'.','2026-09-21')[0]
        ax=fig.axes[0]
        self.assertFalse(fig.findobj(Table))
        self.assertEqual(ax.collections[0].get_segments()[0].tolist(),[[-8.,0.],[12.,0.]])
        self.assertEqual(ax.collections[1].get_offsets()[:,0].tolist(),[2.,-3.])
        pd.testing.assert_frame_equal(frame,before)
        plt.close(fig)

    def test_pngs_publish_and_freeze_with_daily_report(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);run=root/'cache/runs/live_reports/20260921T120000.000000Z';run.mkdir(parents=True)
            (run/'run.json').write_text('{}');(run/'report.html').write_text('<html>same tables</html>')
            (run/'report.md').write_text('![Shared image](share_test.png)')
            (run/'share_test.png').write_bytes(b'png')
            publish(root,run)
            self.assertEqual((root/'outputs/reports/forecast/share_test.png').read_bytes(),b'png')
            self.assertEqual((root/'outputs/reports/history/2026-09-21/live_reports/share_test.png').read_bytes(),b'png')
