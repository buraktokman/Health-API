#!/bin/bash
#-------------------------------------------------------------------------------
# Project   : Health API
# Module    : start_api.sh
# Purpose   : Script to start the API server
# Source    : https://github.com/buraktokman/Health-API
# Version   : 0.1.0 beta
# Status    : Development

# Modified  : 2023 Apr 1
# Created   : 2023 Mar 29
# Author	: Burak Tokman
# Email     : buraktokman@hotmail.com
#-------------------------------------------------------------------------------

# python3 main.py
gunicorn -b :8080 main:app
