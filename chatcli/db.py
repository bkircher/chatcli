import logging
from typing import Any

from sqlalchemy import event, create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.engine import Engine

from alembic.config import Config as AlembicConfig
from alembic import command

from .config import Config


def _run_migration(database_url: str) -> None:
    """Run database migrations."""

    assert database_url

    # Set the SQLAlchemy URL dynamically; ini-file only points to an in-memory
    # engine
    alembic_cfg = AlembicConfig("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", database_url)

    command.upgrade(alembic_cfg, "head")


def init(config: Config) -> Engine:
    """Run migrations and initialize the database engine."""

    # TODO: maybe it's not so good to run migrations on every startup; slooow…
    try:
        _run_migration(config.database_url)
    except OperationalError as exc:
        logging.error(
            "Migrating '%s' failed",
            config.database_url,
            exc_info=True,
        )
        raise RuntimeError("Migration failed") from exc
    return create_engine(config.database_url, echo=False)


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection: Any, _connection_record: Any) -> None:
    """Ensure foreign key constraints are enforced with SQLite."""

    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
