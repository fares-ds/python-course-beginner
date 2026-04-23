# Chapter 2 — behind the pipeline.
#
# Two demos:
#   1. Sentiment analysis without pipeline() — the three steps spelled out.
#   2. Same sentence, three tokenizers — see how subword splitting varies.

import torch
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
)

SENTIMENT_MODEL = "distilbert-base-uncased-finetuned-sst-2-english"

COMPARE_MODELS = [
    "bert-base-uncased",   # WordPiece    (encoder family)
    "gpt2",                # BPE          (decoder family)
    "t5-base",             # SentencePiece/Unigram (encoder-decoder family)
]

SAMPLE_TEXT = "Transformers are awesome and tokenization is sneakier than it looks."


def section(title):
    print()
    print("=" * 60)
    print(title)
    print("=" * 60)


def demo_behind_pipeline():
    section("DEMO 1: behind the pipeline")
    tokenizer = AutoTokenizer.from_pretrained(SENTIMENT_MODEL)
    model = AutoModelForSequenceClassification.from_pretrained(SENTIMENT_MODEL)

    sentence = "Hugging Face is genuinely good."
    print(f"  Input text: {sentence!r}")

    # STEP 1: text -> integer IDs the model understands.
    inputs = tokenizer(sentence, return_tensors="pt")
    print(f"  input_ids:  {inputs['input_ids'][0].tolist()}")
    print(f"  tokens:     {tokenizer.convert_ids_to_tokens(inputs['input_ids'][0])}")

    # STEP 2: input IDs -> logits (raw, unnormalized scores per class).
    # torch.no_grad() turns off gradient tracking — we're not training.
    with torch.no_grad():
        outputs = model(**inputs)
    print(f"  logits:     {[round(x, 3) for x in outputs.logits[0].tolist()]}")

    # STEP 3: logits -> probabilities -> label.
    probs = torch.softmax(outputs.logits, dim=-1)[0]
    label_id = int(probs.argmax())
    label = model.config.id2label[label_id]
    print(f"  probs:      {[round(x, 3) for x in probs.tolist()]}")
    print(f"  label map:  {model.config.id2label}")
    print(f"  -> {label} (score={probs[label_id].item():.3f})")


def demo_tokenizer_compare():
    section("DEMO 2: same sentence, three tokenizers")
    print(f"  Sentence: {SAMPLE_TEXT!r}\n")
    for model_name in COMPARE_MODELS:
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        tokens = tokenizer.tokenize(SAMPLE_TEXT)
        print(f"  {model_name:30s}  {len(tokens):>3} tokens")
        print(f"    {tokens}")
        print()


def main():
    demo_behind_pipeline()
    demo_tokenizer_compare()
    print("On to Chapter 3 — fine-tuning.")


if __name__ == "__main__":
    main()
