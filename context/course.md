---
course: "Statistical Evaluation of AI Systems"
code: "DS-403"
version: "2027.1.0"
scope: "course"
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/ds-403/"
---

# Statistical Evaluation of AI Systems

Treat every evaluation of an AI system as an experiment: report scores with honest intervals, compare systems with paired designs, size evaluations within budget, correct for grader error and audit the claims

Participants treat every evaluation of an AI system as an experiment with a sampling design. On item-level results from small open-weight models on a fictional permits authority's synthetic bilingual task set, they compute clustered standard errors, compare systems with paired designs, size evaluations within a budget, use exact or Bayesian intervals for small sets, correct for grader error and audit benchmark claims. Graders and harnesses are built in AE-303, not here.

- **Audience:** Specialists. Data scientists who have completed the level 300 core or can show equivalent work: a defended analysis with a validated model or a causal estimate that they can explain.
- **Prerequisites:** DS-302 Online Experiments and A/B Testing; DS-305 Uncertainty, Interpretability and Model Validation; Computes bootstrap intervals and paired tests in code; Has logged a language model's outputs through an API; Setup: a laptop CPU with uv, or Google Colab. The sixteen labs read supplied item-level logs and call no model. Pre-work: three hours on the bootstrap and power by simulation, with an entry quiz; see labs/README.md.
- **Case study:** Bunyan Building Permits Authority: Bunyan Building Permits Authority is a fictional regional authority that issues building and construction permits. Its question assistant, Watad, answers applicants in Arabic and English from 80 regulation documents, and four configurations of it (a small and a mid-size open-weight model, each with and without the retrieved regulation) are candidates for release. Participants work on synthetic item-level logs: 600 bilingual questions from 80 documents, five samples per question at two temperatures for four configurations, six configurations for ranking, a 40-item safety set, 300 human-labelled grader verdicts, the configuration leaderboard written by the evaluation lead, and the examples used to tune one configuration. They compute clustered and small-sample intervals, compare configurations with paired designs, size the next evaluation within budget, correct pass rates for the grader's error by language, audit the leaderboard's claims and write a reporting standard. All data is synthetic and generated with a fixed seed; no model produced the logs.

## Outcomes

- LO1 (Applied): Compute standard errors and intervals for an evaluation score that account for clustered items, repeated samples and small item counts, given item-level results where questions share source documents
- LO2 (Performance): Decide whether the difference between two systems is real and large enough to matter, using a paired analysis, given item-level results for two configurations and a minimum effect
- LO3 (Performance): Design an evaluation's size in items, samples per item and grader calls to detect a stated difference within budget, given pilot variances and unit costs
- LO4 (Performance): Evaluate the bias that grader error adds to a pass rate and correct it, carrying calibration uncertainty into the interval, given a model grader with 300 human-labelled verdicts in two languages
- LO5 (Performance): Audit an evaluation claim for statistical validity, contamination risk and unequal tuning or token budgets, given a leaderboard-style report on four systems
- LO6 (Performance): Design a reporting standard for evaluation claims, including results by language and subgroup, given the audit findings and a release process

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

## Day 3: Small sets and imperfect graders

Intervals that keep their promise on small sets, and pass rates corrected for an imperfect grader

#### [day3#title] Small sets and imperfect graders

*SDAIA Academy · Statistical Evaluation of AI Systems*

Day 3: Intervals that keep their promise on small sets, and pass rates corrected for an imperfect grader

Data Science Track · 4 teaching days + capstone day · 4 sessions · 4 labs · DS-403

#### [day3#agenda] Small sets and imperfect graders

*Today*

- **Session 1 · Where large-sample intervals fail**: The normal-approximation interval fails when items are few or the rate is near 0 or 1: coverage measured by simulation
- **Session 2 · Exact and Bayesian intervals**: Exact and Bayesian intervals for a 40-item safety set where one configuration passes every item
- **Session 3 · Graders against people**: A model grader is a measuring instrument: sensitivity and specificity against people, by language
- **Session 4 · Correcting for grader error**: Correct a pass rate for the grader's error and carry the uncertainty of the calibration into the interval, by language

#### [day3#review-day2] What the paired interval allows you to say

*Review of Day 2*

**Question:** D minus C is 2.2 points, paired and clustered 95% interval 0.5 to 3.9, minimum effect 3 points. Dr. Nadeen asks for one sentence. Which is right?

- A. D is three points better; switch
- B. D is better, but not shown to be better by three points
- C. D is better, but by less than three points
- D. No difference can be shown

### Session 1: Where large-sample intervals fail

#### [day3#s1] Where large-sample intervals fail

*Session 1*

- Define the coverage of an interval
- Measure the coverage of four intervals by simulation
- Choose an interval for a small set near 0 or 1

#### [day3#small-sets-common] Many evaluations that matter have tens of items, not thousands

*Small, specialised sets*

- **Safety sets.** 40 questions on exits, walls and fuel.
- **New regulations.** A circular issued last week, 25 questions.
- **Slices.** Heritage-area questions in Arabic: 38.

> **And the rates sit near 0 or 1,** which is exactly where the normal approximation breaks.

#### [day3#coverage-defined] A 95% interval should contain the true rate in 95% of evaluations

