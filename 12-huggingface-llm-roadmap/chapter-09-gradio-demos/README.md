# Chapter 9 — Building and sharing demos with Gradio

Three-line web UIs for models. This is how you turn "I fine-tuned a model" into "I shipped a thing strangers can use."

**Course link:** [Chapter 9 on the HF docs](https://huggingface.co/learn/llm-course/en/chapter9/1)

## What you'll learn

- `gr.Interface` — one-function-one-UI Gradio, the simplest possible web demo.
- `gr.Blocks` — structured layouts for when you need more than one input/output.
- **Hugging Face Spaces** — free hosting for Gradio apps. Drag, drop, done.
- Hub integration — `gr.load("model-name")` autowires a demo for any public model.

## What's in this folder

- [`solution.py`](solution.py) — spins up a local Gradio app for the sentiment model. Runs on `http://127.0.0.1:7860`.
- [`blocks_example.py`](blocks_example.py) — the same app rewritten with `gr.Blocks` so you can see both styles.
- [`requirements.txt`](requirements.txt) — `gradio`, `transformers`, `torch`.

## Setup

```bash
pip install -r requirements.txt
```

## Run it

```bash
python3 solution.py
```

Expected: it prints a URL like `Running on local URL: http://127.0.0.1:7860`. Open that in your browser.

Type a sentence; see the sentiment and confidence. Click "Submit."

To try Blocks:

```bash
python3 blocks_example.py
```

## Key concepts

### `gr.Interface`
```python
gr.Interface(fn=my_function, inputs="text", outputs="label").launch()
```

The `fn` is a normal Python function; Gradio figures out how to wire the UI. `inputs` and `outputs` can be type strings (`"text"`, `"image"`, `"audio"`) or `gr.Textbox(...)` / `gr.Label(...)` components for more control.

### `gr.Blocks`
```python
with gr.Blocks() as demo:
    inp = gr.Textbox(label="Input")
    out = gr.Label(label="Sentiment")
    btn = gr.Button("Analyze")
    btn.click(fn=my_function, inputs=inp, outputs=out)
demo.launch()
```

Use Blocks when you need multiple inputs, multiple outputs, tabs, or a custom layout. The main primitives are `Row`, `Column`, `Tabs`, and component factory functions (`Textbox`, `Slider`, `Dropdown`, etc.).

### Hugging Face Spaces
Create a Space at `huggingface.co/new-space`. Choose "Gradio SDK." Upload `solution.py` as `app.py` and `requirements.txt`. Push. In ~2 minutes, your demo is live at `huggingface.co/spaces/you/name`.

### `gr.load(...)` shortcut
```python
gr.load("distilbert-base-uncased-finetuned-sst-2-english").launch()
```
Autowires a Gradio demo for any public HF model. One line for any public model is wild.

## Mini-tasks

1. Modify `solution.py` to use your own fine-tuned MRPC model from Chapter 4. Test it with a few paraphrase/not-paraphrase pairs.
2. Add a second output showing the model's full probability distribution (not just the top label).
3. Deploy to Spaces. Share the URL with a friend and watch them use your model.

## Focus vs skim

- **Focus:** sections 2 (first demo), 3 (Interface class), 5 (Hub integration), 7 (Blocks).
- **Skim:** advanced interface features on first pass. Come back when you need them.

## Common pitfalls

- **Forgetting `demo.launch(share=True)`** when you want a public URL — locally-launched demos are localhost-only.
- **Putting slow model-loading inside the function** — Gradio calls `fn` on every request. Load the model once, globally, at startup.
- **Rate limits on Spaces** — free Spaces get limited CPU/RAM. For bigger models, enable the `ZeroGPU` hardware option (free, queue-based).

## Expected outcome

You can wrap any model in a Gradio UI and have a public demo on Spaces in under 15 minutes.

## Next

→ [Chapter 10 — Curating high-quality datasets](../chapter-10-curating-datasets/)
