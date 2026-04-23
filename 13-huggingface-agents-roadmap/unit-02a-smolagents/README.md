# Unit 2.1 — The smolagents framework

The most-used part of the course. By the end you'll know smolagents well enough to build any single-agent workflow in 50 lines, plus a 2-agent workflow when one isn't enough.

**Course link:** [Unit 2.1 on the HF docs](https://huggingface.co/learn/agents-course/unit2/smolagents/introduction)

## What you'll learn

- **`CodeAgent` vs `ToolCallingAgent`** — code-emitting vs JSON-emitting agents.
- Built-in tools: web search (`DuckDuckGoSearchTool`), Python interpreter (`PythonInterpreterTool`), image generation.
- Writing your own tools well — type hints, docstrings, return value design.
- **Multi-agent systems** — manager agents that delegate to specialists.
- Vision and browser agents (skim on first pass).

## What's in this folder

- [`solution.py`](solution.py) — a 2-agent system: a "researcher" agent does web search; a "writer" agent summarizes the research into 3 bullet points. Manager dispatches.
- [`requirements.txt`](requirements.txt) — `smolagents` with the search extra.

## Setup

```bash
pip install -r requirements.txt
huggingface-cli login
```

## Run it

```bash
python3 solution.py
```

Expected: the script asks "give me a 3-bullet summary of recent news on \<topic\>". The manager calls the researcher, which calls DuckDuckGo. The writer takes the research and produces bullets. ~30–60 seconds total.

## Key concepts

### `CodeAgent` vs `ToolCallingAgent`

|  | CodeAgent | ToolCallingAgent |
|---|---|---|
| **Output** | Python code | JSON tool call |
| **Strength** | Composes multiple tools per step; handles loops/conditionals | Universally supported by every model |
| **Risk** | Code execution (sandboxed by smolagents) | Less expressive |
| **Use when** | The model can write decent Python (most modern code-tuned models) | You need maximum portability across models |

When in doubt, start with `CodeAgent`. Switch to `ToolCallingAgent` if your model can't write reliable code.

### Built-in tools

```python
from smolagents import DuckDuckGoSearchTool, PythonInterpreterTool

agent = CodeAgent(
    tools=[DuckDuckGoSearchTool(), PythonInterpreterTool(), my_custom_tool],
    model=model,
)
```

Don't reinvent these. The web search tool alone unlocks most "the model needs current info" problems.

### Multi-agent systems

```python
researcher = CodeAgent(tools=[DuckDuckGoSearchTool()], model=model, name="researcher",
                       description="Searches the web for facts.")
writer = CodeAgent(tools=[], model=model, name="writer",
                   description="Writes concise summaries.")
manager = CodeAgent(tools=[], model=model, managed_agents=[researcher, writer])
```

The manager sees the specialists as "tools" it can call. Each specialist has its own state, its own loop, its own tools.

When to use multi-agent: when the *prompts* for two parts of your task are very different. A researcher prompt rewards thoroughness; a writer prompt rewards brevity. Two agents = two prompt-shaped roles.

### `max_steps`
Always set it. The default is generous; a confused agent can burn money in a loop.

```python
agent = CodeAgent(tools=[...], model=model, max_steps=6)
```

## Mini-tasks

1. Add the `DuckDuckGoSearchTool` to a single-agent CodeAgent. Ask "What was today's biggest news?" — the model should search and synthesize.
2. Build the 2-agent system in `solution.py`. Read its trace closely (smolagents prints the full Thought–Action–Observation chain by default). Notice how the manager talks to the specialists.
3. Read the smolagents source for `CodeAgent.run` (it's ~200 lines). Map the code back to the ReAct cycle. The "aha" is realizing the framework is small.

## Focus vs skim

- **Focus:** "Building Agents That Use Code", "Tools", "Multi-Agent Systems".
- **Skim:** "Vision and Browser agents" on first pass — fascinating, come back when you have a use case.

## Common pitfalls

- **Bad tool descriptions** — see Unit 1's pitfall #1. It's the same for every framework.
- **Multi-agent when single would do** — adds complexity, slowness, cost. Use when the prompts genuinely diverge, not by default.
- **Forgetting `max_steps`** — the default is forgiving; a real bug isn't.
- **Not reading the agent's trace** — smolagents prints it. Read it. You can't debug what you don't read.

## Expected outcome

You can build any tool-using or multi-agent workflow in smolagents in under 50 lines. You read agent traces fluently.

## Next

→ [Unit 2.2 — The LlamaIndex framework](../unit-02b-llamaindex/)
