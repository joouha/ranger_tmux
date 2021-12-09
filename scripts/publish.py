# -*- coding: utf-8 -*-
"""Publishes a new releases of ranger-tmux."""
from pathlib import Path

from poetry_publish.publish import poetry_publish  # type: ignore

import ranger_tmux


def publish() -> "None":
    """Publishes a new releasse of euporie to pypi.org."""
    poetry_publish(
        package_root=Path(ranger_tmux.__file__).parent.parent,
        version=ranger_tmux.__version__,
    )


if __name__ == "__main__":
    publish()
