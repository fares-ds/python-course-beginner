# 12 — Optimizer: `BootstrapFinetune` (touches model weights)

The one DSPy optimizer that actually fine-tunes the underlying language model. Where every other optimizer tunes the **prompt**, `BootstrapFinetune` distills your unoptimized DSPy program into a *fine-tuned* small model that runs cheaper and faster.

**Important:** this optimizer needs a finetuning provider (Together AI, OpenAI fine-tuning, etc.). It does **not** work with pure local Ollama. The script in this folder gracefully no-ops if no provider is configured.

**Docs link:** [BootstrapFinetune API](https://dspy.ai/api/optimizers/BootstrapFinetune/)

## What you'll learn

- When to fine-tune the model vs just optimize the prompt.
- The `BootstrapFinetune` recipe: bootstrap traces with a teacher model, then fine-tune a smaller student on those traces.
- Why this is sometimes the right move: cheaper inference, lower latency, better domain alignment.
- Why it's *usually not* the right first move (prompt optimization is faster, cheaper, and often enough).

## What's in this folder

- [`solution.py`](solution.py) — a runnable skeleton. Without `TOGETHER_API_KEY` (or another configured finetune provider), it prints a setup guide and exits cleanly.
- [`requirements.txt`](requirements.txt) — `dspy>=3.0,<4.0`.

## Setup (the long path)

To actually run a fine-tune you need:

1. A **Together AI** account (or another provider DSPy supports for finetuning). Free tier is enough for experimenting.
2. `pip install dspy[together]` (or follow Together's setup docs).
3. `export TOGETHER_API_KEY=...`.

Or, if you don't want to set this up, just **read this folder's README and `solution.py`** to understand the pattern. The other 13 folders give you the full DSPy stack without needing a finetune provider.

## Run it

```bash
python3 solution.py
```

Expected without a finetune provider: prints a clear "skipping — no provider configured" message and the setup steps.

With a provider: uploads training data, kicks off a finetune job, and (after ~10–60 min depending on data size and provider) returns a compiled program backed by the fine-tuned model.

## Key concepts

### Prompt optimization vs weight optimization

| | Prompt optimization (folders 09–11) | Weight optimization (this folder) |
|---|---|---|
| What changes | Instruction text + few-shot demos | Model weights themselves |
| Inference cost | Same as base model + bigger prompt | Often *cheaper* (smaller model can replace bigger one) |
| Setup | None beyond DSPy | A finetune provider, training pipeline |
| Best when | Quick wins, model already capable | Production cost / latency matters; you have lots of training data |

### The "teacher-student distillation" pattern
`BootstrapFinetune`:

1. Runs your unoptimized program (the "teacher") on training questions.
2. Filters successful runs by your metric.
3. Sends those (input → trace → output) tuples to a finetuning API to train a smaller student model.
4. Returns a compiled program that uses the *student* model.

The student is cheaper to run than the teacher. If accuracy survives, you've shrunk inference cost.

### Why prompt optimization usually wins first
- Prompt opt is **free** and **fast** (folders 09–11 take minutes to hours).
- Fine-tuning is **paid** and **slow** (hours to days, plus ongoing inference cost on the new model).
- Most quality gains come from a better prompt, not better weights.

Reach for `BootstrapFinetune` only after MIPROv2/GEPA have plateaued and you need either lower cost or much higher throughput.

## Mini-tasks

1. Read `solution.py`. Map the steps to the "teacher-student" diagram above.
2. (Optional) Set up a Together AI account, export the key, run the script. Compare cost-per-call before vs after.
3. Sketch the cost math: if your prompt-optimized program costs $X per 1k calls and the fine-tuned student costs $Y per 1k calls, at what call volume does fine-tuning pay back the upfront cost?

## Common pitfalls

- **Fine-tuning before prompt optimization is plateauing** — wasted money and time. Always run MIPROv2/GEPA first.
- **Tiny train sets** — fine-tuning needs hundreds-to-thousands of examples to beat a well-prompted base model. With <100 examples, prompt optimization is almost always better.
- **Forgetting that the student is a different model** — its bias / safety / style profile differs. Re-evaluate beyond just your task metric.

## Expected outcome

You understand when fine-tuning fits in the DSPy story (rarely, and late). You can read a `BootstrapFinetune` script without confusion.

## Next

→ [13 — Saving and Deployment](../13-saving-and-deployment/)