*Coverage*

1. **1 · Fix** a true rate p and a size n
2. **2 · Draw** thousands of evaluations
3. **3 · Build** an interval for each
4. **4 · Count** how many contain p

Only n + 1 outcomes are possible, so the coverage can also be computed exactly by summing binomial probabilities.

#### [day3#four-intervals] Wald is the formula of Day 1; three others behave better near the edges

*Four intervals for a proportion*

| Interval | Idea | 38 of 40 |
| --- | --- | --- |
| Wald | p ± 1.96 √(p(1 − p) / n) | 0.883 to 1.018 |
| Wilson | inverts the score test; centre pulled toward 0.5 | 0.835 to 0.986 |
| Clopper-Pearson | exact, from Beta quantiles; never under-covers | 0.831 to 0.994 |
| Jeffreys | Beta(0.5, 0.5) prior, posterior interval | 0.849 to 0.989 |

#### [day3#coverage-table] With 20 items at 98%, Wald covers the truth one time in three

*Lab 3.1 result*

| Coverage at p = 0.98 | n = 20 | 40 | 80 | 200 |
| --- | --- | --- | --- | --- |
| Wald | 0.32 | 0.55 | 0.81 | 0.90 |
| Wilson | 0.94 | 0.96 | 0.98 | 0.93 |
| Jeffreys | 0.94 | 0.96 | 0.98 | 0.96 |
| Clopper-Pearson | 0.99 | 0.99 | 0.98 | 0.96 |

#### [day3#why-wald-fails] Near 1, Wald's estimated variance collapses exactly where it is least reliable

*Why*

- At 40 of 40, √(p(1 − p) / n) = 0: the interval is the single point 1.
- At 39 of 40 it is narrow and centred too high.
- The rate's distribution is skewed near the edge; Wald assumes symmetry.

**87%** Wald's exact coverage at n = 40, p = 0.95

#### [day3#interval-rule] Small or extreme: Wilson or Jeffreys; a safety claim: Clopper-Pearson

*A rule for the standard*

- **Hundreds of items, rate mid-range.** Any interval; the clustered one for documents.
- **Fewer items, or within 0.1 of an edge.** Wilson or Jeffreys: near 95% on average.
- **A claim that must not under-cover.** Clopper-Pearson: at least 95%, wider.

#### [day3#check-coverage] Choosing an interval for a small set

*Checkpoint*

**Question:** A new circular yields 25 questions; configuration D passes 24. The report needs a 95% interval for D's pass rate. Which choice is sound?

- A. p ± 1.96 √(p(1 − p) / n), the standard formula
- B. A bootstrap over the 25 questions
- C. A Wilson or Jeffreys interval, or Clopper-Pearson if it supports a safety claim
- D. No interval: 25 items are too few to say anything

#### [day3#lab-3-1] Coverage by simulation

Lab 3.1 · 25 min

Simulate the coverage of the Wald, Wilson, Clopper-Pearson and Jeffreys intervals for 20 to 200 items at rates near 0, 0.5 and 1.

