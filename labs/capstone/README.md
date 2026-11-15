# Capstone starter: a statistical evaluation report

The capstone of DS-403 is a statistical evaluation of **two or more open-weight configurations** that you run yourself, reported to the course's reporting standard in a **public GitHub repository**, then a 15-minute review.

## What the repository must hold

1. `plan.json`, **committed before any result exists** (Lab 1.4 and Lab 4.4: `capstone_plan.json`). The commit date is checked. An amendment is a new dated commit with its reason.
2. The item-level logs of every run (`logs/*.csv`), one row per question, configuration and sample.
3. The analysis: scores with clustered intervals and design effects, the paired comparison against your minimum effect, a sizing plan checked by simulation, the grader correction by language with intervals that carry the calibration's uncertainty, and the slices by language.
4. A README in the shape of `TEMPLATE_README.md`, reporting the measured results to the standard's fields, with a verification note on any AI output you relied on.
5. The command that rebuilds every number from the logs.

## Serving the models

The catalog allows model serving for the capstone only. Choose one; the runner speaks the same API (OpenAI-compatible chat completions) to all of them:

- **A laptop:** llama.cpp's `llama-server` or Ollama with a small open-weight instruct model. This downloads the model's weights to your machine: check its licence and size first.
- **A free notebook GPU:** vLLM in a free Colab or Kaggle GPU session.
- **No local resources:** a free hosted endpoint that serves open-weight models; put its key in an environment variable and its name in `api_key_env`.

## The starter

| File | What it does |
|---|---|
| `configs.example.json` | Two configurations of one model: a plain prompt and the retrieved regulation in the prompt. Copy it and fill in your endpoints and models |
| `run_eval.py` | Runs every configuration over Bunyan's 600 questions (`../data/items.csv`, `../data/documents.jsonl`), five samples each, and scores each answer by code (the first number must equal the reference). `--limit 20` for a smoke run; `--stub` runs a scripted stand-in model with no endpoint, to check your pipeline |
| `analyze.py` | Reads the logs and writes `results.md`: scores, paired comparison and verdict, sizing, slices by language and, with `--labels`, the grader correction |

```bash
uv run run_eval.py --config configs.json --out logs/run.csv --samples 5 --temperature 0.2
uv run analyze.py logs/run.csv --a baseline --b variant --min-effect 0.03 --labels labels.csv
```

## The grader and the human labels

Scoring by code is exact for Bunyan's numeric questions. The rubric's grader criterion asks for a **model grader** as well, corrected with **your own human labels**: grade each answer with a second open-weight model (a binary pass or fail prompt), label at least 100 answers per language yourself, and pass them to `analyze.py --labels` in the columns `language`, `human_pass`, `grader_pass`. On Bunyan's numeric questions your human label can be the code score: then the correction measures the model grader against it.

## Your own task set

You may use a task set of your own instead of Bunyan's, if its licence allows publishing the logs. It needs a cluster column (`doc_id`: the source the question was written from) and a `language` column. Real personal data never goes into the repository; apply the NDMO classification to anything you log.

## The review

Fifteen minutes. You present the plan, the results by language and one statistical choice. The assessor then drops a cluster or changes the minimum effect, and you predict the consequence before re-running.
