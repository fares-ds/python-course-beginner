# 03 — Predict vs ChainOfThought on the same task.

import dspy

lm = dspy.LM("ollama_chat/qwen2.5-coder:7b", api_base="http://localhost:11434")
dspy.configure(lm=lm)

# A small multi-step arithmetic question. Not trivial for a 7B model.
QUESTION = (
    "A bookstore has 3 shelves with 7 books each, and 2 shelves with 5 books each. "
    "It sells 12 books. How many books are left?"
)


def demo_predict():
    print("=" * 60)
    print("1. dspy.Predict — direct answer")
    print("=" * 60)
    predict = dspy.Predict("question -> answer")
    result = predict(question=QUESTION)
    print(f"  answer = {result.answer}")


def demo_cot():
    print()
    print("=" * 60)
    print("2. dspy.ChainOfThought — asks LM to reason first")
    print("=" * 60)
    cot = dspy.ChainOfThought("question -> answer")
    result = cot(question=QUESTION)
    print(f"  reasoning = {result.reasoning}")
    print(f"  answer    = {result.answer}")


def demo_inspect_history():
    print()
    print("=" * 60)
    print("3. dspy.inspect_history(n=1) — see what was actually sent/received")
    print("=" * 60)
    # Shows the last prompt + response. The #1 debugging tool in DSPy.
    dspy.inspect_history(n=1)


def main():
    demo_predict()
    demo_cot()
    demo_inspect_history()


if __name__ == "__main__":
    main()
