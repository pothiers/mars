#!/bin/bash
# Install and (re)start MARS on provisioned MARS host
# run as: devops

source /opt/mars/venv/bin/activate

########################
## Install
# run in place


########################
## ReStart
pkill -u devops  -f runserver

# NB: "unbuffer" is a small script that comes with the "excpect" package
# --insecure
nohup unbuffer python3 -u /opt/mars/marssite/manage.py runserver 0.0.0.0:8000 \
      >  /var/log/mars/server.log &

