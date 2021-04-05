# -*- coding: utf-8 -*-
from ranger.api.commands import Command

from . import util

SETTINGS = {
    "tmux_cwd_sync": {"key": "s", "type": bool},
}


class tmux_cwd_sync_now(Command):
    ranger_pane = None

    def execute(self):
        if self.ranger_pane:
            pane_id = util.select_shell_pane(self.ranger_pane)
            if pane_id:
                util.cd_pane(self.fm.thisdir.path, pane_id)


def tmux_cwd_sync_init(fm, setting, *args):
    """"""

    fm.execute_console('map xc eval fm.execute_console("tmux_cwd_sync_now")')

    # Find pane with current instance of ranger in it
    ranger_pane = util.get_ranger_pane()
    tmux_cwd_sync_now.ranger_pane = ranger_pane

    cd_signal_handler = None

    def cd_hook(signal):
        if "new" in signal:
            pane_id = util.select_shell_pane(ranger_pane)
            if pane_id:
                util.cd_pane(signal.new, pane_id)

    def setting_signal_handler(signal):
        nonlocal cd_signal_handler
        if signal.value:
            cd_signal_handler = fm.signal_bind("cd", cd_hook)
        else:
            if cd_signal_handler:
                fm.signal_unbind(cd_signal_handler)

    fm.settings.signal_bind(f"setopt.{setting}", setting_signal_handler)

    if fm.settings.__getitem__(setting):
        cd_signal_handler = fm.signal_bind("cd", cd_hook)
