# Unit 2.3 — a 3-node LangGraph that routes input to a QA or summarizer node.

import os
from typing import TypedDict

from langchain_huggingface import HuggingFaceEndpoint
from langgraph.graph import END, START, StateGraph


# 1. Define what the state looks like at any point in the graph.
class GraphState(TypedDict):
    user_input: str
    intent: str
    answer: str


def make_llm():
    if not (os.getenv("HF_TOKEN") or os.getenv("HUGGINGFACE_HUB_TOKEN")):
        raise SystemExit("Need a HF token. Run: huggingface-cli login")
    return HuggingFaceEndpoint(
        repo_id="Qwen/Qwen2.5-72B-Instruct",
        max_new_tokens=128,
        temperature=0.1,
    )


LLM = None  # built lazily so import is cheap

def llm():
    global LLM
    if LLM is None:
        LLM = make_llm()
    return LLM


# 2. Each node is just a function: state in, partial state update out.

def classify(state: GraphState) -> dict:
    """Decide whether the input is a question or a summary request."""
    text = state["user_input"].lower().strip()
    if text.startswith(("summarize", "summarise", "tl;dr")):
        intent = "summary"
    elif text.endswith("?"):
        intent = "question"
    else:
        intent = "question"   # default
    print(f"  [classify] intent = {intent!r}")
    return {"intent": intent}


def answer_qa(state: GraphState) -> dict:
    """Answer a direct question."""
    answer = llm().invoke(f"Answer concisely: {state['user_input']}")
    return {"answer": answer.strip()}


def summarize(state: GraphState) -> dict:
    """Produce a 1-sentence summary."""
    text = state["user_input"]
    if text.lower().startswith(("summarize", "summarise")):
        text = text.split(":", 1)[-1].strip() if ":" in text else text
    answer = llm().invoke(f"Summarize in one sentence: {text}")
    return {"answer": answer.strip()}


def route(state: GraphState) -> str:
    """Conditional edge — return the next node's name."""
    return state["intent"]


# 3. Build the graph.
def build_app():
    graph = StateGraph(GraphState)
    graph.add_node("classify", classify)
    graph.add_node("answer_qa", answer_qa)
    graph.add_node("summarize", summarize)

    graph.add_edge(START, "classify")
    graph.add_conditional_edges(
        "classify", route,
        {"question": "answer_qa", "summary": "summarize"},
    )
    graph.add_edge("answer_qa", END)
    graph.add_edge("summarize", END)
    return graph.compile()


def main():
    app = build_app()
    inputs = [
        "What is the capital of France?",
        "Summarize: Paris is the capital and most populous city of France, known for its art, fashion, and cuisine.",
    ]
    for user_input in inputs:
        print(f"\nINPUT: {user_input}")
        final = app.invoke({"user_input": user_input, "intent": "", "answer": ""})
        print(f"OUTPUT: {final['answer']}")


if __name__ == "__main__":
    main()
