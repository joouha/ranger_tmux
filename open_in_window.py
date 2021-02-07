# -*- coding: utf-8 -*-
import os

import ranger.api

HOOK_INIT_OLD = ranger.api.hook_init

SETTING = "tmux_open_in_window"
SHORTCUT_KEY = "w"


def hook_init(fm, *args):
    """Monkey-patch rifle's preprocessing function.

    This re-writes rifle commands, causing them to run in a new tmux window.

    """

    # Add shortcut to open selected file now
    fm.execute_console('map xe shell tmux new-window -a "rifle %f"')

    # Hook rifle's preprocessing command
    old_preprocessing_command = fm.rifle.hook_command_preprocessing

    def new_preprocessing_command(command):
        if fm.settings.__getitem__(SETTING):
            command = "tmux new-window -a {}".format(command)
        return old_preprocessing_command(command)

    fm.rifle.hook_command_preprocessing = new_preprocessing_command
