# Phoenix Setup for DSPy

[Phoenix](https://phoenix.arize.com) gives you a live trace UI for LLM apps. Free, open source, runs locally.

## Install

```bash
pip install arize-phoenix arize-phoenix-otel openinference-instrumentation-dspy
```

## Run the Phoenix server

```bash
phoenix serve
# UI at http://localhost:6006
```

(Or use Phoenix Cloud — they have a free tier — if you don't want a local process.)

## Wire up DSPy

```python
from phoenix.otel import register
from openinference.instrumentation.dspy import DSPyInstrumentor

register(project_name="my-dspy-app")
DSPyInstrumentor().instrument()

import dspy
lm = dspy.LM("ollama_chat/qwen2.5-coder:7b", api_base="http://localhost:11434")
dspy.configure(lm=lm)

# ... your program. Every Module call shows up in Phoenix as a span.
```

## What you see

- **Trace tree** — for each top-level program call, the full nested call graph: which Modules ran, which sub-Modules they called, etc.
- **Span attributes** — prompt, response, tokens, latency for each LM call.
- **Comparison views** — side-by-side traces from different runs (useful for "before vs after compilation").

## When to use Phoenix vs MLflow

| | Phoenix | MLflow |
|---|---|---|
| Strongest at | Live trace UI for nested LLM/agent calls | Long-term experiment tracking + model registry |
| Setup | One process, one decorator | Heavier, more enterprise-y |
| Best when | Debugging an agent's loop in real time | Tracking many compilations over weeks |

You can run both — they're complementary — but for learning, pick one.
