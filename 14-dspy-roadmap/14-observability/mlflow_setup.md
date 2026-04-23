# MLflow Setup for DSPy

MLflow has first-class DSPy autologging. Three steps to get a UI of every prompt + response your program makes.

## Install

```bash
pip install mlflow
```

## Wire up autologging

At the top of your DSPy script:

```python
import mlflow
import dspy

mlflow.dspy.autolog()                       # captures every LM + Module call
mlflow.set_experiment("my-dspy-experiment") # groups related runs

lm = dspy.LM("ollama_chat/qwen2.5-coder:7b", api_base="http://localhost:11434")
dspy.configure(lm=lm)

# ... your program here. Every call is now logged.
```

## Browse runs

```bash
mlflow ui
# open http://localhost:5000
```

Each program call becomes a "run" in MLflow. Click into a run to see:
- Every prompt sent
- Every LM response
- Module structure traversed
- Latency per call
- Token / cost estimates (when available)

## When to enable

- **Always** during optimizer compilation (folders 09–11). Optimizers make hundreds of calls; the only way to debug a bad compile is to inspect them.
- **Always** during dev-set evaluation runs.
- **Conditionally** in production — autolog adds latency and storage. Sample at, say, 1% of requests.

## Snapshot artifact

You can also explicitly log a compiled program as an MLflow artifact for reproducibility:

```python
mlflow.dspy.log_model(compiled_program, "program")
```

That artifact is then retrievable from any other process, with the same prompt-tuning state baked in.
