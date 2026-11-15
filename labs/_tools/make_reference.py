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


def day2() -> None:
    import math
    from itertools import combinations
    from scipy import stats
    t = U.paired_table("C", "D", 0.2)
    d = t["diff"].mean()
    se_u = math.sqrt(U.clustered_se(t.score_C, t.doc_id) ** 2 + U.clustered_se(t.score_D, t.doc_id) ** 2)
    se_p = U.clustered_se(t["diff"], t.doc_id)
    lo = d - 1.96 * se_p
    v = "switch" if lo >= 0.03 else ("better, not shown to matter" if lo > 0 else "no difference shown")
    write("d2_1", {"diff": f(d), "unpaired_se": f(se_u), "paired_se": f(se_p), "corr": f(t.score_C.corr(t.score_D)),
                   "lo": f(lo), "hi": f(d + 1.96 * se_p), "verdict": v})

    six = U.load("results_six").merge(U.items()[["item_id", "doc_id"]], on="item_id")
    wide = six.pivot(index=["item_id", "doc_id"], columns="config", values="grader_pass").reset_index()
    cs = list("ABCDEF")
    rows = []
    for a, b in combinations(cs, 2):
        x = wide[b] - wide[a]
        se = U.clustered_se(x, wide.doc_id)
        z = x.mean() / se
        rows.append({"a": a, "b": b, "diff": f(x.mean()), "se": f(se), "z": f(z), "p": f(2 * stats.norm.sf(abs(z)))})
    pairs = pd.DataFrame(rows)
    zb = stats.norm.ppf(1 - 0.05 / 30)
    pairs["bonf_lo"] = pairs["diff"] - zb * pairs.se
    pairs["bonf_hi"] = pairs["diff"] + zb * pairs.se
    rej = np.zeros(15, dtype=bool)
    for k, i in enumerate(np.argsort(pairs.p.to_numpy())):
        if pairs.p.iloc[i] <= 0.05 / (15 - k):
            rej[i] = True
        else:
            break
    pairs["holm_reject"] = rej
    means = wide[cs].mean()
    ranks = []
    for c in cs:
        above = below = 0
        for _, r in pairs[pairs.holm_reject].iterrows():
            if c == r.b:
                above += r["diff"] < 0; below += r["diff"] > 0
            elif c == r.a:
                above += r["diff"] > 0; below += r["diff"] < 0
        ranks.append({"config": c, "pass_rate": f(means[c]), "best_rank": int(1 + above), "worst_rank": int(6 - below)})
    ranks = sorted(ranks, key=lambda r: -r["pass_rate"])
    write("d2_2", {"pairs": pd.DataFrame(rows).to_dict("records"), "adjusted": json.loads(pairs.to_json(orient="records")),
                   "n_holm": int(rej.sum()), "ranks": ranks, "means": {c: f(means[c]) for c in cs}})

    s = t["diff"].std(ddof=1)
    deff = (U.clustered_se(t["diff"], t.doc_id) / U.se_formula(t["diff"])) ** 2
    z = stats.norm.ppf(0.975) + stats.norm.ppf(0.8)
    n_ind = math.ceil((z * s / 0.03) ** 2)
    n_need = math.ceil(n_ind * max(deff, 1.0))
    write("d2_3", {"sd": f(s), "deff": f(deff), "n_independent": n_ind, "n_needed": n_need,
                   "simulated": [{"questions": 300, "power": 0.4}, {"questions": n_need, "power": 0.8}, {"questions": 900, "power": 0.97}]})

    costs = json.loads((U.DATA / "costs.json").read_text(encoding="utf-8"))
    ci = costs["new_item_written_and_reviewed"]
    cs_ = costs["answer_generation_per_sample"] + costs["grader_call_per_answer"]
    v13 = json.loads((OUT / "d1_3.json").read_text(encoding="utf-8"))
    out = {}
    for tt in ("0.2", "0.8"):
        b, w = v13[tt]["between"], v13[tt]["within"]
        ds = []
        for K in range(1, 31):
            n = math.floor(costs["budget_next_evaluation"] / (ci + cs_ * K))
            ds.append({"K": K, "n": n, "se": f(math.sqrt((b + w / K) / n))})
        best = min(ds, key=lambda r: r["se"])
        out[tt] = {"designs": ds, "best_k": best["K"], "k_star": f(math.sqrt(ci / cs_ * w / b))}
    write("d2_4", out)


if __name__ == "__main__":
    steps = {"1": day1, "2": day2}
    for k in (sys.argv[1:] or sorted(steps)):
        steps[k]()
        print("day", k, "references written")
