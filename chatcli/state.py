import os
import sqlite3
from typing import Iterable

from prompt_toolkit.styles import Style
from prompt_toolkit.history import History


class ChatHistory(History):
    """A history that loads and stores messages from and to a SQLite DB."""

    def __init__(self, db: sqlite3.Connection) -> None:
        super().__init__()
        self.db = db
        self.messages = []

    def load_history_strings(self) -> Iterable[str]:
        for message in self.messages:
            yield message

    def store_string(self, string: str) -> None:
        self.messages.append(string)


class ChatState:
    """The state of the chat session."""

    def __init__(self, filename: str) -> None:
        assert filename

        self.filename = os.path.expanduser(os.path.expandvars(filename))
        self.style = Style.from_dict(
            {
                "": "#ffffff",
                "pound": "#884444",
            }
        )
        self.message = [
            ("class:pound", ">>> "),
        ]
        self.db = sqlite3.connect(self.filename)
        self.history = ChatHistory(db=self.db)

    def close(self) -> None:
        self.db.close()

    def __enter__(self) -> "ChatState":
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.close()
