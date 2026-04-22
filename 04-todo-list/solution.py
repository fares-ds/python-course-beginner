# To-Do List — a simple task tracker that runs in your terminal.
#
# New idea in this project: LISTS. A list is Python's way of holding many
# things (any things) in a single variable, in order.
#
# Note: when you quit the program, your tasks disappear. Saving to a file
# is a great follow-up project once you've finished this one.


def show_menu():
    print()
    print("What would you like to do?")
    print("  1) Add a task")
    print("  2) Remove a task")
    print("  3) View all tasks")
    print("  4) Quit")


def view_tasks(tasks):
    # len() tells you how many items are in a list.
    if len(tasks) == 0:
        print("You have no tasks yet. Nice and clean!")
        return

    print("Your tasks:")
    # enumerate() walks through the list AND gives you a number for each item.
    # We start numbering at 1 so it looks friendlier than starting at 0.
    for number, task in enumerate(tasks, start=1):
        print(f"  {number}. {task}")


def add_task(tasks):
    task = input("What's the task? ").strip()
    if task == "":
        print("You didn't type anything. Nothing was added.")
        return
    # .append() adds an item to the END of a list.
    tasks.append(task)
    print(f"Added: {task}")


def remove_task(tasks):
    if len(tasks) == 0:
        print("Nothing to remove — your list is empty.")
        return

    view_tasks(tasks)
    answer = input("Which number would you like to remove? ").strip()

    try:
        number = int(answer)
    except ValueError:
        print("That's not a number.")
        return

    # Python lists are "zero-indexed" — the first item is at position 0.
    # The user sees task #1, but internally it's tasks[0], so we subtract 1.
    index = number - 1
    if index < 0 or index >= len(tasks):
        print("That number isn't on the list.")
        return

    # .pop(index) removes AND returns the item at that position.
    removed = tasks.pop(index)
    print(f"Removed: {removed}")


# ---- Main program ----

# An empty list. We'll fill it as the user adds tasks.
tasks = []
print("Welcome to your to-do list.")

while True:
    show_menu()
    choice = input("Pick an option (1-4): ").strip()

    if choice == "1":
        add_task(tasks)
    elif choice == "2":
        remove_task(tasks)
    elif choice == "3":
        view_tasks(tasks)
    elif choice == "4":
        print("Bye!")
        break
    else:
        print("Please pick 1, 2, 3, or 4.")
