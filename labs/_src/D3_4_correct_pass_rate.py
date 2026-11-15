# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy>=2.0", "pandas>=2.2", "scipy>=1.14", "statsmodels>=0.14", "matplotlib>=3.9"]
# ///

# %% [markdown]
# # Lab 3.4 · Correcting the pass rate
#
# Day 3 · Session 4 (Correcting for grader error) · 25 min.
#
# The grader passes a quarter of bad Arabic answers. You correct configurations C's and D's pass rates for the grader's error in each language, and build intervals that resample both the 600 test questions (by document) and the 300 human-labelled verdicts, so the uncertainty of the calibration is carried into the interval.
#
# **Tasks**
# - [ ] The correction formula as a function · 5 min
# - [ ] Corrected rates by language · 5 min
# - [ ] An interval from the test set only · 4 min
# - [ ] A bootstrap over test questions and calibration verdicts · 7 min
# - [ ] The table: uncorrected and corrected, by language · 4 min
# - [ ] ✱ Stretch · Find the observed rates at which the correction leaves 0 to 1

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

REF = U.reference("d3_4")

# %% [markdown]
# ## 1 · The correction formula
#
# If the true pass rate is $\theta$, the grader passes a share $p = \theta\cdot sens + (1-\theta)(1-spec)$ of answers. Solve for $\theta$:
#
# $$\hat\theta = \frac{p + spec - 1}{sens + spec - 1}$$
#
# (Rogan and Gladen's estimator; AE-303 used it for a point estimate.) It needs $sens + spec > 1$: a grader no better than chance cannot be corrected.
#
# ✏️ **Exercise** · Write it.

# %%
def corrected(p: float, sens: float, spec: float) -> float:
    # BEGIN SOLUTION
    return (p + spec - 1) / (sens + spec - 1)
    # END SOLUTION


# %%
try:
    U.check("correction of 0.70 with sens 0.9, spec 0.7", corrected(0.70, 0.9, 0.7), 0.4 / 0.6, 1e-12)
    correct = corrected
except NotImplementedError:
    correct = U.corrected_rate

# %% [markdown]
# ## 2 · Corrected rates by language

# %%
calib = U.load("grader_calibration")
rates = {lang: U.rates(g) for lang, g in calib.groupby("language")}
scores = {c: U.item_means(c, 0.2) for c in ("C", "D")}
rows = []
for c, t in scores.items():
    for lang in ("ar", "en"):
        p = t[t.language == lang].score.mean()
        r = rates[lang]
        rows.append({"config": c, "language": lang, "observed": p, "corrected": correct(p, r["sens"], r["spec"])})
point = pd.DataFrame(rows)
U.check("corrected Arabic rate of C", point.query("config == 'C' and language == 'ar'").corrected.iloc[0], REF["point"]["C_ar"], 1e-9)
print(point.round(4).to_string(index=False))

# %% [markdown]
# **Look at** the Arabic rows: the correction lowers them more, because the grader is more lenient in Arabic.
#
# ## 3 · An interval from the test set only
#
# Treat sens and spec as known: the corrected rate is a linear function of $p$, so its SE is the clustered SE of $p$ divided by $(sens + spec - 1)$. This interval is too narrow: the 49 Arabic failures behind the specificity are themselves a small sample.

# %%
def test_only_se(t: pd.DataFrame, lang: str) -> float:
    g = t[t.language == lang]
    r = rates[lang]
    return U.clustered_se(g.score, g.doc_id) / (r["sens"] + r["spec"] - 1)


for c, t in scores.items():
    print(c, {lang: round(test_only_se(t, lang), 4) for lang in ("ar", "en")})

# %% [markdown]
# ## 4 · A bootstrap over test questions and calibration verdicts
#
# Each replicate resamples **documents** of the test set and, independently, the **calibration verdicts** within each language; recomputes sens, spec and the observed rate; and corrects. The spread carries both sources of uncertainty.
#
# ✏️ **Exercise** · Return an array of `B` corrected rates for one configuration and language.

