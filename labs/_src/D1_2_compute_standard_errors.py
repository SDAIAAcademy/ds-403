# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy>=2.0", "pandas>=2.2", "scipy>=1.14", "statsmodels>=0.14", "matplotlib>=3.9"]
# ///

# %% [markdown]
# # Lab 1.2 · Clustered by document
#
# Day 1 · Session 2 (Clustered items) · 25 min.
#
# The 600 questions of Bunyan's task set were written from 80 regulation documents, four to eleven per document. You compute standard errors clustered by document for the four configurations, the design effect and the effective number of questions, and check your formula two ways.
#
# **Tasks**
# - [ ] Questions per document and pass rate per document · 4 min
# - [ ] The clustered standard error by formula · 7 min
# - [ ] Design effect and effective number of items · 5 min
# - [ ] A cluster bootstrap as a check · 5 min
# - [ ] statsmodels with cluster covariance as a second check · 4 min
# - [ ] ✱ Stretch · Cluster by category instead and explain why eight clusters are too few

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
import statsmodels.api as sm
import bunyan as U

REF = U.reference("d1_2")

# %% [markdown]
# ## 1 · Questions per document and pass rate per document
#
# From here on a question's score is the **mean of its five samples** at temperature 0.2 (`U.item_means`). Look at how unequal the documents are.

# %%
d = U.item_means("D", 0.2)
per_doc = d.groupby("doc_id").score.agg(["count", "mean"])
print(per_doc["count"].describe().round(2).to_string())
fig, ax = plt.subplots(figsize=(7, 3))
ax.hist(per_doc["mean"], bins=20, color="#264653")
ax.set_xlabel("pass rate of D per document (80 documents)")
U.show(fig)

# %% [markdown]
# **Look at** the spread: some documents are almost always answered well, some almost never. Questions inside a document share that level, so 600 questions carry less independent evidence than 600 coin flips.
#
# ## 2 · The clustered standard error by formula
#
# With item scores $x_i$, mean $\bar x$ and documents $g$:
#
# $$SE_{cl} = \frac{1}{n}\sqrt{\sum_g \Big(\sum_{i \in g} (x_i - \bar x)\Big)^2}$$
#
# Deviations inside one document are summed **before** squaring, so documents whose questions fail together add a lot.
#
# ✏️ **Exercise** · Write `clustered_se(x, groups)`.

# %%
def clustered_se(x, groups) -> float:
    # BEGIN SOLUTION
    x = np.asarray(x, dtype=float)
    sums = pd.Series(x - x.mean()).groupby(np.asarray(groups)).sum()
    return float(np.sqrt((sums ** 2).sum()) / len(x))
    # END SOLUTION


# %%
try:
    cl = clustered_se(d.score, d.doc_id)
except NotImplementedError:
    cl = REF["D"]["clustered_se"]
U.check("clustered SE of D", cl, REF["D"]["clustered_se"], 1e-9)
print(f"naive SE {U.se_formula(d.score):.4f}   clustered SE {cl:.4f}")

# %% [markdown]
# ## 3 · Design effect and effective number of items
#
# The **design effect** is the ratio of the variances: $DEFF = (SE_{cl}/SE_{naive})^2$. The **effective number of items** is $n / DEFF$: how many independent questions the 600 are worth.
#
# ✏️ **Exercise** · Return a table with one row per configuration A to D: mean, naive SE, clustered SE, DEFF, effective n.

# %%
def design_table() -> pd.DataFrame:
    rows = []
    for c in "ABCD":
        t = U.item_means(c, 0.2)
        # BEGIN SOLUTION
        naive = U.se_formula(t.score)
        clu = clustered_se(t.score, t.doc_id)
        deff = (clu / naive) ** 2
        rows.append({"config": c, "mean": t.score.mean(), "naive_se": naive, "clustered_se": clu,
                     "deff": deff, "n_eff": len(t) / deff})
        # END SOLUTION
    return pd.DataFrame(rows)


# %%
try:
    table = design_table()
except NotImplementedError:
    table = pd.DataFrame([{"config": c, **REF[c]} for c in "ABCD"])
for c in "ABCD":
    U.check(f"DEFF of {c}", table.set_index("config").loc[c, "deff"], REF[c]["deff"], 1e-6)
print(table.round(4).to_string(index=False))

# %% [markdown]
# ## 4 · A cluster bootstrap as a check
#
# Resample whole documents with replacement and recompute the mean each time. Its spread should be close to your clustered SE.

# %%
def cluster_bootstrap_se(t: pd.DataFrame, B: int, seed: int = 403) -> float:
    g = t.groupby("doc_id").score.agg(["sum", "count"])
    rng = np.random.default_rng(seed)
    pick = rng.integers(0, len(g), size=(B, len(g)))
    means = g["sum"].to_numpy()[pick].sum(axis=1) / g["count"].to_numpy()[pick].sum(axis=1)
    return float(means.std(ddof=1))


boot = cluster_bootstrap_se(d, U.pick(4000, 800))
U.check("cluster bootstrap agrees with the formula", boot, cl, 0.0025)
print(f"cluster bootstrap SE {boot:.4f}   formula {cl:.4f}")

# %% [markdown]
# ## 5 · statsmodels with cluster covariance as a second check
#
# A regression of the score on a constant estimates the mean; asking for cluster-robust covariance gives the clustered SE. statsmodels multiplies by a small-sample factor $\frac{G}{G-1}\cdot\frac{n-1}{n-1}$, so expect it slightly larger.

# %%
fit = sm.OLS(d.score.to_numpy(), np.ones(len(d))).fit(cov_type="cluster", cov_kwds={"groups": pd.factorize(d.doc_id)[0]})
G = d.doc_id.nunique()
U.check("statsmodels equals the formula times the small-sample factor", fit.bse[0], cl * np.sqrt(G / (G - 1)), 1e-6)
print(f"statsmodels SE {fit.bse[0]:.4f}; formula {cl:.4f}; factor {np.sqrt(G / (G - 1)):.4f}")

# %% [markdown]
# ## ✱ Stretch · Cluster by category
#
# Each document belongs to one of eight categories. Cluster by category and compare. With only eight clusters, the clustered SE is itself very noisy, and statsmodels' factor and a t distribution with 7 degrees of freedom matter.

# %%
print(f"clustered by category: {U.clustered_se(d.score, d.category):.4f} (8 clusters)")

# %% [markdown]
# ## Check yourself
#
# 1. D's design effect is about 2.4. What does that mean in questions?
# <details><summary>Answer</summary>The 600 questions carry about as much information as 600 / 2.4, about 250, independent ones. Intervals are about sqrt(2.4), 1.55 times, wider than the naive ones.</details>
#
# 2. The authority wants to add 120 questions. Is it better to write them from the existing 80 documents or from 40 new ones?
# <details><summary>Answer</summary>From new documents: more clusters reduce the clustered SE faster than more items in the same clusters.</details>
#
# 3. Would the design effect vanish if every document had exactly one question?
# <details><summary>Answer</summary>Yes: with one item per cluster the clustered and naive SE coincide (up to the small-sample factor).</details>
#
# ## Carry forward
#
# `U.clustered_se` in the helper module is the same function; every later lab uses it.
