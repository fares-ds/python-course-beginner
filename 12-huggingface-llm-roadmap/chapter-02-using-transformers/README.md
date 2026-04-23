# Chapter 2 — Using 🤗 Transformers

The "lift the hood" chapter. By the end you should be able to do everything `pipeline()` does, by hand, in ~15 lines of code. This is the single most important chapter in the first half of the course.

**Course link:** [Chapter 2 on the HF docs](https://huggingface.co/learn/llm-course/en/chapter2/1)

## What you'll learn

- What `pipeline()` is **actually doing** under the hood: tokenize → model forward pass → post-process.
- `AutoTokenizer` and `AutoModel` — the two halves of every Hugging Face workflow.
- Tokenizer outputs: `input_ids`, `attention_mask`, sometimes `token_type_ids`.
- Padding, truncation, and batching sequences of different lengths.
- Why models output **logits** (not probabilities) and how to convert one to the other with `softmax`.

## What's in this folder

- [`solution.py`](solution.py) — reproduces sentiment analysis manually (no `pipeline()`), then tokenizes the same sentence with three tokenizers from three model families.
- [`requirements.txt`](requirements.txt) — `transformers` + `torch`.

## Setup

```bash
pip install -r requirements.txt
```

## Run it

```bash
python3 solution.py
```

Expected: two demos. First, the manual `tokenize → model → softmax → label` flow. Second, a side-by-side of how BERT, GPT-2, and T5 chop up the same sentence into different numbers of tokens.

## Key concepts

### `AutoTokenizer.from_pretrained(name)`
Returns the tokenizer associated with a checkpoint. **Always use the tokenizer that came with the model** — using the wrong tokenizer is the single most common cause of "the model isn't working" bug reports.

### `AutoModel*.from_pretrained(name)`
There's a family: `AutoModel` (raw outputs), `AutoModelForSequenceClassification` (with a classification head), `AutoModelForCausalLM` (for generation), etc. Pick the one that matches your task — it determines the output shape.

### Logits → softmax → label
The model outputs **logits** (raw, unbounded scores per class). To get probabilities, apply `torch.softmax(logits, dim=-1)`. To get the predicted class, take `argmax`. To get the human-readable label, look it up in `model.config.id2label`.

### Padding and truncation
When you batch sentences of different lengths, you need to:
- **Pad** the shorter ones (so they all have the same length).
- **Truncate** the longer ones (if any exceed `max_length`).
- Use the `attention_mask` to tell the model which tokens are real vs padding.

```python
inputs = tokenizer(sentences, padding=True, truncation=True, return_tensors="pt")
```

## Mini-tasks (after running solution.py)

1. Modify `solution.py` to batch *three* sentences instead of one. Use `padding=True, truncation=True`. Print the `attention_mask` and notice the zeros at the end of the shorter ones.
2. Swap the model for `cardiffnlp/twitter-roberta-base-sentiment-latest`. Notice the labels change (now `negative/neutral/positive` instead of `NEGATIVE/POSITIVE`).
3. Print `model.config.id2label` for two different sentiment models. Confirm they don't agree on label names.

## Focus vs skim (for the official chapter)

- **Focus:** section 2 (behind the pipeline) — re-read it twice. Section 5 (handling multiple sequences). Section 6 (putting it together).
- **Skim:** section 8 (optimized inference deployment) — come back when you need to deploy.

## Common pitfalls

- **Forgetting `return_tensors="pt"`** — without it the tokenizer returns Python lists, and the model expects tensors. You'll get a confusing TypeError.
- **Confusing `AutoModel` with `AutoModelForSequenceClassification`** — `AutoModel` returns the raw transformer outputs (a long vector). The "For" variants add a task-specific head on top.

## Expected outcome

Given any task and any model on the Hub, you can write 15 lines of code that load the model + tokenizer, run inference, and return a label or generation — without `pipeline()`.

## Next

→ [Chapter 3 — Fine-tuning a pretrained model](../chapter-03-fine-tuning/)
