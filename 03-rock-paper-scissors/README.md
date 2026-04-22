# Project 3 — Rock Paper Scissors

Play Rock Paper Scissors against the computer, over and over, tracking the score.

The rules you already know:

- Rock crushes scissors.
- Scissors cuts paper.
- Paper covers rock.
- Same choice = tie.

The real lesson here isn't the game. It's **functions** — the most important idea in programming after variables and loops.

## What you'll learn

- **Functions** — named, reusable blocks of code (`def name(...):`).
- **Parameters** — the inputs a function takes.
- **`return`** — how a function sends a result back.
- **Decomposition** — breaking a big program into small pieces.
- **Boolean logic** — `and`, `or` for combining conditions.
- String methods — `.lower()` and `.strip()`.

## Why functions matter

Without functions, the main body of the program would be a giant pile of `if`-statements and input prompts all tangled together. Hard to read, hard to change.

With functions, the main loop reads almost like English:

```python
user = get_user_choice()
computer = get_computer_choice()
result = decide_winner(user, computer)
```

Each function does **one thing** and has a name that says what it does. If something goes wrong with the decision logic, you know to look in `decide_winner` — you don't have to re-read the whole program.

This is how professional code is written. Start practicing now.

## How the program works

```
define helper functions:
    get_computer_choice   -> returns "rock", "paper", or "scissors"
    get_user_choice       -> asks the user, returns their choice (or "quit")
    decide_winner(a, b)   -> returns "tie", "user", or "computer"

main loop:
    get user choice. if they quit, stop.
    get computer choice.
    decide who won.
    update the score.
    print the score.
```

## Key ideas, explained

### Defining a function

```python
def get_computer_choice():
    return random.choice(["rock", "paper", "scissors"])
```

- `def` starts the definition.
- `get_computer_choice` is the name.
- The parentheses `()` hold the parameters (this one has none).
- Everything indented below the `def` line is inside the function.
- `return` sends a value back.

You **call** the function by writing its name with parentheses: `get_computer_choice()`.

### Parameters

```python
def decide_winner(user, computer):
    ...
```

`user` and `computer` are placeholders. When you call `decide_winner("rock", "paper")`, Python sets `user = "rock"` and `computer = "paper"` inside the function, then runs the code.

### `and` / `or`

```python
user_wins = (
    (user == "rock" and computer == "scissors")
    or (user == "paper" and computer == "rock")
    or (user == "scissors" and computer == "paper")
)
```

- `and` — both sides must be true.
- `or` — at least one side must be true.

This is just math-for-logic. We're building one big yes/no question out of smaller ones.

### `.lower()` and `.strip()`

Strings have **methods** — little functions attached to them. You call them with a dot:

- `"Rock".lower()` → `"rock"`
- `"  rock  ".strip()` → `"rock"`

Chaining them (`answer.lower().strip()`) is a friendly way to accept messy input.

## Run it

```
python3 solution.py
```

Type `quit` when you're done playing.

## Try these extensions

1. **Best of 3.** Stop the game automatically when someone hits 3 wins.
2. **Rock, Paper, Scissors, Lizard, Spock.** Add two more options. You'll need to expand the win logic. (Google "Lizard Spock" if you don't know the rules.)
3. **Smarter computer.** Instead of picking randomly, make the computer pick the move that would beat the user's *previous* choice. (First round, still random.)
4. **Play again loop.** When the user quits, ask "Play another match?" and reset the score if they say yes.
