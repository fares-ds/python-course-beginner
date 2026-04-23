# 05 — Tools & MCP

How DSPy talks to the outside world: tools (regular Python functions) and **MCP** (Model Context Protocol — Anthropic's open standard for plug-and-play tool servers).

**Docs links:** [Tools](https://dspy.ai/learn/programming/tools/) · [MCP](https://dspy.ai/learn/programming/mcp/)

## What you'll learn

- **`dspy.Tool(fn)`** — wrap any Python callable as a tool the agent can introspect.
- The same docstring-as-prompt discipline as Project 13.
- **MCP** — a standard protocol so any MCP-compatible tool server (filesystem, GitHub, Postgres, web search, etc.) can be dropped into a DSPy ReAct agent.

## What's in this folder

- [`solution.py`](solution.py) — three tools (calculator, fake search, get-current-time) wired into a `dspy.ReAct` agent that needs all three to answer a multi-step question.
- [`mcp_example.py`](mcp_example.py) — a tiny MCP-style snippet (commented; needs an MCP server running) showing the connection pattern.
- [`requirements.txt`](requirements.txt) — `dspy>=3.0,<4.0`. (MCP example would also want `mcp`.)

## Setup

```bash
pip install -r requirements.txt
```

## Run it

```bash
python3 solution.py
```

Expected: the agent breaks the question into three sub-tasks, calls each tool, and stitches together the answer.

## Key concepts

### Tools are just Python functions
```python
def search_movies(query: str) -> str:
    """Search a movies database. Returns matching titles + year.

    Args:
        query: A search query, e.g. "best sci-fi 2010s" or "Christopher Nolan".
    """
    ...   # your implementation
```

DSPy reads the function's signature + docstring + type hints to build the tool description. Same discipline as Project 13: the docstring **is** the prompt for whether/how to call it.

### `dspy.Tool` vs passing the function directly
`dspy.ReAct(..., tools=[my_func])` — DSPy auto-wraps the function in a `dspy.Tool`. You only need to instantiate `dspy.Tool(...)` explicitly when you want to override the name, description, or argument schema.

### MCP in one paragraph
[Model Context Protocol](https://modelcontextprotocol.io) is a standard so anyone can publish a "tool server" (filesystem access, web search, database queries, etc.) and any MCP-compatible client can use it. DSPy v3+ has an `MCPServerStdio` / `MCPClient` integration: point at an MCP server, get a list of tools, drop them into your ReAct agent. Same loop, just plumbed through MCP.

The big win: **you don't write the wrapping code anymore.** Want filesystem access? Run the official `mcp-server-filesystem`. Want GitHub? Run the GitHub MCP server. The community publishes them; you consume.

## Mini-tasks

1. Run `solution.py` and read the agent's tool-call trace.
2. Add a fourth tool (e.g., `unit_convert(value, from_unit, to_unit)`). Ask a question that requires it.
3. Find any MCP server (the official [list](https://github.com/modelcontextprotocol/servers) has a dozen). Run it locally. Adapt `mcp_example.py` to point at it.

## Common pitfalls

- **Type hints that fail** — DSPy passes the LM-generated string args through Python's normal coercion. `def f(x: int)` will fail if the LM produces "five". Use `str` and parse inside the function for robust tools.
- **Tool that does too much** — split. "search_and_summarize" is two tools fused. Two tools means the agent can choose to skip one.
- **Forgetting `max_iters`** — `dspy.ReAct(..., max_iters=...)`. Default is generous; cap it for production.

## Expected outcome

You can write a custom DSPy tool in 5 lines, you understand the discipline of writing tool docstrings, and you know what MCP is for.

## Next

→ [06 — RAG Pipeline](../06-rag-pipeline/)
