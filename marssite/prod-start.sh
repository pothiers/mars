#!/bin/sh
LOG=/var/log/mars/mars.log
cd /opt/mars/marssite
gunicorn --bind 0.0.0.0:8000 marssite.wsgi:application >> $LOG &

