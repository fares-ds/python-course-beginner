# 04 — same arithmetic question, four modules, four strategies.

import dspy

lm = dspy.LM("ollama_chat/qwen2.5-coder:7b", api_base="http://localhost:11434")
dspy.configure(lm=lm)

QUESTION = (
    "If a train leaves the station at 9:15 AM and arrives at 11:47 AM, "
    "and the station is 134 km away, what is the train's average speed in km/h? "
    "Round to one decimal place."
)


def calculator(expression: str) -> str:
    """Evaluates a Python math expression and returns the result.

    Args:
        expression: A Python arithmetic expression, e.g. '17 * 23' or '134 / 2.5333'.
    """
    # Tiny safe-eval: no builtins, no name lookups. Production should use
    # asteval, numexpr, or dspy's PythonInterpreter for real safety.
    return str(eval(expression, {"__builtins__": {}}))


def section(title):
    print()
    print("=" * 60)
    print(title)
    print("=" * 60)


def main():
    print(f"Question: {QUESTION}\n")

    section("1. Predict — just ask")
    p = dspy.Predict("question -> answer")
    print(f"  {p(question=QUESTION).answer}")

    section("2. ChainOfThought — think step by step in text")
    cot = dspy.ChainOfThought("question -> answer")
    out = cot(question=QUESTION)
    print(f"  reasoning: {out.reasoning[:200]}...")
    print(f"  answer:    {out.answer}")

    section("3. ReAct — agent with a calculator tool")
    agent = dspy.ReAct("question -> answer", tools=[calculator], max_iters=4)
    print(f"  {agent(question=QUESTION).answer}")

    section("4. ProgramOfThought — write Python, execute it")
    pot = dspy.ProgramOfThought("question -> answer")
    print(f"  {pot(question=QUESTION).answer}")

    print("\nNotice: PoT and ReAct (which has a calculator) usually both")
    print("get it right. Predict often gets it wrong. CoT depends on")
    print("whether the model's mental arithmetic holds up.")


if __name__ == "__main__":
    main()
