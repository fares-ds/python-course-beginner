# Chapter 3 — fine-tune DistilBERT on GLUE/MRPC.
#
# This is the course's canonical first-fine-tune example. ~5 min on a
# Colab T4 GPU; 1-2 hours on CPU. If you don't have a GPU, upload this
# file to Colab and select Runtime > Change runtime type > T4 GPU.
#
# MRPC = "Microsoft Research Paraphrase Corpus" — given two sentences,
# are they paraphrases of each other? (Binary classification.)

import evaluate
import numpy as np
from datasets import load_dataset
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    DataCollatorWithPadding,
    Trainer,
    TrainingArguments,
)

MODEL_NAME = "distilbert-base-uncased"
OUTPUT_DIR = "mrpc-distilbert-finetuned"


def main():
    # 1. Load the dataset.
    raw = load_dataset("glue", "mrpc")
    print(f"Train: {len(raw['train'])}, Validation: {len(raw['validation'])}")
    print(f"Labels: {raw['train'].features['label'].names}")

    # 2. Tokenize both sentences as a pair (MRPC's signature setup).
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    def tokenize(examples):
        return tokenizer(examples["sentence1"], examples["sentence2"], truncation=True)

    tokenized = raw.map(tokenize, batched=True)

    # 3. Build the model with a 2-class classification head.
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=2)

    # 4. Configure the trainer.
    # - eval_strategy="epoch": evaluate on validation set after each epoch.
    # - DataCollatorWithPadding: pads each batch to its own max length (efficient).
    args = TrainingArguments(
        output_dir=OUTPUT_DIR,
        eval_strategy="epoch",
        save_strategy="epoch",
        learning_rate=5e-5,
        per_device_train_batch_size=16,
        per_device_eval_batch_size=16,
        num_train_epochs=3,
        weight_decay=0.01,
        logging_steps=50,
        seed=42,
    )

    # 5. Metric: MRPC uses accuracy + F1 (because the positive class is less common).
    metric = evaluate.load("glue", "mrpc")

    def compute_metrics(eval_pred):
        preds = np.argmax(eval_pred.predictions, axis=1)
        return metric.compute(predictions=preds, references=eval_pred.label_ids)

    trainer = Trainer(
        model=model,
        args=args,
        train_dataset=tokenized["train"],
        eval_dataset=tokenized["validation"],
        tokenizer=tokenizer,
        data_collator=DataCollatorWithPadding(tokenizer),
        compute_metrics=compute_metrics,
    )

    # 6. Train and evaluate.
    trainer.train()
    final = trainer.evaluate()
    print("\nFinal validation metrics:")
    for k, v in final.items():
        print(f"  {k}: {v:.4f}" if isinstance(v, float) else f"  {k}: {v}")

    # Save locally. Chapter 4 shows how to push this to the Hub.
    trainer.save_model(OUTPUT_DIR)
    tokenizer.save_pretrained(OUTPUT_DIR)
    print(f"\nModel saved to ./{OUTPUT_DIR}/ — ready for Chapter 4.")


if __name__ == "__main__":
    main()
