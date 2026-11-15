# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy>=2.0", "pandas>=2.2", "scipy>=1.14", "statsmodels>=0.14", "matplotlib>=3.9"]
# ///

# %% [markdown]
# # Lab 2.3 · Sizing for three points
#
# Day 2 · Session 3 (Sizing an evaluation) · 25 min.
#
# The authority will write a new task set from the 2027 regulations. Dr. Nadeen wants it big enough to detect a three-point difference between two configurations with 80% power at the 5% level. The comparison of C and D on today's 600 questions is your pilot. You size the new set by formula, with the design effect, and check the power by simulation over documents.
#
# **Tasks**
# - [ ] Pilot variance of the paired difference · 4 min
# - [ ] The formula: items for 80% power · 6 min
# - [ ] The design effect in the formula · 4 min
# - [ ] Power by simulation over documents · 8 min
# - [ ] The sizing plan in three lines · 3 min
# - [ ] ✱ Stretch · Size the unpaired design and compare the cost

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

import math
import numpy as np
import pandas as pd
from scipy import stats
import bunyan as U

REF = U.reference("d2_3")
DELTA, ALPHA, POWER = 0.03, 0.05, 0.80

# %% [markdown]
# ## 1 · Pilot variance of the paired difference
#
# The pilot is the per-question difference D minus C (mean of five samples, temperature 0.2). What the sizing needs from it is the **spread** of the differences, not their mean.

# %%
pilot = U.paired_table("C", "D", 0.2)
s = pilot["diff"].std(ddof=1)
deff = (U.clustered_se(pilot["diff"], pilot.doc_id) / U.se_formula(pilot["diff"])) ** 2
per_doc = len(pilot) / pilot.doc_id.nunique()
print(f"SD of the per-question difference {s:.4f}; design effect of the difference {deff:.3f}; {per_doc:.1f} questions per document")
U.check("pilot SD", s, REF["sd"], 1e-9)

# %% [markdown]
# ## 2 · The formula: items for 80% power
#
# For a paired difference tested two-sided at level $\alpha$ with power $1 - \beta$ against a true difference $\delta$:
#
# $$n = \frac{(z_{1-\alpha/2} + z_{1-\beta})^2\, s^2}{\delta^2}$$
#
# ✏️ **Exercise** · Return n, rounded up, for independent questions.

# %%
def n_items(s: float, delta: float, alpha: float = 0.05, power: float = 0.8) -> int:
    # BEGIN SOLUTION
    z = stats.norm.ppf(1 - alpha / 2) + stats.norm.ppf(power)
    return math.ceil((z * s / delta) ** 2)
    # END SOLUTION


# %%
try:
    n_indep = n_items(s, DELTA, ALPHA, POWER)
except NotImplementedError:
    n_indep = REF["n_independent"]
U.check("items, independent", n_indep, REF["n_independent"])
print(f"{n_indep} questions if they were independent")

# %% [markdown]
# ## 3 · The design effect in the formula
#
# Questions come in documents, so multiply by the design effect of the **difference**. Here it is close to 1: the document effect cancels in a paired difference. For a single configuration's score it would be about 2.5 (Lab 1.2), and sizing a single score with the naive formula would be badly short.

# %%
n_needed = math.ceil(n_indep * max(deff, 1.0))
docs_needed = math.ceil(n_needed / per_doc)
print(f"with the design effect (floored at 1): {n_needed} questions, about {docs_needed} documents at {per_doc:.1f} per document")
U.check("items with the design effect", n_needed, REF["n_needed"])

# %% [markdown]
# ## 4 · Power by simulation over documents
#
# The formula assumes normality and a known variance. Check it: draw documents with replacement from the pilot until there are about `n` questions, shift every difference so that the true mean is exactly three points, run the planned clustered test, and count how often it rejects zero.
#
# ✏️ **Exercise** · Complete `simulated_power`.

# %%
docs = {g: d["diff"].to_numpy() for g, d in pilot.groupby("doc_id")}
doc_ids = list(docs)
centre = pilot["diff"].mean()


def simulated_power(n: int, delta: float, sims: int, seed: int = 403) -> float:
    rng = np.random.default_rng(seed)
    m = math.ceil(n / per_doc)
    hits = 0
    for _ in range(sims):
        pick = rng.integers(0, len(doc_ids), size=m)
        # BEGIN SOLUTION
        parts = [docs[doc_ids[i]] - centre + delta for i in pick]
        x = np.concatenate(parts)
        groups = np.repeat(np.arange(m), [len(p) for p in parts])
        se = U.clustered_se(x, groups)
        hits += (x.mean() - 1.96 * se) > 0
        # END SOLUTION
    return hits / sims


# %%
SIMS = U.pick(2000, 300)
try:
    rows = [{"questions": n, "power": simulated_power(n, DELTA, SIMS)} for n in (300, n_needed, 900)]
except NotImplementedError:
    rows = REF["simulated"]
sim = pd.DataFrame(rows)
print(sim.round(3).to_string(index=False))
p_at_n = sim.set_index("questions").loc[n_needed, "power"]
assert 0.70 < p_at_n < 0.90, p_at_n

# %% [markdown]
# **Look at** the middle row: the simulated power at the formula's n should be close to 80%. If it were far below, the formula's assumptions (a normal difference, a well-estimated variance) would not hold for this kind of data.
#
# ## 5 · The sizing plan in three lines

# %%
plan = f"""Sizing plan, 2027 regulation task set
Detect D minus C = 3 points (paired, two-sided, alpha 0.05) with 80% power: {n_needed} questions from about {docs_needed} documents, 5 samples each at temperature 0.2.
Pilot: 600 questions of the 2026 set; SD of the per-question difference {s:.3f}; design effect of the difference {deff:.2f}; simulated power at {n_needed} questions {p_at_n:.0%}."""
print(plan)

# %% [markdown]
# ## ✱ Stretch · The unpaired design
#
# If the two configurations answered different questions, the variance of the difference would be $2\sigma^2 \cdot DEFF$ for each score's variance $\sigma^2$ and DEFF of about 2.5. How many questions per configuration would that need?

# %%
sigma2 = (pilot.score_C.var(ddof=1) + pilot.score_D.var(ddof=1)) / 2
deff_score = (U.clustered_se(pilot.score_D, pilot.doc_id) / U.se_formula(pilot.score_D)) ** 2
z = stats.norm.ppf(0.975) + stats.norm.ppf(0.8)
n_unpaired = math.ceil(z ** 2 * 2 * sigma2 * deff_score / DELTA ** 2)
print(f"unpaired: {n_unpaired} questions per configuration, against {n_needed} paired")

# %% [markdown]
# ## Check yourself
#
# 1. Why does sizing use the pilot's spread and not its observed difference of about two points?
# <details><summary>Answer</summary>The target difference is the minimum effect that matters, fixed by the decision owner; the pilot only tells how noisy the per-question differences are.</details>
#
# 2. The 2027 set will have 12 questions per document. What changes?
# <details><summary>Answer</summary>Fewer documents for the same questions, so a larger design effect for single scores; for the paired difference it may still be near 1, but the simulation should be rerun with the new cluster size.</details>
#
# 3. Why simulate when the formula exists?
# <details><summary>Answer</summary>The simulation uses the real shape of the data, clusters and all, and the planned test. If the two disagree, trust the simulation and find which assumption failed.</details>
#
# ## Carry forward
#
# The sizing plan feeds the capstone: every capstone repository has one.
