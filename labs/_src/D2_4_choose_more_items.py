# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy>=2.0", "pandas>=2.2", "scipy>=1.14", "statsmodels>=0.14", "matplotlib>=3.9"]
# ///

# %% [markdown]
# # Lab 2.4 · Items or samples at fixed cost
#
# Day 2 · Session 4 (Spending the budget) · 25 min.
#
# Furat Al-Zaabi has SAR 6,000 for the next evaluation of configuration D. A new question costs SAR 15 to write and review in both languages; each sample costs one generation and one grader call. You find the design (questions n, samples per question K) with the smallest standard error at that cost, at both temperatures.
#
# **Tasks**
# - [ ] Unit costs and the budget · 3 min
# - [ ] Variance for n items and K samples · 5 min
# - [ ] Every affordable design and its standard error · 7 min
# - [ ] The optimal K by formula · 5 min
# - [ ] The choice at each temperature, with the grader in the cost · 5 min
# - [ ] ✱ Stretch · Reserve part of the budget for human labels of the grader and redo the choice

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
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import bunyan as U

REF = U.reference("d2_4")

# %% [markdown]
# ## 1 · Unit costs and the budget

# %%
costs = json.loads((U.DATA / "costs.json").read_text(encoding="utf-8"))
C_ITEM = costs["new_item_written_and_reviewed"]
C_SAMPLE = costs["answer_generation_per_sample"] + costs["grader_call_per_answer"]
BUDGET = costs["budget_next_evaluation"]
print(json.dumps(costs, indent=1))
print(f"one question with K samples costs {C_ITEM} + {C_SAMPLE:.2f} K")

# %% [markdown]
# ## 2 · Variance for n items and K samples
#
# From Lab 1.3 (configuration D): the between-item and within-item variances at each temperature. If you did not finish Lab 1.3, they are read from its reference file.

# %%
var = U.reference("d1_3")
parts = {t: (var[str(t)]["between"], var[str(t)]["within"]) for t in (0.2, 0.8)}
print(pd.DataFrame(parts, index=["between", "within"]).round(4))

# %% [markdown]
# $$SE(n, K) = \sqrt{\frac{\sigma^2_b + \sigma^2_w / K}{n}}, \qquad n = \left\lfloor \frac{B}{c_{item} + c_{sample} K} \right\rfloor$$
#
# ## 3 · Every affordable design and its standard error
#
# ✏️ **Exercise** · For K from 1 to 30, return a table with K, the affordable n and the SE, for one temperature.

# %%
def designs(between: float, within: float, budget: float = BUDGET, c_item: float = C_ITEM, c_sample: float = C_SAMPLE) -> pd.DataFrame:
    rows = []
    for K in range(1, 31):
        # BEGIN SOLUTION
        n = math.floor(budget / (c_item + c_sample * K))
        rows.append({"K": K, "n": n, "se": math.sqrt((between + within / K) / n)})
        # END SOLUTION
    return pd.DataFrame(rows)


# %%
tables = {}
for t, (b, w) in parts.items():
    try:
        tables[t] = designs(b, w)
    except NotImplementedError:
        tables[t] = pd.DataFrame(REF[str(t)]["designs"])
    best = tables[t].loc[tables[t].se.idxmin()]
    print(f"temperature {t}: best K = {int(best.K)}, n = {int(best.n)}, SE = {best.se:.4f}")
    U.check(f"best K at {t}", best.K, REF[str(t)]["best_k"])
fig, ax = plt.subplots(figsize=(7, 3))
for t, tab in tables.items():
    ax.plot(tab.K, tab.se, marker="o", ms=3, label=f"temperature {t}")
ax.set_xlabel("samples per question K (n falls as K rises)"); ax.set_ylabel("standard error"); ax.legend(frameon=False)
U.show(fig)

# %% [markdown]
# **Look at** the curves: steep from K = 1 to about 5, then nearly flat. Past the minimum, more samples cost questions and the SE rises again slowly.
#
# ## 4 · The optimal K by formula
#
# Minimising the variance at fixed cost gives $K^* = \sqrt{\dfrac{c_{item}}{c_{sample}} \cdot \dfrac{\sigma^2_w}{\sigma^2_b}}$.
#
# ✏️ **Exercise** · Return $K^*$ (not rounded).

# %%
def k_star(between: float, within: float, c_item: float = C_ITEM, c_sample: float = C_SAMPLE) -> float:
    # BEGIN SOLUTION
    return math.sqrt(c_item / c_sample * within / between)
    # END SOLUTION


# %%
for t, (b, w) in parts.items():
    try:
        k = k_star(b, w)
    except NotImplementedError:
        k = REF[str(t)]["k_star"]
    U.check(f"K* at {t}", k, REF[str(t)]["k_star"], 1e-9)
    print(f"temperature {t}: K* = {k:.1f}")

# %% [markdown]
# ## 5 · The choice at each temperature, with the grader in the cost
#
# Questions are expensive (SAR 15) and samples cheap (SAR 0.10), so the optimum has several samples per question, more at 0.8 where sampling noise is larger. If the grader call were forgotten in the cost, K* would look larger still. Compare the SE at K = 5 (today's design) with the optimum.

# %%
for t, tab in tables.items():
    k5 = tab.set_index("K").loc[5]
    best = tab.loc[tab.se.idxmin()]
    print(f"temperature {t}: K=5 gives n={int(k5.n)}, SE {k5.se:.4f}; best K={int(best.K)} gives n={int(best.n)}, SE {best.se:.4f} ({100 * (1 - best.se / k5.se):.1f}% smaller)")
b02, w02 = parts[0.2]
no_grader = (C_ITEM / costs["answer_generation_per_sample"] * w02 / b02) ** 0.5
print(f"K* at 0.2 if the grader call were left out of the cost: {no_grader:.1f}")

# %% [markdown]
# ## ✱ Stretch · Reserve budget for human labels
#
# Day 3 shows that the grader must be checked against people. Reserve SAR 1,200 for 300 human labels (SAR 4 each) and redo the choice with the remaining SAR 4,800.

# %%
left = BUDGET - 300 * costs["human_label_per_verdict"]
rest = pd.DataFrame([{"K": K, "n": math.floor(left / (C_ITEM + C_SAMPLE * K))} for K in range(1, 31)])
rest["se"] = np.sqrt((b02 + w02 / rest.K) / rest.n)
print(rest.loc[rest.se.idxmin()].round(4).to_dict())

# %% [markdown]
# ## Check yourself
#
# 1. Why does the optimum have more samples per question at 0.8 than at 0.2?
# <details><summary>Answer</summary>At 0.8 the within-item variance is larger relative to the between-item variance, so averaging samples removes more noise per riyal.</details>
#
# 2. This calculation ignores clustering by document. What would including it change?
# <details><summary>Answer</summary>The between-item part would be inflated by the design effect, which favours spending on new questions from new documents rather than on samples.</details>
#
# 3. A colleague proposes K = 30 "because samples are cheap". What does the table say?
# <details><summary>Answer</summary>The SE is higher than at the optimum: thirty samples cost SAR 3 per question, which buys fewer questions, and the between-item part dominates.</details>
#
# ## Carry forward
#
# The capstone's sizing plan states n, K and the grader calls with their cost.
