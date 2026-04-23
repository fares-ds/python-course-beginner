# Chapter 5 — The 🤗 Datasets library

The data plumbing layer. By the end you'll stop thinking of `datasets` as "yet another library" and start thinking of it as pandas-for-NLP — except it also handles 300 GB corpora without blinking.

**Course link:** [Chapter 5 on the HF docs](https://huggingface.co/learn/llm-course/en/chapter5/1)

## What you'll learn

- `load_dataset()` — from the Hub, from a local CSV/JSON/Parquet, from a Python generator.
- Memory-mapped **Arrow** storage — why you can load huge datasets without exhausting RAM.
- `.map()`, `.filter()`, `.select()`, `.train_test_split()` — the four operations you'll use constantly.
- **Streaming** (`streaming=True`) for datasets that don't fit on disk.
- **FAISS** semantic search — your first taste of the retrieval machinery behind RAG.

## What's in this folder

- [`solution.py`](solution.py) — loads IMDb, slices/filters/maps it, then builds a tiny FAISS index and does a semantic-search demo.
- [`requirements.txt`](requirements.txt) — `datasets`, `transformers`, `faiss-cpu`, `torch`.

## Setup

```bash
pip install -r requirements.txt
```

First run downloads IMDb (~80 MB) and a small embedding model (~130 MB).

## Run it

```bash
python3 solution.py
```

Expected: four demos. Load IMDb, filter/map it in a chain, do a `train_test_split`, then build a FAISS index on a subset and run a semantic search query.

## Key concepts

### Memory-mapped Arrow
When you `load_dataset("imdb")`, the data lives on disk as Apache Arrow files. The library accesses rows on demand via memory mapping. You can "load" a 300 GB dataset and it takes zero extra RAM — only the rows you actually touch get read.

### The fluent chain
```python
ds = (
    load_dataset("imdb", split="train")
    .filter(lambda ex: len(ex["text"]) > 200)
    .map(tokenize_fn, batched=True)
    .shuffle(seed=42)
    .select(range(1000))
)
```
Each operation returns a new `Dataset`. They compose cleanly, they're lazy-enough, and they're **cache-aware** — re-running a map with the same function uses the cache.

### Streaming mode
```python
ds = load_dataset("c4", "en", split="train", streaming=True)
for example in ds.take(100):
    print(example["text"][:200])
```
Never downloads the full dataset. Essential for >50 GB corpora.

### FAISS indexing
```python
ds = ds.add_faiss_index(column="embeddings")
scores, examples = ds.get_nearest_examples("embeddings", query_vec, k=5)
```
Wraps a FAISS vector index around a dataset column. One line of setup; millisecond retrieval.

## Mini-tasks

1. Load IMDb. Count how many reviews contain the word "terrible". (Hint: `.filter()`)
2. Load a local CSV from disk: `load_dataset("csv", data_files="your.csv")`. Confirm it works the same as a Hub dataset.
3. Stream the first 50 examples from `c4` (the 300+ GB C4 corpus) with `streaming=True`. Notice it doesn't download the whole thing.

## Focus vs skim

- **Focus:** section 3 (slice and dice), section 4 (big data / streaming), section 6 (FAISS — preview of RAG).
- **Skim:** section 5 (creating a custom dataset from scratch) — return to this only when you need it.

## Common pitfalls

- **Forgetting `batched=True` in `.map()`** — 10× slower on large datasets.
- **Changing the map function without clearing the cache** — the stale cache silently wins. Use `load_from_cache_file=False` while iterating.
- **Confusing `.select(range(N))` with `.take(N)`** — the first is random-access and returns a `Dataset`; the second only exists on streaming datasets.

## Expected outcome

You can load, slice, filter, and map any dataset on the Hub in one fluent chain. You understand why this scales to 300 GB.

## Next

→ [Chapter 6 — The 🤗 Tokenizers library](../chapter-06-tokenizers/)
