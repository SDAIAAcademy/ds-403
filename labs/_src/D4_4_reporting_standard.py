# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy>=2.0", "pandas>=2.2", "scipy>=1.14", "statsmodels>=0.14", "matplotlib>=3.9"]
# ///

# %% [markdown]
# # Lab 4.4 · The standard and the capstone choice
#
# Day 4 · Session 4 (A reporting standard) · 25 min.
#
# Every finding of the week becomes a required field: an evaluation claim at Bunyan must carry it before it reaches a release decision. You draft the fields, write a validator, test it on a worked example that passes and on Khattab's leaderboard, which fails, and choose the configurations and plan of your capstone.
#
# **Tasks**
# - [ ] Fields from the week's findings · 6 min
# - [ ] A validator for a report · 6 min
# - [ ] The worked example: pass and fail · 5 min
# - [ ] Choose the capstone configurations · 5 min
# - [ ] Commit the capstone plan · 3 min
# - [ ] ✱ Stretch · Turn the standard into a release gate that blocks a report with a missing field

# %%
import os, sys, subprocess
from pathlib import Path

IN_COLAB = "google.colab" in sys.modules
if IN_COLAB:
    REPO_URL = "https://github.com/SDAIAAcademy/ds-403.git"
    if not Path("/content/ds-403").exists():
        subprocess.run(["git", "clone", "-q", REPO_URL, "/content/ds-403"], check=True)
    os.chdir("/content/ds-403/labs")
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "-r", "requirements-colab.txt"], check=True)
else:
    while not Path("_tools").exists() and Path.cwd() != Path.cwd().parent:
        os.chdir("..")  # solutions/ notebooks run from labs/
sys.path.insert(0, os.getcwd())

import json
import pandas as pd
import bunyan as U

REF = U.reference("d4_4")

# %% [markdown]
# ## 1 · Fields from the week's findings
#
# Each field answers a failure seen this week. Complete the list: the finding on the left is given, the field name on the right is yours (snake_case).
#
# ✏️ **Exercise** · Fill `STANDARD`: a dict from field name to the finding it prevents. At least the twelve below.

# %%
def standard_fields() -> dict:
    # BEGIN SOLUTION
    return {
        "plan_commit": "Day 1: metrics and slices chosen after the results (plan committed before the results, with its date)",
        "population": "Day 1: an interval read as covering questions of another kind",
        "items_and_clusters": "Day 1: 600 questions treated as independent when they come from 80 documents",
        "decoding": "Day 1: temperature, samples per question and how they are combined left unstated",
        "estimand": "Days 1 and 4: mean per sample compared with best of five",
        "interval_method": "Days 1 and 3: naive or Wald intervals where clustered or small-sample ones are needed",
        "comparison": "Day 2: unpaired comparisons of systems that answered the same questions",
        "multiplicity": "Day 2: a winner announced from fifteen unadjusted comparisons",
        "minimum_effect_and_verdict": "Days 1 and 2: significance read as importance",
        "grader_calibration": "Day 3: grader error by language unmeasured, and uncorrected rates",
        "budget_parity": "Day 4: unequal tuning, prompt variants tried on the test set, unequal token budgets",
        "overlap_check": "Day 4: test questions in tuning examples, found only after Arabic normalisation",
        "slices": "Day 4: an Arabic weakness hidden in the average",
        "small_sets": "Day 3: 40 of 40 reported as never failing",
        "reproducibility": "All days: logs, code, seed and the command that rebuilds every number",
    }
    # END SOLUTION


# %%
try:
    STANDARD = standard_fields()
except NotImplementedError:
    STANDARD = REF["standard"]
print(len(STANDARD), "required fields")
assert len(STANDARD) >= 12

# %% [markdown]
# ## 2 · A validator for a report
#
# A report is a dict with one entry per field. The validator returns the problems: a missing or empty field; slices without both languages; a comparison that is not paired when the systems share questions; an interval method of "wald" or "naive" for any reported rate; a grader without sensitivity and specificity per language.
#
# ✏️ **Exercise** · Write `validate(report)`.

# %%
def validate(report: dict) -> list[str]:
    problems = []
    # BEGIN SOLUTION
    for field in STANDARD:
        if report.get(field) in (None, "", [], {}):
            problems.append(f"missing: {field}")
    slices = report.get("slices") or {}
    if not {"ar", "en"} <= set(slices):
        problems.append("slices: Arabic and English results with intervals are required")
    comp = str(report.get("comparison", "")).lower()
    if report.get("shared_items") and "paired" not in comp:
        problems.append("comparison: systems answered the same questions, so the comparison must be paired")
    if str(report.get("interval_method", "")).lower() in ("wald", "naive"):
        problems.append("interval_method: use clustered intervals, and Wilson, Jeffreys or Clopper-Pearson for small sets")
    grader = report.get("grader_calibration") or {}
    if not all(k in grader for k in ("sens_ar", "spec_ar", "sens_en", "spec_en")):
        problems.append("grader_calibration: sensitivity and specificity per language are required")
    # END SOLUTION
    return problems


