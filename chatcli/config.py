import os
import errno
from pathlib import Path
from typing import Union

import click
from appdirs import user_config_dir


def create_dir(directory: Union[str, Path]) -> None:
    """Create a directory if it doesn't exist."""

    try:
        os.makedirs(directory)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


class Config:
    """Configuration for the app."""

    def __init__(self) -> None:
        self.app_name = "ChatCLI"

        # Set command-line options as attributes to have them accessible
        # wherever we pass the Config object
        click_ctx = click.get_current_context()
        for key, value in click_ctx.params.items():
            setattr(self, key, value)

        app_dir = user_config_dir(appname=self.app_name)
        create_dir(app_dir)
        self.app_support_dir = app_dir

        database_file = os.path.join(app_dir, "chat.db")
        assert os.path.isabs(database_file)
        # See Engine Configuration in docs:
        # https://docs.sqlalchemy.org/en/20/core/engines.html#sqlite
        self.database_url = f"sqlite:///{database_file}"
