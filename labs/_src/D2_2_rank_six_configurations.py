# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy>=2.0", "pandas>=2.2", "scipy>=1.14", "statsmodels>=0.14", "matplotlib>=3.9"]
# ///

# %% [markdown]
# # Lab 2.2 · Six configurations ranked
#
# Day 2 · Session 2 (Many configurations) · 25 min.
#
# Khattab added two prompt variants of D, called E and F, and wants a ranking of all six configurations. Each answered the 600 questions once at temperature 0.2. You compute the fifteen paired differences, adjust their intervals for multiplicity, and publish a ranking that says which configurations cannot be told apart.
#
# **Tasks**
# - [ ] Six pass rates and the naive ranking · 3 min
# - [ ] Fifteen paired differences, clustered · 6 min
# - [ ] Bonferroni and Holm adjustments · 6 min
# - [ ] Which pairs are separated · 5 min
# - [ ] A rank table with plausible ranks · 5 min
# - [ ] ✱ Stretch · Bootstrap the rank of each configuration over documents

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

from itertools import combinations
import numpy as np
import pandas as pd
from scipy import stats
import bunyan as U

REF = U.reference("d2_2")

# %% [markdown]
# ## 1 · Six pass rates and the naive ranking

# %%
six = U.load("results_six").merge(U.items()[["item_id", "doc_id"]], on="item_id")
wide = six.pivot(index=["item_id", "doc_id"], columns="config", values="grader_pass").reset_index()
CONFIGS = list("ABCDEF")
means = wide[CONFIGS].mean().sort_values(ascending=False)
print(means.round(4).to_string())

# %% [markdown]
# ## 2 · Fifteen paired differences, clustered
#
# ✏️ **Exercise** · For every pair (a, b) with a before b in `CONFIGS`, return a table with the difference b minus a, its clustered SE, its z and its two-sided p-value.

