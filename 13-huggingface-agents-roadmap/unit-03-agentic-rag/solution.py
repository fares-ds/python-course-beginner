# Unit 3 — agentic RAG over a tiny guest database.
#
# The agent has one tool: search_guests. It decides when to call it,
# what query to pass, and whether one retrieval is enough.

import json
import os
from pathlib import Path

from smolagents import CodeAgent, HfApiModel, tool

DEMO_MODEL = "Qwen/Qwen2.5-Coder-32B-Instruct"
GUESTS = json.loads((Path(__file__).parent / "guests.json").read_text())


@tool
def search_guests(query: str) -> str:
    """Searches the guest database. Returns matching guests as a formatted string.

    Args:
        query: A natural-language search query. Examples: "guests who work at Google",
               "Jane Smith", "guests who studied at Stanford".
    """
    q = query.lower()
    matches = [
        g for g in GUESTS
        if (q in g["name"].lower()
            or q in g["bio"].lower()
            or any(q in keyword.lower() for keyword in g["keywords"]))
    ]
    if not matches:
        return f"No guests matched '{query}'."
    lines = [f"Found {len(matches)} matching guest(s):"]
    for g in matches:
        lines.append(f"- {g['name']}: {g['bio']}")
    return "\n".join(lines)


def main():
    if not (os.getenv("HF_TOKEN") or os.getenv("HUGGINGFACE_HUB_TOKEN")):
        raise SystemExit("Need a HF token. Run: huggingface-cli login")

    model = HfApiModel(DEMO_MODEL)
    agent = CodeAgent(tools=[search_guests], model=model, max_steps=6)

    questions = [
        "Who is Jane Smith?",
        "Tell me about all guests who studied at Stanford, "
        "and write me a one-line intro for each.",
    ]
    for q in questions:
        print(f"\n{'=' * 60}\nQ: {q}\n{'=' * 60}")
        try:
            answer = agent.run(q)
            print(f"\nA: {answer}")
        except Exception as e:
            print(f"\nFailed: {e}")


if __name__ == "__main__":
    main()
