# Chapter 8 — three common mistakes, caught and diagnosed.
#
# Each demo deliberately triggers a canonical HF error. We catch it, print
# the traceback, and explain what the fix is. Reading these patterns once
# saves you hours when you hit them for real.

import traceback


def section(title):
    print()
    print("=" * 60)
    print(title)
    print("=" * 60)


def demo_wrong_automodel_class():
    section("MISTAKE 1: wrong AutoModel class for the task")
    # AutoModel returns the raw transformer outputs (a big tensor).
    # AutoModelForSequenceClassification adds a classification head.
    # Beginners often pick the wrong one and get a "has no attribute
    # 'logits'" error later.
    try:
        from transformers import AutoModel, AutoTokenizer
        tok = AutoTokenizer.from_pretrained("distilbert-base-uncased")
        model = AutoModel.from_pretrained("distilbert-base-uncased")  # wrong class!
        inputs = tok("Hello", return_tensors="pt")
        out = model(**inputs)
        # This attribute doesn't exist on AutoModel outputs:
        print(out.logits)
    except AttributeError as e:
        traceback.print_exc()
        print()
        print("  Diagnosis: AutoModel returns `last_hidden_state`, not `logits`.")
        print("  Fix: use AutoModelForSequenceClassification (or the right 'For' class")
        print("       for your task) to get task-specific outputs.")


def demo_mismatched_num_labels():
    section("MISTAKE 2: num_labels doesn't match the dataset")
    try:
        import torch
        from transformers import AutoModelForSequenceClassification, AutoTokenizer
        tok = AutoTokenizer.from_pretrained("distilbert-base-uncased")
        # Say your dataset has 3 classes, but you forgot to set num_labels=3:
        model = AutoModelForSequenceClassification.from_pretrained(
            "distilbert-base-uncased",  # defaults to num_labels=2
        )
        inputs = tok("Hello", return_tensors="pt")
        # Labels say "class 2" — illegal for a 2-class model.
        outputs = model(**inputs, labels=torch.tensor([2]))
        print(outputs.loss)
    except (IndexError, RuntimeError) as e:
        traceback.print_exc()
        print()
        print("  Diagnosis: the model has a 2-class head but you handed it class ID 2.")
        print("  Fix: pass num_labels=N when you load the model, where N matches your data.")


def demo_tokenizer_model_mismatch():
    section("MISTAKE 3: tokenizer doesn't match the model")
    # Loading a GPT-2 tokenizer and pairing it with a BERT model: the
    # token IDs don't align, so the model sees garbage. It won't raise
    # an error — it'll just silently give nonsense. That's the worst
    # kind of bug.
    try:
        from transformers import AutoModel, AutoTokenizer
        tok = AutoTokenizer.from_pretrained("gpt2")
        model = AutoModel.from_pretrained("bert-base-uncased")
        inputs = tok("Hello world", return_tensors="pt")
        # This may work without error, but the model sees meaningless IDs:
        out = model(**inputs)
        print(f"  This ran without error — hidden shape: {tuple(out.last_hidden_state.shape)}")
        print("  Diagnosis: no exception, but the output is NONSENSE.")
        print("  The GPT-2 vocab and BERT vocab are different. Always use the")
        print("  tokenizer that shipped with your model's checkpoint.")
    except Exception:
        traceback.print_exc()


def main():
    demo_wrong_automodel_class()
    demo_mismatched_num_labels()
    demo_tokenizer_model_mismatch()
    print("\nBookmark this page. You'll be back.")


if __name__ == "__main__":
    main()
