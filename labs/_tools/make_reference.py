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
                   # the powers printed by the Lab 2.3 solution in full mode (2,000 simulations, seed 403)
                   "simulated": [{"questions": 300, "power": 0.71}, {"questions": n_need, "power": 0.846}, {"questions": 900, "power": 0.994}]})

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


def day3() -> None:
    import math
    from scipy import stats
    methods = {"Wald": U.wald, "Wilson": U.wilson, "Clopper-Pearson": U.clopper_pearson,
               "Jeffreys": lambda k, n: U.beta_interval(k, n, 0.5, 0.5)}
    exact = {}
    for name, m in methods.items():
        exact[name] = {}
        for n in (20, 40, 80, 120, 200):
            ks = np.arange(n + 1)
            ivs = [m(int(j), n) for j in ks]
            exact[name][str(n)] = {str(p): f(stats.binom.pmf(ks, n, p)[np.array([lo <= p <= hi for lo, hi in ivs])].sum())
                                   for p in (0.02, 0.05, 0.5, 0.95, 0.98)}
    write("d3_1", {"wald_38_40": list(U.wald(38, 40)), "wilson_38_40": list(U.wilson(38, 40)), "exact": exact})

    counts = U.load("safety_results").groupby("config").safe.agg(["sum", "count"])
    cp, beta = {}, {}
    for c, r in counts.iterrows():
        k, n = int(r["sum"]), int(r["count"])
        cp[c] = list(U.clopper_pearson(k, n))
        beta[c] = {}
        for prior, (a, b) in {"uniform": (1, 1), "Jeffreys": (0.5, 0.5)}.items():
            post = stats.beta(a + k, b + n - k)
            beta[c][prior] = [f(post.mean()), f(post.ppf(0.025)), f(post.ppf(0.975))]
    write("d3_2", {"counts": {c: int(r["sum"]) for c, r in counts.iterrows()}, "cp": cp, "beta": beta,
                   "one_sided_lower_40": f(0.05 ** (1 / 40))})

    calib = U.load("grader_calibration")
    ref = {}
    for lang, g in calib.groupby("language"):
        pos, neg = g[g.human_pass == 1], g[g.human_pass == 0]
        tp, tn = int(pos.grader_pass.sum()), int((neg.grader_pass == 0).sum())
        sl, sh = U.wilson(tp, len(pos)); cl, ch = U.wilson(tn, len(neg))
        ref[lang] = {"sens": f(tp / len(pos)), "sens_lo": f(sl), "sens_hi": f(sh), "spec": f(tn / len(neg)),
                     "spec_lo": f(cl), "spec_hi": f(ch), "n_pos": len(pos), "n_neg": len(neg),
                     "agreement": f((g.human_pass == g.grader_pass).mean())}
    d = ref["en"]["spec"] - ref["ar"]["spec"]
    se = math.sqrt(ref["en"]["spec"] * (1 - ref["en"]["spec"]) / ref["en"]["n_neg"] + ref["ar"]["spec"] * (1 - ref["ar"]["spec"]) / ref["ar"]["n_neg"])
    ref["spec_gap"] = [f(d), f(d - 1.96 * se), f(d + 1.96 * se)]
    ref["agreement"] = f((calib.human_pass == calib.grader_pass).mean())
    write("d3_3", ref)

    rates = {lang: U.rates(g) for lang, g in calib.groupby("language")}
    point, boot, observed = {}, {}, {}
    rng = np.random.default_rng(403)
    for c in ("C", "D"):
        t = U.item_means(c, 0.2)
        for lang in ("ar", "en"):
            g = t[t.language == lang]
            p = g.score.mean()
            r = rates[lang]
            point[f"{c}_{lang}"] = f(U.corrected_rate(p, r["sens"], r["spec"]))
            se = U.clustered_se(g.score, g.doc_id)
            observed[f"{c}_{lang}"] = [f(p), f(p - 1.96 * se), f(p + 1.96 * se)]
            by_doc = g.groupby("doc_id").score.agg(["sum", "count"])
            sums, cnts = by_doc["sum"].to_numpy(), by_doc["count"].to_numpy()
            cal = calib[calib.language == lang]
            h, v = cal.human_pass.to_numpy(), cal.grader_pass.to_numpy()
            out = np.empty(4000)
            for b in range(4000):
                pick = rng.integers(0, len(sums), size=len(sums))
                pb = sums[pick].sum() / cnts[pick].sum()
                j = rng.integers(0, len(h), size=len(h))
                hb, vb = h[j], v[j]
                sens, spec = vb[hb == 1].mean(), 1 - vb[hb == 0].mean()
                out[b] = (pb + spec - 1) / (sens + spec - 1)
            boot[f"{c}_{lang}"] = [f(np.percentile(out, 2.5)), f(np.percentile(out, 97.5))]
    write("d3_4", {"rates": rates, "point": point, "boot": boot, "observed": observed})


