# Project 3 — Rock Paper Scissors

Play Rock Paper Scissors against the computer, over and over, tracking the score.

The rules you already know:

- Rock crushes scissors.
- Scissors cuts paper.
- Paper covers rock.
- Same choice = tie.

The real lesson here isn't the game. It's **functions** — the most important idea in programming after variables and loops.

This project comes in **two versions**, and you should look at them in order:

1. [`solution_v1_messy.py`](solution_v1_messy.py) — the whole game in one big block. No functions. It works, but it's tangled.
2. [`solution.py`](solution.py) — the same game, cleaned up using functions.

We're doing it this way on purpose. Reading v1 first, then v2, is how you'll *feel* why functions exist. If we jumped straight to the tidy version, "use functions" would sound like a rule. After seeing v1, it'll feel like relief.

## What you'll learn

- **Functions** — named, reusable blocks of code (`def name(...):`).
- **Parameters** — the inputs a function takes.
- **`return`** — how a function sends a result back.
- **Decomposition** — breaking a big program into small pieces.
- **Boolean logic** — `and`, `or` for combining conditions.
- String methods — `.lower()` and `.strip()`.

## Start here: play the messy version

Run `solution_v1_messy.py` and play a few rounds. The game works. Now **read it**. Some things to notice:

- The validation loop (asking until the user types a real choice) sits *inside* the main game loop. Loop-inside-a-loop — ugly.
- There are three `elif` branches that all do the same thing: print "You win this round!" and add 1 to the score. Near-identical lines copy-pasted.
- If you wanted to describe what the main loop does in one sentence, you'd struggle. Too much is happening in one place.

The program is **not wrong**. It's just hard to read, hard to change, and hard to explain. Now imagine a bug appears — where would you even look?

## Why functions matter

Think of a function as a **recipe**. You write it down once — the ingredients (parameters) and the steps — and give it a name. Any time you want that dish again, you don't re-derive the recipe; you just call it by name.

In `solution.py`, the messy v1 is **refactored** — reorganized without changing what it does — into three small, named pieces:

- `get_user_choice()` — asks the user, keeps asking until valid, returns their answer.
- `get_computer_choice()` — picks rock/paper/scissors at random.
- `decide_winner(user, computer)` — returns `"tie"`, `"user"`, or `"computer"`.

The main loop then reads almost like English:

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

Some sample calls and what they return:

```python
decide_winner("rock", "scissors")     # -> "user"       (rock crushes scissors)
decide_winner("rock", "paper")        # -> "computer"   (paper covers rock)
decide_winner("paper", "paper")       # -> "tie"
```

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

Both versions play the same game. Run the messy one first, then the tidy one:

```
python3 solution_v1_messy.py
python3 solution.py
```

Type `quit` when you're done playing.

## Example run

The computer picks randomly, so your run will differ — but you'll see the same pattern:

```
$ python3 solution.py
Welcome to Rock Paper Scissors!
Choose rock, paper, or scissors (or 'quit' to stop): rock
Computer chose: scissors
You win this round!
Score — You: 1, Computer: 0

Choose rock, paper, or scissors (or 'quit' to stop): Rock
Computer chose: rock
It's a tie!
Score — You: 1, Computer: 0

Choose rock, paper, or scissors (or 'quit' to stop): banana
I didn't understand that. Try again.
Choose rock, paper, or scissors (or 'quit' to stop): paper
Computer chose: scissors
Computer wins this round!
Score — You: 1, Computer: 1

Choose rock, paper, or scissors (or 'quit' to stop): quit

Final score:
  You:      1
  Computer: 1
Thanks for playing!
```

A few things to notice:

- Typing `Rock` (capital R) still worked, because of `.lower()`.
- Typing `banana` didn't crash — it just re-asked.
- `quit` ends the game and prints the final score.

## Check yourself

Before moving on, can you answer these out loud?

1. Compare `solution_v1_messy.py` to `solution.py`. Point to **one specific thing** that got clearer after the refactor — and one thing that's exactly the same.
2. Why are `get_user_choice` and `get_computer_choice` separate functions, when they both just return one of `"rock"`, `"paper"`, `"scissors"`?
3. In `decide_winner(user, computer)`, what would happen if you accidentally called it as `decide_winner(computer, user)` (arguments swapped)?
4. What would happen if you removed the `return` statement from `get_computer_choice`? What would the function hand back?

## Try these extensions

1. **Best of 3.** Stop the game automatically when someone hits 3 wins.
2. **Rock, Paper, Scissors, Lizard, Spock.** Add two more options. You'll need to expand the win logic. (Google "Lizard Spock" if you don't know the rules.)
3. **Smarter computer.** Instead of picking randomly, make the computer pick the move that would beat the user's *previous* choice. (First round, still random.)
4. **Play again loop.** When the user quits, ask "Play another match?" and reset the score if they say yes.
