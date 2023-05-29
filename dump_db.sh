#!/bin/bash
#-------------------------------------------------------------------------------
# Project   : Health API
# Module    : dump_db.sh
# Purpose   : Script to dump the database
# Source    : https://github.com/buraktokman/Health-API
# Version   : 0.1.0 beta
# Status    : Development

# Modified  : 2023 Apr 1
# Created   : 2023 Apr 1
# Author	: Burak Tokman
# Email     : buraktokman@hotmail.com
#-------------------------------------------------------------------------------
DB_USER='postgres'
DB_PASS='postgres'
DB_HOST='localhost'
DB_NAME='health'
BACKUP_PATH='/home/burak/Desktop'

pg_dump -U $DB_USER -h $DB_HOST -d $DB_NAME -F c -b -v -f $BACKUP_PATH/$DB_NAME-$(date +%Y-%m-%d_%H-%M-%S).sql
