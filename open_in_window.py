# -*- coding: utf-8 -*-
import ranger.api

HOOK_INIT_OLD = ranger.api.hook_init

SETTINGS = {"tmux_open_in_window": {"key": "w", "type": bool, "default": True}}


def tmux_open_in_window_init(fm, setting, *args):
    """Monkey-patch rifle's preprocessing function.

    This re-writes rifle commands, causing them to run in a new tmux window.

    """

    # Add shortcuts to open selected file in new window / pane
    fm.execute_console('map xo shell tmux new-window -a "rifle %f"')
    fm.execute_console('map xl shell tmux split-pane -h "rifle %f"')
    fm.execute_console('map xp shell tmux split-pane -v "rifle %f"')

    # Hook rifle's post-processing command
    old_postprocessing_command = fm.rifle.hook_command_postprocessing

    def new_postprocessing_command(command):
        if fm.settings.__getitem__(setting):
            command = command.replace('"', r"\"").replace("$", r"\$")
            command = 'tmux new-window -a "{}"'.format(command)
        return old_postprocessing_command(command)

    fm.rifle.hook_command_postprocessing = new_postprocessing_command
