from email.mime.text import MIMEText

from apiclient.discovery import build
from apiclient.http import MediaFileUpload
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage

#from apiclient import discovery
#from apiclient.http import MediaFileUpload
#from oauth2client.file import Storage
#from oauth2client import client
#from oauth2client import tools

import os
import zipfile
import zlib
import httplib2
import smtplib
import subprocess
import sys

def terminate(message, subject, params):
	print(params)
	if 'from_email' in params.keys() and 'to_email' in params.keys():
		msg = MIMEText(message + '\n' + params['current_date_string'] + ' ' + params['current_time_string'])
		if not subject:
			msg['Subject'] = 'Backup Error' + ' ' + params['current_date_string'] + ' ' + params['current_time_string']
		else:
			msg['Subject'] = 'Backup Error - ' + subject + ' ' + params['current_date_string'] + ' ' + params['current_time_string']
		msg['From'] = params['from_email']
		msg['To'] = params['to_email']
		s = smtplib.SMTP('localhost')
		s.sendmail(params['from_email'], params['to_email'], msg.as_string())
		s.quit()
	sys.exit(subject + '\n' + message + "\nScript Exiting")

def sendmail(subject, message, from_address, to_address):
	msg = MIMEText(message)
	msg['Subject'] = subject
	msg['From'] = from_address
	msg['To'] = to_address

	s = smtplib.SMTP('localhost')
	s.sendmail(from_address, to_address, msg.as_string())
	s.quit()

def zip_a_file(dir_to_be_zipped, destination_dir, destination_filename_prefix):
#
#	os.chdir(destination_dir)
#	if not destination_filename_prefix:
#		zipf = zipfile.ZipFile(os.path.basename(os.path.normpath(dir_to_be_zipped)) + '.zip', 'w', zipfile.ZIP_DEFLATED)
#	else:
#		zipf = zipfile.ZipFile(destination_filename_prefix + '_' + os.path.basename(os.path.normpath(dir_to_be_zipped)) + '.zip', 'w', zipfile.ZIP_DEFLATED)
#	os.chdir(os.path.dirname(dir_to_be_zipped))
#	for root, dirs, files in os.walk(dir_to_be_zipped):
#		for file in files:
#			zipf.write(os.path.join(root, file))
#	zipf.close();
	print('Zipping ' + os.path.dirname(dir_to_be_zipped))
	os.chdir(os.path.dirname(os.path.dirname(dir_to_be_zipped)))
	dir_name = os.path.basename(os.path.normpath(dir_to_be_zipped))
	if not destination_filename_prefix:
		zip_filename = dir_name + '.zip'
	else:
		zip_filename = destination_filename_prefix + '_' + dir_name + '.zip'
	try:
		zip_status = subprocess.check_output('zip -r ' + zip_filename + ' '+ dir_name + ' > /dev/null && mv ' + zip_filename + ' ' + destination_dir, shell=True, stderr=subprocess.STDOUT)
	except subprocess.CalledProcessError as e:
		if e.returncode == 1:
			pass
		else:
			raise

def upload_to_google_drive(file_to_be_uploaded, filename, params, flags):
	"""
	CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), 'client_secrets.json')
	FLOW = client.flow_from_clientsecrets(CLIENT_SECRETS,
	  scope=[
	      'https://www.googleapis.com/auth/drive',
	      'https://www.googleapis.com/auth/drive.appdata',
	      'https://www.googleapis.com/auth/drive.apps.readonly',
	      'https://www.googleapis.com/auth/drive.file',
	      'https://www.googleapis.com/auth/drive.metadata.readonly',
	      'https://www.googleapis.com/auth/drive.readonly',
	      'https://www.googleapis.com/auth/drive.scripts',
	    ],
	    message=tools.message_if_missing(CLIENT_SECRETS))

	storage = Storage('credentials.dat')
	credentials = storage.get()
	if credentials is None or credentials.invalid:
		credentials = tools.run_flow(FLOW, storage, flags)

	http = httplib2.Http()
	http = credentials.authorize(http)
	service = discovery.build('drive', 'v2', http=http)

	"""
	storage = Storage('credentials.dat')

	if not storage.get():
		# Authenticate with Google Drive
		flow = OAuth2WebServerFlow(params.params['client_id'], params.params['client_secret'], params.params['oauth_scope'], params.params['redirect_url'])
		authorize_url = flow.step1_get_authorize_url()
		print 'Go to the following link in your browser: ' + authorize_url
		code = raw_input('Enter verification code: ').strip()
		credentials = flow.step2_exchange(code)
		storage.put(credentials)
	else:
		credentials = storage.get()

	http = httplib2.Http()
	http = credentials.authorize(http)
	drive_service = build('drive', 'v2', http=http)
	
	print 'Auth success!' # Debug purposes

	media_body = MediaFileUpload(file_to_be_uploaded, mimetype='application/zip', resumable=True)
	body = {
		'title': filename,
		'description': 'Backup ' + params.params['current_date_string'] + ' ' + params.params['current_time_string'],
		'mimeType': 'application/zip'
	}

	file = drive_service.files().insert(body=body, media_body=media_body).execute()
