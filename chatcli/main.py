import os
from typing import Callable, Optional

import click
from openai import OpenAI

from prompt_toolkit import PromptSession
from prompt_toolkit.output import ColorDepth

from .state import ChatState
from .config import Config


version = "0.2.0"


def repl(
    session: PromptSession,
    evalfn: Callable[[Optional[OpenAI], str, ChatState], str],
    context: ChatState,
) -> None:
    """The REPL loop loop loop."""

    client = None

    if not context.config.dry_run:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY env var is not set or empty")
        client = OpenAI(api_key=api_key)

    while True:
        try:
            text = session.prompt(
                message=context.message,
                style=context.style,
                color_depth=ColorDepth.TRUE_COLOR,
            )
            text = text.strip()
        except (EOFError, KeyboardInterrupt):
            return
        if text:
            # TODO: does text here need some sanitization, trimming maybe?
            output = evalfn(client, text, context)
            print(output)
        else:
            # Wait for more input
            continue


def chat(client: Optional[OpenAI], text: str, context: ChatState) -> str:
    """Send message to OpenAI API and return response."""

    context.append_message(role="user", content=text)
    if context.config.dry_run:
        content = (
            "I am running in dry-run mode, no messages sent to OpenAI API."
        )
    else:
        messages = [msg.to_dict() for msg in context.messages]
        response = client.chat.completions.create(
            model="gpt-4", messages=messages
        )
        content = response.choices[0].message.content
    context.append_message(role="assistant", content=content)
    return content


@click.command()
@click.option(
    "-p",
    "--prompt",
    default=None,
    help="A text-file which is set at the beginning of the conversation.",
)
@click.option(
    "--dry-run", is_flag=True, help="Don't send messages to OpenAI API."
)
@click.version_option(
    version=version, package_name="chatcli", prog_name="ChatCLI"
)
def main(prompt: os.PathLike, dry_run: bool) -> None:
    """Quick and dirty OpenAI chat interface for the CLI."""

    config = Config(dry_run=dry_run)
    with ChatState(config=config, prompt_filename=prompt) as state:
        session = PromptSession(history=state.history)
        repl(session=session, evalfn=chat, context=state)


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    main()
