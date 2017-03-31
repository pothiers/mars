#!/bin/bash
SCRIPT=$(readlink -e $0)     #Absolute path to this script
SCRIPTDIR=$(dirname $SCRIPT) #Absolute path this script is in

cd $SCRIPTDIR/marssite
./manage.py test
