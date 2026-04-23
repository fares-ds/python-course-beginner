# Project 9 — Pomodoro Timer

A simple focus timer. 25 minutes of work, 5 minutes of break. The remaining time ticks down, one second at a time, right there in your terminal. When the time is up, the program says so and moves on.

This is the first project where your code **takes real time to run**. Until now, programs finished instantly — you pressed Enter and got the answer. Here, the program tells Python to *wait*, second by second, and watches the real clock. That's a new superpower.

## What you'll learn

- **`time.sleep(seconds)`** — pause the program for a given number of seconds.
- **`datetime.now()`** — the computer's current date and time, as a `datetime` object.
- **Subtracting two `datetime`s → a `timedelta`** — "how long did that take?" answered automatically.
- **`.strftime("%H:%M:%S")`** — format a `datetime` as a human-readable string.
- **`//` and `%`** — whole-number division and remainder. Perfect for converting seconds into minutes + seconds.
- **`{value:02d}`** — format an integer padded with zeros to 2 digits.
- **`print(..., end="\r", flush=True)`** — a live, in-place countdown on a single line.

## How the program works

```
define countdown(label, minutes):
    remember the start time
    say "starting"
    seconds_left = minutes * 60
    while seconds_left > 0:
        print the remaining time (overwriting the same line)
        sleep 1 second
        seconds_left = seconds_left - 1
    remember the end time
    say "done" and how long it took

main:
    countdown("Work",  25)
    countdown("Break", 5)
```

Two calls to the same function, different arguments — the same pattern you've seen since Project 3.

## Key ideas, explained

### `time.sleep(seconds)`

```python
import time

print("one")
time.sleep(1)       # pause for 1 second
print("two")
time.sleep(0.5)     # pause for half a second
print("three")
```

`time.sleep` is the "do nothing for a while" instruction. Your program just… waits. Nothing else happens. When the requested time has elapsed, the next line runs.

This is boring-sounding and absolutely essential. Anything that needs to happen "once a second" or "wait a moment before retrying" uses `time.sleep`.

### `datetime.now()` and `timedelta`

```python
from datetime import datetime

started = datetime.now()       # e.g. 2026-04-23 14:03:22.147321
# ... do some work ...
finished = datetime.now()      # e.g. 2026-04-23 14:28:22.891055

elapsed = finished - started   # subtracting two datetimes gives a `timedelta`
print(elapsed)                 # e.g. 0:25:00.743734
```

A `datetime` is just "a moment in time". When you subtract two of them, Python does the math for you and hands back a `timedelta` — "how long between them". Print it and you get `H:MM:SS.microseconds`. Not perfectly pretty, but honest and readable.

> The `from datetime import datetime` line is a slightly different shape of import than `import random`. It says: "from the `datetime` module, give me the `datetime` class directly." We do it this way so we can just write `datetime.now()` instead of `datetime.datetime.now()`. That's because the module and the class inside it share the same name. A little annoying, but you'll see it often enough.

### `.strftime()` — formatting a datetime

`datetime.now()` prints a lot of information. Usually you only want part of it:

```python
now = datetime.now()
now.strftime("%H:%M:%S")      # -> "14:03:22"
now.strftime("%H:%M")         # -> "14:03"
now.strftime("%Y-%m-%d")      # -> "2026-04-23"
```

`strftime` stands for "**str**ing **f**rom **time**". Each `%X` is a placeholder — `%H` for hour, `%M` for minute, `%S` for second, `%Y` for year, and so on. You never need to memorize them; look them up when you want them.

### Converting seconds to "mm:ss"

```python
total_seconds = 125

minutes = total_seconds // 60     # 2      (whole-number division)
seconds = total_seconds % 60      # 5      (the remainder)

f"{minutes:02d}:{seconds:02d}"    # "02:05"
```

- **`//`** — divide and throw away the fractional part. `125 // 60` is `2`, not `2.08`.
- **`%`** — divide and keep *only* the remainder. `125 % 60` is `5`.
- **`{value:02d}`** — the `:02d` format spec means "integer (`d`), pad with zeros (`0`) so the result is at least 2 wide". So `5` becomes `"05"`, `12` stays `"12"`, `125` becomes `"125"` (never truncated — "at least 2 wide", not "exactly 2").

Together, this turns any second count into a clean `mm:ss` display.

### A one-line countdown with `\r`

When you `print("hello")`, two things happen: the text is shown, and the cursor moves to the **next line**. So if you did this in a loop, you'd get one new line per second — a long, scrolling list.

For a real countdown, we want each tick to **replace** the previous one. Two small tricks:

```python
print(f"  {mmss} remaining   ", end="\r", flush=True)
```

- **`end="\r"`** — instead of ending with a newline, end with a **carriage return**. `\r` moves the cursor back to the start of the *same* line, so the next `print` overwrites this one.
- **`flush=True`** — normally, Python collects text in a buffer and shows it all at once when it sees a newline. `flush=True` says "no, show this right now." Without it, your countdown would sit invisible until the program ended.

After the countdown finishes, we do one plain `print()` to move to a fresh line — otherwise the next message would land on top of the last tick.

## Run it

```
python3 solution.py
```

Full run takes 30 minutes (25 + 5). If you just want to see the behaviour, open `solution.py` and temporarily change the constants at the top:

```python
WORK_MINUTES = 1     # was 25
BREAK_MINUTES = 1    # was 5
```

Now you have a 2-minute demo. **Remember to change them back** when you're actually using the timer.

To stop the program early, press `Ctrl + C`.

## Example run (with shortened durations)

Using `WORK_MINUTES = 0` for the demo doesn't work (the loop wouldn't run), so here's what a short session looks like if you change it to `WORK_MINUTES = 1`:

```
$ python3 solution.py
Pomodoro Timer
==============
One work session of 1 minutes, then a 1-minute break.

Work: 1 minutes. Started at 14:03:22.
  00:00 remaining
Time! Work finished at 14:04:22.
That took 0:01:00.027193.

Break: 1 minutes. Started at 14:04:22.
  00:00 remaining
Time! Break finished at 14:05:22.
That took 0:01:00.014861.

Session complete. Good job.
```

(In reality the `00:00 remaining` line is the *last* of 60 frames — each second, the same line was overwritten with `00:59`, `00:58`, … down to `00:00`. You only see the final frame after it's done.)

## Check yourself

Before moving on, can you answer these out loud?

1. What does `time.sleep(1)` actually do? Where is the program "doing work" during that second?
2. Walk through `format_mmss(95)` in your head. What does `95 // 60` give you? What does `95 % 60` give you? What does the final string look like?
3. What would happen if you removed `flush=True` from the countdown `print()`? (Try it!)

## Try these extensions

1. **Configurable durations.** Ask the user at the start for the work/break lengths, rather than using the constants. Let them press Enter to accept the defaults.
2. **More pomodoros.** The real technique is four work sessions (with short breaks) then a longer break. Add a loop that runs four rounds, and swap the final break for 15 minutes.
3. **Log every session.** When each countdown finishes, append a JSON line to `history.json` — `{"label": "Work", "started": "...", "finished": "...", "duration_seconds": 1500}`. (Uses everything you learned in Project 8, plus a new datetime method: `started.isoformat()`.)
4. **Play a real beep.** `print("\a")` triggers the terminal's alert bell on most systems. Ring it when work ends and when break ends.
5. **Prettier countdown.** Pad the line to a fixed width so the previous frame never "bleeds through" on the edges when text gets shorter. (Hint: format with a minimum width, or add extra spaces at the end.)
