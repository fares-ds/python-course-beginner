# Unit 4 — Final Project: Build a GAIA Agent

The capstone. Build an agent that scores on the GAIA benchmark, submit it to the leaderboard, earn the **Certificate of Excellence**.

**Course link:** [Unit 4 on the HF docs](https://huggingface.co/learn/agents-course/unit4/introduction)

> **🎓 Certificate of Excellence:** complete this unit + Unit 1 + a use-case assignment to earn it. Free.

## What you'll learn

- **GAIA** — a real-world agent benchmark. Multi-step questions like "find the youngest American actress to win an Oscar in the last decade and tell me her birth city's population." See the [GAIA paper](https://arxiv.org/abs/2311.12983).
- **The leaderboard** — where your scored agent shows up alongside other students.
- **Iteration discipline** — read traces, identify failure modes, change one thing, re-score.

## What's in this folder

- [`solution.py`](solution.py) — a starter GAIA agent. smolagents `CodeAgent` + DuckDuckGo + Python interpreter. Runs on a GAIA-style sample question.
- [`requirements.txt`](requirements.txt) — `smolagents` with the search extra.

## Setup

```bash
pip install -r requirements.txt
huggingface-cli login
```

## Run it

```bash
python3 solution.py
```

Expected: the agent runs on a sample GAIA-style question. You'll see its trace as it searches, computes, and arrives at an answer.

To submit to the real GAIA leaderboard, follow the official Unit 4 instructions on the HF site — they include the submission script and the validation set.

## Key concepts

### What makes GAIA hard
Each question is **multi-step** and **adversarially designed** to break naive agents. Examples:

- "What's the average rainfall in the city where the inventor of the World Wide Web was born?"
   → needs: knowledge (TimBerners-Lee, born in London) + retrieval (London rainfall stats) + arithmetic (average).
- "Of the films Christopher Nolan directed before 2010, which one had the smallest opening-weekend box office?"
   → needs: filmography lookup + financial data + filter + min.

A vanilla "ask the LLM" approach fails. So does a vanilla "ask the LLM with web search." You need *iterative* retrieval, code execution for math, and the ability to abandon a wrong path.

### Iteration loop
For every wrong answer:

1. Read the agent's trace top-to-bottom. Where did it go wrong?
2. Was it: bad search query? Bad parsing of the result? Bad arithmetic? Premature termination?
3. Fix one thing — usually a tool description, a system prompt, or adding a missing tool.
4. Re-run on the sample. Then re-run on the validation set.

Don't change five things at once. You won't know what helped.

### Tool budget
GAIA-scoring agents typically have:

- **Web search** (DuckDuckGo, Tavily, Serper)
- **Python interpreter** (for arithmetic, parsing, JSON manipulation)
- **File reader** (for PDF/Excel attachments — yes, GAIA includes those)
- **Vision** (for image-attachment questions)
- **A "submit final answer" tool** (so the agent has a clear stop signal)

## Mini-tasks

1. Run `solution.py`. Read the trace. Did it succeed? If not, where did it go off?
2. Open the official GAIA validation set notebook from the course. Run on 3 questions. What's your accuracy?
3. Add one new tool (e.g., a Wikipedia summary fetcher). Re-run the same 3 questions. Did accuracy go up?
4. (Stretch) Submit to the leaderboard. See where you land.

## Focus vs skim

- **Focus:** "What is GAIA?" (read the paper if you have time), "The Final Hands-On" (the rubric).
- **Skim:** none. The unit is small.

## Common pitfalls

- **Starting from zero** — the official course provides starter code. Use it. Don't build from scratch.
- **Only running on the sample** — the sample is easy. The validation set is harder. The real leaderboard set is hardest. Test broadly.
- **Optimizing for the leaderboard, not the trace** — chasing one wrong answer to get +1 score teaches less than fixing a systemic failure mode that's costing you 10.
- **No retrieval evaluation** — when an answer is wrong, half the time it's because the retrieval was wrong. Log the retrieved context and audit it.

## Expected outcome

A leaderboard-listed agent + the **Certificate of Excellence**. More importantly: real reps reading agent traces and iterating on prompts/tools — the actual job description of an "AI engineer" in 2026.

## Next

You've finished the main course. The bonus units are optional — pick one if you have appetite.

→ [Bonus 1 — Function-calling fine-tuning](../bonus-01-function-calling/) | [Bonus 2 — Observability](../bonus-02-observability/) | [Bonus 3 — Pokemon agents](../bonus-03-pokemon-agent/)
