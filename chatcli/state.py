from typing import Iterable

from sqlalchemy import Engine, text, Integer, String
from prompt_toolkit.styles import Style
from prompt_toolkit.history import History

from .config import Config
from .db import init


class ChatHistory(History):
    """A history that loads and stores messages from and to a SQLite DB."""

    def __init__(self, db: Engine, state: "ChatState") -> None:
        super().__init__()
        self.state = state
        self.db = db

    def load_history_strings(self) -> Iterable[str]:
        with self.db.connect() as conn:
            rows = conn.execute(
                text(r"select value from history order by id asc")
            )
            yield from (row[0] for row in rows)

    def store_string(self, string: str) -> None:
        with self.db.connect() as conn:
            conn.execute(
                text(
                    r"""insert into history (value, conversation_id)
                    values (:value, :conversation_id)"""
                )
                .bindparams(
                    value=string,
                    conversation_id=self.state.current_conversation,
                )
                .columns(value=String, conversation_id=Integer)
            )
            conn.commit()


class ChatState:
    """The state of the chat session."""

    def __init__(self, config: Config) -> None:
        self.style = Style.from_dict(
            {
                "": "#ffffff",
                "pound": "#884444",
            }
        )
        self.message = [
            ("class:pound", ">>> "),
        ]
        self.db = init(config)
        self.history = ChatHistory(db=self.db, state=self)
        self._current_conversation_id = _create_new_conversation(self.db)

    @property
    def current_conversation(self) -> int:
        """The current conversation ID."""
        return self._current_conversation_id

    def close(self) -> None:
        pass

    def __enter__(self) -> "ChatState":
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.close()


def _create_new_conversation(db: Engine) -> int:
    """Create a new conversation and return its ID."""

    with db.connect() as conn:
        conn.execute(text(r"insert into conversation default values"))
        rowid = conn.execute(text(r"select last_insert_rowid()")).scalar()
        conn.commit()
        return rowid
