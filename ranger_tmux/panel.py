# -*- coding: utf-8 -*-
import signal
import sys
import time

import psutil
import ranger
from ranger.container.settings import Settings
from ranger.core.fm import FM
from ranger.core.main import parse_arguments
from ranger.core.shared import FileManagerAware, SettingsAware

from ranger_tmux import util


def main():

    ranger_script_path = util.get_ranger_script()

    # Initiate ranger just enough to allow us to access the settings
    ranger.args = parse_arguments()
    fm = FM()
    SettingsAware.settings_set(Settings())
    FileManagerAware.fm_set(fm)
    ranger.core.main.load_settings(fm, clean=False)

    # Check we're actually in tmux
    if not util.check_tmux(fm):
        sys.exit()

    # Check if we need to animate the drop
    animate = fm.settings.get("tmux_animate")
    duration = fm.settings.get("tmux_animation_duration")

    pane_id, command, pid = util.tmux(
        "display", "-t", "{left}", "-p", "#{pane_id}|#{pane_start_command}|#{pane_pid}"
    ).split("|")

    # Ranger is open - we will close it
    if command.startswith(str(ranger_script_path)):
        # Animate close if wanted
        if animate:
            util.animated_resize(pane_id, 2, "width", duration)
        # Get a handel on ranger
        process = psutil.Process(int(pid))
        # Send interupt to ranger to cancel any unfinished command entry
        process.send_signal(signal.SIGINT)
        # Ask ranger to quit nicely
        util.tmux("send-keys", "-t", pane_id, "Q")
        # Give range half a second to quit before vicously killing it
        dead, alive = psutil.wait_procs([process], timeout=0.5)
        for p in alive:
            p.kill()

    # Ranger is not open - we will open it
    else:
        # Make initial size smaller if we're going to animate
        size = fm.settings.get("tmux_panel_size")
        initial_size = 2 if animate else size
        # Get other pane folder
        pane_dir = util.tmux(
            "display-message", "-p", "-t", pane_id, "#{pane_current_path}"
        )
        # Create a new ranger pane
        pane_id = util.tmux(
            "split-window",
            "-bfh",
            "-F",
            "#{pane_id}",
            "-c",
            pane_dir,
            "-t",
            "{top}",
            "-l",
            initial_size,
            f'{ranger_script_path} --cmd="set tmux_cwd_track True" --cmd="set viewmode multipane"',
        )
        # Animate open if wanted
        if animate:
            util.animated_resize(pane_id, size, "width", duration)


if __name__ == "__main__":
    main()
