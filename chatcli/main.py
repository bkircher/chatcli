import os
from typing import Callable

import openai
from prompt_toolkit import PromptSession
from prompt_toolkit.output import ColorDepth

from .state import ChatState
from .config import Config


def repl(
    session: PromptSession, evalfn: Callable[[str], str], context: ChatState
) -> None:
    """The REPL loop."""

    while True:
        try:
            text = session.prompt(
                message=context.message,
                style=context.style,
                color_depth=ColorDepth.TRUE_COLOR,
            )
        except (EOFError, KeyboardInterrupt):
            return
        if text:
            # TODO: does text here need some sanitization, trimming maybe?
            output = evalfn(text)
            print(output)
        else:
            # Wait for more input
            continue


def chat(text: str) -> str:
    """Send message to OpenAI API and return response."""

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": text}],
    )
    return response.choices[0].message.content

    # TODO: add a dry run mode, like: return "I am so clever, yada yada"


def main() -> None:
    """Main entry point."""

    openai.api_key = os.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        raise RuntimeError("OPENAI_API_KEY env var is not set or empty")

    config = Config()
    with ChatState(config=config) as state:
        session = PromptSession(history=state.history)
        repl(session=session, evalfn=chat, context=state)


if __name__ == "__main__":
    main()
