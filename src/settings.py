#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
#-------------------------------------------------------------------------------
Project		: Health API
Module		: settings
Purpose   	: API server settings
Source		: https://github.com/buraktokman/Health-API
Version		: 0.1.0 beta
Status 		: Development

Modified	: 2023 Apr 1
Created   	: 2023 Mar 29
Author		: Burak Tokman
Email 		: buraktokman@hotmail.com
#-------------------------------------------------------------------------------
'''
# ------ GENERAL ----------------
# TIMEOUT = 60

# ------ GCP --------------------
GCP_PROJECT_ID    		= 'health-api-test'

# ------ POSTGRESQL -------------
SQL_DOCTORS_TABLE 		= 'doctors'
SQL_SPECIALTY_TABLE	    = 'specialty'
SQL_APPOINTMENTS_TABLE 	= 'appointments'
SQL_SHIFTS_TABLE 		= 'shifts'
SQL_PATIENTS_TABLE 		= 'patients'

# TODO: Move credentials to Secret Manager or use environment variables
# SQL_DATABASE_VM_NAME 	= 'health-db'
SQL_HOSTNAME 			= 'localhost'
SQL_PORT 				= '5432'
SQL_USERNAME			= 'postgres'
SQL_PASSWORD 			= 'postgres'
SQL_DATABASE			= 'iatros'

	
