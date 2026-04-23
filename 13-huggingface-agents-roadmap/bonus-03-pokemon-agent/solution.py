# Bonus 3 — toy Pokemon battle with a smolagents-driven trainer.
#
# Two Pokemon, fixed move sets, simple HP-based damage. The agent picks
# one move per turn. The architecture is the same as a "real" game agent
# would use — it's only the simulator that's tiny.

import os
import random
from dataclasses import dataclass, field
from typing import List

from smolagents import CodeAgent, HfApiModel, tool

DEMO_MODEL = "Qwen/Qwen2.5-Coder-32B-Instruct"


@dataclass
class Pokemon:
    name: str
    hp: int
    max_hp: int
    moves: List[str] = field(default_factory=list)


# Move database. (name, base_damage)
MOVES = {
    "Thunderbolt": 25,
    "Quick Attack": 12,
    "Iron Tail": 20,
    "Tackle": 10,
    "Vine Whip": 18,
}

# Battle state — module-level so the tools can read/mutate it.
PLAYER = Pokemon(name="Pikachu", hp=60, max_hp=60, moves=["Thunderbolt", "Quick Attack", "Iron Tail"])
OPPONENT = Pokemon(name="Bulbasaur", hp=70, max_hp=70, moves=["Vine Whip", "Tackle"])

BATTLE_LOG: List[str] = []


def render_state() -> str:
    return (
        f"Your Pokemon: {PLAYER.name} (HP: {PLAYER.hp}/{PLAYER.max_hp})\n"
        f"  Moves: {', '.join(f'{m} ({MOVES[m]} dmg)' for m in PLAYER.moves)}\n"
        f"Opponent: {OPPONENT.name} (HP: {OPPONENT.hp}/{OPPONENT.max_hp})\n"
        f"Recent: {' | '.join(BATTLE_LOG[-3:]) if BATTLE_LOG else 'battle just started'}"
    )


@tool
def use_move(move_name: str) -> str:
    """Use one of your Pokemon's moves against the opponent.

    Args:
        move_name: The move to use. Must be one of your Pokemon's known moves.
    """
    if move_name not in PLAYER.moves:
        return f"Error: {move_name} is not one of {PLAYER.name}'s moves ({PLAYER.moves})."
    damage = MOVES[move_name] + random.randint(-3, 3)
    OPPONENT.hp = max(0, OPPONENT.hp - damage)
    BATTLE_LOG.append(f"{PLAYER.name} used {move_name}, dealt {damage} damage")

    if OPPONENT.hp == 0:
        return f"{PLAYER.name} used {move_name}! It fainted {OPPONENT.name}! YOU WIN."

    # Opponent's turn: pick a random move.
    opp_move = random.choice(OPPONENT.moves)
    opp_damage = MOVES[opp_move] + random.randint(-3, 3)
    PLAYER.hp = max(0, PLAYER.hp - opp_damage)
    BATTLE_LOG.append(f"{OPPONENT.name} used {opp_move}, dealt {opp_damage} damage")

    if PLAYER.hp == 0:
        return f"{PLAYER.name} fainted! YOU LOSE."

    return render_state()


def main():
    if not (os.getenv("HF_TOKEN") or os.getenv("HUGGINGFACE_HUB_TOKEN")):
        raise SystemExit("Need a HF token. Run: huggingface-cli login")

    model = HfApiModel(DEMO_MODEL)
    agent = CodeAgent(tools=[use_move], model=model, max_steps=12)

    initial_state = render_state()
    task = (
        f"You are a Pokemon trainer. Win this battle.\n\n"
        f"{initial_state}\n\n"
        f"Use the use_move tool to attack. Keep attacking with your strongest move "
        f"until either Pokemon faints. Return a short summary at the end."
    )
    print("=" * 60)
    print("BATTLE START")
    print("=" * 60)
    print(initial_state)
    print()
    answer = agent.run(task)
    print("\n" + "=" * 60)
    print("AGENT'S SUMMARY")
    print("=" * 60)
    print(answer)


if __name__ == "__main__":
    main()
