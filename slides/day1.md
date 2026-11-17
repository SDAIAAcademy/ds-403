---
course: "Statistical Evaluation of AI Systems"
code: "DS-403"
version: "2027.1.0"
deck: "day1"
day: 1
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/ds-403/slides/day1.html"
---

# Statistical Evaluation of AI Systems

## Day 1: Scores have standard errors

An evaluation score is an estimate: give it a standard error that respects how the items were drawn

#### [day1#title] Scores have standard errors

*SDAIA Academy · Statistical Evaluation of AI Systems*

Day 1: An evaluation score is an estimate: give it a standard error that respects how the items were drawn

Data Science Track · 4 teaching days + capstone day · 4 sessions · 4 labs · DS-403

#### [day1#agenda] Scores have standard errors

*Today*

- **Session 1 · An evaluation is a sample**: The 600 questions are a sample from a population of questions: the formula standard error and the bootstrap of a pass rate
- **Session 2 · Clustered items**: Questions written from the same document succeed and fail together: clustered standard errors and the design effect
- **Session 3 · Repeated samples**: Five samples per question at two temperatures: variance from items and from sampling, and what averaging samples buys
- **Session 4 · Plan before results**: An analysis plan committed before the results: hypothesis, metric, unit, minimum effect and decision rule

#### [day1#setup-check] Everything runs on a laptop processor or in Colab, from supplied logs

*Before the first lab*

- **Local:** `uv sync` in `labs/`, then `uv run jupyter lab`.
- **Colab:** open a notebook from the course page; its first cell clones the repository.
- **No model call, no key:** every lab reads item-level logs in `labs/data/`.
- **Quick mode:** `DS403_QUICK=1` cuts bootstrap and simulation draws.

- **The proof.** Run `00_setup_check.ipynb`. It imports every library, reads the logs and prints the 600 questions and the four configurations.

> **Pre-work recap.** You classified Bunyan's logs with the NDMO levels: questions and verdicts are Public, the applicants' own messages would not be.

#### [day1#the-case] Bunyan Building Permits Authority must choose a configuration of Watad

*The case study*

Watad answers applicants' questions on building regulations, in Arabic and English. Four configurations are candidates:

|  | Plain prompt | Regulation retrieved |
| --- | --- | --- |
| Small open-weight model | A | B |
| Mid-size open-weight model | C | D |

- **The logs.** 600 questions from 80 regulation documents, five samples per question at temperatures 0.2 and 0.8, a model grader's verdict on every answer. Synthetic, fixed seed.

### Session 1: An evaluation is a sample

#### [day1#s1] An evaluation is a sample

*Session 1*

- Explain what population an evaluation score estimates
- Compute the formula standard error of a pass rate
- Bootstrap a pass rate and compare the two intervals

#### [day1#score-is-estimate] An evaluation is an experiment, and its questions are a sample

*The frame*

1. **Population** every question applicants could ask about the regulations
2. **Sample** the 600 questions someone wrote
3. **Estimate** D passes 74.7% of them

> **The question a reader cares about** is how D would do on questions not yet written. The 74.7% is an estimate of that, with a standard error.

#### [day1#formula-se] A pass rate is a mean of zeros and ones, so it has a standard error

*The formula*

**±1.8** points: the standard error of D's first sample, 600 questions

- `SE = √(p(1 − p) / n)` with p = 0.747 and n = 600 gives 0.0178.
- A 95% interval is p ± 1.96 SE: 71.2% to 78.1%.
- Four times the questions halves the standard error.

> **AI-off.** Work this first standard error by hand, with a calculator, before Lab 1.1 asks for it in code.

#### [day1#bootstrap-idea] Resample the questions to see how much the score would move

*The bootstrap*

1. **1 · Draw** 600 questions with replacement
2. **2 · Score** the pass rate of the draw
3. **3 · Repeat** 5,000 times
4. **4 · Read** the spread is the standard error

> **No formula needed:** the same recipe works for medians, differences and corrected rates later in the course.

#### [day1#two-intervals-agree] With 600 independent questions, the formula and the bootstrap agree

*Lab 1.1 result*

| Method | SE | 95% interval |
| --- | --- | --- |
| Formula | 0.0178 | 71.2% to 78.1% |
| Bootstrap over questions, 5,000 draws | 0.0178 | 71.2% to 78.2% |
| Bootstrap over documents | 0.0254 | wider: session 2 |

