# Project 12 — Hugging Face LLM Course Roadmap

A structured 10-week plan for working through the [Hugging Face LLM Course](https://huggingface.co/learn/llm-course/en/chapter1/1) end-to-end. One sub-folder per chapter. Each has its own `README.md`, a runnable `solution.py`, and a `requirements.txt`.

The course is 13 chapters (0–12). Hugging Face suggests 6–8 hours per chapter per week. At that pace, the main path is ~10 weeks. This project groups the chapters into **5 phases** with bridge projects between them.

## Chapters

| # | Chapter | Phase |
|---|---------|-------|
| 0 | [Setup](chapter-00-setup/) | Foundations |
| 1 | [Transformer models](chapter-01-transformer-models/) | Foundations |
| 2 | [Using 🤗 Transformers](chapter-02-using-transformers/) | Foundations |
| 3 | [Fine-tuning a pretrained model](chapter-03-fine-tuning/) | Make it yours |
| 4 | [Sharing models and tokenizers](chapter-04-sharing-models/) | Make it yours |
| 5 | [The Datasets library](chapter-05-datasets/) | Data plumbing |
| 6 | [The Tokenizers library](chapter-06-tokenizers/) | Data plumbing |
| 7 | [Classical NLP tasks](chapter-07-classical-nlp-tasks/) | Real tasks |
| 8 | [How to ask for help](chapter-08-asking-for-help/) | Real tasks |
| 9 | [Building demos with Gradio](chapter-09-gradio-demos/) | Ship and scale |
| 10 | [Curating high-quality datasets](chapter-10-curating-datasets/) | Ship and scale |
| 11 | [Fine-tune Large Language Models](chapter-11-fine-tuning-llms/) | Ship and scale |
| 12 | [Build Reasoning Models](chapter-12-reasoning-models/) | Ship and scale |

## Start here

```bash
cd chapter-00-setup
pip install -r requirements.txt
python3 solution.py
```

If the environment check passes, you're ready for Chapter 1. Each chapter folder has its own setup instructions (since later chapters add heavier dependencies like `peft`, `trl`, `bitsandbytes`).

## Prerequisites

The course lists two:

| You need | Why | If you're missing it |
|---|---|---|
| **Solid Python** — functions, classes, decorators, `with`, list/dict comprehensions, venvs | Every example is Python; HF APIs lean heavily on classes and context managers. | Do projects 1–10 in this repo. |
| **Basic deep-learning intuition** — gradient descent, loss functions, training vs inference, why GPUs | The course doesn't re-teach these. | [fast.ai Lessons 1–4](https://course.fast.ai/) (~20 hrs) or [Karpathy's Zero to Hero](https://karpathy.ai/zero-to-hero.html) videos 1–4. |

**Optional but useful:** some PyTorch (`nn.Module`, `optimizer.step()`), basic linear algebra, git.

**Self-check:** can you (a) write a Python class with `__init__` and one method, (b) explain what a loss function is in one sentence, (c) run `pip install` in a venv? If any is shaky, do the prep path first.

## The five phases

| Phase | Weeks | Chapters | Theme | Bridge project |
|---|---|---|---|---|
| **1. Foundations** | 1–2 | 0, 1, 2 | Run inference end-to-end, manually and via `pipeline()`. | Pipeline Playground — a CLI that runs different task types. |
| **2. Make it yours** | 3–4 | 3, 4 | First fine-tune + push to the Hub. | Custom sentiment classifier for a domain you care about. |
| **3. Data plumbing** | 5–6 | 5, 6 | Load / slice / filter datasets, train your own tokenizer. | Domain tokenizer + FAISS semantic search. |
| **4. Real tasks** | 7–8 | 7, 8 | Pick 2–3 classical NLP tasks + debugging skills. | End-to-end NER pipeline, Hub-hosted. |
| **5. Ship and scale** | 9–12 | 9, 10, 11, 12 | Gradio demos, data curation, LoRA, reasoning models. | LoRA-fine-tuned chat model with a Gradio demo. |

## Tooling setup (once, before Chapter 1)

### Where to run the code

- **Colab** (recommended for beginners) — free T4 GPU, notebooks open from the course directly.
- **Local venv** — `python3.11 -m venv .venv && source .venv/bin/activate`. CPU-only training is painful past Chapter 3.
- **Kaggle Notebooks** — 30 free GPU hrs/week.
- **Lightning AI / Modal / Paperspace** — paid, for Chapter 7+ when T4 time stops being enough.

**Practical default:** Colab through Chapter 6; paid GPU for 7, 11, 12.

### Hugging Face account

Sign up at [hf.co/join](https://huggingface.co/join), then:

```bash
pip install huggingface_hub
huggingface-cli login   # paste a write-scope token from hf.co/settings/tokens
```

You need this for Chapter 4 onward.

---

## Deep understanding layer

Re-read this whenever something feels too magical.

### Transformers in one paragraph
A Transformer takes tokens, turns each into a vector, and runs them through attention layers. **Attention** lets every token look at every other token and decide which are relevant. Older models (RNNs) processed one at a time and forgot. Transformers process in parallel and remember everything. Depth (layers) and width (hidden dim) are the two main size knobs.

### Encoder vs decoder vs encoder-decoder

| Type | Reads | Writes | Example | Best for |
|---|---|---|---|---|
| Encoder | Whole input, bidirectional | Single label/vector | BERT | Classification, NER, embeddings |
| Decoder | Left-to-right (causal) | One token at a time | GPT, Llama | Generation, chat, code |
| Encoder-decoder | Input + previously generated | One token at a time | T5, BART | Translation, summarization |

ChatGPT/Claude are decoder-only. Encoders still dominate for "understand this short text" tasks.

### Tokenization, intuitively
Models read integer IDs from a fixed vocabulary (32k–256k entries). Words don't map 1:1 — they get split into **subwords**. Same sentence → different lengths in different tokenizers. Non-English text is often 2–5× more tokens than English. GPT-4's "128k context" is 128k *tokens*, not characters or words (~100k English words).

### Fine-tuning vs prompting vs RAG vs training from scratch
Cheapest to most expensive:

1. **Prompting** — change the input only. Free. Try this first.
2. **RAG** — retrieve docs at inference time, stuff into prompt. Cheap. Use for *facts*.
3. **Fine-tuning (SFT/LoRA)** — change the weights. Hours + ~1k–100k examples. Use for *style*.
4. **Training from scratch** — $100k–$100M of compute. Use if you're an AI lab.

The #1 beginner mistake: reaching for fine-tuning when prompting + RAG would work.

### Inference vs training
- **Training** — slow, GPU-heavy, offline, done periodically.
- **Inference** — fast, latency-sensitive, online, done per request.

Production is almost always inference-only. "Inference optimization" (quantization, KV-cache, vLLM, TGI) is its own discipline.

---

## Five capstone projects (pick one after Phase 5)

1. **Domain text classifier** — fine-tune distilbert on domain classification, deploy as a Space. (Chapters 1–4 + 9.)
2. **Custom-tokenizer language model** — train a tokenizer on a niche corpus, fine-tune a 120M model on it. (Chapters 5, 6, 7.)
3. **Extractive QA over your own docs** — fine-tune a QA model on your own writing. (Chapter 7 + 9.)
4. **LoRA-fine-tuned chat assistant** — SFT a small open LLM with LoRA, deploy chat UI. (Chapter 11 + 9. Most career-relevant.)
5. **RAG-powered QA agent** — ingest corpus → chunk → embed → FAISS → retrieve → generate → cite. (All of Chapters 5, 6, 11 + project 13's agentic RAG unit.)

Pick **one**. Depth beats breadth. That single project will get you further in conversations than five half-built ones.

---

## Common pitfalls

1. **Tokenization as a black box** — spend a real day on Chapter 6. Always check `tokenizer.tokenize(text)`.
2. **LLM as a black box** — always check the chat template, generation kwargs, and system prompt. 80% of "broken model" is one of these three.
3. **Skipping evaluation** — write 20 eval prompts *before* training. Score base model. Score after every run. Don't ship if worse.
4. **Over-fine-tuning** — try prompting + few-shot before fine-tuning.
5. **Out-of-memory** — reduce batch size, increase gradient accumulation, enable bf16/fp16, enable gradient checkpointing, switch to LoRA.
6. **Expecting fine-tuning to teach facts** — it teaches style. For facts, use RAG.
7. **No seed, no versions** — `seed=42` in `TrainingArguments`, pin deps in `requirements.txt`, write versions into your model card.

---

## Learning workflow that sticks

For each chapter:

1. **Read** the chapter — no code yet.
2. **Code** the example — type it; don't paste.
3. **Experiment** — change one thing. Predict the outcome. Run. Were you right?
4. **Build** — apply it to a tiny problem of your own (the bridge projects are the suggested form).
5. **Write** — 2–3 sentences: "what was the single biggest 'oh' moment?"

Skipping step 3 (experiment) and step 5 (write) is the most common way learners plateau. Don't.

## Beyond the course

After Phase 5 + a capstone, you have the working knowledge of a junior LLM engineer. Next:

- **Read papers.** [Transformer](https://arxiv.org/abs/1706.03762), BERT, GPT-2, T5, Llama 3, Mixtral, DeepSeek-V3, DeepSeek R1.
- **Follow the [HF blog](https://huggingface.co/blog).**
- **Pick a vertical.** Legal, medical, code, scientific, creative — generalist LLM knowledge is now a commodity; applied expertise in a domain isn't.
- **Ship in public.** One Space, one model, one post.
- **Contribute.** Small PR to `transformers` or `datasets`. Maintainers are friendly.

The field moves fast — what you learn here stays 80% relevant in 2 years. The remaining 20% is the ability to learn, which the course quietly trains. That part doesn't expire.

Good luck. Build something.
