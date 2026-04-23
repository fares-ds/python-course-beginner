# 11 — Optimizer: `GEPA` (Reflective Prompt Evolution)

The newest DSPy optimizer. Instead of randomly sampling instructions like MIPROv2, GEPA **reflects on what went wrong** in failed examples and uses that reflection to propose targeted improvements. Often gets MIPROv2-level results with way fewer LM calls.

**Docs link:** [GEPA Overview](https://dspy.ai/api/optimizers/GEPA/overview/) · [GEPA paper](https://arxiv.org/abs/2507.19457)

## What you'll learn

- The GEPA recipe: **score → reflect → propose → evaluate → keep-best → repeat**.
- Why "reflective" prompt evolution beats random search on most tasks.
- The `auto="light" | "medium" | "heavy"` budget control.
- How GEPA differs from MIPROv2 in practice: faster convergence, fewer total calls, often better final score.

## What's in this folder

- [`solution.py`](solution.py) — same Q&A program as folders 09 and 10, compiled with `GEPA`. Compares accuracy before vs after.
- [`requirements.txt`](requirements.txt) — `dspy>=3.0,<4.0`.

## Setup

```bash
pip install -r requirements.txt
```

## Run it

```bash
python3 solution.py
```

Expected: GEPA runs faster than MIPROv2 (`auto="light"` is ~5–15 min on Ollama). It prints reflection traces — *why* it thinks the current prompt fails, *what* it's proposing to change.

## Key concepts

### Reflective evolution
GEPA's loop:

1. **Run** the current best program on a batch of train examples.
2. **Score** each run with your metric.
3. **Reflect**: ask an LLM to analyze the trace of *failed* runs and propose what's wrong with the current prompt.
4. **Propose**: ask the LLM to write a new candidate prompt that addresses the failure modes.
5. **Evaluate**: score the new candidate on a validation set.
6. **Keep** the best so far. Repeat.

This is structurally similar to evolutionary algorithms — but the "mutation" step is an LLM reading failures and proposing targeted edits, not random.

### Compared to MIPROv2

| | MIPROv2 | GEPA |
|---|---|---|
| Search method | Bayesian over (instructions × demos) | Reflective evolution on instructions |
| Demos? | Yes | Optional |
| Typical runtime | Higher | Lower |
| Strongest when | Lots of train data, good demos available | Hard tasks where you can articulate *why* failures happen |

In the original GEPA paper, GEPA matched or beat MIPROv2 on most benchmarks with **35× fewer rollouts**. That's a big deal when you're paying for LLM calls — or waiting on an Ollama 7B.

### `auto="light" | "medium" | "heavy"`
Same idea as MIPROv2:

| Setting | Approx iterations |
|---|---|
| `light` | 6 |
| `medium` | 12 |
| `heavy` | 18 |

For first-pass exploration, always start with `light`.

### Reading GEPA's output
GEPA prints (at progress-info level):
- The current candidate's instruction text.
- The validation score.
- The reflections used to propose the next candidate.

Read the reflections. They're often more interesting than the final score — they show you what the optimizer thinks is wrong with your prompt.

## Mini-tasks

1. Run `solution.py`. Compare GEPA's final accuracy to MIPROv2's from folder 10.
2. Bump `auto` to `medium`. Compare again — at the cost of ~3× more iterations, how much does the score improve?
3. Read GEPA's reflection output. Are the proposed prompt changes sensible? Sometimes they overshoot — note the failure modes.

## Common pitfalls

- **GEPA needs a metric that returns a float in [0, 1]** — booleans confuse the reflection step.
- **Running `auto="heavy"` overnight with Ollama** — be patient, or use a faster provider (HF Inference API or Anthropic) for these long compilation runs.
- **Treating GEPA as magic** — it's stronger than MIPROv2 on most tasks but not all. Always measure.

## Expected outcome

You've used GEPA, compared its result to MIPROv2, and read at least one reflection trace. You know GEPA is the optimizer to reach for when you have a hard task and limited budget.

## Next

→ [12 — Optimizer: BootstrapFinetune](../12-optimizer-finetune/)
