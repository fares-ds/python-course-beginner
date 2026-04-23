# Chapter 4 — Sharing models and tokenizers

How to get your fine-tuned model out of `./output_dir/` and onto the Hugging Face Hub where anyone can load it with one line.

**Course link:** [Chapter 4 on the HF docs](https://huggingface.co/learn/llm-course/en/chapter4/1)

## What you'll learn

- The Hugging Face Hub as a **git-based** registry for models (and datasets, and Spaces).
- `push_to_hub()` from a `Trainer`, a model, or a tokenizer.
- Writing a **model card** — the README that ships with every model. Why it matters (reproducibility, safety, licensing).
- Public vs gated vs private repos.
- Licensing — Apache 2, MIT, OpenRAIL, when to use each.

## What's in this folder

- [`solution.py`](solution.py) — pushes the MRPC model you fine-tuned in Ch 3 (or any local model) to your HF account. Assumes you've already run `huggingface-cli login`.
- [`model_card_template.md`](model_card_template.md) — a fill-in-the-blanks template for a decent model card.
- [`requirements.txt`](requirements.txt) — `transformers`, `huggingface_hub`.

## Setup

```bash
pip install -r requirements.txt
huggingface-cli login     # must have a WRITE token (not just read)
```

Make sure you've done Chapter 3 first — this uploads the model that chapter produced.

## Run it

```bash
python3 solution.py
```

You'll be asked for a repo name (default: `your-username/mrpc-distilbert-finetuned`). The script pushes the weights + tokenizer + model card.

Visit `https://huggingface.co/your-username/mrpc-distilbert-finetuned` to see your model live.

## Key concepts

### `push_to_hub()`
Three places you'll see it:

```python
trainer.push_to_hub("my-model")          # from Trainer, after training
model.push_to_hub("my-model")            # from a model
tokenizer.push_to_hub("my-model")        # from a tokenizer
```

Behind the scenes: `git init` in your output dir, `git remote add` pointing at `huggingface.co/your-username/my-model`, commit everything, push. You can do it manually with git if you prefer.

### Model cards
The `README.md` that ships with every model on the Hub. A good one answers: what is this model? What was it trained on? What's it good at? What's it *not* good at? How well does it score? What license? Most deployment disasters are traceable to an unread model card.

### Public / gated / private
- **Public**: anyone can download.
- **Gated**: public, but users must agree to terms first (e.g., Llama, Gemma).
- **Private**: only you + collaborators.

Start public for personal work. Gate or privatize if licensing forces it.

## Mini-tasks

1. Push your MRPC model. Confirm it loads back from a fresh Python process: `AutoModel.from_pretrained("yourname/mrpc-distilbert-finetuned")`.
2. Edit the model card on the Hub website (click the Edit button). Add a real "Intended use" and "Limitations" section.
3. Delete your model (from settings) and re-push it — make sure the round trip works.

## Focus vs skim

- **Focus:** section 3 (sharing), section 4 (model cards). The mechanical "how to push" is short; the model-card thinking is what separates a portfolio model from a dump.
- **Skim:** — the chapter is small, read all of it.

## Common pitfalls

- **Read-only token** — `push_to_hub` fails with a 403. Generate a new token with "write" scope at `hf.co/settings/tokens`.
- **No model card** — the Hub lets you push without one. Don't. Even a 5-sentence card is better than nothing.
- **Leaking sensitive data** — if your training data contained PII, assume your model did too. Don't push publicly without thinking.

## Expected outcome

You have at least one model live on your HF profile, with a thoughtful model card. Your portfolio starts here.

## Next

→ [Chapter 5 — The 🤗 Datasets library](../chapter-05-datasets/)
