import unittest,json
from datetime import date
import pandas as pd
import election_lab as lab
from prepare_data import current_questions,forecast_side_shares
from normalize_data import current_senate
from audit_refresh_2026 import csv_form

class IndependentMappingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.review=json.loads((lab.ROOT/'config/candidate_review_2026.json').read_text())
        cls.raw=pd.read_parquet(lab.ROOT/'data/compact/current/feeds/senate.parquet').fillna('')

    def questions(self,state):
        return current_questions(self.raw[self.raw.state.eq(state)].to_dict('records'),self.review,date(2026,9,25))

    def test_independent_head_to_head_is_usable_and_keeps_affiliation(self):
        for state in ['NE','SD']:
            qs,ans=self.questions(state)
            obs,answers=current_senate(csv_form(qs),csv_form(ans))
            admitted=[o for o in obs if o['matchup_status']=='accepted']
            self.assertTrue(admitted)
            self.assertTrue(all(o['dem_rep_margin'] is not None for o in admitted))
            self.assertTrue(any(a['party']=='IND' for a in answers))
        ne=[o for o in self._observations('NE') if o['pollster']=='SurveyUSA' and o['poll_end']=='2026-09-13']
        self.assertTrue(ne); self.assertAlmostEqual(ne[0]['dem_rep_margin'],.04)

    def _observations(self,state):
        qs,ans=self.questions(state)
        return current_senate(csv_form(qs),csv_form(ans))[0]

    def test_third_independent_does_not_exclude_valid_general_question(self):
        for state in ['MN','MS','OK','RI','TN','ID','MT']:
            admitted=[o for o in self._observations(state) if o['matchup_status']=='accepted']
            self.assertTrue(admitted,state)
            self.assertTrue(any('independent_candidate_present' in o['quality_flags'] for o in admitted),state)

    def test_multiple_candidates_are_never_added(self):
        d,r=forecast_side_shares([{'reviewed_party':p,'pct':v} for p,v in [('DEM',20),('IND',35),('REP',40)]])
        self.assertEqual(d-r,-5)

    def test_old_candidate_and_future_release_remain_excluded(self):
        qs,_=self.questions('NE')
        self.assertTrue(any('unreviewed_or_former_contender' in q['reasons'] and not q['accepted_matchup'] for q in qs))
        qs,_=current_questions(self.raw[self.raw.state.eq('NE')].to_dict('records'),self.review,date(2026,1,1))
        self.assertTrue(all(not q['accepted_matchup'] for q in qs if q['created_date']>'2026-01-01'))
