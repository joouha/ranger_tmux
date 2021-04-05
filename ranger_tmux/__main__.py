# -*- coding: utf-8 -*-
import argparse
import importlib.resources
import os
import sys
from pathlib import Path

TMUX_CONFIG = [
    ["#-#-#", "start_of_ranger_tmux_config", "#-#-#"],
    ["bind-key", "Bspace", "run-shell", "-b", f"{sys.executable} -m ranger_tmux.drop"],
    # [
    # "bind-key",
    # "Tab",
    # "split-pane",
    # "-hbf",
    # "-l",
    # "30",
    # f"{util.get_ranger_script()}"
    # ' --cmd="set tmux_cwd_track True"'
    # ' --cmd="set viewmode multipane"'
    # " --cmd=tmux_cwd_track_now",
    # ],
    ["#-#-#", "end_of_ranger_tmux_config", "#-#-#"],
]


def tmux_keybindings(install=True):

    tmux_user_config_path = Path.home() / ".tmux.conf"
    tmux_config_lines = [
        " ".join(
            [
                # Quote command components if they contain spaces
                (f"'{cmd}'" if " " in cmd else str(cmd))
                for cmd in line
            ]
        )
        for line in TMUX_CONFIG
    ]
    new_lines = []
    if tmux_user_config_path.exists():
        # Read existing lines
        with open(tmux_user_config_path, "r") as f:
            old_lines = [x.strip() for x in f.readlines()]
        # Search for tmux_ranger config in tmux config
        start_line = len(old_lines) + 1
        for i, line in enumerate(old_lines):
            if line == tmux_config_lines[0]:
                start_line = i
                break
        end_line = start_line
        for i in range(start_line, len(old_lines)):
            if old_lines[i] == tmux_config_lines[-1]:
                end_line = i
                break
        # Merge in the new config
        new_lines += old_lines[:start_line]
        if install:
            new_lines += tmux_config_lines
        new_lines += old_lines[end_line + 1 :]
    else:
        # No config at all, just use ours
        new_lines += tmux_config_lines

    # Write the updated tmux configuration file
    with open(tmux_user_config_path, "w") as f:
        f.write("\n".join(new_lines) + "\n")

    return TMUX_CONFIG[1:-1]


def confirm_choice(query, options=("y", "n")):
    while True:
        confirm = input(f"{query} ({'/'.join(options)})\n")
        if confirm.lower() in options:
            return confirm
        else:
            print("Invalid Option. Please Enter a Valid Option.")


def install(args):
    print("Installing ranger_tmux plugin")
    print(f"- Plugin installation located at `{args.plugin_script_path}`")
    if args.ranger_plugin_path.exists():
        print("- Removing existing symlink")
        args.ranger_plugin_path.unlink(missing_ok=True)
    print(f"- Creating symlink at `{args.ranger_plugin_path}`")
    args.ranger_plugin_path.symlink_to(args.plugin_script_path)

    if args.tmux is None:
        tmux = (
            confirm_choice(
                "Do you want to install a key-binding for"
                " drop-down ranger in `~/.tmux.conf`?",
                ("y", "n"),
            )
            == "y"
        )
    else:
        tmux = args.tmux
    if tmux:
        print("Installing tmux key-bindings")
        tmux_keybindings(install=True)

    print("Installation complete")


def uninstall(args):
    print("Uninstalling ranger_tmux plugin")
    if args.ranger_plugin_path.exists():
        print(f"- Removing existing symlink `{args.ranger_plugin_path}`")
        args.ranger_plugin_path.unlink(missing_ok=True)

    if args.tmux:
        print("Uninstalling tmux key-bindings")
        tmux_keybindings(install=False)

    print("Uninstallation complete")


def reinstall(args):
    uninstall(args)
    install(args)


def main():
    parser = argparse.ArgumentParser(description="Install ranger_tmux plugin")
    parser.add_argument(
        "--tmux",
        default=None,
        action=argparse.BooleanOptionalAction,
        help="Install/uninstall key-bindings for tmux",
    )
    subparsers = parser.add_subparsers(
        help="Command to run", dest="command", required=True
    )
    parser_install = subparsers.add_parser("install", help="Install plugin")
    parser_install.set_defaults(func=install)
    parser_uninstall = subparsers.add_parser("uninstall", help="Unnstall plugin")
    parser_uninstall.set_defaults(func=uninstall)
    parser_reinstall = subparsers.add_parser("reinstall", help="Re-install plugin")
    parser_reinstall.set_defaults(func=reinstall)

    parser.add_argument(
        "--plugin_script_path",
        help=argparse.SUPPRESS,
        default=importlib.resources.files("ranger_tmux").joinpath("plugin.py"),
    )
    parser.add_argument(
        "--ranger_plugin_path",
        help=argparse.SUPPRESS,
        default=Path(
            os.environ.get(
                "XDG_CONFIG_HOME",
                Path.home() / ".config",
            )
        )
        / "ranger"
        / "plugins"
        / "ranger_tmux.py",
    )

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
