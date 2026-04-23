# Project 14 — DSPy Roadmap

A structured 4–6 week plan for learning [DSPy](https://dspy.ai/) — Stanford's framework for **programming** (rather than prompting) language models. One sub-folder per major concept, each with its own runnable demo.

DSPy doesn't have a numbered "course" the way Hugging Face does — it's a library with three pillars (Programming, Evaluation, Optimization) plus tutorials and production guides. So sub-folders are organized by **DSPy concept**, not chapter, but follow the same per-folder shape as projects 12 and 13: `README.md` + `solution.py` + `requirements.txt`.

> **The DSPy pitch in one paragraph:** instead of writing prompts as strings, you write *typed signatures* (`"question -> answer"`) and *modules* (`Predict`, `ChainOfThought`, `ReAct`). DSPy compiles those into prompts. Then *optimizers* (`BootstrapFewShot`, `MIPROv2`, `GEPA`) automatically search over instructions and few-shot demos to find prompts that score better on **your** evaluation set. The result: programs that improve when you add data, not when you hand-tune strings.

## Folders

| # | Folder | Phase |
|---|--------|-------|
| 01 | [Setup & Language Models](01-setup-and-language-models/) | Programming basics |
| 02 | [Signatures](02-signatures/) | Programming basics |
| 03 | [Modules: Predict, ChainOfThought](03-modules-basics/) | Programming basics |
| 04 | [Modules: ReAct, ProgramOfThought](04-modules-agentic/) | Programming basics |
| 05 | [Tools & MCP](05-tools-and-mcp/) | Tools and RAG |
| 06 | [RAG Pipeline](06-rag-pipeline/) | Tools and RAG |
| 07 | [Data & Examples](07-data-and-examples/) | Evaluation |
| 08 | [Metrics](08-metrics/) | Evaluation |
| 09 | [Optimizer: BootstrapFewShot](09-optimizer-bootstrap/) | Optimization |
| 10 | [Optimizer: MIPROv2](10-optimizer-mipro/) | Optimization |
| 11 | [Optimizer: GEPA](11-optimizer-gepa/) | Optimization |
| 12 | [Optimizer: BootstrapFinetune](12-optimizer-finetune/) | Optimization |
| 13 | [Saving & Deployment](13-saving-and-deployment/) | Production |
| 14 | [Observability](14-observability/) | Production |

## Start here

```bash
cd 01-setup-and-language-models
pip install -r requirements.txt
ollama pull qwen2.5-coder:7b   # if you haven't yet (Project 11 also uses this)
python3 solution.py
```

If the smoke test prints an answer to "What is the capital of France?", you're ready for folder 02.

## Prerequisites

| You need | Why | If you're missing it |
|---|---|---|
| **Python 3.10+** | DSPy requires it | Upgrade from python.org |
| **Basic Python comfort** — functions, classes, type hints, venvs | DSPy uses class signatures with type hints heavily | Do projects 1–10 in this repo |
| **Basic LLM intuition** — what a chat template is, what tokenization does | Folder 02 won't make sense without it | Phase 1 of [Project 12](../12-huggingface-llm-roadmap/) |
| **Basic agent intuition** — what "tool use" and "Thought-Action-Observation" mean | Folders 04 and 05 reference this | Phase 1 of [Project 13](../13-huggingface-agents-roadmap/) |

**Optional but useful:** the LiteLLM docs (DSPy uses LiteLLM under the hood for model routing).

## The five phases

| Phase | Folders | Theme | Outcome |
|---|---|---|---|
| **1. Programming basics** | 01–04 | Signatures, Modules, agentic Modules | Write a working DSPy program |
| **2. Tools and RAG** | 05–06 | External tools, custom Module composition | A RAG pipeline you wrote yourself |
| **3. Evaluation** | 07–08 | Examples, metrics, LM-as-judge | A measurable program |
| **4. Optimization** | 09–12 | The headline feature: optimizers tune your prompts (and weights) automatically | A compiled program that scores better than you'd write by hand |
| **5. Production** | 13–14 | Save / load / serve / observe | A program you can ship |

For the **shortest viable path**: do folders 01, 02, 03, 07, 08, 09. Six folders, ~1 week, you'll have written a DSPy program, evaluated it, and watched an optimizer improve it. That's the minimum to claim "I know DSPy."

## Tooling setup

### Python + Ollama
DSPy needs Python 3.10+. We default to local Ollama (no API key, fully offline):

```bash
ollama --version             # if missing: install from ollama.com
ollama pull qwen2.5-coder:7b # ~4 GB, one-time. Already pulled if you did Project 11.
ollama serve                 # usually auto-started by the Ollama app
```

### DSPy
Per-folder `requirements.txt` files install only what each folder needs. The universal pin is `dspy>=3.0,<4.0`.

### When to switch off Ollama
The optimizer folders (09–11) make many LLM calls. With a 7B local model, expect 30–60+ minutes for a single run. If you want faster iteration, swap one line:

```python
# Replace this:
lm = dspy.LM("ollama_chat/qwen2.5-coder:7b", api_base="http://localhost:11434")

# With one of:
lm = dspy.LM("openai/gpt-4o-mini")                              # paid, fastest
lm = dspy.LM("anthropic/claude-haiku-4-5")                      # paid
lm = dspy.LM("huggingface/Qwen/Qwen2.5-72B-Instruct")           # free with HF token, rate-limited
```

The rest of the program is unchanged. That's a DSPy strength: model-agnostic.

---

## Deep understanding layer

### What DSPy actually is
A framework where:

- **Programs are objects** (subclasses of `dspy.Module`), not strings.
- Each Module has a typed **signature** (input fields → output fields).
- Modules can be composed (a Module's `forward` can call other Modules).
- **Optimizers** search over the space of (instructions × demos × sometimes weights) to maximize a metric you choose.

The slogan: "compile, don't write." You write the *structure* of the program once; an optimizer fills in the prompt details.

### Why this matters
Hand-tuning prompts is slow, brittle, and unreproducible. The same prompt that works on GPT-4 fails on Llama-3.2. The same prompt that works today regresses next month when a model is retrained.

DSPy moves the "what's a good prompt" decision from "the human writes a string" to "the optimizer searches against a metric." When the model changes, you re-compile. When you add training data, you re-compile. The program code doesn't change.

### How DSPy compares to projects 12 and 13

| | Project 12 (HF Transformers) | Project 13 (Agent frameworks) | Project 14 (DSPy) |
|---|---|---|---|
| Mental model | Models as objects, fine-tunable | LLM in a loop with tools | Programs as compiled objects, optimizable |
| Writes prompts? | Yes, you do | Yes, you do (chat templates + system prompts) | No — DSPy generates and tunes them |
| Best at | Training and serving open-source models | Building agentic apps fast | Writing apps whose quality improves with data |

You can use all three together: a DSPy program calling fine-tuned HF models, wrapped as a tool inside a smolagents agent. Each project gives you one lens; together they cover the modern LLM stack.

### Optimizer cheatsheet

| Optimizer | Tunes | Best when |
|---|---|---|
| `LabeledFewShot` | Demos (no metric needed) | You have labeled data, want zero-shot improvement |
| `BootstrapFewShot` | Demos (filtered by metric) | First-pass improvement; cheap and fast |
| `MIPROv2` | Instructions + demos jointly | Most production runs; well-studied |
| `GEPA` | Instructions (via reflection) | Hard tasks; limited budget; want fewer LM calls |
| `BootstrapFinetune` | Model weights (via fine-tuning) | Production cost / latency matters; big training set |

**First-pass recipe:** start with `BootstrapFewShot`. If it plateaus, try `MIPROv2(auto="light")`. If you need every percent of accuracy, try `GEPA(auto="medium")`. Reach for `BootstrapFinetune` only when prompt-side options have plateaued.

---

## Five capstone projects

Pick one after Phase 5.

### A — Beginner: "DSPy Q&A bot for your domain" (1 weekend)
- Build a `ChainOfThought` Q&A program. Hand-curate 30 (question, answer) examples for a topic you care about. Compile with `BootstrapFewShot`. Compare uncompiled vs compiled accuracy on a held-out 10 examples.
- **Why:** the smallest end-to-end DSPy story.

### B — Intermediate: "Optimized RAG over your docs" (1 week)
- Take folder 06's RAG, plug in real docs (your notes, a textbook, a project's docs). Hand-write 20 (question, answer) pairs. Compile with `MIPROv2`. Show that the compiled program beats the unoptimized one on your dev set.
- **Why:** the most common production DSPy use case.

### C — Intermediate: "Multi-step reasoning with PoT + ReAct" (1 week)
- Hard math word problems. Build a `ReAct` agent with a calculator and `ProgramOfThought` as a fallback. Use GSM8K as the dataset. Compile with `GEPA`. Compare to the un-tuned agent.
- **Why:** real reasoning task; great showcase for the optimizer.

### D — Advanced: "Customer-support classifier, fine-tuned" (2 weeks)
- Take a labeled customer-support dataset (or scrape Hacker News). Build a multi-output classifier (intent + sentiment + urgency). Compile with `MIPROv2`, then use `BootstrapFinetune` to distill it into a smaller model. Deploy via FastAPI (folder 13). Add MLflow observability (folder 14).
- **Why:** the full DSPy stack from data to served model.

### E — Advanced: "DSPy + smolagents hybrid" (1–2 weeks)
- Use a DSPy-compiled `ChainOfThought` program as the *reasoning core* inside a smolagents `CodeAgent` (Project 13). The DSPy program is wrapped as a tool. The agent decides when to call it.
- **Why:** combines two frameworks; teaches you that DSPy programs are interoperable.

Pick **one**. Polish, ship.

---

## Common pitfalls

1. **Skipping `with_inputs(...)`** — your optimizer treats every example field as input and gets zero signal. Folder 07's #1 pitfall.
2. **Optimizing without a held-out dev set** — you're measuring "did I overfit to this exact data" rather than "did my program get better." Always split.
3. **Bool metric where DSPy wants float** — wrap with `float(...)`.
4. **Running expensive optimizers on Ollama overnight** — fine, but check the partial results; if dev score plateaus early, kill the run.
5. **Reaching for fine-tuning before prompt optimization is plateauing** — fine-tuning is the most expensive thing in DSPy. Almost always, MIPROv2 or GEPA beats a fine-tune you'd run with the same effort.
6. **No observability** — when an optimization fails, you have no idea why. `inspect_history` plus MLflow autolog or Phoenix tracing is the difference between "it works" and "I can prove it works."
7. **Treating compiled programs as set-and-forget** — they should be re-compiled when the underlying model changes. Treat the compiled artifact like a build artifact, not source code.

---

## Learning workflow

For each folder:

1. **Read** the folder's README.
2. **Run** the `solution.py`. Don't paraphrase; type the changes when you experiment.
3. **`inspect_history`** after every run — see what was actually sent to the LM.
4. **Modify** — change one thing (a signature, a metric, a hyperparameter). Predict what will happen. Run. Were you right?
5. **Build** — by folder 09, you should be able to combine signatures + a Module + a metric + an optimizer in one new script of your own.

Skipping step 3 (`inspect_history`) is the most common reason learners stay confused. The framework is small enough to read end-to-end; the prompts it produces are the most important thing to understand.

---

## Beyond the project

- **Read the [GEPA paper](https://arxiv.org/abs/2507.19457)** — practical and short.
- **Read the [DSPy paper](https://arxiv.org/abs/2310.03714)** — for the framework's philosophy.
- **Watch the [DSPy production case studies](https://dspy.ai/community/use-cases/)** — JetBlue, Databricks, etc.
- **Contribute** — DSPy is small enough to read end-to-end. The teleprompt module is where the optimizers live; reading it once will teach you more about prompt engineering than ten blog posts.
- **Combine** — the most interesting projects use DSPy *with* HF (Project 12) or smolagents (Project 13), not against them.

The DSPy bet is that the future of LLM apps is **compiled, not written**. If you've felt the pain of hand-tuning prompts, you'll feel why. If you haven't, do folder 09 and you will.

Good luck. Go compile something.
