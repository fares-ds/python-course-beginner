# Rock Paper Scissors — messy first draft (version 1).
#
# Before we learn functions, let's build the whole game in one big flow.
# It WORKS — but notice how tangled it gets. Play a round or two, then
# open solution.py to see how we clean it up with functions in version 2.

import random

print("Welcome to Rock Paper Scissors!")
print("Type rock, paper, scissors, or quit.")
user_score = 0
computer_score = 0

while True:
    # --- Ask the user for a choice, looping until it's one of the valid words. ---
    while True:
        user = input("Your choice: ")
        if user == "rock" or user == "paper" or user == "scissors" or user == "quit":
            break
        print("I didn't understand that. Try again.")

    # --- If they quit, stop the whole game. ---
    if user == "quit":
        break

    # --- Pick the computer's move. ---
    computer = random.choice(["rock", "paper", "scissors"])
    print(f"Computer chose: {computer}")

    # --- Figure out who won this round. ---
    if user == computer:
        print("It's a tie!")
    elif user == "rock" and computer == "scissors":
        print("You win this round!")
        user_score = user_score + 1
    elif user == "paper" and computer == "rock":
        print("You win this round!")
        user_score = user_score + 1
    elif user == "scissors" and computer == "paper":
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
