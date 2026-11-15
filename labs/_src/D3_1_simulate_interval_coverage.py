# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy>=2.0", "pandas>=2.2", "scipy>=1.14", "statsmodels>=0.14", "matplotlib>=3.9"]
# ///

# %% [markdown]
# # Lab 3.1 · Coverage by simulation
#
# Day 3 · Session 1 (Where large-sample intervals fail) · 25 min.
#
# Bunyan's safety set has 40 questions, and the configurations pass almost all of them. Before you put intervals on those rates, you measure how often four kinds of 95% interval actually contain the true rate, for 20 to 200 items and rates near 0, 0.5 and 1. No data file is needed: you simulate.
#
# **Tasks**
# - [ ] Four interval functions · 6 min
# - [ ] One coverage estimate by simulation · 5 min
# - [ ] The grid: 20 to 200 items, five rates · 7 min
# - [ ] Read the table: where Wald fails · 4 min
# - [ ] A rule for the authority · 3 min
# - [ ] ✱ Stretch · Compute the exact coverage by summing the binomial and compare

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
from scipy import stats
import bunyan as U

REF = U.reference("d3_1")

# %% [markdown]
# ## 1 · Four interval functions
#
# - **Wald**: $\hat p \pm z\sqrt{\hat p(1-\hat p)/n}$, the formula of Day 1.
# - **Wilson**: inverts the score test; its centre is pulled toward 0.5.
# - **Clopper-Pearson** ("exact"): from Beta quantiles; never covers less than 95%.
# - **Jeffreys**: the Beta(0.5, 0.5)-prior posterior interval.
#
# ✏️ **Exercise** · Write `wald(k, n)` and `wilson(k, n)` returning `(low, high)` at 95%. Clopper-Pearson and Jeffreys are given.

# %%
Z = stats.norm.ppf(0.975)


def wald(k: int, n: int):
    # BEGIN SOLUTION
    p = k / n
    h = Z * np.sqrt(p * (1 - p) / n)
    return (p - h, p + h)
    # END SOLUTION


def wilson(k: int, n: int):
    # BEGIN SOLUTION
    p = k / n
    centre = (p + Z ** 2 / (2 * n)) / (1 + Z ** 2 / n)
    h = Z * np.sqrt(p * (1 - p) / n + Z ** 2 / (4 * n ** 2)) / (1 + Z ** 2 / n)
    return (centre - h, centre + h)
    # END SOLUTION


METHODS = {"Wald": wald, "Wilson": wilson, "Clopper-Pearson": U.clopper_pearson,
           "Jeffreys": lambda k, n: U.beta_interval(k, n, 0.5, 0.5)}

# %%
try:
    got = [wald(38, 40), wilson(38, 40)]
except NotImplementedError:
    METHODS["Wald"], METHODS["Wilson"] = U.wald, U.wilson
    got = [U.wald(38, 40), U.wilson(38, 40)]
U.check("Wald for 38 of 40", got[0], REF["wald_38_40"], 1e-9)
U.check("Wilson for 38 of 40", got[1], REF["wilson_38_40"], 1e-9)
print("Wald", np.round(got[0], 4), " Wilson", np.round(got[1], 4))

# %% [markdown]
# ## 2 · One coverage estimate by simulation
#
# Draw `S` evaluations of `n` items with true rate `p`, build the interval each time, and count how often it contains `p`. Only `n + 1` outcomes are possible, so compute the interval once per outcome `k`.
#
# ✏️ **Exercise** · Return the simulated coverage.

# %%
def coverage(method, n: int, p: float, S: int, rng: np.random.Generator) -> float:
    # BEGIN SOLUTION
    k = rng.binomial(n, p, size=S)
    covers = np.array([lo <= p <= hi for lo, hi in (method(j, n) for j in range(n + 1))])
    return float(covers[k].mean())
    # END SOLUTION


# %%
S = U.pick(4000, 800)
try:
    c = coverage(METHODS["Wald"], 40, 0.95, S, np.random.default_rng(403))
except NotImplementedError:
    c = REF["exact"]["Wald"]["40"]["0.95"]
U.check("Wald coverage at n = 40, p = 0.95 (simulation within 0.03 of exact)", c, REF["exact"]["Wald"]["40"]["0.95"], 0.03)
print(f"Wald covers p = 0.95 with 40 items {c:.1%} of the time, not 95%")

# %% [markdown]
# ## 3 · The grid: 20 to 200 items, five rates

# %%
NS = [20, 40, 80, 120, 200]
PS = [0.02, 0.05, 0.5, 0.95, 0.98]
rng = np.random.default_rng(403)
rows = []
for name, m in METHODS.items():
    for n in NS:
        for p in PS:
            try:
                cv = coverage(m, n, p, S, rng)
            except NotImplementedError:
                cv = REF["exact"][name][str(n)][str(p)]
            rows.append({"method": name, "n": n, "p": p, "coverage": cv})
grid = pd.DataFrame(rows)
table = grid.pivot_table(index=["method", "n"], columns="p", values="coverage").round(3)
print(table.to_string())

# %% [markdown]
# ## 4 · Read the table: where Wald fails
#
# **Look at** Wald near 0 and 1: with 20 or 40 items it covers far less than 95%. When every item passes, Wald's interval is the single point 1, which covers nothing but certainty. Clopper-Pearson covers at least 95% everywhere, at the cost of width; Wilson and Jeffreys are close to 95% on average.

# %%
worst = grid.groupby("method").coverage.min().sort_values()
print("lowest coverage in the grid:")
print(worst.round(3).to_string())
assert worst["Wald"] < 0.80 and worst["Clopper-Pearson"] >= 0.93, worst

# %% [markdown]
# ## 5 · A rule for the authority
#
# Write one sentence for Bunyan's reporting standard: which interval for a pass rate, and when.

# %%
rule = ("Report a pass rate with a Wilson or Jeffreys interval when it has fewer than a few hundred items or lies "
        "within 0.1 of 0 or 1, and with Clopper-Pearson when the claim is about safety and must not under-cover; "
        "never with the normal approximation in those cases.")
print(rule)

# %% [markdown]
# ## ✱ Stretch · Exact coverage
#
# The coverage is a finite sum: $\sum_k P(K = k)\,\mathbb{1}[p \in I(k)]$. Compute it and compare with your simulation.

# %%
def exact_coverage(method, n, p):
    ks = np.arange(n + 1)
    covers = np.array([lo <= p <= hi for lo, hi in (method(j, n) for j in ks)])
    return float(stats.binom.pmf(ks, n, p)[covers].sum())


print(f"exact Wald coverage, n = 40, p = 0.95: {exact_coverage(U.wald, 40, 0.95):.3f}")

# %% [markdown]
# ## Check yourself
#
# 1. Why does Wald's coverage collapse near 1 with few items?
# <details><summary>Answer</summary>When most draws give k close to n, the estimated variance p(1 − p)/n is tiny or zero, so the interval shrinks exactly where the estimate is least reliable.</details>
#
# 2. Clopper-Pearson often covers 97 to 99%. Is that a problem?
# <details><summary>Answer</summary>It is conservative: wider than needed on average. For a safety claim that cost is usually worth paying.</details>
#
# 3. With 600 items and a rate of 0.74, which interval would you use?
# <details><summary>Answer</summary>Any of them: far from 0 and 1 with hundreds of items they agree. The choice matters for small sets and extreme rates.</details>
#
# ## Carry forward
#
# Lab 3.2 applies Clopper-Pearson and Beta intervals to the real 40-item safety set.
