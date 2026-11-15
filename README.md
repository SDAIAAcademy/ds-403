<!-- academy:title -->
# Statistical Evaluation of AI Systems

التقييم الإحصائي لأنظمة الذكاء الاصطناعي

Data Science Track · SDAIA Academy · DS-403 · Level 400

REPLACE: one line under the title: what participants can do after the course

Participants treat every evaluation of an AI system as an experiment with a sampling design. On item-level results from small open-weight models on a fictional permits authority's synthetic bilingual task set, they compute clustered standard errors, compare systems with paired designs, size evaluations within a budget, use exact or Bayesian intervals for small sets, correct for grader error and audit benchmark claims. Graders and harnesses are built in AE-303, not here.

**Format:** Intensive: 4 teaching days of four sessions and a capstone day, with guided pre-work and a tracked follow-up task

**Course page:** https://sdaiaacademy.github.io/ds-403/
<!-- /academy:title -->

## Outcomes

| | Outcomes | Level | Evidence |
|---|---|---|---|
| LO1 | Compute standard errors and intervals for an evaluation score that account for clustered items, repeated samples and small item counts, given item-level results where questions share source documents | Applied | naive, clustered and small-sample intervals with design effects |
| LO2 | Decide whether the difference between two systems is real and large enough to matter, using a paired analysis, given item-level results for two configurations and a minimum effect | Performance | a decision note with the paired difference, its interval and a verdict |
| LO3 | Design an evaluation's size in items, samples per item and grader calls to detect a stated difference within budget, given pilot variances and unit costs | Performance | a sizing plan with power by formula, checked by simulation |
| LO4 | Evaluate the bias that grader error adds to a pass rate and correct it, carrying calibration uncertainty into the interval, given a model grader with 300 human-labelled verdicts in two languages | Performance | corrected and uncorrected pass rates with intervals, by language |
| LO5 | Audit an evaluation claim for statistical validity, contamination risk and unequal tuning or token budgets, given a leaderboard-style report on four systems | Performance | an audit memo classing each claim as supported, unsupported or untestable |
| LO6 | Design a reporting standard for evaluation claims, including results by language and subgroup, given the audit findings and a release process | Performance | a two-page standard with required fields and a worked example |

<!-- academy:units -->
## Units

| Unit | Title | Sessions | Slides |
|---|---|---|---|
| Day 1 | Scores have standard errors | An evaluation is a sample; Clustered items; Repeated samples; Plan before results | [`slides/day1.html`](slides/day1.html) |
| Day 2 | Comparing systems | Paired designs; Many configurations; Sizing an evaluation; Spending the budget | [`slides/day2.html`](slides/day2.html) |
| Day 3 | Small sets and imperfect graders | Where large-sample intervals fail; Exact and Bayesian intervals; Graders against people; Correcting for grader error | [`slides/day3.html`](slides/day3.html) |
| Day 4 | Auditing claims and setting standards | Contamination and unequal budgets; Auditing a report; Slicing by language; A reporting standard | [`slides/day4.html`](slides/day4.html) |
| Capstone | Capstone project presentations |  | [`slides/capstone.html`](slides/capstone.html) |
<!-- /academy:units -->

## Case study

**REPLACE: the name of the fictional organisation every lab works on.** REPLACE: two sentences on the case study and its synthetic data

<!-- academy:labs -->
## Labs

Every lab is a notebook in `labs/`. Open it in Google Colab from the course page, or run it locally with `uv`. Exercises raise `NotImplementedError` until they are done; the reference versions are in `labs/solutions/`.

