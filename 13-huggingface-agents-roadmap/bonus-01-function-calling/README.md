# Bonus Unit 1 — Fine-tuning an LLM for Function Calling

Small open models often emit messy function calls. Fine-tuning on a clean function-calling dataset can make a 7B model competitive with much larger ones for *your* specific tools.

**Course link:** [Bonus 1 on the HF docs](https://huggingface.co/learn/agents-course/bonus-unit1/introduction)

**Pick this if:** you finished Project 12 (LLM Course) and want to deepen the fine-tuning side. Pairs naturally with Chapter 11 (LoRA fine-tuning).

## What you'll learn

- What "function calling" actually is — a structured-output format the LLM emits, that the framework parses.
- Why open models often struggle with function calling out of the box.
- How to fine-tune a small model on a function-calling dataset (SFT + LoRA).
- Why fine-tuned function-callers are sometimes better than bigger models for your specific tool surface.

## What's in this folder

- [`solution.py`](solution.py) — LoRA-fine-tunes a 0.5B model on a small function-calling dataset (`Salesforce/xlam-function-calling-60k`, sliced to 1000 examples). Saves the adapter to `./xlam-lora/`.
- [`requirements.txt`](requirements.txt) — `transformers`, `trl`, `peft`, `datasets`, `accelerate`.

## Setup

```bash
pip install -r requirements.txt
```

**GPU required.** Free Colab T4 is enough.

## Run it

```bash
python3 solution.py
```

Expected: ~30 min on a T4. Saves a tiny LoRA adapter (~10 MB) that, when loaded on top of the base model, makes it noticeably better at producing well-formed function calls for the tool schema you trained on.

## Key concepts

### Function calling format
The LLM emits something like:

```json
{
  "name": "get_weather",
  "arguments": {"city": "Paris", "units": "celsius"}
}
```

The framework parses this, calls `get_weather(city="Paris", units="celsius")`, and feeds the result back to the LLM as an "observation."

Different model families use different formats — some embed in markdown code blocks, some use special tokens, some use XML. The chat template handles this for you (most of the time).

### Why fine-tune for it?
- Small open models (under 7B) often produce **invalid JSON** — extra commas, missing quotes, inventing argument names that don't exist in your schema.
- Fine-tuning on 1k–10k clean examples teaches the model the **format and the discipline**, not new capabilities. It's a very high-leverage fine-tune.
- After fine-tuning, a 1B model can match or beat an unmodified 70B on *your specific tool surface*.

### When NOT to do this
- If you're using GPT-4o / Claude / Gemini, they already function-call well. Don't fine-tune.
- If your tool surface is small (≤3 tools) and well-known, prompt engineering is usually enough.
- If you don't have a clean dataset of (user, tool_call) pairs, get one first.

## Mini-tasks

1. Run `solution.py` to completion.
2. Compare the base model's tool calls vs the fine-tuned model's on 10 hand-crafted prompts. Score by hand: well-formed JSON? Right tool? Right args?
3. (Hard) Try the same with `r=4` vs `r=64`. Tiny adapters vs bigger ones — which works better here?

## Focus vs skim

- **Focus:** the entire bonus unit — it's small.

## Common pitfalls

- **Tiny dataset (<200 examples)** — won't move the needle. Aim for 1k+.
- **Fine-tuning the wrong layer** — for function calling, `target_modules="all-linear"` is a safe default in `LoraConfig`.
- **Forgetting to use the matching chat template at inference time** — the tokenizer's `apply_chat_template` is your friend.

## Expected outcome

You can take a small open model that's bad at function calling and turn it into one that's good at it for your specific tools.

## Next

→ [Bonus 2 — Observability and Evaluation](../bonus-02-observability/)