# %%
def bootstrap_corrected(t: pd.DataFrame, lang: str, B: int, rng: np.random.Generator) -> np.ndarray:
    g = t[t.language == lang]
    by_doc = g.groupby("doc_id").score.agg(["sum", "count"])
    sums, cnts = by_doc["sum"].to_numpy(), by_doc["count"].to_numpy()
    cal = calib[calib.language == lang]
    h, v = cal.human_pass.to_numpy(), cal.grader_pass.to_numpy()
    out = np.empty(B)
    for b in range(B):
        # BEGIN SOLUTION
        pick = rng.integers(0, len(sums), size=len(sums))
        p = sums[pick].sum() / cnts[pick].sum()
        j = rng.integers(0, len(h), size=len(h))
        hb, vb = h[j], v[j]
        sens = vb[hb == 1].mean()
        spec = 1 - vb[hb == 0].mean()
        out[b] = (p + spec - 1) / (sens + spec - 1)
        # END SOLUTION
    return out


# %%
B = U.pick(4000, 600)
rng = np.random.default_rng(403)
rows = []
for c, t in scores.items():
    for lang in ("ar", "en"):
        try:
            draws = bootstrap_corrected(t, lang, B, rng)
            lo, hi = np.percentile(draws, [2.5, 97.5])
        except NotImplementedError:
            lo, hi = REF["boot"][f"{c}_{lang}"]
        rows.append({"config": c, "language": lang, "boot_lo": lo, "boot_hi": hi})
boot = pd.DataFrame(rows)
print(boot.round(4).to_string(index=False))
w_ar = boot.query("config == 'C' and language == 'ar'")
assert abs(w_ar.boot_lo.iloc[0] - REF["boot"]["C_ar"][0]) < 0.03, w_ar

# %% [markdown]
# ## 5 · The table: uncorrected and corrected, by language
#
# For each configuration and language: the observed rate with its clustered interval, the corrected rate with the bootstrap interval. This is the evidence for LO4.

# %%
table = point.merge(boot, on=["config", "language"])
obs_ci = []
for _, r in table.iterrows():
    g = scores[r.config][scores[r.config].language == r.language]
    se = U.clustered_se(g.score, g.doc_id)
    obs_ci.append(f"{100 * r.observed:.1f} ({100 * (r.observed - 1.96 * se):.1f} to {100 * (r.observed + 1.96 * se):.1f})")
table["observed (95% CI)"] = obs_ci
table["corrected (95% CI)"] = [f"{100 * r.corrected:.1f} ({100 * r.boot_lo:.1f} to {100 * r.boot_hi:.1f})" for _, r in table.iterrows()]
print(table[["config", "language", "observed (95% CI)", "corrected (95% CI)"]].to_string(index=False))
out = Path("artifacts/D3_4"); out.mkdir(parents=True, exist_ok=True)
table.to_csv(out / "corrected_rates.csv", index=False)

# %% [markdown]
# **Look at** the widths: the corrected intervals are wider than the observed ones, mostly because of the calibration set, and widest in Arabic, where only 49 failed answers inform the specificity.
#
# ## ✱ Stretch · When the correction leaves 0 to 1
#
# The corrected rate is below 0 when $p < 1 - spec$ and above 1 when $p > sens$. Find those bounds per language, and say what to report when it happens (clip to the bound and say so, or report the interval only).

# %%
for lang, r in rates.items():
    print(lang, f"valid for observed rates between {1 - r['spec']:.3f} and {r['sens']:.3f}")

# %% [markdown]
# ## Check yourself
#
# 1. Why is the test-only interval too narrow?
# <details><summary>Answer</summary>It treats sensitivity and specificity as exact, but they come from 300 labels, and the Arabic specificity from only 49 failed answers.</details>
#
# 2. The corrected Arabic rate of C fell more than the English one. What does that do to the language gap?
# <details><summary>Answer</summary>It widens it: the lenient Arabic grader was hiding part of C's Arabic weakness. Lab 4.3 measures the gap.</details>
#
# 3. What assumption makes the correction valid?
# <details><summary>Answer</summary>That the grader's sensitivity and specificity on the calibration answers equal those on the test answers, in each language: the calibration sample must come from the same kind of answers.</details>
#
# ## Carry forward
#
# `artifacts/D3_4/corrected_rates.csv`; Lab 4.3 recomputes what it needs and has the reference in `data/reference/d3_4.json`.
