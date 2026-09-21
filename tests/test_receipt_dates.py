"""The refresh cutoff is a local calendar date; receipts record UTC instants."""
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
import sys
import json
import unittest
from unittest.mock import patch

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import election_lab
import final_pipeline


class ReceiptDateTests(unittest.TestCase):
    def test_package_manifest_does_not_freeze_runtime_outputs(self):
        manifest=json.loads((election_lab.ROOT/'PACKAGE_MANIFEST.json').read_text())
        self.assertFalse(any(k.endswith('last_check.json') or
                             k.startswith('data/final_work/') or
                             k.startswith('notebooks/') and k.endswith('.ipynb')
                             for k in manifest))
        self.assertIn('NOTEBOOK_SOURCES.json',manifest)

    def test_utc_next_day_is_still_today_in_toronto(self):
        receipt=dict(finished_at='2026-09-21T01:31:07.324294+00:00',
                     finished_at_local='2026-09-20T21:31:07.324294-04:00')
        final_pipeline.validate_receipt_cutoff(receipt,date(2026,9,20))

    def test_genuinely_later_local_day_is_rejected(self):
        receipt=dict(finished_at='2026-09-21T05:31:07+00:00',
                     finished_at_local='2026-09-21T01:31:07-04:00')
        with self.assertRaisesRegex(ValueError,'exceeds requested'):
            final_pipeline.validate_receipt_cutoff(receipt,date(2026,9,20))

    def test_local_timestamp_cannot_be_changed_to_bypass_cutoff(self):
        receipt=dict(finished_at='2026-09-21T05:31:07+00:00',
                     finished_at_local='2026-09-20T01:31:07-04:00')
        with self.assertRaisesRegex(ValueError,'timestamps disagree'):
            final_pipeline.validate_receipt_cutoff(receipt,date(2026,9,20))

    def test_legacy_receipt_uses_local_zone(self):
        # Reproduce the original receipt, which had no local timestamp field.
        class TorontoDateTime(datetime):
            def astimezone(self,tz=None):
                return super().astimezone(tz or timezone(timedelta(hours=-4)))
        with patch.object(final_pipeline,'datetime',TorontoDateTime):
            final_pipeline.validate_receipt_cutoff(
                {'finished_at':'2026-09-21T01:31:07.324294+00:00'},date(2026,9,20))

    def test_positive_offset_receipt_uses_its_recorded_calendar(self):
        receipt=dict(finished_at='2026-09-20T23:30:00+00:00',
                     finished_at_local='2026-09-21T08:30:00+09:00')
        final_pipeline.validate_receipt_cutoff(receipt,date(2026,9,21))
        with self.assertRaisesRegex(ValueError,'exceeds requested'):
            final_pipeline.validate_receipt_cutoff(receipt,date(2026,9,20))


if __name__=='__main__':unittest.main()
