# Hangman — the capstone project.
#
# The computer picks a random word from a file. You guess letters, one at a time.
# Every wrong guess adds a body part to the hangman drawing. Six wrong guesses
# and you lose. Guess the whole word before then and you win.
#
# This program combines everything from the previous projects:
#   - input/output (project 1)
#   - if/else, loops, randomness (project 2)
#   - functions (project 3)
#   - lists (project 4)
# ...plus a few new friends: reading a file, sets, and slightly trickier strings.

import random


# The hangman drawing, stage by stage. HANGMAN_STAGES[0] is the empty gallows;
# HANGMAN_STAGES[6] is the full "you lose" drawing.
# (A list of strings. Each string uses \n for line breaks and triple quotes
# to span multiple lines.)
HANGMAN_STAGES = [
    """
     +---+
     |   |
         |
         |
         |
         |
    =========""",
    """
     +---+
     |   |
     O   |
         |
         |
         |
    =========""",
    """
     +---+
     |   |
     O   |
     |   |
         |
         |
    =========""",
    """
     +---+
     |   |
     O   |
    /|   |
         |
         |
    =========""",
    """
     +---+
     |   |
     O   |
    /|\\  |
         |
         |
    =========""",
    """
     +---+
     |   |
     O   |
    /|\\  |
    /    |
         |
    =========""",
    """
     +---+
     |   |
     O   |
    /|\\  |
    / \\  |
         |
    =========""",
]

MAX_WRONG = 6  # six wrong guesses = lose


def load_words(filename):
    # open(...) opens a file. The "with" block closes it automatically when
    # we're done. .read() reads the whole file as one big string, and
    # .splitlines() breaks it into a list of lines (without the newline chars).
    with open(filename) as f:
        lines = f.read().splitlines()

    # Clean up each line: remove spaces around it, make it lowercase, and skip
    # any blank lines. We build a new list called "words" by appending one item
    # at a time — exactly the pattern you used in the To-Do List project.
    words = []
    for line in lines:
        cleaned = line.strip().lower()
        if cleaned != "":
            words.append(cleaned)
    return words


def display_word(secret, guessed_letters):
    # Build the "_ _ a _ a _" display by showing each letter if we've guessed it,
    # or an underscore otherwise.
    shown = []
    for letter in secret:
        if letter in guessed_letters:
            shown.append(letter)
        else:
            shown.append("_")
    # " ".join(list) glues the items together with a space between each.
    return " ".join(shown)


def get_letter(already_guessed):
    # Loop until the user gives us a single letter we haven't already tried.
    while True:
        answer = input("Guess a letter: ").lower().strip()
        if len(answer) != 1:
            print("Please type exactly one letter.")
            continue
        if not answer.isalpha():
            print("Letters only, please.")
            continue
        if answer in already_guessed:
            print(f"You already guessed '{answer}'. Try another.")
            continue
        return answer


def play_round(secret):
    # A SET is like a list, but with no duplicates and no order. Perfect for
    # "which letters have we guessed?" because we only care whether a letter
    # is in there, not how many times or in what order.
    guessed_letters = set()
    wrong_count = 0

    while True:
        print(HANGMAN_STAGES[wrong_count])
        print("Word: ", display_word(secret, guessed_letters))
        print(f"Wrong guesses left: {MAX_WRONG - wrong_count}")
        print()

        letter = get_letter(guessed_letters)
        guessed_letters.add(letter)

        if letter in secret:
            print(f"Good guess — '{letter}' is in the word.")
        else:
            wrong_count += 1
            print(f"Sorry, '{letter}' is not in the word.")

        # Win? Every letter in the secret has been guessed.
        # set(secret) is the set of unique letters in the word; if all of those
        # are in guessed_letters, we've won.
        if set(secret).issubset(guessed_letters):
            print()
            print(f"You got it! The word was '{secret}'. Great job!")
            return

        # Lose?
        if wrong_count >= MAX_WRONG:
            print(HANGMAN_STAGES[wrong_count])
            print(f"Out of guesses. The word was '{secret}'. Better luck next time!")
            return


# ---- Main program ----

print("Welcome to Hangman!")
words = load_words("words.txt")
secret = random.choice(words)
play_round(secret)
