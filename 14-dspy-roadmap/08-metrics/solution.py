# 08 — three different metrics on the same predictions.

import json
from pathlib import Path

import dspy

lm = dspy.LM("ollama_chat/qwen2.5-coder:7b", api_base="http://localhost:11434")
dspy.configure(lm=lm)

# Reuse the Q&A set from folder 07.
QA_PATH = Path(__file__).parent.parent / "07-data-and-examples" / "data" / "qa_examples.json"
EXAMPLES = [
    dspy.Example(**row).with_inputs("question")
    for row in json.loads(QA_PATH.read_text())
][:6]   # small slice — keep the demo fast


def exact_match(gold, pred, trace=None) -> float:
    return float(str(pred.answer).strip().lower() == str(gold.answer).strip().lower())


def case_insensitive_contains(gold, pred, trace=None) -> float:
    """Partial credit: the gold answer appears anywhere in the prediction."""
    return float(str(gold.answer).strip().lower() in str(pred.answer).strip().lower())


class JudgeAnswer(dspy.Signature):
    """Score how well the predicted answer addresses the question, given the gold answer."""

    question: str = dspy.InputField()
    gold_answer: str = dspy.InputField()
    predicted_answer: str = dspy.InputField()
    score: float = dspy.OutputField(desc="from 0.0 (totally wrong) to 1.0 (correct)")


_judge = dspy.Predict(JudgeAnswer)


def lm_as_judge(gold, pred, trace=None) -> float:
    out = _judge(
        question=gold.question,
        gold_answer=str(gold.answer),
        predicted_answer=str(pred.answer),
    )
    try:
        return float(out.score)
    except (ValueError, TypeError):
        return 0.0


def main():
    program = dspy.Predict("question -> answer")

    print(f"Running on {len(EXAMPLES)} examples (one LM call each).\n")
    predictions = [(ex, program(question=ex.question)) for ex in EXAMPLES]

    metrics = {
        "exact_match": exact_match,
        "contains":    case_insensitive_contains,
        "lm_judge":    lm_as_judge,
    }

    print(f"{'Question':<55} | {'gold':<20} | {'pred':<20} | EM | CONT | JUDGE")
    print("-" * 120)
    totals = {name: 0.0 for name in metrics}
    for ex, pred in predictions:
        scores = {name: m(ex, pred) for name, m in metrics.items()}
        for k, v in scores.items():
            totals[k] += v
        print(
            f"{ex.question[:52]:<55} | {str(ex.answer)[:18]:<20} | "
            f"{str(pred.answer)[:18]:<20} | "
            f"{scores['exact_match']:.1f} | {scores['contains']:.1f} | {scores['lm_judge']:.2f}"
        )

    print("-" * 120)
    n = len(predictions)
    for name, total in totals.items():
        print(f"  {name:<12s} mean: {total / n:.3f}")
    print("\nNotice the three metrics often disagree. They each measure different things.")


if __name__ == "__main__":
    main()
