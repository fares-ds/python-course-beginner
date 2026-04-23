# 01 — Setup & Language Models

The 5-minute pre-flight check. Configure DSPy to talk to your local Ollama, then make a one-line call to verify everything works.

**Docs link:** [Language Models](https://dspy.ai/learn/programming/language_models/)

## What you'll learn

- What DSPy is, in one sentence: a framework for *programming* (not prompting) language models.
- `dspy.LM(...)` — the universal LM wrapper. Same API across OpenAI, Anthropic, Ollama, HF, etc.
- `dspy.configure(lm=...)` — sets the global default LM.
- `dspy.Predict("question -> answer")` — the simplest possible DSPy program.

## What's in this folder

- [`solution.py`](solution.py) — configures Ollama, creates a one-line predictor, asks a question.
- [`requirements.txt`](requirements.txt) — just `dspy>=3.0,<4.0`.

## Setup

You need Python 3.10+ and Ollama installed.

```bash
python3 --version              # must be >= 3.10
ollama --version               # if missing: install from ollama.com
ollama pull qwen2.5-coder:7b   # ~4 GB, one-time. Already pulled if you did Project 11.
pip install -r requirements.txt
```

## Run it

```bash
python3 solution.py
```

Expected: a one-sentence answer to "What is the capital of France?" — printed via `dspy.Predict`. Slow first call (~10 s) while Ollama warms up; subsequent calls are quicker.

## Key concepts

### `dspy.LM`
A thin wrapper around [LiteLLM](https://docs.litellm.ai). It speaks "model strings" — the prefix tells LiteLLM which provider to route to:

| Model string | Provider |
|---|---|
| `openai/gpt-4o-mini` | OpenAI |
| `anthropic/claude-3-5-sonnet-20241022` | Anthropic |
| `ollama_chat/qwen2.5-coder:7b` | Ollama (local) |
| `huggingface/Qwen/Qwen2.5-72B-Instruct` | HF Inference API |

Switching providers is a one-line change. That's intentional: DSPy programs are model-agnostic.

### `dspy.configure(lm=...)`
Sets the **default** LM for every DSPy module in the process. You can also pass `lm=` per-module to override.

### `dspy.Predict("question -> answer")`
The simplest module. The string is a **signature** (next folder covers them). DSPy turns it into a prompt that asks the LM to fill in the `answer` field given the `question`.

```python
predict = dspy.Predict("question -> answer")
result = predict(question="What's the capital of France?")
print(result.answer)
```

## Mini-tasks

1. Run `solution.py` — confirm it answers correctly.
2. Change the signature to `"question -> answer: str, confidence: float"`. Re-run. Notice the model now also produces a confidence score.
3. Switch the LM to a different Ollama model (`ollama pull llama3.1:8b` first). One line of change. Run the same demo. Compare answers.

## Common pitfalls

- **Ollama isn't running** — `Connection refused`. Start the Ollama app, or run `ollama serve` in another terminal.
- **Wrong model prefix** — `ollama` (chat completion only) vs `ollama_chat` (proper chat API). Use `ollama_chat` unless you have a reason not to.
- **Pulling a model you didn't configure** — pulling `llama3.1:8b` doesn't change your default. You also have to update the `dspy.LM(...)` call.

## Expected outcome

You can configure DSPy for any LM provider and run a one-line prediction. You're ready to learn signatures.

## Next

→ [02 — Signatures](../02-signatures/)
