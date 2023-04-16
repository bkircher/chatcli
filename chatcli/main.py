import os
import errno
from pathlib import Path
from typing import Callable, Union

import openai
from appdirs import user_config_dir
from prompt_toolkit import PromptSession
from prompt_toolkit.output import ColorDepth

from .state import ChatState


def create_dir(directory: Union[str, Path]) -> None:
    """Create a directory if it doesn't exist."""

    try:
        os.makedirs(directory)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


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


def main() -> None:
    """Main entry point."""

    openai.api_key = os.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        raise RuntimeError("OPENAI_API_KEY env var is not set or empty")

    appname = "ChatCLI"
    configdir = user_config_dir(appname=appname)
    create_dir(configdir)

    with ChatState(filename=os.path.join(configdir, "chat.db")) as state:
        session = PromptSession(history=state.history)
        repl(session=session, evalfn=chat, context=state)


if __name__ == "__main__":
    main()