# %% [markdown]
# ## 3 · The worked example: pass and fail
#
# The worked example is the decision of this week: D against C, reported to the standard. Khattab's leaderboard, written as a report dict, should fail.

# %%
worked = {
    "plan_commit": "plan_C_vs_D.json, committed before the results",
    "population": "applicants' questions on the 2026 building regulations, Arabic and English",
    "items_and_clusters": "600 questions from 80 documents; standard errors clustered by document",
    "decoding": "temperature 0.2, 5 samples per question, mean per sample",
    "estimand": "mean grader pass rate per sample",
    "interval_method": "clustered by document; Clopper-Pearson for the 40-item safety set",
    "comparison": "paired difference D minus C over the same questions",
    "shared_items": True,
    "multiplicity": "one primary comparison; six-configuration ranking with Holm",
    "minimum_effect_and_verdict": "3 points; D better, not shown to matter (2.2, 95% CI 0.5 to 3.9)",
    "grader_calibration": {"sens_ar": 0.921, "spec_ar": 0.735, "sens_en": 0.981, "spec_en": 0.911, "labels": 300},
    "budget_parity": "both mean of 5 samples, same prompt budget, max tokens 512",
    "overlap_check": "48 test questions in D's tuning examples, after Arabic normalisation; clean-only result reported",
    "slices": {"ar": "per language with clustered intervals and corrected rates", "en": "same"},
    "small_sets": "safety set: D 40 of 40, unsafe rate below 7.2% at 95%",
    "reproducibility": "labs/ in the course repository; seed 403; uv run",
}
leaderboard = {
    "decoding": "temperature 0.2, five samples",
    "estimand": "pass rate",
    "interval_method": "naive",
    "comparison": "ranking by pass rate",
    "shared_items": True,
    "small_sets": "D 40/40: never unsafe",
}
try:
    ok, bad = validate(worked), validate(leaderboard)
except NotImplementedError:
    ok, bad = [], REF["leaderboard_problems"]
print("worked example:", ok or "passes")
print(f"leaderboard: {len(bad)} problems")
for p in bad:
    print(" -", p)
assert ok == [] and len(bad) >= 10, (ok, bad)

# %% [markdown]
# ## 4 · Choose the capstone configurations
#
# The capstone evaluates **two or more open-weight configurations** that you run yourself (a small open-weight model served on a laptop with llama.cpp or Ollama, on a free notebook GPU with vLLM, or a free hosted endpoint), on Bunyan's 600 questions or a task set of your own with a licence that allows it. Fill your choice.

# %%
capstone = {
    "participant": "",
    "configurations": [
        {"name": "baseline", "model": "a small open-weight instruct model", "prompt": "plain", "serving": "Ollama on a laptop"},
        {"name": "variant", "model": "the same model", "prompt": "retrieved regulation in the prompt", "serving": "Ollama on a laptop"},
    ],
    "task_set": "Bunyan's 600 questions (labs/data/items.csv, labs/data/documents.jsonl)",
    "grader": "exact numeric match plus a model grader; 100 human labels per language for calibration",
    "minimum_effect": 0.03,
    "samples_per_item": 5,
    "temperature": 0.2,
    "primary_comparison": "variant minus baseline, paired, clustered by document",
}
assert len(capstone["configurations"]) >= 2

# %% [markdown]
# ## 5 · Commit the capstone plan
#
# Write the plan; in your capstone repository it is the first commit, before any result exists.

# %%
out = Path("artifacts/D4_4"); out.mkdir(parents=True, exist_ok=True)
(out / "capstone_plan.json").write_text(json.dumps(capstone, indent=2), encoding="utf-8")
(out / "reporting_standard.json").write_text(json.dumps(STANDARD, indent=2), encoding="utf-8")
print("written", out / "capstone_plan.json", "and", out / "reporting_standard.json")

# %% [markdown]
# ## ✱ Stretch · A release gate
#
# Write `gate(report)` that raises an error listing the problems when `validate` finds any, and call it on both reports. In the capstone, run it in the repository's test suite so that the README cannot report a number without its fields.

# %%
def gate(report: dict) -> None:
    problems = validate(report)
    if problems:
        raise ValueError("report blocked: " + "; ".join(problems))


try:
    gate(worked)
    print("worked example: released")
    gate(leaderboard)
except NotImplementedError:
    print("write validate first")
except ValueError as e:
    print(str(e)[:200], "...")

# %% [markdown]
# ## Check yourself
#
# 1. Which field would have stopped the leaderboard's headline claim on its own?
# <details><summary>Answer</summary>budget_parity: it forces both configurations to be scored the same way, which removes most of D's reported lead. overlap_check removes most of the rest.</details>
#
# 2. Why is "slices" a required field and not an optional one?
# <details><summary>Answer</summary>Because an average can hide a weaker language: Watad serves applicants in both, and a release must show both with intervals.</details>
#
# 3. The standard has fifteen fields. Is a two-page standard realistic?
# <details><summary>Answer</summary>Yes: each field is a line with its reason and an example; the worked example fills the second page.</details>
#
# ## Carry forward
#
# `artifacts/D4_4/capstone_plan.json` is the first commit of your capstone repository; the starter is in `labs/capstone/`.
