# -*- coding: utf-8 -*-
import atexit
import os
from subprocess import check_output

import ranger.api

from .util import tmux

SETTING = "tmux_set_title"
SHORTCUT_KEY = "i"


def set_tmux_window_title(msg):
    """Set tmux's window format"""
    tmux("set-option", "-p", "automatic-rename-format", msg)


def hook_init(fm, *args):

    # Save tmux's original title format
    original_format = check_output(
        ["tmux", "show-options", "-gv", "automatic-rename-format"]
    ).strip()

    def enable():
        # Set window name to "ranger" on this panel
        set_tmux_window_title("ranger")
        # Reset title at exit
        atexit.register(disable)

    def disable():
        set_tmux_window_title(original_format)
        atexit.unregister(disable)

    def setting_signal_handler(signal):
        if signal.value:
            enable()
        else:
            disable()

    fm.settings.signal_bind(f"setopt.{SETTING}", setting_signal_handler)

    if fm.settings.__getitem__(SETTING):
        enable()
