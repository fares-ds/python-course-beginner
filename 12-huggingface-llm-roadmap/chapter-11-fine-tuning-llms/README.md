# Chapter 11 — Fine-Tune Large Language Models

The chapter most people come to the course for. Don't rush it. By the end you'll have fine-tuned a real chat model with LoRA on a single consumer GPU.

**Course link:** [Chapter 11 on the HF docs](https://huggingface.co/learn/llm-course/en/chapter11/1)

## What you'll learn

- **Chat templates** — `tokenizer.apply_chat_template(...)` and why you should never hand-format messages.
- **SFTTrainer** (from `trl`) — `Trainer`'s cousin, purpose-built for supervised LLM fine-tuning.
- **LoRA** (Low-Rank Adaptation) — fine-tune a 7B model by training only ~0.1% of the weights. Makes consumer-GPU fine-tuning possible.
- **Evaluation for generative models** — ROUGE, BERTScore, LLM-as-judge. Accuracy doesn't apply.

## What's in this folder

- [`solution.py`](solution.py) — LoRA-fine-tunes a small instruction model (~0.5B params) on a 1k-example slice of the Alpaca dataset. Runs on a Colab T4 in ~1 hour.
- [`requirements.txt`](requirements.txt) — `transformers`, `trl`, `peft`, `datasets`, `accelerate`, `bitsandbytes`.

## Setup

```bash
pip install -r requirements.txt
```

**You want a GPU with at least 12 GB of VRAM.** Free Colab T4 works (16 GB). For CPU only, you'd wait hours — not realistic.

## Run it

```bash
python3 solution.py
```

Expected: loads `Qwen/Qwen2.5-0.5B`, attaches LoRA adapters, fine-tunes on 1k Alpaca examples for ~1 hour on a T4, saves the adapter weights (~10 MB, not the full model) to `./qwen-alpaca-lora/`. The script also prints generations from the base vs fine-tuned model on 3 prompts.

## Key concepts

### Chat templates
Modern instruct-tuned LLMs expect a specific format:

```
<|im_start|>user
What's the capital of France?<|im_end|>
<|im_start|>assistant
Paris.<|im_end|>
```

Every model family has its own format. **Never hand-format these.** Use:

```python
messages = [
    {"role": "user", "content": "What's the capital of France?"},
    {"role": "assistant", "content": "Paris."},
]
text = tokenizer.apply_chat_template(messages, tokenize=False)
```

The tokenizer reads the format from the model's config and applies it correctly. If you hand-format and get it wrong, the model will produce subtly-off outputs.

### SFTTrainer vs Trainer
`SFTTrainer` (from `trl`) is `Trainer` with defaults tuned for supervised fine-tuning of LLMs:
- Handles `apply_chat_template` automatically.
- Supports packing (stuff multiple short examples into one sequence).
- Pairs with `peft` for LoRA seamlessly.

The underlying training loop is the same as `Trainer`. If you understand Chapter 3, you understand SFTTrainer.

### LoRA in one paragraph
Instead of updating all the model's weights, you add small "adapter" matrices beside the attention layers and only train those. For a 7B model, you might train 10 MB of adapter weights instead of 28 GB of full weights. Quality is ~90–95% of full fine-tuning. Memory and compute savings are huge.

```python
from peft import LoraConfig
lora = LoraConfig(
    r=16,                          # rank — higher = more capacity, more params
    lora_alpha=32,
    target_modules="all-linear",   # which layers to adapt
    task_type="CAUSAL_LM",
)
```

### Evaluating generative models
Accuracy is meaningless for generation. Instead:

- **ROUGE / BLEU** — n-gram overlap with a reference. Fast, cheap, brittle.
- **BERTScore** — semantic similarity using embeddings. Slower, better.
- **LLM-as-judge** — ask GPT-4 (or Claude) to rate your output vs a baseline. Accurate but expensive.
- **Hand evaluation** — 20 prompts, score each by hand. Tedious but the gold standard.

For this chapter's mini-tasks, hand evaluation on 10 prompts is plenty.

## Mini-tasks

1. Run `tokenizer.apply_chat_template` on `[{"role": "user", "content": "hi"}, {"role": "assistant", "content": "hey"}]` for three models (`Qwen2.5-0.5B-Instruct`, `Llama-3.2-1B-Instruct`, any Mistral). Compare the output strings — notice each family's format.
2. Run `solution.py` to do the LoRA fine-tune. Then load the adapter and generate on 10 prompts with both the base and fine-tuned model. Which does better?
3. Try `r=4` vs `r=64` — a tiny adapter vs a big one. How different are the results?

## Focus vs skim

- **Focus:** all sections. This chapter is small but dense.

## Common pitfalls

- **Forgetting the chat template on training data** — you'll fine-tune on "rawinput" instead of "<|im_start|>user\nrawinput<|im_end|>", and the model will produce weird output.
- **LoRA on non-instruct base models** — `Qwen2.5-0.5B` (no "-Instruct") has no chat template by default. Start from the instruct version.
- **Expecting the fine-tune to teach new facts** — it teaches style and format. For facts, use RAG (Agents Course, Unit 3).
- **Running out of memory** — set `load_in_4bit=True` or drop batch size and increase `gradient_accumulation_steps`.

## Expected outcome

You've fine-tuned a real chat model with LoRA. You understand the difference between base and fine-tuned outputs viscerally.

## Next

→ [Chapter 12 — Build Reasoning Models](../chapter-12-reasoning-models/)
