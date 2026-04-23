# 13 — Saving and Deployment

A compiled DSPy program is just data — instructions and demos. Save it to disk; load it later; serve it behind a FastAPI endpoint.

**Docs link:** [Saving](https://dspy.ai/tutorials/saving/) · [Deployment](https://dspy.ai/tutorials/deployment/)

## What you'll learn

- `program.save("path.json")` and `dspy.load("path.json")` — round-trip a compiled program.
- The "JSON" save format vs the "pickle/whole-module" format — when to use each.
- A 30-line FastAPI wrapper that serves a saved DSPy program over HTTP.

## What's in this folder

- [`solution.py`](solution.py) — saves a small compiled program (CoT for Q&A) to `program.json`, then loads it back and runs a query.
- [`server.py`](server.py) — a tiny FastAPI app that wraps the loaded program. `uvicorn server:app --reload` to start.
- [`requirements.txt`](requirements.txt) — `dspy`, `fastapi`, `uvicorn`.

## Setup

```bash
pip install -r requirements.txt
```

## Run it

Save & reload:

```bash
python3 solution.py
```

Expected: trains a tiny program with `BootstrapFewShot`, saves it to `program.json`, loads it back from a fresh process, runs a query. Confirms the round-trip works.

Serve over HTTP:

```bash
uvicorn server:app --reload
# in another terminal:
curl -X POST http://127.0.0.1:8000/ask -H "Content-Type: application/json" \
  -d '{"question": "Who wrote Hamlet?"}'
```

Expected: a JSON response with the answer.

## Key concepts

### `save("path.json")` — the "instructions + demos" format
```python
compiled.save("program.json")
loaded = dspy.load("program.json")   # need a `program` object to load INTO
```

This format saves only the **prompt-tuning state** — instructions and demos for each `Predict`. The Module structure (i.e., the `forward` method, the sub-modules) is *not* saved. You need to re-instantiate the same Module class first, then call `.load(...)`.

This is what you want 95% of the time: text JSON, diff-friendly, version-controllable.

### `save("path.pkl", save_program=True)` — the whole-module format
```python
compiled.save("program.pkl", save_program=True)
loaded = dspy.load("program.pkl")    # no need for a class definition
```

Saves the entire Module object via pickle. Useful when you don't have the Python class on the loading side. Less safe (pickle), less portable.

### Deployment shape
The minimum viable serving:

```python
from fastapi import FastAPI
import dspy

app = FastAPI()
program = ... # rebuild + load

@app.post("/ask")
def ask(payload: dict):
    return {"answer": program(question=payload["question"]).answer}
```

For production you'd add: per-request LM context (`with dspy.context(lm=...):`), structured request/response models with Pydantic, a request queue, observability (folder 14).

## Mini-tasks

1. Run `solution.py`. Confirm the round-trip works.
2. Run `uvicorn server:app --reload`. Hit it with `curl`. Confirm you get an answer.
3. Modify `server.py` to accept a `model` query parameter so callers can swap which LM the program uses. (Hint: `with dspy.context(lm=dspy.LM(model)):`)

## Common pitfalls

- **Loading without re-instantiating the Module first** — `dspy.load(...)` for `.json` saves needs you to pass an existing `program` instance. Confusing first-time gotcha.
- **Loading model state across DSPy versions** — JSON saves are mostly forward-compatible; pickle saves are not. Pin your DSPy version in production.
- **Serving without rate limiting** — a single slow request can block the worker. Use FastAPI's `BackgroundTasks` or proper async handling for real loads.

## Expected outcome

You can save / reload a DSPy program and serve it over HTTP. You know which save format to use when.

## Next

→ [14 — Observability](../14-observability/)
