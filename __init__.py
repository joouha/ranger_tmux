# -*- coding: utf-8 -*-
import ranger.api
from ranger.container.settings import (
    ALLOWED_SETTINGS,
    SIGNAL_PRIORITY_SANITIZE,
    SIGNAL_PRIORITY_SYNC,
)

from . import cwd_sync, cwd_track, open_in_window, set_window_name, util
from .cwd_sync import tmux_cwd_sync_now
from .cwd_track import tmux_cwd_track_now

MODULES = [open_in_window, set_window_name, cwd_sync, cwd_track]

HOOK_INIT_OLD = ranger.api.hook_init


# Add settings to ranger when plugin is loaded
# These are added in the plugin's root scope so they are available to ranger
for mod in MODULES:
    if hasattr(mod, "SETTING"):
        setting = mod.SETTING
        ALLOWED_SETTINGS[setting] = bool
        ranger.fm.settings.signal_bind(
            f"setopt.{setting}",
            ranger.fm.settings._sanitize,
            priority=SIGNAL_PRIORITY_SANITIZE,
        )
        ranger.fm.settings.signal_bind(
            f"setopt.{setting}",
            ranger.fm.settings._raw_set_with_signal,
            priority=SIGNAL_PRIORITY_SYNC,
        )


def hook_init(fm):

    # Add ranger_tmux hooks if we are in a tmux session
    if util.check_tmux(fm):

        # Extra tmux key-bindings
        fm.execute_console("map x- shell tmux split-window -v -c %d")
        fm.execute_console("map x| shell tmux split-window -h -c %d")

        # Load all modules
        for mod in MODULES:
            mod.hook_init(fm, MODULES)
            # Add key-bindings for module
            if hasattr(mod, "SHORTCUT_KEY"):
                fm.execute_console(f"map x{mod.SHORTCUT_KEY} set {mod.SETTING}!")

    return HOOK_INIT_OLD(fm)


ranger.api.hook_init = hook_init
