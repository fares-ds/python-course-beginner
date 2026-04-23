# Unit 2.3 — The LangGraph framework

LangGraph is the "agent as a state machine" framework. By the end you'll know when to reach for it (structured workflows with branching and human-in-the-loop) and when smolagents would have been faster.

**Course link:** [Unit 2.3 on the HF docs](https://huggingface.co/learn/agents-course/unit2/langgraph/introduction)

## What you'll learn

- The graph metaphor: **nodes** are functions; **edges** are conditional transitions; **state** is a typed dict that flows through.
- When to use a graph vs a loop — graphs win when you have multiple "modes" (research / write / review / publish).
- Building your first graph: define state, define nodes, wire edges, compile.
- Human-in-the-loop pauses (the graph can stop and wait for input).

## What's in this folder

- [`solution.py`](solution.py) — a 3-node graph that classifies an input as "question" or "summary request," routes to the matching node, and returns the result.
- [`requirements.txt`](requirements.txt) — `langgraph` + `langchain` (LangChain provides the LLM wrapper LangGraph uses).

## Setup

```bash
pip install -r requirements.txt
huggingface-cli login
```

## Run it

```bash
python3 solution.py
```

Expected: the script runs the graph on two inputs ("What is the capital of France?" and "Summarize: Paris is..."). Each one is routed to the right node and produces the right kind of output.

## Key concepts

### State
LangGraph state is a typed dict (or dataclass) that's passed to every node and merged with that node's output. The state of the graph at any point is the cumulative dict.

```python
from typing import TypedDict
class GraphState(TypedDict):
    user_input: str
    intent: str
    answer: str
```

### Nodes
A node is a Python function: `state -> partial state update`.

```python
def classify_intent(state: GraphState) -> dict:
    intent = "question" if state["user_input"].endswith("?") else "summary"
    return {"intent": intent}
```

### Edges
Edges connect nodes. Conditional edges are functions returning the name of the next node.

```python
graph.add_conditional_edges(
    "classify",
    lambda state: state["intent"],     # routing function
    {"question": "answer_qa", "summary": "summarize"},
)
```

### When to pick LangGraph vs smolagents

- **smolagents**: a single agent (or two), tools, looping until done. Best for "the LLM decides everything."
- **LangGraph**: a multi-step workflow with predetermined branching, human approvals, retries, parallel branches. Best for "I designed the flow; the LLM is one of the steps."

If your flow chart has more than 4 boxes and 3 conditionals, LangGraph is probably the right pick.

### Human-in-the-loop
LangGraph natively supports pausing at a node, waiting for human input, and resuming. Essential for production: "the agent has prepared a draft email; show it to the user before sending."

## Mini-tasks

1. Run `solution.py`. Read the output and trace the path through the graph for each input.
2. Add a third intent ("translation") with its own node. Update the routing function.
3. Add a `pause_for_approval` node before the final answer. Run the graph; it should stop and wait. (See LangGraph's `interrupt_before` / `interrupt_after`.)

## Focus vs skim

- **Focus:** "Building Blocks of LangGraph", "Building Your First LangGraph". This is most of the unit.
- **Skim:** none. The unit is short; read all of it.

## Common pitfalls

- **Mutable state in nodes** — nodes should return *partial updates* to state, not mutate it in place. LangGraph merges them; in-place mutation leads to confusing bugs.
- **Forgetting to compile** — `app = graph.compile()`. Forgetting this leaves you with a graph definition, not an executable.
- **Using LangGraph for problems smolagents would solve** — graphs add boilerplate. Worth it for structured flows; overkill for "an agent + 2 tools."

## Expected outcome

You can express a multi-step workflow as a graph in 60 lines. You know when *not* to use LangGraph (when one looped agent would do).

## Next

→ [Unit 3 — Use Case for Agentic RAG](../unit-03-agentic-rag/)
