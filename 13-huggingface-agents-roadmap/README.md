# Project 13 — Hugging Face Agents Course Roadmap

A structured 6–10 week plan for working through the [Hugging Face Agents Course](https://huggingface.co/learn/agents-course/unit0/introduction) end-to-end. One sub-folder per unit. Each has its own `README.md`, a runnable `solution.py`, and a `requirements.txt`.

The course is **5 main units (0–4)** + **3 sub-units inside Unit 2** (smolagents, LlamaIndex, LangGraph) + **3 bonus units**. HF suggests 3–4 hours per unit per week. This project groups them into **4 phases** with bridge projects between.

## Units

| # | Unit | Phase |
|---|------|-------|
| 0 | [Welcome & Onboarding](unit-00-onboarding/) | Foundations |
| 1 | [Introduction to Agents](unit-01-introduction-to-agents/) **🎓 cert checkpoint** | Foundations |
| 2.1 | [smolagents](unit-02a-smolagents/) | Frameworks |
| 2.2 | [LlamaIndex](unit-02b-llamaindex/) | Frameworks |
| 2.3 | [LangGraph](unit-02c-langgraph/) | Frameworks |
| 3 | [Agentic RAG](unit-03-agentic-rag/) | Real use case |
| 4 | [Final Project — GAIA](unit-04-final-project-gaia/) **🎓 cert of excellence** | Final + certify |
| B1 | [Bonus — Function-calling fine-tune](bonus-01-function-calling/) | Bonus |
| B2 | [Bonus — Observability](bonus-02-observability/) | Bonus |
| B3 | [Bonus — Pokemon agent](bonus-03-pokemon-agent/) | Bonus |

## Start here

```bash
cd unit-00-onboarding
pip install -r requirements.txt
huggingface-cli login
python3 solution.py
```

If it prints your HF username, you're ready. Each unit folder has its own setup (since later units add `smolagents`, `llama-index`, `langgraph`, etc.).

## Prerequisites

| You need | Why | If you're missing it |
|---|---|---|
| **Basic Python** — functions, classes, decorators, type hints, venvs | You'll define tools as decorated Python functions, instantiate agent classes. | Do projects 1–10 in this repo. |
| **Basic LLM intuition** — tokenizer, chat template, "models are non-deterministic" | Unit 1 has a 1-hour LLM recap, but doesn't re-teach from zero. | Do Phase 1 of [Project 12](../12-huggingface-llm-roadmap/) first. |

**Optional but useful:** API/HTTP basics (Project 10), some prompting experience.

## The four phases

| Phase | Weeks | Units | Theme | Bridge project |
|---|---|---|---|---|
| **1. Foundations** | 1 | 0, 1 | What agents are. Build your first one. | Personal helper agent (4 tools, deployed to a Space). |
| **2. Frameworks** | 2–4 | 2.1, 2.2, 2.3 | The three big agent frameworks side by side. | The same task built three different ways + a comparison post. |
| **3. Real use case** | 5 | 3 | Agentic RAG end-to-end. | Agentic RAG over a corpus you actually care about. |
| **4. Final project + certify** | 6–7 | 4 | A GAIA-benchmark agent. | A scored agent on the leaderboard + Certificate of Excellence. |
| **Bonus** | 8–10 | B1 / B2 / B3 | Pick at most one to do well. | One bonus, polished. |

## Tooling setup

### Hugging Face account
The single most important thing. Sign up at [hf.co/join](https://huggingface.co/join), then:

```bash
pip install huggingface_hub
huggingface-cli login   # paste a token from hf.co/settings/tokens
```

You get free access to the HF Inference API for the course's models — no OpenAI/Anthropic key needed for most units.

### Where to run notebooks
- **Browser** (HF Spaces, Colab) for Units 0–2.
- **Local** for Units 3–4 onward.

### LLM provider beyond HF Inference API
When you outgrow free rate limits (typically Phase 3+), pick: OpenAI/Anthropic (paid, fast), local Ollama (free, slow), or Together/Groq/Fireworks (paid, cheap).

---

## Deep understanding layer

### What an "agent" actually is
An LLM in a loop, with tools. The whole pseudocode:

```
state = []
while not done:
    thought = llm(state, available_tools)
    action = parse_tool_call(thought)
    observation = run_tool(action)
    state.append(thought, action, observation)
return final_answer(state)
```

Every framework decorates this loop. Once you understand the loop, switching frameworks is mostly remembering different class names.

### ReAct
"Reasoning + Acting." Ask the LLM to **write down its reasoning before each action**:

> *Thought: I need the weather. I'll call get_weather.*
> *Action: get_weather("Paris")*

Costs a few extra tokens. Pays back in tool-selection accuracy + debuggability + recovery from mistakes.

### Function calling vs code-as-actions

|  | JSON function calling | Code as actions (smolagents `CodeAgent`) |
|---|---|---|
| Output | `{"tool": "f", "args": {...}}` | `result = f(...)` |
| Safety | Sandboxed | Needs a sandbox (smolagents provides one) |
| Expressiveness | One tool per step | Can compose multiple in one block |
| Support | Universal | smolagents only (others on the way) |

### Agentic vs vanilla RAG

|  | Vanilla RAG | Agentic RAG |
|---|---|---|
| Retrievals/query | Always 1 | 0, 1, or N — agent decides |
| Cost | Predictable | Variable |
| When | Simple Q&A on known corpus | Multi-step, comparative, "I'm not sure I have an answer" |

**If vanilla RAG already scores >85% on your eval, don't add agency.**

### When to use which framework

| Framework | Strongest at | Weakest at |
|---|---|---|
| smolagents | Single agents that benefit from code-as-actions | Complex stateful workflows |
| LlamaIndex | Heavy RAG, many data sources | Pure non-RAG workflows |
| LangGraph | Branching workflows, human-in-the-loop | Quick prototypes (more boilerplate) |

If you can't decide: start with **smolagents**.

---

## Five capstone projects

1. **Personal helper agent** — smolagents + 4 tools + Spaces. (Unit 1.)
2. **Agentic RAG over a corpus you care about** — LlamaIndex or smolagents + a vector store + Gradio. (Unit 3.)
3. **Multi-agent newsroom** — researcher / writer / editor. smolagents or LangGraph. (Unit 2.)
4. **GAIA agent** — the official Unit 4 final. Earns the Certificate of Excellence.
5. **Observable, evaluated agent in production** — any of the above + Bonus 2 tooling.

Pick **one**. Polish it. Ship it.

---

## Common pitfalls

1. **Confusing "agent" with "chatbot"** — agents have a loop and tools.
2. **Infinite loops** — set `max_steps`. Always.
3. **Bad tool descriptions** — the docstring is what the LLM reads. Spend time on it.
4. **Cost / latency surprise** — every step is an LLM call. A 5-step agent on 10 questions is 50 calls.
5. **Picking a framework based on hype** — match the framework to the problem shape.
6. **Skipping eval** — write 10–20 (input, expected) pairs *before* iterating. Score every change.
7. **Untrusted code execution** — smolagents has a sandboxed interpreter. Use it. For other frameworks, use `e2b` or Docker.

## Learning workflow

1. **Read** the unit start to finish.
2. **Code** — type the examples; don't paste.
3. **Trace** — read the agent's logs. Every step. **This is the single most important skill in the course.**
4. **Break** — make the agent fail on purpose. Watch how it recovers (or doesn't).
5. **Build** — the bridge project at the end of each phase.
6. **Write** — 2–3 sentences after each unit on what surprised you.

Skipping step 3 (trace-reading) is the most common reason learners plateau.

## Beyond the course

- **Foundational papers**: [ReAct](https://arxiv.org/abs/2210.03629), [Toolformer](https://arxiv.org/abs/2302.04761), [GAIA](https://arxiv.org/abs/2311.12983), [SWE-Agent](https://arxiv.org/abs/2405.15793), [Reflexion](https://arxiv.org/abs/2303.11366).
- **Pick a vertical**: coding agents, browser agents, customer-support agents — generalist agent knowledge is now a commodity.
- **Production observability**: [Langfuse](https://langfuse.com), [Phoenix](https://phoenix.arize.com), [W&B Weave](https://wandb.ai/site/weave).
- **Contribute**: smolagents is small enough to read end-to-end. Add a tool, fix a bug, open a PR.

The agent space moves as fast as anything in AI. The frameworks will evolve, the models will get better at tool use — but **the loop** doesn't change. That's the part that lasts.

Good luck. Build something that does things.
