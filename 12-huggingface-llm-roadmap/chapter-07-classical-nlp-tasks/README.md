# Chapter 7 — Classical NLP tasks

The biggest, most hands-on chapter in the course. Seven canonical tasks: token classification (NER), masked LM, translation, summarization, training a causal LM from scratch, question answering, and a general "mastering LLMs" section.

**Don't try to do all seven in one week.** The course suggests picking 2–3. This folder picks **NER** as the in-depth example (most practical for real apps) and points you to the official chapter for the others.

**Course link:** [Chapter 7 on the HF docs](https://huggingface.co/learn/llm-course/en/chapter7/1)

## What you'll learn

- The workflow pattern that **all** the tasks share: load dataset → align labels → tokenize → fine-tune → evaluate.
- **Token classification** specifically: how word-level labels map onto subword tokens (this is the trickiest part).
- `seqeval` — the F1 metric for NER (not sklearn F1 — they score differently).
- When to pick which task and which model family.
- Why the data-prep step is the real skill (models are interchangeable; data isn't).

## What's in this folder

- [`solution.py`](solution.py) — fine-tunes `distilbert-base-uncased` on the CoNLL-2003 NER dataset. Evaluated with seqeval.
- [`requirements.txt`](requirements.txt) — adds `seqeval` to the Chapter 3 deps.

## Setup

```bash
pip install -r requirements.txt
```

**GPU strongly recommended.** On CPU, this takes an hour. On a Colab T4, ~10 minutes.

## Run it

```bash
python3 solution.py
```

Expected: the script loads CoNLL-2003 (~6 MB), aligns word-level labels to subword tokens, fine-tunes DistilBERT, and prints precision/recall/F1 per entity type. Final F1 ≈ 0.93.

## Key concepts

### The "align labels to subwords" problem
CoNLL has one label per **word**. But the tokenizer splits words into subwords. So `"Washington"` → `["Wash", "##ington"]` — two tokens, but only one label.

**The convention:** give the first subword the real label, and mark the continuation subwords with `-100` (PyTorch's "ignore" label). This is the step most NER pipelines get wrong.

```python
def align_labels(word_ids, word_labels):
    aligned = []
    prev = None
    for wid in word_ids:
        if wid is None:
            aligned.append(-100)            # special token (CLS, SEP) — ignore
        elif wid == prev:
            aligned.append(-100)            # continuation subword — ignore
        else:
            aligned.append(word_labels[wid])
        prev = wid
    return aligned
```

### `DataCollatorForTokenClassification`
A data collator that pads both inputs and labels correctly (padding the label sequence with `-100` so the loss ignores it). Use it instead of `DataCollatorWithPadding` for token classification.

### seqeval
The metric used by the CoNLL leaderboard. It's **span-level** F1 — getting `B-PER I-PER` on "Barack Obama" counts as 1 correct span, not 2 correct tokens. This matters: a model that predicts every single token correctly still gets 0 F1 on a span it split.

## Mini-tasks

1. Print the per-entity F1 (`PER`, `ORG`, `LOC`, `MISC`). Which is hardest? Why?
2. Run inference on your own sentence. Does it identify entities correctly? Try weird cases ("I saw Obama's dog eating apples").
3. (Harder) Swap token classification for **question answering**. The course has a dedicated section — the data prep is harder (span start/end alignment) but the training loop is similar.

## Recommended pairings

The course suggests picking 2–3 sections. Most useful pairings:

- **Token classification (this folder) + QA** → build apps that extract structured info from text.
- **MLM fine-tuning + summarization** → domain-adapt a model, then use it to summarize that domain.
- **Translation + summarization** → both are encoder-decoder workflows; doing both consolidates that pattern.

## Focus vs skim

- **Focus on:** the data-prep step of whichever tasks you pick. That's the real skill.
- **Skim:** section 6 ("Training a causal LM from scratch") — useful conceptually, expensive in practice (needs multi-GPU + a few days).

## Common pitfalls

- **Passing `label` instead of `labels`** to the model — HF models universally expect the plural. Easy typo, cryptic error.
- **Forgetting `-100`** on continuation subwords — the model "learns" that continuation tokens are all `O` (outside) and accuracy tanks.
- **Using `sklearn.f1_score`** for NER — it scores per-token, which overstates performance vs seqeval's per-span.

## Expected outcome

You can pick any of the classical NLP tasks, read the course section once, and implement it on a new dataset without re-reading from scratch.

## Next

→ [Chapter 8 — How to ask for help](../chapter-08-asking-for-help/)
