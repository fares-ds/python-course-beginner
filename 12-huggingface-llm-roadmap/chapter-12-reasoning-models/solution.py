# Chapter 12 — tiny GRPO demo on arithmetic questions.
#
# Teaches a small model to answer "What is A + B?" correctly, via RL.
# Needs a GPU; takes 30-60 min on a T4. This is toy-scale — just enough
# to see GRPO run end-to-end. DeepSeek R1 used billions of examples.

import random
import re

from datasets import Dataset
from transformers import AutoModelForCausalLM, AutoTokenizer
from trl import GRPOConfig, GRPOTrainer

BASE_MODEL = "Qwen/Qwen2.5-0.5B-Instruct"
OUTPUT_DIR = "qwen-arith-grpo"


def make_arithmetic_dataset(n=200, seed=42):
    rng = random.Random(seed)
    rows = []
    for _ in range(n):
        a, b = rng.randint(1, 50), rng.randint(1, 50)
        rows.append({
            "prompt": f"What is {a} + {b}? Answer with just the number.",
            "answer": str(a + b),
        })
    return Dataset.from_list(rows)


def reward_correct_answer(completions, answer, **kwargs):
    """The whole job. 1.0 if the completion contains the right number, else 0.0.
    (A real reward function would penalize length, reward reasoning, etc.)"""
    rewards = []
    for comp, ans in zip(completions, answer):
        # Grab the first integer in the completion.
        match = re.search(r"-?\d+", comp)
        predicted = match.group(0) if match else ""
        rewards.append(1.0 if predicted == ans else 0.0)
    return rewards


def main():
    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)
    model = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL,
        torch_dtype="auto",
        device_map="auto",
    )

    dataset = make_arithmetic_dataset(n=200)
    print(f"Dataset: {len(dataset)} prompts. Sample:")
    print(f"  {dataset[0]}\n")

    # GRPO config — G=4 means generate 4 completions per prompt, pick per-group.
    config = GRPOConfig(
        output_dir=OUTPUT_DIR,
        num_train_epochs=1,
        per_device_train_batch_size=4,
        gradient_accumulation_steps=2,
        num_generations=4,
        max_prompt_length=64,
        max_completion_length=32,
        learning_rate=1e-5,
        logging_steps=10,
        save_strategy="no",
        bf16=True,
        report_to="none",
    )

    trainer = GRPOTrainer(
        model=model,
        args=config,
        train_dataset=dataset,
        tokenizer=tokenizer,
        reward_funcs=reward_correct_answer,
    )

    # Quick "before" probe.
    probe_prompts = ["What is 7 + 9? Answer with just the number.",
                     "What is 23 + 45? Answer with just the number."]

    def generate(prompt):
        messages = [{"role": "user", "content": prompt}]
        inputs = tokenizer.apply_chat_template(messages, return_tensors="pt",
                                               add_generation_prompt=True).to(model.device)
        out = model.generate(inputs, max_new_tokens=30, do_sample=False)
        return tokenizer.decode(out[0][inputs.shape[1]:], skip_special_tokens=True).strip()

    print("BEFORE training:")
    for p in probe_prompts:
        print(f"  Q: {p}\n  A: {generate(p)}\n")

    trainer.train()

    print("AFTER training:")
    for p in probe_prompts:
        print(f"  Q: {p}\n  A: {generate(p)}\n")


if __name__ == "__main__":
    main()
