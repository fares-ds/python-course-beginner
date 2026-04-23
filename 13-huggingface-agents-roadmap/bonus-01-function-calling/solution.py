# Bonus 1 — LoRA fine-tune a 0.5B model on function-calling examples.
# Needs GPU. ~30 min on Colab T4.

from datasets import load_dataset
from peft import LoraConfig, get_peft_model
from transformers import AutoModelForCausalLM, AutoTokenizer
from trl import SFTConfig, SFTTrainer

BASE_MODEL = "Qwen/Qwen2.5-0.5B-Instruct"
OUTPUT_DIR = "xlam-lora"


def to_chat(example):
    """xlam-function-calling-60k has 'query', 'tools', 'answers' columns.
    Format as a chat conversation the model can learn from."""
    return {
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a function-calling assistant. Available tools:\n"
                    f"{example['tools']}\n"
                    "Respond with a JSON list of tool calls."
                ),
            },
            {"role": "user", "content": example["query"]},
            {"role": "assistant", "content": example["answers"]},
        ]
    }


def main():
    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)
    model = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL,
        torch_dtype="auto",
        device_map="auto",
    )

    # LoRA — train only the adapters.
    lora = LoraConfig(
        r=16,
        lora_alpha=32,
        lora_dropout=0.05,
        target_modules="all-linear",
        task_type="CAUSAL_LM",
    )
    model = get_peft_model(model, lora)
    model.print_trainable_parameters()

    raw = load_dataset("Salesforce/xlam-function-calling-60k", split="train[:1000]")
    dataset = raw.map(to_chat, remove_columns=raw.column_names)

    args = SFTConfig(
        output_dir=OUTPUT_DIR,
        num_train_epochs=1,
        per_device_train_batch_size=4,
        gradient_accumulation_steps=4,
        learning_rate=2e-4,
        logging_steps=20,
        save_strategy="epoch",
        bf16=True,
        report_to="none",
        max_seq_length=1024,
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
    print(f"\nAdapter saved to {OUTPUT_DIR}/. Load with peft.PeftModel.from_pretrained(...)")


if __name__ == "__main__":
    main()
