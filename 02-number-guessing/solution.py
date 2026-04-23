# Number Guessing Game.
# The computer picks a secret number; you try to guess it.

# "import" lets us use code other people have already written.
# The "random" module knows how to pick random numbers.
import random

# Pick a whole number between 1 and 100 (both ends included).
secret = random.randint(1, 100)

# We'll count how many guesses the user takes.
attempts = 0

print("I'm thinking of a number between 1 and 100.")
print("Can you guess it?")

# A "while True:" loop runs forever — until we explicitly break out of it.
while True:
    answer = input("Your guess: ")

    # input() always gives us a string (text). To compare it as a number,
    # we convert it using int(). But if the user typed "banana", int() would
    # crash the program — so we wrap it in try/except to handle that gracefully.
    try:
        guess = int(answer)
    except ValueError:
        print("That's not a whole number. Try again.")
        continue  # "continue" jumps back to the top of the loop.

    attempts = attempts + 1

    if guess < secret:
        print("Too low.")
    elif guess > secret:
        print("Too high.")
    else:
        # The only remaining option is guess == secret.
        print(f"Got it! The number was {secret}.")
        print(f"You took {attempts} guesses.")
        break  # "break" exits the loop, ending the game.
