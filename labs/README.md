# Statistical Evaluation of AI Systems: labs

## Quick start

- Google Colab: open a notebook from the course page; its first cell clones this repository.
- Locally: clone the repository, then open the notebooks in `labs/` with Jupyter.

| Unit | Session | Notebook |
|---|---|---|
| Day 1 | Session 1 · An evaluation is a sample | [`D1_1_bootstrap_pass_rate.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-403/blob/main/labs/D1_1_bootstrap_pass_rate.ipynb) |
| Day 1 | Session 2 · Clustered items | [`D1_2_compute_standard_errors.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-403/blob/main/labs/D1_2_compute_standard_errors.ipynb) |
| Day 1 | Session 3 · Repeated samples | [`D1_3_split_variance_into.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-403/blob/main/labs/D1_3_split_variance_into.ipynb) |
| Day 1 | Session 4 · Plan before results | [`D1_4_draft_pre_registered.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-403/blob/main/labs/D1_4_draft_pre_registered.ipynb) |
| Day 2 | Session 1 · Paired designs | [`D2_1_compare_paired_unpaired.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-403/blob/main/labs/D2_1_compare_paired_unpaired.ipynb) |
| Day 2 | Session 2 · Many configurations | [`D2_2_rank_six_configurations.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-403/blob/main/labs/D2_2_rank_six_configurations.ipynb) |
| Day 2 | Session 3 · Sizing an evaluation | [`D2_3_size_evaluation_three.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-403/blob/main/labs/D2_3_size_evaluation_three.ipynb) |
| Day 2 | Session 4 · Spending the budget | [`D2_4_choose_more_items.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-403/blob/main/labs/D2_4_choose_more_items.ipynb) |
| Day 3 | Session 1 · Where large-sample intervals fail | [`D3_1_simulate_interval_coverage.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-403/blob/main/labs/D3_1_simulate_interval_coverage.ipynb) |
| Day 3 | Session 2 · Exact and Bayesian intervals | [`D3_2_compute_exact_beta.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-403/blob/main/labs/D3_2_compute_exact_beta.ipynb) |
| Day 3 | Session 3 · Graders against people | [`D3_3_estimate_grader_sensitivity.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-403/blob/main/labs/D3_3_estimate_grader_sensitivity.ipynb) |
| Day 3 | Session 4 · Correcting for grader error | [`D3_4_correct_pass_rate.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-403/blob/main/labs/D3_4_correct_pass_rate.ipynb) |
| Day 4 | Session 1 · Contamination and unequal budgets | [`D4_1_check_comparison_test.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-403/blob/main/labs/D4_1_check_comparison_test.ipynb) |
| Day 4 | Session 2 · Auditing a report | [`D4_2_classify_each_claim.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-403/blob/main/labs/D4_2_classify_each_claim.ipynb) |
| Day 4 | Session 3 · Slicing by language | [`D4_3_report_arabic_english.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-403/blob/main/labs/D4_3_report_arabic_english.ipynb) |
| Day 4 | Session 4 · A reporting standard | [`D4_4_draft_standard_s.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-403/blob/main/labs/D4_4_draft_standard_s.ipynb) |

The notebooks are generated from the percent-format sources in `labs/_src/` by `labs/_tools/py2nb.py` (`uv run python _tools/py2nb.py` from `labs/`), which also writes the solutions to `labs/solutions/`. Edit the sources, not the notebooks.
