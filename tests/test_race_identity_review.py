import json,unittest
from pathlib import Path
import election_lab as lab
from audit_refresh_2026 import validate_race_ids
from prepare_data import current_questions
from datetime import date
import pandas as pd


class RaceIdentityTests(unittest.TestCase):
    def test_registered_identity_does_not_accept_candidate_matchup(self):
        review=json.loads((lab.ROOT/'config/candidate_review_2026.json').read_text())
        review['contests']['LA']['candidates']=[]
        review['contests']['LA']['scalar_seat_mapping_ready']=False
        base=pd.read_parquet(lab.ROOT/'data/compact/current/feeds/senate.parquet')
        rows=base.iloc[:3].fillna('').to_dict('records')
        for r in rows:
            r.update(state='LA',race_id='08728cf9-27d9-4d84-8a37-2168f60a35cb',cycle='2026',office_type='U.S. Senate',stage='general',election_date='2026-11-03')
        validate_race_ids([],rows,review)
        questions,_=current_questions(rows,review,date(2026,9,24))
        self.assertTrue(all(not q['accepted_matchup'] for q in questions))
        self.assertTrue(all('pending_matchup_review' in q['reasons'] for q in questions))
        rows[0]['race_id']='unrecognized'
        with self.assertRaisesRegex(ValueError,'LA: unrecognized'):validate_race_ids([],rows,review)

    def test_registered_identity_requires_matching_election_metadata(self):
        review={'contests':{'LA':{'source_race_ids':['known']}}}
        row=dict(state='LA',race_id='known',cycle='2026',office_type='U.S. Senate',stage='primary',election_date='2026-11-03')
        with self.assertRaisesRegex(ValueError,'incompatible'):validate_race_ids([],[row],review)

    def test_reviewed_louisiana_poll_is_selected_and_enters_prepared_data(self):
        import shutil,tempfile
        from compact_data import poll_update
        from prepare_data import select_current
        review=json.loads((lab.ROOT/'config/candidate_review_2026.json').read_text())
        base=lab.ROOT/'data/compact/current'
        raw=pd.read_parquet(base/'feeds/senate.parquet')
        rows=raw[raw.state.eq('LA')].fillna('').to_dict('records')
        rows=[r for r in rows if r['poll_id']=='fd9a2472-db8c-46ca-87c5-5459d7092293']
        self.assertTrue(rows)
        qs,_=current_questions(rows,review,date(2026,9,24));select_current(qs,date(2026,9,24),14)
        self.assertEqual(len(qs),1)
        self.assertTrue(qs[0]['accepted_matchup'])
        self.assertEqual(qs[0]['selection'],'selected')
        self.assertEqual(qs[0]['dem_rep_margin'],-4)
        self.assertTrue(qs[0]['scalar_seat_mapping_ready'])
        with tempfile.TemporaryDirectory(dir=lab.ROOT/'cache') as tmp:
            out=Path(tmp)/'inputs';shutil.copytree(base,out)
            source=json.loads((out/'sources.json').read_text())['polls']
            poll_update(out,source,date(2026,9,24))
            polls=pd.read_parquet(out/'tables/polls.parquet')
            la=polls[polls.cycle.eq(2026)&polls.geography.eq('LA')]
            la=la[la.source_poll_id.eq('fd9a2472-db8c-46ca-87c5-5459d7092293')]
            self.assertEqual(len(la),1)
            self.assertTrue(la.iloc[0].scalar_seat_mapping_ready)
            self.assertEqual(la.iloc[0].selection_status,'selected')
