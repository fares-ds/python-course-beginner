---
license: apache-2.0
base_model: distilbert-base-uncased
tags:
  - text-classification
  - paraphrase-detection
datasets:
  - glue
metrics:
  - accuracy
  - f1
language:
  - en
---

# MRPC DistilBERT (fine-tuned)

A small paraphrase-detection model: given two English sentences, predicts whether they mean the same thing.

## Intended use

- Educational — this is a Chapter 3 exercise from the Hugging Face LLM Course.
- Playing with paraphrase detection on short English pairs.

## Not for

- Production-grade paraphrase detection (use a larger, better-evaluated model).
- Languages other than English.
- Sentence pairs longer than ~256 tokens (they get truncated).

## Training details

- **Base model:** `distilbert-base-uncased`
- **Dataset:** [GLUE / MRPC](https://huggingface.co/datasets/glue) (3,668 training pairs).
- **Epochs:** 3
- **Learning rate:** 5e-5
- **Batch size:** 16
- **Optimizer:** AdamW (default from `Trainer`)

## Evaluation

Results on the MRPC validation set (408 pairs):

| Metric   | Score |
|----------|-------|
| Accuracy | ~0.85 |
| F1       | ~0.90 |

(Your numbers will vary slightly — seed, GPU, version drift.)

## Limitations and biases

- Trained on news-wire paraphrases from the early 2000s; unusual on modern informal / social-media text.
- Inherits any biases from the base DistilBERT pretraining data (Wikipedia + BookCorpus).
- Only 2 classes (paraphrase / not paraphrase) — there's no "degree of similarity" score.

## How to use

```python
from transformers import pipeline

clf = pipeline("text-classification", model="YOUR-USERNAME/mrpc-distilbert-finetuned")
clf({"text": "The cat sat on the mat.", "text_pair": "A feline was resting on the rug."})
```
