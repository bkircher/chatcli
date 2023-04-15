import os
from typing import Callable

import openai
from prompt_toolkit import PromptSession
from prompt_toolkit.output import ColorDepth
from prompt_toolkit.styles import Style


def repl(session: PromptSession, eval_fn: Callable[[str], str]) -> None:
    style = Style.from_dict(
        {
            "": "#ffffff",
            "pound": "#884444",
        }
    )
    message = [
        ("class:pound", ">>> "),
    ]
    while True:
        try:
            text = session.prompt(
                message=message,
                style=style,
                color_depth=ColorDepth.TRUE_COLOR,
            )
        except (EOFError, KeyboardInterrupt):
            return
        if text:
            output = eval_fn(text)
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
        raise RuntimeError("OPENAI_API_KEY env var is not set or empty")

    session = PromptSession()
    repl(session=session, eval_fn=chat)


if __name__ == "__main__":
    main()
