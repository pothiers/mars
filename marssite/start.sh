#!/bin/bash
# PURPOSE:
#   Start MARS server
#

SCRIPT=$(readlink -e $0)     #Absolute path to this script
SCRIPTDIR=$(dirname $SCRIPT) #Absolute path this script is in

#LOG=$HOME/mars.log
LOG=/var/log/mars/mars.log

# NB: "unbuffer" is a small script that comes with the "excpect" package
#!pushd $SCRIPTDIR
#! nohup unbuffer python3 -u manage.py runserver 0.0.0.0:8000 >  $LOG &

# Simplist way to insure projec is on PYthon path is run from same dir
# as manage.py file
# gunicorn --bind 0.0.0.0:8000 marssite.wsgi:application

gunicorn --pythonpath /opt/mars/marssite  --bind 0.0.0.0:8000 marssite.wsgi:application

#! uwsgi --pythonpath /opt/mars/marssite --http :8000 --module marssite.wsgi
# Proved this stack operates correctly:
#  : the web client <-> uWSGI <-> Django

#! uwsgi --pythonpath /opt/mars/marssite --socket :8001 --module marssite.wsgi
# Browse: http://localhost:8000/
# Proved this stack operates correctly:
#  : the web client <-> the web server <-> the socket <-> uWSGI <-> Python
# (But ADMIN/javascript not working)

# With nginx server started and its config pointing
# /static to /var/www/mars/static
#! uwsgi --pythonpath /opt/mars/marssite --socket :8001 --module marssite.wsgi
# Proved this stack operates correctly:
#  : the web client <-> the web server <-> the socket <-> uWSGI <-> Python
# AND css for admin works!


popd

# tail -F $LOG &

# To find where mars is installed:
#   python3 -m inspect -d marssite

# For development
# python3 manage.py runserver --insecure 0.0.0.0:8000
