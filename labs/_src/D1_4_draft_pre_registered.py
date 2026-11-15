# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy>=2.0", "pandas>=2.2", "scipy>=1.14", "statsmodels>=0.14", "matplotlib>=3.9"]
# ///

# %% [markdown]
# # Lab 1.4 · A plan before the results
#
# Day 1 · Session 4 (Plan before results) · 25 min.
#
# Dr. Nadeen Al-Shaya, director of digital services, will choose between configurations C and D for release. Before anyone looks at the comparison, you write the analysis plan, check it against the required fields, and measure by simulation what happens when the metric is chosen after the results.
#
# **Tasks**
# - [ ] Read the plan template and the required fields · 3 min
# - [ ] Fill the plan for C against D · 8 min
# - [ ] Validate it: missing or vague fields · 4 min
# - [ ] Simulate four metrics chosen after the fact · 7 min
# - [ ] Commit the plan to a file with its date · 3 min
# - [ ] ✱ Stretch · Add a second, secondary comparison and decide how it is adjusted

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
import datetime as dt
import numpy as np
import pandas as pd
import bunyan as U

REF = U.reference("d1_4")

# %% [markdown]
# ## 1 · The plan template and the required fields
#
# `data/plan_template.json` holds the fields of an evaluation plan. The validator below needs every one of `REQUIRED` filled. A plan written after the results is a description, not a plan.

# %%
template = json.loads((U.DATA / "plan_template.json").read_text(encoding="utf-8"))
REQUIRED = ["title", "owner", "date_committed", "question", "systems", "population", "items", "unit_of_analysis",
            "primary_metric", "grader", "samples_per_item", "temperature", "clustering", "comparison",
            "minimum_effect", "alpha", "power", "decision_rule", "slices", "exclusions"]
print(json.dumps(template, indent=1)[:600])

# %% [markdown]
# ## 2 · Fill the plan for C against D
#
# Fix what Day 1 taught: the score is the mean over five samples at temperature 0.2; questions are clustered by document; the comparison is paired; the minimum effect is three points; the decision rule says what happens for each outcome; the slices include language.
#
# ✏️ **Exercise** · Fill `plan`. Keep `date_committed` as today's date.

# %%
def fill_plan(template: dict) -> dict:
    plan = dict(template)
    # BEGIN SOLUTION
    plan.update({
    "title": "Watad release: configuration D against configuration C",
    "owner": "Qamar Al-Saqri, evaluation statistician",
    "date_committed": dt.date.today().isoformat(),
    "question": "Is D's pass rate at least three points higher than C's on the regulation task set?",
    "systems": ["C", "D"],
    "population": "Questions applicants ask about the authority's building regulations, Arabic and English",
    "items": "The 600 questions of the regulation task set, 80 documents",
    "unit_of_analysis": "question",
    "primary_metric": "mean grader pass rate per sample",
    "grader": "the model grader; corrected with the human-labelled verdicts as a secondary analysis",
    "samples_per_item": 5,
    "temperature": 0.2,
    "clustering": "standard errors clustered by source document",
    "comparison": "paired difference D minus C over the same questions",
    "minimum_effect": 0.03,
    "alpha": 0.05,
    "power": 0.8,
    "decision_rule": "Release D if the lower end of the 95% interval of D minus C is above 0; call it worth the switch only if the interval also includes or exceeds the minimum effect of 0.03; otherwise keep C",
    "slices": ["language", "category"],
    "exclusions": "none; questions that fail to run are scored as failures",
    "secondary_metrics": ["pass rate corrected for grader error, by language", "safety set, 40 items"],
    })
    # END SOLUTION
    return plan


# %%
try:
    plan = fill_plan(template)
except NotImplementedError:
    plan = json.loads((U.DATA / "reference" / "plan_C_vs_D.json").read_text(encoding="utf-8"))
print(json.dumps(plan, indent=1, ensure_ascii=False)[:400])

# %% [markdown]
# ## 3 · Validate it
#
# ✏️ **Exercise** · Return a list of problems: each required field that is empty, a minimum effect that is not a positive number, an alpha outside (0, 0.1], clustering that does not mention documents, and slices without language.

# %%
def validate_plan(p: dict) -> list[str]:
    problems = []
    # BEGIN SOLUTION
    for k in REQUIRED:
        if p.get(k) in (None, "", [], {}):
            problems.append(f"missing: {k}")
    me = p.get("minimum_effect")
    if not isinstance(me, (int, float)) or me <= 0:
        problems.append("minimum_effect must be a positive number")
    a = p.get("alpha")
    if not isinstance(a, (int, float)) or not 0 < a <= 0.1:
        problems.append("alpha must be in (0, 0.1]")
    if "document" not in str(p.get("clustering", "")).lower():
        problems.append("clustering must name the source documents")
    if "language" not in [str(s).lower() for s in p.get("slices", [])]:
        problems.append("slices must include language")
    # END SOLUTION
    return problems


