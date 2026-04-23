# Chapter 6 — The 🤗 Tokenizers library

The thing that turns text into numbers. Most "my model is weird" bugs trace back to this. By the end you'll stop treating tokenizers as a black box.

**Course link:** [Chapter 6 on the HF docs](https://huggingface.co/learn/llm-course/en/chapter6/1)

## What you'll learn

- **Three subword algorithms**: BPE (GPT-2/Llama), WordPiece (BERT), Unigram (T5/SentencePiece). They're not interchangeable.
- **Fast** (Rust-backed) vs **slow** (Python) tokenizers. Always fast unless you have a reason.
- Training a tokenizer from scratch on your own corpus.
- `offset_mapping` — how to map a token back to the original characters. Essential for NER and QA.
- Why the same text is "5 tokens" here and "8 tokens" there, and why that affects your context window and bill.

## What's in this folder

- [`solution.py`](solution.py) — (1) trains a small BPE tokenizer on a tiny corpus, (2) uses `offset_mapping` to map tokens back to source characters, (3) compares three tokenizers on the same sentence.
- [`requirements.txt`](requirements.txt) — `transformers`, `tokenizers`.

## Setup

```bash
pip install -r requirements.txt
```

## Run it

```bash
python3 solution.py
```

Expected: three demos. A fresh tokenizer you trained, an offset-mapping demo showing which token covers which characters, and a three-way comparison.

## Key concepts

### Subword tokenization in one paragraph
Models don't read text — they read integer IDs from a fixed-size vocabulary (typically 30k–100k entries). Whole words rarely fit; subword algorithms split rare words into pieces the vocabulary does contain. So `"tokenization"` might be `["token", "##ization"]` in BERT, or `["token", "ization"]` in GPT-2.

### BPE / WordPiece / Unigram
Three ways to decide what goes in the vocabulary:

- **BPE** (Byte Pair Encoding) — greedily merge the most common character pair. Used by GPT, Llama, RoBERTa.
- **WordPiece** — similar to BPE but merges the pair that maximizes likelihood. Used by BERT, DistilBERT.
- **Unigram / SentencePiece** — start with a large vocab, prune the least useful tokens. Used by T5, mBART.

In practice, for most tasks they perform similarly on well-pretrained models. Knowing which is which matters when you train a new tokenizer.

### `offset_mapping`
```python
enc = tokenizer(text, return_offsets_mapping=True)
for token_id, (start, end) in zip(enc["input_ids"], enc["offset_mapping"]):
    print(f"{tokenizer.decode([token_id])!r} -> chars [{start}:{end}] = {text[start:end]!r}")
```
You need this any time you want to highlight a token back in the source, or align token-level labels (NER, QA) with character-level inputs.

### Training a new tokenizer
```python
new_tokenizer = old_tokenizer.train_new_from_iterator(corpus_iter, vocab_size=32000)
```
Takes minutes, not hours. The result: a tokenizer tuned to *your* domain's vocabulary, often 30–50% more efficient than a general-purpose one on that domain.

## Mini-tasks

1. Train a tokenizer on a small Python codebase. Compare its token count on a Python file vs the GPT-2 tokenizer's count. The domain-specific one should be smaller.
2. Use `offset_mapping` to highlight which characters in a sentence map to which tokens (e.g., print the sentence with `|` between token boundaries).
3. Tokenize a French or German sentence with `bert-base-uncased`. Count tokens. Now do it with `xlm-roberta-base`. The multilingual one is far more efficient for non-English text.

## Focus vs skim

- **Focus:** section 2 (training a new tokenizer from an old one), section 3 (fast tokenizer powers — especially `offset_mapping`).
- **Skim on first pass:** sections 5–7 (BPE/WP/Unigram internals). Fascinating but you can ship a year of projects without knowing them. Return when you have time.

## Common pitfalls

- **Using the wrong tokenizer for a checkpoint** — `AutoTokenizer.from_pretrained("bert-base")` plus a GPT-2 model gives nonsense. Always use the checkpoint's matching tokenizer.
- **Forgetting special tokens** — `[CLS]`, `[SEP]`, `<|endoftext|>`, etc. Each family has its own. `tokenizer.encode(text)` handles them for you; manual ID construction does not.
- **Inflated token counts for emojis, CJK, or code** — if you're surprised by a bill, it's usually this.

## Expected outcome

You can train a tokenizer, use `offset_mapping` for any task that needs character alignment, and predict in advance whether a model will be efficient on a given type of text.

## Next

→ [Chapter 7 — Classical NLP tasks](../chapter-07-classical-nlp-tasks/)
