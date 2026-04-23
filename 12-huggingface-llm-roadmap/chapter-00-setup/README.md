# Chapter 0 — Setup

The 30-minute pre-flight check before Chapter 1. If this folder runs cleanly, your machine is ready for the rest of the course.

**Course link:** [Chapter 0 on the HF docs](https://huggingface.co/learn/llm-course/en/chapter0/1)

## What you'll learn

- How to verify your Python version (must be 3.9–3.11 for the course's notebooks).
- How to create a virtual environment.
- How to install the core libraries (`transformers`, `huggingface_hub`).
- How to log in to the Hugging Face Hub from the command line.

## What's in this folder

- [`solution.py`](solution.py) — prints your Python + library versions and confirms you're logged in to the Hub.
- [`requirements.txt`](requirements.txt) — the absolute minimum: `transformers`, `huggingface_hub`.

## Setup

```bash
python3 --version            # must be 3.9 - 3.11
python3 -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Sign up for a free account at [huggingface.co/join](https://huggingface.co/join), then:

```bash
huggingface-cli login        # paste a token from hf.co/settings/tokens
```

## Run it

```bash
python3 solution.py
```

Expected: a short report listing your Python version, key library versions, and your HF username (if logged in). No errors.

## Key concepts

### Virtual environment
Isolates this project's dependencies from the rest of your system. If you skip this and `pip install` globally, you will eventually break some other Python tool. Don't skip.

### The Hugging Face Hub
A git-based registry of models, datasets, and Spaces. You don't need to push anything in Chapter 0 — just confirm you can authenticate, so the rest of the course doesn't trip over it.

### Why Python 3.11 (not 3.12+)
Several libraries the course uses (Argilla in Ch 10, parts of `pandasai` if you go side-quest with Project 11) lag behind on the latest Python. 3.11 is the safest "everything works" version as of 2026.

## Mini-tasks

1. Run `pip list` after install — count the packages. Notice how many transitive deps `transformers` pulled in.
2. From a Python REPL: `from huggingface_hub import HfApi; print(HfApi().whoami())`. Confirm it prints your username.

## Common pitfalls

- **"command not found: huggingface-cli"** — your venv isn't activated, or the install failed silently. Re-activate and re-run `pip install`.
- **403 / token errors** — your token has only `read` scope. For Ch 4 onward you'll need `write`. You can leave it `read` for now.

## Expected outcome

`solution.py` runs cleanly and reports your username. You're ready for Chapter 1.

## Next

→ [Chapter 1 — Transformer models](../chapter-01-transformer-models/)
