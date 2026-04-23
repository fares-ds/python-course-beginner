# Chapter 7 — fine-tune DistilBERT for Named Entity Recognition on CoNLL-2003.
#
# Use a GPU. On CPU: ~1 hour. On Colab T4: ~10 minutes.

import evaluate
import numpy as np
from datasets import load_dataset
from transformers import (
    AutoModelForTokenClassification,
    AutoTokenizer,
    DataCollatorForTokenClassification,
    Trainer,
    TrainingArguments,
)

MODEL_NAME = "distilbert-base-uncased"
OUTPUT_DIR = "conll-distilbert-ner"


def align_labels_with_subwords(examples, tokenizer):
    """CoNLL has one label per WORD. Tokenizer splits words into subwords.
    Convention: first subword keeps the label; continuation subwords get -100
    (PyTorch's "ignore in loss" sentinel)."""
    tokenized = tokenizer(
        examples["tokens"],
        is_split_into_words=True,   # tells the tokenizer inputs are pre-split into words
        truncation=True,
    )
    aligned_labels = []
    for i, word_labels in enumerate(examples["ner_tags"]):
        word_ids = tokenized.word_ids(batch_index=i)
        new_labels = []
        prev = None
        for wid in word_ids:
            if wid is None:
                new_labels.append(-100)
            elif wid == prev:
                new_labels.append(-100)
            else:
                new_labels.append(word_labels[wid])
            prev = wid
        aligned_labels.append(new_labels)
    tokenized["labels"] = aligned_labels
    return tokenized


def main():
    raw = load_dataset("conll2003", trust_remote_code=True)
    label_names = raw["train"].features["ner_tags"].feature.names
    print(f"Labels ({len(label_names)}): {label_names}")

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    tokenized = raw.map(
        lambda ex: align_labels_with_subwords(ex, tokenizer),
        batched=True,
        remove_columns=raw["train"].column_names,
    )

    model = AutoModelForTokenClassification.from_pretrained(
        MODEL_NAME,
        num_labels=len(label_names),
        id2label={i: l for i, l in enumerate(label_names)},
        label2id={l: i for i, l in enumerate(label_names)},
    )

    metric = evaluate.load("seqeval")

    def compute_metrics(eval_pred):
        logits, labels = eval_pred
        preds = np.argmax(logits, axis=-1)
        # Convert IDs to strings and drop -100 positions.
        true_preds, true_labels = [], []
        for p_row, l_row in zip(preds, labels):
            p_str, l_str = [], []
            for p, l in zip(p_row, l_row):
                if l == -100:
                    continue
                p_str.append(label_names[p])
                l_str.append(label_names[l])
            true_preds.append(p_str)
            true_labels.append(l_str)
        scores = metric.compute(predictions=true_preds, references=true_labels)
        return {
            "precision": scores["overall_precision"],
            "recall": scores["overall_recall"],
            "f1": scores["overall_f1"],
            "accuracy": scores["overall_accuracy"],
        }

    args = TrainingArguments(
        output_dir=OUTPUT_DIR,
        eval_strategy="epoch",
        save_strategy="epoch",
        learning_rate=2e-5,
        per_device_train_batch_size=16,
        per_device_eval_batch_size=16,
        num_train_epochs=3,
        weight_decay=0.01,
        logging_steps=50,
        seed=42,
    )

    trainer = Trainer(
        model=model,
        args=args,
        train_dataset=tokenized["train"],
        eval_dataset=tokenized["validation"],
        tokenizer=tokenizer,
        data_collator=DataCollatorForTokenClassification(tokenizer),
        compute_metrics=compute_metrics,
    )

    trainer.train()
    final = trainer.evaluate()
    print("\nFinal validation metrics:")
    for k, v in final.items():
        print(f"  {k}: {v:.4f}" if isinstance(v, float) else f"  {k}: {v}")


if __name__ == "__main__":
    main()
