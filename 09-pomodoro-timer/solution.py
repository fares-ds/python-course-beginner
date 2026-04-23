# Pomodoro Timer — a simple focus timer.
#
# 25 minutes of WORK, then a 5-minute BREAK. The program prints the remaining
# time each second. When the time is up, it says so and moves on.
#
# This project introduces two ways your code can interact with TIME:
#   - time.sleep(1)    — pause the program for one second
#   - datetime.now()   — ask the computer "what time is it right now?"

import time
from datetime import datetime

WORK_MINUTES = 25
BREAK_MINUTES = 5


def format_mmss(total_seconds):
    # Turn 90 seconds into "01:30".
    #   //  is whole-number division:  95 // 60 == 1
    #   %   gives the remainder:       95 %  60 == 35
    # The "02d" format means "integer, pad with zeros to 2 digits".
    # So 5 becomes "05", 12 stays "12".
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    return f"{minutes:02d}:{seconds:02d}"


def countdown(label, minutes):
    started = datetime.now()
    print(f"{label}: {minutes} minutes. Started at {started.strftime('%H:%M:%S')}.")

    seconds_left = minutes * 60
    while seconds_left > 0:
        # end="\r" moves the cursor back to the start of the line (no newline),
        # so each tick overwrites the previous one — a live countdown.
        # flush=True tells Python to actually SHOW the line right now instead
        # of waiting for a newline to come along.
        print(f"  {format_mmss(seconds_left)} remaining   ", end="\r", flush=True)
        time.sleep(1)             # pause for a real wall-clock second
        seconds_left = seconds_left - 1

    # Once the countdown is done, print a fresh line so the next message
    # doesn't land on top of our last tick.
    print(f"  {format_mmss(0)} remaining   ")

    finished = datetime.now()
    elapsed = finished - started   # subtracting two datetimes gives a timedelta
    print(f"Time! {label} finished at {finished.strftime('%H:%M:%S')}.")
    print(f"That took {elapsed}.")


# ---------- main ----------

print("Pomodoro Timer")
print("==============")
print(f"One work session of {WORK_MINUTES} minutes, then a {BREAK_MINUTES}-minute break.")
print()

countdown("Work", WORK_MINUTES)
print()
countdown("Break", BREAK_MINUTES)
print()
print("Session complete. Good job.")
