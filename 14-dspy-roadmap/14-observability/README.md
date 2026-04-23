# 14 — Observability

When your DSPy program goes wrong in production, you need to see *what* happened. This folder covers the tools.

**Docs link:** [Debugging & Observability](https://dspy.ai/tutorials/observability/)

## What you'll learn

- `dspy.inspect_history(n=...)` — your local-debugging lifeline.
- **MLflow autolog** for DSPy — captures every LM call, prompt, response, and module call automatically.
- **Phoenix** (Arize) for tracing — live UI showing the agent's loop step by step.
- The **eval-after-every-change** discipline that makes optimization work.

## What's in this folder

- [`solution.py`](solution.py) — runs a small CoT pipeline and uses `dspy.inspect_history(n=2)` to print the last two LM exchanges.
- [`mlflow_setup.md`](mlflow_setup.md) — how to wire up MLflow autologging (a few lines of code).
- [`phoenix_setup.md`](phoenix_setup.md) — how to wire up Phoenix.
- [`requirements.txt`](requirements.txt) — `dspy>=3.0,<4.0`.

## Setup

```bash
pip install -r requirements.txt
```

## Run it

```bash
python3 solution.py
```

Expected: runs two questions through a CoT program, prints the answers, then shows the last two prompt+response pairs in detail.

## Key concepts

### `dspy.inspect_history(n=N)`
The local-development MVP. Prints the last N (prompt, response) pairs the configured LM produced. Use during interactive development; remove (or guard) before production.

```python
result = my_program(question=q)
dspy.inspect_history(n=1)   # see exactly what was sent and received
```

### MLflow autolog
For real apps, you want every call automatically captured. MLflow has first-class DSPy integration:

```python
import mlflow
mlflow.dspy.autolog()
mlflow.set_experiment("my-dspy-app")
# ... now every program call gets logged: prompts, completions, modules, latency, cost.
```

Visit `http://localhost:5000` (after `mlflow ui`) to browse runs. See [`mlflow_setup.md`](mlflow_setup.md) for the full setup.

### Phoenix tracing
[Phoenix](https://phoenix.arize.com) (open source from Arize) gives you a live trace UI specifically for LLM apps. It speaks OpenInference, the same protocol you set up in Project 13's Bonus 2 unit. Same instrumentation, different backend. See [`phoenix_setup.md`](phoenix_setup.md).

### When to use which

| Tool | When |
|---|---|
| `inspect_history` | Active development, single-shot debugging |
| MLflow | You want a long-term log + UI; experiment tracking; reproducibility |
| Phoenix | You want a live trace UI specifically for agent/RAG loops |
| Logs (plain old logger) | Production, headless, when you'll grep later |

You don't need all three. Pick one and use it consistently.

## Mini-tasks

1. Run `solution.py`. Read the `inspect_history` output — confirm you can map the printed prompt back to the signature you defined.
2. Set up MLflow per `mlflow_setup.md`. Run any program from folders 09–11 with autologging on; browse the UI.
3. Build the eval/observability habit: after any change to a program or optimizer, **before** you ship, evaluate on the dev set and check the trace of the worst-scoring example. The trace tells you why; the score alone doesn't.

## Common pitfalls

- **Logging in tight loops** — `inspect_history(n=100)` for every request inside a loop floods stdout. Cap N.
- **Different observability tools double-instrumenting** — MLflow + Phoenix together can produce duplicate traces. Pick one.
- **No PII redaction** — every prompt may contain user data. Scrub before logging in production.

## Expected outcome

You can debug a DSPy program with `inspect_history`, set up at least one production-grade observability tool, and have the eval-after-every-change discipline.

## Next

You've finished the DSPy roadmap. Go back to the [parent README](../README.md) and pick a capstone project. Your toolkit now: DSPy as a third lens on "how to build with LLMs" — alongside the HF Transformers stack (Project 12) and the agent-frameworks landscape (Project 13).
