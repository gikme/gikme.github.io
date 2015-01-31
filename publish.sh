#!/bin/bash

GIT_ROOT="/var/www/gik.me/pelican_site"
VIRTUALENV="/var/www/gik.me/.env/bin"
PELICAN="$VIRTUALENV/pelican"
PY="$VIRTUALENV/python"
PIP="$VIRTUALENV/pip"
INPUTDIR="$GIT_ROOT/site/content"
OUTPUTDIR="$GIT_ROOT/site/output"
CONFFILE="$GIT_ROOT/site/publishconf.py"


cd $GIT_ROOT
git pull
$PIP install -r requirements.txt
cd $GIT_ROOT/site
$PELICAN $INPUTDIR -o $OUTPUTDIR -s $CONFFILE > $GIT_ROOT/../last.log
