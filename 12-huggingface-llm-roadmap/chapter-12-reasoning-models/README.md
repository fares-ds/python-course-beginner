# Chapter 12 — Build Reasoning Models

The most cutting-edge chapter — and the most optional. Walks through the DeepSeek R1 recipe: using reinforcement learning (GRPO) to teach an LLM to "think out loud" before answering.

**Course link:** [Chapter 12 on the HF docs](https://huggingface.co/learn/llm-course/en/chapter12/1)

## What you'll learn

- **RL on LLMs** in plain English — training on (prompt, output, reward) triples instead of (prompt, ideal-answer) pairs.
- **GRPO** (Group Relative Policy Optimization) — the simpler alternative to PPO that DeepSeek R1 used.
- **The "aha moment"** — what the DeepSeek paper showed about emergent reasoning.
- How to implement GRPO in `trl`, optionally accelerated with `unsloth`.

## What's in this folder

- [`solution.py`](solution.py) — a *tiny* GRPO demo: fine-tune a 0.5B model on arithmetic questions, rewarding correct answers. Not production; just enough to see GRPO actually run.
- [`requirements.txt`](requirements.txt) — `trl`, `transformers`, `peft`, `datasets`.

## Setup

```bash
pip install -r requirements.txt
```

**GPU required.** GRPO is ~3× slower than SFT because it generates multiple completions per example.

## Run it

```bash
python3 solution.py
```

Expected: the script generates a toy arithmetic dataset (`"What is 3 + 5?"` → `"8"`), trains via GRPO with a simple reward (`1.0` if the answer is correct, `0.0` otherwise), and shows before/after generations. Takes ~30–60 min on a T4 even with the tiny setup.

## Key concepts

### Why RL, not SFT?
SFT shows the model the right answer, once per example. If the right answer requires multi-step reasoning, the model learns to *copy the reasoning trace*, not to produce it. RL scores the final answer (or the reasoning) and lets the model explore its own way to produce it. The reasoning that emerges is its own, not copied.

### GRPO in 5 lines of math-ish English
1. For each prompt, generate `G` completions (typically 4–8).
2. Score each one with your reward function.
3. Compute the mean reward across the group.
4. Up-weight completions above the mean, down-weight ones below.
5. Take a gradient step.

No separate "critic" model (unlike PPO). No KL penalty against a separate reference model (DeepSeek did include one, but simpler GRPO works without). Just group-relative.

### The reward function is the whole job
RL is "show me what 'good' looks like, I'll find a way." If your reward function is flawed, the model will **exploit the flaw**, not solve your problem. Spend more time on the reward function than on the model.

### The aha moment
DeepSeek R1's [paper](https://arxiv.org/abs/2501.12948) showed that with a simple reward (correctness) and GRPO, a base model can **discover** chain-of-thought reasoning — it starts writing "Let me think…" and "Wait, that's wrong…" completely on its own. That finding is what this chapter is about.

## Mini-tasks

1. Run `solution.py` to completion. Look at the before/after generations: does the fine-tuned model ever produce longer/more careful reasoning?
2. Modify the reward function: reward shorter correct answers more than longer correct answers. Re-train. Does the model produce terser output?
3. (Optional, if you have a bigger GPU) Replace the arithmetic dataset with GSM8K. Warning: takes hours.

## Focus vs skim

- **Focus:** sections 1, 2, 3 conceptually. Read the DeepSeek R1 paper — it's very readable.
- **Skim:** sections 4–6 (practical exercises) unless you have a GPU you can leave running. The conceptual understanding is the main win.

## Common pitfalls

- **Reward hacking** — the model finds a way to maximize your reward without solving the task. Example: reward "output contains the right answer" and the model prints "the answer is 1 2 3 4 5 6 7 8 9". Always cap, penalize long outputs, or use composite rewards.
- **Compute cost** — GRPO generates `G` completions per example. That's `G`× the compute of SFT. Budget accordingly.
- **Skipping KL control on bigger runs** — without a KL penalty against the original model, the model can drift far from its pretrained distribution and become incoherent. For serious runs, add `beta=0.04` (KL coefficient) as DeepSeek did.

## Expected outcome

You can read the DeepSeek R1 paper without being lost. You know when to reach for RL (multi-step problems where correctness is easy to score) and when not to (open-ended text — harder to score, SFT usually wins).

## Next

You're done with the course. Go back to the [parent project README](../README.md) and pick a capstone project.
