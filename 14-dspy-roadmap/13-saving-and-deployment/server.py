# 13 — serve the saved DSPy program behind a FastAPI endpoint.
#
# Run:
#   python3 solution.py            # first, to create program.json
#   uvicorn server:app --reload    # then, to start the server
#
# Then in another terminal:
#   curl -X POST http://127.0.0.1:8000/ask \
#     -H 'Content-Type: application/json' \
#     -d '{"question": "Who wrote Hamlet?"}'

from pathlib import Path

import dspy
from fastapi import FastAPI
from pydantic import BaseModel

SAVE_PATH = Path(__file__).parent / "program.json"

# Configure once at startup.
lm = dspy.LM("ollama_chat/qwen2.5-coder:7b", api_base="http://localhost:11434")
dspy.configure(lm=lm)

# Re-instantiate the Module, then load the compiled state into it.
program = dspy.ChainOfThought("question -> answer")
if SAVE_PATH.exists():
    program.load(str(SAVE_PATH))
    print(f"Loaded compiled program from {SAVE_PATH}")
else:
    print(f"WARNING: {SAVE_PATH} not found. Run solution.py first to compile + save.")
    print("Serving the un-compiled program for now.")

app = FastAPI(title="DSPy Q&A server")


class AskRequest(BaseModel):
    question: str


class AskResponse(BaseModel):
    answer: str


@app.post("/ask", response_model=AskResponse)
def ask(req: AskRequest):
    result = program(question=req.question)
    return AskResponse(answer=str(result.answer))


@app.get("/")
def root():
    return {"status": "ok", "endpoint": "POST /ask {question: str}"}
