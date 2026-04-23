# Project 7 — Contact Book

A contact book that lives in your terminal. You can add someone by name, look them up, list everyone, and remove people.

The menu pattern and the functions should feel familiar — it's Project 4's to-do list wearing a new outfit. The big new idea is the **dictionary**: a collection that maps a **name** to its **details**, so you can jump straight to the right person instead of scanning a list.

## What you'll learn

- **Dictionaries (`dict`)** — `{key: value}` pairs. Python's phone book.
- Creating one: `{}`, `{"name": "Alice"}`.
- Adding and updating: `d[key] = value`.
- Looking up: `d[key]` (crashes if missing) and `d.get(key)` (returns `None` if missing).
- Checking: `key in d`.
- Removing: `del d[key]`.
- **Looping with `.items()`** — `for key, value in d.items():` gives you both at once.
- **Dict of dicts** — a dict whose values are themselves dicts. Perfect for "one name → many fields".

## Why dictionaries?

Lists and dictionaries both hold many things, but the question they answer is different.

- A **list** answers: "*what's at position 3?*" You use it when order matters and you're happy to scan.
- A **dict** answers: "*what's Alice's phone number?*" You use it when each thing has a name (a key) and you want to jump straight to it.

Think of a real **phone book**. You don't read it page 1 to page 800 looking for your friend; you flip to their name. That's a dict.

Or think of a real dictionary (the book): you look up a word (**key**) and get its definition (**value**). That's where the name comes from.

## How the program works

```
contacts = {}              # start empty

loop:
    show the menu
    read the choice
    if 1: ask for name + phone + email, store them under the name
    if 2: ask for a name, print that contact's info
    if 3: print every contact
    if 4: ask for a name, remove it
    if 5: quit
```

## Key ideas, explained

### Dict basics

```python
# Make a dict.
contacts = {}                                       # empty
contacts = {"Alice": "555-1234"}                    # one entry

# Add / update.
contacts["Bob"] = "555-5678"                        # add
contacts["Alice"] = "555-0000"                      # overwrite

# Look up.
contacts["Alice"]                                   # -> "555-0000"
contacts["Zoe"]                                     # -> CRASH: KeyError

# Check before looking up.
"Alice" in contacts                                 # -> True
"Zoe" in contacts                                   # -> False

# Remove.
del contacts["Bob"]

# How many entries?
len(contacts)                                       # -> 1
```

The `[key]` syntax looks like list indexing, but a key can be any string (or number, or tuple). The key is a *label*, not a position.

### Looping with `.items()`

You've looped over lists already. Looping over a dict is just as easy, but you usually want both the key and the value:

```python
contacts = {"Alice": "555-1234", "Bob": "555-5678"}

for name, phone in contacts.items():
    print(f"{name}: {phone}")
```

prints:

```
Alice: 555-1234
Bob: 555-5678
```

`.items()` hands you pairs — one per loop step. (There are also `.keys()` and `.values()` if you only need one side, but `.items()` covers most cases.)

### Dict of dicts — storing more than one piece of info per key

One phone number per contact is nice, but contacts usually have a phone **and** an email. So instead of mapping name → phone, we map name → a small dict of details:

```python
contacts = {
    "Alice": {"phone": "555-1234", "email": "alice@example.com"},
    "Bob":   {"phone": "555-5678", "email": "bob@example.com"},
}

contacts["Alice"]                # -> {"phone": "555-1234", "email": "alice@..."}
contacts["Alice"]["phone"]       # -> "555-1234"
```

That `contacts["Alice"]["phone"]` reads as *"in the outer dict, look up Alice; in the dict that comes back, look up phone"*. Two lookups, right to left. You'll see this shape constantly in real code — JSON from an API is almost always a dict of dicts.

### `.get()` — a safer look-up

`contacts[name]` crashes if the name isn't there. `contacts.get(name)` returns `None` instead — and you can also give it a **default** to return:

```python
contacts.get("Alice")                    # -> "555-1234"
contacts.get("Zoe")                      # -> None
contacts.get("Zoe", "not found")         # -> "not found"
```

We mostly use `in` in this project (it reads like English), but `.get()` is the tool you reach for whenever "maybe there's a value, maybe there isn't" is the point.

## Run it

```
python3 solution.py
```

Try adding a couple of contacts, listing them, looking one up by name, removing one, and looking up a name that doesn't exist.

## Example run

```
$ python3 solution.py
Welcome to your contact book.

What would you like to do?
  1) Add a contact
  2) Look up a contact
  3) List all contacts
  4) Remove a contact
  5) Quit
Pick an option (1-5): 1
Name: Alice
Phone: 555-1234
Email: alice@example.com
Added Alice.

... (menu shown again) ...
Pick an option (1-5): 1
Name: Bob
Phone: 555-5678
Email: bob@example.com
Added Bob.

... (menu shown again) ...
Pick an option (1-5): 3
You have 2 contact(s):
  Alice  —  555-1234  —  alice@example.com
  Bob  —  555-5678  —  bob@example.com

... (menu shown again) ...
Pick an option (1-5): 2
Whose contact? Alice
Alice
  phone: 555-1234
  email: alice@example.com

... (menu shown again) ...
Pick an option (1-5): 2
Whose contact? Charlie
No contact named 'Charlie'.

... (menu shown again) ...
Pick an option (1-5): 4
Remove whose contact? Bob
Removed Bob.

... (menu shown again) ...
Pick an option (1-5): 5
Bye!
```

## Check yourself

Before moving on, can you answer these out loud?

1. Why do we store contacts as `{name: {"phone": ..., "email": ...}}` instead of as a list like `[name, phone, email]`? What do dictionaries make easier?
2. What's the difference between `contacts["Zoe"]` and `contacts.get("Zoe")` when `"Zoe"` isn't in the book?
3. In `for name, contact in contacts.items():`, what *is* `contact` — a string? a list? something else? How do you pull the phone number out of it?

## Try these extensions

1. **Edit an existing contact.** Add a menu option to change someone's phone or email without deleting and re-adding them. (Hint: just reassign the inner dict's field: `contacts[name]["phone"] = new_phone`.)
2. **Partial-name search.** Make "look up" match any contact whose name *contains* what the user typed, not just exact matches. Case-insensitive. (Hint: `.lower()` and the `in` operator on strings.)
3. **Sorted list.** When listing all contacts, show them alphabetically by name. (Hint: `sorted()` works on a dict's keys.)
4. **Multiple phones.** Let one contact have more than one phone number. The inner structure becomes `{"phones": ["555-1234", "555-9999"], "email": "..."}`. Now you're using a **list inside a dict inside a dict** — perfectly normal, but pay attention to each `[ ]` / `[ ]` step.
