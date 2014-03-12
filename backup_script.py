# Written for Python 2.7 for Linux Servers
# Author: Vighnesh Iyer

"""Dependencies:
pip install httplib2
pip install google-api-python-client
MAKE SURE that your PYTHONPATH contains the library path ( in Ubuntu make sure ~/.profile contains export PYTHONPATH=$PYTHONPATH:/usr/local/lib/python2.7/dist-packages/ )
"""
import time
import subprocess
import sys
import os
import xrange
#import httplib2
#import pprint
import logging
import calendar
from email.mime.text import MIMEText
#import smtplib

from userparams import UserParams
import os_functions
import mysql_functions

#from apiclient.discovery import build
#from apiclient.http import MediaFileUpload
#from oauth2client.client import OAuth2WebServerFlow
#from oauth2client.file import Storage

logging.basicConfig()

params = UserParams('config.dat')
params.fetch_params()
# params.params is a dictionary with the parameter names mapped to the user entered values in the config file

# Generate the name of the folder in which all the SQL and directory zips will go
backup_folder_name = params.params['backup_prefix'] + '_' + params.params['current_date_string'] + '_' + params.params['current_time_string'] # kpdb_02-17-2014_12:17:23
# Generate the absolute path to the main backup folder
backup_folder_path = params.params['working_path'] + backup_folder_name + '/' # /home/kp_backup/files/kpdb_02-17-2014_12:17:23/

# Actually create the main backup folder
if not os.path.exists(backup_folder_path):
	os.makedirs(backup_folder_path)

# Run mysqldump and dump all the SQL files into the main backup folder
for index in xrange(0, params.params['db_name'].length()):
	name = params.params['db_name'][index]
	user = params.params['db_user'][index]
	user_pwd = params.params['db_user_password'][index]
	dest_path = backup_folder_path
	filename = params.params['db_prefix'][index] + '_' + params.params['current_date_string'] + '.sql'
	attempt_dump(name, user, user_pwd, dest_path, filename)