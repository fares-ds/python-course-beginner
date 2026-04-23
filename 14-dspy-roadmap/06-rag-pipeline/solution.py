# 06 — a RAG pipeline as a dspy.Module subclass.

import json
from pathlib import Path

import dspy

lm = dspy.LM("ollama_chat/qwen2.5-coder:7b", api_base="http://localhost:11434")
dspy.configure(lm=lm)

NOTES = json.loads((Path(__file__).parent / "data" / "notes.json").read_text())


def keyword_retrieve(query: str, k: int = 2) -> list[str]:
    """Tiny keyword retriever. Returns the top-k notes whose text shares
    the most word overlap with the query. Fine for a 5-note demo; replace
    with FAISS / ColBERT / Chroma for anything real."""
    query_words = set(query.lower().split())
    scored = [
        (len(query_words & set(n["text"].lower().split())), n["text"])
        for n in NOTES
    ]
    scored.sort(reverse=True)
    return [text for _, text in scored[:k]]


class RAG(dspy.Module):
    """Retrieve top-k notes, then answer the question grounded in them."""

    def __init__(self, k: int = 2):
        super().__init__()
        self.k = k
        # Both sub-modules become discoverable to DSPy optimizers later.
        self.answer = dspy.ChainOfThought("context, question -> answer")

    def forward(self, question: str):
        passages = keyword_retrieve(question, k=self.k)
        context = "\n\n".join(passages)
        return self.answer(context=context, question=question)


def main():
    rag = RAG(k=2)
    questions = [
        "How do I cook pasta well?",
        "What's the best neighborhood to stay in Lisbon?",
        "Why use a Python virtual environment?",
    ]
    for q in questions:
        print(f"\n{'=' * 60}\nQ: {q}\n{'=' * 60}")
        result = rag(question=q)
        print(f"A: {result.answer}")


if __name__ == "__main__":
    main()
