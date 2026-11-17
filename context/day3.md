---
course: "Statistical Evaluation of AI Systems"
code: "DS-403"
version: "2027.1.0"
deck: "day3"
day: 3
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/ds-403/slides/day3.html"
---

# Statistical Evaluation of AI Systems

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
