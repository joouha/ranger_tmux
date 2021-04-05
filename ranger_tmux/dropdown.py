# -*- coding: utf-8 -*-
from ranger.api.commands import Command

from ranger_tmux.__main__ import tmux_keybindings

from . import util

SETTINGS = {
    "tmux_dropdown_percent": {"type": int, "default": 60},
    "tmux_dropdown_animate": {"type": bool, "default": True},
    "tmux_dropdown_duration": {"type": int, "default": 100},
}


class install_tmux_dropdown_shortcut(Command):
    def execute(self):
        def callback(answer):
            if answer == "y":
                tmux_cmds = tmux_keybindings(install=True)
                # Add shortcut to current session
                for cmd in tmux_cmds:
                    util.tmux(*cmd)
                util.tmux("display", "Tmux shortcut for drop-down ranger installed")

        self.fm.ui.console.ask(
            "Are you sure you want to install the drop-down ranger key-binding in"
            " ~/.tmux.conf? (y/n)",
            callback,
            "yn",
        )


def init(fm, *args):
    fm.execute_console(
        'map xh eval fm.execute_console("install_tmux_dropdown_shortcut")'
    )
