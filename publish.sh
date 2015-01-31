#!/bin/bash

GIT_ROOT="/var/www/gik.me/pelican_site"
VIRTUALENV="/var/www/gik.me/.env/bin"
PELICAN="$VIRTULAENV/pelican"
PY="$VIRTULAENV/python"
PIP="$VIRTULAENV/pip"
INPUTDIR="$GIT_ROOT/site/content"
OUTPUTDIR="$GIT_ROOT/site/output"
CONFFILE="$GIT_ROOT/site/publishconf.py"


cd $GIT_ROOT
exec $PIP install -r requirements.txt
exec $PELICAN $INPUTDIR -o $OUTPUTDIR -s $CONFFILE
