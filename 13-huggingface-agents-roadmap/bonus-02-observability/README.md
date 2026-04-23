# Bonus Unit 2 — Agent Observability and Evaluation

Production agents without observability are gambling. By the end you'll have a real eval suite and a way to see every step your agent takes.

**Course link:** [Bonus 2 on the HF docs](https://huggingface.co/learn/agents-course/bonus-unit2/introduction)

**Pick this if:** you're going to ship an agent. Or if you want a "real engineer" portfolio piece.

## What you'll learn

- **Why agents are hard to evaluate** — non-determinism, variable step counts, no single right answer.
- **Tracing** — capturing every LLM call, tool call, and observation in a structured log.
- **Eval discipline** — a fixed test set scored after every change. The only way to tell whether you got better.
- Tools: **Langfuse**, **Phoenix** (Arize), **OpenTelemetry / OpenLLMetry**.

## What's in this folder

- [`solution.py`](solution.py) — runs a smolagents agent under OpenTelemetry instrumentation. Each LLM call + tool call gets logged. Configurable to send to Langfuse or Phoenix; defaults to console.
- [`eval_set.json`](eval_set.json) — 5 hand-crafted (input, expected) pairs. The minimum viable eval.
- [`requirements.txt`](requirements.txt) — `smolagents` + `opentelemetry` + `openinference-instrumentation-smolagents`.

## Setup

```bash
pip install -r requirements.txt
huggingface-cli login
```

For Langfuse or Phoenix backends, see comments in `solution.py`.

## Run it

```bash
python3 solution.py
```

Expected: the agent runs on the 5 eval cases. Each step prints. At the end, an eval summary: pass/fail per case + an overall score.

## Key concepts

### Why agent eval is hard
- **Non-deterministic**: same input, different output across runs.
- **Variable cost**: a "good" run is 4 steps; a "bad" run is 30. The cost difference is 8×.
- **No single right answer**: many questions have multiple valid answers ("Paris" vs "Paris, France").
- **Trace-level vs answer-level**: an agent can get the right answer via terrible reasoning, or the wrong answer via great reasoning. Both matter.

The fix isn't a single metric — it's a **panel**: pass-rate, average steps, average tokens, average latency, average cost. Look at all of them after every change.

### Tracing in 4 lines
With OpenInference's smolagents instrumentation:

```python
from openinference.instrumentation.smolagents import SmolagentsInstrumentor
SmolagentsInstrumentor().instrument()
# ... now run your agent. Every call is captured.
```

Send the traces somewhere viewable: Phoenix (free, local), Langfuse (free tier + cloud), or just console.

### A real eval set
Doesn't need to be big to start. **5 cases is better than 0.** Curate over time:

```json
[
  {"input": "What's the capital of France?", "expected": "Paris"},
  {"input": "Compute 17 + 25", "expected": "42"},
  ...
]
```

Score with: did the answer contain the expected string? Did the agent finish in <10 steps? Did the agent use the right tool? Pick what matters for your use case.

## Mini-tasks

1. Run `solution.py`. Read the eval summary. How many cases passed?
2. Make the agent fail one case on purpose (give it a misleading tool description). Re-run. Verify your eval catches it.
3. Add a 6th eval case for an edge case you suspect would break the agent. Iterate the agent until it passes.

## Focus vs skim

- **Focus:** the workflow (instrument → run → trace → evaluate → iterate). The specific tool (Langfuse vs Phoenix) is a detail.

## Common pitfalls

- **Eval cases that are too easy** — if the agent passes all 5 trivially, you've measured nothing. Include hard cases.
- **No trace-reading** — having traces is useless if you don't read them. Block 20 minutes/week to read your own traces in production.
- **Optimizing for one metric** — pass-rate goes up but average tokens triple. Look at the panel, not one number.

## Expected outcome

You can ship an agent and prove (with traces + an eval suite) whether your last change made it better or worse.

## Next

→ [Bonus 3 — Agents in Games with Pokemon](../bonus-03-pokemon-agent/)
