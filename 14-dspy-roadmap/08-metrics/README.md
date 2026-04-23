# 08 — Metrics

A metric is a function `(gold_example, prediction) -> score`. It's how every optimizer in folders 09–12 knows whether your program is getting better.

**Docs link:** [Metrics](https://dspy.ai/learn/evaluation/metrics/)

## What you'll learn

- The metric signature: `def metric(example, pred, trace=None) -> float | bool`.
- **Built-in metrics**: `dspy.evaluate.answer_exact_match`, `dspy.evaluate.answer_passage_match`, `dspy.SemanticF1`.
- **Custom metrics** — when "exact match" is too strict and "is this answer good?" is too vague.
- **LM-as-judge** — your toughest cases: ask another LLM to grade.

## What's in this folder

- [`solution.py`](solution.py) — runs the same Q&A program through three different metrics on the same dev set: exact match, semantic F1, and an LM-as-judge.
- [`requirements.txt`](requirements.txt) — `dspy>=3.0,<4.0`.

## Setup

```bash
pip install -r requirements.txt
```

## Run it

```bash
python3 solution.py
```

Expected: three scores on the same predictions. Notice they don't agree — exact match is harshest; semantic F1 is more forgiving; LM-as-judge sits somewhere in the middle (and varies between runs).

## Key concepts

### The metric signature
```python
def my_metric(gold, pred, trace=None) -> float:
    # gold: dspy.Example with the labels
    # pred: dspy.Prediction from your program
    # trace: optional execution trace (only used by some optimizers)
    return float(gold.answer.lower() == pred.answer.lower())
```

A metric returns a number. Higher = better. (Most return 0/1 for booleans; some return continuous like F1.) The third arg `trace` is only used by some advanced optimizers — usually you can ignore it.

### Built-ins
- **`answer_exact_match`** — `pred.answer == gold.answer`. Strict.
- **`answer_passage_match`** — `gold.answer in retrieved_passage`. Useful for RAG to check the right passage was found.
- **`SemanticF1`** — token-overlap F1 with normalization. More forgiving than exact match.

### Custom metrics
Most projects need one. Examples:

```python
def case_insensitive_contains(gold, pred, trace=None):
    return float(gold.answer.lower() in pred.answer.lower())
```

```python
def is_valid_json(gold, pred, trace=None):
    try:
        json.loads(pred.answer)
        return 1.0
    except json.JSONDecodeError:
        return 0.0
```

Three lines. Often that's all you need.

### LM-as-judge
For open-ended outputs (summaries, generated code, free-form answers), no string-matching metric works. Ask an LLM to grade:

```python
class JudgeAnswer(dspy.Signature):
    """Score how well the predicted answer addresses the question, given the gold answer."""
    question: str = dspy.InputField()
    gold_answer: str = dspy.InputField()
    predicted_answer: str = dspy.InputField()
    score: float = dspy.OutputField(desc="0.0 to 1.0")

judge = dspy.Predict(JudgeAnswer)
def lm_judge(gold, pred, trace=None):
    return judge(question=gold.question, gold_answer=gold.answer,
                 predicted_answer=pred.answer).score
```

Costs an LLM call per example. Worth it for tasks where humans wouldn't agree on string-match either.

## Mini-tasks

1. Run `solution.py`. Notice how the three metrics disagree. Which is "right"? Trick question — they each measure different things.
2. Write a custom metric that scores partial credit (e.g., 1.0 if exact, 0.5 if the gold answer is a substring of the prediction, 0.0 otherwise).
3. Try LM-as-judge on a creative-writing task (a Predict that "writes a haiku about X"). String-match obviously fails; the LM judge can give a sensible 0–1.

## Common pitfalls

- **Metric returns a bool when the optimizer wants a float** — wrap with `float(...)`.
- **LM-as-judge with the *same* model** — the judge will be biased toward the model's own style. Use a different/stronger model for the judge if you can.
- **Single-number metrics for multi-aspect tasks** — a summary can be "factually accurate AND too long." Either split into multiple metrics or weight them.

## Expected outcome

You can pick (or write) the right metric for any DSPy task. You understand why "good is hard to measure" is the hardest part of LLM eng.

## Next

→ [09 — Optimizer: BootstrapFewShot](../09-optimizer-bootstrap/)
