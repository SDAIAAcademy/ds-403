# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy>=2.0", "pandas>=2.2", "scipy>=1.14", "statsmodels>=0.14", "matplotlib>=3.9"]
# ///

# %% [markdown]
# # Lab 4.3 · Arabic and English
#
# Day 4 · Session 3 (Slicing by language) · 25 min.
#
# Watad serves applicants in both languages; a configuration that is weaker in Arabic must not hide behind its average. You report each configuration's Arabic and English pass rates with clustered intervals, test the gap using the documents that have questions in both languages, and show how the grader correction of Day 3 changes the gap.
#
# **Tasks**
# - [ ] Pass rates by language for four configurations · 4 min
# - [ ] Clustered intervals per language · 5 min
# - [ ] The gap and its interval · 7 min
# - [ ] The gap after grader correction · 5 min
# - [ ] The slice table for the report · 4 min
# - [ ] ✱ Stretch · Slice by category as well and adjust for eight comparisons

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

REF = U.reference("d4_3")

# %% [markdown]
# ## 1 · Pass rates by language

# %%
scores = {c: U.item_means(c, 0.2) for c in "ABCD"}
rates = pd.DataFrame({c: t.groupby("language").score.mean() for c, t in scores.items()}).T
rates["average"] = [t.score.mean() for t in scores.values()]
print(rates.round(4).to_string())

# %% [markdown]
# ## 2 · Clustered intervals per language
#
# Within one language, questions still cluster by document.

# %%
rows = []
for c, t in scores.items():
    for lang in ("ar", "en"):
        g = t[t.language == lang]
        se = U.clustered_se(g.score, g.doc_id)
        rows.append({"config": c, "language": lang, "rate": g.score.mean(), "lo": g.score.mean() - 1.96 * se,
                     "hi": g.score.mean() + 1.96 * se, "questions": len(g), "documents": g.doc_id.nunique()})
by_lang = pd.DataFrame(rows)
print(by_lang.round(4).to_string(index=False))

# %% [markdown]
# ## 3 · The gap and its interval
#
# The gap is the Arabic rate minus the English rate. Most documents have questions in both languages, so the two rates are **not** independent: a hard document lowers both. Write the gap as a sum over questions of weights times deviations, $+1/n_{ar}$ for Arabic questions and $-1/n_{en}$ for English ones, and cluster that sum by document.
#
# ✏️ **Exercise** · Return `(gap, se)` for one configuration's table.

# %%
def language_gap(t: pd.DataFrame):
    # BEGIN SOLUTION
    ar, en = t.language == "ar", t.language == "en"
    m_ar, m_en = t.score[ar].mean(), t.score[en].mean()
    contrib = np.where(ar, (t.score - m_ar) / ar.sum(), -(t.score - m_en) / en.sum())
    per_doc = pd.Series(contrib).groupby(t.doc_id.to_numpy()).sum()
    return float(m_ar - m_en), float(np.sqrt((per_doc ** 2).sum()))
    # END SOLUTION


# %%
gaps = []
for c, t in scores.items():
    try:
        g, se = language_gap(t)
    except NotImplementedError:
        g, se = REF["gap"][c]
    gaps.append({"config": c, "gap": g, "lo": g - 1.96 * se, "hi": g + 1.96 * se, "p": 2 * stats.norm.sf(abs(g / se))})
gaps = pd.DataFrame(gaps)
U.check("C's language gap", gaps.set_index("config").loc["C", "gap"], REF["gap"]["C"][0], 1e-9)
print(gaps.round(4).to_string(index=False))

# %% [markdown]
# **Look at** C: its average (72.1%) is close to D's, but its Arabic rate is several points below its English one, and the interval just excludes zero.
#
# ## 4 · The gap after grader correction
#
# The grader is more lenient in Arabic (Lab 3.3), so observed Arabic rates are inflated and the observed gap is too small. Correct both languages, and bootstrap documents and calibration verdicts together.
#
# ✏️ **Exercise** · Return `B` corrected gaps (Arabic minus English) for one configuration.

# %%
calib = U.load("grader_calibration")
cal = {lang: (g.human_pass.to_numpy(), g.grader_pass.to_numpy()) for lang, g in calib.groupby("language")}
r0 = {lang: U.rates(g) for lang, g in calib.groupby("language")}


