# 14 — local debugging with dspy.inspect_history.

import dspy

lm = dspy.LM("ollama_chat/qwen2.5-coder:7b", api_base="http://localhost:11434")
dspy.configure(lm=lm)


def main():
    program = dspy.ChainOfThought("question -> answer")
    questions = [
        "What's the capital of France?",
        "Who painted the Mona Lisa?",
    ]
    for q in questions:
        result = program(question=q)
        print(f"Q: {q}")
        print(f"A: {result.answer}\n")

    print("=" * 60)
    print("Last 2 LLM exchanges (prompt + response):")
    print("=" * 60)
    dspy.inspect_history(n=2)


if __name__ == "__main__":
    main()
