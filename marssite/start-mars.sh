#!/bin/bash


source /opt/mars/venv/bin/activate

# NB: "unbuffer" is a small script that comes with the "excpect" package
nohup unbuffer python3 -u /opt/mars/marssite/manage.py  runserver --insecure 0.0.0.0:8000 \
      >  /var/log/mars/server.log &

