---
course: "Statistical Evaluation of AI Systems"
code: "DS-403"
version: "2027.1.0"
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/ds-403/index.html"
---

# Statistical Evaluation of AI Systems

التقييم الإحصائي لأنظمة الذكاء الاصطناعي

Data Science Track · 4 teaching days + capstone day · 26 hours · Level 400

Treat every evaluation of an AI system as an experiment: report scores with honest intervals, compare systems with paired designs, size evaluations within budget, correct for grader error and audit the claims

Participants treat every evaluation of an AI system as an experiment with a sampling design. On item-level results from small open-weight models on a fictional permits authority's synthetic bilingual task set, they compute clustered standard errors, compare systems with paired designs, size evaluations within a budget, use exact or Bayesian intervals for small sets, correct for grader error and audit benchmark claims. Graders and harnesses are built in AE-303, not here.

**Who it is for:** Specialists. Data scientists who have completed the level 300 core or can show equivalent work: a defended analysis with a validated model or a causal estimate that they can explain.

**Format:** Intensive: 4 teaching days of four sessions and a capstone day, with guided pre-work and a tracked follow-up task

## The case study

**Bunyan Building Permits Authority.** Bunyan Building Permits Authority is a fictional regional authority that issues building and construction permits. Its question assistant, Watad, answers applicants in Arabic and English from 80 regulation documents, and four configurations of it (a small and a mid-size open-weight model, each with and without the retrieved regulation) are candidates for release. Participants work on synthetic item-level logs: 600 bilingual questions from 80 documents, five samples per question at two temperatures for four configurations, six configurations for ranking, a 40-item safety set, 300 human-labelled grader verdicts, the configuration leaderboard written by the evaluation lead, and the examples used to tune one configuration. They compute clustered and small-sample intervals, compare configurations with paired designs, size the next evaluation within budget, correct pass rates for the grader's error by language, audit the leaderboard's claims and write a reporting standard. All data is synthetic and generated with a fixed seed; no model produced the logs.

## The course

### Day 1: Scores have standard errors

Slides: https://sdaiaacademy.github.io/ds-403/slides/day1.md

