# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy>=2.0", "pandas>=2.2", "scipy>=1.14", "statsmodels>=0.14", "matplotlib>=3.9"]
# ///

# %% [markdown]
# # Lab 1.3 · Item and sampling variance
#
# Day 1 · Session 3 (Repeated samples) · 25 min.
#
# Every question was answered five times by each configuration, at temperature 0.2 and again at 0.8. You split the variance of D's score into the part that comes from which questions were written (between items) and the part that comes from the model's sampling (within items), and predict how the standard error falls with more samples per question.
#
# **Tasks**
# - [ ] One row per question: the mean of five samples · 4 min
# - [ ] Within-item variance at each temperature · 6 min
# - [ ] Between-item variance, corrected for sampling · 6 min
# - [ ] The standard error for 1, 5 and 20 samples · 5 min
# - [ ] pass@5 and pass^5 next to the mean · 4 min
# - [ ] ✱ Stretch · Check the predicted standard error for K = 2 by subsampling the logs

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

import numpy as np
import pandas as pd
import bunyan as U

REF = U.reference("d1_3")

# %% [markdown]
# ## 1 · One row per question: the mean of five samples
#
# Make a table with one row per question and one column per sample (1 to 5) for configuration D at a given temperature.

# %%
def sample_matrix(config: str, temperature: float) -> pd.DataFrame:
    r = U.results(config, temperature)
    return r.pivot(index="item_id", columns="sample", values="grader_pass")


m02, m08 = sample_matrix("D", 0.2), sample_matrix("D", 0.8)
print(m02.head())
print("mean of five samples:", round(m02.to_numpy().mean(), 4), "at 0.2;", round(m08.to_numpy().mean(), 4), "at 0.8")

# %% [markdown]
# ## 2 · Within-item variance at each temperature
#
# For one question, the variance of its five verdicts (with `ddof=1`) measures how much the model's answer changes from sample to sample. Average it over questions: $\hat\sigma^2_{within}$.
#
# ## 3 · Between-item variance, corrected for sampling
#
# The variance of the per-question means mixes two parts: $\mathrm{Var}(\bar x_i) = \sigma^2_{between} + \sigma^2_{within}/K$ with $K = 5$. Subtract to get $\hat\sigma^2_{between}$.
#
# ✏️ **Exercise** · Return a dict with `within`, `between` and `var_means` for one sample matrix.

# %%
def variance_parts(m: pd.DataFrame) -> dict:
    # BEGIN SOLUTION
    x = m.to_numpy(dtype=float)
    K = x.shape[1]
    within = x.var(axis=1, ddof=1).mean()
    var_means = x.mean(axis=1).var(ddof=1)
    return {"within": float(within), "between": float(var_means - within / K), "var_means": float(var_means)}
    # END SOLUTION


# %%
parts = {}
for t, m in ((0.2, m02), (0.8, m08)):
    try:
        parts[t] = variance_parts(m)
    except NotImplementedError:
        parts[t] = {k: REF[str(t)][k] for k in ("within", "between", "var_means")}
    U.check(f"within-item variance at {t}", parts[t]["within"], REF[str(t)]["within"], 1e-9)
    U.check(f"between-item variance at {t}", parts[t]["between"], REF[str(t)]["between"], 1e-9)
print(pd.DataFrame(parts).T.round(4))

# %% [markdown]
# **Look at** the two rows. At 0.8 the model's own randomness is a larger share of the variance: more of the noise in the score comes from the draw, not from the questions.
#
# ## 4 · The standard error for 1, 5 and 20 samples
#
# With $n$ questions and $K$ samples each, ignoring clustering: $SE_K = \sqrt{(\sigma^2_{between} + \sigma^2_{within}/K)/n}$.
#
# ✏️ **Exercise** · Return the predicted SE for a given K.

# %%
def se_for_k(between: float, within: float, n: int, K: int) -> float:
    # BEGIN SOLUTION
    return float(np.sqrt((between + within / K) / n))
    # END SOLUTION


# %%
rows = []
for t in (0.2, 0.8):
    for K in (1, 5, 20):
        try:
            s = se_for_k(parts[t]["between"], parts[t]["within"], 600, K)
        except NotImplementedError:
            s = REF[str(t)][f"se_k{K}"]
        rows.append({"temperature": t, "K": K, "se": s})
se_table = pd.DataFrame(rows)
U.check("SE for K = 5 at 0.2", se_table.query("temperature == 0.2 and K == 5").se.iloc[0], REF["0.2"]["se_k5"], 1e-9)
print(se_table.pivot(index="K", columns="temperature", values="se").round(4))

# %% [markdown]
# Going from 1 to 5 samples helps more at 0.8 than at 0.2, and going to 20 helps little at either: the between-item part does not shrink with K. Only more questions shrink it.
#
# ## 5 · pass@5 and pass^5 next to the mean
#
# Three different estimands from the same logs: the **mean** pass rate per sample; **pass@5**, the share of questions answered correctly in at least one of five samples; **pass^5**, the share answered correctly in all five. They answer different questions, and a report must say which one it uses.

# %%
def three_estimands(m: pd.DataFrame) -> dict:
    x = m.to_numpy()
    return {"mean": x.mean(), "pass@5": x.max(axis=1).mean(), "pass^5": x.min(axis=1).mean()}


est = pd.DataFrame({t: three_estimands(m) for t, m in ((0.2, m02), (0.8, m08))})
U.check("pass@5 at 0.2", est.loc["pass@5", 0.2], REF["0.2"]["pass_at_5"], 1e-9)
print(est.round(4))

# %% [markdown]
# ## ✱ Stretch · Check the prediction for K = 2
#
# Keep only samples 1 and 2, compute the per-question mean, and compare its standard error over questions with `se_for_k(..., K=2)`.

# %%
k2 = m08[[1, 2]].mean(axis=1)
predicted = np.sqrt((parts[0.8]["between"] + parts[0.8]["within"] / 2) / 600)
print(f"observed SE with K=2 at 0.8: {U.se_formula(k2):.4f}; predicted {predicted:.4f}")

# %% [markdown]
# ## Check yourself
#
# 1. A colleague runs 20 samples per question to "make the score precise". At temperature 0.2, how much does that buy over 5?
# <details><summary>Answer</summary>Very little: most of the variance is between questions, which more samples do not reduce.</details>
#
# 2. Which estimand would you report for a permit assistant that answers once per applicant?
# <details><summary>Answer</summary>The mean pass rate per sample: an applicant sees one answer. pass@5 describes a user who could ask five times and pick the right answer, which an applicant cannot.</details>
#
# 3. Why is pass^5 lower at 0.8?
# <details><summary>Answer</summary>Sampling varies more at 0.8, so it is less likely that all five answers to a question pass.</details>
#
# ## Carry forward
#
# The variance parts return in Lab 2.4, which reads them from `data/reference/d1_3.json` if this lab was not finished.
