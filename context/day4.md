---
course: "Statistical Evaluation of AI Systems"
code: "DS-403"
version: "2027.1.0"
deck: "day4"
day: 4
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/ds-403/slides/day4.html"
---

# Statistical Evaluation of AI Systems

## Day 4: Auditing claims and setting standards

Audit the claims an evaluation makes, slice by language, and write the standard every report must meet

#### [day4#title] Auditing claims and setting standards

*SDAIA Academy · Statistical Evaluation of AI Systems*

Day 4: Audit the claims an evaluation makes, slice by language, and write the standard every report must meet

Data Science Track · 4 teaching days + capstone day · 4 sessions · 4 labs · DS-403

#### [day4#agenda] Auditing claims and setting standards

*Today*

- **Session 1 · Contamination and unequal budgets**: Test items in the tuning examples, best of many prompts, and best of five samples: why two scores are not comparable
- **Session 2 · Auditing a report**: Every claim of a report is supported, unsupported or untestable, and the memo says which and why
- **Session 3 · Slicing by language**: An average hides a language: Arabic and English results with intervals, and a test of the gap
- **Session 4 · A reporting standard**: A reporting standard: the fields every evaluation claim must carry, a worked example, and the capstone choice

#### [day4#review-day3] A grader, a small set, and an interval

*Review of Day 3*

**Question:** A grader's Arabic specificity is 0.73, from 49 human-failed answers. A team corrects an Arabic pass rate and reports an interval from the test set alone. What should the reviewer ask for?

- A. Nothing: the corrected rate is unbiased
- B. A Clopper-Pearson interval on the test set
- C. An interval that also resamples the calibration verdicts
- D. The uncorrected rate, which has a narrower interval

### Session 1: Contamination and unequal budgets

#### [day4#s1] Contamination and unequal budgets

*Session 1*

- Detect overlap between test items and tuning examples, including Arabic spelling variants
- Measure how overlap changes a score
- Recompute a comparison at equal budgets

#### [day4#the-leaderboard] D at 86.7%, fifteen points ahead of C

*Khattab's leaderboard*

| Item | Value |
| --- | --- |
| D | 86.7% |
| C | 72.1% |
| B | 69.8% |
| A | 63.2% |

- 600 questions, temperature 0.2, five samples, model grader.
- No intervals, no slices, no word on how D was tuned.

#### [day4#settings-differ] D was scored differently and tuned on the test set

*How each was scored*

| Config | Scored as | Prompt variants tried on the test set | Max output tokens |
| --- | --- | --- | --- |
| A, B, C | mean of 5 samples | 1 | 512 |
| D | best of 5 samples | 12 | 2,048 |

#### [day4#contamination] Test questions inside the tuning examples inflate the score on exactly those questions

*Contamination*

- **Pre-training contamination:** a public benchmark in a model's training data.
- **Tuning contamination:** test items among the few-shot or prompt-tuning examples.
- The model then recalls answers instead of reading the regulation.

- **The test.** Find the overlap, then compare each configuration's score on overlapping and clean questions.

#### [day4#arabic-normalisation] An exact match finds 35 overlapping questions; normalising Arabic finds 48

*Arabic spelling variants*

| Folded | Example |
| --- | --- |
| hamza on alef | الأدنى ← الادنى |
| ta marbuta | لائحة ← لائحه |
| alef maqsura | في ← فى |
| diacritics, tatweel, spaces | removed |

**13 of 21** Arabic overlaps found only after normalisation

#### [day4#overlap-effect] Only D scores higher on the overlapping questions: 90.4% against 72.9%

*Lab 4.1 result*

| Config | Overlapping (48) | Clean (552) | Difference |
| --- | --- | --- | --- |
| A | 64.6% | 63.0% | +1.5 |
| B | 68.3% | 69.9% | −1.6 |
| C | 72.1% | 72.1% | 0.0 |
| D | 90.4% | 72.9% | +17.6 |

#### [day4#equal-budgets] Fifteen points become two, then one, and the last one is not shown

*The comparison, made fair*

| D minus C | Points |
| --- | --- |
| As reported: D best of 5, C mean of 5 | 14.6 |
| Equal budget: both mean of 5, all questions | 2.2 (0.5 to 3.9) |
| Equal budget, clean questions only | 0.8 (−0.8 to 2.3) |

