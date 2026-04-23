# Bonus Unit 3 — Agents in Games with Pokemon

The "for fun" capstone. Build an agent that plays Pokemon battles. No serious career relevance — just a great portfolio piece because strangers actually click on it.

**Course link:** [Bonus 3 on the HF docs](https://huggingface.co/learn/agents-course/bonus-unit3/introduction)

**Pick this if:** you want a portfolio piece that gets people excited. Or you just like Pokemon.

## What you'll learn

- The state-of-the-art in **LLMs as game-playing agents** — the chunk of work that produced Voyager, SIMA, Cradle, and the Pokemon-specific systems.
- How to bridge an LLM to a structured game environment via tools.
- Game-state representation — turning a battle screen into text the agent can reason about.

## What's in this folder

- [`solution.py`](solution.py) — a tiny "battle arena" simulator (5 moves, 2 Pokemon) plus a smolagents agent that picks moves. Toy-scale, but the architecture is the same as the real course's example.
- [`requirements.txt`](requirements.txt) — `smolagents`.

## Setup

```bash
pip install -r requirements.txt
huggingface-cli login
```

## Run it

```bash
python3 solution.py
```

Expected: a battle plays out turn by turn. The agent picks each move based on the current state. Both Pokemon take damage; one faints; the battle ends.

## Key concepts

### Game state as text
The agent can't see pixels (well, it can with vision models, but expensive). The trick is to **describe the state in text**:

```
Your Pokemon: Pikachu (HP: 35/35)
  Moves: Thunderbolt (90 dmg, electric), Quick Attack (40 dmg, normal), ...
Opponent: Bulbasaur (HP: 45/45, type: grass)
  Last move: Vine Whip
```

Now the LLM can reason about it.

### Tools as actions
Each legal action is a tool. `use_move(name)`, `switch_pokemon(name)`, etc. The agent picks one per turn.

### Why this is harder than it looks
- **Long games**: a 30-turn battle is 30 LLM calls. Cost adds up.
- **Memory**: the agent needs to remember what the opponent has done. Use the chat history; don't re-summarize from scratch each turn.
- **Determinism vs creativity**: against a tough opponent, a deterministic agent loses. Some randomness in move selection helps. (This is true of poker, Go, and everything game-theoretic.)

### State of the art
The course's official Pokemon battle agent uses a more elaborate stack — image vision for the screen, an emulator integration, multi-turn memory. The version in this folder is a toy simulation just to teach the architecture. For the real thing, follow the official notebook.

## Mini-tasks

1. Run `solution.py`. Watch the agent's move selection over a battle. Does it play sensibly?
2. Add a third move type ("status moves" that don't deal damage but inflict effects). Does the agent learn to use them?
3. Run two battles back to back: same agent, same opponent, no memory between. Did the agent's strategy change? Should it have?

## Focus vs skim

- **Focus:** the architecture pattern (text state + tools-as-actions + a loop).
- **Skim:** Pokemon-specific mechanics. The pattern generalizes to chess, Catan, MUDs, anything turn-based.

## Common pitfalls

- **Cost** — long battles + many runs = real money. Set hard caps in your code.
- **Vision when text would do** — adding vision multiplies cost per turn ~3×. Use it only if the text representation is genuinely insufficient.
- **No randomness in move choice** — a deterministic agent is exploitable. Sample sometimes.

## Expected outcome

A toy Pokemon agent + the architecture template for any turn-based-game agent you want to build. (Connect Four, chess, Hangman from Project 5 in this very repo.)

## Next

You're done with the course. Pick a capstone project from the parent README and ship it.
