# /// script
# requires-python = ">=3.11"
# dependencies = ["openai>=1.50"]
# ///
"""Run two or more model configurations over the Bunyan task set and write item-level logs.

    uv run run_eval.py --config configs.json --out logs/run.csv --samples 5 --temperature 0.2
    uv run run_eval.py --config configs.json --out logs/smoke.csv --limit 20 --stub   # no model: a scripted stand-in

Each configuration in configs.json names an OpenAI-compatible endpoint: a model served on your laptop
(llama.cpp's llama-server or Ollama), on a free notebook GPU (vLLM), or a free hosted endpoint:

    [{"name": "baseline", "base_url": "http://127.0.0.1:11434/v1", "model": "<a small open-weight model>",
      "api_key_env": "", "retrieval": false},
     {"name": "variant",  "base_url": "http://127.0.0.1:11434/v1", "model": "<the same model>",
      "api_key_env": "", "retrieval": true}]

The key, when the endpoint needs one, is read from the environment variable named in api_key_env;
never write a key into a file. Every answer is scored by code: the first number in the answer must
equal the reference value. Logs: one row per question, configuration and sample.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import random
import zlib
import re
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data"

SYSTEM = ("You answer questions about building regulations of a permits authority. "
          "Answer with the number and its unit only. If the regulation text is given, use it.")


def load_items(limit: int | None):
    with open(DATA / "items.csv", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    return rows[:limit] if limit else rows


def load_docs():
    docs = {}
    with open(DATA / "documents.jsonl", encoding="utf-8") as f:
        for line in f:
            d = json.loads(line)
            docs[d["doc_id"]] = d
    return docs


def prompt(item, doc, retrieval: bool) -> list[dict]:
    user = item["question"]
    if retrieval:
        facts = "\n".join(x[item["language"]] for x in doc["facts"])
        user = f"Regulation {doc['doc_id']}:\n{facts}\n\nQuestion: {user}"
    return [{"role": "system", "content": SYSTEM}, {"role": "user", "content": user}]


def first_number(text: str):
    m = re.search(r"-?\d+(?:[.,]\d+)?", text.translate(str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789")))
    return float(m.group().replace(",", ".")) if m else None


class Stub:
    """A scripted stand-in model for checking the pipeline without any model: it reads the retrieved
    regulation when it is in the prompt and is right most of the time; without it, it guesses."""

    def __init__(self, seed: int):
        self.rng = random.Random(seed)

    def answer(self, messages, item, retrieval: bool, temperature: float) -> str:
        right = self.rng.random() < (0.85 if retrieval else 0.55) - 0.1 * temperature
        value = int(item["answer"]) if right else int(item["answer"]) + self.rng.choice([-2, -1, 1, 2, 5])
        return f"{value} {item['unit']}"


def call(client, model: str, messages, temperature: float, retries: int = 5) -> str:
    for attempt in range(retries):
        try:
            r = client.chat.completions.create(model=model, messages=messages, temperature=temperature, max_tokens=64)
            return r.choices[0].message.content or ""
        except Exception as e:  # rate limits and busy endpoints: wait and retry
            if attempt == retries - 1:
                raise
            time.sleep(2 ** attempt)
            print(f"retry after {type(e).__name__}", file=sys.stderr)
    return ""


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--samples", type=int, default=5)
    ap.add_argument("--temperature", type=float, default=0.2)
    ap.add_argument("--limit", type=int, default=None, help="first N questions only, for a smoke run")
    ap.add_argument("--stub", action="store_true", help="use the scripted stand-in model, no endpoint")
    args = ap.parse_args()

    configs = json.loads(Path(args.config).read_text(encoding="utf-8"))
    items, docs = load_items(args.limit), load_docs()
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["item_id", "doc_id", "language", "config", "temperature", "sample", "answer", "correct"])
        for cfg in configs:
            if args.stub:
                stub = Stub(seed=zlib.crc32(cfg["name"].encode()))
            else:
                from openai import OpenAI
                key = os.environ.get(cfg.get("api_key_env") or "", "") or "not-needed"
                client = OpenAI(base_url=cfg["base_url"], api_key=key)
            for item in items:
                msgs = prompt(item, docs[item["doc_id"]], cfg.get("retrieval", False))
                for s in range(1, args.samples + 1):
                    if args.stub:
                        text = stub.answer(msgs, item, cfg.get("retrieval", False), args.temperature)
                    else:
                        text = call(client, cfg["model"], msgs, args.temperature)
                    num = first_number(text)
                    correct = int(num is not None and abs(num - float(item["answer"])) < 1e-9)
                    w.writerow([item["item_id"], item["doc_id"], item["language"], cfg["name"], args.temperature, s,
                                text.replace("\n", " ")[:200], correct])
            print(f"{cfg['name']}: {len(items)} questions × {args.samples} samples", file=sys.stderr)
    print("wrote", out)


if __name__ == "__main__":
    main()
