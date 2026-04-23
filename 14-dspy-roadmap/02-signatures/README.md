# 02 — Signatures

The typed "contract" between you and the LM. A signature says what goes in and what should come out; DSPy turns that into a prompt for you.

**Docs link:** [Signatures](https://dspy.ai/learn/programming/signatures/)

## What you'll learn

- **Inline signatures**: `"question -> answer"` — the one-liner style.
- **Class signatures**: subclass `dspy.Signature` with docstring, `InputField`, `OutputField`. More expressive, re-usable.
- **Types** in signatures — use Python type hints to coerce outputs (`int`, `float`, `list[str]`, Pydantic models).
- **Multi-output signatures** — one call, several named outputs.

## What's in this folder

- [`solution.py`](solution.py) — three styles side by side: inline string, class with type hints, multi-output.
- [`requirements.txt`](requirements.txt) — `dspy>=3.0,<4.0`.

## Setup

```bash
pip install -r requirements.txt
ollama pull qwen2.5-coder:7b   # if you haven't yet
```

## Run it

```bash
python3 solution.py
```

Expected: three demos showing the same rough task (classify a sentence) with three signature styles, so you can see how the prompt changes with each.

## Key concepts

### Inline signatures
```python
classify = dspy.Predict("sentence -> label")
```
Fastest to type. Fine for prototyping. Get the string syntax right: fields comma-separated, `->` between inputs and outputs, optional type annotations (`"sentence -> label: str"`).

### Class signatures
```python
class Classify(dspy.Signature):
    """Classify the sentiment of a sentence as positive, neutral, or negative."""
    sentence: str = dspy.InputField(desc="the sentence to classify")
    label: str = dspy.OutputField(desc="one of: positive, neutral, negative")

classify = dspy.Predict(Classify)
```
More verbose, but:
- The **class docstring** becomes the task description in the prompt.
- `desc=` adds hints for each field.
- You get auto-completion and type-checking in your editor.
- You can reuse the class across multiple Modules.

### Types
DSPy parses the LM's output into the types you declared.

```python
class ExtractNumbers(dspy.Signature):
    text: str = dspy.InputField()
    numbers: list[int] = dspy.OutputField()
```

It'll try to parse the output as a list of ints. If the LM returned a messy string, DSPy's adapter will retry with a corrective reprompt.

Pydantic models also work, which is how you get structured JSON output without writing JSON-schema by hand.

### Multi-output signatures
```python
class AnalyzeReview(dspy.Signature):
    review: str = dspy.InputField()
    sentiment: str = dspy.OutputField()
    topics: list[str] = dspy.OutputField()
    summary: str = dspy.OutputField()
```

One LM call produces all three fields. Much cheaper than three separate calls.

## Mini-tasks

1. Run `solution.py`. Compare the outputs of the three styles on the same input.
2. Write a class signature that extracts (name, email, phone) from a sentence like "Contact Jane at jane@corp.com or 555-1234." Use `list[dict]` or a Pydantic model for the output.
3. Add `confidence: float = dspy.OutputField()` to any of the class signatures. Run it. Is the model's confidence well-calibrated?

## Common pitfalls

- **Forgetting the docstring in class signatures** — the docstring IS the task description. Without it, the model guesses what you want.
- **Types that are too strict** — `int` fails if the model says "forty-two"; `str` is more forgiving. Tighten types only when you've tested that the LM can produce them.
- **Overloaded output fields** — "summary: str" + "key_points: list[str]" + "tone: str" all in one call can confuse smaller models. Break into two Modules if accuracy matters.

## Expected outcome

You can read any DSPy signature and predict its prompt shape. You know when to reach for a class signature vs an inline one.

## Next

→ [03 — Modules (Predict, ChainOfThought)](../03-modules-basics/)
