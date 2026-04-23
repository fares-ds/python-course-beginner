# Bonus 2 — agent + tracing + eval set.
#
# Runs a smolagents agent on a small eval set, traces every step,
# and prints a pass/fail summary.
#
# To send traces to Phoenix: pip install arize-phoenix, then `phoenix serve`
# in another terminal, then uncomment the Phoenix block below.

import json
import os
from pathlib import Path

from openinference.instrumentation.smolagents import SmolagentsInstrumentor
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
)
from smolagents import CodeAgent, HfApiModel, tool

DEMO_MODEL = "Qwen/Qwen2.5-Coder-32B-Instruct"
EVAL_SET = json.loads((Path(__file__).parent / "eval_set.json").read_text())


@tool
def add_numbers(a: float, b: float) -> float:
    """Adds two numbers and returns the sum.

    Args:
        a: First number.
        b: Second number.
    """
    return a + b


@tool
def capital_of(country: str) -> str:
    """Returns the capital of a country.

    Args:
        country: The country name, e.g. "France".
    """
    capitals = {
        "france": "Paris",
        "germany": "Berlin",
        "japan": "Tokyo",
        "australia": "Canberra",
        "brazil": "Brasilia",
    }
    return capitals.get(country.lower(), f"unknown country: {country}")


def setup_tracing():
    """Console exporter — replace with Phoenix/Langfuse for visual UIs."""
    provider = TracerProvider()
    provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
    trace.set_tracer_provider(provider)
    SmolagentsInstrumentor().instrument(tracer_provider=provider)

    # To use Phoenix instead, install arize-phoenix and uncomment:
    # from phoenix.otel import register
    # register(project_name="agent-eval")


def main():
    if not (os.getenv("HF_TOKEN") or os.getenv("HUGGINGFACE_HUB_TOKEN")):
        raise SystemExit("Need a HF token. Run: huggingface-cli login")

    setup_tracing()

    model = HfApiModel(DEMO_MODEL)
    agent = CodeAgent(tools=[add_numbers, capital_of], model=model, max_steps=4)

    results = []
    for case in EVAL_SET:
        print(f"\n--- Case: {case['input']!r}")
        try:
            answer = agent.run(case["input"])
            ans_str = str(answer)
            passed = case["expected"].lower() in ans_str.lower()
            results.append((case, ans_str, passed))
            print(f"    answer: {ans_str}")
            print(f"    expected substring: {case['expected']}  ->  {'PASS' if passed else 'FAIL'}")
        except Exception as e:
            results.append((case, f"ERROR: {e}", False))
            print(f"    ERROR: {e}")

    # Summary.
    passed = sum(1 for _, _, ok in results if ok)
    print(f"\n{'=' * 60}")
    print(f"EVAL: {passed}/{len(results)} passed")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
