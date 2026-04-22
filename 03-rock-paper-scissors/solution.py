# Rock Paper Scissors — play against the computer, as many rounds as you want.
#
# This project introduces FUNCTIONS: named blocks of reusable code.
# Notice how we split the program into small pieces, each doing ONE thing.
# That's the main lesson here.

import random


# A function is defined with "def name(inputs):".
# The "inputs" in the parentheses are called PARAMETERS — they're the data
# the function needs to do its job.
#
# "return" sends a value back to whoever called the function.
def get_computer_choice():
    # random.choice picks one item from a list at random.
    return random.choice(["rock", "paper", "scissors"])


def get_user_choice():
    # Keep asking until the user gives a valid answer.
    while True:
        answer = input("Choose rock, paper, or scissors (or 'quit' to stop): ")
        # .lower() turns "Rock" or "ROCK" into "rock", so we accept any capitalization.
        # .strip() removes any spaces the user accidentally typed around their answer.
        answer = answer.lower().strip()
        if answer in ["rock", "paper", "scissors", "quit"]:
            return answer
        print("I didn't understand that. Try again.")


def decide_winner(user, computer):
    # "tie" is the easy case: same choice.
    if user == computer:
        return "tie"
    # Otherwise there are three ways the user wins; everything else is a loss.
    user_wins = (
        (user == "rock" and computer == "scissors")
        or (user == "paper" and computer == "rock")
        or (user == "scissors" and computer == "paper")
    )
    if user_wins:
        return "user"
    return "computer"


# This is the MAIN part of the program — the flow of the game.
# Notice how it reads almost like English, because the hard parts are hidden
# inside the functions above.
print("Welcome to Rock Paper Scissors!")
user_score = 0
computer_score = 0

while True:
    user = get_user_choice()
    if user == "quit":
        break

    computer = get_computer_choice()
    print(f"Computer chose: {computer}")

    result = decide_winner(user, computer)
    if result == "tie":
        print("It's a tie!")
    elif result == "user":
        print("You win this round!")
        user_score = user_score + 1
    else:
        print("Computer wins this round!")
        computer_score = computer_score + 1

    print(f"Score — You: {user_score}, Computer: {computer_score}")
    print()

print()
print("Final score:")
print(f"  You:      {user_score}")
print(f"  Computer: {computer_score}")
print("Thanks for playing!")
