# -*- coding: utf-8 -*-


def init(fm, *args):
    """Extra tmux key-bindings to splt tmux windows."""
    fm.execute_console("map x- shell tmux split-window -v -c %d")
    fm.execute_console("map x| shell tmux split-window -h -c %d")
