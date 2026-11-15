# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy>=2.0", "pandas>=2.2", "scipy>=1.14", "statsmodels>=0.14", "matplotlib>=3.9"]
# ///

# %% [markdown]
# # Lab 4.2 · Auditing the leaderboard
#
# Day 4 · Session 2 (Auditing a report) · 25 min.
#
# Khattab's leaderboard (`data/leaderboard_report.md`) makes eight claims. Dr. Nadeen wants an audit memo before she decides: each claim classed as **supported** (the data back it at the stated strength), **unsupported** (the data available contradict it or do not back it as stated) or **untestable** (no data the authority holds could decide it), each with the re-analysis that decides it.
#
# **Tasks**
# - [ ] Read the report and its eight claims · 3 min
# - [ ] The evidence each claim needs · 4 min
# - [ ] Re-analyse the testable claims · 10 min
# - [ ] Classify all eight · 4 min
# - [ ] The audit memo · 4 min
# - [ ] ✱ Stretch · Rewrite one unsupported claim so that the data supports it

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

REF = U.reference("d4_2")

# %% [markdown]
# ## 1 · The report and its claims

# %%
print((U.DATA / "leaderboard_report.md").read_text(encoding="utf-8"))
claims = U.load("leaderboard_claims")
print(claims.to_string(index=False))

# %% [markdown]
# ## 2 · The evidence each claim needs
#
# | Claim | What would decide it |
# |---|---|
# | C1 | D minus C at equal budgets, paired and clustered, on questions not in D's tuning examples |
# | C2 | B minus A, paired and clustered, temperature 0.2 |
# | C3 | B minus A at temperature 0.8 |
# | C4 | An upper bound on D's unsafe rate from 40 out of 40 |
# | C5 | The grader's specificity by language and what correction does |
# | C6 | C's Arabic minus English gap with a clustered interval |
# | C7 | Results on the 2027 regulations |
# | C8 | Applicants' preferences between D's and C's answers |
#
# ## 3 · Re-analyse the testable claims
#
# The helper `paired(a, b, temperature, keep)` returns the paired clustered difference b minus a and its 95% interval.

# %%
r41 = U.reference("d4_1")
leaked = set(r41["leaked"])
CLAIMED_LEAD = r41["report_D"] - r41["report_C"]   # the lead the report claims for D over C


def paired(a: str, b: str, temperature: float = 0.2, keep=None):
    t = U.paired_table(a, b, temperature)
    if keep is not None:
        t = t[t.item_id.isin(keep)]
    d, se = t["diff"].mean(), U.clustered_se(t["diff"], t.doc_id)
    return d, d - 1.96 * se, d + 1.96 * se


clean_ids = set(U.items().item_id) - leaked
evidence = {}
evidence["C1"] = paired("C", "D", 0.2, clean_ids)
evidence["C2"] = paired("A", "B", 0.2)
evidence["C3"] = paired("A", "B", 0.8)
evidence["C4"] = 1 - 0.05 ** (1 / 40)
calib = U.load("grader_calibration")
evidence["C5"] = {lang: U.rates(g)["spec"] for lang, g in calib.groupby("language")}
r43 = U.reference("d4_3")
evidence["C6"] = r43["gap"]["C"]
for k, v in evidence.items():
    print(k, np.round(v, 4) if not isinstance(v, dict) else {a: round(b, 3) for a, b in v.items()})

# %% [markdown]
# ## 4 · Classify all eight
#
# ✏️ **Exercise** · Return a dict from claim id to `"supported"`, `"unsupported"` or `"untestable"`, using the evidence above. For C6, the gap and its SE are `evidence["C6"]` (`[gap, se]`).

# %%
def classify(ev: dict) -> dict:
    # BEGIN SOLUTION
    out = {}
    d, lo, hi = ev["C1"]
    out["C1"] = "supported" if lo > 0 and lo <= CLAIMED_LEAD <= hi else "unsupported"
    out["C2"] = "supported" if ev["C2"][1] > 0 else "unsupported"
    out["C3"] = "supported" if ev["C3"][1] > 0 else "unsupported"
    out["C4"] = "unsupported"                                  # 40/40 bounds the rate below about 7%, not at 0
    out["C5"] = "unsupported" if min(ev["C5"].values()) < 0.85 else "supported"
    gap, se = ev["C6"]
    out["C6"] = "unsupported" if abs(gap) - 1.96 * se > 0 else "supported"
    out["C7"] = "untestable"
    out["C8"] = "untestable"
    return out
    # END SOLUTION


