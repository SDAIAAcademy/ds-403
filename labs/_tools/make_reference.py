"""Write the reference results of the labs' exercises into labs/data/reference/*.json.

    cd labs
    uv run python _tools/make_reference.py

The safety-net cells of the notebooks read these files when an exercise is not done yet, and the
solutions assert that they reproduce them. The values are computed here from the data with the
helper module's reference statistics, independently of the notebooks.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

LABS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(LABS))
import bunyan as U  # noqa: E402

OUT = U.DATA / "reference"


def write(name: str, obj) -> None:
    OUT.mkdir(exist_ok=True)
    (OUT / f"{name}.json").write_text(json.dumps(obj, indent=1, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def f(x):
    return float(round(float(x), 10))


def day1() -> None:
    r = U.results("D", 0.2)
    x = r[r["sample"] == 1].sort_values("item_id").grader_pass.to_numpy()
    p, n = x.mean(), len(x)
    se = np.sqrt(p * (1 - p) / n)
    write("d1_1", {"verdicts": x.tolist(), "p": f(p), "se": f(se), "lo": f(p - 1.96 * se), "hi": f(p + 1.96 * se),
                   "line": f"D: {100 * p:.1f}% (95% CI {100 * (p - 1.96 * se):.1f} to {100 * (p + 1.96 * se):.1f}), {n} questions, 1 sample each, temperature 0.2"})

    ref = {}
    for c in "ABCD":
        t = U.item_means(c, 0.2)
        naive, clu = U.se_formula(t.score), U.clustered_se(t.score, t.doc_id)
        ref[c] = {"mean": f(t.score.mean()), "naive_se": f(naive), "clustered_se": f(clu),
                  "deff": f((clu / naive) ** 2), "n_eff": f(len(t) / (clu / naive) ** 2)}
    write("d1_2", ref)

    ref = {}
    for t in (0.2, 0.8):
        m = U.results("D", t).pivot(index="item_id", columns="sample", values="grader_pass").to_numpy(dtype=float)
        within = m.var(axis=1, ddof=1).mean()
        vm = m.mean(axis=1).var(ddof=1)
        between = vm - within / 5
        ref[str(t)] = {"within": f(within), "between": f(between), "var_means": f(vm),
                       **{f"se_k{K}": f(np.sqrt((between + within / K) / 600)) for K in (1, 5, 20)},
                       "pass_at_5": f(m.max(axis=1).mean()), "pass_hat_5": f(m.min(axis=1).mean()), "mean": f(m.mean())}
    write("d1_3", ref)

    template = json.loads((U.DATA / "plan_template.json").read_text(encoding="utf-8"))
    required = ["title", "owner", "date_committed", "question", "systems", "population", "items", "unit_of_analysis",
                "primary_metric", "grader", "samples_per_item", "temperature", "clustering", "comparison",
                "minimum_effect", "alpha", "power", "decision_rule", "slices", "exclusions"]
    problems = [f"missing: {k}" for k in required] + ["minimum_effect must be a positive number",
                                                      "alpha must be in (0, 0.1]", "clustering must name the source documents",
                                                      "slices must include language"]
    write("d1_4", {"template_problems": problems, "n_template_problems": len(problems),
                   "false_win_single": 0.05, "false_win_any": 0.16})
    plan = {**template,
            "title": "Watad release: configuration D against configuration C",
            "owner": "Qamar Al-Saqri, evaluation statistician", "date_committed": "2026-11-15",
            "question": "Is D's pass rate at least three points higher than C's on the regulation task set?",
            "systems": ["C", "D"],
            "population": "Questions applicants ask about the authority's building regulations, Arabic and English",
            "items": "The 600 questions of the regulation task set, 80 documents", "unit_of_analysis": "question",
            "primary_metric": "mean grader pass rate per sample",
            "grader": "the model grader; corrected with the human-labelled verdicts as a secondary analysis",
            "samples_per_item": 5, "temperature": 0.2, "clustering": "standard errors clustered by source document",
            "comparison": "paired difference D minus C over the same questions", "minimum_effect": 0.03,
            "alpha": 0.05, "power": 0.8,
            "decision_rule": "Release D if the lower end of the 95% interval of D minus C is above 0; call it worth the switch only if the interval also includes or exceeds the minimum effect of 0.03; otherwise keep C",
            "slices": ["language", "category"], "exclusions": "none; questions that fail to run are scored as failures",
            "secondary_metrics": ["pass rate corrected for grader error, by language", "safety set, 40 items"]}
    write("plan_C_vs_D", plan)


if __name__ == "__main__":
    steps = {"1": day1}
    for k in (sys.argv[1:] or sorted(steps)):
        steps[k]()
        print("day", k, "references written")