- **Session 1: An evaluation is a sample**
  - Explain what population an evaluation score estimates
  - Compute the formula standard error of a pass rate
  - Bootstrap a pass rate and compare the two intervals
  - [Lab 1.1: A pass rate with two intervals (25 min)](https://sdaiaacademy.github.io/ds-403/labs/D1_1_bootstrap_pass_rate.ipynb)
- **Session 2: Clustered items**
  - Explain why items from one source document are not independent
  - Compute a standard error clustered by document
  - Report the design effect and the effective number of items
  - [Lab 1.2: Clustered by document (25 min)](https://sdaiaacademy.github.io/ds-403/labs/D1_2_compute_standard_errors.ipynb)
- **Session 3: Repeated samples**
  - Split the variance of a score into item and sampling parts
  - Predict the standard error for K samples per item
  - Distinguish the mean pass rate, pass@k and pass^k
  - [Lab 1.3: Item and sampling variance (25 min)](https://sdaiaacademy.github.io/ds-403/labs/D1_3_split_variance_into.ipynb)
- **Session 4: Plan before results**
  - Explain how choices made after the results inflate false wins
  - Write an analysis plan for a comparison of two configurations
  - State a minimum effect and a decision rule in advance
  - [Lab 1.4: A plan before the results (25 min)](https://sdaiaacademy.github.io/ds-403/labs/D1_4_draft_pre_registered.ipynb)

### Day 2: Comparing systems

Slides: https://sdaiaacademy.github.io/ds-403/slides/day2.md

- **Session 1: Paired designs**
  - Compute a paired difference with a clustered standard error
  - Explain the width of paired and unpaired intervals from the correlation
  - Write a verdict against a minimum effect
  - [Lab 2.1: Paired against unpaired (25 min)](https://sdaiaacademy.github.io/ds-403/labs/D2_1_compare_paired_unpaired.ipynb)
- **Session 2: Many configurations**
  - Explain why fifteen comparisons need adjustment
  - Compute Bonferroni and Holm adjusted paired intervals
  - Report a ranking with the set of plausible ranks
  - [Lab 2.2: Six configurations ranked (25 min)](https://sdaiaacademy.github.io/ds-403/labs/D2_2_rank_six_configurations.ipynb)
- **Session 3: Sizing an evaluation**
  - Derive the number of items from the paired variance, the design effect and the minimum effect
  - Check a sizing formula by simulation over documents
  - Explain what the pilot can and cannot tell
  - [Lab 2.3: Sizing for three points (25 min)](https://sdaiaacademy.github.io/ds-403/labs/D2_3_size_evaluation_three.ipynb)
- **Session 4: Spending the budget**
  - Write the variance of a score as a function of items and samples
  - Find the number of samples per item that minimises variance at fixed cost
  - Include grader calls and human labels in an evaluation budget
  - [Lab 2.4: Items or samples at fixed cost (25 min)](https://sdaiaacademy.github.io/ds-403/labs/D2_4_choose_more_items.ipynb)

### Day 3: Small sets and imperfect graders

Slides: https://sdaiaacademy.github.io/ds-403/slides/day3.md

- **Session 1: Where large-sample intervals fail**
  - Define the coverage of an interval
  - Measure the coverage of four intervals by simulation
  - Choose an interval for a small set near 0 or 1
  - [Lab 3.1: Coverage by simulation (25 min)](https://sdaiaacademy.github.io/ds-403/labs/D3_1_simulate_interval_coverage.ipynb)
- **Session 2: Exact and Bayesian intervals**
  - Compute a Clopper-Pearson interval for a small set
  - Compute a Beta posterior interval and state its prior
  - Report 40 out of 40 without claiming perfection
  - [Lab 3.2: Forty safety questions (25 min)](https://sdaiaacademy.github.io/ds-403/labs/D3_2_compute_exact_beta.ipynb)
- **Session 3: Graders against people**
  - Estimate a grader's sensitivity and specificity from human labels
  - Compare the grader's errors by language with intervals
  - Decide which logs may go to a hosted grader under the data classification
  - [Lab 3.3: The grader against people (25 min)](https://sdaiaacademy.github.io/ds-403/labs/D3_3_estimate_grader_sensitivity.ipynb)
- **Session 4: Correcting for grader error**
  - Correct an observed pass rate with sensitivity and specificity
  - Carry calibration uncertainty into the interval by bootstrap
  - Report corrected and uncorrected rates by language
  - [Lab 3.4: Correcting the pass rate (25 min)](https://sdaiaacademy.github.io/ds-403/labs/D3_4_correct_pass_rate.ipynb)

### Day 4: Auditing claims and setting standards

Slides: https://sdaiaacademy.github.io/ds-403/slides/day4.md

- **Session 1: Contamination and unequal budgets**
  - Detect overlap between test items and tuning examples, including Arabic spelling variants
  - Measure how overlap changes a score
  - Recompute a comparison at equal budgets
  - [Lab 4.1: Overlap and unequal budgets (25 min)](https://sdaiaacademy.github.io/ds-403/labs/D4_1_check_comparison_test.ipynb)
- **Session 2: Auditing a report**
  - Classify an evaluation claim by the evidence it needs
  - Re-analyse a claim from item-level logs
  - Write an audit memo a decision owner can act on
  - [Lab 4.2: Auditing the leaderboard (25 min)](https://sdaiaacademy.github.io/ds-403/labs/D4_2_classify_each_claim.ipynb)
- **Session 3: Slicing by language**
  - Report a score by language with clustered intervals
  - Test the gap between languages using documents with questions in both
  - Show how grader correction changes a gap
  - [Lab 4.3: Arabic and English (25 min)](https://sdaiaacademy.github.io/ds-403/labs/D4_3_report_arabic_english.ipynb)
- **Session 4: A reporting standard**
  - List the required fields of an evaluation report
  - Validate a worked example against the standard
  - Choose the configurations and the plan of the capstone
  - [Lab 4.4: The standard and the capstone choice (25 min)](https://sdaiaacademy.github.io/ds-403/labs/D4_4_reporting_standard.ipynb)

### Capstone: Capstone project presentations

Slides: https://sdaiaacademy.github.io/ds-403/slides/capstone.md

## Capstone

A statistical evaluation report on two or more open-weight configurations with a committed plan, clustered and paired analysis, sizing, grader correction and results by language, in a public repository whose README reports measured results; 15-minute review

**What you submit:** A public GitHub repository link. The repository holds the analysis plan, committed before any result exists; the item-level logs of two or more open-weight configurations; the analysis (clustered and paired intervals, the sizing, the grader correction and the results by language); and a README that reports the measured results to the course reporting standard, with a verification note on any AI output relied on. Then a 15-minute review in which the assessor drops a cluster or changes the minimum effect and the participant predicts the consequence before re-running.

**Rubric:**

- Plan: 20%
- Uncertainty and comparison: 25%
- Sizing: 15%
- Grader correction and slicing: 20%
- Reporting and reproducibility: 20%

## Outcomes

- **LO1** Compute standard errors and intervals for an evaluation score that account for clustered items, repeated samples and small item counts, given item-level results where questions share source documents (Applied) Evidence: naive, clustered and small-sample intervals with design effects
- **LO2** Decide whether the difference between two systems is real and large enough to matter, using a paired analysis, given item-level results for two configurations and a minimum effect (Performance) Evidence: a decision note with the paired difference, its interval and a verdict
- **LO3** Design an evaluation's size in items, samples per item and grader calls to detect a stated difference within budget, given pilot variances and unit costs (Performance) Evidence: a sizing plan with power by formula, checked by simulation
- **LO4** Evaluate the bias that grader error adds to a pass rate and correct it, carrying calibration uncertainty into the interval, given a model grader with 300 human-labelled verdicts in two languages (Performance) Evidence: corrected and uncorrected pass rates with intervals, by language
- **LO5** Audit an evaluation claim for statistical validity, contamination risk and unequal tuning or token budgets, given a leaderboard-style report on four systems (Performance) Evidence: an audit memo classing each claim as supported, unsupported or untestable
- **LO6** Design a reporting standard for evaluation claims, including results by language and subgroup, given the audit findings and a release process (Performance) Evidence: a two-page standard with required fields and a worked example

## Tools

- **Open-weight model serving (capstone only):** llama.cpp or Ollama on a laptop, vLLM on a free notebook GPU
- **Evaluation harness with item-level logs:** Inspect AI, lm-evaluation-harness, promptfoo
- **Statistics and simulation:** SciPy, statsmodels, PyMC
- **Analysis environment:** Python through uv with Jupyter or marimo, Quarto

## Prerequisites

- DS-302 Online Experiments and A/B Testing
- DS-305 Uncertainty, Interpretability and Model Validation
- Computes bootstrap intervals and paired tests in code
- Has logged a language model's outputs through an API
- Setup: a laptop CPU with uv, or Google Colab. The sixteen labs read supplied item-level logs and call no model. Pre-work: three hours on the bootstrap and power by simulation, with an entry quiz; see labs/README.md.

## Sources

### Statistics of evaluations

- [Evan Miller: Adding Error Bars to Evals: A Statistical Approach to Language Model Evaluations (arXiv 2411.00640)](https://arxiv.org/abs/2411.00640)
- [Anthropic: A statistical approach to model evaluations](https://www.anthropic.com/research/statistical-approach-to-model-evals)
- [Bowyer, Aitchison and Ivanova: Position: Don't Use the CLT in LLM Evals With Fewer Than a Few Hundred Datapoints (arXiv 2503.01747)](https://arxiv.org/abs/2503.01747)
- [Brown, Cai and DasGupta: Interval Estimation for a Binomial Proportion, Statistical Science 16(2), 2001](https://doi.org/10.1214/ss/1009213286)

### Graders, claims and contamination

- [How to Correctly Report LLM-as-a-Judge Evaluations (arXiv 2511.21140)](https://arxiv.org/abs/2511.21140)
- [Angelopoulos and others: Prediction-Powered Inference (arXiv 2301.09633)](https://arxiv.org/abs/2301.09633)
- [Benchmark Data Contamination of Large Language Models: A Survey (arXiv 2406.04244)](https://arxiv.org/abs/2406.04244)
- [The Leaderboard Illusion (arXiv 2504.20879)](https://arxiv.org/abs/2504.20879)

### Tools

- [Inspect, an evaluation framework](https://inspect.aisi.org.uk/)
- [EleutherAI lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness)
- [promptfoo documentation](https://www.promptfoo.dev/docs/intro/)
- [SciPy: scipy.stats.binomtest](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.binomtest.html)
- [statsmodels: proportion_confint](https://www.statsmodels.org/stable/generated/statsmodels.stats.proportion.proportion_confint.html)
- [uv](https://docs.astral.sh/uv/)
- [marimo](https://marimo.io/)
- [Quarto](https://quarto.org/)
- [llama.cpp](https://github.com/ggml-org/llama.cpp)
- [Ollama](https://ollama.com/)

### National references

- [National AI Risk Management Framework, English executive summary (SDAIA)](https://sdaia.gov.sa/en/MediaCenter/KnowledgeCenter/ResearchLibrary/ExecutiveSummaryEn.pdf)
- [AI Ethics Principles (SDAIA)](https://sdaia.gov.sa/en/SDAIA/about/Documents/ai-principles.pdf)
- [AI Bias Reference Guide (SDAIA)](https://sdaia.gov.sa/en/MediaCenter/KnowledgeCenter/ResearchLibrary/EN-AI-BIAS.pdf)
- [Data Classification Policy (National Data Management Office, SDAIA)](https://sdaia.gov.sa/en/SDAIA/about/Documents/DataClassificationPolicy.pdf)

---

SDAIA Academy · Data Science Track · Statistical Evaluation of AI Systems

Course version 2027.1.0 · engine 1.0.0 · built 2026-11-15 · commit d0b0715
