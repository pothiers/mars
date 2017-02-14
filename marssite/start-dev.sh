#!/bin/bash

source /opt/mars/venv/bin/activate
top=/sandbox/mars

# NB: "unbuffer" is a small script that comes with the "excpect" package
# --insecure
nohup unbuffer python3 -u $top/marssite/manage.py runserver 0.0.0.0:8000  >  /var/log/mars/server.log &

