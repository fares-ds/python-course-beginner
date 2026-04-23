# Chapter 10 — push a sample into Argilla, label it, pull it back.
#
# Assumes you have an Argilla server running (local Docker or HF Space).
# Set ARGILLA_API_URL and ARGILLA_API_KEY env vars first.
#
# Usage:
#   python3 solution.py            # push 20 IMDb records to Argilla
#   python3 solution.py --export   # pull labeled records back

import os
import sys

import argilla as rg
from datasets import load_dataset

DATASET_NAME = "imdb-demo"
WORKSPACE = "argilla"  # the default workspace


def connect():
    url = os.getenv("ARGILLA_API_URL")
    key = os.getenv("ARGILLA_API_KEY")
    if not (url and key):
        raise SystemExit("Set ARGILLA_API_URL and ARGILLA_API_KEY env vars.")
    return rg.Argilla(api_url=url, api_key=key)


def push(client):
    raw = load_dataset("imdb", split="train").shuffle(seed=42).select(range(20))

    settings = rg.Settings(
        guidelines="Is this movie review positive or negative?",
        fields=[rg.TextField(name="review")],
        questions=[
            rg.LabelQuestion(
                name="sentiment",
                labels=["positive", "negative"],
                title="What's the sentiment of this review?",
            ),
        ],
    )

    # Delete any previous version, then create fresh.
    try:
        client.datasets(DATASET_NAME, workspace=WORKSPACE).delete()
    except Exception:
        pass

    dataset = rg.Dataset(name=DATASET_NAME, workspace=WORKSPACE, settings=settings)
    dataset.create()

    records = [
        rg.Record(fields={"review": ex["text"][:1000]})   # truncate for display
        for ex in raw
    ]
    dataset.records.log(records)
    print(f"Pushed {len(records)} records to Argilla dataset '{DATASET_NAME}'.")
    print(f"Open: {os.getenv('ARGILLA_API_URL')} and label them.")


def export(client):
    dataset = client.datasets(DATASET_NAME, workspace=WORKSPACE)
    labeled = list(dataset.records)
    print(f"Pulled {len(labeled)} records from Argilla.")
    labeled_count = sum(1 for r in labeled if r.responses)
    print(f"  {labeled_count} have been labeled.")
    # In a real workflow you'd convert to a HF dataset here and push it
    # to the Hub. For the demo we just print the first few.
    for r in labeled[:3]:
        print(f"  - responses: {[(resp.question_name, resp.value) for resp in r.responses]}")


def main():
    client = connect()
    if "--export" in sys.argv:
        export(client)
    else:
        push(client)


if __name__ == "__main__":
    main()
