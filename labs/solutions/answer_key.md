# DS-403 answer key (trainers only)

Every number below comes from the solutions run in full mode on the committed data (seed 403). Quick mode (`DS403_QUICK=1`) changes bootstrap and simulation results in the second decimal; the planted answers do not change. The true values the generator used are in `truth.json`.

## The planted problems

| # | Planted problem | Found in | What the solution shows |
|---|---|---|---|
| 1 | Questions cluster by document (document sd 1.5 on the logit scale) | Lab 1.2 | Design effects A 2.88, B 2.72, C 2.54, D 2.41; ignoring them shrinks every interval by a factor of about 1.6 |
| 2 | Five samples per question at two temperatures | Lab 1.3 | At 0.2 within-question variance .068, between .123; at 0.8 within .124, between .087 |
| 3 | C and D answer the same questions (correlation of per-question scores .827) | Lab 2.1 | D minus C 2.2 points (0.5 to 3.9) paired; the unpaired analysis gives ±6.6 points and no conclusion |
| 4 | Six configurations, two of them prompt variants of D | Lab 2.2 | Holm separates 8 of 15 pairs (Bonferroni 6, unadjusted 10); plausible ranks F 1 to 3, E 1 to 4, D 1 to 5, C 2 to 5, B 3 to 5, A 6 |
| 5 | A 3-point minimum effect needs more questions than the 600 | Lab 2.3 | 417 questions per configuration by formula at the paired SD; simulation over documents gives 85% power |
| 6 | The budget can buy new questions or more samples | Lab 2.4 | K* = 9.1 samples per question at 0.2 and 14.7 at 0.8 under the stated unit costs; the best affordable design at 0.8 uses 13 samples |
| 7 | The safety set has 40 items and few failures | Labs 3.1, 3.2 | A 36, B 38, C 39, D 40 safe; the Wald interval collapses for D; one-sided 95% Clopper-Pearson bound 7.2% for D (rule of three 7.5%) |
| 8 | The grader is worse in Arabic | Lab 3.3 | Arabic sensitivity .921, specificity .735; English .981 and .911 (true values .90/.70 and .94/.90) |
| 9 | Grader error inflates Arabic scores | Lab 3.4 | Corrected C: Arabic 65.2 (52.1 to 76.4), English 74.1 (66.8 to 80.9); D: Arabic 72.7 (60.5 to 83.6), English 73.4 (65.6 to 80.3) |
| 10 | 48 test questions leaked into D's tuning examples (35 verbatim, 13 more after Arabic normalisation) | Lab 4.1 | D scores 90.4 on overlapping questions against 72.9 on clean ones |
| 11 | The leaderboard scored D as the best of 5 samples and the others as the mean of 5, after trying 12 prompts for D on the test questions | Labs 4.1, 4.2 | Reported lead 14.6 points; 2.2 at equal budget; 0.8 (−0.8 to 2.3) on clean questions at equal budget |
| 12 | Eight leaderboard claims | Lab 4.2 | C1 unsupported, C2 and C3 supported, C4 to C6 unsupported, C7 and C8 untestable with these data |
| 13 | C is weaker in Arabic | Lab 4.3 | Observed gap −5.78 points (−11.53 to −0.02, p .049); after grader correction −9.0 (−22.2 to +2.4): the correction widens the interval past zero |
| 14 | The leaderboard report misses the standard's fields | Lab 4.4 | 14 problems against the standard |

## Discussion answers

- **Lab 1.1.** The first-sample pass rate for D is 74.7% (71.2 to 78.1) with the textbook SE 0.0178; resampling documents gives SE 0.0254.
- **Lab 1.4 and 4.4.** A complete plan names the population, the metric, the minimum effect, the clustering unit, the samples per question, the test and the adjustment, and is dated before results. No single right plan: mark against the template's fields.
- **Lab 2.1.** Verdict for D against C with a 3-point minimum effect: "better, not shown to matter".
- **Lab 1.4.** Between two identical configurations, a false win happens about 5.2% of the time with one planned metric and 16.3% when the best of four metrics is chosen after the results.
- **Lab 2.3.** 417 questions by formula; simulated power 71% at 300 questions, 85% at 417 and 99% at 900.
- **Lab 4.3.** The C language gap is borderline: say so, report the corrected interval beside it, and do not claim a gap after correction.
