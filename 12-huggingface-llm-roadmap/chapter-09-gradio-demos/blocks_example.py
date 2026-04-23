# Chapter 9 — the same sentiment app, using gr.Blocks for more control.

import gradio as gr
from transformers import pipeline

classifier = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english",
)


def analyze(text: str) -> dict:
    results = classifier(text, top_k=None)
    return {r["label"]: float(r["score"]) for r in results}


with gr.Blocks(title="Sentiment Analyzer") as demo:
    gr.Markdown("# Sentiment Analyzer\nType a sentence and click **Analyze**.")

    with gr.Row():
        with gr.Column():
            inp = gr.Textbox(label="Your text", lines=4)
            btn = gr.Button("Analyze", variant="primary")
        with gr.Column():
            out = gr.Label(label="Sentiment", num_top_classes=2)

    btn.click(fn=analyze, inputs=inp, outputs=out)
    # Also allow pressing Enter in the textbox.
    inp.submit(fn=analyze, inputs=inp, outputs=out)


if __name__ == "__main__":
    demo.launch()