# %%
def pair_table(wide: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for a, b in combinations(CONFIGS, 2):
        # BEGIN SOLUTION
        d = wide[b] - wide[a]
        se = U.clustered_se(d, wide.doc_id)
        z = d.mean() / se
        rows.append({"a": a, "b": b, "diff": d.mean(), "se": se, "z": z, "p": 2 * stats.norm.sf(abs(z))})
        # END SOLUTION
    return pd.DataFrame(rows)


# %%
try:
    pairs = pair_table(wide)
except NotImplementedError:
    pairs = pd.DataFrame(REF["pairs"])
U.check("fifteen pairs", len(pairs), 15)
U.check("p-value of E against F", pairs.query("a == 'E' and b == 'F'").p.iloc[0],
        [r["p"] for r in REF["pairs"] if r["a"] == "E" and r["b"] == "F"][0], 1e-9)
print(pairs.round(4).to_string(index=False))

# %% [markdown]
# ## 3 · Bonferroni and Holm adjustments
#
# Fifteen tests at 5% give, among truly equal configurations, a good chance of at least one false separation. **Bonferroni** tests each at 0.05 / 15 and widens each interval with $z_{1 - 0.05/30}$. **Holm** sorts the p-values and compares the k-th smallest with 0.05 / (15 − k + 1), stopping at the first that fails: it separates at least as many pairs as Bonferroni and keeps the same family-wise guarantee.
#
# ✏️ **Exercise** · Add columns `bonf_lo`, `bonf_hi` (Bonferroni-adjusted 95% intervals) and `holm_reject` (True or False).

# %%
def adjust(pairs: pd.DataFrame, alpha: float = 0.05) -> pd.DataFrame:
    pairs = pairs.copy()
    m = len(pairs)
    # BEGIN SOLUTION
    z = stats.norm.ppf(1 - alpha / (2 * m))
    pairs["bonf_lo"] = pairs["diff"] - z * pairs.se
    pairs["bonf_hi"] = pairs["diff"] + z * pairs.se
    order = np.argsort(pairs.p.to_numpy())
    reject = np.zeros(m, dtype=bool)
    for k, i in enumerate(order):
        if pairs.p.iloc[i] <= alpha / (m - k):
            reject[i] = True
        else:
            break
    pairs["holm_reject"] = reject
    # END SOLUTION
    return pairs


# %%
try:
    adj = adjust(pairs)
except NotImplementedError:
    adj = pd.DataFrame(REF["adjusted"])
U.check("pairs separated by Holm", int(adj.holm_reject.sum()), REF["n_holm"])
print(f"separated at 5% unadjusted: {(adj.p < 0.05).sum()}; Bonferroni: {((adj.bonf_lo > 0) | (adj.bonf_hi < 0)).sum()}; Holm: {adj.holm_reject.sum()}")

# %% [markdown]
# ## 4 · Which pairs are separated
#
# **Look at** the pairs among C, D, E and F. The naive ranking puts one of them first; the adjusted analysis cannot separate it from the next.

# %%
print(adj[["a", "b", "diff", "p", "bonf_lo", "bonf_hi", "holm_reject"]].round(4).to_string(index=False))

# %% [markdown]
# ## 5 · A rank table with plausible ranks
#
# A configuration's best plausible rank is 1 plus the number of configurations separated **above** it; its worst plausible rank is 6 minus the number separated **below** it (Holm).
#
# ✏️ **Exercise** · Return a table with `config`, `pass_rate`, `best_rank`, `worst_rank`, sorted by pass rate.

# %%
def rank_table(means: pd.Series, adj: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for c in CONFIGS:
        # BEGIN SOLUTION
        above = below = 0
        for _, r in adj[adj.holm_reject].iterrows():
            if c in (r.a, r.b):
                other_better = (r.b != c and r["diff"] > 0) or (r.a != c and r["diff"] < 0)
                if other_better:
                    above += 1
                else:
                    below += 1
        rows.append({"config": c, "pass_rate": means[c], "best_rank": 1 + above, "worst_rank": 6 - below})
        # END SOLUTION
    return pd.DataFrame(rows).sort_values("pass_rate", ascending=False).reset_index(drop=True)


# %%
try:
    ranks = rank_table(means, adj)
except NotImplementedError:
    ranks = pd.DataFrame(REF["ranks"])
U.check("plausible ranks", ranks[["best_rank", "worst_rank"]].to_numpy(), pd.DataFrame(REF["ranks"])[["best_rank", "worst_rank"]].to_numpy())
ranks["plausible"] = ranks.apply(lambda r: f"{r.best_rank}" if r.best_rank == r.worst_rank else f"{r.best_rank} to {r.worst_rank}", axis=1)
print(ranks.round(4).to_string(index=False))

# %% [markdown]
# ## ✱ Stretch · Bootstrap the ranks over documents
#
# Resample documents, recompute the six means, rank them, and count how often each configuration is first.

# %%
g = wide.groupby("doc_id")[CONFIGS].agg(["sum", "count"])
sums = np.stack([g[(c, "sum")].to_numpy() for c in CONFIGS], axis=1)
counts = g[(CONFIGS[0], "count")].to_numpy()
rng = np.random.default_rng(403)
pick = rng.integers(0, len(g), size=(U.pick(2000, 400), len(g)))
boot = sums[pick].sum(axis=1) / counts[pick].sum(axis=1)[:, None]
first = pd.Series(np.array(CONFIGS)[boot.argmax(axis=1)]).value_counts(normalize=True)
print("share of resamples in which each configuration ranks first:")
print(first.round(3).to_string())

# %% [markdown]
# ## Check yourself
#
# 1. F has the highest pass rate. Can the report say "F is the best configuration"?
# <details><summary>Answer</summary>No: after adjustment F is not separated from D or E. The report can say F, D and E are tied at the top.</details>
#
# 2. Why not simply report fifteen unadjusted 95% intervals?
# <details><summary>Answer</summary>Among fifteen comparisons of equal configurations, one or more would look different by chance far more often than 5% of the time.</details>
#
# 3. Holm separated more pairs than Bonferroni. Is Holm less safe?
# <details><summary>Answer</summary>No: it controls the same family-wise error rate; it is uniformly more powerful because it relaxes the threshold step by step.</details>
#
# ## Carry forward
#
# Nothing to save. Day 4's audit uses the same reasoning on the leaderboard's ranking.
