# Chapter 9 — sentiment analysis as a Gradio web app (Interface style).
#
# After `python3 solution.py`, open http://127.0.0.1:7860 in your browser.

import gradio as gr
from transformers import pipeline

# Load ONCE at startup — not per-request.
classifier = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english",
)


def analyze(text: str) -> dict:
    """Returns {label: score} pairs for all classes, not just the top."""
    results = classifier(text, top_k=None)  # top_k=None returns all classes
    return {r["label"]: float(r["score"]) for r in results}


demo = gr.Interface(
    fn=analyze,
    inputs=gr.Textbox(
        label="Text",
        placeholder="Type a sentence...",
        lines=3,
    ),
    outputs=gr.Label(num_top_classes=2, label="Sentiment"),
    title="Sentiment Analyzer",
    description="Fine-tuned DistilBERT on SST-2. Works best on short English text.",
    examples=[
        "I absolutely loved the movie.",
        "The food was cold and the service was slow.",
        "It's fine, I guess.",
    ],
)


if __name__ == "__main__":
    demo.launch()