def corrected_gaps(t: pd.DataFrame, B: int, rng: np.random.Generator) -> np.ndarray:
    docs = t.doc_id.unique()
    by = {lang: t[t.language == lang].groupby("doc_id").score.agg(["sum", "count"]).reindex(docs, fill_value=0) for lang in ("ar", "en")}
    out = np.empty(B)
    for b in range(B):
        pick = rng.integers(0, len(docs), size=len(docs))
        theta = {}
        for lang in ("ar", "en"):
            # BEGIN SOLUTION
            p = by[lang]["sum"].to_numpy()[pick].sum() / by[lang]["count"].to_numpy()[pick].sum()
            h, v = cal[lang]
            j = rng.integers(0, len(h), size=len(h))
            sens, spec = v[j][h[j] == 1].mean(), 1 - v[j][h[j] == 0].mean()
            theta[lang] = (p + spec - 1) / (sens + spec - 1)
            # END SOLUTION
        out[b] = theta["ar"] - theta["en"]
    return out


# %%
B = U.pick(3000, 500)
rng = np.random.default_rng(403)
rows = []
for c, t in scores.items():
    point = (U.corrected_rate(t[t.language == "ar"].score.mean(), r0["ar"]["sens"], r0["ar"]["spec"])
             - U.corrected_rate(t[t.language == "en"].score.mean(), r0["en"]["sens"], r0["en"]["spec"]))
    try:
        lo, hi = np.percentile(corrected_gaps(t, B, rng), [2.5, 97.5])
    except NotImplementedError:
        lo, hi = REF["corrected_gap_ci"][c]
    rows.append({"config": c, "corrected gap": point, "lo": lo, "hi": hi})
cgaps = pd.DataFrame(rows)
U.check("C's corrected gap", cgaps.set_index("config").loc["C", "corrected gap"], REF["corrected_gap"]["C"], 1e-9)
print(cgaps.round(4).to_string(index=False))

# %% [markdown]
# ## 5 · The slice table for the report

# %%
rows = []
for c in "ABCD":
    row = {"config": c}
    for lang, col in (("ar", "Arabic"), ("en", "English")):
        r = by_lang.query("config == @c and language == @lang").iloc[0]
        row[col] = f"{100 * r.rate:.1f} ({100 * r.lo:.1f} to {100 * r.hi:.1f})"
    gr = gaps.set_index("config").loc[c]
    cg = cgaps.set_index("config").loc[c]
    row["gap, observed"] = f"{100 * gr.gap:+.2f} ({100 * gr.lo:+.2f} to {100 * gr.hi:+.2f})"
    row["gap, corrected"] = f"{100 * cg['corrected gap']:+.1f} ({100 * cg.lo:+.1f} to {100 * cg.hi:+.1f})"
    rows.append(row)
table = pd.DataFrame(rows).set_index("config")
print(table.to_string())
out = Path("artifacts/D4_3"); out.mkdir(parents=True, exist_ok=True)
table.to_csv(out / "language_slices.csv")

# %% [markdown]
# ## ✱ Stretch · Slice by category
#
# Eight categories: report C's rate per category with clustered intervals, and widen them with Bonferroni for eight comparisons. Which categories cannot be told apart from the average?

# %%
z8 = stats.norm.ppf(1 - 0.05 / 16)
t = scores["C"]
for cat, g in t.groupby("category"):
    se = U.clustered_se(g.score, g.doc_id)
    print(f"{cat:11s} {g.score.mean():.3f}  ({g.score.mean() - z8 * se:.3f} to {g.score.mean() + z8 * se:.3f})")

# %% [markdown]
# ## Check yourself
#
# 1. C's average is close to D's. Why is that not enough for the release decision?
# <details><summary>Answer</summary>C is clearly weaker in Arabic. Applicants who write in Arabic would get a worse service, and the average hides it.</details>
#
# 2. Why cluster the gap by document instead of treating the two languages as independent samples?
# <details><summary>Answer</summary>Most documents have questions in both languages; a hard document lowers both rates, and that shared part should not count as evidence about the gap.</details>
#
# 3. What did the grader correction do to C's gap?
# <details><summary>Answer</summary>It widened the point estimate, because the lenient Arabic grader had been passing some of C's bad Arabic answers. The corrected interval is much wider, carrying the calibration's uncertainty, and now includes zero: the next step is more Arabic labels, not a conclusion that the gap is gone.</details>
#
# ## Carry forward
#
# The slice table is a required field of the reporting standard drafted in Lab 4.4.
