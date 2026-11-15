# [Your title]: a statistical evaluation of [configurations]

## The claim

One sentence: what was compared, on which population, and the verdict against the minimum effect.

## Plan

Link to `plan.json` and the commit that added it. Amendments, each with its date and reason.

## Population and items

What the questions represent; how many; from how many source documents; languages; any exclusions.

## Configurations and budgets

| Configuration | Model | Prompt | Serving | Samples per question | Temperature | Max output tokens | Prompt variants tried |
|---|---|---|---|---|---|---|---|

Overlap check between your test questions and anything a configuration saw (few-shot examples, tuning data), with Arabic normalisation.

## Results

| Configuration | Score | 95% CI (clustered) | Design effect |
|---|---|---|---|

Paired difference, its interval and the verdict against the minimum effect. Adjusted intervals if more than two configurations.

## Sizing

The questions needed for the minimum effect at 80% power, by formula and by simulation, and what the next evaluation should change.

## Grader and correction

The grader, its sensitivity and specificity per language from your human labels, with intervals; corrected and uncorrected scores by language, with intervals that carry the calibration's uncertainty.

## By language

| Configuration | Arabic (95% CI) | English (95% CI) | Gap (95% CI) | Gap after correction |
|---|---|---|---|---|

## Small sets

Any slice or safety set under a few hundred items, with Wilson, Jeffreys or Clopper-Pearson intervals.

## What is untestable here

Claims these data cannot decide, and the evaluation that would.

## Reproduce

The commands that rebuild every number from `logs/`.

## Verification note

The AI outputs you relied on (code, text, analysis), and how you checked each one.
