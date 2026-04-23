# 01 — configure DSPy with Ollama, run a one-line predictor.
#
# Before running:
#   ollama pull qwen2.5-coder:7b
#   pip install -r requirements.txt

import dspy

# Universal pattern: LM string + api_base. Switch providers by changing
# the string — the rest of the program stays the same.
lm = dspy.LM("ollama_chat/qwen2.5-coder:7b", api_base="http://localhost:11434")
dspy.configure(lm=lm)


def main():
    # The string "question -> answer" is a SIGNATURE — DSPy reads it as
    # "input field: question, output field: answer". Folder 02 explains.
    predict = dspy.Predict("question -> answer")

    result = predict(question="What is the capital of France?")
    print(f"Answer: {result.answer}")

    # `result` is a dspy.Prediction — a dict-like object with an attribute
    # per output field declared in the signature.
    print(f"\nFull prediction object: {result}")


if __name__ == "__main__":
    main()
