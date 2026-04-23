# 10 — Optimizer: `MIPROv2`

The most-used DSPy optimizer. Where `BootstrapFewShot` only picks demos, `MIPROv2` **jointly tunes instructions and demos**: it proposes alternative system prompts, samples demo combinations, and uses Bayesian optimization to pick the best mix.

**Docs link:** [MIPROv2 API](https://dspy.ai/api/optimizers/MIPROv2/)

## What you'll learn

- What MIPROv2 actually does that BootstrapFewShot doesn't.
- The `auto="light"` / `"medium"` / `"heavy"` shortcut for picking budget.
- Why MIPROv2 needs more train calls (and money / Ollama time) than `BootstrapFewShot`.
- How to read its progress output: candidate proposals, validation scores, the chosen winner.

## What's in this folder

- [`solution.py`](solution.py) — same Q&A program as folder 09, but compiled with `MIPROv2(auto="light")`. Compares accuracy before vs after.
- [`requirements.txt`](requirements.txt) — `dspy>=3.0,<4.0`.

## Setup

```bash
pip install -r requirements.txt
```

## Run it

```bash
python3 solution.py
```

Expected: ~10–30 min on Ollama. MIPROv2 makes many more calls than BootstrapFewShot — it's proposing alternative instructions and scoring each. The `auto="light"` setting limits it to a small budget; for serious tuning you'd use `medium` or `heavy`.

## Key concepts

### MIPROv2 in three sentences
1. **Bootstrap demos** (same as `BootstrapFewShot`).
2. **Propose new instructions** — uses an LLM to draft 5–20 alternative versions of every signature's docstring.
3. **Bayesian search** over (instructions × demo combinations) to find the configuration that maximizes the metric on a validation set.

The output is a compiled program where every Predict/CoT inside has a tuned instruction and the best-found demos.

### `auto="light" | "medium" | "heavy"`
Three preset budgets:

| Setting | Approx LM calls | When to use |
|---|---|---|
| `light` | ~50–200 | Sanity check, prototyping |
| `medium` | ~500–1500 | Most real runs |
| `heavy` | ~3000+ | When you have lots of train data and you're optimizing the production model |

On Ollama with a 7B model, `light` is ~30 min; `medium` is several hours. On a fast OpenAI/Anthropic model, those are minutes / tens of minutes.

### Why MIPROv2 usually beats BootstrapFewShot
The instruction tuning step is the differentiator. A well-phrased instruction often improves a small model more than 4 extra few-shots do. MIPROv2 finds those phrasings automatically.

## Mini-tasks

1. Run `solution.py` with `auto="light"`. Compare against the BootstrapFewShot result from folder 09.
2. (Patient) Re-run with `auto="medium"`. Notice the much longer runtime and (usually) higher score.
3. Print the compiled program's chosen instruction (it's stored on each `Predict` sub-module). How different is it from the original signature docstring?

## Common pitfalls

- **Running `auto="medium"` on Ollama overnight without checking the trajectory** — DSPy prints incremental scores; if dev score plateaus early, kill the run and use the best-so-far.
- **Tiny dev set** — MIPROv2's signal is noisy with fewer than ~30 dev examples. Add more.
- **Tuning the metric and the program at the same time** — you'll fool yourself. Lock the metric before optimizing.

## Expected outcome

You can run MIPROv2, read its output, and compare to a `BootstrapFewShot` baseline. You know which preset to start with.

## Next

→ [11 — Optimizer: GEPA](../11-optimizer-gepa/)
