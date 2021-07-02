# -*- coding: utf-8 -*-
import os
import shutil
import signal
import time
from subprocess import CalledProcessError, check_output

try:
    import importlib_metadata
except ImportError:
    import importlib.metadata as importlib_metadata

TMUX_PANE_TARGETS = {"height": "{top}", "width": "{left}"}
TMUX_DIRECTION_FLAGS = {
    "height": {1: "-D", -1: "-U"},
    "width": {1: "-R", -1: "-L"},
}
TMUX_DIMENSION_FLAGS = {"width": "-x", "height": "-y"}


def animated_resize(pane_id, target_size, dim="height", duration=500, lines=2):
    """Animates the resizing of a tmux pane."""
    pane_size = int(
        tmux("display", "-t", TMUX_PANE_TARGETS[dim], "-p", f"#{{pane_{dim}}}")
    )
    window_size = int(tmux("display", "-p", f"#{{window_{dim}}}"))

    size = int("".join([x for x in str(target_size) if x.isdigit()]))
    if str(target_size).endswith("%"):
        size = int(size / 100 * window_size)
    size = max(size, 2)

    direction = (pane_size < size) * 2 - 1
    frames = max(1, abs(pane_size - size) // lines - 1)
    timeout = duration / 1000 / frames

    while abs(size - pane_size) > 0:
        change = min(lines, abs(size - pane_size))
        tmux(
            "resize-pane",
            TMUX_DIRECTION_FLAGS[dim][direction],
            "-t",
            pane_id,
            abs(change),
        )
        pane_size += change * direction
        time.sleep(timeout)
    tmux("resize-pane", "-t", pane_id, TMUX_DIMENSION_FLAGS[dim], target_size)


def get_ranger_script():
    scripts = importlib_metadata.files("ranger-fm")
    if scripts is not None:
        ranger_script_paths = [path for path in scripts if path.name == "ranger"]
        if ranger_script_paths:
            return ranger_script_paths[0].locate().resolve()
    return shutil.which("ranger")


def check_tmux(fm):
    # TODO chcek tmux is in path too
    tmuxed = os.environ.get("TMUX")
    if not tmuxed:
        fm.notify("Not running in tmux session, ranger_tmux is disabled")
    return tmuxed


def tmux(*args):
    try:
        return check_output(["tmux"] + list(map(str, args))).decode("utf8").strip()
    except CalledProcessError:
        return


def get_ranger_pane():
    import psutil

    # Find pane with current instance of ranger in
    ranger_pid = os.getpid()
    panes = tmux("list-panes", "-aF", "#{pane_pid},#{pane_id}")
    if panes:
        panes = {
            int(pid): pane_id.strip()
            for pid, pane_id in [info.split(",") for info in panes.split("\n")]
        }
        for pid, pane_id in panes.items():
            if ranger_pid == pid or ranger_pid in [
                x.pid for x in psutil.Process(pid).children(recursive=True)
            ]:
                return pane_id


def select_shell_pane(ranger_pane):

    # Panes can move windows, so check this every time
    ranger_window = tmux("display", "-t", ranger_pane, "-p", "#{window_id}")

    # Get all panes in this window
    window_panes = tmux("list-panes", "-F", "#{pane_id}", "-t", ranger_window).split(
        "\n"
    )
    other_panes = set(window_panes) - set(ranger_pane)

    if not other_panes:
        return

    # Check for a marked pane in this window
    marks = tmux("display", "-p", "-F", "#{window_flags}", "-t", ranger_pane)
    has_marked_pane = "M" in marks  # marks' values can be `#!~*-MZ`
    if has_marked_pane:
        pane = tmux("display", "-p", "-t", "{marked}", "#{pane_id}")
        if pane in other_panes and pane != ranger_pane:
            return pane

    pane = tmux("display", "-p", "#{pane_id}")
    if pane in other_panes and pane != ranger_pane:
        return pane

    pane = tmux("display", "-p", "-t", "{last}", "#{pane_id}")
    if pane in other_panes and pane != ranger_pane:
        return pane

    pane = tmux("display", "-p", "-t", "{next}", "#{pane_id}")
    if pane in other_panes and pane != ranger_pane:
        return pane

    if other_panes:
        return list(sorted(other_panes))[0]


def cd_pane(path, pane_id):
    import psutil

    pane_process = psutil.Process(
        int(tmux("display", "-p", "-t", pane_id, "-F", "#{pane_pid}"))
    )
    with pane_process.oneshot():
        if not pane_process.children():
            if pane_process.cwd() != str(path):
                pane_process.send_signal(signal.SIGINT)
                tmux("send-keys", "-t", pane_id, ' cd "{}"'.format(path), "Enter")
