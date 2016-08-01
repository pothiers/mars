#!/bin/sh

#LOG=$HOME/mars.log
LOG=/var/log/mars/mars.log

pushd ~/sandbox/mars/marssite
# NB: "unbuffer" is a small script that comes with the "excpect" package
nohup unbuffer python3 -u manage.py runserver 0.0.0.0:8000 >  $LOG &
# gunicorn --bind 0.0.0.0:8000 marssite.wsgi:application
# gunicorn --pythonpath /usr/lib/python3.4/site-packages/marssite --bind 0.0.0.0:8000 marssite.wsgi:application
tail -F $LOG &


# To find where mars is installed:
#   python3 -m inspect -d marssite
