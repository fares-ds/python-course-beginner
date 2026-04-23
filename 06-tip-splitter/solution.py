# Tip Splitter — splits a bill (including a tip) between friends.
#
# This project introduces FLOATS: numbers with a decimal point.
# Until now, we've worked with whole numbers (int). Money and
# percentages need decimals — floats are how Python handles those.


def ask_for_float(question):
    # Keep asking until the user types a valid number.
    while True:
        answer = input(question)
        try:
            # float() is like int(), but allows decimals.
            # float("12.50") -> 12.5
            return float(answer)
        except ValueError:
            print("Please type a number (like 42 or 42.50).")


def ask_for_positive_int(question):
    while True:
        answer = input(question)
        try:
            number = int(answer)
            if number > 0:
                return number
            print("Please type a whole number greater than zero.")
        except ValueError:
            print("Please type a whole number.")


print("Tip Splitter")
print("============")

bill = ask_for_float("Bill total: $")
tip_percent = ask_for_float("Tip percentage (e.g. 18 for 18%): ")
people = ask_for_positive_int("How many people? ")

# Do the math. All of these are floats.
tip_amount = bill * (tip_percent / 100)
total = bill + tip_amount

# round(value, 2) rounds to 2 decimal places — useful for money.
# 50.15 / 3 gives 16.7166..., round(..., 2) gives 16.72.
per_person = round(total / people, 2)

# f-strings can format numbers:
#   {value:.2f}  -> exactly 2 decimal places.  1.6 shows as "1.60".
#   {value:g}    -> show naturally, drop trailing zeros. 18.0 shows as "18".
print()
print(f"Bill:        ${bill:.2f}")
print(f"Tip:         ${tip_amount:.2f}   ({tip_percent:g}% of bill)")
print(f"Total:       ${total:.2f}")
print(f"Per person:  ${per_person:.2f}   (split {people} ways)")
