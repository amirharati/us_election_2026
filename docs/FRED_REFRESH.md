# FRED refresh investigation — September 21, 2026

The old Python CSV request timed out while reading FRED's CPI export. A browser
user-agent did not resolve it. A curl HTTP/2 download also failed with a stream
error. The same public CSV downloaded successfully with curl over HTTP/1.1 using
curl's default headers. This identifies a reproducible client/endpoint transport
problem; the tests do not establish the internal cause at FRED's servers.

The downloader now uses curl HTTP/1.1 for public FRED graph CSV exports when curl
is installed. TLS verification remains enabled, redirects are restricted to
HTTPS, and time/size limits and CSV validation remain in place. Systems without
curl retain the Python transport. Other providers and the authenticated vintage
API are unchanged. Future refresh failures preserve the detailed error as well
as its class. Failed acquisition continues to use verified saved inputs.

All seven configured series downloaded successfully. Comparing these downloads
with the saved compact inputs produced identical economic context, model feature
scores and active feature vectors at the September 21 cutoff. Thus the earlier
FRED failure did not change this forecast's model inputs. A future failed refresh
could matter if it missed new observations or revisions.

The cached model series covered August CPI/gasoline/unemployment, July real
income, and second-quarter GDP. Observation periods differ from download dates;
a successful daily check does not mean monthly or quarterly data changed.

The freshness table now shows `None` for missing optional fields and leaves an
absent error detail blank. It no longer displays `NaN` as if a successful source
had missing economic data. Failed sources still show their actual error.

For a fresh forecast, run notebook 04 (Run All) or `python run.py live`. These
refresh evidence, update inference and generate reports using the saved model
specifications and historical fits. Conditional Student sampling may run again;
that is not historical retraining or model promotion. Other experiment notebooks
are only needed when you want to refresh their comparison outputs.

Validation: 44 tests passed, including transport failure handling and source-status
formatting. Input comparison is recorded in
[fred_investigation.json](../outputs/validation/fred_investigation.json).

FRED provides public CSV exports through its
[download options](https://fredhelp.stlouisfed.org/fred/data/downloading/using-the-download-data-link/).

The full live notebook subsequently passed all 10 code cells. FRED now reports
`checked_online`. All state margins, win probabilities and 95% interval endpoints
match the pre-fix saved forecast exactly across all models. Active model assets
were checked against their original hashes and remain unchanged.
