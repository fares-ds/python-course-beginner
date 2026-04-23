# Persistent To-Do List — Project 4, but your tasks SURVIVE.
# Quit the program, come back tomorrow, your tasks are still there.
#
# This project introduces two new ideas:
#   1. Writing to a file (not just reading).
#   2. The JSON format — a simple way to save lists, dicts, strings, and numbers
#      as text so a program can load them back exactly as they were.

import json
import os

TASKS_FILE = "tasks.json"


def load_tasks():
    # If the file doesn't exist yet (first run), start with an empty list.
    if not os.path.exists(TASKS_FILE):
        return []
    # Open the file for reading, turn its JSON text back into a Python list.
    with open(TASKS_FILE) as f:
        return json.load(f)


def save_tasks(tasks):
    # Open the file for WRITING ("w") — creates it if missing, or replaces
    # whatever was in it. Then dump the list as JSON text.
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f)


def show_menu():
    print()
    print("What would you like to do?")
    print("  1) Add a task")
    print("  2) Remove a task")
    print("  3) View all tasks")
    print("  4) Quit")


def add_task(tasks):
    task = input("What's the task? ").strip()
    if task == "":
        print("Empty task, nothing added.")
        return
    tasks.append(task)
    save_tasks(tasks)
    print(f"Added: {task}")


def view_tasks(tasks):
    if len(tasks) == 0:
        print("Your to-do list is empty.")
        return
    print("Your tasks:")
    for number, task in enumerate(tasks, start=1):
        print(f"  {number}. {task}")


def remove_task(tasks):
    if len(tasks) == 0:
        print("Nothing to remove — the list is empty.")
        return
    view_tasks(tasks)
    answer = input("Which number would you like to remove? ").strip()
    try:
        number = int(answer)
    except ValueError:
        print("That's not a number.")
        return
    if number < 1 or number > len(tasks):
        print("That number isn't on the list.")
        return
    # The user sees "task #3"; internally that's tasks[2]. Convert here.
    index = number - 1
    removed = tasks.pop(index)
    save_tasks(tasks)
    print(f"Removed: {removed}")


# ---------- main ----------

tasks = load_tasks()
print("Welcome to your to-do list.")
if len(tasks) > 0:
    print(f"Loaded {len(tasks)} task(s) from {TASKS_FILE}.")

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
