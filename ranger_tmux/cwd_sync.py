# -*- coding: utf-8 -*-
"""Add options and commands for syncing panes to ranger's current working directory."""

from ranger.api.commands import Command

from . import util

SETTINGS = {
    "tmux_cwd_sync": {"key": "s", "type": bool},
    "tmux_cwd_sync_now_focus": {"type": bool},
}


class tmux_cwd_sync_now(Command):
    """Sync working directory of the "other" pane to match ranger's."""

    ranger_pane = None

    def execute(self):
        """Executes the command."""
        if self.ranger_pane:
            pane_id = util.select_shell_pane(self.ranger_pane)
            if pane_id:
                util.cd_pane(self.fm.thisdir.path, pane_id)
                if self.fm.settings.get("tmux_cwd_sync_now_focus", False):
                    util.tmux("select-pane", "-t", pane_id)


def tmux_cwd_sync_init(fm, setting, *args):
    """Allows ranger to sync it's cwd to the other tmux pane."""
    fm.execute_console('map xc eval fm.execute_console("tmux_cwd_sync_now")')

    # Find pane with current instance of ranger in it
    ranger_pane = util.get_ranger_pane()
    tmux_cwd_sync_now.ranger_pane = ranger_pane

    non_local = {"cd_signal_handler": None}

    def cd_hook(signal):
        if "new" in signal:
            pane_id = util.select_shell_pane(ranger_pane)
            if pane_id:
                util.cd_pane(signal.new, pane_id)

    def setting_signal_handler(signal):
        if signal.value:
            non_local["cd_signal_handler"] = fm.signal_bind("cd", cd_hook)
        else:
            if non_local["cd_signal_handler"]:
                fm.signal_unbind(non_local["cd_signal_handler"])

    fm.settings.signal_bind("setopt.{}".format(setting), setting_signal_handler)

    if fm.settings.__getitem__(setting):
        non_local["cd_signal_handler"] = fm.signal_bind("cd", cd_hook)
