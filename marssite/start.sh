#!/bin/sh

#LOG=$HOME/mars.log
LOG=/etc/mars/mars.log

pushd ~/sandbox/mars/marssite
# NB: "unbuffer" is a small script that comes with the "excpect" package
nohup unbuffer python3 -u manage.py runserver 0.0.0.0:8000 >  $LOG &
# gunicorn --bind 0.0.0.0:8000 marssite.wsgi:application
tail -F $LOG &




