"""Helpers shared by the DS-403 labs: the Bunyan Building Permits Authority data and reference statistics.

    import bunyan as U

Loading: U.items(), U.results(config, temperature), U.item_means(config, temperature), U.load(name).
Quick mode: DS403_QUICK=1 makes U.pick(full, quick) return the small value (fewer bootstrap and
simulation draws). Safety nets: U.reference(name) returns the result an exercise should produce,
written by _tools/make_reference.py. Self-checks: U.check(label, got, want, tol).

The statistics below are the course's reference versions. A lab asks you to write one of them
yourself first; later labs and days may import it from here.
"""

from __future__ import annotations

import json
import os
import re
import unicodedata
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

LABS = Path(__file__).resolve().parent
DATA = LABS / "data"
QUICK = os.environ.get("DS403_QUICK", "0") == "1"
Z95 = 1.959963984540054


def pick(full, quick):
    """The full value normally, the small one in quick mode."""
    return quick if QUICK else full


def load(name: str) -> pd.DataFrame:
    """A CSV file of labs/data by name, without the extension."""
    return pd.read_csv(DATA / f"{name}.csv")


def items() -> pd.DataFrame:
    return load("items")


def results(config: str | None = None, temperature: float | None = None) -> pd.DataFrame:
    """Item-level logs joined with the question's document and language."""
    r = load("results").merge(items()[["item_id", "doc_id", "category", "language"]], on="item_id")
    if config is not None:
        r = r[r.config == config]
    if temperature is not None:
        r = r[np.isclose(r.temperature, temperature)]
    return r.reset_index(drop=True)


def item_means(config: str, temperature: float = 0.2) -> pd.DataFrame:
    """One row per question: the mean grader verdict over its five samples."""
    r = results(config, temperature)
    return (r.groupby(["item_id", "doc_id", "category", "language"], as_index=False)
             .grader_pass.mean().rename(columns={"grader_pass": "score"}))


def reference(name: str):
    """The reference result of an exercise, for the safety-net cells."""
    return json.loads((DATA / "reference" / f"{name}.json").read_text(encoding="utf-8"))


def show(fig) -> None:
    """Display a figure in a notebook; close it quietly when the lab runs as a script."""
    try:
        from IPython import get_ipython
        from IPython.display import display
        if get_ipython() is not None:
            display(fig)
    except ImportError:
        pass
    import matplotlib.pyplot as plt
    plt.close(fig)


def check(label: str, got, want, tol: float = 1e-9) -> bool:
    ok = bool(np.allclose(np.asarray(got, dtype=float), np.asarray(want, dtype=float), atol=tol, rtol=0))
    print(("✅ " if ok else "❌ ") + label + ("" if ok else f": got {got}, expected {want}"))
    return ok


# ---------------------------------------------------------------- standard errors

def se_formula(x) -> float:
    """Standard error of a mean of item scores, items independent."""
    x = np.asarray(x, dtype=float)
    return float(x.std(ddof=1) / np.sqrt(len(x)))


def clustered_se(x, groups) -> float:
    """Standard error of the mean of x, clustered by groups (the sandwich form, no small-sample factor)."""
    x = np.asarray(x, dtype=float)
    dev = pd.Series(x - x.mean()).groupby(np.asarray(groups)).sum().to_numpy()
    return float(np.sqrt((dev ** 2).sum()) / len(x))


def interval(est: float, se: float, z: float = Z95):
    return (float(est - z * se), float(est + z * se))


# ---------------------------------------------------------------- intervals for a proportion

def wald(k: int, n: int, level: float = 0.95):
    z = stats.norm.ppf(0.5 + level / 2)
    p = k / n
    h = z * np.sqrt(p * (1 - p) / n)
    return (float(p - h), float(p + h))


def wilson(k: int, n: int, level: float = 0.95):
    z = stats.norm.ppf(0.5 + level / 2)
    p = k / n
    centre = (p + z * z / (2 * n)) / (1 + z * z / n)
    h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return (float(centre - h), float(centre + h))


def clopper_pearson(k: int, n: int, level: float = 0.95):
    a = 1 - level
    lo = 0.0 if k == 0 else stats.beta.ppf(a / 2, k, n - k + 1)
    hi = 1.0 if k == n else stats.beta.ppf(1 - a / 2, k + 1, n - k)
    return (float(lo), float(hi))


def beta_interval(k: int, n: int, a0: float = 1.0, b0: float = 1.0, level: float = 0.95):
    """Equal-tailed interval of the Beta(a0 + k, b0 + n - k) posterior. Jeffreys: a0 = b0 = 0.5."""
    a = 1 - level
    post = stats.beta(a0 + k, b0 + n - k)
    return (float(post.ppf(a / 2)), float(post.ppf(1 - a / 2)))


# ---------------------------------------------------------------- comparisons

def paired_table(a: str, b: str, temperature: float = 0.2, data: pd.DataFrame | None = None) -> pd.DataFrame:
    """One row per question with the scores of configurations a and b and their difference b - a."""
    if data is None:
        ta, tb = item_means(a, temperature), item_means(b, temperature)
    else:
        ta = data[data.config == a].rename(columns={"grader_pass": "score"})
        tb = data[data.config == b].rename(columns={"grader_pass": "score"})
    t = ta.merge(tb[["item_id", "score"]], on="item_id", suffixes=(f"_{a}", f"_{b}"))
    t["diff"] = t[f"score_{b}"] - t[f"score_{a}"]
    return t


# ---------------------------------------------------------------- graders

def rates(calib: pd.DataFrame) -> dict:
    """Sensitivity and specificity of the grader from human-labelled verdicts."""
    pos, neg = calib[calib.human_pass == 1], calib[calib.human_pass == 0]
    return {"sens": float(pos.grader_pass.mean()), "spec": float(1 - neg.grader_pass.mean()),
            "n_pos": int(len(pos)), "n_neg": int(len(neg))}


def corrected_rate(p_obs: float, sens: float, spec: float) -> float:
    """The pass rate corrected for grader error (Rogan and Gladen); may leave [0, 1] when the grader is weak."""
    return float((p_obs + spec - 1) / (sens + spec - 1))


# ---------------------------------------------------------------- text

_AR_DIACRITICS = re.compile("[ً-ْٰـ]")


def normalize(text: str) -> str:
    """Normalise a question for overlap checks: Unicode form, Arabic diacritics and tatweel removed,
    alef forms unified, ta marbuta and alef maqsura folded, punctuation and spaces collapsed."""
    t = unicodedata.normalize("NFKC", str(text))
    t = _AR_DIACRITICS.sub("", t)
    t = re.sub("[إأآ]", "ا", t).replace("ة", "ه").replace("ى", "ي")
    t = re.sub(r"[^\w\s]", " ", t.lower())
    return re.sub(r"\s+", " ", t).strip()
