# Mad Libs — your first Python program.
# This asks you for a few words, then drops them into a silly story.

print("Welcome to Mad Libs!")
print("Give me a few words and I'll make you a story.")
print()  # an empty print() prints a blank line

# input() shows a message and waits for the user to type something and press Enter.
# Whatever they type is stored in a variable (a name we give to a piece of data).
name = input("Your name: ")
adjective = input("An adjective (a describing word, like 'sparkly'): ")
animal = input("An animal: ")
verb = input("A verb ending in -ing (like 'dancing'): ")
place = input("A place: ")

# A blank line before the story, so it stands out.
print()
print("--- Your story ---")

# An f-string (notice the f before the quote) lets us drop variables into text
# by wrapping them in curly braces { }.
print(f"One morning, {name} woke up to find a {adjective} {animal} in the kitchen.")
print(f"The {animal} was {verb} on the table and refused to leave.")
print(f"Eventually they both moved to {place} and lived happily ever after.")
