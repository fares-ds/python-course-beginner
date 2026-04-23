# 11 — compile the Q&A program with GEPA (reflective prompt evolution).

import json
import random
from pathlib import Path

import dspy

lm = dspy.LM("ollama_chat/qwen2.5-coder:7b", api_base="http://localhost:11434")
dspy.configure(lm=lm)

QA_PATH = Path(__file__).parent.parent / "07-data-and-examples" / "data" / "qa_examples.json"


def metric(gold, pred, trace=None) -> float:
    return float(str(gold.answer).strip().lower() in str(pred.answer).strip().lower())


def main():
    examples = [
        dspy.Example(**row).with_inputs("question")
        for row in json.loads(QA_PATH.read_text())
    ]
    rng = random.Random(42)
    rng.shuffle(examples)
    n = len(examples)
    train = examples[: int(0.5 * n)]
    dev = examples[int(0.5 * n) :]
    print(f"train={len(train)}  dev={len(dev)}")

    program = dspy.ChainOfThought("question -> answer")

    evaluator = dspy.Evaluate(devset=dev, metric=metric, num_threads=1, display_progress=True)
    print("\n--- BASELINE ---")
    print(f"baseline = {evaluator(program)}")

    print("\n--- COMPILING with GEPA(auto='light') ---")
    print("GEPA reflects on failed examples and proposes improved prompts.\n")

    # GEPA needs the same LM for reflection (or a separate, stronger reflection_lm).
    # Default uses the configured LM for both, which is fine here.
    optimizer = dspy.GEPA(
        metric=metric,
        auto="light",
        reflection_lm=lm,
    )
    compiled = optimizer.compile(student=program, trainset=train, valset=dev)

    print("\n--- AFTER ---")
    print(f"compiled = {evaluator(compiled)}")

    print("\nGEPA's chosen instruction(s):")
    for name, sub_module in compiled.named_predictors():
        print(f"  [{name}] {sub_module.signature.instructions}")


if __name__ == "__main__":
    main()
