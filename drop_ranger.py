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

# Initiate ranger just enough to allow us to access the settings
ranger.args = parse_arguments()
fm = FM()
SettingsAware.settings_set(Settings())
FileManagerAware.fm_set(fm)
ranger.core.main.load_settings(fm, clean=False)

# An added bonus is that plugins are loaded by the above
# This means we can import from this plugin
from plugins.ranger_tmux import util  # noqa E402


def animated_resize(pane_id, target_perc):
    """Animates the resizing a tmux pane."""
    # lines = fm.settings.get("tmux_dropdown_animate_lines")
    duration = fm.settings.get("tmux_dropdown_duration")
    pane_height = int(util.tmux("display", "-t", "{top}", "-p", "#{pane_height}"))
    window_height = int(util.tmux("display", "-p", "#{window_height}"))
    target_height = int(target_perc / 100 * window_height)
    direction = pane_height < target_height
    lines = int(duration < 500) + 1
    frames = max(1, abs(pane_height - target_height) // lines - 1)
    timeout = duration / 1000 / frames
    for i in range(frames):
        util.tmux("resize-pane", "-D" if direction else "-U", "-t", pane_id, lines)
        time.sleep(timeout)
    util.tmux("resize-pane", "-t", pane_id, "-y", f"{target_perc}%")


def main():

    # Check we're actually in tmux
    if not util.check_tmux(fm):
        sys.exit()

    # Check if we need to animate the drop
    animate = fm.settings.get("tmux_dropdown_animate")

    pane_id, command, pid = util.tmux(
        "display", "-t", "{top}", "-p", "#{pane_id}|#{pane_start_command}|#{pane_pid}"
    ).split("|")

    # Ranger is open - we will close it
    if command == "ranger":
        # Animate close if wanted
        if animate:
            animated_resize(pane_id, 0)
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
        # Load ranger pane height from ranger settings
        percent = fm.settings.get("tmux_dropdown_percent")
        # Make initial size smaller if we're going to animate
        initial_size = "1" if animate else f"{percent}%"
        # Get other pane folder
        pane_dir = util.tmux(
            "display-message", "-p", "-t", pane_id, "#{pane_current_path}"
        )
        # Create a new ranger pane
        pane_id = util.tmux(
            "split-window",
            "-bfv",
            "-F",
            "#{pane_id}",
            "-c",
            pane_dir,
            "-t",
            "{top}",
            "-l",
            initial_size,
            "ranger",
        )
        # Animate open if wanted
        if animate:
            animated_resize(pane_id, percent)


if __name__ == "__main__":
    main()