[D3_1_simulate_interval_coverage.ipynb](https://sdaiaacademy.github.io/ds-403/labs/D3_1_simulate_interval_coverage.ipynb)

- [ ] Four interval functions (6 min)
- [ ] One coverage estimate by simulation (5 min)
- [ ] The grid: 20 to 200 items, five rates (7 min)
- [ ] Read the table: where Wald fails (4 min)
- [ ] A rule for the authority (3 min)
- [ ] ✱ Stretch: Compute the exact coverage by summing the binomial and compare

### Session 2: Exact and Bayesian intervals

#### [day3#s2] Exact and Bayesian intervals

*Session 2*

- Compute a Clopper-Pearson interval for a small set
- Compute a Beta posterior interval and state its prior
- Report 40 out of 40 without claiming perfection

#### [day3#safety-set] Forty questions where a wrong answer could hurt someone

*Bunyan's safety set*

| Item | Value |
| --- | --- |
| A | 36 / 40 |
| B | 38 / 40 |
| C | 39 / 40 |
| D | 40 / 40 |

One greedy answer per question per configuration; each marked safe or unsafe by Sereen's panel. Topics: exits blocked during works, load-bearing walls, fuel in basements, floors added without a structural report, steep ramps.

#### [day3#forty-of-forty] Forty out of forty does not mean never

*The edge case*

- **[1, 1]** Wald: certainty from 40 questions
- **0.928** one-sided 95% lower bound, 0.051/40
- **7.2%** the unsafe rate the data cannot rule out

The rule of three gives nearly the same: 3 / 40 = 7.5%.

#### [day3#clopper-pearson-code] Clopper-Pearson comes from two Beta quantiles

*Exact intervals*

```python
# file: Lab 3.2
def clopper_pearson(k, n, level=0.95):
    a = 1 - level
    lo = 0.0 if k == 0 else stats.beta.ppf(a / 2, k, n - k + 1)
    hi = 1.0 if k == n else stats.beta.ppf(1 - a / 2, k + 1, n - k)
    return lo, hi
```

D, 40 of 40: 0.912 to 1. C, 39 of 40: 0.868 to 0.999. A, 36 of 40: 0.763 to 0.972.

#### [day3#beta-posterior] A Beta prior and k of n give a Beta posterior, and its interval

*Bayesian intervals*

`prior Beta(a, b) → posterior Beta(a + k, b + n − k)`

- Uniform prior, Beta(1, 1): D 0.914 to 0.999.
- Jeffreys prior, Beta(0.5, 0.5): D 0.940 to 1.000.

- **State the prior.** At 40 of 40 the prior moves the lower end by 2.6 points. In a safety claim the uniform prior is the more cautious of the two.

#### [day3#compare-small] Is C safer than A? Probably, but 40 questions cannot settle it

*Comparing on a small set*

**0.90** posterior probability that C's safe rate exceeds A's (39/40 against 36/40)

- Draw from both uniform posteriors, count how often C is ahead.
- A one-in-ten chance that A is in fact at least as safe.
- For a release gate, set the threshold before looking.

#### [day3#safety-line] Write what the 40 questions show, and stop there

*The release note*

Prompt for Safety line:

```text
Safety set (40 questions, one greedy answer each): D was safe on 40 of 40; with 95% confidence its unsafe-answer rate on such questions is below 7.2% (one-sided Clopper-Pearson). C 39/40, B 38/40, A 36/40.
```

#### [day3#check-safety] Zero failures

*Checkpoint*

**Question:** A configuration answers 60 safety questions with no unsafe answer. Which statement can the report make at 95% confidence?

- A. Its unsafe rate on such questions is below about 5%
- B. It never gives unsafe answers on such questions
- C. Its unsafe rate is 0% ± 0
- D. At most 3 of the next 60 answers will be unsafe

#### [day3#lab-3-2] Forty safety questions

Lab 3.2 · 25 min

Compute exact and Beta-posterior intervals for the four configurations on the 40-item safety set, including 40 out of 40, and compare them with the normal approximation.

[D3_2_compute_exact_beta.ipynb](https://sdaiaacademy.github.io/ds-403/labs/D3_2_compute_exact_beta.ipynb)

- [ ] Safe answers per configuration (3 min)
- [ ] The normal-approximation interval and its failure (4 min)
- [ ] Clopper-Pearson intervals (6 min)
- [ ] Beta posteriors under two priors (7 min)
- [ ] The safety line for the release note (5 min)
- [ ] ✱ Stretch: The posterior probability that C is safer than A

### Session 3: Graders against people

#### [day3#s3] Graders against people

*Session 3*

- Estimate a grader's sensitivity and specificity from human labels
- Compare the grader's errors by language with intervals
- Decide which logs may go to a hosted grader under the data classification

#### [day3#grader-instrument] Every pass rate so far was a model's verdict, and a model makes errors

*The grader is a measuring instrument*

- **Sensitivity.** Of answers people pass, the share the grader passes.
- **Specificity.** Of answers people fail, the share the grader fails.

> **Graders are built in AE-303.** Here the grader is given; the question is what its errors do to the statistics.

#### [day3#calibration-set] Sereen's panel labelled 300 answers, 150 in each language

*The calibration set*

| Arabic | grader fails | grader passes |
| --- | --- | --- |
| people fail | 36 | 13 |
| people pass | 8 | 93 |

| English | grader fails | grader passes |
| --- | --- | --- |
| people fail | 41 | 4 |
| people pass | 2 | 103 |

#### [day3#rates-by-language] The grader passes a quarter of the bad Arabic answers

*Lab 3.3 result*

|  | Sensitivity | Specificity |
| --- | --- | --- |
| Arabic | 0.921 (0.851 to 0.959) | 0.735 (0.597 to 0.838) |
| English | 0.981 (0.933 to 0.995) | 0.911 (0.793 to 0.965) |

Wilson intervals. Specificity rests on 49 failed answers in Arabic and 45 in English.

#### [day3#agreement-hides] Ninety-one per cent agreement, and an Arabic error that inflates every Arabic score

*What agreement hides*

| Item | Value |
| --- | --- |
| Agreement, overall | 91% |
| Agreement, English | 96% |
| Agreement, Arabic | 86% |
| Bad Arabic answers passed | 26.5% |

#### [day3#unequal-error] The specificity gap between languages is real

*Unequal error by language*

**0.18** English minus Arabic specificity, 95% CI 0.03 to 0.33

- Arabic pass rates are inflated more than English ones.
- A configuration weak in Arabic looks less weak than it is.
- The SDAIA AI Bias Reference Guide names measurement and evaluation bias: this is both.

#### [day3#more-labels] To pin specificity down, find more failed answers, not more answers

*More labels, of the right kind*

- **At random.** Specificity within ±0.05 needs 300 failed Arabic answers: about 919 labels, SAR 3,676.
- **Targeted.** Label answers the grader passed and those it is unsure of: false passes appear far more often.

#### [day3#check-grader] Reading a grader report

*Checkpoint*

**Question:** A grader agrees with people on 92% of 400 verdicts. In Arabic its specificity is 0.70; in English 0.92. What does that do to the pass rates it reports?

- A. Nothing: 92% agreement is good enough
- B. Arabic pass rates are understated
- C. Both languages are biased equally, so comparisons are safe
- D. Arabic pass rates are inflated more than English ones, shrinking any language gap

#### [day3#lab-3-3] The grader against people

Lab 3.3 · 25 min

Estimate the model grader's sensitivity and specificity in Arabic and English from 300 human-labelled verdicts, with intervals, and test whether its errors differ by language.

[D3_3_estimate_grader_sensitivity.ipynb](https://sdaiaacademy.github.io/ds-403/labs/D3_3_estimate_grader_sensitivity.ipynb)

- [ ] The 300 verdicts: a confusion table per language (5 min)
- [ ] Sensitivity and specificity with Wilson intervals (7 min)
- [ ] Overall agreement and what it hides (4 min)
- [ ] The difference between languages (5 min)
- [ ] How many more labels, and of which kind (4 min)
- [ ] ✱ Stretch: Cohen's kappa per language next to agreement

### Session 4: Correcting for grader error

#### [day3#s4] Correcting for grader error

*Session 4*

- Correct an observed pass rate with sensitivity and specificity
- Carry calibration uncertainty into the interval by bootstrap
- Report corrected and uncorrected rates by language

#### [day3#correction-formula] Solve the grader's mixing for the true pass rate

*The correction*

`observed = θ × sens + (1 − θ) × (1 − spec)`

`θ = (observed + spec − 1) / (sens + spec − 1)`

- **Example.** C in Arabic: observed 0.692, sens 0.921, spec 0.735, corrected 0.652.

> **It needs sens + spec above 1,** and it leaves 0 to 1 when the observed rate is below 1 − spec or above sens.

#### [day3#correction-point] The correction lowers Arabic rates four times as much as English ones for C

*Lab 3.4 result*

|  | Observed | Corrected | Change |
| --- | --- | --- | --- |
| C, Arabic | 69.2% | 65.2% | −4.1 |
| C, English | 75.0% | 74.1% | −0.9 |
| D, Arabic | 74.2% | 72.7% | −1.5 |
| D, English | 74.3% | 73.4% | −1.0 |

#### [day3#two-uncertainties] The corrected rate is uncertain because of the test set and because of the calibration set

*Two sources of uncertainty*

- **Test set only.** Clustered SE of the observed rate divided by (sens + spec − 1): ±8.3 points for C in Arabic. Too narrow.
- **Both.** Resample documents of the test set and, independently, the calibration verdicts; recompute sens, spec and the correction each time.

#### [day3#bootstrap-both-code] Resample both sets, then correct

*One replicate*

```python
# file: Lab 3.4
pick = rng.integers(0, len(sums), size=len(sums))      # documents
p = sums[pick].sum() / cnts[pick].sum()
j = rng.integers(0, len(h), size=len(h))               # calibration verdicts
sens = v[j][h[j] == 1].mean()
spec = 1 - v[j][h[j] == 0].mean()
draw = (p + spec - 1) / (sens + spec - 1)
```

#### [day3#corrected-table] Corrected rates are lower and their intervals much wider, most of all in Arabic

*The evidence for LO4*

|  | Observed (95% CI) | Corrected (95% CI) |
| --- | --- | --- |
| C, Arabic | 69.2 (63.8 to 74.6) | 65.2 (52.1 to 76.4) |
| C, English | 75.0 (69.3 to 80.8) | 74.1 (66.8 to 80.9) |
| D, Arabic | 74.2 (69.0 to 79.4) | 72.7 (60.5 to 83.6) |
| D, English | 74.3 (68.7 to 80.0) | 73.4 (65.6 to 80.3) |

#### [day3#correction-assumption] The correction holds only if the grader errs on test answers as it did on calibration answers

*The assumption*

- Calibrate per language, and per configuration if their answers differ in style.
- Draw calibration answers from the same population as the test answers.
- Re-calibrate when the grader, its prompt or the configurations change.

#### [day3#check-correction] An interval for a corrected rate

*Checkpoint*

**Question:** You corrected an Arabic pass rate with sensitivity and specificity from 150 labelled answers, and built the interval from the test set's clustered standard error only. What is wrong?

- A. Nothing: the correction removes the grader's error
- B. The interval ignores the uncertainty of sensitivity and specificity, so it is too narrow
- C. The calibration set should have been clustered by document too
- D. Corrected rates should be reported without intervals

#### [day3#lab-3-4] Correcting the pass rate

Lab 3.4 · 25 min

Correct configuration C's and D's pass rates for grader error in each language, and build intervals that resample both the test questions and the 300 human-labelled verdicts.

[D3_4_correct_pass_rate.ipynb](https://sdaiaacademy.github.io/ds-403/labs/D3_4_correct_pass_rate.ipynb)

- [ ] The correction formula as a function (5 min)
- [ ] Corrected rates by language (5 min)
- [ ] An interval from the test set only (4 min)
- [ ] A bootstrap over test questions and calibration verdicts (7 min)
- [ ] The table: uncorrected and corrected, by language (4 min)
- [ ] ✱ Stretch: Find the observed rates at which the correction leaves 0 to 1

#### [day3#wrap-up] Three things to keep

*Day 3 · wrap-up*

- **Small or extreme: not Wald.** Wilson or Jeffreys; Clopper-Pearson for safety.
- **Forty of forty is a bound.** Below 7.2% unsafe at 95%, not "never".
- **Correct for the grader, by language.** And carry the calibration's uncertainty into the interval.

#### [day3#next] Day 4: Auditing claims and setting standards

*Next*

Read Khattab's leaderboard (labs/data/leaderboard_report.md) tonight: eight claims, and you will class each one tomorrow.

## Day 4: Auditing claims and setting standards

Audit the claims an evaluation makes, slice by language, and write the standard every report must meet

#### [day4#title] Auditing claims and setting standards

*SDAIA Academy · Statistical Evaluation of AI Systems*

Day 4: Audit the claims an evaluation makes, slice by language, and write the standard every report must meet

Data Science Track · 4 teaching days + capstone day · 4 sessions · 4 labs · DS-403

#### [day4#agenda] Auditing claims and setting standards

*Today*

- **Session 1 · Contamination and unequal budgets**: Test items in the tuning examples, best of many prompts, and best of five samples: why two scores are not comparable
- **Session 2 · Auditing a report**: Every claim of a report is supported, unsupported or untestable, and the memo says which and why
- **Session 3 · Slicing by language**: An average hides a language: Arabic and English results with intervals, and a test of the gap
- **Session 4 · A reporting standard**: A reporting standard: the fields every evaluation claim must carry, a worked example, and the capstone choice

#### [day4#review-day3] A grader, a small set, and an interval

*Review of Day 3*

**Question:** A grader's Arabic specificity is 0.73, from 49 human-failed answers. A team corrects an Arabic pass rate and reports an interval from the test set alone. What should the reviewer ask for?

- A. Nothing: the corrected rate is unbiased
- B. A Clopper-Pearson interval on the test set
- C. An interval that also resamples the calibration verdicts
- D. The uncorrected rate, which has a narrower interval

### Session 1: Contamination and unequal budgets

#### [day4#s1] Contamination and unequal budgets

*Session 1*

- Detect overlap between test items and tuning examples, including Arabic spelling variants
- Measure how overlap changes a score
- Recompute a comparison at equal budgets

#### [day4#the-leaderboard] D at 86.7%, fifteen points ahead of C

*Khattab's leaderboard*

| Item | Value |
| --- | --- |
| D | 86.7% |
| C | 72.1% |
| B | 69.8% |
| A | 63.2% |

- 600 questions, temperature 0.2, five samples, model grader.
- No intervals, no slices, no word on how D was tuned.

#### [day4#settings-differ] D was scored differently and tuned on the test set

*How each was scored*

| Config | Scored as | Prompt variants tried on the test set | Max output tokens |
| --- | --- | --- | --- |
| A, B, C | mean of 5 samples | 1 | 512 |
| D | best of 5 samples | 12 | 2,048 |

#### [day4#contamination] Test questions inside the tuning examples inflate the score on exactly those questions

*Contamination*

- **Pre-training contamination:** a public benchmark in a model's training data.
- **Tuning contamination:** test items among the few-shot or prompt-tuning examples.
- The model then recalls answers instead of reading the regulation.

- **The test.** Find the overlap, then compare each configuration's score on overlapping and clean questions.

#### [day4#arabic-normalisation] An exact match finds 35 overlapping questions; normalising Arabic finds 48

*Arabic spelling variants*

| Folded | Example |
| --- | --- |
| hamza on alef | الأدنى ← الادنى |
| ta marbuta | لائحة ← لائحه |
| alef maqsura | في ← فى |
| diacritics, tatweel, spaces | removed |

**13 of 21** Arabic overlaps found only after normalisation

#### [day4#overlap-effect] Only D scores higher on the overlapping questions: 90.4% against 72.9%

*Lab 4.1 result*

| Config | Overlapping (48) | Clean (552) | Difference |
| --- | --- | --- | --- |
| A | 64.6% | 63.0% | +1.5 |
| B | 68.3% | 69.9% | −1.6 |
| C | 72.1% | 72.1% | 0.0 |
| D | 90.4% | 72.9% | +17.6 |

#### [day4#equal-budgets] Fifteen points become two, then one, and the last one is not shown

*The comparison, made fair*

| D minus C | Points |
| --- | --- |
| As reported: D best of 5, C mean of 5 | 14.6 |
| Equal budget: both mean of 5, all questions | 2.2 (0.5 to 3.9) |
| Equal budget, clean questions only | 0.8 (−0.8 to 2.3) |

Choosing the best of 12 equally good prompts on the test set adds about 0.8 points by itself (Lab 4.1 stretch).

#### [day4#saturation] A saturated or public benchmark cannot separate strong systems

*One more threat*

- When every system scores near the ceiling, differences sit inside the noise (Day 3).
- A public set may be in some systems' training data and not others'.
- Keep a private, versioned set, refreshed as regulations change.

#### [day4#check-budgets] A fair comparison

*Checkpoint*

**Question:** A report compares two configurations. One was scored as the best of five samples and tuned on 12 prompt variants using the test questions; the other as the mean of five, untuned. What must the audit do first?

- A. Rescore both the same way and remove the test questions used in tuning before comparing
- B. Add confidence intervals to the reported numbers
- C. Ask for more test questions
- D. Accept it: the tuned configuration earned its lead

#### [day4#lab-4-1] Overlap and unequal budgets

Lab 4.1 · 25 min

Check configuration D's comparison for test questions that appear in its tuning examples, after Arabic normalisation, measure the score on clean questions, and recompute the comparison at equal budgets.

[D4_1_check_comparison_test.ipynb](https://sdaiaacademy.github.io/ds-403/labs/D4_1_check_comparison_test.ipynb)

- [ ] Exact matches between tuning examples and test questions (4 min)
- [ ] Arabic normalisation and the matches it adds (6 min)
- [ ] D on clean and overlapping questions (5 min)
- [ ] Best of five against mean of five (5 min)
- [ ] The comparison at equal budgets, clean questions only (5 min)
- [ ] ✱ Stretch: Estimate the winner's curse of choosing the best of twelve prompts on the test set

### Session 2: Auditing a report

#### [day4#s2] Auditing a report

*Session 2*

- Classify an evaluation claim by the evidence it needs
- Re-analyse a claim from item-level logs
- Write an audit memo a decision owner can act on

#### [day4#three-classes] Every claim is supported, unsupported or untestable

*Auditing a claim*

- **Supported.** The data back it at the strength stated.
- **Unsupported.** The available data contradict it, or do not back it as stated.
- **Untestable.** No data the authority holds could decide it.

> **From DS-305.** The same three classes were used for model-card claims; here the evidence is statistical.

#### [day4#evidence-needed] Write down what would decide each claim

*Before re-analysing*

| Claim | Decided by |
| --- | --- |
| C1 D leads C by 15 points | equal budgets, clean questions, paired and clustered |
| C2, C3 B beats A (at 0.2, at 0.8) | paired clustered difference at each temperature |
| C4 D never unsafe | an upper bound from 40 of 40 |
| C5 no grader correction needed | specificity by language |
| C6 C equal in both languages | clustered gap, observed and corrected |
| C7, C8 the 2027 lead; applicants' preference | data the authority does not have |

#### [day4#audit-results] Two claims supported, four unsupported, two untestable

*Lab 4.2 result*

| Claim | Class | Deciding number |
| --- | --- | --- |
| C1 | unsupported | clean, equal budgets: 0.8 points (−0.8 to 2.3) |
| C2 | supported | B minus A 6.6 points (4.5 to 8.8) |
| C3 | supported | at 0.8: 2.1 points (0.2 to 4.1) |
| C4 | unsupported | unsafe rate below 7.2%, not zero |
| C5 | unsupported | Arabic specificity 0.73 against 0.91 |
| C6 | unsupported | Arabic minus English −5.8 points (−11.5 to just below 0) |
| C7, C8 | untestable | no 2027 data; no preference data |

#### [day4#untestable-is-information] An untestable claim tells the decision owner what evidence to commission

*Untestable claims*

- **C7 · the 2027 regulations.** A new population: size a new set (Day 2: 417 questions for three points).
- **C8 · applicants' preference.** Needs a preference study or an online experiment (DS-302), not grader verdicts.

#### [day4#memo-shape] One line per claim: the class, the number, the claim that would be supported

*The audit memo*

Prompt for Audit memo, line C4:

```text
C4 unsupported: 40 of 40 bounds D's unsafe rate below 7.2% at 95%; it does not show "never". Supported version: "D gave no unsafe answer on the 40-question safety set; with 95% confidence its unsafe rate on such questions is below 7.2%."
```

#### [day4#audit-ethics] Audit the claims, not the person

*Auditing colleagues' work*

- Khattab's numbers were computed correctly; the comparison was not fair.
- Show every re-analysis with its code, so the author can rerun it.
- A standard (session 4) prevents the next report from needing an audit.

#### [day4#check-audit] Classing a claim

*Checkpoint*

**Question:** A report claims "the assistant is equally accurate for all regions". The logs carry no region field. How should the audit class the claim?

- A. Supported: no regional difference was found
- B. Unsupported: equal accuracy is unlikely
- C. Supported, because regions should not matter for regulations
- D. Untestable with these logs; name the data that would test it

#### [day4#lab-4-2] Auditing the leaderboard

Lab 4.2 · 25 min

Classify each of the eight claims of the configuration leaderboard as supported, unsupported or untestable, with the re-analysis that decides each, and write the audit memo.

[D4_2_classify_each_claim.ipynb](https://sdaiaacademy.github.io/ds-403/labs/D4_2_classify_each_claim.ipynb)

- [ ] Read the report and its eight claims (3 min)
- [ ] The evidence each claim needs (4 min)
- [ ] Re-analyse the testable claims (10 min)
- [ ] Classify all eight (4 min)
- [ ] The audit memo (4 min)
- [ ] ✱ Stretch: Rewrite one unsupported claim so that the data supports it

### Session 3: Slicing by language

#### [day4#s3] Slicing by language

*Session 3*

- Report a score by language with clustered intervals
- Test the gap between languages using documents with questions in both
- Show how grader correction changes a gap

#### [day4#averages-hide] C and D have similar averages; one of them is weaker in Arabic

*Averages hide groups*

| Item | Value |
| --- | --- |
| C · Arabic | 69.2% |
| C · English | 75.0% |
| D · Arabic | 74.2% |
| D · English | 74.3% |

#### [day4#slice-intervals] Each slice keeps its clustering: about 300 questions over the same 80 documents

*Intervals per language*

| Config | Arabic (95% CI) | English (95% CI) |
| --- | --- | --- |
| A | 63.0 (57.4 to 68.6) | 63.4 (56.7 to 70.1) |
| B | 70.6 (65.2 to 75.9) | 69.0 (62.9 to 75.1) |
| C | 69.2 (63.8 to 74.6) | 75.0 (69.3 to 80.8) |
| D | 74.2 (69.0 to 79.4) | 74.3 (68.7 to 80.0) |

#### [day4#gap-test] Test the gap itself, clustered by document, because most documents have questions in both languages

*Testing the gap*

- Each Arabic question gets weight +1 / nar, each English one −1 / nen.
- Sum the weighted deviations within each document, then square.
- A hard document lowers both languages; that part cancels.

**−5.8** C's Arabic minus English, 95% CI −11.5 to −0.02 points

#### [day4#corrected-gap] Correction widens C's gap to nine points, and its interval with it

*With the grader corrected*

| Config | Observed gap | Corrected gap (95% CI) |
| --- | --- | --- |
| C | −5.8 | −9.0 (−22.2 to +2.4) |
| A | −0.4 | −5.5 (−19.6 to +6.8) |
| D | −0.2 | −0.7 (−12.4 to +10.8) |

The lenient Arabic grader was shrinking the gap; the 49 failed Arabic answers in the calibration set make the corrected interval wide.

#### [day4#slice-table] A slice table: rate and interval per language, the gap, observed and corrected

*What the report shows*

- Every configuration, both languages, with clustered intervals.
- The gap with its own interval; corrected for the grader by language.
- Categories as a second slice, adjusted for eight comparisons.

#### [day4#check-slices] Two overlapping intervals

*Checkpoint*

**Question:** C's Arabic interval is 63.8 to 74.6 and its English interval 69.3 to 80.8. They overlap. Most documents have questions in both languages. What can you conclude about the gap?

- A. No gap: the intervals overlap
- B. Nothing yet: test the gap itself with a standard error clustered by document
- C. Compute the gap's SE as the root sum of the two squared SEs
- D. Report both rates; gaps are never tested

#### [day4#lab-4-3] Arabic and English

Lab 4.3 · 25 min

Report each configuration's Arabic and English pass rates with clustered intervals, test the gap, and show how the grader correction changes it.

[D4_3_report_arabic_english.ipynb](https://sdaiaacademy.github.io/ds-403/labs/D4_3_report_arabic_english.ipynb)

- [ ] Pass rates by language for four configurations (4 min)
- [ ] Clustered intervals per language (5 min)
- [ ] The gap and its interval (7 min)
- [ ] The gap after grader correction (5 min)
- [ ] The slice table for the report (4 min)
- [ ] ✱ Stretch: Slice by category as well and adjust for eight comparisons

### Session 4: A reporting standard

#### [day4#s4] A reporting standard

*Session 4*

- List the required fields of an evaluation report
- Validate a worked example against the standard
- Choose the configurations and the plan of the capstone

#### [day4#findings-to-fields] Every failure this week becomes a required field of the standard

*From findings to fields*

| Field | The failure it prevents |
| --- | --- |
| plan_commit | metric and slices chosen after the results |
| items_and_clusters | 600 questions treated as independent |
| estimand, decoding | best of five compared with mean of five |
| comparison, multiplicity | unpaired comparisons; unadjusted rankings |
| grader_calibration | a lenient Arabic grader left uncorrected |
| budget_parity, overlap_check | tuning on the test set; unequal scoring |
| slices, small_sets | an Arabic gap hidden; 40 of 40 read as never |

#### [day4#validator] A validator turns the standard into a gate

*Make it checkable*

```python
# file: Lab 4.4
def validate(report):
    problems = [f"missing: {f}" for f in STANDARD if not report.get(f)]
    if not {"ar", "en"} <= set(report.get("slices") or {}):
        problems.append("slices: Arabic and English required")
    if report.get("shared_items") and "paired" not in report.get("comparison", ""):
        problems.append("comparison must be paired")
    return problems
```

#### [day4#worked-example] The week's decision passes the standard; the leaderboard fails on fourteen counts

*The worked example*

- **D against C, reported to the standard.** Plan committed; clustered and paired; 3-point minimum effect; grader by language; overlap checked; slices; safety bound. Passes.
- **The leaderboard.** Ten fields missing; naive intervals; an unpaired ranking; no slices; no grader rates. Fourteen problems.

#### [day4#release-process] The standard is checked before a report reaches the release decision

*Where the standard sits*

1. **1 · Plan** committed, dated
2. **2 · Run** logs kept per item
3. **3 · Report** to the standard
4. **4 · Gate** validator, then review
5. **5 · Decide** Dr. Nadeen

#### [day4#capstone-choice] Choose two open-weight configurations, and commit the plan before anything runs

*The capstone*

- Two or more configurations you serve yourself: a laptop (llama.cpp, Ollama), a free notebook GPU (vLLM), or a free hosted endpoint.
- Bunyan's 600 questions, or your own set with a licence that allows it.
- Starter: `labs/capstone/`.

- **First commit.** capstone_plan.json from Lab 4.4: configurations, minimum effect, samples, temperature, primary comparison.

#### [day4#check-standard] The field that matters

*Checkpoint*

**Question:** A team's report has intervals, a plan and slices, but scores its own configuration as the best of five samples and the vendor's as the mean of five. Which field of the standard catches it?

- A. multiplicity
- B. slices
- C. budget_parity, with the estimand stated per configuration
- D. interval_method

#### [day4#lab-4-4] The standard and the capstone choice

Lab 4.4 · 25 min

Draft the reporting standard's required fields, test a worked example against them, and choose the configurations and the plan of the capstone.

[D4_4_reporting_standard.ipynb](https://sdaiaacademy.github.io/ds-403/labs/D4_4_reporting_standard.ipynb)

- [ ] Fields from the week's findings (6 min)
- [ ] A validator for a report (6 min)
- [ ] The worked example: pass and fail (5 min)
- [ ] Choose the capstone configurations (5 min)
- [ ] Commit the capstone plan (3 min)
- [ ] ✱ Stretch: Turn the standard into a release gate that blocks a report with a missing field

#### [day4#wrap-up] Three things to keep

*Day 4 · wrap-up*

- **Same budget, clean items.** Fifteen points became 0.8, not shown.
- **Three classes, one number each.** Supported, unsupported, untestable, with the claim that would be supported.
- **Slice, correct, standardise.** Arabic and English with intervals; fifteen required fields.

#### [day4#next] Capstone: your statistical evaluation report

*Next*

Commit your plan before any result. Bring the repository link, results by language and one statistical choice you are ready to defend.

## Capstone: Capstone project presentations

Fifteen minutes each: the committed plan, the measured results, and one statistical choice defended live

#### [capstone#title] Capstone project presentations

*SDAIA Academy · Statistical Evaluation of AI Systems*

Capstone: Fifteen minutes each: the committed plan, the measured results, and one statistical choice defended live

Data Science Track · 4 teaching days + capstone day · 15 min talk and demo · DS-403

#### [capstone#agenda] How the capstone day runs

*Capstone*

- **Supervised check and final prep**: AI-off on paper, then the rubric and a last rehearsal
- **Reviews**: each one timed, the assessor's challenge inside
- **Review and closing**: peer feedback, the trainer's review, what next

#### [capstone#rubric] The rubric

*How presentations are scored*

| Item | Value |
| --- | --- |
| Plan | 20% |
| Uncertainty and comparison | 25% |
| Sizing | 15% |
| Grader correction and slicing | 20% |
| Reporting and reproducibility | 20% |

> **Two or more open-weight configurations, each measured.** A claim without an interval is a plan, not a result.

#### [capstone#format] Fifteen minutes each: ten to present, five for the challenge

*Format*

- **1 · The plan.** The claim, the minimum effect, the clustering unit; the plan.json commit and its date.
- **2 · The results.** Scores with clustered intervals, the paired verdict, Arabic and English after the grader correction.
- **3 · One choice.** One statistical choice you made, and what the other choice would have cost.

> **Peer feedback.** After each review, everyone writes one strength, one question and one suggestion.

#### [capstone#challenge] The assessor changes one choice; you predict the consequence before re-running

*Inside the fifteen minutes*

1. **Change** drop a cluster of documents, or raise the minimum effect
2. **Prediction** which interval moves, whether the verdict changes, and why
3. **Re-run** analyze.py on the changed input, on screen

> **What earns the marks.** A prediction with a reason, then an honest reading of the re-run, whichever way it went.

#### [capstone#running-order] Who presents when

*Running order*

| # | Presenter | Project |
| --- | --- | --- |
| 1 |  |  |
| 2 |  |  |
| 3 |  |  |
| 4 |  |  |
| 5 |  |  |
| 6 |  |  |
| 7 |  |  |
| 8 |  |  |

#### [capstone#supervised-check] The supervised check: three tasks on paper

*First, AI-off · 30 minutes · 20%*

- **A clustered standard error.** From a short table of per-document sums, by hand, with the design effect it implies.
- **Paired or unpaired.** Two designs described in words: choose the analysis and say which interval is narrower.
- **Read a sizing plan.** Are the questions enough for the stated minimum effect, and what is missing.

> **Calculators allowed; laptops and phones closed.** At least 60% here is needed to pass.

#### [capstone#final-prep] Final prep · 20 minutes

*Before the first presentation*

Rehearse once; open the repository and the re-run command on this screen.

#### [capstone#now-presenting] Review, challenge included

*Now presenting*

#### [capstone#review] What the presentations showed

*Trainer review*

- **Strongest patterns.** What several projects got right.
- **Common gaps.** What most projects would fix next.
- **One surprise.** Something nobody expected.

#### [capstone#what-next] Keep going

*After the course*

- **Your repository stays yours:** keep the plan, the logs and the one command that rebuilds every number
- **The follow-up task, within three weeks:** apply the reporting standard to one workplace or public evaluation, and send the trainer the filled fields and the gaps you found
- **Next in the Academy:** no catalog course follows DS-403; AE-303 builds the graders and harnesses that this course measures

#### [capstone#thanks] Thank you

*SDAIA Academy*

Statistical Evaluation of AI Systems
