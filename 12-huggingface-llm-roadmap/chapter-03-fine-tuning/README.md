# Chapter 3 — Fine-tuning a pretrained model

Your first real training run. By the end you'll have fine-tuned a small BERT-style model on a classification task, looked at the loss curves, and understood what "3 epochs at lr=5e-5" actually means.

**Course link:** [Chapter 3 on the HF docs](https://huggingface.co/learn/llm-course/en/chapter3/1)

## What you'll learn

- **Transfer learning** — why fine-tuning beats training from scratch.
- The `Trainer` API (`TrainingArguments` + `Trainer`) — 95% of your training needs in 20 lines.
- Reading **learning curves**: underfit vs overfit vs clean convergence.
- The `evaluate` library — picking the right metric (accuracy, F1, BLEU, ROUGE).
- What `seed`, `epochs`, `batch_size`, and `learning_rate` each do, approximately.

## What's in this folder

- [`solution.py`](solution.py) — fine-tunes `distilbert-base-uncased` on GLUE/MRPC (paraphrase detection). Short and canonical — this is the course's default example.
- [`requirements.txt`](requirements.txt) — `transformers`, `datasets`, `evaluate`, `torch`, `accelerate`.

## Setup

```bash
pip install -r requirements.txt
```

**You want a GPU for this.** On a CPU, fine-tuning takes 1–2 hours. On a free Colab T4, it takes ~5 minutes.

Quickest path: [open solution.py in Colab](https://colab.research.google.com) — upload the file, install the requirements, run it. Or spin up a T4 Kaggle notebook.

## Run it

```bash
python3 solution.py
```

Expected: the script downloads MRPC (~3 MB), tokenizes it, fine-tunes DistilBERT for 3 epochs, and prints final accuracy + F1 on the validation set. You should see accuracy around 0.83–0.87 and F1 around 0.88–0.91.

## Key concepts

### `Trainer` and `TrainingArguments`
`TrainingArguments` holds the hyperparameters (learning rate, batch size, epochs, output dir). `Trainer` holds the moving parts (model, data, optimizer, metrics) and runs the loop. Between them, they handle ~95% of training runs.

```python
args = TrainingArguments(output_dir="out", eval_strategy="epoch", learning_rate=5e-5, num_train_epochs=3)
trainer = Trainer(model=model, args=args, train_dataset=..., eval_dataset=..., compute_metrics=...)
trainer.train()
```

### Learning curves
After training, look at `trainer.state.log_history`. Three shapes to recognize:

- **Good run**: train loss goes down, validation loss goes down, they plateau together.
- **Overfit**: train loss keeps going down, validation loss bottoms out and starts rising. Stop earlier or add regularization.
- **Underfit**: both losses are still going down at the end. Train longer or use a bigger model.

### Picking a metric
Accuracy is fine for balanced classification. For imbalanced data (e.g., fraud detection, rare-disease labels), use F1. For generation, use ROUGE (summarization) or BLEU (translation). The `evaluate` library has one-liners for all of these.

## Mini-tasks

1. Re-run with `learning_rate=1e-1` instead of `5e-5`. Watch the loss explode. This trains your eye for "wrong LR."
2. Re-run with `num_train_epochs=10`. Does the validation F1 keep going up, or does it peak and drop? (This is overfitting in the flesh.)
3. Swap MRPC for another GLUE task (`sst2`, `cola`). How does the model do?

## Focus vs skim

- **Focus:** section 3 (Trainer API), section 5 (learning curves). These are 70% of the chapter's value.
- **Skim:** section 4 (manual training loop) on first pass. You'll come back when you need custom training logic.

## Common pitfalls

- **Forgetting to tokenize with `padding` and `truncation`** → the model gets ragged inputs and crashes.
- **Using the wrong `num_labels`** → `AutoModelForSequenceClassification.from_pretrained(model, num_labels=N)` must match the dataset's label count.
- **Not calling `trainer.evaluate()`** → the reported training loss is *training* loss. Always evaluate on the validation set separately.

## Expected outcome

You've fine-tuned a model end-to-end, read the loss curves, and understand the knobs. You're ready to push it to the Hub (Chapter 4).

## Next

→ [Chapter 4 — Sharing models and tokenizers](../chapter-04-sharing-models/)
