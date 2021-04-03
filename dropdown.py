# -*- coding: utf-8 -*-
import sys
from pathlib import Path

from ranger.api.commands import Command

from . import util

SETTINGS = {
    "tmux_dropdown_percent": {"type": int, "default": 60},
    "tmux_dropdown_animate": {"type": bool, "default": True},
    "tmux_dropdown_duration": {"type": int, "default": 100},
}


class install_tmux_dropdown_shortcut(Command):
    def execute(self):

        self.fm.notify("Installing drop-down shortcut in tmux")

        tmux_user_config_path = Path.home() / ".tmux.conf"

        bind_key_cmd = [
            "bind-key",
            "Bspace",
            "run-shell",
            "-b",
            " ".join(
                [
                    sys.executable,
                    str(Path(__file__).parent / "drop_ranger.py"),
                ]
            ),
        ]
        config_lines = [
            "#-#-# start of ranger_tmux config #-#-#",
            "# These lines were automatically added by ranger_tmux",
            " ".join(bind_key_cmd),
            "#-#-# end of ranger_tmux config #-#-#",
        ]

        if tmux_user_config_path.exists():
            with open(tmux_user_config_path, "r") as f:
                lines = [x.strip() for x in f.readlines()]

            # Search for tmux_ranger config in tmux config
            start_line = -1
            end_line = -1
            for i, line in enumerate(lines):
                if line == config_lines[0]:
                    start_line = i
                if line == config_lines[-1]:
                    end_line = i
                    break
            if start_line > -1 and end_line > -1:
                # Existing config found, update ours
                lines = lines[:start_line] + config_lines + lines[end_line + 1 :]
            else:
                # No existing config found, append ours
                lines += [""] + config_lines + [""]
        else:
            # No config at all, just use ours
            lines = [""] + config_lines + [""]

        # Write the updated tmux configuration file
        with open(tmux_user_config_path, "w") as f:
            f.write("\n".join(lines))

        # Run in current session
        util.tmux(*bind_key_cmd)
        util.tmux("display", "Tmux shortcut for drop-down ranger installed")


def init(fm, *args):
    fm.execute_console(
        'map xh eval fm.execute_console("install_tmux_dropdown_shortcut")'
    )
