# Unit 3 — Use Case for Agentic RAG

The most career-relevant unit. By the end you'll have built an agent that intelligently retrieves over a corpus you choose — the same shape as 80% of "LLM apps" that ship in industry.

**Course link:** [Unit 3 on the HF docs](https://huggingface.co/learn/agents-course/unit3/agentic-rag/introduction)

## What you'll learn

- **"Agentic" RAG** vs **vanilla RAG** — and why the agentic version is sometimes worse for simple Q&A.
- A retriever as a **tool** the agent can choose to call (or not).
- The course's worked example — a "Gala Agent" that retrieves guest stories on demand.

## What's in this folder

- [`solution.py`](solution.py) — a smolagents `CodeAgent` with a "search guest database" tool. Given a question, the agent decides whether to retrieve, what to retrieve, and how many times.
- [`guests.json`](guests.json) — a tiny made-up guest database (5 people).
- [`requirements.txt`](requirements.txt) — `smolagents`.

## Setup

```bash
pip install -r requirements.txt
huggingface-cli login
```

## Run it

```bash
python3 solution.py
```

Expected: the script asks two questions. The first ("Who is Jane Smith?") triggers a single retrieval. The second ("Tell me about all the guests who studied at Stanford and write me a one-line intro for each") triggers multiple retrievals + synthesis.

## Key concepts

### Vanilla RAG vs agentic RAG

|  | Vanilla RAG | Agentic RAG |
|---|---|---|
| Retrievals per query | Always 1 | 0, 1, 2, or N — agent decides |
| Query reformulation | None | Agent rewrites if results are weak |
| When to use | Simple Q&A over known corpus | Multi-step, comparative, or "I'm not sure I have an answer yet" |
| Cost | 1 LLM call + 1 retrieval | N LLM calls + M retrievals — variable |

If vanilla RAG already scores >85% on your eval, **don't add agency** — it'll cost more without helping.

### Retriever as tool
The retriever is just a Python function:

```python
@tool
def search_guests(query: str) -> str:
    """Returns guest information matching the query.

    Args:
        query: A natural-language search query, e.g. "guests who work at Google".
    """
    return run_search(query)
```

The agent sees its description, decides when to call it, decides what to pass as `query`. That's the whole "agentic" part.

### Why this is the most career-relevant unit
The shape "user question → maybe retrieve → maybe retrieve again → answer" is the shape of:
- Customer support bots
- "Chat with your docs" products
- Code assistants over your codebase
- Internal company knowledge agents
- Most of what people mean by "RAG" in 2026

If you only get one unit out of this course, get this one.

## Mini-tasks

1. Run `solution.py` on the sample data. Read the agent's traces. Count how many retrievals each question triggered.
2. Replace `guests.json` with 20 guests of your invention. Add at least one ambiguity (two guests with the same first name) and see how the agent handles it.
3. Add a vanilla-RAG baseline: a function that always retrieves once, then generates. Compare its answers to the agent's on 5 questions. Where does the agent help? Where does it just spend more tokens?

## Focus vs skim

- **Focus:** the entire unit. It's short (5 sections) and dense.

## Common pitfalls

- **Over-engineering** — if vanilla RAG works, ship it. Agency adds latency, cost, and failure modes.
- **No eval** — agentic RAG with no eval is just expensive vanilla RAG. Always measure.
- **Bad retriever description** — the agent calls the tool too often (because "looks helpful") or too rarely (because "doesn't seem relevant"). The fix is in the docstring.

## Expected outcome

You have a working agentic RAG pipeline you can adapt to any corpus. You can articulate when agentic RAG beats vanilla RAG (and when it doesn't).

## Next

→ [Unit 4 — Final Project: GAIA](../unit-04-final-project-gaia/)
