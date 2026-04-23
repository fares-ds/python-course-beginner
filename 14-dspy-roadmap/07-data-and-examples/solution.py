# 07 — load Q&A examples, wrap as dspy.Example, split into train/dev/test.

import json
import random
from pathlib import Path

import dspy

RAW = json.loads((Path(__file__).parent / "data" / "qa_examples.json").read_text())


def main():
    # 1. Build dspy.Example objects.
    examples = [dspy.Example(**row) for row in RAW]
    print(f"Loaded {len(examples)} raw examples.")
    print(f"  First example: {examples[0]}\n")

    # 2. Mark inputs. Everything NOT named in with_inputs is treated as a label.
    examples = [ex.with_inputs("question") for ex in examples]
    print(f"  After .with_inputs('question'):")
    print(f"  inputs:  {dict(examples[0].inputs())}")
    print(f"  labels:  {dict(examples[0].labels())}")

    # 3. Shuffle deterministically and split 60/20/20.
    rng = random.Random(42)
    rng.shuffle(examples)
    n = len(examples)
    train = examples[: int(0.6 * n)]
    dev = examples[int(0.6 * n) : int(0.8 * n)]
    test = examples[int(0.8 * n) :]

    print(f"\nSplits:")
    print(f"  train: {len(train)}")
    print(f"  dev:   {len(dev)}")
    print(f"  test:  {len(test)}")
    print(f"\nFirst training example's question: {train[0].question}")
    print(f"First dev example's question:      {dev[0].question}")


if __name__ == "__main__":
    main()
