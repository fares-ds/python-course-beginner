# Project 11 — Data Analyst Agent (with PandasAI)

Load a real dataset of top Spotify songs. Ask it questions in plain English. Watch a language model write the pandas code, run it, and hand you back the answer.

This is a **post-graduation project** — it goes beyond what's in projects 1–10. Two things are new and one is huge:

- **`pandas`** — the standard Python library for working with tables of data. The thing every data scientist uses.
- **A local language model (LLM)** — running on your own machine, no cloud API key, no usage cost. We talk to it via [Ollama](https://ollama.com).
- **`pandasai`** — the glue that turns your English questions into pandas code, using that LLM.

## What you'll learn

- **`pandas.DataFrame`** — what a table looks like in code: rows, columns, `df.head()`, `df.info()`.
- **PandasAI** — how to wrap a dataframe so you can `.chat()` with it.
- **LiteLLM + Ollama** — pointing PandasAI at a local model instead of a paid cloud one.
- **Prompt design for data** — why "average bpm of dance pop songs" works and "the tempo for that one genre" doesn't.
- **`Agent`** — a multi-turn version of `.chat()` that remembers what you asked before, so you can say "and the next 50?" without restating everything.
- **Reading a generated traceback** — when the model writes broken code, you'll see why and how to recover.

## Before you start

This project has more setup than any of the previous ten. Three gates, in order. Don't skip any — each one breaks the next if you do.

### 1. Python 3.11 (not 3.12+)

PandasAI v3 only supports **Python 3.8 through 3.11**. If your Python is 3.12 or newer, the install will look like it works but break at import time.

Check what you've got:

```
python3 --version
```

If it prints `Python 3.11.x`, you're fine. If it prints `3.12` or higher, the easiest fix is to install Python 3.11 alongside it (from [python.org/downloads](https://www.python.org/downloads/release/python-3119/)) and create a virtual environment that uses it:

```
python3.11 -m venv .venv
source .venv/bin/activate     # macOS / Linux
.venv\Scripts\activate        # Windows PowerShell
```

Once activated, `python3 --version` should report 3.11.x. Everything else in this project should be done from inside that activated venv.

### 2. Ollama and a model

[Ollama](https://ollama.com) is a tiny program that runs language models locally. Install it from the website (one-click on Mac/Windows, one command on Linux). Then check:

```
ollama --version
```

Now download a model. We recommend **`qwen2.5-coder:7b`** because it's purpose-built for writing code, which is exactly what PandasAI needs:

```
ollama pull qwen2.5-coder:7b
```

This downloads about 4 GB. Takes a few minutes on a normal connection. Confirm it landed:

```
ollama list
```

You should see `qwen2.5-coder:7b` in the output. The first time you actually *use* the model, Ollama will start serving it on `http://localhost:11434` automatically.

### 3. The Python packages

From inside this project folder:

```
pip install -r requirements.txt
```

That installs three things:

- **`pandasai`** — the natural-language data library.
- **`pandasai-litellm`** — the bridge that lets PandasAI use Ollama (or 100+ other model providers).
- **`python-dotenv`** — reads variables from a `.env` file, so you don't have to hardcode model names in your script.

Sanity check the install:

```
python3 -c "import pandasai; print(pandasai.__version__)"
```

Should print `3.0.0` (or higher).

### 4. A `.env` file

Copy the template:

```
cp .env.example .env       # macOS / Linux
copy .env.example .env     # Windows
```

The defaults inside it work as-is. Open it only if you used a different model name or a different Ollama port.

## What is PandasAI?

**`pandas`** is the standard Python library for working with tables — CSVs, spreadsheets, database results. You load a table into a `DataFrame` (think: a 2D variable, with named columns), and then you call methods like `df.mean()`, `df.groupby("genre").size()`, `df[df["year"] == 2015]`. It's powerful, but the syntax takes weeks to internalize.

**`pandasai`** sits on top. You wrap your dataframe with it, then ask questions in English:

```python
df.chat("What is the average bpm of songs in the 'dance pop' genre?")
```

Under the hood, PandasAI builds a prompt like *"Here is the dataframe's schema: [...]. Write Python pandas code to answer this question: [...]"*, sends it to a language model, gets back code, runs it, and returns the result. You see the answer; the code generation is invisible (unless you turn on debugging — see below).

The catch: the LLM has to be **good at code**. A weak model writes pandas code that crashes or returns nonsense. A strong model gets it right almost every time. We picked Qwen Coder because it's the best small model for code generation as of early 2026.

## The dataset

`data/spotify_top_songs.csv` — about 600 rows of top tracks from 2010–2019. The columns:

| Column | Meaning |
|---|---|
| `title` | song title |
| `artist` | who performs it |
| `top genre` | genre label (e.g. `dance pop`, `hip hop`, `pop`) |
| `year` | year the song was on the chart |
| `bpm` | beats per minute (tempo) |
| `nrgy` | energy (0–100, higher = more intense) |
| `dnce` | danceability (0–100) |
| `dB` | loudness in decibels (negative numbers; closer to 0 = louder) |
| `live` | "liveness" — likelihood of being a live recording |
| `val` | valence — musical positivity (0–100) |
| `dur` | duration in seconds |
| `acous` | acousticness (0–100) |
| `spch` | speechiness (talky-ness — high for rap, low for instrumentals) |
| `pop` | popularity score (0–100) |

A couple of sample rows:

```
title                  artist   top genre        year  bpm  nrgy  dnce  ...  pop
"Hey, Soul Sister"     Train    neo mellow       2010  97   89    67    ...  83
"Love The Way You Lie" Eminem   detroit hip hop  2010  87   93    75    ...  82
```

## Your first question

The smallest possible PandasAI program. Type this into a fresh file (don't copy-paste — you learn by typing):

```python
import pandas as pd
import pandasai as pai
from pandasai_litellm import LiteLLM

llm = LiteLLM(model="ollama/qwen2.5-coder:7b", api_base="http://localhost:11434")
pai.config.set({"llm": llm})

raw = pd.read_csv("data/spotify_top_songs.csv", index_col=0)
df = pai.DataFrame(raw)

print(df.chat("How many songs are in the dataset?"))
```

Run it. It will pause for a few seconds (the model is thinking), then print something like `603`. Slower than calling `len(raw)` directly, but you didn't have to know the word "len".

**What just happened, line by line:**

- `LiteLLM(model="ollama/qwen2.5-coder:7b", api_base="...")` — build a tiny object that knows how to talk to your local Ollama. The `"ollama/"` prefix is a LiteLLM convention: it tells LiteLLM which "provider" to route to.
- `pai.config.set({"llm": llm})` — register that LLM as PandasAI's default. From now on, every `.chat()` call uses it.
- `pd.read_csv(..., index_col=0)` — load the CSV into a regular pandas DataFrame. `index_col=0` tells pandas "the first column is just row numbers, treat it as the index, don't make it a real column."
- `pai.DataFrame(raw)` — wrap the pandas DataFrame so it gets the `.chat()` method.
- `df.chat("...")` — send the question to the LLM, get the answer back.

## Five questions, five capabilities

Each one teaches a new way to push the agent. Run them in order. Some will take 10–30 seconds on a 7B model — that's normal.

### 1. Direct lookup
```python
df.chat("How many songs are in the dataset?")
```
The roundtrip-test question. If this returns a sensible number, your install works.

### 2. Filter + aggregate
```python
df.chat("What is the average bpm of songs in the 'dance pop' genre?")
```
The first time you've asked the model to filter the data ("only dance pop") *and then* aggregate ("the mean of bpm"). Two operations, one English sentence.

### 3. Group-by comparison
```python
df.chat("Which 5 artists have the most songs in the dataset?")
```
Now the model has to group by artist, count rows in each group, sort, and take the top 5. Four operations from one question. This is where PandasAI starts to feel magical.

### 4. Chart
```python
df.chat("Plot a histogram of song popularity scores and save it as 'pop_hist.png'.")
```
The answer this time isn't a number — it's an image. PandasAI saves charts to `exports/charts/` by default. If you want the file in your current folder, ask for it explicitly (as above). Open the PNG to see the shape of the popularity distribution.

### 5. Multi-step reasoning
```python
df.chat(
    "Among the 50 most popular songs, which genre appears most often, "
    "and what is the average danceability of songs in that genre?"
)
```
This is **filter → rank → group-by → count → second aggregate**, all from one sentence. A 7B model may not nail it on the first try; if it fumbles, see the "Debugging" section below.

## Multi-turn with `Agent`

`df.chat()` answers each question in isolation — it doesn't remember what you asked before. For a real conversation, use `Agent`:

```python
from pandasai import Agent

agent = Agent([df])
agent.chat("Which artist has the most songs?")
agent.follow_up("What is the average energy of their songs?")
```

The follow-up's "their" refers to whatever the previous answer was. The Agent stores the prior question + answer in its memory and includes them in the next prompt to the LLM. That's the *whole* difference — but it's the difference between Q&A and an actual back-and-forth.

In `solution.py`, the interactive REPL at the bottom uses `agent.chat()` for every question, so all your questions during one session can build on each other.

## Run it

```
python3 solution.py
```

Expected: it prints the dataset's columns and first 3 rows, runs the 5 demo questions one at a time (each one takes a few seconds), then drops you into a `Ask a question:` prompt.

## Example run

```
$ python3 solution.py
Loaded 602 rows. Columns:
  - title
  - artist
  - top genre
  - year
  - bpm
  ...
  - pop

First 3 rows:
                  title  artist        top genre  year  bpm  nrgy  ...
1   Hey, Soul Sister     Train         neo mellow 2010   97    89  ...
2   Love The Way You Lie Eminem        detroit hip hop 2010   87    93 ...
3   TiK ToK              Kesha         dance pop  2010  120    84  ...

============================================================
DEMO: 5 questions, 5 capabilities
============================================================

[1/5] Q: How many songs are in the dataset?
      A: 602

[2/5] Q: What is the average bpm of songs in the 'dance pop' genre?
      A: 119.3

[3/5] Q: Which 5 artists have the most songs in the dataset?
      A:    artist        count
         Katy Perry      17
         Justin Bieber   16
         Maroon 5        15
         Rihanna         15
         Lady Gaga       14

[4/5] Q: Plot a histogram of song popularity scores and save it as 'pop_hist.png'.
      A: pop_hist.png

[5/5] Q: Among the 50 most popular songs, which genre appears most often...
      A: dance pop, with average danceability 71.4

============================================================
Your turn. Ask the agent anything about the data.
Type 'quit' or press Ctrl+C to exit.
============================================================

Ask a question: which year had the highest average song popularity?
-> 2015 (avg popularity 70.8)

Ask a question: quit
Bye!
```

The actual numbers you get may differ slightly — local LLMs are non-deterministic, so two runs can pick slightly different rows when answering ambiguous phrasing.

## When it goes wrong (debugging)

You will hit each of these. Here's how to read them.

### Pitfall 1 — "no such column" or hallucinated columns

The LLM occasionally references a column that doesn't exist (`tempo` instead of `bpm`, `popularity_score` instead of `pop`). The error usually looks like:

```
KeyError: 'tempo'
```

**Two fixes**, in order of preference:

1. **Use the exact column name** in your question. The dataset's columns are listed at the top of `solution.py`'s output. `bpm`, not "tempo". `pop`, not "popularity score".
2. **Tell the agent the column** explicitly: `"Use the 'pop' column to find the most popular song."` This works as a one-off; the better long-term habit is option 1.

### Pitfall 2 — the model writes weird code or gives a strange answer

7B parameter models are not GPT-4. On harder questions (especially question 5), they sometimes write code that runs but does the wrong thing, or rambles in plain English instead of returning a value.

**Three fixes**, in order:

1. **Rephrase more explicitly.** "What is the most common genre?" → "Group the songs by 'top genre', count how many there are in each group, and tell me the genre with the highest count."
2. **Break it into two questions.** Instead of asking question 5 in one go, do it as two `agent.chat()` calls: first "what genre appears most often in the top 50?", then "what is the average danceability of songs in that genre?".
3. **Try a bigger model.** `ollama pull llama3.1:70b` (40 GB, only if your machine has 64 GB+ RAM) or pay for a cloud model — see Extension 2 below.

### Pitfall 3 — connection refused / Ollama isn't running

You'll see something like:

```
litellm.exceptions.APIConnectionError: ... Connection refused
```

**Fix**: in another terminal, run `ollama list`. If that command itself errors, Ollama isn't running — start it (on Mac/Windows it usually starts automatically when you launch the app; on Linux it's `ollama serve`). If `ollama list` works but the script still fails, double-check the `OLLAMA_BASE_URL` in `.env` matches where Ollama actually listens.

## Check yourself

Before calling this project complete, can you answer these out loud?

1. What does `pai.config.set({"llm": llm})` actually do? Why do we need to call it before `df.chat()`?
2. What's the difference between `df.chat("...")` and `agent.chat("...")`? When would you use one over the other?
3. Where does PandasAI save chart images by default? How would you change that?

## Try these extensions

1. **Verbose mode.** Set `pai.config.set({"verbose": True})` and re-run a question. You'll see the full prompt that was sent to the LLM and the code it wrote. This is the single best debugging tool. Read a few prompts — you'll start to understand *why* certain phrasings work better than others.
2. **Swap the model.** Try `ollama pull llama3.1:8b` (general-purpose) or `ollama pull mistral` (smaller, faster, sometimes worse). Change `OLLAMA_MODEL` in `.env`. Run the same 5 demo questions. Which model gets question 5 right most often?
3. **Add a second dataframe.** Find a CSV of artist nationalities (or make a small one yourself). Pass both dataframes to the Agent: `Agent([songs_df, artists_df])`. Ask cross-table questions: "what's the most popular country of origin among the top 50 songs?" PandasAI will figure out it needs to join.
4. **Save the conversation.** Extend the REPL to log every question + answer to `conversation.json` (Project 8 territory). Bonus: add a `replay` command that re-runs the saved questions.
5. **Tiny web UI.** `pip install streamlit`, then write a 30-line Streamlit app that puts an input box on a webpage and calls your agent. It's the closest you'll get to "shipped product" with a single file of Python.

## What you actually built

A program that takes a CSV no human has annotated, plus an English question, and produces an answer. That used to take a data analyst an hour; now it takes you a sentence.

The pattern generalizes far beyond Spotify. Sales reports, app analytics, scientific data, your personal expense log — anything that fits in a table is something a PandasAI agent can analyze. The bottleneck stops being "do I know pandas" and becomes "do I know what question to ask." That's a much better problem to have.
