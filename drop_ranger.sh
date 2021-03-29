#!/bin/sh

top_command=$(tmux display -t '{top}' -p "#{pane_start_command}")

if [ "$top_command" = "ranger" ]; then
    ( kill -2 $( tmux display-message -p -t '{top}' '#{pane_pid}' ) && tmux send-keys -t '{top}' Q ) || tmux kill-pane -t '{top}'
else
    PANE_DIR=$(tmux display-message -p '#{pane_current_path}')
    tmux split-window -bfv -c "$PANE_DIR" -t '{top}' -l 60% ranger
fi
