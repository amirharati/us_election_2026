# All-state polling audit

D/Independent is the forecast side, not a party label. Independent candidates remain IND. For questions with multiple D/IND candidates, the input is the strongest individual candidate minus the Republican, never their combined votes. This is a scalar proxy, not a joint candidate-level win model. Independent winners count on the D/Independent chamber side by modeling assumption, not a verified caucus commitment. Reviewed supplements and exact candidate aliases are applied automatically. Conditional/reduced-ballot versions are kept separately from the preferred ballot. Partial ballots and inferred date bounds remain explicitly flagged. All source questions are retained in the audit. Obsolete matchups, incompatible questions, duplicate sample versions and observations unavailable at the cutoff do not contribute.

Counts are question versions, not independent samples. Recency affects weighting; older eligible polls are retained.

| State   |   Questions |   Eligible |   Excluded | Independent candidates in eligible polls   |
|:--------|------------:|-----------:|-----------:|:-------------------------------------------|
| AK      |          28 |         14 |         14 | None                                       |
| AL      |           1 |          1 |          0 | None                                       |
| AR      |           4 |          4 |          0 | None                                       |
| CO      |           0 |          0 |          0 | None                                       |
| DE      |           0 |          0 |          0 | None                                       |
| FL      |          25 |          9 |         16 | None                                       |
| GA      |          50 |         16 |         34 | Allen Buckley                              |
| IA      |          33 |         20 |         13 | None                                       |
| ID      |          12 |          6 |          6 | Natalie Fleming, Todd Achilles             |
| IL      |           0 |          0 |          0 | None                                       |
| KS      |          15 |          6 |          9 | None                                       |
| KY      |           6 |          2 |          4 | None                                       |
| LA      |           2 |          2 |          0 | None                                       |
| MA      |          19 |         10 |          9 | None                                       |
| ME      |          61 |         12 |         49 | None                                       |
| MI      |          82 |         35 |         47 | None                                       |
| MN      |          16 |          8 |          8 | Marisa Simonetti                           |
| MS      |           5 |          2 |          3 | Ty Pinkins                                 |
| MT      |          28 |         10 |         18 | Seth Bodnar                                |
| NC      |          48 |         36 |         12 | None                                       |
| NE      |          10 |          7 |          3 | Dan Osborn                                 |
| NH      |          45 |         19 |         26 | Matt Giovonizzi, Tim Harris                |
| NJ      |           0 |          0 |          0 | None                                       |
| NM      |           1 |          1 |          0 | None                                       |
| OH      |          26 |         22 |          4 | Gregory Levy                               |
| OK      |           2 |          1 |          1 | Curtis Stinnett, Ron Meinhardt             |
| OR      |           0 |          0 |          0 | None                                       |
| RI      |           4 |          4 |          0 | Michael Bahry                              |
| SC      |          18 |          3 |         15 | None                                       |
| SD      |          11 |          7 |          4 | Brian Bengs                                |
| TN      |           2 |          1 |          1 | Generic Candidate                          |
| TX      |          90 |         39 |         51 | Camencia Ford, Hans Truelson, Joshua Cain  |
| VA      |           3 |          2 |          1 | Mark Moran                                 |
| WV      |           0 |          0 |          0 | None                                       |
| WY      |           0 |          0 |          0 | None                                       |

## Integrity checks

| Check                                                      | Passed   |
|:-----------------------------------------------------------|:---------|
| Every source question has a forecast disposition           | True     |
| All admitted questions have valid margins and sample sizes | True     |
| No rejected ballot/scenario enters the forecast            | True     |
| No admitted fieldwork or known release is after cutoff     | True     |

## Reviewed qualifications

| State   | pollster                       | poll_end   | quality_flags                                                                                    |
|:--------|:-------------------------------|:-----------|:-------------------------------------------------------------------------------------------------|
| LA      | Public Policy Polling          | 2026-07-22 | reviewed_candidate_alias                                                                         |
| ID      | The Bullfinch Group            | 2026-06-01 | D_IND_vs_REP|independent_candidate_present|partial_ballot_coverage                               |
| ID      | Change Research                | 2026-07-30 | D_IND_vs_REP|independent_candidate_present|reviewed_missing_sample_size|strongest_opponent_proxy |
| ID      | Public Policy Polling          | 2026-03-17 | D_IND_vs_REP|independent_candidate_present|partial_ballot_coverage                               |
| ID      | The Bullfinch Group            | 2026-08-07 | D_IND_vs_REP|independent_candidate_present|partial_ballot_coverage                               |
| ID      | Advanced Targeting Research    | 2026-09-16 | D_IND_vs_REP|independent_candidate_present|partial_ballot_coverage                               |
| VA      | The Public Sentiment Institute | 2026-06-16 | D_IND_vs_REP|independent_candidate_present|publication_date_upper_bound|strongest_opponent_proxy |

