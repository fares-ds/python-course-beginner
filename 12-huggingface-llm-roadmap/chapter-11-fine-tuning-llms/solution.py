# Chapter 11 — LoRA fine-tune Qwen2.5-0.5B-Instruct on Alpaca instructions.
#
# Needs a GPU (~12 GB VRAM). Free Colab T4 is enough.
# Full run: ~1 hour for 1000 examples, 1 epoch.

from datasets import load_dataset
from peft import LoraConfig, get_peft_model
from transformers import AutoModelForCausalLM, AutoTokenizer
from trl import SFTConfig, SFTTrainer

BASE_MODEL = "Qwen/Qwen2.5-0.5B-Instruct"
OUTPUT_DIR = "qwen-alpaca-lora"


def format_example(example):
    """Alpaca rows are (instruction, input, output). Turn them into chat messages."""
    user_content = example["instruction"]
    if example.get("input"):
        user_content += f"\n\n{example['input']}"
    return {
        "messages": [
            {"role": "user", "content": user_content},
            {"role": "assistant", "content": example["output"]},
        ]
    }


def main():
    # 1. Load the base model + tokenizer.
    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)
    model = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL,
        torch_dtype="auto",
        device_map="auto",
    )

    # 2. Attach LoRA adapters to the attention layers.
    lora = LoraConfig(
        r=16,
        lora_alpha=32,
        lora_dropout=0.05,
        bias="none",
        target_modules="all-linear",
        task_type="CAUSAL_LM",
    )
    model = get_peft_model(model, lora)
    model.print_trainable_parameters()   # shows ~0.5% trainable

    # 3. Load a small slice of Alpaca and format it into chat messages.
    raw = load_dataset("tatsu-lab/alpaca", split="train[:1000]")
    dataset = raw.map(format_example, remove_columns=raw.column_names)

    # 4. Train.
    args = SFTConfig(
        output_dir=OUTPUT_DIR,
        num_train_epochs=1,
        per_device_train_batch_size=4,
        gradient_accumulation_steps=4,
        learning_rate=2e-4,                # LoRA tolerates higher LR than full FT
        logging_steps=20,
        save_strategy="epoch",
        bf16=True,                         # use bf16 if your GPU supports it; else fp16=True
        report_to="none",
        max_seq_length=512,
        seed=42,
    )

    trainer = SFTTrainer(
        model=model,
        args=args,
        train_dataset=dataset,
        tokenizer=tokenizer,
    )
    trainer.train()
    trainer.save_model(OUTPUT_DIR)
    print(f"\nAdapter saved to {OUTPUT_DIR}/ (just ~10 MB — the base model stays untouched)")

    # 5. Quick sanity-check generation.
    model.eval()
    for prompt in [
        "Explain gravity in one sentence.",
        "Give me three names for a coffee shop.",
        "How do I boil an egg?",
    ]:
        messages = [{"role": "user", "content": prompt}]
        inputs = tokenizer.apply_chat_template(
            messages, return_tensors="pt", add_generation_prompt=True
        ).to(model.device)
        out = model.generate(inputs, max_new_tokens=80, do_sample=False)
        text = tokenizer.decode(out[0][inputs.shape[1]:], skip_special_tokens=True)
        print(f"\nQ: {prompt}\nA: {text.strip()}")


if __name__ == "__main__":
    main()
