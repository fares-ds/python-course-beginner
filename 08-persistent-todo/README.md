# Project 8 — Persistent To-Do List

This is Project 4's to-do list, but with one huge upgrade: **your tasks survive quitting**. Add two things, quit the program, come back tomorrow — they're still there.

The trick is to write the list to a small file every time it changes, and read the file back whenever the program starts. The menu and the functions are 90% the same as Project 4; the new code is almost entirely about **saving and loading**.

## What you'll learn

- **Writing to a file** — `open(path, "w")` (not just `open(path)` for reading).
- **The JSON format** — a universal way to write lists, dicts, strings, and numbers as text so a program can read them back exactly as they were.
- **`json.dump()` and `json.load()`** — Python ↔ JSON, in one function call each.
- **`os.path.exists(path)`** — check whether a file is there before trying to open it.
- **Program state that survives restarts** — the difference between a toy and a tool.

## Why this matters

A program that forgets everything when you close it is a demo. A program that remembers is a **tool**. Almost every real app does this somehow — your browser remembers open tabs, your editor remembers your recent files, your phone remembers your contacts. The simplest way to make a small program do the same thing is: write a file when something changes, read it back when you start.

## What is JSON?

JSON is just **text that follows a strict format**. It was designed so that any programming language can read it. Open `tasks.json` in a text editor after using this program and you'll see something like:

```
["buy eggs", "water plants"]
```

That's it. A list of strings, written the way Python would print it. JSON also handles dicts (`{"name": "Alice"}`), numbers, `true`, `false`, `null`, and nesting — which means the dict-of-dicts from Project 7 saves cleanly too:

```
{"Alice": {"phone": "555-1234", "email": "a@x.com"}}
```

Most APIs speak JSON. Most config files are JSON. You'll see this format **everywhere**.

## How the program works

```
load tasks from tasks.json if it exists     (otherwise start with an empty list)

loop:
    show the menu
    read the choice
    if 1: add a task     (then save)
    if 2: remove a task  (then save)
    if 3: view tasks
    if 4: quit
```

Saving happens after every change. So even if the program crashes, the file is up-to-date.

## Key ideas, explained

### Reading vs writing

In Project 5 you saw `open("words.txt")` — reading. To write, you pass a second argument, `"w"`:

```python
with open("tasks.json") as f:          # "r" is the default — read mode
    ...

with open("tasks.json", "w") as f:     # "w" — write mode (overwrites!)
    ...
```

- **`"r"`** — read. File must exist.
- **`"w"`** — write. Creates the file if missing; **replaces** everything if it does exist.

"Replaces everything" sounds scary, but it's exactly what we want here: "here is the whole current list; save it." We don't have to manage edits to individual lines.

### `json.dump()` — Python → JSON file

```python
tasks = ["buy eggs", "water plants"]
with open("tasks.json", "w") as f:
    json.dump(tasks, f)
```

`json.dump(value, file)` writes any JSON-safe value (lists, dicts, strings, numbers, booleans, `None`) to the file as JSON text.

### `json.load()` — JSON file → Python

```python
with open("tasks.json") as f:
    tasks = json.load(f)
```

`json.load(file)` reads JSON text from the file and hands you back a normal Python value — the same shape it had when you dumped it. List goes in, list comes out.

### `os.path.exists(path)`

```python
import os

os.path.exists("tasks.json")      # -> True or False
```

On the very first run of this program, `tasks.json` doesn't exist yet — trying to `open()` it for reading would crash. We check first, and if it's missing we just start with an empty list.

### Where does `tasks.json` live?

In the folder you ran the program **from**. If you `cd` into `08-persistent-todo` and run `python3 solution.py`, the file appears right next to `solution.py`. If you run it from a different folder, the file shows up there instead. "Current directory" matters.

## Run it

```
python3 solution.py
```

Add a few tasks, view them, quit. Then run it again — you should see `Loaded N task(s) from tasks.json.` at startup. Open `tasks.json` in any text editor to peek at what got saved.

To start fresh, just delete `tasks.json`.

## Example run

### First run — adding tasks

```
$ python3 solution.py
Welcome to your to-do list.

What would you like to do?
  1) Add a task
  2) Remove a task
  3) View all tasks
  4) Quit
Pick an option (1-4): 1
What's the task? buy eggs
Added: buy eggs

... (menu shown again) ...
Pick an option (1-4): 1
What's the task? water plants
Added: water plants

... (menu shown again) ...
Pick an option (1-4): 4
Bye!
```

At this point, `tasks.json` on disk contains:

```
["buy eggs", "water plants"]
```

### Second run — tasks are still there

```
$ python3 solution.py
Welcome to your to-do list.
Loaded 2 task(s) from tasks.json.

... (menu shown) ...
Pick an option (1-4): 3
Your tasks:
  1. buy eggs
  2. water plants

... (menu shown) ...
Pick an option (1-4): 2
Your tasks:
  1. buy eggs
  2. water plants
Which number would you like to remove? 1
Removed: buy eggs

... (menu shown) ...
Pick an option (1-4): 4
Bye!
```

Now `tasks.json` contains:

```
["water plants"]
```

This is the confidence moment. You just wrote a program that **remembers things between runs**. That's what real software does.

## Check yourself

Before moving on, can you answer these out loud?

1. What would happen if we called `open("tasks.json", "w")` but the file already had stuff in it? Why is that actually fine for *this* program?
2. Why do we call `save_tasks(tasks)` inside `add_task` and `remove_task`, instead of once at the end (say, just before quitting)?
3. Open `tasks.json` in a text editor — what does it look like? If you edited it by hand and added a new task string to the list, would the program notice the next time it ran? Why or why not?

## Try these extensions

1. **Corrupt-file safety.** What happens if `tasks.json` exists but is empty or garbled? Right now `json.load()` would crash. Wrap the load in a `try`/`except` so that any error falls back to an empty list, with a warning. (Hint: the exception type is `json.JSONDecodeError`, but you can also catch plain `Exception` to start.)
2. **`json.dump(..., indent=2)`.** Try this tweak in `save_tasks`. Open `tasks.json` afterward — notice how much easier it is to read. `indent` is a named (keyword) argument: pass it by name.
3. **A removed-tasks history.** Every time you remove a task, append it to a second file (`history.json`) with a `{"task": ..., "removed_at": ...}` entry. Suddenly you're keeping records! (You'll want `datetime.now().isoformat()` — a little peek at Project 9's tools.)
4. **Mark done, don't delete.** Change each task from a plain string to a dict: `{"text": "buy eggs", "done": false}`. View should show `[x]` or `[ ]` in front. Add a "mark done" menu option. (Now the file is genuinely a dict-of-dicts-ish structure — exactly the shape you saved in Project 7.)
