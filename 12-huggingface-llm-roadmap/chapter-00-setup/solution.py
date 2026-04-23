# Chapter 0 — Setup verification.
#
# Prints your Python version, key library versions, and (if you're logged
# in) your Hugging Face username. If everything prints with no exceptions,
# you're ready for Chapter 1.
#
# Run:
#   pip install -r requirements.txt
#   python3 solution.py

import platform
import sys


def report_python():
    print(f"Python:        {platform.python_version()}  ({sys.executable})")
    major, minor = sys.version_info[:2]
    if not (3, 9) <= (major, minor) <= (3, 11):
        print(f"  WARNING: course examples target Python 3.9-3.11; you have {major}.{minor}.")


def report_libraries():
    try:
        import transformers
        print(f"transformers:  {transformers.__version__}")
    except ImportError:
        print("transformers:  NOT INSTALLED — run: pip install -r requirements.txt")

    try:
        import huggingface_hub
        print(f"huggingface_hub: {huggingface_hub.__version__}")
    except ImportError:
        print("huggingface_hub: NOT INSTALLED")


def report_hf_login():
    try:
        from huggingface_hub import HfApi
    except ImportError:
        return
    try:
        # whoami() reads the token saved by `huggingface-cli login`.
        info = HfApi().whoami()
        print(f"HF user:       {info['name']}  (logged in)")
    except Exception:
        # No token, or token invalid — not fatal for Chapter 0, but you
        # need it for Chapter 4 onward.
        print("HF user:       NOT LOGGED IN — run: huggingface-cli login")


def main():
    print("=" * 60)
    print("Chapter 0 — environment check")
    print("=" * 60)
    report_python()
    report_libraries()
    report_hf_login()
    print()
    print("If nothing above says NOT INSTALLED, you're ready for Chapter 1.")


if __name__ == "__main__":
    main()
