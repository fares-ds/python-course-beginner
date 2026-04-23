# Chapter 4 — push a local fine-tuned model to the Hugging Face Hub.
#
# Assumes:
#   - you ran Chapter 3 and have a ./mrpc-distilbert-finetuned/ dir, OR
#   - you have some other local dir with a model + tokenizer + config
#   - you ran: huggingface-cli login  (with a WRITE-scope token)
#
# The script loads the local model, reads a model-card template, and
# pushes everything to huggingface.co/<your-username>/<repo-name>.

from pathlib import Path

from huggingface_hub import HfApi
from transformers import AutoModelForSequenceClassification, AutoTokenizer

DEFAULT_LOCAL_DIR = "../chapter-03-fine-tuning/mrpc-distilbert-finetuned"
CARD_TEMPLATE = "model_card_template.md"


def main():
    # 1. Confirm who we are on the Hub.
    api = HfApi()
    try:
        username = api.whoami()["name"]
    except Exception as e:
        raise SystemExit(
            "Not logged in. Run: huggingface-cli login (need WRITE scope)"
        ) from e
    print(f"Logged in as: {username}")

    # 2. Ask where the local model is and what to name the repo.
    local_dir = input(f"Local model dir [{DEFAULT_LOCAL_DIR}]: ").strip() or DEFAULT_LOCAL_DIR
    default_name = Path(local_dir).name
    repo_name = input(f"Repo name [{default_name}]: ").strip() or default_name
    repo_id = f"{username}/{repo_name}"

    if not Path(local_dir).exists():
        raise SystemExit(f"{local_dir} does not exist. Train Chapter 3 first.")

    # 3. Load the model + tokenizer from disk (sanity check they're valid).
    model = AutoModelForSequenceClassification.from_pretrained(local_dir)
    tokenizer = AutoTokenizer.from_pretrained(local_dir)

    # 4. Create the repo (idempotent — safe to re-run).
    api.create_repo(repo_id, exist_ok=True, private=False)

    # 5. Push model + tokenizer.
    print(f"Pushing model to {repo_id}...")
    model.push_to_hub(repo_id)
    tokenizer.push_to_hub(repo_id)

    # 6. Upload the model card.
    card_path = Path(CARD_TEMPLATE)
    if card_path.exists():
        api.upload_file(
            path_or_fileobj=str(card_path),
            path_in_repo="README.md",
            repo_id=repo_id,
        )
        print("Uploaded model card (README.md).")
    else:
        print(f"WARNING: {CARD_TEMPLATE} not found — model card not uploaded.")

    print(f"\nDone. Visit: https://huggingface.co/{repo_id}")


if __name__ == "__main__":
    main()