def day4() -> None:
    items = U.items()
    tune = U.load("tuning_examples")
    seen = {U.normalize(q) for q in tune.question}
    leaked = sorted(items.loc[items.question.map(U.normalize).isin(seen), "item_id"])
    cvo = []
    for c in "ABCD":
        t = U.item_means(c, 0.2)
        on = t.item_id.isin(leaked)
        cvo.append({"config": c, "overlap": f(t[on].score.mean()), "clean": f(t[~on].score.mean()),
                    "gap": f(t[on].score.mean() - t[~on].score.mean())})
    rep = {}
    for c in "ABCD":
        m = U.results(c, 0.2).pivot(index="item_id", columns="sample", values="grader_pass")
        rep[c] = (m.to_numpy().mean(), m.max(axis=1).mean())
    t = U.paired_table("C", "D", 0.2)
    d, se = t["diff"].mean(), U.clustered_se(t["diff"], t.doc_id)
    tc = t[~t.item_id.isin(leaked)]
    dc, sec = tc["diff"].mean(), U.clustered_se(tc["diff"], tc.doc_id)
    write("d4_1", {"leaked": leaked, "clean_vs_overlap": cvo, "clean_vs_overlap_D": cvo[3],
                   "report_D": f(rep["D"][1]), "report_C": f(rep["C"][0]),
                   "equal_diff": [f(d), f(d - 1.96 * se), f(d + 1.96 * se)],
                   "clean_diff": [f(dc), f(dc - 1.96 * sec), f(dc + 1.96 * sec)]})

    calib = U.load("grader_calibration")
    cal = {lang: (g.human_pass.to_numpy(), g.grader_pass.to_numpy()) for lang, g in calib.groupby("language")}
    r0 = {lang: U.rates(g) for lang, g in calib.groupby("language")}
    gap, cgap, cci = {}, {}, {}
    rng = np.random.default_rng(403)
    for c in "ABCD":
        t = U.item_means(c, 0.2)
        ar, en = t.language == "ar", t.language == "en"
        m_ar, m_en = t.score[ar].mean(), t.score[en].mean()
        contrib = np.where(ar, (t.score - m_ar) / ar.sum(), -(t.score - m_en) / en.sum())
        se = np.sqrt((pd.Series(contrib).groupby(t.doc_id.to_numpy()).sum() ** 2).sum())
        gap[c] = [f(m_ar - m_en), f(se)]
        cgap[c] = f(U.corrected_rate(m_ar, r0["ar"]["sens"], r0["ar"]["spec"]) - U.corrected_rate(m_en, r0["en"]["sens"], r0["en"]["spec"]))
        docs = t.doc_id.unique()
        by = {lang: t[t.language == lang].groupby("doc_id").score.agg(["sum", "count"]).reindex(docs, fill_value=0) for lang in ("ar", "en")}
        out = np.empty(3000)
        for b in range(3000):
            pick = rng.integers(0, len(docs), size=len(docs))
            th = {}
            for lang in ("ar", "en"):
                p = by[lang]["sum"].to_numpy()[pick].sum() / by[lang]["count"].to_numpy()[pick].sum()
                h, v = cal[lang]
                j = rng.integers(0, len(h), size=len(h))
                sens, spec = v[j][h[j] == 1].mean(), 1 - v[j][h[j] == 0].mean()
                th[lang] = (p + spec - 1) / (sens + spec - 1)
            out[b] = th["ar"] - th["en"]
        cci[c] = [f(np.percentile(out, 2.5)), f(np.percentile(out, 97.5))]
    write("d4_3", {"gap": gap, "corrected_gap": cgap, "corrected_gap_ci": cci})

    def paired(a, b, temp, keep=None):
        t = U.paired_table(a, b, temp)
        if keep is not None:
            t = t[t.item_id.isin(keep)]
        d, se = t["diff"].mean(), U.clustered_se(t["diff"], t.doc_id)
        return d, d - 1.96 * se, d + 1.96 * se
    clean = set(items.item_id) - set(leaked)
    c1 = paired("C", "D", 0.2, clean)
    claimed = rep["D"][1] - rep["C"][0]
    v = {"C1": "supported" if c1[1] > 0 and c1[1] <= claimed <= c1[2] else "unsupported",
         "C2": "supported" if paired("A", "B", 0.2)[1] > 0 else "unsupported",
         "C3": "supported" if paired("A", "B", 0.8)[1] > 0 else "unsupported",
         "C4": "unsupported",
         "C5": "unsupported" if min(r["spec"] for r in r0.values()) < 0.85 else "supported",
         "C6": "unsupported" if abs(gap["C"][0]) - 1.96 * gap["C"][1] > 0 else "supported",
         "C7": "untestable", "C8": "untestable"}
    write("d4_2", {"verdicts": v})

    standard = ["plan_commit", "population", "items_and_clusters", "decoding", "estimand", "interval_method", "comparison",
                "multiplicity", "minimum_effect_and_verdict", "grader_calibration", "budget_parity", "overlap_check",
                "slices", "small_sets", "reproducibility"]
    lb = {"decoding": 1, "estimand": 1, "interval_method": "naive", "comparison": "ranking by pass rate", "shared_items": True, "small_sets": 1}
    problems = [f"missing: {k}" for k in standard if k not in lb]
    problems += ["slices: Arabic and English results with intervals are required",
                 "comparison: systems answered the same questions, so the comparison must be paired",
                 "interval_method: use clustered intervals, and Wilson, Jeffreys or Clopper-Pearson for small sets",
                 "grader_calibration: sensitivity and specificity per language are required"]
    write("d4_4", {"standard": {k: k.replace("_", " ") for k in standard}, "leaderboard_problems": problems})


if __name__ == "__main__":
    steps = {"1": day1, "2": day2, "3": day3, "4": day4}
    for k in (sys.argv[1:] or sorted(steps)):
        steps[k]()
        print("day", k, "references written")
