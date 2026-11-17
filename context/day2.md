---
course: "Statistical Evaluation of AI Systems"
code: "DS-403"
version: "2027.1.0"
deck: "day2"
day: 2
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/ds-403/slides/day2.html"
---

# Statistical Evaluation of AI Systems

## Day 2: Comparing systems

Decide whether one configuration beats another, and plan an evaluation big enough to tell

#### [day2#title] Comparing systems

*SDAIA Academy · Statistical Evaluation of AI Systems*

Day 2: Decide whether one configuration beats another, and plan an evaluation big enough to tell

Data Science Track · 4 teaching days + capstone day · 4 sessions · 4 labs · DS-403

#### [day2#agenda] Comparing systems

*Today*

- **Session 1 · Paired designs**: The same questions for both configurations: the paired difference, its standard error, and a verdict against a minimum effect
- **Session 2 · Many configurations**: Six configurations and fifteen comparisons: family-wise error, adjusted intervals and ranks that are honest about ties
- **Session 3 · Sizing an evaluation**: How many questions are needed to detect a three-point difference: the power formula with a design effect, checked by simulation
- **Session 4 · Spending the budget**: More questions or more samples per question at a fixed cost, with the grader calls in the budget

#### [day2#review-day1] Which standard error belongs in the report?

*Review of Day 1*

**Question:** A new task set has 400 questions from 40 documents. The naive standard error of a configuration's score is 0.020 and the clustered one is 0.032. Which should the report use, and what does it imply?

- A. The naive one: it is more precise
- B. The mean of the two, 0.026
- C. Either, if each question was sampled five times
- D. The clustered one: the 400 questions are worth about 156 independent ones

### Session 1: Paired designs

#### [day2#s1] Paired designs

*Session 1*

- Compute a paired difference with a clustered standard error
- Explain the width of paired and unpaired intervals from the correlation
- Write a verdict against a minimum effect

#### [day2#same-questions] C and D answered the same 600 questions, so compare them question by question

*The design you already have*

- **Unpaired.** Two scores, two standard errors, combined as if the question sets were different.
- **Paired.** One difference per question, D minus C, and the standard error of that one column.

> **Same mean, different width.** Both estimate D minus C = 2.2 points; only the paired analysis uses the fact that the questions are shared.

#### [day2#variance-of-difference] Hard questions are hard for both, and the difference removes what they share

*Why pairing helps*

`Var(D − C) = Var(D) + Var(C) − 2 Cov(C, D)`

Unpaired analysis drops the covariance term. With a strong positive correlation it overstates the variance of the difference several times over.

**0.83** correlation of C's and D's per-question scores

#### [day2#four-widths] Pairing makes the interval four times narrower than the clustered unpaired one

*Lab 2.1 result*

| Analysis of D minus C | SE | 95% half-width |
| --- | --- | --- |
| Unpaired, naive | 0.0215 | ±4.2 points |
| Unpaired, clustered | 0.0338 | ±6.6 points |
| Paired, naive | 0.0089 | ±1.7 points |
| Paired, clustered by document | 0.0086 | ±1.7 points |

#### [day2#paired-code] One column of differences, one clustered standard error

*The calculation*

```python
# file: Lab 2.1
t = U.paired_table("C", "D", 0.2)     # one row per question
d = t["diff"].mean()                  # 0.0217
se = U.clustered_se(t["diff"], t.doc_id)   # 0.0086
lo, hi = d - 1.96 * se, d + 1.96 * se      # 0.005 to 0.039
```

#### [day2#three-verdicts] D is better than C, but not shown to be better by three points

*The verdict against the minimum effect*

Figure: Paired, clustered by document; 600 questions, five samples at temperature 0.2 (Lab 2.1).

#### [day2#decision-note] Three lines the decision owner can act on

*The decision note*

Prompt for Decision note:

```text
Paired difference D minus C: 2.2 points, 95% CI 0.5 to 3.9, clustered by document, 600 questions, 5 samples, temperature 0.2. Minimum effect: 3 points. Verdict: better, not shown to matter. The unpaired analysis would have given ±6.6 points and no conclusion.
```

- At temperature 0.8 the difference is 2.9 points, CI 0.8 to 5.0: the same verdict.

