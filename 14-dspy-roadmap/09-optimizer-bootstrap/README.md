# 09 — Optimizer: `BootstrapFewShot`

The first optimizer. The simplest one. **The one that proves the whole DSPy pitch.** Take a working program, hand it some training examples, and watch DSPy automatically find good few-shot demos that improve quality.

**Docs link:** [Optimizers](https://dspy.ai/learn/optimization/optimizers/) · [BootstrapFewShot API](https://dspy.ai/api/optimizers/BootstrapFewShot/)

## What you'll learn

- How an **optimizer** works in DSPy: take a Module + a metric + a train set, return an *optimized* version of the same Module.
- **`BootstrapFewShot`** — runs your unoptimized program on training questions, keeps the runs the metric scored as good, and adds them as few-shot examples in the prompt.
- The before/after measurement habit — never claim improvement without measuring on a held-out dev set.

## What's in this folder

- [`solution.py`](solution.py) — fine-tunes a `dspy.ChainOfThought("question -> answer")` Q&A program with `BootstrapFewShot` on the Q&A data from folder 07. Measures accuracy before vs after.
- [`requirements.txt`](requirements.txt) — `dspy>=3.0,<4.0`.

## Setup

```bash
pip install -r requirements.txt
```

## Run it

```bash
python3 solution.py
```

Expected:
1. Baseline accuracy on the dev set with the un-tuned program.
2. `BootstrapFewShot.compile(...)` runs (~1–3 min on Ollama; the optimizer makes many LM calls during bootstrap).
3. Accuracy after compilation. Should be the same or higher.

## Key concepts

### What an "optimizer" actually does
A DSPy optimizer is **not** training neural-network weights (most of them, anyway). It's tuning the **prompt** — specifically, the few-shot demonstrations DSPy puts in front of the model.

```python
from dspy.teleprompt import BootstrapFewShot

optimizer = BootstrapFewShot(metric=my_metric, max_bootstrapped_demos=4)
compiled_program = optimizer.compile(student=my_program, trainset=train)
```

`compiled_program` is a copy of `my_program` with **selected demos** baked into the prompts of every Predict/CoT inside.

### How `BootstrapFewShot` picks demos
1. For each training example: run the (unoptimized) program; capture the trace.
2. Apply the metric: did the program get this one right?
3. If yes: keep the trace as a "demo" (an input/output pair the model can see in the prompt at inference time).
4. Stop after `max_bootstrapped_demos` good demos are found.

That's it. Stupidly simple, often dramatically effective for small models.

### Before/after measurement
**Always** measure. Programs sometimes get *worse* after compilation if the metric is noisy or the train/dev sets are too small.

```python
evaluator = dspy.Evaluate(devset=dev, metric=my_metric, num_threads=1)
print("Baseline:", evaluator(program))
print("Compiled:", evaluator(compiled))
```

If compiled < baseline, the right move is to fix the metric or add more train data — not to ship the worse one.

## Mini-tasks

1. Run `solution.py`. Was the compiled program better, worse, or the same?
2. Increase `max_bootstrapped_demos` from 4 to 8. Does dev accuracy go up? At what point does the prompt get too long?
3. Use `LabeledFewShot` (also in `dspy.teleprompt`) for comparison — it just picks demos directly from the train set without checking the metric. Compare against `BootstrapFewShot`.

## Common pitfalls

- **Metric returns a bool when DSPy needs a float** — wrap with `float(...)`.
- **Train and dev share examples** — your "improvement" is fake. Use a fixed-seed split (folder 07 shows the right way).
- **Tiny train set + harsh metric** — the optimizer can't find any good demos; the compiled program is identical to the baseline. Either add more train data or loosen the metric.

## Expected outcome

You've run your first DSPy optimizer end-to-end and measured before/after. You understand that "optimization" in DSPy means tuning the prompt's contents, not the model's weights.

## Next

→ [10 — Optimizer: MIPROv2](../10-optimizer-mipro/)
