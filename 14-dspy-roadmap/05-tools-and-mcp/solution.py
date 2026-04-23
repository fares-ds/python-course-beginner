# 05 — three tools, one ReAct agent, a question that needs all of them.

import datetime as dt

import dspy

lm = dspy.LM("ollama_chat/qwen2.5-coder:7b", api_base="http://localhost:11434")
dspy.configure(lm=lm)


def calculator(expression: str) -> str:
    """Evaluates a Python arithmetic expression.

    Args:
        expression: A math expression, e.g. '17 * 23' or '(2024 - 1973) * 12'.
    """
    return str(eval(expression, {"__builtins__": {}}))


def fake_search(query: str) -> str:
    """Search a tiny in-memory facts database. Returns matching facts.

    Args:
        query: A natural-language query, e.g. 'who invented Python'.
    """
    facts = {
        "python": "Python was created by Guido van Rossum in 1991.",
        "linux": "Linux was created by Linus Torvalds in 1991.",
        "git": "Git was created by Linus Torvalds in 2005.",
        "transformer": "The Transformer architecture was introduced in 2017 in 'Attention Is All You Need'.",
    }
    q = query.lower()
    matches = [v for k, v in facts.items() if k in q]
    return matches[0] if matches else f"No facts found for '{query}'."


def current_year() -> int:
    """Returns the current year as an integer."""
    return dt.date.today().year


def main():
    agent = dspy.ReAct(
        "question -> answer",
        tools=[calculator, fake_search, current_year],
        max_iters=6,
    )

    question = (
        "How many years ago was Python created? Use the search tool to find "
        "the year, the current_year tool for today's year, and the calculator "
        "to compute the difference."
    )
    print(f"Question: {question}\n")
    result = agent(question=question)
    print(f"\nFinal answer: {result.answer}")

    print("\n--- Last LLM exchange ---")
    dspy.inspect_history(n=1)


if __name__ == "__main__":
    main()
