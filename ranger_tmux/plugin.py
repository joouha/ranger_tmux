# -*- coding: utf-8 -*-
import ranger.api
from ranger.container.settings import (
    ALLOWED_SETTINGS,
    SIGNAL_PRIORITY_SANITIZE,
    SIGNAL_PRIORITY_SYNC,
)

from ranger_tmux import (
    cwd_sync,
    cwd_track,
    dropdown,
    open_in_window,
    set_window_name,
    splits,
    util,
)
from ranger_tmux.cwd_sync import tmux_cwd_sync_now  # noqa F401
from ranger_tmux.cwd_track import tmux_cwd_track_now  # noqa F401
from ranger_tmux.dropdown import install_tmux_dropdown_shortcut  # noqa F401

MODULES = [open_in_window, set_window_name, cwd_sync, cwd_track, dropdown, splits]

HOOK_INIT_OLD = ranger.api.hook_init


# Add settings to ranger when plugin is loaded
# Adding these at import means the plugin's settings are available to ranger
for mod in MODULES:
    if hasattr(mod, "SETTINGS"):
        for setting, info in mod.SETTINGS.items():
            ALLOWED_SETTINGS[setting] = info.get("type", bool)
            value = info.get("default")
            if value:
                ranger.fm.settings._raw_set(setting, value)
            ranger.fm.settings.signal_bind(
                "setopt.{}".format(setting),
                ranger.fm.settings._sanitize,
                priority=SIGNAL_PRIORITY_SANITIZE,
            )
            ranger.fm.settings.signal_bind(
                "setopt.{}".format(setting),
                ranger.fm.settings._raw_set_with_signal,
                priority=SIGNAL_PRIORITY_SYNC,
            )


def hook_init(fm):

    # Add ranger_tmux hooks if we are in a tmux session
    if util.check_tmux(fm):

        # Load all modules
        for mod in MODULES:
            # Add key-bindings for module
            if hasattr(mod, "SETTINGS"):
                for setting, info in mod.SETTINGS.items():
                    if hasattr(mod, "{}_init".format(setting)):
                        getattr(mod, "{}_init".format(setting))(fm, setting, MODULES)
                    key = info.get("key")
                    if key:
                        fm.execute_console("map x{} set {}!".format(key, setting))
            if hasattr(mod, "init"):
                mod.init(fm, MODULES)

    return HOOK_INIT_OLD(fm)


ranger.api.hook_init = hook_init
