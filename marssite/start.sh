#!/bin/sh

LOG=$HOME/mars.log
# NB: "unbuffer" is a small script that comes with the "excpect" package
nohup unbuffer python3 -u manage.py runserver 0.0.0.0:8000 >  $LOG &
tail -F $LOG &




