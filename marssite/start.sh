#!/bin/sh

nohup python3 -u manage.py runserver 0.0.0.0:8000 > $HOME/mars.log &