#### [day1#what-interval-says] The interval is about new questions, not about these 600

*Reading an interval*

- **It says.** If questions were written again the same way, intervals built like this would contain D's true pass rate 95% of the time.
- **It does not say.** That D passes between 71.2% and 78.1% of these 600 questions: on these, the rate is known exactly.

> **And it is silent** on questions of a different kind: dialect, new regulations, other agencies.

#### [day1#report-with-interval] A score travels with its interval, its n, its samples and its temperature

*Reporting*

Prompt for Report line:

```text
D: 74.7% (95% CI 71.2 to 78.1), 600 questions, 1 sample each, temperature 0.2
```

- Without the interval, a one-point lead looks like a win.
- Without n, samples and temperature, nobody can reproduce or compare it.

#### [day1#check-sample] What does the interval describe?

*Checkpoint*

**Question:** Configuration B scores 69.8% on the 600 questions, 95% interval 66.7% to 72.9%. A manager asks what the interval means. Which answer is right?

- A. B passes between 66.7% and 72.9% of these 600 questions
- B. B's pass rate on questions written the same way is plausibly between 66.7% and 72.9%
- C. Each answer of B passes with a probability between 66.7% and 72.9%
- D. B will score between 66.7% and 72.9% on next year's regulations

#### [day1#lab-1-1] A pass rate with two intervals

Lab 1.1 · 25 min

Bootstrap configuration D's pass rate on the 600 questions and compare the interval with the one from the formula standard error.

