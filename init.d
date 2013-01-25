#!/bin/bash

DAEMON=/usr/bin/python
ARGS="/home/pi/git/sloth/sloth.py"
PIDFILE=/var/run/sloth/sloth.pid
LOG_DIR=/var/log/sloth

case "$1" in
  start)
    echo "Starting server"
    /sbin/start-stop-daemon --start --pidfile $PIDFILE \
        --user root --group root \
        -b --make-pidfile \
        --chuid root \
        --exec $DAEMON $ARGS
    ;;
  stop)
    echo "Stopping server"
    /sbin/start-stop-daemon --stop --pidfile $PIDFILE --verbose
    ;;
  *)
    echo "Usage: /etc/init.d/sloth {start|stop}"
    exit 1
    ;;
esac

exit 0
