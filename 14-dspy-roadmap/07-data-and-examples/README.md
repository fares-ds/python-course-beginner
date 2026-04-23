# 07 — Data & Examples

The data layer that the optimizers (folders 09–12) need. A `dspy.Example` is a labeled training example; `.with_inputs(...)` says which fields the program receives at inference time.

**Docs link:** [Data Handling](https://dspy.ai/learn/evaluation/data/)

## What you'll learn

- **`dspy.Example`** — the training-example object. Looks like a dict; behaves like a dict; has a few extras.
- **`.with_inputs(...)`** — declares which fields are inputs (the rest are labels).
- Building a small dev set by hand. **5–20 examples is plenty to start.**
- Train / dev / test splits — what each is for, and the cardinal sin of letting your test data peek.

## What's in this folder

- [`solution.py`](solution.py) — loads `data/qa_examples.json`, turns each row into a `dspy.Example`, splits into train/dev/test, and pretty-prints the structure.
- [`data/qa_examples.json`](data/qa_examples.json) — 12 simple Q&A pairs.
- [`requirements.txt`](requirements.txt) — `dspy>=3.0,<4.0`.

## Setup

```bash
pip install -r requirements.txt
```

## Run it

```bash
python3 solution.py
```

Expected: prints the splits + shows what an `Example` looks like before and after `.with_inputs()`.

## Key concepts

### `dspy.Example`
```python
ex = dspy.Example(question="What's the capital of France?", answer="Paris")
ex.question   # "What's the capital of France?"
ex.answer     # "Paris"
ex.with_inputs("question")   # marks 'question' as input; everything else is label
```

When DSPy runs your program against `ex`, it passes only the input fields. The rest are gold labels for scoring.

### Train / dev / test
Same conventions as classical ML:

- **Train**: examples optimizers use to bootstrap demos and find good prompts.
- **Dev** (a.k.a. validation): used during optimization to score candidate programs.
- **Test**: held out completely; only used at the very end to report final performance.

For DSPy, the practical sizes are smaller than you'd expect:
- Train: 10–200 (hundreds is plenty for most optimizers)
- Dev: 20–200
- Test: 50+

### The cardinal sin
**Never let your optimizer see test data.** If you pick the "best" run on test, you've overfit to test, and your reported score is meaningless. Use dev for picking; touch test only once, at the end.

### Where do examples come from?
- Hand-write 20 of them — usually enough to get started.
- Pull from a public dataset (HotPotQA, GSM8K, etc.).
- Bootstrap from your live system: log inputs, hand-label outputs, append.

## Mini-tasks

1. Run `solution.py` to see the data structure.
2. Add 3 more Q&A pairs to `data/qa_examples.json`. Re-run; confirm splits change.
3. Build an `Example` with multiple inputs (e.g., `question + context -> answer` like RAG). Mark both as inputs.

## Common pitfalls

- **Forgetting `.with_inputs(...)`** — DSPy will treat *every* field as an input and give the optimizer zero signal. Most common silent failure for beginners.
- **Test set too small** — fewer than 50 examples and your reported numbers have wide error bars. Increase test if you can.
- **Train and test sharing examples** — a copy-paste mistake. Sample randomly with a fixed seed.

## Expected outcome

You can build a small labeled set, split it correctly, and prepare it for a DSPy optimizer.

## Next

→ [08 — Metrics](../08-metrics/)
