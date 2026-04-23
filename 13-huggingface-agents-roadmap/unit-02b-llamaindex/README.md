# Unit 2.2 — The LlamaIndex framework

LlamaIndex is the "data-and-RAG-first" framework. By the end you'll know when to reach for it (heavy ingestion, many sources, RAG-centric apps) and when smolagents would have been faster.

**Course link:** [Unit 2.2 on the HF docs](https://huggingface.co/learn/agents-course/unit2/llama-index/introduction)

## What you'll learn

- **LlamaHub** — the registry of pre-built loaders for ~150 data sources. (PDFs, Notion, Slack, Postgres, etc.)
- **Components**: `LLM`, `Embedding`, `Index`, `QueryEngine`, `Tool`, `Agent`. Each small, composable.
- **Workflows** — LlamaIndex's structured way to chain steps. Their answer to LangGraph.
- **Agents in LlamaIndex** — function-calling style. Less "code-as-action" than smolagents.

## What's in this folder

- [`solution.py`](solution.py) — ingests a folder of text files into a `VectorStoreIndex`, wraps the resulting query engine as a tool, and gives it to a `FunctionAgent`. The agent answers questions over your docs.
- [`sample_docs/`](sample_docs/) — three short notes you can replace with your own.
- [`requirements.txt`](requirements.txt) — `llama-index` + `llama-index-llms-huggingface-api`.

## Setup

```bash
pip install -r requirements.txt
huggingface-cli login
```

## Run it

```bash
python3 solution.py
```

Expected: the script ingests the three sample docs, then asks two questions. The agent decides whether to search the docs or answer from general knowledge.

## Key concepts

### Components in one paragraph each

- **`LLM`**: the model wrapper. `HuggingFaceInferenceAPI`, `OpenAI`, `Anthropic`, `Ollama` — same interface, swappable.
- **`Embedding`**: turns text into vectors for similarity search. `HuggingFaceEmbedding` is the default OSS choice.
- **`Index`**: a data structure for fast retrieval. `VectorStoreIndex` is the default; there are also keyword, knowledge-graph, and hybrid variants.
- **`QueryEngine`**: an `Index` + an `LLM`, exposed as `.query("question")`.
- **`Tool`**: any callable the agent can use. `QueryEngineTool.from_defaults(query_engine=...)` makes one from a query engine.
- **`Agent`**: an LLM + a list of tools + a loop. `FunctionAgent` is the default modern style.

### The mental model: "RAG made of LEGO"
You can swap any component. Want a different LLM? Swap `LLM`. Different vector store? Swap `Index`. Different retrieval logic? Subclass `QueryEngine`. The framework rewards thinking about RAG as composition, not magic.

### Workflows
LlamaIndex's structured way to express "step A → step B → branch on C → step D." Conceptually similar to LangGraph (Unit 2.3) but with a different API. Use when your agent has discrete phases (ingest → retrieve → rank → answer → format).

## Mini-tasks

1. Run `solution.py` on the sample docs.
2. Replace `sample_docs/` with a folder of *your* PDFs (LlamaIndex's `SimpleDirectoryReader` reads PDFs natively if you `pip install pypdf`). Re-run with questions about your own data.
3. Add a `DuckDuckGoSearchToolSpec` so the agent has both your docs *and* web search. Ask a question that requires both.

## Focus vs skim

- **Focus:** "Components" (the conceptual core), "Workflows" (the practical core).
- **Skim:** the LlamaHub catalog — read the index, don't memorize.

## Common pitfalls

- **LlamaIndex when smolagents would do** — if your task is "agent + a couple of tools," smolagents is shorter. LlamaIndex shines when retrieval is the main act.
- **Picking the wrong Embedding** — the default OSS embedder is fine for English. For multilingual, pick a multilingual embedder explicitly.
- **Not chunking docs** — `SimpleDirectoryReader` does basic splitting; for long PDFs you want explicit chunk size + overlap. See `SentenceSplitter`.

## Expected outcome

You understand when LlamaIndex is the right pick: lots of data, lots of source types, complex retrieval logic. You can ingest a corpus and query it with an agent in 30 lines.

## Next

→ [Unit 2.3 — The LangGraph framework](../unit-02c-langgraph/)
