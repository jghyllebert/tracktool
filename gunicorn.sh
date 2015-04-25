#!/bin/bash
set -e
LOGFILE=/var/www/log/gunicorn/tracktool.log
LOGDIR=$(dirname $LOGFILE)
# user/group to run as
USER=jghyllebert
GROUP=jghyllebert
cd /var/tracktool/tracktool
# Path to activate file
source /var/tracktool/bin/activate
test -d $LOGDIR || mkdir -p $LOGDIR
#Path to gunicorn_django executable
exec ../bin/gunicorn -w 3 \
--pythonpath /var/tracktool/ \
--settings tracktool.settings \
--user=$USER --group=$GROUP --log-level=info \
--log-file=$LOGFILE 2>>$LOGFILE --bind=unix:/var/tracktool/tracktool.sock tracktool/settings.py
