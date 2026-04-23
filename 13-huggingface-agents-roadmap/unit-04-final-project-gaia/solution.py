# Unit 4 — starter GAIA agent.
#
# A smolagents CodeAgent with web search + Python interpreter. Run it on
# a sample multi-step question. To submit to the real GAIA leaderboard,
# follow the official Unit 4 notebook on the HF site (it has the validation
# set + the submission code).

import os

from smolagents import CodeAgent, DuckDuckGoSearchTool, HfApiModel, PythonInterpreterTool

DEMO_MODEL = "Qwen/Qwen2.5-Coder-32B-Instruct"

# A sample GAIA-style question. Multi-step: needs lookup + arithmetic.
SAMPLE_QUESTION = (
    "How many Olympic gold medals did Usain Bolt win in his career? "
    "Multiply that number by the number of Summer Olympics held between 2000 and 2020. "
    "Return only the final number."
)


def main():
    if not (os.getenv("HF_TOKEN") or os.getenv("HUGGINGFACE_HUB_TOKEN")):
        raise SystemExit("Need a HF token. Run: huggingface-cli login")

    model = HfApiModel(DEMO_MODEL)
    agent = CodeAgent(
        tools=[DuckDuckGoSearchTool(), PythonInterpreterTool()],
        model=model,
        # max_steps generous because GAIA-style questions are multi-step.
        max_steps=10,
        # Add explicit guidance to the agent about its job.
        additional_authorized_imports=["json", "math", "statistics"],
    )

    print("=" * 60)
    print("Sample GAIA-style question")
    print("=" * 60)
    print(f"Q: {SAMPLE_QUESTION}\n")
    try:
        answer = agent.run(SAMPLE_QUESTION)
        print(f"\nFinal answer: {answer}")
    except Exception as e:
        print(f"\nFailed: {e}")
        print("(GAIA is hard. Read the trace, change one thing, try again.)")


if __name__ == "__main__":
    main()
