# Chapter 6 — tokenizer tour: train, align, compare.

from transformers import AutoTokenizer


def section(title):
    print()
    print("=" * 60)
    print(title)
    print("=" * 60)


# A toy corpus — a few dozen lines of English. For a real project you'd
# train on millions of lines, but the code is the same.
TOY_CORPUS = [
    "Transformers are a type of neural network.",
    "The quick brown fox jumps over the lazy dog.",
    "Hugging Face builds tools for natural language processing.",
    "Subword tokenization handles unknown words by splitting them.",
    "BERT uses WordPiece. GPT-2 uses BPE. T5 uses Unigram.",
    "Tokenization is the bridge between text and integers.",
] * 20  # repeat so there's enough data for a small training run


def demo_train_new_tokenizer():
    section("DEMO 1: train a BPE tokenizer from scratch (tiny corpus)")
    old = AutoTokenizer.from_pretrained("gpt2")

    def corpus_iter():
        # `train_new_from_iterator` wants an iterator of strings or lists-of-strings.
        for i in range(0, len(TOY_CORPUS), 2):
            yield TOY_CORPUS[i:i + 2]

    # Small vocab for the demo; real training uses 30k - 100k.
    new_tok = old.train_new_from_iterator(corpus_iter(), vocab_size=500)
    sample = "BERT uses WordPiece tokenization."
    print(f"  Old (gpt2) tokens:    {old.tokenize(sample)}")
    print(f"  New (tiny) tokens:    {new_tok.tokenize(sample)}")


def demo_offset_mapping():
    section("DEMO 2: offset_mapping — tokens <-> characters")
    tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
    text = "Transformers are sneakier than they look."
    enc = tokenizer(text, return_offsets_mapping=True, add_special_tokens=False)
    print(f"  Text: {text!r}\n")
    for token_id, (start, end) in zip(enc["input_ids"], enc["offset_mapping"]):
        token_str = tokenizer.decode([token_id])
        print(f"  token={token_str!r:15s}  chars [{start:2d}:{end:2d}] = {text[start:end]!r}")


def demo_three_way_compare():
    section("DEMO 3: three tokenizers, same sentence")
    sentence = "The quick brown fox jumps over the unhappiness of tokenization."
    for model_name in ["bert-base-uncased", "gpt2", "t5-base"]:
        tok = AutoTokenizer.from_pretrained(model_name)
        tokens = tok.tokenize(sentence)
        print(f"  {model_name:22s} {len(tokens):>3} tokens   {tokens}")


def main():
    demo_train_new_tokenizer()
    demo_offset_mapping()
    demo_three_way_compare()
    print("\nOn to Chapter 7 — classical NLP tasks.")


if __name__ == "__main__":
    main()
