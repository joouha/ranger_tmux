# -*- coding: utf-8 -*-
import atexit

from . import util

SETTINGS = {"tmux_set_title": {"key": "i", "type": bool, "default": True}}


def set_tmux_window_title(msg):
    """Set tmux's window format"""
    util.tmux("set-option", "-p", "automatic-rename-format", msg)


def tmux_set_title_init(fm, setting, *args):

    # Save tmux's original title format
    original_format = util.tmux("show-options", "-gv", "automatic-rename-format")

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

    setting = list(SETTINGS.keys())[0]
    fm.settings.signal_bind(f"setopt.{setting}", setting_signal_handler)

    if fm.settings.__getitem__(setting):
        enable()