# %%
try:
    verdicts = classify(evidence)
except NotImplementedError:
    verdicts = REF["verdicts"]
assert verdicts == REF["verdicts"], verdicts
print(pd.Series(verdicts).to_string())

# %% [markdown]
# ## 5 · The audit memo
#
# One line per claim: the class, the number that decides it, and what the claim should have said.

# %%
d1, lo1, hi1 = evidence["C1"]
lines = [
    "Audit memo: Watad configuration leaderboard, October 2026",
    "To: Dr. Nadeen Al-Shaya. From: Qamar Al-Saqri, evaluation statistician.",
    "",
    f"C1 {verdicts['C1']}: D was scored as best of 5 and C as mean of 5; D's prompt was tuned on 12 variants and 48 test questions. "
    f"At equal budgets on clean questions D minus C is {100 * d1:.1f} points (95% CI {100 * lo1:.1f} to {100 * hi1:.1f}).",
    f"C2 {verdicts['C2']}: B minus A {100 * evidence['C2'][0]:.1f} points (95% CI {100 * evidence['C2'][1]:.1f} to {100 * evidence['C2'][2]:.1f}), paired and clustered.",
    f"C3 {verdicts['C3']}: at temperature 0.8, B minus A {100 * evidence['C3'][0]:.1f} points (95% CI {100 * evidence['C3'][1]:.1f} to {100 * evidence['C3'][2]:.1f}).",
    f"C4 {verdicts['C4']}: 40 of 40 bounds D's unsafe rate below {100 * evidence['C4']:.1f}% at 95%; it does not show 'never'.",
    f"C5 {verdicts['C5']}: overall agreement is 91%, but the grader's Arabic specificity is {evidence['C5']['ar']:.2f} against {evidence['C5']['en']:.2f} in English; Arabic rates need correction.",
    f"C6 {verdicts['C6']}: C's Arabic minus English gap is {100 * evidence['C6'][0]:.2f} points (95% CI {100 * (evidence['C6'][0] - 1.96 * evidence['C6'][1]):.2f} to {100 * (evidence['C6'][0] + 1.96 * evidence['C6'][1]):.2f}); "
    f"after grader correction the point gap is {100 * r43['corrected_gap']['C']:.1f} points, with a wide interval ({100 * r43['corrected_gap_ci']['C'][0]:.1f} to {100 * r43['corrected_gap_ci']['C'][1]:.1f}) until more Arabic answers are labelled.",
    f"C7 {verdicts['C7']}: no data from the 2027 regulations; size a new set (Lab 2.3).",
    f"C8 {verdicts['C8']}: no preference data; the logs hold grader verdicts, not applicants' choices.",
]
memo = "\n".join(lines)
print(memo)
out = Path("artifacts/D4_2"); out.mkdir(parents=True, exist_ok=True)
(out / "audit_memo.txt").write_text(memo, encoding="utf-8")

# %% [markdown]
# ## ✱ Stretch · Rewrite a claim
#
# Rewrite C4 so that the data supports it, for example: "D gave no unsafe answer on the 40-question safety set; with 95% confidence its unsafe rate on such questions is below 7.2%."
#
# ## Check yourself
#
# 1. Why is C1 unsupported rather than untestable?
# <details><summary>Answer</summary>The logs can test it: at equal budgets and on clean questions the lead is a fraction of what is claimed and its interval includes zero. The data contradict the claim as stated.</details>
#
# 2. What makes C7 untestable and not simply unsupported?
# <details><summary>Answer</summary>No data the authority holds come from the 2027 regulations; the current set is a different population. A new evaluation could test it.</details>
#
# 3. C2 is supported. Does the audit endorse B?
# <details><summary>Answer</summary>No: the audit classes claims. Supported means the data back B over A at the stated strength, nothing about B against C or D.</details>
#
# ## Carry forward
#
# `artifacts/D4_2/audit_memo.txt` is the evidence for LO5. Its findings feed the reporting standard in Lab 4.4.
