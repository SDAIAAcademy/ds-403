# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy>=2.0", "pandas>=2.2", "scipy>=1.14"]
# ///
"""The capstone analysis: scores with clustered intervals, the paired comparison, the sizing check,
the grader correction and the slices by language, from item-level logs.

    uv run analyze.py logs/run.csv --a baseline --b variant --min-effect 0.03 [--labels labels.csv]

Logs: the columns written by run_eval.py, with a 0/1 column "correct" (or "grader_pass" for a model
grader's verdict). Labels (optional): human verdicts next to the grader's, with the columns
language, human_pass, grader_pass, as in the course's grader_calibration.csv. Writes results.md.
"""

from __future__ import annotations

import argparse
import math
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats


def clustered_se(x, groups) -> float:
    x = np.asarray(x, dtype=float)
    dev = pd.Series(x - x.mean()).groupby(np.asarray(groups)).sum().to_numpy()
    return float(np.sqrt((dev ** 2).sum()) / len(x))


def corrected(p, sens, spec):
    return (p + spec - 1) / (sens + spec - 1)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("logs")
    ap.add_argument("--a", required=True)
    ap.add_argument("--b", required=True)
    ap.add_argument("--min-effect", type=float, default=0.03)
    ap.add_argument("--labels")
    ap.add_argument("--out", default="results.md")
    ap.add_argument("--boot", type=int, default=2000)
    args = ap.parse_args()

    logs = pd.read_csv(args.logs)
    col = "grader_pass" if "grader_pass" in logs.columns else "correct"
    means = logs.groupby(["item_id", "doc_id", "language", "config"], as_index=False)[col].mean()
    lines = [f"# Results\n\nScore: mean of `{col}` per question over its samples; intervals clustered by document.\n",
             "| Configuration | Questions | Score | 95% CI | Design effect |", "|---|---|---|---|---|"]
    for c, g in means.groupby("config"):
        naive = g[col].std(ddof=1) / math.sqrt(len(g))
        cl = clustered_se(g[col], g.doc_id)
        lines.append(f"| {c} | {len(g)} | {g[col].mean():.3f} | {g[col].mean() - 1.96 * cl:.3f} to {g[col].mean() + 1.96 * cl:.3f} | {(cl / naive) ** 2:.2f} |")

    w = means.pivot(index=["item_id", "doc_id", "language"], columns="config", values=col).reset_index()
    d = w[args.b] - w[args.a]
    se = clustered_se(d, w.doc_id)
    lo, hi = d.mean() - 1.96 * se, d.mean() + 1.96 * se
    verdict = "worth the switch" if lo >= args.min_effect else ("better, not shown to matter" if lo > 0 else "no difference shown")
    lines += ["", f"## {args.b} minus {args.a}, paired", "",
              f"{d.mean():+.4f} (95% CI {lo:+.4f} to {hi:+.4f}), clustered by document. Minimum effect {args.min_effect}. Verdict: {verdict}."]

    s = d.std(ddof=1)
    n_need = math.ceil(((stats.norm.ppf(0.975) + stats.norm.ppf(0.8)) * s / args.min_effect) ** 2)
    lines += ["", "## Sizing", "", f"SD of the per-question difference {s:.3f}: {n_need} questions detect {args.min_effect} with 80% power (independent questions; multiply by the design effect of the difference if above 1, and check by simulation)."]

    lines += ["", "## By language", "", "| Configuration | Arabic | English | Gap (ar − en) |", "|---|---|---|---|"]
    for c in (args.a, args.b):
        g = means[means.config == c]
        ar, en = g.language == "ar", g.language == "en"
        m_ar, m_en = g[col][ar].mean(), g[col][en].mean()
        contrib = np.where(ar, (g[col] - m_ar) / ar.sum(), -(g[col] - m_en) / en.sum())
        gse = math.sqrt((pd.Series(contrib).groupby(g.doc_id.to_numpy()).sum() ** 2).sum())
        lines.append(f"| {c} | {m_ar:.3f} | {m_en:.3f} | {m_ar - m_en:+.3f} ({m_ar - m_en - 1.96 * gse:+.3f} to {m_ar - m_en + 1.96 * gse:+.3f}) |")

    if args.labels:
        lab = pd.read_csv(args.labels)
        lines += ["", "## Grader correction (bootstrap over documents and labels)", "", "| Configuration | Language | Observed | Corrected (95% CI) |", "|---|---|---|---|"]
        rng = np.random.default_rng(403)
        for c in (args.a, args.b):
            g = means[means.config == c]
            for lang, gl in g.groupby("language"):
                cal = lab[lab.language == lang]
                h, v = cal.human_pass.to_numpy(), cal.grader_pass.to_numpy()
                sens, spec = v[h == 1].mean(), 1 - v[h == 0].mean()
                by = gl.groupby("doc_id")[col].agg(["sum", "count"])
                su, cn = by["sum"].to_numpy(), by["count"].to_numpy()
                draws = []
                for _ in range(args.boot):
                    k = rng.integers(0, len(su), len(su))
                    j = rng.integers(0, len(h), len(h))
                    sb, cb = v[j][h[j] == 1].mean(), 1 - v[j][h[j] == 0].mean()
                    draws.append(corrected(su[k].sum() / cn[k].sum(), sb, cb))
                p = gl[col].mean()
                q = np.percentile(draws, [2.5, 97.5])
                lines.append(f"| {c} | {lang} | {p:.3f} | {corrected(p, sens, spec):.3f} ({q[0]:.3f} to {q[1]:.3f}) |")

    Path(args.out).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
