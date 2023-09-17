#!/bin/bash
strace -o "trace.log" ./sender.sh | ./receiver.sh || echo "exit status:${PIPESTATUS[@]}" &


pgrep -f 'receiver.sh' | xargs kill -PIPE
