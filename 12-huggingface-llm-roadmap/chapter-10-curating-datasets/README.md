# Chapter 10 — Curate high-quality datasets with Argilla

"Good data beats more data." Most fine-tuning gains in 2026 come from *cleaner labels*, not bigger models. This chapter teaches the workflow and the tool.

**Course link:** [Chapter 10 on the HF docs](https://huggingface.co/learn/llm-course/en/chapter10/1)

## What you'll learn

- **Why dataset quality dominates** — the shift from "more data" to "better data" in modern ML.
- **Argilla** — Hugging Face's labeling / curation UI. Install, load a dataset, annotate, export.
- **Workflow patterns** — look at every 50th example; look at the examples where the model is least confident; look at disagreements between annotators.

## What's in this folder

- [`solution.py`](solution.py) — loads a small sample of IMDb into Argilla, lets you (or a team) relabel the records, exports back to a Hugging Face dataset.
- [`requirements.txt`](requirements.txt) — `argilla`, `datasets`, `transformers`.

## Setup

Argilla has a server (runs in Docker) and a Python client (what you use here).

### Easiest path: use the Argilla demo server

Hugging Face hosts a free Argilla workspace in Spaces. Create one via [hf.co/new-space](https://huggingface.co/new-space) → pick "Argilla" template. Follow the wizard. You'll get a URL + API key.

### Local path: Docker

```bash
pip install -r requirements.txt
docker run -d --name argilla -p 6900:6900 argilla/argilla-server:latest
```

Open `http://localhost:6900` in your browser. Sign in (default: `argilla` / `1234`). Create an API key in your user settings.

## Run it

Set two env vars (from the wizard or your local setup):

```bash
export ARGILLA_API_URL="http://localhost:6900"   # or your Space URL
export ARGILLA_API_KEY="your-api-key-here"
python3 solution.py
```

Expected: the script loads 20 IMDb reviews into Argilla under a dataset called `imdb-demo`. Open the Argilla UI, label them, then re-run the script with the `--export` flag to pull the labels back.

## Key concepts

### Why this matters
Before 2023, "better model" usually meant "bigger model." Since then, papers like [DoReMi](https://arxiv.org/abs/2305.10429), [Less is More for Alignment](https://arxiv.org/abs/2305.11206), and the Llama 3 technical report all point the same way: **for a fixed compute budget, better data quality dominates bigger model size.** So the skill of looking at your data systematically isn't a nice-to-have anymore — it's the main skill.

### Argilla's record model
Each record has:
- **Fields**: the text the annotator reads (`text`, `title`, etc.).
- **Questions**: what you're asking them to label (a label choice, a rating, a text box for feedback).
- **Suggestions**: a pre-filled answer from a model — annotators can accept or correct.
- **Metadata**: filters for slicing (source, difficulty, model version).

### The three things to look at
1. **Every Nth example** — find systematic issues (bad punctuation in your scraper, truncated rows).
2. **Low-confidence model predictions** — the examples the model is least sure about. Usually where your labels are worst.
3. **Annotator disagreements** — if two humans disagree, your task definition is probably ambiguous, and the model will learn the ambiguity.

## Mini-tasks

1. Load 20 records into Argilla. Relabel 5 of them differently. Export. Confirm the new labels came through.
2. Load model predictions as "suggestions" so annotators start from the model's guess. See how much it speeds up labeling.
3. (Optional) Invite a friend as a second annotator. Compare your labels. Where did you disagree? What does that tell you about the task?

## Focus vs skim

- **Focus:** the workflow, not the tool. The skill ("look at your data systematically") generalizes far beyond Argilla.
- **Skip:** this whole chapter if you don't currently have a dataset that needs cleaning. Come back when you do.

## Common pitfalls

- **Labeling everything yourself** — you will get tired by record 300, and you will get worse at it. Label 100 samples, train a tiny model, use it to flag the hardest remaining ones for human review.
- **Never re-reading your own labels** — do a "spot audit" on every 50th record a week after you labeled it. You'll find your own mistakes.
- **Skipping the task definition document** — before you label one record, write down in prose what the labels mean. One paragraph per label. Otherwise you and anyone else will drift.

## Expected outcome

You understand why data curation is now the biggest lever in applied ML, and you can set up a labeling workflow when you need one.

## Next

→ [Chapter 11 — Fine-tune Large Language Models](../chapter-11-fine-tuning-llms/)