# %%
try:
    found = validate_plan(template)
    mine = validate_plan(plan)
except NotImplementedError:
    found, mine = REF["template_problems"], []
assert len(found) == REF["n_template_problems"], found
print("the empty template has", len(found), "problems; yours has", len(mine), ":", mine)
if mine:
    print("Fix your plan, or load the reference plan: data/reference/plan_C_vs_D.json")

# %% [markdown]
# ## 4 · Simulate four metrics chosen after the fact
#
# Two configurations that are **identical**: every question has the same pass probability under both (taken from D's per-question means). The analyst computes four metrics (the mean of five samples, the first sample only, pass@5, the Arabic questions only), tests each at 5%, and reports whichever is significant. How often does that find a "difference" that is not there?
#
# ✏️ **Exercise** · Complete `one_null_study`: return the four p-values of paired z tests of B minus A.

# %%
from scipy import stats

probs = U.item_means("D", 0.2).set_index("item_id").score.clip(0.02, 0.98).to_numpy()
is_ar = (U.items().set_index("item_id").language == "ar").to_numpy()


def paired_p(a: np.ndarray, b: np.ndarray) -> float:
    d = b - a
    se = d.std(ddof=1) / np.sqrt(len(d))
    return float(2 * stats.norm.sf(abs(d.mean() / se))) if se > 0 else 1.0


def one_null_study(rng: np.random.Generator) -> list[float]:
    a = (rng.random((len(probs), 5)) < probs[:, None]).astype(float)
    b = (rng.random((len(probs), 5)) < probs[:, None]).astype(float)
    # BEGIN SOLUTION
    return [paired_p(a.mean(1), b.mean(1)), paired_p(a[:, 0], b[:, 0]),
            paired_p(a.max(1), b.max(1)), paired_p(a[is_ar].mean(1), b[is_ar].mean(1))]
    # END SOLUTION


# %%
S = U.pick(2000, 400)
rng = np.random.default_rng(403)
try:
    ps = np.array([one_null_study(rng) for _ in range(S)])
    single, any4 = (ps[:, 0] < 0.05).mean(), (ps < 0.05).any(axis=1).mean()
except NotImplementedError:
    single, any4 = REF["false_win_single"], REF["false_win_any"]
print(f"false wins with the planned metric: {single:.3f}; with the best of four chosen after: {any4:.3f}")
assert single < 0.08 and any4 > 0.09, (single, any4)

# %% [markdown]
# **Look at** the ratio: with one planned metric about one study in twenty finds a false difference; choosing the best of four after the results roughly doubles or triples that. The plan is what keeps the 5% honest.
#
# ## 5 · Commit the plan
#
# Write the plan to a file with its date. In the capstone this file is committed to git **before** the results exist, and the commit's date is the evidence.

# %%
out = Path("artifacts/D1_4"); out.mkdir(parents=True, exist_ok=True)
final = plan if not mine else json.loads((U.DATA / "reference" / "plan_C_vs_D.json").read_text(encoding="utf-8"))
(out / "plan_C_vs_D.json").write_text(json.dumps(final, indent=2, ensure_ascii=False), encoding="utf-8")
print("written", out / "plan_C_vs_D.json")

# %% [markdown]
# ## ✱ Stretch · A secondary comparison
#
# Add "D against C in Arabic only" as a secondary comparison. Decide: is it adjusted for multiplicity (Holm over two tests) or reported as exploratory? Write the choice in `secondary_metrics`.
#
# ## Check yourself
#
# 1. The results show D ahead on pass@5 but not on the mean. What does the plan say to report?
# <details><summary>Answer</summary>The planned primary metric, the mean pass rate per sample, and its verdict. pass@5 may appear as a labelled secondary result, not as the headline.</details>
#
# 2. Why is the minimum effect in the plan and not chosen after seeing the interval?
# <details><summary>Answer</summary>Chosen afterwards it can be set just below whatever difference was observed; fixed before, it states what difference matters to the decision.</details>
#
# 3. Is a plan that changes during the analysis worthless?
# <details><summary>Answer</summary>No: a dated amendment with its reason, reported next to the original, keeps the reader informed. Silent changes are the problem.</details>
#
# ## Carry forward
#
# Lab 2.1 compares C and D under this plan. A reference plan is in `data/reference/plan_C_vs_D.json`.
