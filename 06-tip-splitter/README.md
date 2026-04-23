# Project 6 — Tip Splitter

A quick restaurant helper: you give it the bill, a tip percentage, and the number of people. It tells you the tip, the total, and each person's share.

This is the first project of **Tier 2 — Fundamentals**. The tier-1 projects taught you the *shape* of programming (variables, decisions, loops, functions, lists, files). Tier 2 fills in the core data types and tools you're missing. We start with **floats** — numbers that have a decimal point. Until now, everything has been whole numbers. Money, percentages, measurements, and division results aren't always whole — so floats are unavoidable.

## What you'll learn

- **`float`** — numbers like `3.14`, `42.50`, `0.18`.
- **`float()`** — turning text like `"12.50"` into the number `12.5`. (Just like `int()`, but decimals allowed.)
- **Arithmetic with floats** — the usual `+`, `-`, `*`, `/` all work; as soon as one float is involved, the result is a float.
- **`round(value, 2)`** — rounding a number to 2 decimal places.
- **Formatting money with `:.2f`** — `f"${x:.2f}"` always shows exactly 2 decimals.
- **`:g`** — a format that hides trailing zeros, good for percentages.

## How the program works

```
ask for the bill total       (float)
ask for the tip percentage   (float)
ask for the number of people (positive whole number)

tip      = bill * (tip_percent / 100)
total    = bill + tip
share    = round(total / people, 2)

print everything with dollar signs and 2 decimals.
```

## Key ideas, explained

### Floats vs ints

```python
int("42")         # -> 42        (a whole number)
float("42")       # -> 42.0      (a whole number, but stored as a float)
float("42.50")    # -> 42.5      (a float; int("42.50") would CRASH)
```

Why two types? Ints are exact and fast; floats handle decimals. You can spot the difference in Python: if a number has a dot, it's a float.

When you do math, if *any* number involved is a float, the result is a float:

```python
10 / 3        # -> 3.3333333333333335   (float; / always gives a float)
10.0 + 5      # -> 15.0                 (float, because 10.0 is a float)
10 + 5        # -> 15                   (int, because both inputs are ints)
```

### Numbers aren't always clean

```python
10 / 3        # 3.3333333333333335
0.1 + 0.2     # 0.30000000000000004  (surprise!)
```

That long tail is real. Computers store decimal numbers in binary, and some decimals can't be represented exactly. 99% of the time you won't care — but you do notice when you try to print `$3.33` and get `$3.3333333333333335` instead.

That's what `round()` and `:.2f` are for.

### `round(value, places)`

```python
round(3.3333, 2)     # -> 3.33
round(1.6666, 2)     # -> 1.67
round(3.5, 0)        # -> 4
```

It rounds to the given number of decimal places, using the normal rules you learned in school. (One nerdy footnote: on ties like `round(2.5)`, Python gives `2`, not `3` — it rounds to the nearest *even* number. You'll meet this once in a blue moon.)

### Formatting money with `:.2f`

Inside an f-string, you can tell Python *how* to display a value. `:.2f` means "floating-point number, 2 digits after the decimal":

```python
price = 5
f"${price:.2f}"        # -> "$5.00"

price = 1.6
f"${price:.2f}"        # -> "$1.60"

price = 1.6666
f"${price:.2f}"        # -> "$1.67"   (rounded for display)
```

So `:.2f` does two things at once: pads with zeros when there aren't enough decimals, and rounds when there are too many. Exactly what money wants.

`round()` changes the **value**; `:.2f` only changes how it's **displayed**. Our program uses both: `round()` to store a clean per-person number, and `:.2f` to make sure the displayed bill still shows two decimals even if the number happens to be something like `42.5`.

### Formatting naturally with `:g`

For the tip percentage, we don't want to show `18.00%` — that's ugly. `:g` strips trailing zeros:

```python
f"{18.0:g}"         # -> "18"
f"{18.5:g}"         # -> "18.5"
f"{0.075:g}"        # -> "0.075"
```

Use `:g` when you want the number to look "natural", and `:.2f` when you want money-clean.

## Run it

```
python3 solution.py
```

Try some weird inputs: `banana` for the bill, `0` for number of people, `18.5` for the tip percent.

## Example run

```
$ python3 solution.py
Tip Splitter
============
Bill total: $42.50
Tip percentage (e.g. 18 for 18%): 18
How many people? 3

Bill:        $42.50
Tip:         $7.65   (18% of bill)
Total:       $50.15
Per person:  $16.72   (split 3 ways)
```

Notice: 3 people × $16.72 = $50.16, but the total was $50.15. That one-cent gap is real — no way around it when $50.15 doesn't divide evenly by 3. It's a **rounding gap**. Extension #2 below asks you to fix it.

## Check yourself

Before moving on, can you answer these out loud?

1. Why does `float("42.50")` work but `int("42.50")` crash? What's the difference between these two types?
2. What does `:.2f` do to the number `5`? What does it do to `1.6666`? What does it do differently from `round(value, 2)`?
3. If the bill is $10 and there are 3 people paying, what does Python give you for `10 / 3`? How does the final output end up showing as `$3.33` instead of that long decimal?

## Try these extensions

1. **Round up to the nearest dollar.** Add a "round up?" option: if yes, round each person's share up to the next whole dollar. (Look up `math.ceil()`.)
2. **Fix the rounding gap.** Compute everyone's share as `round(total / people, 2)`, then figure out how many cents are still missing (total − share × people). Assign the leftover cents one at a time to the first few people so the math balances exactly. (Hint: `%` — modulo — gives you remainders, and is very handy here.)
3. **Smart default.** If the user just presses Enter for the tip percent, default to 18. (Hint: check if the input string is `""`.)
4. **Tax-aware.** Some places separate tax from tip. Ask for a tax rate too, and compute the tip on the **pre-tax** amount, then add tax after.
