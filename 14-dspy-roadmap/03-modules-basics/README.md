# 03 — Modules: `Predict` and `ChainOfThought`

Modules are the building blocks. A Module takes a signature and defines a *strategy* for how the LM fills it in. `Predict` just asks; `ChainOfThought` asks the LM to think step-by-step first.

**Docs link:** [Modules](https://dspy.ai/learn/programming/modules/)

## What you'll learn

- **`dspy.Predict`** — direct prompting. What you've seen so far.
- **`dspy.ChainOfThought`** — same signature, but the LM is asked for a `reasoning` field *before* the declared outputs. Often dramatically better on reasoning tasks.
- **`dspy.inspect_history(n=1)`** — see the last prompt/response pair. Your single most useful debugging tool.

## What's in this folder

- [`solution.py`](solution.py) — runs `Predict` and `ChainOfThought` on the same math word problem. Prints both answers + the CoT rationale + `inspect_history` for the CoT call.

## Setup

```bash
pip install -r requirements.txt
```

## Run it

```bash
python3 solution.py
```

Expected: two answers to a math word problem. The `Predict` answer may be wrong; the `ChainOfThought` answer, with visible reasoning, is usually right.

## Key concepts

### `Predict` vs `ChainOfThought`
They take the same signature. The difference is what DSPy adds to the prompt:

- **`Predict`**: "Given `question`, produce `answer`." Done.
- **`ChainOfThought`**: "Given `question`, first produce `reasoning`, then `answer`." The rationale is a free extra output field.

For anything that needs arithmetic, multi-step reasoning, or careful consideration, CoT is almost always worth the extra tokens.

### The rationale is real
```python
result = cot(question="If a shelf has 3 rows of 7 books and 2 rows of 5 books, how many books total?")
print(result.reasoning)   # "3 rows x 7 = 21. 2 rows x 5 = 10. Total: 21 + 10 = 31."
print(result.answer)      # "31"
```

You can read the reasoning. That's how you catch subtle bugs.

### `dspy.inspect_history(n=1)`
Prints the last `n` (prompt, response) pairs sent to the LM. Your debugging lifeline:

```python
dspy.inspect_history(n=1)
```

You'll see the exact prompt DSPy built, the exact LM reply, and how DSPy parsed it into the `Prediction` object. If something's off, it's here.

### Why these are called "Modules"
They subclass `dspy.Module`. They're composable: a custom Module can *call* other Modules inside its `forward`. The RAG folder (06) will show this.

## Mini-tasks

1. Run `solution.py`. Compare `Predict` and `ChainOfThought` answers on a multi-step math question. Read the `inspect_history` output and find where the reasoning is in the prompt.
2. Try both on "What's 2 + 2?" — does CoT still add value? (Not really — short tasks don't need it.)
3. Write your own multi-step word problem. Does `Predict` get it? Does CoT?

## Common pitfalls

- **CoT on trivial tasks** — wastes tokens. Use `Predict` when the answer is direct.
- **Ignoring the reasoning field** — CoT's rationale is yours to read. It's the first place to look when the answer is wrong.
- **Large models don't need CoT as much** — GPT-4-class models often CoT implicitly. Smaller models (7B) improve dramatically with explicit CoT.

## Expected outcome

You can pick `Predict` vs `ChainOfThought` by looking at a task. You use `inspect_history` reflexively when something seems off.

## Next

→ [04 — Modules: `ReAct` and `ProgramOfThought`](../04-modules-agentic/)
