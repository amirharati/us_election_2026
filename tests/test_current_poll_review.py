import copy,json,shutil,tempfile,unittest
from pathlib import Path
from datetime import date
import pandas as pd
import election_lab as lab
from current_poll_review import reviewed_feed
from prepare_data import current_questions
from normalize_data import current_senate
from audit_refresh_2026 import csv_form
from compact_data import poll_update,seal

class CurrentPollReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.review=json.loads((lab.ROOT/'config/candidate_review_2026.json').read_text())
        cls.supp=json.loads((lab.ROOT/'config/supplemental_polls_2026.json').read_text())
        cls.raw=pd.read_parquet(lab.ROOT/'data/compact/current/feeds/senate.parquet').fillna('').to_dict('records')
        cls.rows,cls.receipts=reviewed_feed(cls.raw,cls.supp,date(2026,9,25))
        cls.qs,cls.answers=current_questions(cls.rows,cls.review,date(2026,9,25))

    def test_alias_preserves_source_identity_without_aliasing_replacements(self):
        q=next(q for q in self.qs if q['state']=='LA' and q['pollster']=='Public Policy Polling')
        self.assertTrue(q['accepted_matchup']);self.assertEqual(q['dem_rep_margin'],-4)
        a=next(a for a in self.answers if a['question_key']==q['question_key'] and a['candidate_name']=='James Davis')
        self.assertNotEqual(a['candidate_id'],a['canonical_candidate_id'])
        self.assertEqual(a['canonical_candidate_name'],'Jamie Davis')
        old=[q for q in self.qs if q['state']=='MT' and q['end_date']<'2026-03-01']
        self.assertTrue(old);self.assertTrue(all(not q['accepted_matchup'] for q in old))

    def test_montana_requires_both_current_opponents(self):
        accepted=[q for q in self.qs if q['state']=='MT' and q['accepted_matchup']]
        self.assertEqual(len(accepted),10)
        for q in accepted:
            parties={a['reviewed_party'] for a in self.answers if a['question_key']==q['question_key']}
            self.assertTrue({'DEM','IND','REP'}<=parties)
        self.assertTrue(any(q['state']=='MT' and 'conditional_missing_ballot_contender' in q['reasons'] for q in self.qs))

    def test_supplement_fuller_ballot_and_raw_sample_repair(self):
        atr=[q for q in self.qs if q['poll_id']=='reviewed:ID:ATR:2026-09']
        self.assertEqual(sum(q['accepted_matchup'] for q in atr),1)
        used=next(q for q in atr if q['accepted_matchup'])
        self.assertAlmostEqual(used['dem_rep_margin'],6.1)
        self.assertIn('partial_ballot_coverage',used['review_flags'])
        change=[q for q in self.qs if q['poll_id']=='909a333a-6acb-47ed-9a65-5b475b941da2']
        self.assertTrue(all(q['sample_size']==1213 for q in change))
        self.assertTrue(all(r['sample_size']=='' for r in self.raw if r['poll_id']==change[0]['poll_id']))

    def test_upstream_arrival_does_not_double_count_supplement(self):
        copied=[dict(r,poll_id='new-upstream-id',source='') for r in self.rows if r['poll_id']=='reviewed:ID:ATR:2026-09']
        merged,receipts=reviewed_feed(self.raw+copied,self.supp,date(2026,9,25))
        self.assertFalse(any(r['poll_id']=='reviewed:ID:ATR:2026-09' for r in merged))
        self.assertTrue(any(r['poll_id']=='reviewed:ID:ATR:2026-09' and r['status']=='upstream_sample_present' for r in receipts))

    def test_changed_source_invalidates_question_review(self):
        rows=copy.deepcopy(self.rows)
        row=next(r for r in rows if r['question_id']=='86bd6638-1c0f-4a24-b124-9304d97e6bd9')
        row['pct']=str(float(row['pct'])+1)
        with self.assertRaisesRegex(ValueError,'Source revised reviewed question'):
            current_questions(rows,self.review,date(2026,9,25))

    def test_full_pipeline_counts_availability_overlap_and_immutable_upstream(self):
        base=lab.ROOT/'data/compact/current'
        with tempfile.TemporaryDirectory(dir=lab.ROOT/'cache') as temp:
            out=Path(temp)/'inputs';shutil.copytree(base,out)
            before=(out/'feeds/senate.parquet').read_bytes()
            poll_update(out,json.loads((out/'sources.json').read_text())['polls'],date(2026,9,25));seal(out)
            pd.testing.assert_frame_equal(pd.read_parquet(base/'feeds/senate.parquet'),pd.read_parquet(out/'feeds/senate.parquet'))
            e=lab.prepare_live_evidence(out);q=e['q'].set_index('geography')
            for state,count in [('ID',6),('MT',10),('LA',2),('VA',2),('SC',3)]:self.assertEqual(q.loc[state,'sample_count'],count,state)
            p=pd.read_parquet(out/'tables/polls.parquet')
            dates=pd.read_parquet(out/'tables/poll_availability.parquet').set_index('observation_id')
            atr=p[p.source_poll_id.eq('reviewed:ID:ATR:2026-09')]
            self.assertTrue(all(dates.loc[o,'documented_release_date']=='2026-09-17' for o in atr.observation_id))
            early=lab.prepare_live_evidence(out,'2026-09-16')['poll_audit'].set_index('observation_id')
            self.assertFalse(any(early.loc[o,'baseline_status']=='eligible' for o in atr.observation_id))
            self.assertTrue((out/'review/receipts.json').exists())
