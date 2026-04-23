# 04 — Modules: `ReAct` and `ProgramOfThought`

The agentic and code-generation modules. `ReAct` loops with tools (Thought → Action → Observation). `ProgramOfThought` writes Python and executes it instead of doing math in its head.

**Docs link:** [Modules](https://dspy.ai/learn/programming/modules/) (scroll to ReAct + ProgramOfThought sections)

## What you'll learn

- **`dspy.ReAct`** — DSPy's agent module. Same shape as smolagents/LangGraph agents you saw in Project 13.
- **`dspy.ProgramOfThought`** — when in doubt about math, ask the LM to *write code* and let DSPy execute it.
- **`dspy.Refine`** and **`dspy.BestOfN`** — meta-modules that retry/sample to improve quality.
- When to reach for which.

## What's in this folder

- [`solution.py`](solution.py) — runs the same multi-step problem through `Predict`, `ChainOfThought`, `ReAct` (with a calculator tool), and `ProgramOfThought`. Compare answers.

## Setup

```bash
pip install -r requirements.txt
```

## Run it

```bash
python3 solution.py
```

Expected: four answers to the same arithmetic-heavy problem. PoT and ReAct (with calculator) usually both nail it; Predict often misses; CoT lands somewhere in between.

## Key concepts

### `dspy.ReAct(signature, tools=[...])`
Wraps a signature with the Thought–Action–Observation loop. Tools are plain Python functions:

```python
def calculator(expression: str) -> str:
    """Evaluates a math expression and returns the result."""
    return str(eval(expression, {"__builtins__": {}}))

agent = dspy.ReAct("question -> answer", tools=[calculator])
```

The agent's loop is exactly the loop you saw in Project 13:

```
Thought: I need to compute 17 * 23
Action: calculator(expression="17 * 23")
Observation: 391
Thought: Now I have the answer.
```

### `dspy.ProgramOfThought("question -> answer")`
Asks the LM to write Python code that produces the answer, then executes it in a sandbox. For arithmetic, dates, list operations — anything where deterministic execution beats vibes — PoT is gold.

### `dspy.Refine` and `dspy.BestOfN`
Meta-modules.

- `dspy.Refine(module, N=3, reward_fn=...)` — runs the module up to N times; if a reward function says "good enough," stops; otherwise keeps trying. The reward function returns a score; the module stops once it crosses your threshold.
- `dspy.BestOfN(module, N=3)` — runs N times, returns the best by some criterion.

Useful when single-shot is unreliable and you have a quick way to score the result.

### When to use which

| Module | Use for |
|---|---|
| `Predict` | Direct extraction or simple formatting |
| `ChainOfThought` | Multi-step reasoning, classification, anything benefiting from "think first" |
| `ProgramOfThought` | Anything involving arithmetic, dates, list manipulation — code-gen is more reliable than mental math |
| `ReAct` | Tasks needing external lookups, multi-step actions, or tool use |
| `Refine` / `BestOfN` | Quality-critical outputs where one shot isn't reliable |

## Mini-tasks

1. Run `solution.py`. Read all four answers. Which got the right number?
2. Add a `dspy.inspect_history(n=5)` after the ReAct call. Read the trace. Count the steps the agent took.
3. Wrap your `ChainOfThought` from folder 03 in `dspy.BestOfN(N=3)`. Compare the result against single-shot CoT on a couple of questions.

## Common pitfalls

- **Bad tool docstrings** — same as Project 13. The docstring is what the LM reads to decide whether/how to call it. Spend time on it.
- **Unsafe `eval` in calculator tools** — the demo's `eval(expr, {"__builtins__": {}})` is the smallest safe sandbox; for real apps use `numexpr`, `asteval`, or `dspy.PythonInterpreter`.
- **PoT on tasks that need external knowledge** — PoT runs in a sandbox with no internet. For those, use ReAct with a search tool.

## Expected outcome

You can pick the right module for a task without re-reading the docs. You understand that DSPy's agent loop (ReAct) is the same loop you saw in Project 13 — different framework, same architecture.

## Next

→ [05 — Tools & MCP](../05-tools-and-mcp/)