[D1_1_bootstrap_pass_rate.ipynb](https://sdaiaacademy.github.io/ds-403/labs/D1_1_bootstrap_pass_rate.ipynb)

- [ ] Load the logs and compute the pass rate of one sample (4 min)
- [ ] The formula standard error and a 95% interval (5 min)
- [ ] A bootstrap over questions (8 min)
- [ ] Compare the two intervals and the two distributions (5 min)
- [ ] Write the score as a reader should see it (3 min)
- [ ] ✱ Stretch: Bootstrap over documents and say why the interval widens

### Session 2: Clustered items

#### [day1#s2] Clustered items

*Session 2*

- Explain why items from one source document are not independent
- Compute a standard error clustered by document
- Report the design effect and the effective number of items

#### [day1#questions-share-documents] Questions written from one document succeed and fail together

*How the items were written*

- Khattab's team wrote 4 to 9 questions from each of 80 regulation documents.
- A document the model reads well yields many passes; an obscure one, many failures.
- So the 600 questions are not 600 independent draws: they are 80 clusters.

- **What it does.** Formulas that assume independence understate the standard error. The interval is too narrow and differences look more certain than they are.

#### [day1#clustered-formula] Sum the deviations inside each document before squaring

*The clustered standard error*

```python
# file: Lab 1.2
def clustered_se(x, groups):
    x = np.asarray(x, dtype=float)
    sums = pd.Series(x - x.mean()).groupby(groups).sum()
    return np.sqrt((sums ** 2).sum()) / len(x)
```

Deviations of the same sign inside one document add up, so a document whose questions fail together contributes much more than nine independent questions would.

#### [day1#design-effect] The design effect says how many independent questions the 600 are worth

*Design effect*

- `DEFF = (SE clustered / SE naive)²`
- Effective number of questions: n / DEFF
- D: naive SE 0.0151, clustered 0.0234

**2.4** D's design effect: 600 questions are worth about 249 independent ones

#### [day1#deff-all-configs] Every configuration's interval widens by half once documents are counted

*Lab 1.2 result*

| Config | Mean | Naive SE | Clustered SE | DEFF | Effective n |
| --- | --- | --- | --- | --- | --- |
| A | 63.2% | 0.0165 | 0.0281 | 2.88 | 209 |
| B | 69.8% | 0.0156 | 0.0258 | 2.72 | 221 |
| C | 72.1% | 0.0153 | 0.0244 | 2.54 | 236 |
| D | 74.3% | 0.0151 | 0.0234 | 2.41 | 249 |

#### [day1#cluster-bootstrap] Resample documents, or ask statsmodels for cluster covariance

*Two checks*

- **Cluster bootstrap.** Draw 80 documents with replacement and keep all their questions: SE 0.0231 against 0.0234 by formula.
- **statsmodels.** OLS on a constant with `cov_type="cluster"`: 0.0236, the formula times √(G / (G − 1)).

> **Few clusters.** With 8 categories as clusters the estimate is itself noisy; with 80 documents it is stable.

#### [day1#more-documents] New documents buy more precision than more questions per document

*What it means for writing items*

- **120 more questions from the same 80 documents.** The document effects stay; the clustered SE barely moves.
- **120 questions from 16 new documents.** More clusters: the clustered SE falls by about the square root of 96/80.

#### [day1#check-clusters] Which change narrows the interval most?

*Checkpoint*

**Question:** C's design effect is 2.5. Furat can pay for 160 more questions. Which plan narrows C's clustered interval most?

- A. 160 questions from the same 80 documents, two per document
- B. Ten samples per question in place of five
- C. 160 questions from 20 new documents
- D. Report the naive interval, which is already narrower

#### [day1#lab-1-2] Clustered by document

Lab 1.2 · 25 min

Compute standard errors clustered by source document for four configurations, the design effect and the effective number of items, and check the formula with a cluster bootstrap and statsmodels.

[D1_2_compute_standard_errors.ipynb](https://sdaiaacademy.github.io/ds-403/labs/D1_2_compute_standard_errors.ipynb)

- [ ] Questions per document and pass rate per document (4 min)
- [ ] The clustered standard error by formula (7 min)
- [ ] Design effect and effective number of items (5 min)
- [ ] A cluster bootstrap as a check (5 min)
- [ ] statsmodels with cluster covariance as a second check (4 min)
- [ ] ✱ Stretch: Cluster by category instead and explain why eight clusters are too few

### Session 3: Repeated samples

#### [day1#s3] Repeated samples

*Session 3*

- Split the variance of a score into item and sampling parts
- Predict the standard error for K samples per item
- Distinguish the mean pass rate, pass@k and pass^k

#### [day1#two-sources] A score varies because of which questions were written and because the model samples

*Two sources of noise*

- **Between items.** Some questions are easy, some hard. Only more questions reduce this part.
- **Within items.** Asked twice, the model may answer differently. More samples per question reduce this part.

`Var(question mean) = between + within / K` for the mean of K samples per question.

#### [day1#within-between-split] At temperature 0.8 the model's own randomness is more than half the variance

*Lab 1.3 result*

| Item | Value |
| --- | --- |
| 0.2 · between | 0.123 |
| 0.2 · within | 0.068 |
| 0.8 · between | 0.087 |
| 0.8 · within | 0.124 |

#### [day1#se-by-k] Five samples help; twenty barely help more

*What more samples buy*

| Samples per question | SE at 0.2 | SE at 0.8 |
| --- | --- | --- |
| 1 | 0.0179 | 0.0187 |
| 5 | 0.0151 | 0.0136 |
| 20 | 0.0145 | 0.0124 |

600 questions, configuration D, ignoring clustering. The floor is the between-item part.

#### [day1#three-estimands] The mean, pass@5 and pass^5 answer three different questions

*Pass rates over repeated attempts*

| Estimand | The question it answers | D at 0.2 | D at 0.8 |
| --- | --- | --- | --- |
| Mean per sample | One answer to one applicant | 74.3% | 70.0% |
| pass@5 | Right at least once in five tries | 86.7% | 91.2% |
| pass^5 | Right every time in five | 59.2% | 41.2% |

#### [day1#temperature-is-design] Fix the temperature and the samples in the plan, not after the results

*Temperature is part of the design*

- Evaluate at the temperature the deployed configuration will use.
- At temperature 0, sampling variance is near zero, but the score still has between-item error.
- Report the samples per question and how they were combined.

#### [day1#check-samples] Twenty samples per question

*Checkpoint*

**Question:** At temperature 0.2, D's between-item variance is 0.123 and its within-item variance 0.068. A colleague proposes 20 samples per question in place of 5 to "make the score precise". What happens?

- A. The standard error barely falls, because the between-item part does not shrink with samples
- B. The standard error halves, as it would with four times the questions
- C. The pass rate rises, because more samples find more right answers
- D. The score becomes pass@20, which is the right metric at last

#### [day1#lab-1-3] Item and sampling variance

Lab 1.3 · 25 min

Split the variance of the pass rate into item and sampling parts at temperatures 0.2 and 0.8, and predict how the standard error falls with more samples per question.

[D1_3_split_variance_into.ipynb](https://sdaiaacademy.github.io/ds-403/labs/D1_3_split_variance_into.ipynb)

- [ ] One row per question: the mean of five samples (4 min)
- [ ] Within-item variance at each temperature (6 min)
- [ ] Between-item variance, corrected for sampling (6 min)
- [ ] The standard error for 1, 5 and 20 samples (5 min)
- [ ] pass@5 and pass^5 next to the mean (4 min)
- [ ] ✱ Stretch: Check the predicted standard error for K = 2 by subsampling the logs

### Session 4: Plan before results

#### [day1#s4] Plan before results

*Session 4*

- Explain how choices made after the results inflate false wins
- Write an analysis plan for a comparison of two configurations
- State a minimum effect and a decision rule in advance

#### [day1#forking-paths] Each choice made after seeing the results is another chance of a false win

*Choices after the results*

- **Metric.** mean, first sample, pass@5
- **Subset.** all, Arabic, one category
- **Analysis.** paired or not, clustered or not
- **Exclusions.** drop "broken" questions

> **Every path is defensible alone.** Choosing the one that wins is what inflates the error rate.

#### [day1#false-wins-simulated] Choosing the best of four metrics after the fact triples the false wins

*Lab 1.4 result*

| Item | Value |
| --- | --- |
| One planned metric | 5.2% |
| Best of four, chosen after | 16.3% |

2,000 simulated comparisons of two **identical** configurations, 600 questions, five samples each.

#### [day1#what-plan-fixes] The plan fixes the question, the metric, the analysis and the decision

*What a plan fixes*

| Field | For C against D |
| --- | --- |
| Question | Is D at least three points better than C? |
| Primary metric | mean grader pass rate per sample, 5 samples, temperature 0.2 |
| Analysis | paired difference D minus C, clustered by document |
| Minimum effect | 3 points; alpha 0.05; power 0.8 |
| Slices | language and category, declared now |

#### [day1#minimum-effect] A difference can be real and still too small to act on

*The minimum effect*

- Switching configurations costs migration, retesting and serving.
- Dr. Nadeen will switch only for three points or more.
- Written before the results, the threshold cannot drift to fit them.

- **Three verdicts.** Worth switching; real but too small to matter; not shown. The plan says which interval leads to which.

#### [day1#decision-rule] Write what each possible interval leads to, before you see it

*The decision rule*

1. **Whole interval above 3 points** switch to D
2. **Above 0, but includes values below 3** D is better; whether by enough is not shown
3. **Includes 0** no difference shown; keep C

#### [day1#commit-plan] Commit the plan to git before the results exist

*Evidence that the plan came first*

```bash
# file: capstone repository
git add plan.json
git commit -m "Commit the analysis plan"
# later, in a separate commit
git add results/ analysis/
```

The commit history is the timestamp the capstone review checks. An amendment is a new dated commit with its reason, never a silent edit.

#### [day1#check-plan] The metric changed after the results

*Checkpoint*

**Question:** The plan named the mean pass rate. After the run, D beats C on pass@5 but not on the mean. The team wants to headline pass@5 "because it shows D's potential". What should the report do?

- A. Headline pass@5, since it is a recognised metric
- B. Headline pass@5 with alpha lowered to 0.01
- C. Delete pass@5 from the report entirely
- D. Headline the planned mean and label pass@5 as an unplanned, exploratory result

#### [day1#lab-1-4] A plan before the results

Lab 1.4 · 25 min

Draft a pre-registered plan comparing configurations C and D, validate it against the required fields, and simulate how choosing among four metrics after the results inflates false wins.

[D1_4_draft_pre_registered.ipynb](https://sdaiaacademy.github.io/ds-403/labs/D1_4_draft_pre_registered.ipynb)

- [ ] Read the plan template and the required fields (3 min)
- [ ] Fill the plan for C against D (8 min)
- [ ] Validate it: missing or vague fields (4 min)
- [ ] Simulate four metrics chosen after the fact (7 min)
- [ ] Commit the plan to a file with its date (3 min)
- [ ] ✱ Stretch: Add a second, secondary comparison and decide how it is adjusted

#### [day1#wrap-up] Three things to keep

*Day 1 · wrap-up*

- **A score is an estimate.** Report it with its interval, n, samples and temperature.
- **Count documents, not questions.** D's 600 questions are worth about 249 independent ones.
- **Plan first.** Metric, analysis, minimum effect and decision rule, committed before the results.

#### [day1#next] Day 2: Comparing systems

*Next*

Bring your plan for C against D. Tomorrow you test it with a paired analysis and size the next evaluation within Furat's budget.