Choosing the best of 12 equally good prompts on the test set adds about 0.8 points by itself (Lab 4.1 stretch).

#### [day4#saturation] A saturated or public benchmark cannot separate strong systems

*One more threat*

- When every system scores near the ceiling, differences sit inside the noise (Day 3).
- A public set may be in some systems' training data and not others'.
- Keep a private, versioned set, refreshed as regulations change.

#### [day4#check-budgets] A fair comparison

*Checkpoint*

**Question:** A report compares two configurations. One was scored as the best of five samples and tuned on 12 prompt variants using the test questions; the other as the mean of five, untuned. What must the audit do first?

- A. Rescore both the same way and remove the test questions used in tuning before comparing
- B. Add confidence intervals to the reported numbers
- C. Ask for more test questions
- D. Accept it: the tuned configuration earned its lead

#### [day4#lab-4-1] Overlap and unequal budgets

Lab 4.1 · 25 min

Check configuration D's comparison for test questions that appear in its tuning examples, after Arabic normalisation, measure the score on clean questions, and recompute the comparison at equal budgets.

[D4_1_check_comparison_test.ipynb](https://sdaiaacademy.github.io/ds-403/labs/D4_1_check_comparison_test.ipynb)

- [ ] Exact matches between tuning examples and test questions (4 min)
- [ ] Arabic normalisation and the matches it adds (6 min)
- [ ] D on clean and overlapping questions (5 min)
- [ ] Best of five against mean of five (5 min)
- [ ] The comparison at equal budgets, clean questions only (5 min)
- [ ] ✱ Stretch: Estimate the winner's curse of choosing the best of twelve prompts on the test set

### Session 2: Auditing a report

#### [day4#s2] Auditing a report

*Session 2*

- Classify an evaluation claim by the evidence it needs
- Re-analyse a claim from item-level logs
- Write an audit memo a decision owner can act on

#### [day4#three-classes] Every claim is supported, unsupported or untestable

*Auditing a claim*

- **Supported.** The data back it at the strength stated.
- **Unsupported.** The available data contradict it, or do not back it as stated.
- **Untestable.** No data the authority holds could decide it.

> **From DS-305.** The same three classes were used for model-card claims; here the evidence is statistical.

#### [day4#evidence-needed] Write down what would decide each claim

*Before re-analysing*

| Claim | Decided by |
| --- | --- |
| C1 D leads C by 15 points | equal budgets, clean questions, paired and clustered |
| C2, C3 B beats A (at 0.2, at 0.8) | paired clustered difference at each temperature |
| C4 D never unsafe | an upper bound from 40 of 40 |
| C5 no grader correction needed | specificity by language |
| C6 C equal in both languages | clustered gap, observed and corrected |
| C7, C8 the 2027 lead; applicants' preference | data the authority does not have |

#### [day4#audit-results] Two claims supported, four unsupported, two untestable

*Lab 4.2 result*

| Claim | Class | Deciding number |
| --- | --- | --- |
| C1 | unsupported | clean, equal budgets: 0.8 points (−0.8 to 2.3) |
| C2 | supported | B minus A 6.6 points (4.5 to 8.8) |
| C3 | supported | at 0.8: 2.1 points (0.2 to 4.1) |
| C4 | unsupported | unsafe rate below 7.2%, not zero |
| C5 | unsupported | Arabic specificity 0.73 against 0.91 |
| C6 | unsupported | Arabic minus English −5.8 points (−11.5 to just below 0) |
| C7, C8 | untestable | no 2027 data; no preference data |

#### [day4#untestable-is-information] An untestable claim tells the decision owner what evidence to commission

*Untestable claims*

- **C7 · the 2027 regulations.** A new population: size a new set (Day 2: 417 questions for three points).
- **C8 · applicants' preference.** Needs a preference study or an online experiment (DS-302), not grader verdicts.

#### [day4#memo-shape] One line per claim: the class, the number, the claim that would be supported

*The audit memo*

Prompt for Audit memo, line C4:

```text
C4 unsupported: 40 of 40 bounds D's unsafe rate below 7.2% at 95%; it does not show "never". Supported version: "D gave no unsafe answer on the 40-question safety set; with 95% confidence its unsafe rate on such questions is below 7.2%."
```

#### [day4#audit-ethics] Audit the claims, not the person

*Auditing colleagues' work*

- Khattab's numbers were computed correctly; the comparison was not fair.
- Show every re-analysis with its code, so the author can rerun it.
- A standard (session 4) prevents the next report from needing an audit.

#### [day4#check-audit] Classing a claim

*Checkpoint*

**Question:** A report claims "the assistant is equally accurate for all regions". The logs carry no region field. How should the audit class the claim?

- A. Supported: no regional difference was found
- B. Unsupported: equal accuracy is unlikely
- C. Supported, because regions should not matter for regulations
- D. Untestable with these logs; name the data that would test it

#### [day4#lab-4-2] Auditing the leaderboard

Lab 4.2 · 25 min

Classify each of the eight claims of the configuration leaderboard as supported, unsupported or untestable, with the re-analysis that decides each, and write the audit memo.

[D4_2_classify_each_claim.ipynb](https://sdaiaacademy.github.io/ds-403/labs/D4_2_classify_each_claim.ipynb)

- [ ] Read the report and its eight claims (3 min)
- [ ] The evidence each claim needs (4 min)
- [ ] Re-analyse the testable claims (10 min)
- [ ] Classify all eight (4 min)
- [ ] The audit memo (4 min)
- [ ] ✱ Stretch: Rewrite one unsupported claim so that the data supports it

### Session 3: Slicing by language

#### [day4#s3] Slicing by language

*Session 3*

- Report a score by language with clustered intervals
- Test the gap between languages using documents with questions in both
- Show how grader correction changes a gap

#### [day4#averages-hide] C and D have similar averages; one of them is weaker in Arabic

*Averages hide groups*

| Item | Value |
| --- | --- |
| C · Arabic | 69.2% |
| C · English | 75.0% |
| D · Arabic | 74.2% |
| D · English | 74.3% |

#### [day4#slice-intervals] Each slice keeps its clustering: about 300 questions over the same 80 documents

*Intervals per language*

| Config | Arabic (95% CI) | English (95% CI) |
| --- | --- | --- |
| A | 63.0 (57.4 to 68.6) | 63.4 (56.7 to 70.1) |
| B | 70.6 (65.2 to 75.9) | 69.0 (62.9 to 75.1) |
| C | 69.2 (63.8 to 74.6) | 75.0 (69.3 to 80.8) |
| D | 74.2 (69.0 to 79.4) | 74.3 (68.7 to 80.0) |

#### [day4#gap-test] Test the gap itself, clustered by document, because most documents have questions in both languages

*Testing the gap*

- Each Arabic question gets weight +1 / nar, each English one −1 / nen.
- Sum the weighted deviations within each document, then square.
- A hard document lowers both languages; that part cancels.

**−5.8** C's Arabic minus English, 95% CI −11.5 to −0.02 points

#### [day4#corrected-gap] Correction widens C's gap to nine points, and its interval with it

*With the grader corrected*

| Config | Observed gap | Corrected gap (95% CI) |
| --- | --- | --- |
| C | −5.8 | −9.0 (−22.2 to +2.4) |
| A | −0.4 | −5.5 (−19.6 to +6.8) |
| D | −0.2 | −0.7 (−12.4 to +10.8) |

The lenient Arabic grader was shrinking the gap; the 49 failed Arabic answers in the calibration set make the corrected interval wide.

#### [day4#slice-table] A slice table: rate and interval per language, the gap, observed and corrected

*What the report shows*

- Every configuration, both languages, with clustered intervals.
- The gap with its own interval; corrected for the grader by language.
- Categories as a second slice, adjusted for eight comparisons.

#### [day4#check-slices] Two overlapping intervals

*Checkpoint*

**Question:** C's Arabic interval is 63.8 to 74.6 and its English interval 69.3 to 80.8. They overlap. Most documents have questions in both languages. What can you conclude about the gap?

- A. No gap: the intervals overlap
- B. Nothing yet: test the gap itself with a standard error clustered by document
- C. Compute the gap's SE as the root sum of the two squared SEs
- D. Report both rates; gaps are never tested

#### [day4#lab-4-3] Arabic and English

Lab 4.3 · 25 min

Report each configuration's Arabic and English pass rates with clustered intervals, test the gap, and show how the grader correction changes it.

[D4_3_report_arabic_english.ipynb](https://sdaiaacademy.github.io/ds-403/labs/D4_3_report_arabic_english.ipynb)

- [ ] Pass rates by language for four configurations (4 min)
- [ ] Clustered intervals per language (5 min)
- [ ] The gap and its interval (7 min)
- [ ] The gap after grader correction (5 min)
- [ ] The slice table for the report (4 min)
- [ ] ✱ Stretch: Slice by category as well and adjust for eight comparisons

### Session 4: A reporting standard

#### [day4#s4] A reporting standard

*Session 4*

- List the required fields of an evaluation report
- Validate a worked example against the standard
- Choose the configurations and the plan of the capstone

#### [day4#findings-to-fields] Every failure this week becomes a required field of the standard

*From findings to fields*

| Field | The failure it prevents |
| --- | --- |
| plan_commit | metric and slices chosen after the results |
| items_and_clusters | 600 questions treated as independent |
| estimand, decoding | best of five compared with mean of five |
| comparison, multiplicity | unpaired comparisons; unadjusted rankings |
| grader_calibration | a lenient Arabic grader left uncorrected |
| budget_parity, overlap_check | tuning on the test set; unequal scoring |
| slices, small_sets | an Arabic gap hidden; 40 of 40 read as never |

#### [day4#validator] A validator turns the standard into a gate

*Make it checkable*

```python
# file: Lab 4.4
def validate(report):
    problems = [f"missing: {f}" for f in STANDARD if not report.get(f)]
    if not {"ar", "en"} <= set(report.get("slices") or {}):
        problems.append("slices: Arabic and English required")
    if report.get("shared_items") and "paired" not in report.get("comparison", ""):
        problems.append("comparison must be paired")
    return problems
```

#### [day4#worked-example] The week's decision passes the standard; the leaderboard fails on fourteen counts

*The worked example*

- **D against C, reported to the standard.** Plan committed; clustered and paired; 3-point minimum effect; grader by language; overlap checked; slices; safety bound. Passes.
- **The leaderboard.** Ten fields missing; naive intervals; an unpaired ranking; no slices; no grader rates. Fourteen problems.

#### [day4#release-process] The standard is checked before a report reaches the release decision

*Where the standard sits*

1. **1 · Plan** committed, dated
2. **2 · Run** logs kept per item
3. **3 · Report** to the standard
4. **4 · Gate** validator, then review
5. **5 · Decide** Dr. Nadeen

#### [day4#capstone-choice] Choose two open-weight configurations, and commit the plan before anything runs

*The capstone*

- Two or more configurations you serve yourself: a laptop (llama.cpp, Ollama), a free notebook GPU (vLLM), or a free hosted endpoint.
- Bunyan's 600 questions, or your own set with a licence that allows it.
- Starter: `labs/capstone/`.

- **First commit.** capstone_plan.json from Lab 4.4: configurations, minimum effect, samples, temperature, primary comparison.

#### [day4#check-standard] The field that matters

*Checkpoint*

**Question:** A team's report has intervals, a plan and slices, but scores its own configuration as the best of five samples and the vendor's as the mean of five. Which field of the standard catches it?

- A. multiplicity
- B. slices
- C. budget_parity, with the estimand stated per configuration
- D. interval_method

#### [day4#lab-4-4] The standard and the capstone choice

Lab 4.4 · 25 min

Draft the reporting standard's required fields, test a worked example against them, and choose the configurations and the plan of the capstone.

[D4_4_reporting_standard.ipynb](https://sdaiaacademy.github.io/ds-403/labs/D4_4_reporting_standard.ipynb)

- [ ] Fields from the week's findings (6 min)
- [ ] A validator for a report (6 min)
- [ ] The worked example: pass and fail (5 min)
- [ ] Choose the capstone configurations (5 min)
- [ ] Commit the capstone plan (3 min)
- [ ] ✱ Stretch: Turn the standard into a release gate that blocks a report with a missing field

#### [day4#wrap-up] Three things to keep

*Day 4 · wrap-up*

- **Same budget, clean items.** Fifteen points became 0.8, not shown.
- **Three classes, one number each.** Supported, unsupported, untestable, with the claim that would be supported.
- **Slice, correct, standardise.** Arabic and English with intervals; fifteen required fields.

#### [day4#next] Capstone: your statistical evaluation report

*Next*

Commit your plan before any result. Bring the repository link, results by language and one statistical choice you are ready to defend.
