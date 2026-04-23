# 10 — compile the Q&A program with MIPROv2 (auto="light").
#
# Slower than folder 09 (BootstrapFewShot). Plan for ~10-30 min on Ollama
# with auto="light", longer for "medium".

import json
import random
from pathlib import Path

import dspy
from dspy.teleprompt import MIPROv2

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

    print("\n--- COMPILING with MIPROv2(auto='light') (~10-30 min on Ollama) ---")
    print("MIPROv2 will: (1) bootstrap demos, (2) propose alternate instructions,")
    print("(3) Bayesian-search over the combinations.\n")

    optimizer = MIPROv2(metric=metric, auto="light")
    compiled = optimizer.compile(
        student=program,
        trainset=train,
        # Cap the work so the demo finishes in a reasonable time.
        requires_permission_to_run=False,
    )

    print("\n--- AFTER ---")
    print(f"compiled = {evaluator(compiled)}")

    print("\nThe winning instruction MIPROv2 chose:")
    for name, sub_module in compiled.named_predictors():
        print(f"  [{name}] {sub_module.signature.instructions}")


if __name__ == "__main__":
    main()
