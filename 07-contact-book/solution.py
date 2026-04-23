# Contact Book — a simple address book that lives in your terminal.
#
# This project introduces DICTIONARIES: a collection that maps a KEY
# (like a name) to a VALUE (like a phone number).
# If a list is a shopping list, a dictionary is a phone book — you flip
# to the name, and the number is right there.


def show_menu():
    print()
    print("What would you like to do?")
    print("  1) Add a contact")
    print("  2) Look up a contact")
    print("  3) List all contacts")
    print("  4) Remove a contact")
    print("  5) Quit")


def add_contact(contacts):
    name = input("Name: ").strip()
    if name == "":
        print("Name can't be empty.")
        return
    # "in" works on dicts the same way it works on lists.
    # It checks whether a KEY is in the dict.
    if name in contacts:
        print(f"'{name}' already exists. Remove it first to replace.")
        return
    phone = input("Phone: ").strip()
    email = input("Email: ").strip()
    # Each contact is a small dict of its own — so `contacts` is a dict of dicts.
    contacts[name] = {"phone": phone, "email": email}
    print(f"Added {name}.")


def find_contact(contacts):
    name = input("Whose contact? ").strip()
    if name not in contacts:
        print(f"No contact named '{name}'.")
        return
    # contacts[name] gives us the inner dict. Then we pull phone/email from it.
    contact = contacts[name]
    phone = contact["phone"]
    email = contact["email"]
    print(name)
    print(f"  phone: {phone}")
    print(f"  email: {email}")


def list_all(contacts):
    if len(contacts) == 0:
        print("Your contact book is empty.")
        return
    print(f"You have {len(contacts)} contact(s):")
    # .items() gives us each (key, value) pair as we loop.
    # Here, `name` is the key and `contact` is the inner dict.
    for name, contact in contacts.items():
        phone = contact["phone"]
        email = contact["email"]
        print(f"  {name}  —  {phone}  —  {email}")


def remove_contact(contacts):
    name = input("Remove whose contact? ").strip()
    if name not in contacts:
        print(f"No contact named '{name}'.")
        return
    # `del` removes a key-value pair from a dict.
    del contacts[name]
    print(f"Removed {name}.")


# ---------- main ----------

contacts = {}   # an empty dict. Ready for entries.
print("Welcome to your contact book.")

while True:
    show_menu()
    choice = input("Pick an option (1-5): ").strip()
    if choice == "1":
        add_contact(contacts)
    elif choice == "2":
        find_contact(contacts)
    elif choice == "3":
        list_all(contacts)
    elif choice == "4":
        remove_contact(contacts)
    elif choice == "5":
        print("Bye!")
        break
    else:
        print("Please pick 1, 2, 3, 4, or 5.")
