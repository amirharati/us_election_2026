# Secret-scanning alert review

Reviewed on September 21, 2026: [GitHub alert 1](https://github.com/amirharati/us_election_2026/security/secret-scanning/1), identified as a HashiCorp Vault Service Token in commit `47cd3942185810126247df9e70b5e474282c0013`.

**Finding: a false positive in compressed binary data.** The alert remains open on GitHub; this investigation does not change its status.

The flagged file is `data/compact/current/feature_records.parquet`. The matched 26-byte sequence occurs once, at byte offset 6,217,786, inside the SNAPPY-compressed `logical_key` column in row group 0. Every decoded cell in the 70,856-row table was checked. None contains the sequence. Re-encoding the same logical table with ZSTD also removes the sequence.

The current working-tree file does not contain the sequence. An exact-byte scan of the existing Git-eligible working-tree files found no other occurrence. This is an investigation of this specific alert, not a general credential audit. The suspected value is intentionally omitted here.

No credential rotation or history rewrite is indicated for this binary match. GitHub can continue displaying the alert because the old commit still contains the compressed bytes. The appropriate alert resolution is **False positive**. Keep secret scanning enabled.
