# Chapter 5 — slice, filter, map, search over a real dataset.

import numpy as np
import torch
from datasets import load_dataset
from transformers import AutoModel, AutoTokenizer

EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


def section(title):
    print()
    print("=" * 60)
    print(title)
    print("=" * 60)


def demo_load_and_slice():
    section("DEMO 1: load, filter, map, split")
    # Load only the train split so it downloads fast.
    ds = load_dataset("imdb", split="train")
    print(f"  Loaded {len(ds)} reviews")
    print(f"  First example: {ds[0]['text'][:120]}...")
    print(f"  Label: {ds[0]['label']} (0=neg, 1=pos)")

    # Chain: keep longer-than-200-char reviews, shuffle, take 500.
    subset = (
        ds.filter(lambda ex: len(ex["text"]) > 200)
        .shuffle(seed=42)
        .select(range(500))
    )
    print(f"  After filter+shuffle+select: {len(subset)} reviews")

    # Split the subset into train/test.
    split = subset.train_test_split(test_size=0.1, seed=42)
    print(f"  Train: {len(split['train'])}, Test: {len(split['test'])}")


def demo_map():
    section("DEMO 2: .map() to add a computed column")
    ds = load_dataset("imdb", split="train[:200]")
    # `batched=True` passes a batch of rows at once — much faster than one-by-one.
    ds = ds.map(
        lambda batch: {"char_count": [len(t) for t in batch["text"]]},
        batched=True,
    )
    print(f"  Column names: {ds.column_names}")
    print(f"  Avg chars: {sum(ds['char_count']) / len(ds):.0f}")


def mean_pool(last_hidden_state, attention_mask):
    # Average the token embeddings, ignoring padding. Standard sentence-embedding recipe.
    mask = attention_mask.unsqueeze(-1).float()
    summed = (last_hidden_state * mask).sum(dim=1)
    counts = mask.sum(dim=1).clamp(min=1)
    return summed / counts


def embed(texts, tokenizer, model):
    inputs = tokenizer(texts, padding=True, truncation=True, max_length=128, return_tensors="pt")
    with torch.no_grad():
        out = model(**inputs)
    pooled = mean_pool(out.last_hidden_state, inputs["attention_mask"])
    # L2-normalize so cosine similarity == inner product.
    return torch.nn.functional.normalize(pooled, p=2, dim=1).numpy()


def demo_faiss_search():
    section("DEMO 3: FAISS semantic search over 200 reviews")
    ds = load_dataset("imdb", split="train[:200]")
    tokenizer = AutoTokenizer.from_pretrained(EMBED_MODEL)
    model = AutoModel.from_pretrained(EMBED_MODEL)

    # Embed every review (small enough to do in one batch).
    embeddings = embed(ds["text"], tokenizer, model)
    ds = ds.add_column("embeddings", [e for e in embeddings])
    ds.add_faiss_index(column="embeddings")

    query = "a brilliant, underrated thriller"
    q_vec = embed([query], tokenizer, model).astype(np.float32)
    scores, examples = ds.get_nearest_examples("embeddings", q_vec[0], k=3)
    print(f"  Query: {query!r}")
    for i, (score, text) in enumerate(zip(scores, examples["text"])):
        print(f"\n  {i+1}. score={score:.3f}")
        print(f"     {text[:180]}...")


def demo_streaming():
    section("DEMO 4: streaming — don't download the whole dataset")
    try:
        ds = load_dataset("wikitext", "wikitext-2-raw-v1", split="train", streaming=True)
        for i, example in enumerate(ds):
            if i >= 3:
                break
            text = example["text"][:100].replace("\n", " ")
            print(f"  [{i}] {text}...")
    except Exception as e:
        print(f"  Streaming demo skipped: {e}")


def main():
    demo_load_and_slice()
    demo_map()
    demo_faiss_search()
    demo_streaming()
    print("\nOn to Chapter 6 — tokenizers.")


if __name__ == "__main__":
    main()
