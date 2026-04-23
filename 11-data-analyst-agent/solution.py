# Data Analyst Agent — your first project with PandasAI.
#
# Load a CSV of top Spotify songs, then ask questions about it in plain English.
# The questions go to a local language model (running on your own machine via
# Ollama), which writes pandas code, runs it, and gives you the answer back.
#
# The shape of the program:
#   1. Configure PandasAI to talk to a local Ollama model.
#   2. Load the CSV with pandas, then wrap it as a PandasAI dataframe.
#   3. Run a guided demo of 5 questions of escalating complexity.
#   4. Drop the user into a REPL where they can ask their own questions.
#
# Before running:
#   - Python 3.11 (PandasAI v3 does not support 3.12+ yet)
#   - Ollama installed and `ollama pull qwen2.5-coder:7b` done
#   - pip install -r requirements.txt
#   - cp .env.example .env

import os

import pandas as pd
import pandasai as pai
from pandasai import Agent
from pandasai_litellm import LiteLLM
from dotenv import load_dotenv

DATA_PATH = "data/spotify_top_songs.csv"
DEFAULT_MODEL = "qwen2.5-coder:7b"
DEFAULT_BASE_URL = "http://localhost:11434"

# The 5 walkthrough questions, in order of escalating difficulty.
# Each one teaches a new capability — see README.md section "Five questions".
DEMO_QUESTIONS = [
    "How many songs are in the dataset?",
    "What is the average bpm of songs in the 'dance pop' genre?",
    "Which 5 artists have the most songs in the dataset?",
    "Plot a histogram of song popularity scores and save it as 'pop_hist.png'.",
    "Among the 50 most popular songs, which genre appears most often, "
    "and what is the average danceability of songs in that genre?",
]


def build_llm():
    # Read model name + Ollama URL from .env, falling back to sensible defaults.
    # The "ollama/" prefix tells LiteLLM to route this through Ollama's API.
    model = os.getenv("OLLAMA_MODEL", DEFAULT_MODEL)
    base_url = os.getenv("OLLAMA_BASE_URL", DEFAULT_BASE_URL)
    return LiteLLM(model=f"ollama/{model}", api_base=base_url)


def load_data():
    # The CSV has an unnamed index column at position 0 — drop it on read so
    # the dataframe is clean. Then wrap it as a PandasAI dataframe so we can
    # call .chat() on it.
    raw = pd.read_csv(DATA_PATH, index_col=0)
    print(f"Loaded {len(raw)} rows. Columns:")
    for col in raw.columns:
        print(f"  - {col}")
    print()
    print("First 3 rows:")
    print(raw.head(3))
    print()
    return pai.DataFrame(raw)


def run_demo(df):
    print("=" * 60)
    print("DEMO: 5 questions, 5 capabilities")
    print("=" * 60)
    for i, question in enumerate(DEMO_QUESTIONS, start=1):
        print(f"\n[{i}/5] Q: {question}")
        try:
            answer = df.chat(question)
            print(f"      A: {answer}")
        except Exception as e:
            # Don't crash the whole demo if one question fails — just show
            # the error and move on. (Local models occasionally produce
            # broken code; the README "Debugging" section explains why.)
            print(f"      ERROR: {e}")


def run_repl(agent):
    print()
    print("=" * 60)
    print("Your turn. Ask the agent anything about the data.")
    print("Type 'quit' or press Ctrl+C to exit.")
    print("=" * 60)
    while True:
        try:
            question = input("\nAsk a question: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            return
        if question == "" or question.lower() in ("quit", "exit"):
            print("Bye!")
            return
        try:
            answer = agent.chat(question)
            print(f"-> {answer}")
        except Exception as e:
            # Same as in the demo — print the error so the user can read it,
            # then loop back for the next question.
            print(f"-> ERROR: {e}")


def main():
    load_dotenv()
    pai.config.set({"llm": build_llm()})

    df = load_data()
    run_demo(df)

    # An Agent remembers previous questions, so you can ask follow-ups like
    # "what about for the next 50?" without repeating the full context.
    agent = Agent([df])
    run_repl(agent)


if __name__ == "__main__":
    main()
