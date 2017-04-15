#!/bin/bash
if [ $# -eq 0 ] ; then
echo "Usage: $0 script [script_args]"
exit 1
fi

export PYTHONPATH=/home/pronosfoot/modules:/home/pronosfoot
export DJANGO_SETTINGS_MODULE=pronosfoot.settings
cd /home/pronosfoot/pronosfoot/admin
python -W ignore $@

