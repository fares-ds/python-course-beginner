# Learn Python by Building Things

Welcome! This is a hands-on path for someone who has **never written code before**. You'll build small Python programs, one after the other. Each one teaches you a new idea, and by the end you'll know enough Python to start building your own projects.

The path is split into two tiers:

- **Tier 1 — Absolute Beginner** (projects 1–5). The shape of programming: input/output, decisions, loops, functions, lists, files.
- **Tier 2 — Fundamentals** (project 6 onward). The rest of the core toolkit: floats, dictionaries, persistence, time, and APIs.

Every project has:

- **`README.md`** — explains the new ideas in plain English, then walks through the code line by line.
- **`solution.py`** — a finished, working version you can run and read.

No extra libraries to install. Everything uses Python that comes with your computer.

> **Teaching with this repo?** If you're a tutor (human or AI) using this to teach someone, read [CLAUDE.md](CLAUDE.md) first — it explains the teaching philosophy, pacing, and what *not* to do.

---

## Before you start: setting up Python

### 1. Check if Python is installed

Open a **terminal**:

- **macOS**: press `Cmd + Space`, type "Terminal", press Enter.
- **Windows**: press the Windows key, type "PowerShell", press Enter.
- **Linux**: you already know.

Type this and press Enter:

```
python3 --version
```

If you see something like `Python 3.11.5`, you're ready. If you get an error, install Python from [python.org/downloads](https://www.python.org/downloads/) and try again.

### 2. How to run a project

Every solution is a file called `solution.py`. To run it:

```
cd path/to/python-projects/01-mad-libs
python3 solution.py
```

`cd` means "change directory" — it moves your terminal into that folder. Then `python3 solution.py` tells Python to run the file.

To stop a program while it's running, press `Ctrl + C`.

---

## The projects

Do them in order. Each one builds on the last.

### Tier 1 — Absolute Beginner

| # | Project | What you'll learn |
|---|---------|-------------------|
| 1 | [Mad Libs](01-mad-libs/) | Printing text, asking for input, variables, strings |
| 2 | [Number Guessing Game](02-number-guessing/) | `if` / `else`, loops, randomness |
| 3 | [Rock Paper Scissors](03-rock-paper-scissors/) | Functions — breaking a program into pieces |
| 4 | [To-Do List](04-todo-list/) | Lists — storing many things in one place |
| 5 | [Hangman](05-hangman/) | Putting it all together (files, sets) |

### Tier 2 — Fundamentals

| # | Project | What you'll learn |
|---|---------|-------------------|
| 6 | [Tip Splitter](06-tip-splitter/) | Floats, `round()`, formatting money |
| 7 | [Contact Book](07-contact-book/) | Dictionaries — name → details lookup |
| 8 | [Persistent To-Do](08-persistent-todo/) | Saving to a file with JSON — state that survives |
| 9 | [Pomodoro Timer](09-pomodoro-timer/) | `time.sleep`, `datetime`, code that runs over wall-clock time |
| 10 | [Weather Fetcher](10-weather-fetcher/) | `pip install`, `requests`, HTTP, APIs — talking to the internet |

---

## How to use these projects

1. **Read the project's README first.** Don't skip it. It explains the idea before showing the code.
2. **Try to predict what the code does** before you run it.
3. **Run the solution** and play with it. Change numbers, change words, break it on purpose.
4. **Answer the "Check yourself" questions** at the end of each README before moving on. If you can't explain it out loud, re-read and run things again — don't push forward.
5. **Try the extensions.** That's where real learning happens.

### One more tip: type, don't copy-paste

The `solution.py` files are references, not something to copy. If you really want this to stick, **open an empty file next to the solution and retype it yourself, line by line**. Your fingers remember what your eyes skim past, and every tiny typo you make is a chance to learn how Python reports errors.

Have fun!
