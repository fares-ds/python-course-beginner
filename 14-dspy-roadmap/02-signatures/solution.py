# 02 — three signature styles for the same task (classify a sentence).

import dspy

lm = dspy.LM("ollama_chat/qwen2.5-coder:7b", api_base="http://localhost:11434")
dspy.configure(lm=lm)

SENTENCE = "The movie had stunning visuals but the plot was boring."


def demo_inline():
    print("=" * 60)
    print("1. Inline signature")
    print("=" * 60)
    classify = dspy.Predict("sentence -> label")
    result = classify(sentence=SENTENCE)
    print(f"  label = {result.label!r}")


# Class-style signature. The docstring becomes the task description,
# desc= hints describe each field to the model.
class Classify(dspy.Signature):
    """Classify the sentiment of a sentence as positive, neutral, or negative."""

    sentence: str = dspy.InputField(desc="the sentence to classify")
    label: str = dspy.OutputField(desc="one of: positive, neutral, negative")


def demo_class():
    print()
    print("=" * 60)
    print("2. Class signature (with docstring + descriptions)")
    print("=" * 60)
    classify = dspy.Predict(Classify)
    result = classify(sentence=SENTENCE)
    print(f"  label = {result.label!r}")


class AnalyzeReview(dspy.Signature):
    """Analyze a product or movie review. Return multiple fields at once."""

    review: str = dspy.InputField()
    sentiment: str = dspy.OutputField(desc="positive | neutral | negative")
    topics: list[str] = dspy.OutputField(desc="1-4 topics mentioned in the review")
    summary: str = dspy.OutputField(desc="a 1-sentence summary")


def demo_multi_output():
    print()
    print("=" * 60)
    print("3. Multi-output signature (one call, three fields)")
    print("=" * 60)
    analyze = dspy.Predict(AnalyzeReview)
    result = analyze(review=SENTENCE)
    # DSPy parses each declared output type. `topics` comes back as a Python list.
    print(f"  sentiment = {result.sentiment!r}")
    print(f"  topics    = {result.topics}")
    print(f"  summary   = {result.summary!r}")


def main():
    demo_inline()
    demo_class()
    demo_multi_output()


if __name__ == "__main__":
    main()
