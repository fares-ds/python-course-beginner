# Chapter 1 — Transformer models

The conceptual on-ramp. By the end you should be able to (a) explain in one sentence what a Transformer is, (b) name three families and a use case for each, and (c) call `pipeline()` for half a dozen tasks without looking up the syntax.

**Course link:** [Chapter 1 on the HF docs](https://huggingface.co/learn/llm-course/en/chapter1/1)

## What you'll learn

- The `pipeline()` function — your "easy mode" entry point.
- The 8 task strings every NLP person knows by heart (sentiment, generation, ner, qa, summarization, translation, fill-mask, zero-shot).
- The three Transformer families: **encoder-only** (BERT), **decoder-only** (GPT/Llama), **encoder-decoder** (T5/BART).
- "Pretraining" vs "fine-tuning" — what's expensive vs cheap, what you do vs what they do.
- The bias problem — models inherit the biases of their data.

## What's in this folder

- [`solution.py`](solution.py) — runs five different `pipeline()` tasks back-to-back so you can see the API shape across them.
- [`requirements.txt`](requirements.txt) — `transformers` + `torch`.

## Setup

```bash
pip install -r requirements.txt
```

First run downloads ~600 MB of small models. One-time.

## Run it

```bash
python3 solution.py
```

Expected: five task demos print one after the other (sentiment, zero-shot classification, text generation, NER, fill-mask). Each one labelled clearly.

## Key concepts

### `pipeline(task, model=None)`
The function that wraps "tokenize → forward pass → post-process" into one call. If you don't pass `model=`, HF picks a sensible default for that task. For learning, pass `model=` explicitly so you know what you're running.

### Three families, one sentence each
- **Encoder** — reads the whole input bidirectionally, outputs a vector or label. Use for: classification, NER, embeddings.
- **Decoder** — reads left-to-right, generates one token at a time. Use for: chat, completion, code.
- **Encoder-decoder** — reads input, generates output. Use for: translation, summarization.

### Pretraining vs fine-tuning
- **Pretraining**: $1M-$100M of compute, done once by a lab on the entire internet. You don't do this.
- **Fine-tuning**: $1-$100 of compute, done by you on your task. Chapter 3 teaches this.

## Mini-tasks (after running solution.py)

1. Run `pipeline("sentiment-analysis")` on five sentences of your own writing. Find one where it's wrong. Why?
2. Try `pipeline("translation_en_to_fr")` on a long English paragraph. Notice it'll silently truncate. Look up the model's max length.
3. Try `pipeline("text-generation", model="gpt2")` with the same prompt 3 times. Why are the outputs different even with the same prompt?

## Focus vs skim (for the official chapter)

- **Focus on:** sections 3 (what they can do), 4 (how they work), 6 (architectures).
- **Skim:** section 9 (bias) — read once, don't memorize. Section 11 (certification exam) is optional.

## Common pitfalls

- **Treating defaults as production-ready** — `pipeline("sentiment-analysis")` ships a tiny English-only model. Don't deploy it on French tweets.
- **Passing huge inputs to `text-generation`** — by default it generates only ~20 tokens. Pass `max_new_tokens=200` if you want more.

## Expected outcome

You can pick a task name, call `pipeline(task)`, and predict roughly what the output shape will be (a dict? a list of dicts? a string?).

## Next

→ [Chapter 2 — Using 🤗 Transformers](../chapter-02-using-transformers/)
