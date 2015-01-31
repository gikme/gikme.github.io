#!/bin/bash

GIT_ROOT=/var/www/gik.me/pelican_site
VIRTUALENV=/var/www/gik.me/.env/bin
PELICAN=$VIRTUAENV/pelican
PY=$VIRTUAENV/python
PIP=$VIRTUAENV/pip
INPUTDIR=$GIT_ROOT/site/content
OUTPUTDIR=$GIT_ROOT/site/output
CONFFILE=$GIT_ROOT/site/publishconf.py


cd $GIT_ROOT
$PIP install -r requirements.txt
$PELICAN $INPUTDIR -o $OUTPUTDIR -s $CONFFILE
