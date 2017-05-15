#!/bin/sh
LOG=/var/log/mars/mars.log
cd /opt/mars/marssite
# Stop old
pkill -f "manage.py runserver"
pkill -f gunicorn

gunicorn --env DJANGO_SETTINGS_MODULE=marssite.settings \
	 --bind 0.0.0.0:8000 \
	 marssite.wsgi:application >> $LOG &

