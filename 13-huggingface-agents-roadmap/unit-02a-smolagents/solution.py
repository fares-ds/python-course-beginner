# Unit 2.1 — a 2-agent system: researcher + writer.
#
# The researcher does web search (with DuckDuckGo). The writer takes the
# research and produces a 3-bullet summary. A manager agent dispatches.
#
# Needs: huggingface-cli login (free Inference API).

import os

from smolagents import CodeAgent, DuckDuckGoSearchTool, HfApiModel

DEMO_MODEL = "Qwen/Qwen2.5-Coder-32B-Instruct"


def main():
    if not (os.getenv("HF_TOKEN") or os.getenv("HUGGINGFACE_HUB_TOKEN")):
        raise SystemExit("Need a HF token. Run: huggingface-cli login")

    model = HfApiModel(DEMO_MODEL)

    # SPECIALIST 1: researcher. Has web search; thorough by design.
    researcher = CodeAgent(
        tools=[DuckDuckGoSearchTool()],
        model=model,
        name="researcher",
        description="Searches the web and returns relevant facts and quotes about a topic. Use when current information is needed.",
        max_steps=4,
    )

    # SPECIALIST 2: writer. No tools; just synthesizes.
    writer = CodeAgent(
        tools=[],
        model=model,
        name="writer",
        description="Takes raw research notes and produces a polished 3-bullet summary. Each bullet is one short sentence.",
        max_steps=2,
    )

    # MANAGER: dispatches to specialists. Sees them as callable tools.
    manager = CodeAgent(
        tools=[],
        model=model,
        managed_agents=[researcher, writer],
        max_steps=6,
    )

    topic = "the latest news about renewable energy"
    print(f"Topic: {topic}\n")
    print("Running... (this calls the LLM multiple times, may take 30-90s)\n")
    answer = manager.run(
        f"Give me a 3-bullet summary of {topic}. "
        f"Use the researcher to gather facts, then the writer to format the bullets."
    )
    print("\n" + "=" * 60)
    print("FINAL ANSWER")
    print("=" * 60)
    print(answer)


if __name__ == "__main__":
    main()
