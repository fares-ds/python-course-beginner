# Unit 0 — confirm you're logged in to the Hugging Face Hub.
#
# Run:
#   pip install -r requirements.txt
#   huggingface-cli login
#   python3 solution.py


def main():
    print("=" * 60)
    print("Unit 0 — login check")
    print("=" * 60)

    try:
        from huggingface_hub import HfApi
    except ImportError:
        raise SystemExit("huggingface_hub not installed. Run: pip install -r requirements.txt")

    try:
        info = HfApi().whoami()
        print(f"  Logged in as: {info['name']}")
        print(f"  Email:        {info.get('email', '(not visible)')}")
        print(f"  Token type:   {info.get('auth', {}).get('accessToken', {}).get('role', 'unknown')}")
    except Exception as e:
        raise SystemExit(
            f"Not logged in. Run: huggingface-cli login\n"
            f"Detail: {e}"
        )

    print()
    print("Ready for Unit 1 — Introduction to Agents.")


if __name__ == "__main__":
    main()