#### [day2#check-paired] Two configurations on the same questions

*Checkpoint*

**Question:** Two configurations answer the same 500 questions. Their scores' intervals overlap heavily. A colleague concludes there is no difference. What is wrong with that?

- A. Overlapping separate intervals ignore the correlation; the paired interval of the difference can exclude zero
- B. The intervals should have been clustered first
- C. Nothing: overlapping intervals mean no difference
- D. The difference must be checked against the minimum effect before anything else

#### [day2#lab-2-1] Paired against unpaired

Lab 2.1 · 25 min

Compare configurations C and D with paired and unpaired analyses, explain the two widths from the correlation between them, and write a decision note against a minimum effect of three points.

[D2_1_compare_paired_unpaired.ipynb](https://sdaiaacademy.github.io/ds-403/labs/D2_1_compare_paired_unpaired.ipynb)

- [ ] One row per question with both configurations (3 min)
- [ ] The unpaired interval (4 min)
- [ ] The paired interval, clustered by document (7 min)
- [ ] The correlation explains the widths (5 min)
- [ ] A decision note with a verdict (6 min)
- [ ] ✱ Stretch: Repeat at temperature 0.8 and say whether the verdict holds

### Session 2: Many configurations

#### [day2#s2] Many configurations

*Session 2*

- Explain why fifteen comparisons need adjustment
- Compute Bonferroni and Holm adjusted paired intervals
- Report a ranking with the set of plausible ranks

#### [day2#six-configs] Six configurations mean fifteen comparisons, and fifteen chances of a false separation

*Many configurations*

| Item | Value |
| --- | --- |
| F · D, Arabic system prompt | 76.5% |
| D · mid-size, retrieval | 74.7% |
| E · D, long instructions | 74.7% |
| C · mid-size, plain | 73.2% |
| B · small, retrieval | 70.0% |
| A · small, plain | 62.7% |

One greedy sample per question, 600 questions, temperature 0.2. The naive ranking crowns F.

#### [day2#family-wise] Adjust the threshold to the number of comparisons you make

*Family-wise error*

| Method | Rule | Pairs separated |
| --- | --- | --- |
| Unadjusted | each test at 5% | 10 |
| Bonferroni | each test at 5% / 15; intervals with z = 2.94 | 6 |
| Holm | k-th smallest p against 5% / (15 − k + 1), stop at the first failure | 8 |

Both adjustments keep the chance of any false separation among the fifteen at 5%. Holm never separates fewer pairs than Bonferroni.

#### [day2#separated-pairs] At the top, nothing is separated except F from C

*Lab 2.2 result*

| Pair | Difference | p | Bonferroni interval | Holm |
| --- | --- | --- | --- | --- |
| C, F | +3.3 | 0.006 | −0.2 to 6.9 | separated |
| D, F | +1.8 | 0.24 | −2.7 to 6.4 | not |
| E, F | +1.8 | 0.19 | −2.3 to 6.0 | not |
| C, D | +1.5 | 0.32 | −2.9 to 5.9 | not |
| D, E | 0.0 | 1.00 | −4.3 to 4.3 | not |

#### [day2#plausible-ranks] Report each configuration's plausible ranks, not one number

*Ranks with honest ties*

| Config | Pass rate | Plausible ranks |
| --- | --- | --- |
| F | 76.5% | 1 to 3 |
| E | 74.7% | 1 to 4 |
| D | 74.7% | 1 to 5 |
| C | 73.2% | 2 to 5 |
| B | 70.0% | 3 to 5 |
| A | 62.7% | 6 |

#### [day2#rank-bootstrap] Resampled over documents, F is first four times in five

*Lab 2.2 stretch*

| Item | Value |
| --- | --- |
| F first | 81% |
| D first | 11% |
| E first | 7% |

2,000 resamples of the 80 documents. Likely first is not the same as shown to be first.

#### [day2#check-ranking] Announcing a winner

*Checkpoint*

**Question:** Of six configurations, F has the highest pass rate. After Holm adjustment F is separated from A, B and C, but not from D or E. What may the release note say?

- A. F is the best configuration
- B. F is the best, because it beats D at the 25% level
- C. F, D and E are tied at the top; F is better than A, B and C
- D. F, D and E are shown to be equally good

#### [day2#lab-2-2] Six configurations ranked

Lab 2.2 · 25 min

Rank six configurations on the same 600 questions with paired intervals adjusted for fifteen comparisons, and report which configurations cannot be told apart.

[D2_2_rank_six_configurations.ipynb](https://sdaiaacademy.github.io/ds-403/labs/D2_2_rank_six_configurations.ipynb)

- [ ] Six pass rates and the naive ranking (3 min)
- [ ] Fifteen paired differences, clustered (6 min)
- [ ] Bonferroni and Holm adjustments (6 min)
- [ ] Which pairs are separated (5 min)
- [ ] A rank table with plausible ranks (5 min)
- [ ] ✱ Stretch: Bootstrap the rank of each configuration over documents

### Session 3: Sizing an evaluation

#### [day2#s3] Sizing an evaluation

*Session 3*

- Derive the number of items from the paired variance, the design effect and the minimum effect
- Check a sizing formula by simulation over documents
- Explain what the pilot can and cannot tell

#### [day2#sizing-question] Size the evaluation for the difference that matters, not for the one you hope to see

*Before the next evaluation*

- **The effect.** Three points, from Dr. Nadeen: the minimum worth a switch.
- **The errors.** 5% false alarm, 80% power: a true three-point gain is found four times in five.
- **The noise.** The spread of per-question differences, from a pilot.

#### [day2#power-formula] Questions needed grow with the square of the noise over the effect

*The formula*

`n = (z0.975 + z0.80)² × s² / δ² = (1.96 + 0.84)² × 0.219² / 0.03²`

- **0.219** SD of the per-question difference D minus C
- **0.93** design effect of the difference: floored at 1
- **417** questions, about 56 documents

#### [day2#deff-in-sizing] Sizing a single score with the naive formula falls far short

*Where the design effect bites*

- **Paired difference.** DEFF about 1: the documents cancel. 417 questions.
- **Unpaired, each score DEFF about 2.4.** 5,826 questions per configuration for the same three points.

> **The same rule for a single score:** to estimate D's pass rate within ±2 points, multiply the naive n by its design effect of 2.4.

#### [day2#power-by-simulation] Resample documents from the pilot, plant three points, run the planned test

*Check by simulation*

1. **1 · Draw** 56 documents with replacement
2. **2 · Plant** shift differences to a mean of 3 points
3. **3 · Test** clustered paired interval above 0?
4. **4 · Count** 2,000 times

#### [day2#simulated-power] At the formula's 417 questions the simulated power is 85%

*Lab 2.3 result*

| Item | Value |
| --- | --- |
| 300 questions | 71% |
| 417 questions | 85% |
| 900 questions | 99% |

The formula is slightly conservative here, because the difference's design effect is below 1 and the formula floored it.

#### [day2#sizing-plan] Three lines that go into the committed plan

*The sizing plan*

Prompt for Sizing plan:

```text
Detect D minus C = 3 points (paired, two-sided, alpha 0.05) with 80% power: 417 questions from about 56 documents, 5 samples each at temperature 0.2. Pilot: 600 questions of the 2026 set; SD of the per-question difference 0.219; design effect 0.93; simulated power at 417 questions 85%.
```

#### [day2#check-sizing] Sizing from a pilot

*Checkpoint*

**Question:** A pilot of two configurations on 200 shared questions shows a 6-point difference and an SD of per-question differences of 0.25. The decision needs to detect 3 points. Which inputs should the sizing use?

- A. The 6-point difference and SD 0.25
- B. The 3-point minimum effect and SD 0.25
- C. 3 points and the SD of each configuration's scores
- D. 200 questions, since the pilot already found a difference

#### [day2#lab-2-3] Sizing for three points

Lab 2.3 · 25 min

Size an evaluation to detect a three-point difference between two configurations with 80% power, using the pilot variance and the design effect, and check the power by simulation.

[D2_3_size_evaluation_three.ipynb](https://sdaiaacademy.github.io/ds-403/labs/D2_3_size_evaluation_three.ipynb)

- [ ] Pilot variance of the paired difference (4 min)
- [ ] The formula: items for 80% power (6 min)
- [ ] The design effect in the formula (4 min)
- [ ] Power by simulation over documents (8 min)
- [ ] The sizing plan in three lines (3 min)
- [ ] ✱ Stretch: Size the unpaired design and compare the cost

### Session 4: Spending the budget

#### [day2#s4] Spending the budget

*Session 4*

- Write the variance of a score as a function of items and samples
- Find the number of samples per item that minimises variance at fixed cost
- Include grader calls and human labels in an evaluation budget

#### [day2#budget-question] Every riyal buys either new questions or more samples of the old ones

*A fixed budget*

| Unit (synthetic costs from Furat) | SAR |
| --- | --- |
| A new question, written and reviewed in both languages | 15.00 |
| One sample: a generation | 0.04 |
| One sample: a grader call | 0.06 |
| A human label of a grader verdict | 4.00 |
| Budget of the next evaluation | 6,000 |

#### [day2#variance-and-cost] The variance falls with questions and samples; the cost rises with both

*The trade-off*

- **Variance.** `(between + within / K) / n`
- **Cost.** `n × (15 + 0.10 K) ≤ 6,000`

Minimising the first under the second gives `K* = √((15 / 0.10) × within / between)`.

#### [day2#budget-result] The optimum is flat: from five to ten samples changes the error by 1%

*Lab 2.4 result*

| Temperature | K\* | Best design | SE | At K = 5 |
| --- | --- | --- | --- | --- |
| 0.2 | 9.1 | 375 questions × 10 | 0.0186 | 387 × 5: 0.0188 |
| 0.8 | 14.7 | 368 questions × 13 | 0.0162 | 387 × 5: 0.0170 |

Questions cost 150 samples each, so several samples per question pay; more of them pay at 0.8, where sampling noise is larger.

#### [day2#grader-in-budget] Leave the grader out of the cost and you over-sample; leave people out and you cannot correct

*What the budget must include*

- **Grader call forgotten.** K\* at 0.2 rises from 9.1 to 14.4: the plan buys samples it cannot afford to grade.
- **Human labels reserved.** SAR 1,200 for 300 labels leaves 300 questions × 10: SE 0.0208 instead of 0.0186.

#### [day2#clusters-in-budget] With documents in the picture, new questions should come from new documents

*One more term*

- The between-item part is inflated by the design effect, about 2.4 for one score.
- That favours spending on questions over samples, and on documents over questions per document.
- A full model has three costs: a document, a question, a sample.

#### [day2#check-budget] Spending the next SAR 6,000

*Checkpoint*

**Question:** A new question costs SAR 15 and a sample with its grader call SAR 0.10. At temperature 0.8 within-item variance exceeds between-item variance. Which design is closest to the best at a fixed budget?

- A. As many questions as possible, one sample each
- B. Few questions, thirty samples each
- C. Whatever K, since the grader cost does not enter
- D. About ten to fifteen samples per question, the rest on questions

#### [day2#lab-2-4] Items or samples at fixed cost

Lab 2.4 · 25 min

Choose between more questions and more samples per question for the next evaluation at a fixed budget, from the variance components and the unit costs, at two temperatures.

[D2_4_choose_more_items.ipynb](https://sdaiaacademy.github.io/ds-403/labs/D2_4_choose_more_items.ipynb)

- [ ] Unit costs and the budget (3 min)
- [ ] Variance for n items and K samples (5 min)
- [ ] Every affordable design and its standard error (7 min)
- [ ] The optimal K by formula (5 min)
- [ ] The choice at each temperature, with the grader in the cost (5 min)
- [ ] ✱ Stretch: Reserve part of the budget for human labels of the grader and redo the choice

#### [day2#wrap-up] Three things to keep

*Day 2 · wrap-up*

- **Pair whenever you can.** Same questions, one column of differences: four times narrower here.
- **Adjust for the comparisons you make.** Six configurations, fifteen pairs: report plausible ranks.
- **Size for the effect that matters.** 417 questions for three points, checked by simulation; spend between questions and samples.

#### [day2#next] Day 3: Small sets and imperfect graders

*Next*

Tomorrow: a 40-item safety set where one configuration passes everything, and a grader that is more lenient in Arabic than in English.
