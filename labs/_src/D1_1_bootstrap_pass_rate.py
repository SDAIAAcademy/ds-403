# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy>=2.0", "pandas>=2.2", "scipy>=1.14", "statsmodels>=0.14", "matplotlib>=3.9"]
# ///

# %% [markdown]
# # Lab 1.1 · A pass rate with two intervals
#
# Day 1 · Session 1 (An evaluation is a sample) · 25 min.
#
# Watad, the question assistant of **Bunyan Building Permits Authority**, answered 600 regulation questions. You compute configuration D's pass rate, put a 95% interval on it twice (the formula and the bootstrap), and write the score the way a reader should see it. The logs are synthetic; no model call is made.
#
# **Tasks**
# - [ ] Load the logs and compute the pass rate of one sample · 4 min
# - [ ] The formula standard error and a 95% interval · 5 min
# - [ ] A bootstrap over questions · 8 min
# - [ ] Compare the two intervals and the two distributions · 5 min
# - [ ] Write the score as a reader should see it · 3 min
# - [ ] ✱ Stretch · Bootstrap over documents and say why the interval widens

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
import matplotlib.pyplot as plt
import bunyan as U

REF = U.reference("d1_1")
print("quick mode:", U.QUICK)

# %% [markdown]
# ## 1 · Load the logs and compute the pass rate of one sample
#
# `data/results.csv` has one row per question, configuration, temperature and sample. `grader_pass` is the model grader's verdict (1 = pass). Keep configuration D at temperature 0.2 and its **first** sample only: one verdict per question.
#
# ✏️ **Exercise** · Return the 0/1 verdicts of D's first sample at temperature 0.2, as a NumPy array in question order.

# %%
results = U.results()
print(results.head())


def first_sample_verdicts(results: pd.DataFrame) -> np.ndarray:
    # BEGIN SOLUTION
    r = results[(results.config == "D") & np.isclose(results.temperature, 0.2) & (results["sample"] == 1)]
    return r.sort_values("item_id").grader_pass.to_numpy()
    # END SOLUTION


# %%
# Check, with a safety net: the cells below still run when the exercise is not done yet
try:
    x = first_sample_verdicts(results)
except NotImplementedError:
    x = np.array(REF["verdicts"])
p, n = x.mean(), len(x)
U.check("600 questions", n, 600)
U.check("pass rate of D, first sample", p, REF["p"], 1e-9)
print(f"pass rate {p:.4f} on {n} questions")

# %% [markdown]
# ## 2 · The formula standard error and a 95% interval
#
# Each question is one draw from the population of questions the authority could have written. The pass rate is the mean of 0/1 values, so its standard error is $\sqrt{p(1-p)/n}$ and a 95% interval is $p \pm 1.96\,SE$.
#
# ✏️ **Exercise** · Return `(se, lo, hi)`.

# %%
def formula_interval(x: np.ndarray):
    # BEGIN SOLUTION
    p, n = x.mean(), len(x)
    se = np.sqrt(p * (1 - p) / n)
    return float(se), float(p - 1.96 * se), float(p + 1.96 * se)
    # END SOLUTION


# %%
try:
    se, lo, hi = formula_interval(x)
except NotImplementedError:
    se, lo, hi = REF["se"], REF["lo"], REF["hi"]
U.check("formula standard error", se, REF["se"], 1e-6)
print(f"SE {se:.4f}  ->  95% interval {lo:.3f} to {hi:.3f}")

# %% [markdown]
# ## 3 · A bootstrap over questions
#
# Resample the 600 questions with replacement, recompute the pass rate, repeat. The spread of those rates estimates the standard error without a formula; the 2.5th and 97.5th percentiles give a percentile interval.
#
# ✏️ **Exercise** · Return an array of `B` bootstrap pass rates. Use the generator `rng` you are given.

# %%
B = U.pick(5000, 1000)


def bootstrap_rates(x: np.ndarray, B: int, rng: np.random.Generator) -> np.ndarray:
    # BEGIN SOLUTION
    idx = rng.integers(0, len(x), size=(B, len(x)))
    return x[idx].mean(axis=1)
    # END SOLUTION


# %%
try:
    boot = bootstrap_rates(x, B, np.random.default_rng(403))
