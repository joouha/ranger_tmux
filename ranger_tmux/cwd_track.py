# -*- coding: utf-8 -*-
import time
from threading import Thread

from ranger.api.commands import Command

from . import util

SETTINGS = {
    "tmux_cwd_track": {"key": "t", "type": bool},
    "tmux_cwd_track_interval": {"type": float, "default": 0.5},
}


class tmux_cwd_track_now(Command):
    ranger_pane = None

    def execute(self):
        if self.ranger_pane:
            pane_id = util.select_shell_pane(self.ranger_pane)
            if pane_id:
                new_path = util.tmux(
                    "display", "-p", "-t", pane_id, "-F", "#{pane_current_path}"
                )
                if new_path != self.fm.thisdir.path:
                    self.fm.cd(new_path)


class MonitorPane(Thread):
    def __init__(self, fm, ranger_pane):
        Thread.__init__(self)
        self.daemon = True
        self.stopped = False
        self.fm = fm
        self.last_path = None
        self.ranger_pane = ranger_pane
        self.start()

    def run(self):
        while not self.stopped:
            pane_id = util.select_shell_pane(self.ranger_pane)
            if pane_id:
                new_path = util.tmux(
                    "display", "-p", "-t", pane_id, "-F", "#{pane_current_path}"
                )
                if self.last_path != new_path and new_path != self.fm.thisdir.path:
                    self.fm.cd(new_path)
                    self.last_path = new_path
            time.sleep(self.fm.settings.get("tmux_cwd_track_interval", 1))


def tmux_cwd_track_init(fm, setting, *args):
    """"""

    fm.execute_console('map xd eval fm.execute_console("tmux_cwd_track_now")')

    # Find pane with current instance of ranger in it
    ranger_pane = util.get_ranger_pane()
    tmux_cwd_track_now.ranger_pane = ranger_pane

    non_local = {"pane_monitor_thread": None}

    def enable():
        non_local["pane_monitor_thread"] = MonitorPane(fm, ranger_pane)

    def disable():
        if non_local["pane_monitor_thread"]:
            non_local["pane_monitor_thread"].stopped = True

    def setting_signal_handler(signal):
        if signal.value:
            enable()
        else:
            disable()

    fm.settings.signal_bind("setopt.{}".format(setting), setting_signal_handler)

    if fm.settings.__getitem__(setting):
        enable()
