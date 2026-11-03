# Historical Senate archive coverage

Generated 2026-09-26T03:38:52.914458+00:00. Source: [Envio on-chain archive](https://huggingface.co/datasets/moose-code/polymarket-onchain-v1), snapshot `7eeb860dea5b79d5c74f3182b70bd08c85c8f833`. CC-BY-4.0; attribution: Envio.

|   cycle | category          |   markets |   with_events |   observations |   pre_election |
|--------:|:------------------|----------:|--------------:|---------------:|---------------:|
|    2022 | control           |         1 |             1 |           5105 |           3734 |
|    2022 | margin            |         2 |             2 |           1754 |              0 |
|    2022 | primary           |        17 |            17 |           9323 |           9309 |
|    2022 | runoff_occurrence |         1 |             1 |            324 |            178 |
|    2022 | winner            |        15 |            15 |           9785 |           4838 |
|    2024 | control           |         1 |             1 |           8439 |           7011 |
|    2024 | margin            |         8 |             8 |          27631 |            686 |
|    2024 | primary           |        51 |            50 |           7518 |           7518 |
|    2024 | seats             |         8 |             8 |          25170 |          13708 |
|    2024 | winner            |       102 |           102 |         265802 |         194016 |

Full Senate-only event rows are saved in `cache/polymarket_history/senate_archive/selected/`. Compact daily observations and coverage are saved in `outputs/results/research/senate_archive/`. Raw original fields, both outcomes, fees, block/log identities and available post-election events are retained. Post-election events are not eligible for pre-election prediction tests.

## Interpretation and limits

- Third-party blockchain index; not guaranteed exhaustive for deleted or misdated markets.
- Archive state rows are retrospective; never use them as dated forecast features.
- Average executed prices are not historical bid/ask quotes or marginal pool probabilities.
- Raw exchange fills can contain matching-engine counterpart events; do not sum their volume as independent trades.
- Daily files keep the last observed event and its actual timestamp; missing days stay missing.
- Zero-amount and token/token events remain in the raw extract; normalization_audit explains why they have no derived price.
- Primary and runoff contracts require separate forecast mappings. No new backtest or strategy claim.

FPMM prices remove fees from buy payments and add fees back to sell receipts, then divide by outcome shares. This is the average price for that transaction. Separate fields preserve actual cash-per-share and fee-per-share. CLOB prices divide the collateral amount by the outcome-token amount; raw fee fields are retained.

Legacy event-count audit: 42 of 42 pool totals match the source snapshot.

Liquidity-event audit: additions and removals both match for 42 of 42 pools.

## 2022: every market

|   market_id | question                                                                                                       |   observations |   pre_general_election | status    |
|------------:|:---------------------------------------------------------------------------------------------------------------|---------------:|-----------------------:|:----------|
|      244021 | Will Matt Dolan win 2nd place in the Republican primary for the 2022 United States Senate election in Ohio?    |            364 |                    362 | available |
|      241064 | Will J. D. Vance win the Republican nomination for the 2022 United States Senate election in Ohio?             |            702 |                    702 | available |
|      241065 | Will Josh Mandel win the Republican nomination for the 2022 United States Senate election in Ohio?             |            340 |                    340 | available |
|      241066 | Will Jane Timken win the Republican nomination for the 2022 United States Senate election in Ohio?             |            136 |                    136 | available |
|      241067 | Will Mike Gibbons win the Republican nomination for the 2022 United States Senate election in Ohio?            |            256 |                    256 | available |
|      243805 | Will Matt Dolan win the Republican nomination for the 2022 United States Senate election in Ohio?              |            238 |                    238 | available |
|      241032 | Will John Fetterman win the Democratic nomination for the 2022 United States Senate election in Pennsylvania?  |            428 |                    428 | available |
|      241033 | Will Conor Lamb win the Democratic nomination for the 2022 United States Senate election in Pennsylvania?      |            406 |                    406 | available |
|      241048 | Will David McCormick win the Republican nomination for the 2022 United States Senate election in Pennsylvania? |            940 |                    938 | available |
|      241049 | Will Mehmet Oz win the Republican nomination for the 2022 United States Senate election in Pennsylvania?       |           1670 |                   1668 | available |
|      241050 | Will Jeff Bartos win the Republican nomination for the 2022 United States Senate election in Pennsylvania?     |             96 |                     96 | available |
|      243678 | Will Kathy Barnette win the Republican nomination for the 2022 United States Senate election in Pennsylvania?  |            495 |                    495 | available |
|      242424 | Will Katie Britt win the 2022 Alabama Republican Senate nomination?                                            |            625 |                    623 | available |
|      242823 | Will Blake Masters win the 2022 Arizona Republican Senate nomination?                                          |           1443 |                   1441 | available |
|      240615 | Which party will control the U.S. Senate after the 2022 election?                                              |           5105 |                   3734 | available |
|      240593 | Senate: Will a Democrat (Hassan) or Republican (Bolduc) win in New Hampshire?                                  |            539 |                    337 | available |
|      240594 | Senate: Will a Democrat (Welch) or Republican (Malloy) win in Vermont?                                         |            138 |                    123 | available |
|      240595 | Senate:  Will a Democrat (Kelly) or Republican (Masters) win in Arizona?                                       |           1504 |                    840 | available |
|      240596 | Senate: Will a Democrat (Warnock) or Republican (Walker) win in Georgia?                                       |           1918 |                    558 | available |
|      240597 | Senate: Will a Democrat (Franken) or Republican (Grassley) win in Iowa?                                        |            228 |                    211 | available |
|      240599 | Senate: Will a Democrat (Fetterman) or Republican (Oz) win in Pennsylvania?                                    |           1310 |                    839 | available |
|      240600 | Senate: Will a Democrat (Masto) or Republican (Laxalt) win in Nevada?                                          |           1837 |                    375 | available |
|      240601 | Senate: Will a Democrat (Barnes) or Republican (Johnson) win in Wisconsin?                                     |            469 |                    312 | available |
|      240602 | Senate: Will a Democrat (Bennet) or Republican (O'Dea) win in Colorado?                                        |            521 |                    435 | available |
|      244331 | Senate: Will a Democrat (Ryan) or Republican (Vance) win in Ohio?                                              |            469 |                    344 | available |
|      247017 | Senate: Will a Democrat (Beasley) or Republican (Budd) win in North Carolina?                                  |            239 |                    128 | available |
|      247018 | Senate: Will a Democrat (Demings) or Republican (Rubio) win in Florida?                                        |            104 |                     62 | available |
|      247676 | Senate: Will an Independent (McMullin) or Republican (Lee) win in Utah?                                        |            176 |                    131 | available |
|      247791 | Senate: Will a Democrat (Murray) or Republican (Smiley) win in Washington?                                     |             93 |                     36 | available |
|      247671 | Will there be a run-off in the 2022 Georgia Senate election?                                                   |            324 |                    178 | available |
|      247721 | Will Lisa Murkowski win the 2022 Alaska Senate election?                                                       |            240 |                    107 | available |
|      247836 | Will the Margin of Victory in the Georgia runoff be 2.5% or greater?                                           |           1136 |                      0 | available |
|      248012 | Will the Margin of Victory in the Georgia runoff be 5.0% or greater?                                           |            618 |                      0 | available |
|      244921 | Will Eric Greitens win the 2022 Missouri Republican Senate nomination?                                         |            551 |                    549 | available |
|      244922 | Will Vicky Hartzler win the 2022 Missouri Republican Senate nomination?                                        |            269 |                    269 | available |
|      244923 | Will Eric Schmitt win the 2022 Missouri Republican Senate nomination?                                          |            364 |                    362 | available |

## 2024: every market

|   market_id | question                                                                    |   observations |   pre_general_election | status                         |
|------------:|:----------------------------------------------------------------------------|---------------:|-----------------------:|:-------------------------------|
|      252332 | Will Adam Schiff advance from the 2024 CA Senate Primary?                   |            375 |                    375 | available                      |
|      252331 | Will Katie Porter advance from the 2024 CA Senate Primary?                  |            112 |                    112 | available                      |
|      252338 | Will Barbara Lee advance from the 2024 CA Senate Primary?                   |             14 |                     14 | available                      |
|      252484 | Will Laphonza Butler advance from the 2024 CA Senate Primary?               |             10 |                     10 | available                      |
|      254170 | Will Steve Garvey advance from the 2024 CA Senate Primary?                  |            139 |                    139 | available                      |
|      255211 | Will Colin Allred win the Texas Democratic Senate Primary?                  |             44 |                     44 | available                      |
|      255212 | Will Meri Gomez win the Texas Democratic Senate Primary?                    |              5 |                      5 | available                      |
|      255213 | Will Mark Gonzalez win the Texas Democratic Senate Primary?                 |              9 |                      9 | available                      |
|      255214 | Will Roland Gutierrez win the Texas Democratic Senate Primary?              |             43 |                     43 | available                      |
|      255215 | Will Robert Hassan win the Texas Democratic Senate Primary?                 |              9 |                      9 | available                      |
|      255216 | Will Steven Keough win the Texas Democratic Senate Primary?                 |              8 |                      8 | available                      |
|      255217 | Will Carl Sherman win the Texas Democratic Senate Primary?                  |              9 |                      9 | available                      |
|      255219 | Will Thierry Tchenko win the Texas Democratic Senate Primary?               |              3 |                      3 | available                      |
|      255218 | Will Heli Rodriguez-Prilliman win the Texas Democratic Senate Primary?      |              4 |                      4 | available                      |
|      255220 | Will another candidate win the Texas Democratic Senate Primary?             |              7 |                      7 | available                      |
|      255221 | Will Adam Schiff get first place in the California Senate Primary?          |           2065 |                   2065 | available                      |
|      255222 | Will Steve Garvey get first place in the California Senate Primary?         |           1240 |                   1240 | available                      |
|      255223 | Will Katie Porter get first place in the California Senate Primary?         |             90 |                     90 | available                      |
|      255224 | Will another candidate get first place in the California Senate Primary?    |             44 |                     44 | available                      |
|      255245 | Will Matt Dolan win the Ohio Republican Senate Primary?                     |            238 |                    238 | available                      |
|      255246 | Will Frank LaRose win the Ohio Republican Senate Primary?                   |            138 |                    138 | available                      |
|      255247 | Will Bernie Moreno win the Ohio Republican Senate Primary?                  |            233 |                    233 | available                      |
|      255264 | Will another candidate win the Ohio Republican Senate Primary?              |             57 |                     57 | available                      |
|      255329 | Will Garvey win the California Senate Primary by more than 4% of the vote?  |             90 |                     90 | available                      |
|      255330 | Will Garvey win the California Senate Primary by between 2-4% of the vote?  |            173 |                    173 | available                      |
|      255331 | Will Garvey win the California Senate Primary by between 0-2% of the vote?  |            180 |                    180 | available                      |
|      255332 | Will Schiff win the California Senate Primary?                              |            364 |                    364 | available                      |
|      255422 | Will Roger Wicker win the Mississippi Republican Senate Primary?            |             14 |                     14 | available                      |
|      255423 | Will Ghannon Burton win the Mississippi Republican Senate Primary?          |              5 |                      5 | available                      |
|      255424 | Will Dan Eubanks win the Mississippi Republican Senate Primary?             |              5 |                      5 | available                      |
|      255425 | Will another candidate win the Mississippi Republican Senate Primary?       |              0 |                      0 | no_recorded_trades_zero_volume |
|      500652 | Will David Trone win Maryland US Senate Democratic Primary?                 |            270 |                    270 | available                      |
|      500653 | Will Angela Alsobrooks win Maryland US Senate Democratic Primary?           |            251 |                    251 | available                      |
|      500654 | Will another candidate win Maryland US Senate Democratic Primary?           |              6 |                      6 | available                      |
|      502030 | Will Andy Kim win New Jersey Dem Senate Primary?                            |             34 |                     34 | available                      |
|      502148 | Will Jacky Rosen win the 2024 Nevada Senate Democratic Primary?             |            101 |                    101 | available                      |
|      502149 | Will Mike Schaefer win the 2024 Nevada Senate Democratic Primary?           |             78 |                     78 | available                      |
|      502150 | Will Troy Walker win the 2024 Nevada Senate Democratic Primary?             |             68 |                     68 | available                      |
|      502151 | Will another candidate win the 2024 Nevada Senate Democratic Primary?       |             68 |                     68 | available                      |
|      502152 | Will Sam Brown win the 2024 Nevada Senate Republican Primary?               |            187 |                    187 | available                      |
|      502153 | Will Jeff Gunter win the 2024 Nevada Senate Republican Primary?             |             86 |                     86 | available                      |
|      502154 | Will Jim Marchant win the 2024 Nevada Senate Republican Primary?            |             51 |                     51 | available                      |
|      502155 | Will Tony Grady win the 2024 Nevada Senate Republican Primary?              |             65 |                     65 | available                      |
|      502156 | Will another candidate win the 2024 Nevada Senate Republican Primary?       |             46 |                     46 | available                      |
|      502224 | Will Hung Cao win the 2024 Virginia Senate Republican Primary?              |            132 |                    132 | available                      |
|      502225 | Will Jonathan Walker Emord win the 2024 Virginia Senate Republican Primary? |             54 |                     54 | available                      |
|      502226 | Will Eddie Garcia win the 2024 Virginia Senate Republican Primary?          |             33 |                     33 | available                      |
|      502228 | Will Scott Parkinson win the 2024 Virginia Senate Republican Primary?       |             35 |                     35 | available                      |
|      502229 | Will Chuck Smith win the 2024 Virginia Senate Republican Primary?           |             39 |                     39 | available                      |
|      502230 | Will another person win the 2024 Virginia Senate Republican Primary?        |             55 |                     55 | available                      |
|      504322 | Kari Lake wins Arizona Senate Primary?                                      |            132 |                    132 | available                      |
|      500105 | Will a Democrat win Nevada US Senate Election?                              |           4713 |                   1913 | available                      |
|      500106 | Will a Republican win Nevada US Senate Election?                            |           3072 |                   1000 | available                      |
|      500107 | Will a candidate from another party win Nevada US Senate Election?          |           2515 |                   2254 | available                      |
|      500108 | Will a Democrat win Pennsylvania US Senate Election?                        |           4234 |                   1183 | available                      |
|      500109 | Will a Republican win Pennsylvania US Senate Election?                      |           7124 |                   1357 | available                      |
|      500110 | Will a candidate from another party win Pennsylvania US Senate Election?    |           4783 |                   4173 | available                      |
|      500111 | Will a Democrat win Wisconsin US Senate Election?                           |           1559 |                   1153 | available                      |
|      500112 | Will a Republican win Wisconsin US Senate Election?                         |           1781 |                   1318 | available                      |
|      500113 | Will a candidate from another party win Wisconsin US Senate Election?       |           4434 |                   4247 | available                      |
|      500114 | Will a Democrat win Montana US Senate Election?                             |           2204 |                   2068 | available                      |
|      500115 | Will a Republican win Montana US Senate Election?                           |           3145 |                   2916 | available                      |
|      500116 | Will a candidate from another party win Montana US Senate Election?         |          12447 |                  12324 | available                      |
|      500117 | Will a Democrat win Ohio US Senate Election?                                |           5298 |                   4873 | available                      |
|      500118 | Will a Republican win Ohio US Senate Election?                              |           8845 |                   7902 | available                      |
|      500120 | Will a candidate from another party win Ohio US Senate Election?            |          22478 |                  22096 | available                      |
|      500614 | Will a Democrat win Arizona US Senate Election?                             |          22327 |                   4366 | available                      |
|      500615 | Will a Republican win Arizona US Senate Election?                           |          19551 |                   3769 | available                      |
|      500616 | Will a candidate from another party win Arizona US Senate Election?         |          14260 |                  11553 | available                      |
|      500618 | Will a Democrat win Texas US Senate Election?                               |           2875 |                   2506 | available                      |
|      500619 | Will a Republican win Texas US Senate Election?                             |           3386 |                   2971 | available                      |
|      500620 | Will a candidate from another party win Texas US Senate Election?           |           7809 |                   7646 | available                      |
|      500621 | Will a Democrat win Maryland US Senate Election?                            |           1152 |                   1101 | available                      |
|      500622 | Will a Republican win Maryland US Senate Election?                          |           1106 |                   1056 | available                      |
|      500623 | Will a candidate from another party win Maryland US Senate Election?        |           3244 |                   3045 | available                      |
|      500656 | Will a Democrat win Florida US Senate Election?                             |           1141 |                   1049 | available                      |
|      500657 | Will a Republican win Florida US Senate Election?                           |           1378 |                   1223 | available                      |
|      500658 | Will a candidate from another party win Florida US Senate Election?         |           8689 |                   6089 | available                      |
|      500659 | Will a Democrat win California US Senate Election?                          |            499 |                    462 | available                      |
|      500660 | Will a Republican win California US Senate Election?                        |            412 |                    385 | available                      |
|      500661 | Will a candidate from another party win California US Senate Election?      |            493 |                    457 | available                      |
|      500663 | Will a Democrat win Washington US Senate Election?                          |           1158 |                    501 | available                      |
|      500664 | Will a Republican win Washington US Senate Election?                        |            392 |                    386 | available                      |
|      500666 | Will a candidate from another party win Washington US Senate Election?      |            469 |                    427 | available                      |
|      500669 | Will a Democrat win Utah US Senate Election?                                |            345 |                    334 | available                      |
|      500670 | Will a Republican win Utah US Senate Election?                              |            578 |                    557 | available                      |
|      500671 | Will a candidate from another party win Utah US Senate Election?            |           1012 |                    990 | available                      |
|      500672 | Will a Democrat win Wyoming US Senate Election?                             |            446 |                    440 | available                      |
|      500673 | Will a Republican win Wyoming US Senate Election?                           |            367 |                    361 | available                      |
|      500674 | Will a candidate from another party win Wyoming US Senate Election?         |            565 |                    560 | available                      |
|      500677 | Will a Democrat win New Mexico US Senate Election?                          |            890 |                    496 | available                      |
|      500679 | Will a Republican win New Mexico US Senate Election?                        |            375 |                    369 | available                      |
|      500681 | Will a candidate from another party win New Mexico US Senate Election?      |            780 |                    667 | available                      |
|      500683 | Will a Democrat win North Dakota US Senate Election?                        |            319 |                    312 | available                      |
|      500684 | Will a Republican win North Dakota US Senate Election?                      |            459 |                    445 | available                      |
|      500685 | Will a candidate from another party win North Dakota US Senate Election?    |            640 |                    505 | available                      |
|      500686 | Will a Democrat win Nebraska US Senate Election?                            |           5151 |                   5028 | available                      |
|      500687 | Will a Republican win Nebraska US Senate Election?                          |           3764 |                   2930 | available                      |
|      500688 | Will a candidate from another party win Nebraska US Senate Election?        |           2466 |                   2199 | available                      |
|      500689 | Will a Democrat win Minnesota US Senate Election?                           |           1166 |                   1123 | available                      |
|      500690 | Will a Republican win Minnesota US Senate Election?                         |            700 |                    681 | available                      |
|      500691 | Will a candidate from another party win Minnesota US Senate Election?       |           2188 |                   2052 | available                      |
|      500692 | Will a Democrat win Missouri US Senate Election?                            |            502 |                    484 | available                      |
|      500693 | Will a Republican win Missouri US Senate Election?                          |            450 |                    421 | available                      |
|      500694 | Will a candidate from another party win Missouri US Senate Election?        |           1222 |                   1098 | available                      |
|      500695 | Will a Democrat win Tennessee US Senate Election?                           |            374 |                    330 | available                      |
|      500696 | Will a Republican win Tennessee US Senate Election?                         |            496 |                    489 | available                      |
|      500697 | Will a candidate from another party win Tennessee US Senate Election?       |           1287 |                   1261 | available                      |
|      500698 | Will a Democrat win Mississippi US Senate Election?                         |            569 |                    528 | available                      |
|      500699 | Will a Republican win Mississippi US Senate Election?                       |            568 |                    521 | available                      |
|      500700 | Will a candidate from another party win Mississippi US Senate Election?     |           1342 |                   1272 | available                      |
|      500701 | Will a Democrat win Indiana US Senate Election?                             |            336 |                    326 | available                      |
|      500702 | Will a Republican win Indiana US Senate Election?                           |           1154 |                    580 | available                      |
|      500703 | Will a candidate from another party win Indiana US Senate Election?         |            392 |                    362 | available                      |
|      500704 | Will a Democrat win West Virginia US Senate Election?                       |            327 |                    319 | available                      |
|      500705 | Will a Republican win West Virginia US Senate Election?                     |           1070 |                    526 | available                      |
|      500706 | Will a candidate from another party win West Virginia US Senate Election?   |           1187 |                   1142 | available                      |
|      500708 | Will a Democrat win Virginia US Senate Election?                            |            492 |                    416 | available                      |
|      500709 | Will a Republican win Virginia US Senate Election?                          |            569 |                    482 | available                      |
|      500710 | Will a candidate from another party win Virginia US Senate Election?        |           1117 |                    999 | available                      |
|      500711 | Will a Democrat win Delaware US Senate Election?                            |            461 |                    445 | available                      |
|      500712 | Will a Republican win Delaware US Senate Election?                          |            335 |                    322 | available                      |
|      500713 | Will a candidate from another party win Delaware US Senate Election?        |            705 |                    680 | available                      |
|      500715 | Will a Democrat win New Jersey US Senate Election?                          |           1557 |                   1474 | available                      |
|      500716 | Will a Republican win New Jersey US Senate Election?                        |            634 |                    594 | available                      |
|      500717 | Will a candidate from another party win New Jersey US Senate Election?      |            704 |                    626 | available                      |
|      500718 | Will a Democrat win New York US Senate Election?                            |           2222 |                   1567 | available                      |
|      500719 | Will a Republican win New York US Senate Election?                          |            501 |                    478 | available                      |
|      500720 | Will a candidate from another party win New York US Senate Election?        |           2227 |                   2132 | available                      |
|      500721 | Will a Democrat win Connecticut US Senate Election?                         |           1489 |                    816 | available                      |
|      500722 | Will a Republican win Connecticut US Senate Election?                       |            505 |                    494 | available                      |
|      500723 | Will a candidate from another party win Connecticut US Senate Election?     |            773 |                    740 | available                      |
|      500724 | Will a Democrat win Rhode Island US Senate Election?                        |            429 |                    417 | available                      |
|      500725 | Will a Republican win Rhode Island US Senate Election?                      |            742 |                    728 | available                      |
|      500726 | Will a candidate from another party win Rhode Island US Senate Election?    |           1205 |                   1199 | available                      |
|      500728 | Will a Democrat win Massachusetts US Senate Election?                       |           1015 |                    942 | available                      |
|      500729 | Will a Republican win Massachusetts US Senate Election?                     |            901 |                    867 | available                      |
|      500730 | Will a candidate from another party win Massachusetts US Senate Election?   |           2873 |                   2801 | available                      |
|      500731 | Will a Democrat win Vermont US Senate Election?                             |            399 |                    387 | available                      |
|      500732 | Will a Republican win Vermont US Senate Election?                           |            386 |                    349 | available                      |
|      500733 | Will a candidate from another party win Vermont US Senate Election?         |           2062 |                   2016 | available                      |
|      500735 | Will a Democrat win Maine US Senate Election?                               |           1278 |                    680 | available                      |
|      500736 | Will a Republican win Maine US Senate Election?                             |            269 |                    250 | available                      |
|      500737 | Will a candidate from another party win Maine US Senate Election?           |           3710 |                   3531 | available                      |
|      500738 | Will a Democrat win Hawaii US Senate Election?                              |           1636 |                   1358 | available                      |
|      500739 | Will a Republican win Hawaii US Senate Election?                            |            517 |                    447 | available                      |
|      500740 | Will a candidate from another party win Hawaii US Senate Election?          |           9372 |                   5600 | available                      |
|      501694 | Will Republicans have 49 or fewer seats in Senate after election?           |           2540 |                   1940 | available                      |
|      501695 | Will Republicans have 50 seats in Senate after election?                    |           1789 |                   1421 | available                      |
|      501696 | Will Republicans have 51 seats in Senate after election?                    |           1857 |                   1460 | available                      |
|      501697 | Will Republicans have 52 seats in Senate after election?                    |           3044 |                   1350 | available                      |
|      501698 | Will Republicans have 53 seats in Senate after election?                    |           4412 |                   1389 | available                      |
|      501699 | Will Republicans have 54 seats in Senate after election?                    |           4341 |                   1789 | available                      |
|      501700 | Will Republicans have 55 seats in Senate after election?                    |           3867 |                   2119 | available                      |
|      501701 | Will Republicans have 56 or more seats in Senate after election?            |           3320 |                   2240 | available                      |
|      507546 | Will a Democrat win Nebraska Special Senate Election?                       |            196 |                    174 | available                      |
|      507547 | Will a Republican win Nebraska Special Senate Election?                     |            267 |                    241 | available                      |
|      507548 | Will a candidate from another party win Nebraska Special Senate Election?   |            363 |                    339 | available                      |
|      511406 | Will Fischer win Nebraska senate election by 7+ points?                     |           2317 |                    686 | available                      |
|      252298 | Senate control after 2024 election?                                         |           8439 |                   7011 | available                      |
|      255448 | Will a Democrat win Michigan US Senate Election?                            |           3173 |                   2540 | available                      |
|      255449 | Will a Republican win Michigan US Senate Election?                          |           2184 |                   1474 | available                      |
|      255450 | Will a candidate from another party win US Michigan Senate Election?        |           6074 |                   5934 | available                      |
|      512450 | Will Gallego win Arizona Senate election by 3% or more?                     |           3271 |                      0 | available                      |
|      512452 | Will Gallego win Arizona Senate election by 2-3%?                           |           4385 |                      0 | available                      |
|      512455 | Will Gallego win Arizona Senate election by 1-2%?                           |           3732 |                      0 | available                      |
|      512457 | Will Gallego win Arizona Senate election by 0-1%?                           |           2775 |                      0 | available                      |
|      512458 | Will Kari Lake win Arizona Senate election by 0-1%?                         |           2842 |                      0 | available                      |
|      512459 | Will Kari Lake win Arizona Senate election by 1-2%?                         |           2396 |                      0 | available                      |
|      512460 | Will Kari Lake win Arizona Senate election by 2% or more?                   |           5913 |                      0 | available                      |


## Original archived price files

These are independently saved CLOB price-history observations from the original downloader. Empty files are reported as empty; they are not evidence of no trading. Full histories stay in the ignored cache.

|   cycle |   outcome_files |   nonempty |      points |
|--------:|----------------:|-----------:|------------:|
|    2022 |              72 |          0 | 0           |
|    2024 |             340 |        328 | 6.85242e+07 |
