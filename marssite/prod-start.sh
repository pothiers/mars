#!/bin/sh
LOG=/var/log/mars/mars.log
cd /opt/mars/marssite
gunicorn --env DJANGO_SETTINGS_MODULE=marssite.settings \
	 --bind 0.0.0.0:8000 \
	 marssite.wsgi:application >> $LOG &

