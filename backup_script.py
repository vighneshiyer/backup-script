# Written for Python 2.7 for Linux Servers
# Author: Vighnesh Iyer

"""Dependencies:
pip install httplib2
pip install google-api-python-client
MAKE SURE that your PYTHONPATH contains the library path ( in Ubuntu make sure ~/.profile contains export PYTHONPATH=$PYTHONPATH:/usr/local/lib/python2.7/dist-packages/ )
"""
import os
import logging
import argparse
from oauth2client import tools
import sys

from userparams import UserParams
import os_functions
import mysql_functions

def main(argv):
	parser = argparse.ArgumentParser(
	description=__doc__,
	formatter_class=argparse.RawDescriptionHelpFormatter,
	parents=[tools.argparser])

	flags = parser.parse_args(argv[1:])

	logging.basicConfig()

	params = UserParams('config.dat')
	params.fetch_params()
	# params.params is a dictionary with the parameter names mapped to the user entered values in the config file

	# Generate the name of the folder in which all the SQL and directory zips will go
	backup_folder_name = params.params['backup_prefix'] + '_' + params.params['current_date_string'] + '_' + params.params['current_time_string'] # kpdb_02-17-2014_12:17:23
	# Generate the absolute path to the main backup folder
	backup_folder_path = params.params['working_path'] + '/' + backup_folder_name + '/' # /home/kp_backup/files/kpdb_02-17-2014_12:17:23/

	# Actually create the main backup folder
	if not os.path.exists(backup_folder_path):
		os.makedirs(backup_folder_path)

	# Run mysqldump and dump all the SQL files into the main backup folder
	if params.params['db_backup'] is True:
		for index in xrange(0, params.params['db_name'].__len__()):
			name = params.params['db_name'][index]
			user = params.params['db_user'][index]
			user_pwd = params.params['db_user_password'][index]
			dest_path = backup_folder_path
			filename = params.params['db_prefix'][index] + '_' + params.params['current_date_string'] + '.sql'
			mysql_functions.attempt_dump(name, user, user_pwd, dest_path, filename, params)

	# Zip up all the directories into the main backup folder
	if params.params['dir_backup'] is True:
		for index in xrange(0, params.params['db_name'].__len__()):
			destination_dir = backup_folder_path
			dir_to_be_zipped = params.params['dir_list'][index]
			prefix = params.params['dir_prefix'][index]
			os_functions.zip_a_file(dir_to_be_zipped, destination_dir, prefix)

	# Zip up the main backup folder
	os_functions.zip_a_file(backup_folder_path, params.params['working_path'], '')

	# Upload zipped backup folder to Google Drive
	main_backup_folder_zipped_path = params.params['working_path'] + backup_folder_name + '.zip'
	os_functions.upload_to_google_drive(main_backup_folder_zipped_path, backup_folder_name, params, flags)

	# Send notification email
	os_functions.sendmail(message='Backup completed on ' + params.params['current_date_string'] + ' ' + params.params['current_time_string'],
	subject='Successful Backup',
	from_address=params.params['from_email'],
	to_address=params.params['to_email'])

if __name__ == '__main__':
	main(sys.argv)