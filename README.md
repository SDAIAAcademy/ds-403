<!-- academy:title -->
# Statistical Evaluation of AI Systems

التقييم الإحصائي لأنظمة الذكاء الاصطناعي

Data Science Track · SDAIA Academy · DS-403 · Level 400

Treat every evaluation of an AI system as an experiment: report scores with honest intervals, compare systems with paired designs, size evaluations within budget, correct for grader error and audit the claims

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

**Bunyan Building Permits Authority** is a fictional regional authority that issues building and construction permits. Its question assistant, Watad, answers applicants in Arabic and English from 80 regulation documents, and four configurations of it are candidates for release: a small and a mid-size open-weight model, each with and without the retrieved regulation in the prompt.

Every lab works on synthetic item-level logs, generated with a fixed seed by `labs/prepare_data.py`: 600 bilingual questions from 80 documents, five samples per question at temperatures 0.2 and 0.8 for the four configurations, six configurations for ranking, a 40-item safety set, 300 human-labelled verdicts of the model grader, the configuration leaderboard written by the evaluation lead, and the examples used to tune one configuration. No model produced these logs: they are drawn from a stated statistical model so that every planted problem has a known answer. The labs call no model and run on a laptop processor or in Google Colab.

| Person (fictional) | Role in the case |
|---|---|
| Dr. Nadeen Al-Shaya | Director of digital services; decides which configuration is released |
| Khattab Al-Ruhaili | Evaluation lead; wrote the leaderboard audited on Day 4 |
| Sereen Al-Sadiq | Leads the bilingual human-labelling panel |
| Furat Al-Zaabi | Platform engineer; owns serving and the grader budget |
| Rawdha Al-Hujailan | Data protection officer |
| Qamar Al-Saqri | Evaluation statistician: the participant's role |

<!-- academy:labs -->
## Labs

Every lab is a notebook in `labs/`. Open it in Google Colab from the course page, or run it locally with `uv`. Exercises raise `NotImplementedError` until they are done; the reference versions are in `labs/solutions/`.

| | Session | Lab | File |
|---|---|---|---|
| 1.1 | Day 1 · Session 1 | A pass rate with two intervals | [`D1_1_bootstrap_pass_rate.ipynb`](labs/D1_1_bootstrap_pass_rate.ipynb) |
| 1.2 | Day 1 · Session 2 | Clustered by document | [`D1_2_compute_standard_errors.ipynb`](labs/D1_2_compute_standard_errors.ipynb) |
| 1.3 | Day 1 · Session 3 | Item and sampling variance | [`D1_3_split_variance_into.ipynb`](labs/D1_3_split_variance_into.ipynb) |
| 1.4 | Day 1 · Session 4 | A plan before the results | [`D1_4_draft_pre_registered.ipynb`](labs/D1_4_draft_pre_registered.ipynb) |
| 2.1 | Day 2 · Session 1 | Paired against unpaired | [`D2_1_compare_paired_unpaired.ipynb`](labs/D2_1_compare_paired_unpaired.ipynb) |
| 2.2 | Day 2 · Session 2 | Six configurations ranked | [`D2_2_rank_six_configurations.ipynb`](labs/D2_2_rank_six_configurations.ipynb) |
| 2.3 | Day 2 · Session 3 | Sizing for three points | [`D2_3_size_evaluation_three.ipynb`](labs/D2_3_size_evaluation_three.ipynb) |
| 2.4 | Day 2 · Session 4 | Items or samples at fixed cost | [`D2_4_choose_more_items.ipynb`](labs/D2_4_choose_more_items.ipynb) |
| 3.1 | Day 3 · Session 1 | Coverage by simulation | [`D3_1_simulate_interval_coverage.ipynb`](labs/D3_1_simulate_interval_coverage.ipynb) |
| 3.2 | Day 3 · Session 2 | Forty safety questions | [`D3_2_compute_exact_beta.ipynb`](labs/D3_2_compute_exact_beta.ipynb) |
| 3.3 | Day 3 · Session 3 | The grader against people | [`D3_3_estimate_grader_sensitivity.ipynb`](labs/D3_3_estimate_grader_sensitivity.ipynb) |
| 3.4 | Day 3 · Session 4 | Correcting the pass rate | [`D3_4_correct_pass_rate.ipynb`](labs/D3_4_correct_pass_rate.ipynb) |
| 4.1 | Day 4 · Session 1 | Overlap and unequal budgets | [`D4_1_check_comparison_test.ipynb`](labs/D4_1_check_comparison_test.ipynb) |
| 4.2 | Day 4 · Session 2 | Auditing the leaderboard | [`D4_2_classify_each_claim.ipynb`](labs/D4_2_classify_each_claim.ipynb) |
| 4.3 | Day 4 · Session 3 | Arabic and English | [`D4_3_report_arabic_english.ipynb`](labs/D4_3_report_arabic_english.ipynb) |
| 4.4 | Day 4 · Session 4 | The standard and the capstone choice | [`D4_4_reporting_standard.ipynb`](labs/D4_4_reporting_standard.ipynb) |
<!-- /academy:labs -->

## Capstone

A statistical evaluation report on two or more open-weight configurations with a committed plan, clustered and paired analysis, sizing, grader correction and results by language, in a public repository whose README reports measured results; 15-minute review

**Submission:** a public GitHub repository link. The repository holds the analysis plan, committed before any result exists; the item-level logs of two or more open-weight configurations; the analysis (clustered and paired intervals, the sizing, the grader correction and the results by language); and a README that reports the measured results to the course reporting standard, with a verification note on any AI output relied on. Then a 15-minute review in which the assessor drops a cluster or changes the minimum effect and the participant predicts the consequence before re-running.

The starter is in `labs/capstone/`. The rubric: plan 20, uncertainty and comparison 25, sizing 15, grader correction and slicing 20, reporting and reproducibility 20.

**Assessment.** An AI-off supervised check (20%): a clustered standard error by hand, paired or unpaired, reading a sizing plan. The capstone repository (60%). The live review challenging one statistical choice (20%). Passing: 70% overall, with at least 60% on the capstone rubric and on the supervised check.

**AI use.** AI-off for the supervised check and the first standard error, done by hand. In labs an AI tutor may give hints, not finished code. In the capstone AI assistance is allowed, and every output relied on is checked in a verification note.

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
<!-- /academy:sources -->

### National references

- National AI Risk Management Framework (SDAIA), English executive summary: https://sdaia.gov.sa/en/MediaCenter/KnowledgeCenter/ResearchLibrary/ExecutiveSummaryEn.pdf
- SDAIA AI Ethics Principles: https://sdaia.gov.sa/en/SDAIA/about/Documents/ai-principles.pdf
- SDAIA AI Bias Reference Guide: https://sdaia.gov.sa/en/MediaCenter/KnowledgeCenter/ResearchLibrary/EN-AI-BIAS.pdf
- NDMO Data Classification Policy: https://sdaia.gov.sa/en/SDAIA/about/Documents/DataClassificationPolicy.pdf
