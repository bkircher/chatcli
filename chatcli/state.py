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
                text(r"select value from history order by id desc")
            )
            yield from (row[0] for row in rows)

    def store_string(self, string: str) -> None:
        string = string.strip()
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


class Message:
    """A message in the chat session."""

    def __init__(self, role: str, content: str) -> None:
        self.role = role
        self.content = content

    def __repr__(self) -> str:
        return f"Message(role={self.role}, content={self.content})"

    def to_dict(self) -> dict:
        """Return a dict representation of the message."""

        return {
            "role": self.role,
            "content": self.content,
        }


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
        self._current_conversation_id = self._create_new_conversation()

    @property
    def current_conversation(self) -> int:
        """The current conversation ID."""

        return self._current_conversation_id

    @property
    def messages(self) -> Iterable[Message]:
        """The messages in the current conversation."""
        with self.db.connect() as conn:
            rows = conn.execute(
                text(
                    r"""select role, content from message
                    where conversation_id = :conversation_id
                    order by id asc"""
                )
                .bindparams(conversation_id=self.current_conversation)
                .columns(conversation_id=Integer)
            )
            yield from (Message(role=row[0], content=row[1]) for row in rows)

    def append_message(self, role: str, content: str) -> None:
        """Add a new message to the current conversation."""

        with self.db.connect() as conn:
            conn.execute(
                text(
                    r"""insert into message (role, content, conversation_id)
                    values (:role, :content, :conversation_id)"""
                )
                .bindparams(
                    role=role,
                    content=content,
                    conversation_id=self.current_conversation,
                )
                .columns(role=String, content=String, conversation_id=Integer)
            )
            conn.commit()

    def close(self) -> None:
        pass

    def __enter__(self) -> "ChatState":
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.close()

    def _create_new_conversation(self) -> int:
        """Create a new conversation and return its ID."""

        with self.db.connect() as conn:
            conn.execute(text(r"insert into conversation default values"))
            conversation_id = conn.execute(
                text(r"select last_insert_rowid()")
            ).scalar()
            # Add a default system message to the conversation
            conn.execute(
                text(
                    r"""insert into message (role, content, conversation_id)
                    values (:role, :content, :conversation_id)"""
                )
                .bindparams(
                    role="system",
                    content="You are a helpful assistant.",
                    conversation_id=conversation_id,
                )
                .columns(role=String, content=String, conversation_id=Integer)
            )
            conn.commit()
            return conversation_id
