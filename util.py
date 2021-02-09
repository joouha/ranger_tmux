# -*- coding: utf-8 -*-
import os
from subprocess import CalledProcessError, check_output

import psutil


def check_tmux(fm):
    # TODO chcek tmux is in path too
    tmuxed = os.environ.get("TMUX")
    if not tmuxed:
        fm.notify("Not running in tmux session, ranger_tmux is disabled")
    return tmuxed


def tmux(*args):
    return check_output(["tmux", *args]).decode("utf8").strip()


def get_ranger_pane():
    # Find window with current instance of ranger in
    ranger_pid = os.getpid()
    panes = {
        int(pid): pane_id
        for pid, pane_id in [
            info.split(",")
            for info in tmux("list-panes", "-aF", "#{pane_pid},#{pane_id}").split("\n")
        ]
    }
    for pid, pane_id in panes.items():
        process = psutil.Process(pid)
        if find_process(process, ranger_pid):
            return pane_id


def find_process(process, pid):
    if process.pid == pid:
        return True
    else:
        for child in process.children():
            is_child = find_process(child, pid)
            if is_child:
                return is_child
    return False


def select_shell_pane(ranger_pane):

    # Panes can move windows, so check this every time
    ranger_window = tmux("display", "-t", ranger_pane, "-p", "#{window_id}")

    # Get all panes in this window
    window_panes = tmux("list-panes", "-F", "#{pane_id}", "-t", ranger_window).split(
        "\n"
    )
    other_panes = {*window_panes} - {ranger_pane}
    n_other_panes = len(other_panes)

    # Check for a marked pane in this window
    has_marked_pane = int(
        tmux("display", "-p", "-F", "#{window_marked_flag}", "-t", ranger_pane)
    )

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
    if tmux("display", "-p", "-t", pane_id, "-F", "#{pane_current_path}") != path:
        tmux("send-keys", "-t", pane_id, "C-c")
        tmux("send-keys", "-t", pane_id, f' cd "{path}"', "Enter")
