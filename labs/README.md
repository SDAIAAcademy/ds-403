# Statistical Evaluation of AI Systems: labs

Hands-on notebooks for the SDAIA Academy course **DS-403 Statistical Evaluation of AI Systems (التقييم الإحصائي لأنظمة الذكاء الاصطناعي)**. Every lab works on the synthetic evaluation logs of **Bunyan Building Permits Authority**, whose question assistant **Watad (وتد)** answers applicants on building regulations in Arabic and English. Each lab starts from the supplied data, so none depends on an earlier one.

**No lab calls a model.** The sixteen labs read item-level logs in `data/`, and a laptop processor or a Colab CPU runtime is enough. Only the capstone runs models (see `capstone/README.md`).

## Quick start

**Google Colab.** Open a notebook from the [course page](https://sdaiaacademy.github.io/ds-403/), or directly: `https://colab.research.google.com/github/SDAIAAcademy/ds-403/blob/main/labs/<notebook>.ipynb`. Run the first cell: it clones this repository and installs `requirements-colab.txt`.

**Local.**
```bash
git clone https://github.com/SDAIAAcademy/ds-403
cd ds-403/labs
uv sync                        # creates .venv from pyproject.toml (uv.lock pins every version)
uv run jupyter lab
```
Run `00_setup_check.ipynb` once before Day 1. `uv run prepare_data.py` rebuilds `data/` (committed; the same bytes on every run) and `uv run python _tools/make_reference.py` rebuilds `data/reference/`.

**Quick mode.** Set `DS403_QUICK=1` to cut bootstrap and simulation draws; every solution then runs in well under a minute.

**Windows and long folder paths.** If an import fails with "The filename or extension is too long", keep the virtual environment in a short folder: set `UV_PROJECT_ENVIRONMENT` to a short path (for example a folder at the root of your drive) before `uv sync`.

## Notebooks

| Day | Session | Notebook |
|---|---|---|
| 0 | Setup | [`00_setup_check.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-403/blob/main/labs/00_setup_check.ipynb) |
| 1 | An evaluation is a sample | [`D1_1_bootstrap_pass_rate.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-403/blob/main/labs/D1_1_bootstrap_pass_rate.ipynb) |
| 1 | Clustered items | [`D1_2_compute_standard_errors.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-403/blob/main/labs/D1_2_compute_standard_errors.ipynb) |
| 1 | Repeated samples | [`D1_3_split_variance_into.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-403/blob/main/labs/D1_3_split_variance_into.ipynb) |
| 1 | Plan before results | [`D1_4_draft_pre_registered.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-403/blob/main/labs/D1_4_draft_pre_registered.ipynb) |
| 2 | Paired designs | [`D2_1_compare_paired_unpaired.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-403/blob/main/labs/D2_1_compare_paired_unpaired.ipynb) |
| 2 | Many configurations | [`D2_2_rank_six_configurations.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-403/blob/main/labs/D2_2_rank_six_configurations.ipynb) |
| 2 | Sizing an evaluation | [`D2_3_size_evaluation_three.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-403/blob/main/labs/D2_3_size_evaluation_three.ipynb) |
| 2 | Spending the budget | [`D2_4_choose_more_items.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-403/blob/main/labs/D2_4_choose_more_items.ipynb) |
| 3 | Where large-sample intervals fail | [`D3_1_simulate_interval_coverage.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-403/blob/main/labs/D3_1_simulate_interval_coverage.ipynb) |
| 3 | Exact and Bayesian intervals | [`D3_2_compute_exact_beta.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-403/blob/main/labs/D3_2_compute_exact_beta.ipynb) |
| 3 | Graders against people | [`D3_3_estimate_grader_sensitivity.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-403/blob/main/labs/D3_3_estimate_grader_sensitivity.ipynb) |
| 3 | Correcting for grader error | [`D3_4_correct_pass_rate.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-403/blob/main/labs/D3_4_correct_pass_rate.ipynb) |
| 4 | Contamination and unequal budgets | [`D4_1_check_comparison_test.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-403/blob/main/labs/D4_1_check_comparison_test.ipynb) |
| 4 | Auditing a report | [`D4_2_classify_each_claim.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-403/blob/main/labs/D4_2_classify_each_claim.ipynb) |
| 4 | Slicing by language | [`D4_3_report_arabic_english.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-403/blob/main/labs/D4_3_report_arabic_english.ipynb) |
| 4 | A reporting standard | [`D4_4_reporting_standard.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-403/blob/main/labs/D4_4_reporting_standard.ipynb) |

Exercises are marked **✏️ Exercise** and raise `NotImplementedError` until you fill them in; the cell after each one has a safety net that loads the reference result from `data/reference/`, so the rest of the notebook still runs. Complete reference versions are in `solutions/`. Cells marked **✱ Stretch** are optional. Self-checks print ✅ or ❌.

The notebooks are generated from the percent-format sources in `_src/` by `_tools/py2nb.py` (`uv run python _tools/py2nb.py` from `labs/`), which also writes the solutions. Edit the sources, not the notebooks. A lab that writes a file writes it under `artifacts/`; delete that folder when you are done.

## The data

Synthetic and deterministic (seed 403). No model produced these logs: they are drawn from a stated statistical model, so every planted problem has a known answer.

| File | Contents |
|---|---|
| `data/documents.jsonl` | 80 regulation documents in eight categories, each with its facts in Arabic and English |
| `data/items.csv` | 600 questions (303 Arabic, 297 English), 4 to 9 per document, with the document, category, language and reference answer |
| `data/results.csv` | The model grader's verdict on every answer: 4 configurations × 2 temperatures (0.2, 0.8) × 5 samples × 600 questions |
| `data/results_six.csv` | Six configurations (A to D and two prompt variants of D), one greedy sample per question |
| `data/configs.json` | What each configuration is |
| `data/safety_items.csv`, `data/safety_results.csv` | The 40-item safety set and the four configurations' safe or unsafe answers |
| `data/grader_calibration.csv` | 300 answers (150 per language) labelled by the human panel next to the grader's verdict |
| `data/costs.json` | Unit costs of a new question, a generated answer, a grader call and a human label, and the next evaluation's budget |
| `data/plan_template.json` | The fields of an analysis plan |
| `data/leaderboard_report.md`, `data/leaderboard_claims.csv`, `data/report_settings.csv` | The configuration leaderboard, its eight claims, and how each configuration was scored |
| `data/tuning_examples.csv` | The 120 examples used to tune configuration D's prompt |
| `data/reference/` | Reference results for the safety nets, written by `_tools/make_reference.py` |

The configurations: **A** a small open-weight model with a plain prompt; **B** the same with the retrieved regulation in the prompt; **C** a mid-size open-weight model with a plain prompt; **D** the same with the retrieved regulation; **E** and **F** two prompt variants of D. The names describe size classes, not products.

## Capstone

`capstone/` holds the capstone starter: `run_eval.py` runs two or more open-weight configurations over Bunyan's questions through any OpenAI-compatible endpoint (or a scripted stand-in with `--stub`), `analyze.py` writes the clustered, paired, sizing, language and grader-correction results, and `TEMPLATE_README.md` is the shape of the report. See `capstone/README.md`.

## Trainers

`solutions/answer_key.md` lists every planted problem, the lab that finds it and the numbers each solution prints (left out of a trainee build).

## Helpers: `bunyan.py`

| Helper | What it does |
|---|---|
| `items()`, `results(config, temperature)`, `item_means(config, temperature)`, `load(name)` | Load the data; `item_means` gives one row per question, the mean of its five verdicts |
| `pick(full, quick)`, `QUICK` | Quick mode |
| `reference(name)`, `check(label, got, want, tol)` | Safety nets and self-checks |
| `se_formula`, `clustered_se`, `interval` | Standard errors |
| `wald`, `wilson`, `clopper_pearson`, `beta_interval` | Intervals for a proportion |
| `paired_table(a, b)` | One row per question with both configurations and their difference |
| `rates(calib)`, `corrected_rate(p, sens, spec)` | Grader sensitivity and specificity, and the corrected pass rate |
| `normalize(text)` | Arabic-aware normalisation for overlap checks |
