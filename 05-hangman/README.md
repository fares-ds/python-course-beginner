# Project 5 — Hangman

The classic word-guessing game. The computer picks a word; you try to guess it letter by letter. Six wrong guesses and the little ASCII-art stick figure is fully drawn.

This is the **capstone**. It brings together everything from the first four projects — input/output, conditionals, loops, randomness, functions, lists — and adds a couple of new tools: reading from a file, and a new kind of collection called a **set**.

## What you'll learn

- Reading data from a file with `open()` and `.read()` / `.splitlines()`.
- **Sets** — like lists, but no duplicates and no order. Great for "have I seen this?" checks.
- **String methods**: `.isalpha()`, `.lower()`, `.strip()`, `" ".join(...)`.
- **Constants** — all-caps variables at the top of the file for values that never change.
- Combining everything you already know.

## How the program works

```
load all words from words.txt
pick one at random -> that's the secret

loop:
    draw the hangman at current stage
    show the word with revealed letters (the rest as underscores)
    show how many wrong guesses are left
    ask for a letter
    if the letter is in the secret: reveal it
    otherwise: count it as a wrong guess
    if every letter has been guessed: you win, stop
    if too many wrong guesses: you lose, stop
```

## Key ideas, explained

### Reading a file

```python
with open("words.txt") as f:
    words = f.read().splitlines()
```

- `open("words.txt")` opens the file.
- The `with` block automatically closes it when we're done (even if something goes wrong).
- `f.read()` reads the whole file as one long string.
- `.splitlines()` splits that string into a list of lines.

### Sets

```python
guessed_letters = set()     # empty set
guessed_letters.add("e")    # now: {"e"}
guessed_letters.add("e")    # still: {"e"} — no duplicates
"e" in guessed_letters      # True
```

A **set** is like a list but:

- No duplicates. Adding the same thing twice has no effect.
- No order. You can't say "the first item".
- Very fast for "is X in here?" checks.

Perfect for tracking which letters have been guessed. A list would work too, but a set is the right tool here.

### `set(secret).issubset(guessed_letters)`

Reads as "is every letter in the secret word also in guessed_letters?" — i.e., "have we guessed every letter?". If yes, the user wins.

### `" ".join(list)`

Takes a list of strings and glues them together with `" "` between each:

```python
" ".join(["p", "_", "_", "h", "o", "n"])
# -> "p _ _ h o n"
```

We use this to build the display string from a list of letters-or-underscores.

### How the word display evolves

If the secret is `"piano"` and the user has guessed nothing yet, `display_word` produces:

```
_ _ _ _ _
```

After they guess `a`:

```
_ _ _ a _
```

After `p`:

```
p _ _ a _
```

After `i`, `n`, `o`:

```
p i a n o
```

...at which point `set(secret).issubset(guessed_letters)` is `True` and the player wins.

### Constants

```python
MAX_WRONG = 6
HANGMAN_STAGES = [...]
```

Python doesn't really have true "constants", but by convention, **ALL-CAPS** names mean "don't change this". It's a signal to humans reading the code.

## Why this program is long-ish

Look at how it's organized:

- Constants at the top (the hangman art, `MAX_WRONG`).
- Small helper functions, each doing one thing:
  - `load_words` — read the word list.
  - `display_word` — build the "_ _ p t _ _ n" display.
  - `get_letter` — get a valid letter from the user.
  - `play_round` — run one full game.
- A tiny main section at the bottom that ties them together.

You're reading real code now. This is how grown-up Python looks.

## Run it

Make sure `words.txt` is in the same folder:

```
python3 solution.py
```

## Example run

Here's an abbreviated session where the secret word is `piano`. The word and number of wrong guesses remaining are shown each turn — the transcript below only shows a few turns to keep it readable.

```
$ python3 solution.py
Welcome to Hangman!

     +---+
     |   |
         |
         |
         |
         |
    =========
Word:  _ _ _ _ _
Wrong guesses left: 6

Guess a letter: a
Good guess — 'a' is in the word.

     +---+
     |   |
         |
         |
         |
         |
    =========
Word:  _ _ _ a _
Wrong guesses left: 6

Guess a letter: e
Sorry, 'e' is not in the word.

     +---+
     |   |
     O   |
         |
         |
         |
    =========
Word:  _ _ _ a _
Wrong guesses left: 5

Guess a letter: 5
Letters only, please.
Guess a letter: ab
Please type exactly one letter.
Guess a letter: a
You already guessed 'a'. Try another.
Guess a letter: p

... (a few good and bad guesses later) ...

Word:  p i a n o
Wrong guesses left: 3

You got it! The word was 'piano'. Great job!
```

And if you run out of guesses, you see the full hangman and the reveal:

```
     +---+
     |   |
     O   |
    /|\  |
    / \  |
         |
    =========
Out of guesses. The word was 'keyboard'. Better luck next time!
```

## Try these extensions

1. **Play again.** Wrap the main section in a loop so the user can keep playing new rounds.
2. **Difficulty levels.** Split `words.txt` into easy (short) and hard (long) words, and let the user choose.
3. **Show guessed letters.** Print the letters the user has already tried each turn, so they don't have to remember.
4. **Two-player mode.** Let one player type a word (hide it!) and have the other player guess. (Trickier than it looks — search "how to hide input in python terminal" and look up `getpass`.)
5. **Score.** Track wins and losses across rounds.
