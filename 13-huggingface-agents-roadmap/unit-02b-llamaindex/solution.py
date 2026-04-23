# Unit 2.2 — LlamaIndex agent answering questions over a folder of docs.

import os

from llama_index.core import Settings, SimpleDirectoryReader, VectorStoreIndex
from llama_index.core.agent.workflow import FunctionAgent
from llama_index.core.tools import QueryEngineTool
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.huggingface_api import HuggingFaceInferenceAPI


def main():
    if not (os.getenv("HF_TOKEN") or os.getenv("HUGGINGFACE_HUB_TOKEN")):
        raise SystemExit("Need a HF token. Run: huggingface-cli login")

    # 1. Configure components globally (you can also pass them per-object).
    Settings.embed_model = HuggingFaceEmbedding("sentence-transformers/all-MiniLM-L6-v2")
    Settings.llm = HuggingFaceInferenceAPI(model_name="Qwen/Qwen2.5-72B-Instruct")

    # 2. Ingest the sample docs into a vector index.
    docs = SimpleDirectoryReader("sample_docs").load_data()
    print(f"Ingested {len(docs)} documents.")
    index = VectorStoreIndex.from_documents(docs)

    # 3. Wrap the index as a tool.
    notes_tool = QueryEngineTool.from_defaults(
        query_engine=index.as_query_engine(),
        name="search_notes",
        description="Search the user's personal notes about cooking, travel, and Python.",
    )

    # 4. Build a FunctionAgent that has the notes tool.
    agent = FunctionAgent(
        tools=[notes_tool],
        llm=Settings.llm,
        system_prompt=(
            "You are a helpful assistant. When the user asks about cooking, travel, "
            "or programming, search their notes first. Otherwise answer from general knowledge."
        ),
    )

    # 5. Ask two questions. First should hit the notes; second shouldn't.
    for question in [
        "What did I write about cooking pasta?",
        "What is the capital of Australia?",
    ]:
        print(f"\nQ: {question}")
        response = agent.run(question)
        # `response` may be a coroutine in some LlamaIndex versions; handle both.
        if hasattr(response, "__await__"):
            import asyncio
            response = asyncio.run(response)
        print(f"A: {response}")


if __name__ == "__main__":
    main()
