# Project 4 — To-Do List

A tiny to-do list that lives in your terminal. You can add tasks, see them, and remove them.

The main new idea: **lists**. Until now, every variable has held one thing — a number, a word, a choice. A list holds *many* things in one variable.

> **Heads up:** this program forgets your tasks when you quit. Making it remember means saving to a file, which is a perfect next project on your own.

## What you'll learn

- **Lists** — `[]`, the go-to way to hold multiple items in Python.
- **List methods**: `.append()`, `.pop()`, `len()`.
- **`for` loops** — stepping through a list one item at a time.
- **`enumerate()`** — numbering each item in a list as you loop.
- **The menu pattern** — a loop that shows options and reacts to the user's choice. You'll reuse this pattern forever.

## How the program works

```
tasks = empty list

loop forever:
    show the menu
    read the user's choice
    if 1: add a task
    if 2: remove a task
    if 3: view tasks
    if 4: quit
```

Each action is its own function. The main loop is tiny.

## Key ideas, explained

### Lists

```python
tasks = []            # empty list
tasks.append("eggs")  # now: ["eggs"]
tasks.append("milk")  # now: ["eggs", "milk"]
len(tasks)            # 2
tasks[0]              # "eggs"  — lists start at index 0
tasks.pop(0)          # removes "eggs", returns it
```

Think of a list as a numbered row of boxes, left-to-right. You can put things in, take them out, and ask how many are in there.

### Zero-indexed

Python starts counting at 0. The first item in a list is `tasks[0]`, the second is `tasks[1]`, and so on.

This trips up almost every beginner. It's also why we use `index = number - 1` when the user picks "task #3" — internally, that's the item at position `2`.

### `for` loop with `enumerate()`

```python
for number, task in enumerate(tasks, start=1):
    print(f"  {number}. {task}")
```

A `for` loop walks through something item by item. Plain `for task in tasks` gives you just each task. `enumerate(tasks, start=1)` also gives you a counter, so we can print "1. eggs", "2. milk", etc.

With `tasks = ["eggs", "milk", "bread"]`, the loop above prints:

```
  1. eggs
  2. milk
  3. bread
```

### The menu pattern

```python
while True:
    show_menu()
    choice = input(...)
    if choice == "1":
        ...
    elif choice == "2":
        ...
    elif choice == "4":
        break
```

This pattern — loop, show options, read choice, dispatch to a function, repeat until quit — is one of the most common program shapes. You'll see it everywhere.

### Why are `tasks` passed into functions?

```python
def add_task(tasks):
    tasks.append(...)
```

We pass the list to each function so they can work on it. When you `.append()` to the list inside a function, the change sticks — because the list itself is shared, not copied. (For experienced readers: Python lists are mutable and passed by reference.)

## Run it

```
python3 solution.py
```

Try adding a few tasks, viewing them, removing one by number. Try removing from an empty list, or typing "banana" at the menu. A good program doesn't crash when the user makes mistakes.

## Example run

Here's a full session: adding two tasks, viewing them, removing one, then quitting. (The menu prints every turn; we've marked the repeats with `...` to keep the transcript short.)

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
What's the task? water the plants
Added: water the plants

... (menu shown again) ...
Pick an option (1-4): 3
Your tasks:
  1. buy eggs
  2. water the plants

... (menu shown again) ...
Pick an option (1-4): 2
Your tasks:
  1. buy eggs
  2. water the plants
Which number would you like to remove? 1
Removed: buy eggs

... (menu shown again) ...
Pick an option (1-4): 4
Bye!
```

And here's what each kind of mistake looks like:

```
Pick an option (1-4): 7
Please pick 1, 2, 3, or 4.

Pick an option (1-4): 2
Your tasks:
  1. water the plants
Which number would you like to remove? banana
That's not a number.

Pick an option (1-4): 2
Your tasks:
  1. water the plants
Which number would you like to remove? 99
That number isn't on the list.
```

None of these crash the program — they just print a message and go back to the menu.

## Try these extensions

1. **Mark tasks as done** instead of deleting them. Show done tasks with a `[x]` next to them.
2. **Clear all tasks.** Add a menu option that empties the list after asking "Are you sure?".
3. **Save to a file.** When the program starts, read tasks from `tasks.txt`. When you add/remove a task, write the new list back. (This is a big step — you'll need the `open()` function. Google "python read write text file".)
4. **Due dates.** Let the user enter a due date with each task. You'll need to store more than one piece of info per task — look up **dictionaries** in Python.
