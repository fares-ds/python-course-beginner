# Project 2 — Number Guessing Game

The computer picks a secret number between 1 and 100. You guess. It tells you "too high" or "too low". Keep guessing until you get it.

This project introduces the three most important tools in any programming language: **making decisions, repeating things, and handling randomness.** Once you have these, you can write almost anything.

## What you'll learn

- **`import`** — bringing in extra features (here, the ability to pick random numbers).
- **`if` / `elif` / `else`** — making decisions based on conditions.
- **Comparison operators** — `<`, `>`, `==` (two equals signs means "is equal to").
- **`while` loops** — repeating a block of code.
- **`break` and `continue`** — controlling how a loop ends or skips.
- **`int()`** — converting a string like `"42"` into the number `42`.
- **`try` / `except`** — handling mistakes without crashing the program.

## How the program works

```
pick a secret number
loop:
    ask for a guess
    if guess is too low, say so and keep looping
    if guess is too high, say so and keep looping
    if guess is exactly right, celebrate and stop
```

That plain-English sketch (sometimes called **pseudocode**) maps almost line-for-line to the real code.

## Key ideas, explained

### `import random`

At the top of the file. `random` is a **module** — a bundle of code that ships with Python. `random.randint(1, 100)` gives us a whole number between 1 and 100.

### `while True:`

A `while` loop runs as long as the condition after `while` is true. `True` is always true, so `while True:` runs forever — until we leave using `break`.

Why not write a loop that stops on its own? Because we don't know how many guesses the user will take. A "keep going until something happens" loop is the right shape for this problem.

### `if` / `elif` / `else`

```python
if guess < secret:
    print("Too low.")
elif guess > secret:
    print("Too high.")
else:
    print("Got it!")
```

Python checks these in order:

1. Is `guess < secret` true? If yes, run that block, **skip the rest**.
2. Otherwise, is `guess > secret` true? If yes, run that block, skip the rest.
3. Otherwise, run the `else` block.

`elif` is short for "else if". You can have as many `elif` branches as you want.

### `int()` and `try` / `except`

`input()` always gives you text, even if the user typed `42`. To do math or comparisons, you need a number. `int("42")` turns the text `"42"` into the number `42`.

But `int("banana")` **crashes the program**. We don't want that. `try` / `except` lets us say "try this; if something goes wrong, do this other thing instead":

```python
try:
    guess = int(answer)
except ValueError:
    print("That's not a whole number.")
    continue
```

`continue` jumps back to the top of the loop, skipping the rest of this iteration. So we just ask again.

## Run it

```
python3 solution.py
```

Try typing `banana` to see the error handling work. Try guessing on purpose-badly to see the hint system.

## Try these extensions

1. **Change the range.** Make it 1 to 1000 instead of 1 to 100.
2. **Limit the number of guesses.** If the user takes more than 10, the computer wins. (Hint: check `attempts` each turn, and use `break` if it's too high.)
3. **Warmer / colder hints.** Instead of "too high" / "too low", say "very close" if within 5, "close" if within 15, "far" otherwise.
4. **Play again?** After a win, ask "Play again? (y/n)". If yes, start over. (Hint: wrap the whole game in another loop.)
