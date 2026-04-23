# 13 — save a compiled DSPy program, then load it back from a fresh process.

import json
import random
from pathlib import Path

import dspy
from dspy.teleprompt import BootstrapFewShot

lm = dspy.LM("ollama_chat/qwen2.5-coder:7b", api_base="http://localhost:11434")
dspy.configure(lm=lm)

QA_PATH = Path(__file__).parent.parent / "07-data-and-examples" / "data" / "qa_examples.json"
SAVE_PATH = Path(__file__).parent / "program.json"


def metric(gold, pred, trace=None) -> float:
    return float(str(gold.answer).strip().lower() in str(pred.answer).strip().lower())


def train_and_save():
    examples = [
        dspy.Example(**row).with_inputs("question")
        for row in json.loads(QA_PATH.read_text())
    ]
    rng = random.Random(42)
    rng.shuffle(examples)

    program = dspy.ChainOfThought("question -> answer")
    print("Compiling with BootstrapFewShot (~1-2 min on Ollama)...")
    optimizer = BootstrapFewShot(metric=metric, max_bootstrapped_demos=3)
    compiled = optimizer.compile(student=program, trainset=examples[:8])

    compiled.save(str(SAVE_PATH))
    print(f"Saved compiled program to {SAVE_PATH}")
    return compiled


def load_and_test():
    """Simulates loading from a fresh process — no in-memory state."""
    fresh = dspy.ChainOfThought("question -> answer")
    fresh.load(str(SAVE_PATH))
    print(f"\nLoaded from {SAVE_PATH}")
    result = fresh(question="Who wrote Hamlet?")
    print(f"  Q: Who wrote Hamlet?\n  A: {result.answer}")


def main():
    train_and_save()
    load_and_test()


if __name__ == "__main__":
    main()
