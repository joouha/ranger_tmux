# ranger_tmux

Tmux integration for ranger-fm.

<img>

## Install

To install this plugin, clone the respository into ranger's pligins folder:

```
git clone https://github.com/joouha/ranger_tmux ~/.config/ranger/plugins/ranger_tmux
```

To install the [drop-down ranger](#drop-down-file-manager) tmux keybinding, run ranger in a tmux session and type `xh`.

## Features

- Open files from ranger in a new tmux window
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

### Drop-down ranger

Running the `:install_tmux_dropdown_shortcut` command in ranger (or typing the `xh` shortcut) will install add a keybinding to your tmux configuration in `~/.tmux.conf`, which enables ranger to act as a drop-down filemanager in tmux. A drop-down ranger pane can be summoned by pressing `prefix` (`Ctrl+b`) followed by `backspace`. When drop-down ranger is summoned, the current tmux window is split and a new pane running ranger is created at the top of the window.

The default key-binding installed is `prefix` `backspace`, but this can be changed by editing the lines added to `~/.tmux.conf`.

## Shortcut keys

| Key Sequence | Command                                                                           |
| ------------ | --------------------------------------------------------------------------------- |
| `xh`         | Adds the dropdown shortcut in `~/.tmux.conf`                                      |
| `xc`         | Change the current working directory in the other pane to the directory in ranger |
| `xd`         | Change ranger's current directory to the directory of the other pane              |
| `xs`         | Toggle syncing of ranger's current directory to the other pane                    |
| `xt`         | Toggle tracking of the other pane's working directory to tmux                     |
| `xw`         | Toggle opening files in a new tmux window                                         |
| `xi`         | Toggle setting the tmux window's title to "ranger" when ranger is running         |
| `xe`         | Open the selected file with rifle in a new tmux window                            |
| `x\|`        | Split ranger's current tmux pane vertially                                        |
| `x-`         | Split ranger's current tmux pane horizontally                                     |

## Settings

This plugin adds several settings to ranger:

| Setting                  | Type  | Default | Meaning                                                                                  |
| ------------------------ | ----- | ------- | ---------------------------------------------------------------------------------------- |
| `tmux_cwd_sync`          | bool  | False   | When True, ranger's current directory is synced to the other pane                        |
| `tmux_cwd_track`         | bool  | False   | When True, ranger's current directory tracks the other pane                              |
| `tmux_open_in_window`    | bool  | True    | When True, files opened with ranger will open in a new tmux window                       |
| `tmux_set_title`         | bool  | True    | When True, the tumx window will be renamed to "ranger" when ranger is running            |
| `tmux_dropdown_percent`  | int   | 60      | The height of the pane created when the drop-down tmux key-binding is installed and used |
| `tmux_dropdown_animate`  | bool  | True    | When True, dropped-down ranger will grow / shrink when summoned                          |
| `tmux_dropdown_duration` | float | 500     | Drop-down animation time in miliseconds                                                  |

The default values can be modified by setting them in `~/.config/ranger/rc.conf`:

```
set tmux_cwd_sync true
set tmux_cwd_track true
set tmux_set_title true
set tmux_open_in_window true
```
