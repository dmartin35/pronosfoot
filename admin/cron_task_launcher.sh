#!/bin/bash
if [ $# -eq 0 ] ; then
echo "Usage: $0 <django-admin command>"
exit 1
fi

export DJANGO_SETTINGS_MODULE=pronosfoot.settings.prod
/home/pronosfoot/.python/venv/pronosfoot/bin/python /home/pronosfoot/pronosfoot/manage.py ${*}
