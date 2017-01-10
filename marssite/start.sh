#!/bin/bash
# PURPOSE:
#   Start MARS server
#

SCRIPT=$(readlink -e $0)     #Absolute path to this script
SCRIPTDIR=$(dirname $SCRIPT) #Absolute path this script is in

#LOG=$HOME/mars.log
LOG=/var/log/mars/mars.log

pushd $SCRIPTDIR
# NB: "unbuffer" is a small script that comes with the "excpect" package
nohup unbuffer python3 -u manage.py runserver 0.0.0.0:8000 >  $LOG &
# gunicorn --bind 0.0.0.0:8000 marssite.wsgi:application
# gunicorn --pythonpath /usr/lib/python3.4/site-packages/marssite --bind 0.0.0.0:8000 marssite.wsgi:application

popd

# tail -F $LOG &

# To find where mars is installed:
#   python3 -m inspect -d marssite

# For development
# python3 manage.py runserver --insecure 0.0.0.0:8000
