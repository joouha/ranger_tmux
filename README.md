# ranger-tmux

Tmux integration for ranger

## Install

To install this plugin, clone the respository into ranger's plugins folder, or install it with pip:

```
pip install ranger-tmux
# Then run this to install the package as a ranger plugin:
python -m ranger_tmux install
```

## Features

<img src="https://i.postimg.cc/SRz46CNH/output.gif" align="right" width=300>

- Open files from ranger in a new tmux window or pane
- Make your terminal track ranger's directory
- Make ranger track your terminal's directory
- Set tmux window title to show ranger is running
- Drop down file-manager in your tmux session
- Easily split a ranger pane to launch a shell in the current folder

### Other pane tracking & syncing

This plugin enables syncing of the current working directory between ranger and other tmux panes in the same window.

The pane to be used for syncing or tracking is determined in the following order:

1. A marked pane;
2. The currently selected pane;
3. The last selected pane;
4. The next pane.

Ranger will only sync its working directory to another pane if the process running in another pane does not have any child processes. This prevents ranger typing `cd` commands if you have launched a text editor from the shell in the other pane.

### Drop-down ranger

When installing the plugin, you will be asked if you want to install a key-binding in `~/.tmux.conf` for drop-down ranger. This allows you to toggle ranger in a drop-down tmux pane in the current window. This can be run manually by running `python -m ranger_tmux.drop` in a tmux session.

The key binding can be installed by running `python -m ranger_tmux --tmux install`, or by running the `:install_tmux_dropdown_shortcut` command in ranger (or typing the `xh` shortcut). The default key-binding installed is `prefix, backspace`, but this can be changed by editing the lines added to `~/.tmux.conf`.

## Shortcut keys

| Key Sequence | Command                                                                           |
| ------------ | --------------------------------------------------------------------------------- |
| `xc`         | Change the current working directory in the other pane to the directory in ranger |
| `xd`         | Change ranger's current directory to the directory of the other pane              |
| `xs`         | Toggle syncing of ranger's current directory to the other pane                    |
| `xt`         | Toggle tracking of the other pane's working directory to tmux                     |
| `xw`         | Toggle opening files in a new tmux window                                         |
| `xi`         | Toggle setting the tmux window's title to "ranger" when ranger is running         |
| `xe`         | Open the selected file with rifle in a new tmux window                            |
| `x\|`        | Split ranger's current tmux pane vertially                                        |
| `x-`         | Split ranger's current tmux pane horizontally                                     |
| `xh`         | Adds the dropdown shortcut to `~/.tmux.conf`                                      |

## Settings

This plugin adds several settings to ranger:

| Setting                   | Type  | Default | Meaning                                                                                  |
| ------------------------- | ----- | ------- | ---------------------------------------------------------------------------------------- |
| `tmux_cwd_sync`           | bool  | False   | When True, ranger's current directory is synced to the other pane                        |
| `tmux_cwd_sync_now_focus` | bool  | False   | When True, the other pane will be focused after manually syncing it with ranger          |
| `tmux_cwd_track`          | bool  | False   | When True, ranger's current directory tracks the other pane                              |
| `tmux_cwd_track_interval` | float | 0.5     | Time between checks of the directory of the other pane when tracking                     |
| `tmux_open_in_window`     | bool  | True    | When True, files opened with ranger will open in a new tmux window                       |
| `tmux_set_title`          | bool  | True    | When True, the tumx window will be renamed to "ranger" when ranger is running            |
| `tmux_dropdown_percent`   | int   | 60      | The height of the pane created when the drop-down tmux key-binding is installed and used |
| `tmux_dropdown_animate`   | bool  | True    | When True, dropped-down ranger will grow / shrink when summoned                          |
| `tmux_dropdown_duration`  | float | 100     | Drop-down animation time in miliseconds                                                  |

The default values can be modified by setting them in `~/.config/ranger/rc.conf`, e.g.:

```
set tmux_cwd_sync true
set tmux_cwd_track true
set tmux_set_title true
set tmux_open_in_window true
set tmux_dropdown_percent 60
```
