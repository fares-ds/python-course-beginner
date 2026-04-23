# 09 — compile a Q&A program with BootstrapFewShot. Measure before/after.

import json
import random
from pathlib import Path

import dspy
from dspy.teleprompt import BootstrapFewShot

lm = dspy.LM("ollama_chat/qwen2.5-coder:7b", api_base="http://localhost:11434")
dspy.configure(lm=lm)

QA_PATH = Path(__file__).parent.parent / "07-data-and-examples" / "data" / "qa_examples.json"


def metric(gold, pred, trace=None) -> float:
    """Case-insensitive substring match — forgiving but not trivial."""
    return float(str(gold.answer).strip().lower() in str(pred.answer).strip().lower())


def main():
    # Load + split.
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

    # The program we want to optimize.
    program = dspy.ChainOfThought("question -> answer")

    # Baseline: how good is it before optimization?
    evaluator = dspy.Evaluate(devset=dev, metric=metric, num_threads=1, display_progress=True)
    print("\n--- BASELINE ---")
    baseline = evaluator(program)
    print(f"baseline accuracy = {baseline}")

    # Compile with BootstrapFewShot. Picks up to max_bootstrapped_demos
    # successful train examples and bakes them into the prompt as few-shots.
    print("\n--- COMPILING with BootstrapFewShot (~1-3 min on Ollama) ---")
    optimizer = BootstrapFewShot(metric=metric, max_bootstrapped_demos=4)
    compiled = optimizer.compile(student=program, trainset=train)

    print("\n--- AFTER ---")
    after = evaluator(compiled)
    print(f"compiled accuracy = {after}")

    print("\nNotice DSPy added training-derived few-shots to the prompt. Inspect:")
    dspy.inspect_history(n=1)


if __name__ == "__main__":
    main()
