# Unit 1 — Introduction to Agents

The conceptual foundation for the whole course. By the end you should be able to (a) define an agent in one sentence, (b) explain the Thought–Action–Observation loop, (c) build a working tool-using agent in under 20 lines.

**Course link:** [Unit 1 on the HF docs](https://huggingface.co/learn/agents-course/unit1/introduction)

> **🎓 Certificate checkpoint:** finish this unit's quiz to earn the free **Fundamentals Certificate**. If you only have a week, do this and stop — it's a real credential.

## What you'll learn

- **What is an agent?** An LLM in a loop, given the ability to call tools.
- **LLMs recap** — chat templates, special tokens, messages. (If you came from Project 12, this will feel familiar.)
- **Tools** — plain Python functions exposed to the LLM via descriptions.
- **The Thought–Action–Observation cycle (ReAct)** — the loop every modern agent runs.
- **smolagents** — Hugging Face's own agent framework. Small, code-first, friendly.

## What's in this folder

- [`solution.py`](solution.py) — builds a smolagents `CodeAgent` with two tools (weather + calculator) and runs it. Three demos: tool definition, agent construction (offline), and a live agent run (if you have a token).
- [`requirements.txt`](requirements.txt) — `smolagents` + `huggingface_hub`.

## Setup

```bash
pip install -r requirements.txt
huggingface-cli login   # for the live demo (free Inference API)
```

## Run it

```bash
python3 solution.py
```

Expected: three demos. Tool inspection (offline), agent construction (offline), and — if logged in — a live agent run that calls both tools and stitches the answer together.

## Key concepts

### What an agent IS
Concretely: an `LLM + tools + a loop`. The pseudocode fits on one screen:

```
state = []
while not done:
    thought = llm(prompt + state + tool_descriptions)
    action = parse_tool_call(thought)
    observation = run_tool(action)
    state.append(thought, action, observation)
return final_answer(state)
```

That's the whole magic trick. Frameworks decorate this loop with conveniences (prompt templates, error handling, multi-agent handoffs), but the loop is the loop.

### Tools
Plain Python functions you decorate with `@tool`. The framework introspects the signature and docstring to build the LLM's "menu" of available actions:

```python
from smolagents import tool

@tool
def get_weather(city: str) -> str:
    """Returns the current weather for a city.

    Args:
        city: The city name, e.g. "Paris".
    """
    return ...
```

The docstring is the prompt. Spend time on it.

### Thought → Action → Observation (ReAct)
Asking the LLM to **write down its reasoning** before each action. Costs a few tokens; gains massive accuracy + debuggability. Almost every modern agent uses this pattern.

```
Thought: I need to know the weather. I'll call get_weather.
Action: get_weather("Paris")
Observation: sunny, 22°C
Thought: Now I have what I need.
```

### smolagents `CodeAgent`
smolagents' signature feature: instead of emitting a JSON tool call, the LLM writes **Python code** that calls the tools. This is more flexible (loops, conditionals, multi-step in one block) and tends to be more accurate. The framework runs the code in a sandbox.

## Mini-tasks

1. Run `solution.py` — get all three demos working.
2. Add a third tool (e.g., `lookup_stock_price(ticker)` returning hardcoded data). Re-run with a question that needs all three.
3. Take Unit 1's quiz on the HF site. Earn the Fundamentals Certificate.

## Focus vs skim

- **Focus:** "What is an Agent?", "What are Tools?", "Thought–Action–Observation Cycle", and the smolagents tutorial at the end. The tutorial is the spine of the unit.
- **Skim:** "Dummy Agent Library" — useful for intuition (the loop without an LLM), but don't dwell.

## Common pitfalls

- **Bad tool descriptions** — the docstring is what the LLM sees. "Gets weather" is worse than "Returns the current weather for a city. Args: city: e.g. 'Paris', 'Tokyo'."
- **Forgetting `max_steps`** — without it, a confused agent can loop forever.
- **Treating the agent like a chatbot** — agents *do things*. If your code has no loop and no tools, it's not an agent.

## Expected outcome

You can build a working tool-using agent from scratch in under 20 lines. You understand that the *loop* (not the model) is what makes it an agent. You've earned the Fundamentals Certificate.

## Next

→ [Unit 2.1 — The smolagents framework](../unit-02a-smolagents/)
