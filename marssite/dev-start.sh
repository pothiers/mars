#!/bin/sh

#LOG=$HOME/mars.log
LOG=/var/log/mars/server.log

pushd ~/sandbox/mars/marssite

# NB: "unbuffer" is a small script that comes with the "excpect" package
nohup unbuffer python3 -u manage.py  runserver --insecure 0.0.0.0:8000 >  /var/log/mars/server.log &
echo "tail -F $LOG"
tail -F $LOG
