# Chapter 1 — five pipeline() tasks back-to-back.
#
# Same API shape (pipeline(task)(input)), five different jobs. The point of
# running this is to feel how the API looks across tasks before going deeper.
#
# First run downloads ~600 MB of models (cached afterward).

from transformers import pipeline


def section(title):
    print()
    print("=" * 60)
    print(title)
    print("=" * 60)


def demo_sentiment():
    section("1. Sentiment analysis (encoder model)")
    clf = pipeline("sentiment-analysis")
    for sentence in ["This course is great.", "This is awful."]:
        result = clf(sentence)[0]
        print(f"  {sentence!r} -> {result['label']} ({result['score']:.3f})")


def demo_zero_shot():
    section("2. Zero-shot classification (no fine-tuning needed)")
    clf = pipeline("zero-shot-classification")
    sentence = "The new movie is full of stunning special effects."
    labels = ["technology", "entertainment", "politics", "sports"]
    result = clf(sentence, candidate_labels=labels)
    # Result includes parallel `labels` and `scores` lists, sorted high to low.
    for label, score in zip(result["labels"], result["scores"]):
        print(f"  {label:14s} {score:.3f}")


def demo_text_generation():
    section("3. Text generation (decoder model)")
    gen = pipeline("text-generation", model="gpt2")
    prompt = "In the year 2050, machine learning will"
    out = gen(prompt, max_new_tokens=30, num_return_sequences=1)
    print(f"  Prompt:     {prompt!r}")
    print(f"  Completion: {out[0]['generated_text']}")


def demo_ner():
    section("4. Named entity recognition (token classification)")
    ner = pipeline("ner", grouped_entities=True)
    sentence = "Hugging Face is a company based in New York City."
    for entity in ner(sentence):
        # `entity_group` is the label (PER, ORG, LOC, MISC).
        print(f"  {entity['word']:25s} -> {entity['entity_group']} ({entity['score']:.3f})")


def demo_fill_mask():
    section("5. Fill-mask (masked language modeling)")
    fill = pipeline("fill-mask")
    sentence = f"This course is teaching me about {fill.tokenizer.mask_token}."
    for guess in fill(sentence, top_k=3):
        print(f"  {guess['token_str']:15s} ({guess['score']:.3f})")


def main():
    demo_sentiment()
    demo_zero_shot()
    demo_text_generation()
    demo_ner()
    demo_fill_mask()
    print("\nFive tasks, one API. On to Chapter 2.")


if __name__ == "__main__":
    main()
