# Project 1 — Mad Libs

Mad Libs is a word game: you fill in blanks without knowing the story, and the result is usually silly. We're going to write a program that does this for us.

## What you'll learn

- **`print()`** — how to make your program show text on the screen.
- **`input()`** — how to ask the user a question and remember the answer.
- **Variables** — names we give to pieces of data so we can use them later. Think of a variable as a **labeled box**: you write a name on the box (`name`), drop a value inside (`"Alice"`), and any time you say the box's name later, Python hands you what's inside.
- **Strings** — text in Python (anything inside quotes `" "`).
- **f-strings** — a way to mix variables into text.
- **Comments** — notes in your code that Python ignores. They start with `#`.

## How the program works

Every program you'll ever write does three things, in some order: **gets input → processes it → produces output**. Mad Libs is the simplest possible example:

1. Ask the user for a few words.
2. Glue those words into a pre-written story.
3. Print the finished story.

That's it. No loops, no decisions, no math. Just in → out.

## Read the solution

Open [`solution.py`](solution.py) in any text editor. Read it top to bottom. A few things to notice:

### Lines starting with `#` are comments

```python
# This is a comment. Python ignores it.
```

Comments are for humans. Use them to explain *why* something is happening, not *what* — the code already shows what.

### `input()` waits for the user to type

```python
name = input("Your name: ")
```

Three things are happening on this one line:

1. `input("Your name: ")` prints the text inside the parentheses and waits for the user to press Enter.
2. Whatever they typed is handed back.
3. The `=` sign **stores** that value in a variable called `name`.

Now any time we write `name` elsewhere in the program, Python replaces it with what the user typed.

Concretely, if the user types `Alice` and presses Enter:

```
Your name: Alice      <- user typed "Alice"
```

...then `name` is now the string `"Alice"`.

### f-strings put variables inside text

```python
print(f"Hello, {name}!")
```

The `f` right before the quote turns this into a **formatted string**. Anything inside `{ }` is treated as a Python variable and swapped in. Without the `f`, Python would print the literal text `Hello, {name}!` — braces and all.

Side-by-side:

```python
name = "Alice"
print(f"Hello, {name}!")    # prints:  Hello, Alice!
print("Hello, {name}!")     # prints:  Hello, {name}!   (no f, no magic)
```

## Run it

From your terminal, inside this folder:

```
python3 solution.py
```

Try entering silly answers and reading your story out loud. That's the whole joy of Mad Libs.

## Example run

Here's what a session looks like. The text at the end of each prompt line is what **you type** — the rest is what the program prints.

```
$ python3 solution.py
Welcome to Mad Libs!
Give me a few words and I'll make you a story.

Your name: Alice
An adjective (a describing word, like 'sparkly'): sparkly
An animal: dragon
A verb ending in -ing (like 'dancing'): singing
A place: the moon

--- Your story ---
One morning, Alice woke up to find a sparkly dragon in the kitchen.
The dragon was singing on the table and refused to leave.
Eventually they both moved to the moon and lived happily ever after.
```

## Check yourself

Before moving on, can you answer these out loud, in your own words?

1. What's the difference between `"Hello, {name}"` and `f"Hello, {name}"`?
2. In `name = input("Your name: ")`, which part does the user see, and which part is where the answer gets stored?
3. If you swap the order of the `input()` lines — ask for the animal before the name — does the story still work? Why or why not?

## Try these extensions

Stuck on what to do next? Try these, in order from easiest to hardest:

1. **Add another blank.** Ask for a number, a color, or a food, and work it into the story.
2. **Write a completely new story.** Change the sentences in the `print(...)` lines. The words you ask for should match your new story.
3. **Make a longer story.** Add 5 more sentences with more variables.
4. **Two stories.** Ask the user at the start: "Would you like story A or story B?" — but wait, that needs an `if` statement. Come back to this after Project 2.
