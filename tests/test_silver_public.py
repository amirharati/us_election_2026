from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import election_lab
import live_published_comparison as pub
from silver_public import public_topline,fetch_silver,LANDING,FEED


def article(paragraph):
    return ('<div class="available-content"><h5>Updated September 21, 2026</h5><p>'+paragraph+'</p></div>').encode()


class SilverPublicTests(unittest.TestCase):
    def test_deluxe_not_range_threshold_or_market(self):
        raw=article('Democrats Senate chances are between 62 percent and 68 percent, including 64 percent in our headline “Deluxe” version. A toss-up threshold is 60 percent; markets say 61 percent.')
        s=public_topline(raw,LANDING)
        self.assertEqual(s['D_control_pct'],64)
        self.assertEqual(s['published_date'],'2026-09-21')
        self.assertEqual(s['rows'],[])
        self.assertIsNone(s['expected_D'])
        pub.validate(s)

    def test_unsupported_or_hidden_text_is_not_used(self):
        for raw in [article('Markets give Democrats 70 percent for the Senate; Deluxe is our model.'),
                    b'<script>Democrats Senate including 64 percent in our headline Deluxe</script>',
                    b'<div class="available-content"><div class="paywall"><p>Democrats Senate including 64 percent in our headline Deluxe</p></div></div>']:
            self.assertIsNone(public_topline(raw,LANDING))

    def test_conflicting_probabilities_are_not_guessed(self):
        self.assertIsNone(public_topline(article('Democrats Senate: including 64 percent in our headline Deluxe, including 66 percent in our headline Deluxe.'),LANDING))

    def test_public_feed_discovers_article_and_keeps_its_date(self):
        url='https://www.natesilver.net/p/new-model-commentary'
        feed=f'<rss><channel><item><link>{url}</link><description>Senate Deluxe forecast</description><pubDate>Sun, 20 Sep 2026 19:08:19 GMT</pubDate></item></channel></rss>'.encode()
        pages={LANDING:article('Updated charts require a subscription.'),FEED:feed,
               url:article('Democrats Senate including 64 percent in our headline Deluxe version.')}
        result=fetch_silver(lambda url,timeout:pages[url],10)
        self.assertEqual(result['published_date'],'2026-09-20')
        self.assertEqual(result['source_url'],url)
        self.assertIn(url,result['discovery_sha256'])

    def test_topline_only_cannot_hide_incomplete_state_feed(self):
        s=dict(published_date='2026-09-20',rows=[],D_control_pct=64.,expected_D=None)
        with self.assertRaises(ValueError):pub.validate(s)

    def test_each_publisher_has_separate_chamber_differences(self):
        import pandas as pd
        p=pd.DataFrame(columns=['model','geography'])
        s=pd.DataFrame([dict(model='Bayesian',p_D_control=.45,expected_D=50.)])
        snapshots={k:dict(published_date='2026-09-20',rows=[],D_control_pct=v,expected_D=None) for k,v in [('silver',64.),('rttwh',68.)]}
        result=pub.compare(p,s,snapshots,'2026-09-21',set(),('Bayesian',),15,.75)
        gaps=result['chamber_gaps'].set_index('Publisher')['Gap (pp)']
        self.assertEqual(gaps['Silver Bulletin Deluxe'],-19.)
        self.assertEqual(gaps['Race to the WH'],-23.)
        self.assertEqual(result['overall']['D control %'].tolist(),[45.,64.,68.])
