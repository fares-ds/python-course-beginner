# 06 — RAG Pipeline

Build a custom `dspy.Module` that composes **retrieval + reasoning + answering** over a small document set. This is your first multi-step DSPy program.

**Docs link:** [Retrieval-Augmented Generation tutorial](https://dspy.ai/tutorials/rag/)

## What you'll learn

- Subclass `dspy.Module` and define `forward(...)` — how to compose Modules into a pipeline.
- A simple in-memory retriever (no FAISS needed for a small corpus).
- The standard RAG shape: **(question + retrieved context) → answer**.
- Why DSPy's RAG looks identical whether your retriever is in-memory, ColBERT, FAISS, or a SaaS vector DB — they're all just "callable that returns a list of strings."

## What's in this folder

- [`solution.py`](solution.py) — a `RAG` Module that retrieves the top-k matching notes from `data/notes.json` and answers a question over them.
- [`data/notes.json`](data/notes.json) — 5 short notes (cooking, travel, Python).
- [`requirements.txt`](requirements.txt) — `dspy>=3.0,<4.0`.

## Setup

```bash
pip install -r requirements.txt
```

## Run it

```bash
python3 solution.py
```

Expected: three questions — one cooking, one travel, one Python. Each one retrieves the relevant note and answers.

## Key concepts

### Custom `dspy.Module`
This is where DSPy goes from "library of cool primitives" to "a real programming model":

```python
class RAG(dspy.Module):
    def __init__(self, k=2):
        super().__init__()
        self.retrieve = MyRetriever(k=k)
        self.answer = dspy.ChainOfThought("context, question -> answer")

    def forward(self, question):
        context = self.retrieve(question)
        return self.answer(context=context, question=question)
```

`forward` looks like a regular method but it's the thing optimizers later optimize. Two key Modules: `retrieve` (a tool) and `answer` (a `ChainOfThought` Predict). They're both attributes; DSPy walks the tree to find them when compiling.

### Retrievers are just callables
DSPy doesn't impose a retriever class. A retriever is anything you can call like `retriever(query, k=5)` and get back a list of passage strings.

For real apps you'd plug in a vector DB (FAISS, Chroma, Pinecone, ColBERT). For learning, a tiny in-memory keyword search works.

### Why `ChainOfThought` for the answer step?
RAG over multiple documents is reasoning: "given these 3 notes, which one is relevant, and what does it say?" CoT helps the model think before answering, especially when the retrieved context is noisy.

## Mini-tasks

1. Run `solution.py`. Read the answers. Are they grounded in the retrieved notes?
2. Add a 6th note (about anything). Ask a question that requires it. Does the retriever surface it?
3. Replace the keyword retriever with a real vector retriever — `dspy.Embeddings` or `sentence-transformers` + `faiss`. The `forward` method shouldn't need to change.

## Common pitfalls

- **Retriever returning too much** — k=20 stuffs the prompt with noise. Start with k=2 or 3.
- **Forgetting `super().__init__()`** in your Module class — DSPy can't find your sub-modules without it. Subtle but breaks compilation.
- **Hardcoding k inside `forward`** — make it a constructor arg so you can tune it later.

## Expected outcome

You can write a `dspy.Module` subclass that composes retrieval + an LM call. This pattern generalizes to any multi-step pipeline you'll build.

## Next

→ [07 — Data & Examples](../07-data-and-examples/)
