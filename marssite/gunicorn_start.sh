#!/bin/bash
# see: http://michal.karzynski.pl/blog/2013/06/09/django-nginx-gunicorn-virtualenv-supervisor/


#! python manage.py collectstatic
# then browse to http://localhost:8000/static/images/sitelogo.png

source /opt/mars/venv/bin/activate
gunicorn --pythonpath /opt/mars/marssite  --bind 0.0.0.0:8000 marssite.wsgi:application
