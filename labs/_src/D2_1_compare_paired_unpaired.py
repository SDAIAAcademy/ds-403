# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy>=2.0", "pandas>=2.2", "scipy>=1.14", "statsmodels>=0.14", "matplotlib>=3.9"]
# ///

# %% [markdown]
# # Lab 2.1 · Paired against unpaired
#
# Day 2 · Session 1 (Paired designs) · 25 min.
#
# Dr. Nadeen Al-Shaya will switch Watad from configuration C to D only if D is at least three points better. Both answered the same 600 questions. You compare them twice, as if the questions were different (unpaired) and as they are (paired), explain the two widths from the correlation, and write the decision note the plan of Lab 1.4 calls for.
#
# **Tasks**
# - [ ] One row per question with both configurations · 3 min
# - [ ] The unpaired interval · 4 min
# - [ ] The paired interval, clustered by document · 7 min
# - [ ] The correlation explains the widths · 5 min
# - [ ] A decision note with a verdict · 6 min
# - [ ] ✱ Stretch · Repeat at temperature 0.8 and say whether the verdict holds

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
import numpy as np
import pandas as pd
import bunyan as U

REF = U.reference("d2_1")
MIN_EFFECT = 0.03

# %% [markdown]
# ## 1 · One row per question with both configurations
#
# `U.paired_table("C", "D")` returns one row per question: the mean of five samples for C and for D at temperature 0.2, and `diff` = D minus C.

# %%
t = U.paired_table("C", "D", 0.2)
print(t.head())
print(f"C {t.score_C.mean():.4f}   D {t.score_D.mean():.4f}   D minus C {t['diff'].mean():.4f}")

# %% [markdown]
# ## 2 · The unpaired interval
#
# Treat the two scores as if they came from different question sets: $SE = \sqrt{SE_C^2 + SE_D^2}$. Use the clustered standard error of each (Day 1).
#
# ✏️ **Exercise** · Return the unpaired clustered SE of the difference.

# %%
def unpaired_se(t: pd.DataFrame) -> float:
    # BEGIN SOLUTION
    return float(np.sqrt(U.clustered_se(t.score_C, t.doc_id) ** 2 + U.clustered_se(t.score_D, t.doc_id) ** 2))
    # END SOLUTION


# %%
try:
    se_u = unpaired_se(t)
except NotImplementedError:
    se_u = REF["unpaired_se"]
U.check("unpaired SE", se_u, REF["unpaired_se"], 1e-9)
d = t["diff"].mean()
print(f"unpaired: {d:.4f} ± {1.96 * se_u:.4f}")

# %% [markdown]
# ## 3 · The paired interval, clustered by document
#
# Work on the per-question differences: their mean is the same, but their standard error is that of one column, `diff`, clustered by document.
#
# ✏️ **Exercise** · Return the paired clustered SE.

# %%
def paired_se(t: pd.DataFrame) -> float:
    # BEGIN SOLUTION
    return U.clustered_se(t["diff"], t.doc_id)
    # END SOLUTION


# %%
try:
    se_p = paired_se(t)
except NotImplementedError:
    se_p = REF["paired_se"]
U.check("paired clustered SE", se_p, REF["paired_se"], 1e-9)
lo, hi = d - 1.96 * se_p, d + 1.96 * se_p
print(f"paired: {d:.4f}, 95% CI {lo:.4f} to {hi:.4f}; the interval is {se_u / se_p:.1f} times narrower than unpaired")

# %% [markdown]
# ## 4 · The correlation explains the widths
#
# $\mathrm{Var}(D - C) = \mathrm{Var}(D) + \mathrm{Var}(C) - 2\,\mathrm{Cov}(C, D)$. Questions that are hard for C are hard for D, so the covariance is large and pairing removes it. Clustering matters less for the difference: the document effect is shared by both and cancels.

# %%
corr = t.score_C.corr(t.score_D)
naive_paired = U.se_formula(t["diff"])
table = pd.DataFrame({
    "analysis": ["unpaired, naive", "unpaired, clustered", "paired, naive", "paired, clustered"],
    "SE": [np.sqrt(U.se_formula(t.score_C) ** 2 + U.se_formula(t.score_D) ** 2), se_u, naive_paired, se_p],
})
table["half-width (points)"] = 100 * 1.96 * table.SE
print(table.round(4).to_string(index=False))
print(f"correlation of C and D over questions: {corr:.3f}")
U.check("correlation", corr, REF["corr"], 1e-9)

# %% [markdown]
# **Look at** the four rows. Clustering widens the unpaired interval; pairing narrows the interval far more, and once paired, clustering barely matters, because each document's effect is shared by C and D.
#
# ## 5 · A decision note with a verdict
#
# The plan's rule: if the whole interval is above the minimum effect, switch; if it is above 0 but includes values below the minimum effect, D is better but not shown to be better by enough; if it includes 0, no difference is shown.
#
# ✏️ **Exercise** · Return the verdict string: `"switch"`, `"better, not shown to matter"` or `"no difference shown"`.

# %%
def verdict(lo: float, hi: float, min_effect: float) -> str:
    # BEGIN SOLUTION
    if lo >= min_effect:
        return "switch"
    if lo > 0:
        return "better, not shown to matter"
    return "no difference shown"
    # END SOLUTION


# %%
try:
    v = verdict(lo, hi, MIN_EFFECT)
except NotImplementedError:
    v = REF["verdict"]
assert v == REF["verdict"], v
note = f"""Decision note: D against C (plan of Lab 1.4)
Paired difference D minus C: {100 * d:.1f} points, 95% CI {100 * lo:.1f} to {100 * hi:.1f}, clustered by document, 600 questions, 5 samples, temperature 0.2.
Minimum effect: {100 * MIN_EFFECT:.0f} points. Verdict: {v}.
The unpaired analysis would have given +/- {100 * 1.96 * se_u:.1f} points and no conclusion."""
print(note)
out = Path("artifacts/D2_1"); out.mkdir(parents=True, exist_ok=True)
(out / "decision_note.txt").write_text(note, encoding="utf-8")

# %% [markdown]
# ## ✱ Stretch · Temperature 0.8
#
# Repeat sections 3 and 5 at temperature 0.8. Does the verdict hold?

# %%
t8 = U.paired_table("C", "D", 0.8)
d8, s8 = t8["diff"].mean(), U.clustered_se(t8["diff"], t8.doc_id)
print(f"at 0.8: {100 * d8:.1f} points, 95% CI {100 * (d8 - 1.96 * s8):.1f} to {100 * (d8 + 1.96 * s8):.1f}")

# %% [markdown]
# ## Check yourself
#
# 1. Why is the paired interval narrower although it uses the same 600 questions?
# <details><summary>Answer</summary>Each question's difficulty affects C and D alike (correlation about 0.83); the difference removes that shared part, leaving less variance.</details>
#
# 2. Why does clustering widen the unpaired interval but hardly the paired one?
# <details><summary>Answer</summary>The document effect moves both configurations together, so it inflates each score's variance but cancels in their difference.</details>
#
# 3. The verdict is "better, not shown to matter". What can Dr. Nadeen do?
# <details><summary>Answer</summary>Keep C (the cheaper switch), or commission a larger evaluation sized in Lab 2.3 to tell whether the gain reaches three points. Day 4 adds another reason for caution about D.</details>
#
# ## Carry forward
#
# The note is in `artifacts/D2_1/decision_note.txt`. Lab 2.3 sizes an evaluation from this pilot.
