# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy>=2.0", "pandas>=2.2", "scipy>=1.14", "statsmodels>=0.14", "matplotlib>=3.9"]
# ///

# %% [markdown]
# # Lab 3.2 · Forty safety questions
#
# Day 3 · Session 2 (Exact and Bayesian intervals) · 25 min.
#
# The safety set holds 40 questions where a wrong answer could endanger people: blocked exits, load-bearing walls, fuel in basements. Each configuration answered once, greedily, and the human panel marked each answer safe or unsafe. Configuration D was safe on all 40. You put exact and Bayesian intervals on the four rates and write the safety line of the release note without claiming perfection.
#
# **Tasks**
# - [ ] Safe answers per configuration · 3 min
# - [ ] The normal-approximation interval and its failure · 4 min
# - [ ] Clopper-Pearson intervals · 6 min
# - [ ] Beta posteriors under two priors · 7 min
# - [ ] The safety line for the release note · 5 min
# - [ ] ✱ Stretch · The posterior probability that C is safer than A

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

REF = U.reference("d3_2")

# %% [markdown]
# ## 1 · Safe answers per configuration

# %%
safety = U.load("safety_results")
counts = safety.groupby("config").safe.agg(k="sum", n="count")
print(counts.to_string())

# %% [markdown]
# ## 2 · The normal-approximation interval and its failure

# %%
for c, r in counts.iterrows():
    print(c, f"{r.k}/{r.n}", np.round(U.wald(r.k, r.n), 3))

# %% [markdown]
# **Look at** D: 40 out of 40 gives the interval [1, 1]. It claims certainty from 40 questions. A and B's upper ends may also pass 1.
#
# ## 3 · Clopper-Pearson intervals
#
# The exact interval's lower end for k successes in n is the 2.5% quantile of Beta(k, n − k + 1); its upper end the 97.5% quantile of Beta(k + 1, n − k). At k = n the upper end is 1 and, for a one-sided statement, the lower bound at 95% is $0.05^{1/n}$.
#
# ✏️ **Exercise** · Return the two-sided 95% Clopper-Pearson interval with `scipy.stats.beta`.

# %%
def clopper_pearson(k: int, n: int, level: float = 0.95):
    a = 1 - level
    # BEGIN SOLUTION
    lo = 0.0 if k == 0 else stats.beta.ppf(a / 2, k, n - k + 1)
    hi = 1.0 if k == n else stats.beta.ppf(1 - a / 2, k + 1, n - k)
    return (float(lo), float(hi))
    # END SOLUTION


# %%
cp = {}
for c, r in counts.iterrows():
    try:
        cp[c] = clopper_pearson(int(r.k), int(r.n))
    except NotImplementedError:
        cp[c] = tuple(REF["cp"][c])
    U.check(f"Clopper-Pearson for {c}", cp[c], REF["cp"][c], 1e-9)
print({c: np.round(v, 4) for c, v in cp.items()})
print(f"one-sided 95% lower bound for 40/40: {0.05 ** (1 / 40):.4f}; rule of three: {1 - 3 / 40:.4f}")

# %% [markdown]
# ## 4 · Beta posteriors under two priors
#
# With a Beta(a, b) prior and k safe answers out of n, the posterior is Beta(a + k, b + n − k). Use the uniform prior Beta(1, 1) and Jeffreys' Beta(0.5, 0.5); report the equal-tailed 95% interval and the posterior mean.
#
# ✏️ **Exercise** · Return `(mean, low, high)` of the posterior.

# %%
def beta_posterior(k: int, n: int, a: float, b: float):
    # BEGIN SOLUTION
    post = stats.beta(a + k, b + n - k)
    return (float(post.mean()), float(post.ppf(0.025)), float(post.ppf(0.975)))
    # END SOLUTION


# %%
rows = []
for c, r in counts.iterrows():
    for prior, (a, b) in {"uniform": (1, 1), "Jeffreys": (0.5, 0.5)}.items():
        try:
            m, lo, hi = beta_posterior(int(r.k), int(r.n), a, b)
        except NotImplementedError:
            m, lo, hi = REF["beta"][c][prior]
        rows.append({"config": c, "prior": prior, "mean": m, "low": lo, "high": hi})
post = pd.DataFrame(rows)
U.check("uniform posterior for D", post.query("config == 'D' and prior == 'uniform'")[["mean", "low", "high"]].to_numpy()[0], REF["beta"]["D"]["uniform"], 1e-9)
table = pd.DataFrame({
    "uniform": [f"{post.query('config == @c and prior == \"uniform\"').low.iloc[0]:.3f} to {post.query('config == @c and prior == \"uniform\"').high.iloc[0]:.3f}" for c in counts.index],
    "Jeffreys": [f"{post.query('config == @c and prior == \"Jeffreys\"').low.iloc[0]:.3f} to {post.query('config == @c and prior == \"Jeffreys\"').high.iloc[0]:.3f}" for c in counts.index],
    "Clopper-Pearson": [f"{cp[c][0]:.3f} to {cp[c][1]:.3f}" for c in counts.index],
}, index=counts.index)
print(table.to_string())

# %% [markdown]
# **Look at** the two priors: with 40 items they differ in the third decimal. The prior matters most at 40 out of 40, where the data say little about how close to 1 the rate is.
#
# ## 5 · The safety line for the release note
#
# Say what the 40 questions show, and what they do not: "unsafe on fewer than about 9% of such questions" is supported; "never unsafe" is not.

# %%
lo_d = 0.05 ** (1 / 40)
line = (f"Safety set (40 questions, one greedy answer each): D was safe on 40 of 40; with 95% confidence its unsafe-answer "
        f"rate on such questions is below {100 * (1 - lo_d):.1f}% (one-sided Clopper-Pearson). C 39/40, B 38/40, A 36/40.")
print(line)

# %% [markdown]
# ## ✱ Stretch · Is C safer than A?
#
# Draw from both uniform posteriors and estimate $P(p_C > p_A)$.

# %%
rng = np.random.default_rng(403)
kA, kC = int(counts.loc["A", "k"]), int(counts.loc["C", "k"])
draws_a = rng.beta(1 + kA, 1 + 40 - kA, 100_000)
draws_c = rng.beta(1 + kC, 1 + 40 - kC, 100_000)
print(f"P(C safer than A) = {(draws_c > draws_a).mean():.3f}")

# %% [markdown]
# ## Check yourself
#
# 1. Khattab writes "D never gives an unsafe answer". What does the data support instead?
# <details><summary>Answer</summary>An upper bound: with 95% confidence D's unsafe rate on such questions is below about 7.2%. Zero failures in 40 is compatible with a real rate of several percent.</details>
#
# 2. How many safety questions with zero failures would support "below 1%" at 95%?
# <details><summary>Answer</summary>About 300 (rule of three: 3 / n = 0.01).</details>
#
# 3. Why prefer a posterior interval to a p-value here?
# <details><summary>Answer</summary>The question is "how unsafe could D be?", a range for the rate; a test against a single value does not answer it.</details>
#
# ## Carry forward
#
# The safety line goes into the reporting standard of Day 4 as a required field for safety sets.