except NotImplementedError:
    boot = np.random.default_rng(403).choice(x, size=(B, len(x))).mean(axis=1)
boot_se = boot.std(ddof=1)
b_lo, b_hi = np.percentile(boot, [2.5, 97.5])
U.check("bootstrap SE close to the formula", boot_se, se, 0.002)
print(f"bootstrap SE {boot_se:.4f}; percentile interval {b_lo:.3f} to {b_hi:.3f} ({B} draws)")

# %% [markdown]
# ## 4 · Compare the two intervals and the two distributions
#
# **Look at** the histogram: the bootstrap rates and the normal curve the formula assumes. With 600 questions and a rate far from 0 or 1 they agree. Day 3 shows where they stop agreeing.

# %%
fig, ax = plt.subplots(figsize=(7, 3.2))
ax.hist(boot, bins=40, density=True, color="#2a9d8f", alpha=0.7, label="bootstrap pass rates")
g = np.linspace(boot.min(), boot.max(), 200)
ax.plot(g, np.exp(-0.5 * ((g - p) / se) ** 2) / (se * np.sqrt(2 * np.pi)), color="#e76f51", label="normal, formula SE")
ax.axvline(lo, color="#e76f51", ls=":"); ax.axvline(hi, color="#e76f51", ls=":")
ax.set_xlabel("pass rate of D"); ax.legend(frameon=False)
U.show(fig)
print(pd.DataFrame({"method": ["formula", "bootstrap"], "SE": [se, boot_se],
                    "low": [lo, b_lo], "high": [hi, b_hi]}).round(4).to_string(index=False))

# %% [markdown]
# ## 5 · Write the score as a reader should see it
#
# A score without its interval invites readers to treat a one-point difference as real. Write one line: the configuration, the rate with its interval in percent to one decimal, the number of questions, the samples per question and the temperature.
#
# ✏️ **Exercise** · Return that line, in the form `D: 70.0% (95% CI 66.0 to 74.0), 600 questions, 1 sample each, temperature 0.2` with your numbers.

# %%
def report_line(name: str, p: float, lo: float, hi: float, n: int) -> str:
    # BEGIN SOLUTION
    return f"{name}: {100 * p:.1f}% (95% CI {100 * lo:.1f} to {100 * hi:.1f}), {n} questions, 1 sample each, temperature 0.2"
    # END SOLUTION


# %%
try:
    line = report_line("D", p, lo, hi, n)
except NotImplementedError:
    line = REF["line"]
assert "95% CI" in line and str(n) in line, line
print(line)

# %% [markdown]
# ## ✱ Stretch · Bootstrap over documents
#
# The 600 questions come from 80 regulation documents. Resample **documents** with replacement and keep all their questions. The interval widens: questions from one document succeed and fail together. Session 2 measures by how much.

# %%
one = results[(results.config == "D") & np.isclose(results.temperature, 0.2) & (results["sample"] == 1)]
docs = one.groupby("doc_id").grader_pass.agg(["sum", "count"])
rng = np.random.default_rng(7)
pick = rng.integers(0, len(docs), size=(U.pick(3000, 600), len(docs)))
doc_rates = docs["sum"].to_numpy()[pick].sum(axis=1) / docs["count"].to_numpy()[pick].sum(axis=1)
print(f"document bootstrap SE {doc_rates.std(ddof=1):.4f} against {se:.4f} over questions")

# %% [markdown]
# ## Check yourself
#
# 1. The interval says 71.2 to 78.1. Is that a statement about these 600 questions or about something else?
# <details><summary>Answer</summary>About the population of questions the 600 were drawn from: the pass rate D would get on new questions written the same way. On these 600 questions the rate is known exactly.</details>
#
# 2. Why do the formula and the bootstrap agree here?
# <details><summary>Answer</summary>The verdicts are treated as independent and the rate is far from 0 or 1 with 600 items, so the sampling distribution is close to normal.</details>
#
# 3. What would make both of them too narrow?
# <details><summary>Answer</summary>Questions that are not independent: several written from one document. Both methods resample single questions and miss that.</details>
#
# ## Carry forward
#
# Session 2 keeps the same data and replaces "questions are independent" with "questions share documents". Nothing from this lab needs to be saved.
