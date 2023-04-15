import os
from typing import Callable

import openai


def repl(evaluate: Callable[[str], str]) -> None:
    while True:
        try:
            text = input(">>> ")
        except (EOFError, KeyboardInterrupt):
            return
        if text:
            output = evaluate(text)
            print(output)
        else:
            # Wait for more input
            continue


def chat(text: str) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": text}],
    )
    return response.choices[0].message.content


def main() -> None:
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        raise RuntimeError("OPENAI_API_KEY env var is not set")

    repl(chat)


if __name__ == "__main__":
    main()
