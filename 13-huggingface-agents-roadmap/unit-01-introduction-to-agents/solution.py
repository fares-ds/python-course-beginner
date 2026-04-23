# Unit 1 — your first smolagents agent.
#
# Three demos:
#   1. Define two @tool functions and inspect their schemas.
#   2. Construct a CodeAgent (offline — no LLM call).
#   3. (If HF_TOKEN is set) actually run the agent on a real question.

import os

from smolagents import CodeAgent, HfApiModel, tool

DEMO_MODEL = "Qwen/Qwen2.5-Coder-32B-Instruct"


@tool
def get_weather(city: str) -> str:
    """Returns the current weather for a city.

    Args:
        city: The city name, e.g. "Paris" or "Tokyo".
    """
    fake = {
        "paris": "sunny, 22°C",
        "tokyo": "rainy, 18°C",
        "berlin": "cloudy, 15°C",
    }
    return fake.get(city.lower(), f"no weather data for {city}")


@tool
def add_numbers(a: float, b: float) -> float:
    """Adds two numbers and returns the sum.

    Args:
        a: First number.
        b: Second number.
    """
    return a + b


def section(title):
    print()
    print("=" * 60)
    print(title)
    print("=" * 60)


def demo_tools():
    section("DEMO 1: tools defined")
    for t in (get_weather, add_numbers):
        print(f"  - {t.name}: {t.description.splitlines()[0]}")
        print(f"    inputs: {list(t.inputs.keys())}")


def demo_construction():
    section("DEMO 2: agent constructed (offline)")
    model = HfApiModel(DEMO_MODEL)
    agent = CodeAgent(tools=[get_weather, add_numbers], model=model, max_steps=4)
    print(f"  {type(agent).__name__} with {len(agent.tools)} tools:")
    for name in agent.tools:
        print(f"    - {name}")


def demo_live_run():
    section("DEMO 3: live run (needs HF_TOKEN)")
    if not (os.getenv("HF_TOKEN") or os.getenv("HUGGINGFACE_HUB_TOKEN")):
        print("  Skipped — no HF token. Run: huggingface-cli login")
        return

    model = HfApiModel(DEMO_MODEL)
    agent = CodeAgent(tools=[get_weather, add_numbers], model=model, max_steps=4)
    question = "What's the weather in Paris and what's 17 plus 25?"
    print(f"  Q: {question}\n")
    try:
        answer = agent.run(question)
        print(f"\n  A: {answer}")
    except Exception as e:
        print(f"\n  Run failed: {e}")
        print("  Usually a token, rate-limit, or network issue.")


def main():
    demo_tools()
    demo_construction()
    demo_live_run()
    print("\nUnit 1 done. Take the quiz on the HF site for the certificate.")


if __name__ == "__main__":
    main()
