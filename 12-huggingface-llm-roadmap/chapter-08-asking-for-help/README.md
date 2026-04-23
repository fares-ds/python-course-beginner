# Chapter 8 — How to ask for help

The shortest chapter, and one of the most important. Bookmark this; re-read it the first time something breaks and you don't know why.

**Course link:** [Chapter 8 on the HF docs](https://huggingface.co/learn/llm-course/en/chapter8/1)

## What you'll learn

- **Reading a Python traceback** inside a Hugging Face stack — where does *your* code end and *their* code start?
- **Hugging Face forums + GitHub issues etiquette** — how to ask in a way that gets answered within a day.
- **Debugging a flat loss** — the symptom checklist when your fine-tune isn't learning.
- **The minimal reproducible example** — shrinking your 500-line broken script to a 20-line repro.

## What's in this folder

- [`solution.py`](solution.py) — a script that deliberately breaks in three common ways, catches the error, and prints a guided diagnosis. Run it, read the output, internalize the patterns.
- [`requirements.txt`](requirements.txt) — `transformers` (to reproduce the broken patterns).

## Setup

```bash
pip install -r requirements.txt
```

## Run it

```bash
python3 solution.py
```

Expected: three fake errors, each with the traceback shown and the common cause explained.

## Key concepts

### Reading a HF traceback
Tracebacks read top → bottom (most recent call last). In a HF stack, the bottom is usually inside `transformers/...`. **Scroll up until you see a path that's in your project.** That's the line you control. Start there.

### Symptoms of "my fine-tune isn't learning"

| Symptom | Likely cause |
|---|---|
| Loss = NaN from step 1 | Learning rate too high; or `fp16` overflowing; or bad input |
| Loss flat (doesn't move) | Wrong `num_labels`; labels never in loss (e.g. all -100); wrong task-head |
| Train loss drops, eval loss doesn't | Label leak, or your eval set is mis-prepped |
| Everything works in training but predict returns garbage | Forgot `model.eval()`; or you're using the wrong `AutoModel*` class for inference |

### The minimal reproducible example
Before asking for help, shrink your problem:

1. Can you reproduce with a tiny input (1 sentence)?
2. Can you reproduce with a tiny model (`distilbert-base-uncased`)?
3. Can you reproduce with no data-prep (feed raw text directly)?
4. Can you paste the 20 offending lines into a comment box?

If yes to all four, you'll usually have answered your own question by the end of step 3.

### Asking on the forum
The [Hugging Face forum](https://discuss.huggingface.co/) is the best place. Your post should have:
- **Title**: specific — "Trainer loss NaN with fp16 on T5" not "help".
- **What you're trying to do**: one sentence.
- **What you tried**: the minimal repro.
- **What happened**: the actual error, copy-pasted as code, not screenshotted.
- **Versions**: `transformers`, `torch`, Python.

Skip any of those and you'll wait days for someone to ask you to add them.

## Mini-tasks

1. Run `solution.py`. For each of the three fake errors, predict the cause before reading the explanation.
2. Find your most recent real Python error (from any project). Follow the "read top → bottom, scroll until my file appears" discipline. Was the fix in a line you wrote, or a library line?

## Focus vs skim

- **Focus:** section 2 (reading errors), section 4 (debugging the training pipeline). These are the actionable parts.
- **Skim:** sections 3 and 5 (forum/issue etiquette) — read once, internalize, move on.

## Common pitfalls (meta)

- **Googling the full traceback verbatim** — sometimes works, usually drowns you in unrelated hits. Google the **last line** (the exception type + message) instead.
- **Posting a screenshot** — forum readers can't copy-paste text from a screenshot. Always paste text as formatted code.

## Expected outcome

When a training run NaNs at 2am, you have a checklist instead of a panic.

## Next

→ [Chapter 9 — Building and sharing demos (Gradio)](../chapter-09-gradio-demos/)
