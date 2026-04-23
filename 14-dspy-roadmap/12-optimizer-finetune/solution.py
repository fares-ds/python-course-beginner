# 12 — BootstrapFinetune skeleton. Needs a finetune provider (Together AI default).
#
# Without TOGETHER_API_KEY, this script exits with a helpful message instead
# of crashing. Read the code below to understand the pattern even if you
# don't run it.

import json
import os
import random
from pathlib import Path

import dspy

QA_PATH = Path(__file__).parent.parent / "07-data-and-examples" / "data" / "qa_examples.json"


def metric(gold, pred, trace=None) -> float:
    return float(str(gold.answer).strip().lower() in str(pred.answer).strip().lower())


def main():
    if not os.getenv("TOGETHER_API_KEY"):
        print("BootstrapFinetune actually fine-tunes a model, which Ollama can't do.")
        print("To run for real, you need a finetuning provider:")
        print()
        print("  1. Sign up at https://together.ai (free tier is enough)")
        print("  2. pip install together")
        print("  3. export TOGETHER_API_KEY=...")
        print("  4. Re-run this script")
        print()
        print("For learning purposes, the rest of this folder's README explains the pattern.")
        print("If you want to stay in Ollama land, skip this folder and continue to 13.")
        return

    from dspy.teleprompt import BootstrapFinetune

    # Teacher: a strong model, used to generate training traces.
    teacher_lm = dspy.LM("openai/gpt-4o-mini")  # or any strong LM you have access to
    # Student: the smaller model we'll fine-tune.
    student_lm = dspy.LM("together_ai/meta-llama/Llama-3.2-1B-Instruct-Reference")

    # Configure DSPy to use the teacher initially. The optimizer will
    # eventually swap in a fine-tuned student.
    dspy.configure(lm=teacher_lm)

    examples = [
        dspy.Example(**row).with_inputs("question")
        for row in json.loads(QA_PATH.read_text())
    ]
    rng = random.Random(42)
    rng.shuffle(examples)

    program = dspy.ChainOfThought("question -> answer")

    optimizer = BootstrapFinetune(metric=metric)
    compiled = optimizer.compile(
        student=program,
        trainset=examples,
        target=student_lm,    # fine-tune target
    )

    print("Done. The compiled program now uses the fine-tuned student model.")
    print(f"Test: {compiled(question='Who painted the Mona Lisa?').answer}")


if __name__ == "__main__":
    main()