| | Session | Lab | File |
|---|---|---|---|
| 1.1 | Day 1 · Session 1 | Bootstrap a pass rate and compare it with the formula standard error | [`D1_1_bootstrap_pass_rate.ipynb`](labs/D1_1_bootstrap_pass_rate.ipynb) |
| 1.2 | Day 1 · Session 2 | Compute standard errors clustered by source document and the design effect | [`D1_2_compute_standard_errors.ipynb`](labs/D1_2_compute_standard_errors.ipynb) |
| 1.3 | Day 1 · Session 3 | Split variance into item and sampling parts at two temperatures | [`D1_3_split_variance_into.ipynb`](labs/D1_3_split_variance_into.ipynb) |
| 1.4 | Day 1 · Session 4 | Draft a pre-registered plan comparing two configurations | [`D1_4_draft_pre_registered.ipynb`](labs/D1_4_draft_pre_registered.ipynb) |
| 2.1 | Day 2 · Session 1 | Compare paired and unpaired analyses and explain the widths | [`D2_1_compare_paired_unpaired.ipynb`](labs/D2_1_compare_paired_unpaired.ipynb) |
| 2.2 | Day 2 · Session 2 | Rank six configurations with adjusted intervals | [`D2_2_rank_six_configurations.ipynb`](labs/D2_2_rank_six_configurations.ipynb) |
| 2.3 | Day 2 · Session 3 | Size an evaluation for a three-point difference; check by simulation | [`D2_3_size_evaluation_three.ipynb`](labs/D2_3_size_evaluation_three.ipynb) |
| 2.4 | Day 2 · Session 4 | Choose more items or more samples per item at fixed cost | [`D2_4_choose_more_items.ipynb`](labs/D2_4_choose_more_items.ipynb) |
| 3.1 | Day 3 · Session 1 | Simulate interval coverage for 20 to 200 items near 0 or 1 | [`D3_1_simulate_interval_coverage.ipynb`](labs/D3_1_simulate_interval_coverage.ipynb) |
| 3.2 | Day 3 · Session 2 | Compute exact and beta-posterior intervals for a 40-item safety set | [`D3_2_compute_exact_beta.ipynb`](labs/D3_2_compute_exact_beta.ipynb) |
| 3.3 | Day 3 · Session 3 | Estimate grader sensitivity and specificity by language | [`D3_3_estimate_grader_sensitivity.ipynb`](labs/D3_3_estimate_grader_sensitivity.ipynb) |
| 3.4 | Day 3 · Session 4 | Correct a pass rate, carrying calibration uncertainty into its interval | [`D3_4_correct_pass_rate.ipynb`](labs/D3_4_correct_pass_rate.ipynb) |
| 4.1 | Day 4 · Session 1 | Check a comparison for test-item overlap and unequal tuning | [`D4_1_check_comparison_test.ipynb`](labs/D4_1_check_comparison_test.ipynb) |
| 4.2 | Day 4 · Session 2 | Classify each claim as supported, unsupported or untestable | [`D4_2_classify_each_claim.ipynb`](labs/D4_2_classify_each_claim.ipynb) |
| 4.3 | Day 4 · Session 3 | Report Arabic and English results with intervals and test the gap | [`D4_3_report_arabic_english.ipynb`](labs/D4_3_report_arabic_english.ipynb) |
| 4.4 | Day 4 · Session 4 | Draft the standard's required fields and choose the capstone systems | [`D4_4_draft_standard_s.ipynb`](labs/D4_4_draft_standard_s.ipynb) |
<!-- /academy:labs -->

## Capstone

A statistical evaluation report on two or more open-weight configurations with a committed plan, clustered and paired analysis, sizing, grader correction and results by language, in a public repository whose README reports measured results; 15-minute review

**Submission:** REPLACE: what participants submit and how: a public repository link, or a shared folder for a course without code

## Prerequisites

- DS-302 Online Experiments and A/B Testing
- DS-305 Uncertainty, Interpretability and Model Validation
- Computes bootstrap intervals and paired tests in code
- Has logged a language model's outputs through an API

<!-- academy:tools -->
## Tools

Each line is a capability; the examples are interchangeable.

- **Open-weight model serving (capstone only):** llama.cpp or Ollama on a laptop, vLLM on a free notebook GPU
- **Evaluation harness with item-level logs:** Inspect AI, lm-evaluation-harness, promptfoo
- **Statistics and simulation:** SciPy, statsmodels, PyMC
- **Analysis environment:** Python through uv with Jupyter or marimo, Quarto
<!-- /academy:tools -->

<!-- academy:sources -->
## Sources

- REPLACE: every source the course cites, with its address, in course.json under "sources"; this list is written from there
<!-- /academy:sources -->

### National references

- National AI Risk Management Framework: REPLACE: the address of the official text
- SDAIA AI Ethics Principles: REPLACE: the address of the official text
- SDAIA AI Bias Reference Guide: REPLACE: the address of the official text
- NDMO Data Classification Policy: REPLACE: the address of the official text
