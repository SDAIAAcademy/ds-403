# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy>=2.0", "pandas>=2.2", "scipy>=1.14", "statsmodels>=0.14", "matplotlib>=3.9"]
# ///

# %% [markdown]
# # Lab 3.3 · The grader against people
#
# Day 3 · Session 3 (Graders against people) · 25 min.
#
# Every pass rate so far came from a model grader. Sereen Al-Sadiq's bilingual panel labelled 300 of the answers by hand (150 Arabic, 150 English) as pass or fail. You treat the grader as a measuring instrument: its sensitivity (it passes answers people pass) and specificity (it fails answers people fail), in each language, with intervals.
#
# **Tasks**
# - [ ] The 300 verdicts: a confusion table per language · 5 min
# - [ ] Sensitivity and specificity with Wilson intervals · 7 min
# - [ ] Overall agreement and what it hides · 4 min
# - [ ] The difference between languages · 5 min
# - [ ] How many more labels, and of which kind · 4 min
# - [ ] ✱ Stretch · Cohen's kappa per language next to agreement

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

REF = U.reference("d3_3")

# %% [markdown]
# ## 1 · A confusion table per language

# %%
calib = U.load("grader_calibration")
for lang, g in calib.groupby("language"):
    print(f"--- {lang}")
    print(pd.crosstab(g.human_pass.rename("human"), g.grader_pass.rename("grader")).to_string())

# %% [markdown]
# ## 2 · Sensitivity and specificity with Wilson intervals
#
# Sensitivity = P(grader passes | people pass); specificity = P(grader fails | people fail). Each is a proportion in its own column of the table, so each gets a Wilson interval on its own count (Lab 3.1).
#
# ✏️ **Exercise** · Return a dict with `sens`, `sens_lo`, `sens_hi`, `spec`, `spec_lo`, `spec_hi`, `n_pos`, `n_neg` for one language.

# %%
def grader_rates(g: pd.DataFrame) -> dict:
    # BEGIN SOLUTION
    pos, neg = g[g.human_pass == 1], g[g.human_pass == 0]
    tp, tn = int(pos.grader_pass.sum()), int((neg.grader_pass == 0).sum())
    s_lo, s_hi = U.wilson(tp, len(pos))
    c_lo, c_hi = U.wilson(tn, len(neg))
    return {"sens": tp / len(pos), "sens_lo": s_lo, "sens_hi": s_hi,
            "spec": tn / len(neg), "spec_lo": c_lo, "spec_hi": c_hi, "n_pos": len(pos), "n_neg": len(neg)}
    # END SOLUTION


# %%
rates = {}
for lang, g in calib.groupby("language"):
    try:
        rates[lang] = grader_rates(g)
    except NotImplementedError:
        rates[lang] = REF[lang]
    U.check(f"specificity in {lang}", rates[lang]["spec"], REF[lang]["spec"], 1e-9)
print(pd.DataFrame(rates).T.round(3).to_string())

# %% [markdown]
# ## 3 · Overall agreement and what it hides
#
# Khattab's report says the grader "agrees with the human panel on most verdicts". Compute agreement overall and by language. Agreement is dominated by the larger class (answers people pass), so it can be high while the grader passes a quarter of the bad Arabic answers.

# %%
agree = (calib.human_pass == calib.grader_pass)
print(f"overall agreement {agree.mean():.3f}; Arabic {agree[calib.language == 'ar'].mean():.3f}; English {agree[calib.language == 'en'].mean():.3f}")
false_pass_ar = 1 - rates["ar"]["spec"]
print(f"share of bad Arabic answers the grader passes: {false_pass_ar:.1%}")

# %% [markdown]
# ## 4 · The difference between languages
#
# ✏️ **Exercise** · Return the difference in specificity, English minus Arabic, and its 95% interval (two independent proportions: add the variances).

# %%
def spec_gap(r_en: dict, r_ar: dict):
    # BEGIN SOLUTION
    d = r_en["spec"] - r_ar["spec"]
    se = math.sqrt(r_en["spec"] * (1 - r_en["spec"]) / r_en["n_neg"] + r_ar["spec"] * (1 - r_ar["spec"]) / r_ar["n_neg"])
    return d, d - 1.96 * se, d + 1.96 * se
    # END SOLUTION


# %%
try:
    gap = spec_gap(rates["en"], rates["ar"])
except NotImplementedError:
    gap = tuple(REF["spec_gap"])
U.check("specificity gap", gap, REF["spec_gap"], 1e-9)
print(f"specificity English minus Arabic: {gap[0]:.3f} (95% CI {gap[1]:.3f} to {gap[2]:.3f})")

# %% [markdown]
# **Look at** the interval: it excludes zero. The grader is more lenient with Arabic answers, so Arabic pass rates are inflated more than English ones. This is the unequal error by language the course's responsible-use line asks you to check.
#
# ## 5 · How many more labels, and of which kind
#
# The specificity rests on the answers people **fail**: only 49 in Arabic. To estimate it within ±0.05, you need about $1.96^2\, s(1-s) / 0.05^2$ failed answers. Since people fail about a third of answers, labelling at random wastes most labels on passes. Sampling answers the **grader passed** finds false passes faster.

# %%
s = rates["ar"]["spec"]
need_neg = math.ceil(1.96 ** 2 * s * (1 - s) / 0.05 ** 2)
share_neg = rates["ar"]["n_neg"] / (rates["ar"]["n_neg"] + rates["ar"]["n_pos"])
print(f"Arabic: {need_neg} failed answers needed; at random that is about {math.ceil(need_neg / share_neg)} labels, at SAR 4 each")

# %% [markdown]
# ## ✱ Stretch · Cohen's kappa
#
# Kappa corrects agreement for chance. Compute it per language with `sklearn`-free arithmetic.

# %%
for lang, g in calib.groupby("language"):
    po = (g.human_pass == g.grader_pass).mean()
    pe = g.human_pass.mean() * g.grader_pass.mean() + (1 - g.human_pass.mean()) * (1 - g.grader_pass.mean())
    print(lang, f"agreement {po:.3f}, kappa {(po - pe) / (1 - pe):.3f}")

# %% [markdown]
# ## Check yourself
#
# 1. Agreement is 91% overall. Why is that not enough to trust the grader's pass rates?
# <details><summary>Answer</summary>Agreement mixes the two error rates and is dominated by the common class; the Arabic specificity of about 0.73 means a quarter of bad Arabic answers are passed, which inflates Arabic pass rates.</details>
#
# 2. Which logs may be sent to a hosted grader?
# <details><summary>Answer</summary>Per the NDMO classification applied in the pre-work: the synthetic questions and answers are Public; real applicants' messages with personal data would not be, and would need a grader inside the authority's own environment.</details>
#
# 3. The panel's labels are the reference here. What if the panel itself disagrees?
# <details><summary>Answer</summary>Then measure the panel's agreement first (AE-303 does this with kappa) and treat the human labels as noisy too; the correction of Lab 3.4 assumes the reference is right.</details>
#
# ## Carry forward
#
# Lab 3.4 corrects pass rates with these rates; it recomputes them from `grader_calibration.csv`.