## Exclusion reasons

| State   | Reason                                                                                                                                                             |   Questions |
|:--------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------:|
| AK      | D_IND_vs_REP|independent_candidate_present|rcv_round_1|strongest_opponent_proxy|unreviewed_or_former_contender                                                     |           1 |
| AK      | before_two_year_cycle                                                                                                                                              |           1 |
| AK      | conditional_missing_ballot_contender|missing_reviewed_contender|unreviewed_or_former_contender                                                                     |           2 |
| AK      | rcv_round_1|strongest_opponent_proxy|unreviewed_or_former_contender                                                                                                |           1 |
| AK      | rcv_round_1|unreviewed_or_former_contender                                                                                                                         |           6 |
| AK      | rcv_round_2|unreviewed_or_former_contender                                                                                                                         |           1 |
| AK      | unreviewed_or_former_contender                                                                                                                                     |           2 |
| FL      | conditional_missing_ballot_contender|missing_reviewed_contender|unreviewed_or_former_contender                                                                     |          16 |
| GA      | alternative_population_or_basis                                                                                                                                    |           3 |
| GA      | conditional_missing_ballot_contender|missing_reviewed_contender|unreviewed_or_former_contender                                                                     |          30 |
| GA      | conditional_missing_ballot_contender|missing_reviewed_contender|unreviewed_or_former_contender|unsupported_population_or_subgroup                                  |           1 |
| IA      | alternative_population_or_basis                                                                                                                                    |           2 |
| IA      | conditional_missing_ballot_contender|missing_reviewed_contender|unreviewed_or_former_contender                                                                     |          11 |
| ID      | D_IND_vs_REP|alternative_reduced_ballot_same_sample|independent_candidate_present|partial_ballot_coverage                                                          |           2 |
| ID      | D_IND_vs_REP|independent_candidate_present|partial_ballot_coverage|strongest_opponent_proxy|unreviewed_or_former_contender                                         |           1 |
| ID      | D_IND_vs_REP|independent_candidate_present|reviewed_missing_sample_size|strongest_opponent_proxy|unreviewed_or_former_contender                                    |           1 |
| ID      | D_IND_vs_REP|independent_candidate_present|strongest_opponent_proxy|unreviewed_or_former_contender                                                                 |           1 |
| ID      | conditional_missing_ballot_contender|missing_reviewed_contender|unreviewed_or_former_contender                                                                     |           1 |
| KS      | D_IND_vs_REP|conditional_missing_ballot_contender|independent_candidate_present|missing_reviewed_contender                                                         |           2 |
| KS      | D_IND_vs_REP|conditional_missing_ballot_contender|independent_candidate_present|missing_reviewed_contender|strongest_opponent_proxy|unreviewed_or_former_contender |           1 |
| KS      | conditional_missing_ballot_contender|missing_reviewed_contender|unreviewed_or_former_contender                                                                     |           5 |
| KS      | invalid_sample_size|missing_or_invalid_sample_size                                                                                                                 |           1 |
| KY      | conditional_missing_ballot_contender|missing_reviewed_contender|unreviewed_or_former_contender                                                                     |           4 |
| MA      | conditional_missing_ballot_contender|missing_reviewed_contender|unreviewed_or_former_contender                                                                     |           9 |
| ME      | alternative_population_or_basis                                                                                                                                    |           2 |
| ME      | conditional_missing_ballot_contender|missing_reviewed_contender|unreviewed_or_former_contender                                                                     |          47 |
| MI      | alternative_population_or_basis                                                                                                                                    |           4 |
| MI      | alternative_reduced_ballot_same_sample                                                                                                                             |           1 |
| MI      | conditional_missing_ballot_contender|missing_reviewed_contender|unreviewed_or_former_contender                                                                     |          42 |
| MN      | alternative_population_or_basis                                                                                                                                    |           1 |
| MN      | conditional_missing_ballot_contender|missing_reviewed_contender|unreviewed_or_former_contender                                                                     |           7 |
| MS      | alternative_reduced_ballot_same_sample                                                                                                                             |           1 |
| MS      | conditional_missing_ballot_contender|missing_reviewed_contender                                                                                                    |           2 |
| MT      | D_IND_vs_REP|conditional_missing_ballot_contender|independent_candidate_present                                                                                    |           6 |
| MT      | D_IND_vs_REP|conditional_missing_ballot_contender|independent_candidate_present|missing_reviewed_contender|strongest_opponent_proxy|unreviewed_or_former_contender |           2 |
| MT      | D_IND_vs_REP|conditional_missing_ballot_contender|independent_candidate_present|missing_reviewed_contender|unreviewed_or_former_contender                          |           2 |
| MT      | D_IND_vs_REP|conditional_missing_ballot_contender|independent_candidate_present|strongest_opponent_proxy|unreviewed_or_former_contender                            |           1 |
| MT      | conditional_missing_ballot_contender                                                                                                                               |           4 |
| MT      | conditional_missing_ballot_contender|missing_reviewed_contender|unreviewed_or_former_contender                                                                     |           3 |
| NC      | alternative_population_or_basis                                                                                                                                    |           7 |
| NC      | conditional_missing_ballot_contender|missing_reviewed_contender|unreviewed_or_former_contender                                                                     |           5 |
| NE      | conditional_missing_ballot_contender|missing_reviewed_contender|unreviewed_or_former_contender                                                                     |           3 |
| NH      | D_IND_vs_REP|independent_candidate_present|strongest_opponent_proxy|unreviewed_or_former_contender                                                                 |           1 |
| NH      | conditional_missing_ballot_contender|missing_reviewed_contender|unreviewed_or_former_contender                                                                     |          25 |
| OH      | alternative_population_or_basis                                                                                                                                    |           1 |
| OH      | alternative_reduced_ballot_same_sample                                                                                                                             |           1 |
| OH      | conditional_missing_ballot_contender|missing_reviewed_contender|unreviewed_or_former_contender                                                                     |           2 |
| OK      | D_IND_vs_REP|conditional_missing_ballot_contender|independent_candidate_present|missing_reviewed_contender|strongest_opponent_proxy|unreviewed_or_former_contender |           1 |
| SC      | alternative_population_or_basis                                                                                                                                    |           2 |
| SC      | conditional_missing_ballot_contender|missing_reviewed_contender|unreviewed_or_former_contender                                                                     |          13 |
| SD      | D_IND_vs_REP|conditional_missing_ballot_contender|independent_candidate_present|missing_reviewed_contender|strongest_opponent_proxy|unreviewed_or_former_contender |           1 |
| SD      | D_IND_vs_REP|independent_candidate_present|strongest_opponent_proxy|unreviewed_or_former_contender                                                                 |           1 |
| SD      | conditional_missing_ballot_contender|missing_reviewed_contender|unreviewed_or_former_contender                                                                     |           2 |
| TN      | alternative_population_or_basis                                                                                                                                    |           1 |
| TX      | conditional_missing_ballot_contender|missing_reviewed_contender|unreviewed_or_former_contender                                                                     |          51 |
| VA      | conditional_missing_ballot_contender|missing_reviewed_contender|unreviewed_or_former_contender                                                                     |           1 |

## Supplemental source receipts

| state   | status           | publication_date   | source_url                                                                                       |
|:--------|:-----------------|:-------------------|:-------------------------------------------------------------------------------------------------|
| ID      | supplement_added | 2026-09-17         | https://www.advancedtargetingresearch.com/_files/ugd/03a624_0fca9a6dd7f846f7bc96f97429561064.pdf |
| VA      | supplement_added | 2026-05-05         | https://docs.google.com/spreadsheets/d/1BHuaXuhWj-xJdeJ4WoIOr778OubyduRuWa8aItCpANo/edit         |
| VA      | supplement_added | 2026-06-16         | https://docs.google.com/spreadsheets/d/1_WppnTBtVE63Er7OnXf-cy5gFceU3SZMvh6J_jr7xLc/edit         |
| SC      | supplement_added | 2026-09-01         | https://pbs.twimg.com/media/HRGJkaIWwAAUqgW.jpg                                                  |

[Every question, candidate affiliation and reason](poll_audit_details.parquet)
