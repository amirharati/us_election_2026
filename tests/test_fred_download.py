"""FRED transport bounds, actionable failures and readable source receipts."""
from pathlib import Path
from types import SimpleNamespace
import sys,unittest
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import election_lab
import feature_download as fd
from source_status import format_source_status

URL='https://fred.stlouisfed.org/graph/fredgraph.csv?id=CPIAUCSL'
class FredDownloadTests(unittest.TestCase):
    def test_validated_http1_transport_preserves_receipt(self):
        def downloaded(cmd,**kwargs):
            self.assertIn('--http1.1',cmd)
            self.assertNotIn('--insecure',cmd)
            Path(cmd[cmd.index('--output')+1]).write_bytes(b'observation_date,CPIAUCSL\n2026-08-01,300\n')
            Path(cmd[cmd.index('--dump-header')+1]).write_text('HTTP/1.1 200 OK\nContent-Type: application/csv\nLast-Modified: Mon, 21 Sep 2026 12:00:00 GMT\n')
            return SimpleNamespace(returncode=0,stdout=URL,stderr='')
        with patch('shutil.which',return_value='/usr/bin/curl'),patch('subprocess.run',side_effect=downloaded):
            raw,meta=fd.request_fred_csv(URL,timeout=5)
        self.assertTrue(raw.startswith(b'observation_date'))
        self.assertEqual(meta['transport'],'curl_http1.1')
        self.assertEqual(meta['content_type'],'application/csv')

    def test_failed_download_does_not_become_successful_receipt(self):
        with patch('shutil.which',return_value='/usr/bin/curl'),patch('subprocess.run',return_value=SimpleNamespace(returncode=28,stderr='Operation timed out',stdout='')):
            with self.assertRaisesRegex(RuntimeError,'curl 28.*timed out'):fd.request_fred_csv(URL)

    def test_without_curl_retains_python_transport(self):
        with patch('shutil.which',return_value=None),patch.object(fd,'request_bytes',return_value=(b'data',{})) as download:
            self.assertEqual(fd.request_fred_csv(URL),(b'data',{}))
            download.assert_called_once_with(URL,30)

    def test_receipt_formatting_distinguishes_failure_from_no_failure(self):
        result=format_source_status([dict(source='polls',acquisition_status='fresh_check_cache'),
            dict(source='fred',acquisition_status='stale_cache_after_failure',failure_type='RuntimeError',failure_detail='timeout')])
        self.assertFalse(result.isna().any().any())
        self.assertEqual(result.iloc[0].failure_type,'None')
        self.assertEqual(result.iloc[1].failure_detail,'timeout')

if __name__=='__main__':unittest.main()
