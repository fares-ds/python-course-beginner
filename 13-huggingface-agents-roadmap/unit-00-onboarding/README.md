# Unit 0 — Welcome and Onboarding

The 30-minute admin chapter. Get an HF account, get a token, optionally join the Discord, decide whether you're going for a certificate.

**Course link:** [Unit 0 on the HF docs](https://huggingface.co/learn/agents-course/unit0/introduction)

## What you'll learn

- Why this course exists, and how it's organized.
- How to choose between **audit mode** (no certificate, no deadlines) and the **certification path**.
- Where to ask questions (the Discord + the HF forums).
- How to set up your Hugging Face account so the rest of the course works.

## What's in this folder

- [`solution.py`](solution.py) — verifies your HF login and reports your username.
- [`requirements.txt`](requirements.txt) — `huggingface_hub`.

## Setup

```bash
pip install -r requirements.txt
```

Sign up at [hf.co/join](https://huggingface.co/join) (free), then:

```bash
huggingface-cli login    # paste a token from hf.co/settings/tokens (read scope is enough for now)
```

## Run it

```bash
python3 solution.py
```

Expected output: your HF username + a "ready for Unit 1" message. If it says "not logged in," go fix that before continuing.

## Key concepts

### Audit vs certification
- **Audit mode**: do as much (or as little) of the course as you want. No grading, no deadlines, no certificate. Good if you're just exploring.
- **Fundamentals certificate**: complete Unit 1 + its quiz. Free. Real credential.
- **Certificate of Excellence**: complete Unit 1 + a use-case assignment + the Unit 4 final challenge (GAIA). Also free.

There's no deadline for either certificate path.

### Why the HF account matters
The course's hands-on exercises live as Hugging Face Spaces. To run them yourself (rather than just read), to push your own agents, to submit to the Unit 4 leaderboard — you need an account. It's free; do it now and forget about it.

### Discord
Optional. Useful if you like learning in groups and want to find people working on the same units at the same time. The course's #agents-course-questions channel is responsive.

## Mini-tasks

1. Run `solution.py` — confirm it prints your username.
2. Visit your HF profile page (`huggingface.co/your-username`). It's empty for now; by the end of this course it will have several agents on it.
3. Decide: are you auditing, or going for a certificate? Write it down somewhere. (Most people who say "I'll decide later" never do, and don't certify.)

## Common pitfalls

- **Skipping the account step** — the course's later units assume you have one. You'll hit a wall.
- **Using a read-only token forever** — fine for now, but Units 1+ will want a write-scope token to push agents.

## Expected outcome

You're logged in to the Hub from your terminal. You know what you're aiming for (audit or cert). You're ready for Unit 1.

## Next

→ [Unit 1 — Introduction to Agents](../unit-01-introduction-to-agents/)
