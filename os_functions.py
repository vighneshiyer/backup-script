import httplib2
import smtplib
from userparams import UserParams
from email.mime.text import MIMEText

from apiclient.discovery import build
from apiclient.http import MediaFileUpload
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage

import zipfile
import zlib

params = UserParams('config.dat')
params.fetch_params()
current_date = params.params['current_date_string']
current_time = params.params['current_time_string']
from_email = params.params['from_email']
to_email = params.params['to_email']

def terminate(self, message, subject=''):
	msg = MIMEText(message + '\n' + current_date + ' ' + current_time)
	if not subject:
		msg['Subject'] = 'Backup Error' + ' ' + current_date + ' ' + current_time
	else:
		msg['Subject'] = 'Backup Error - ' + subject + ' ' + current_date + ' ' + current_time
	msg['From'] = from_email
	msg['To'] = to_email
	s = smtplib.SMTP('localhost')
	s.sendmail(from_email, to_email, msg.as_string())
	s.quit()
	sys.exit(message + "\nScript Exiting")

def sendmail(self, subject, message, from_address, to_address):
	msg = MIMEText(message)
	msg['Subject'] = subject
	msg['From'] = from_address
	msg['To'] = to_address

	s = smtplib.SMTP('localhost')
	s.sendmail(from_address, to_address, msg.as_string())
	s.quit()

def zip_a_file(dir_to_be_zipped, destination_dir, destination_filename_prefix):
	os.chdir(destination_dir)
	zipf = zipfile.ZipFile(destination_filename_prefix + os.path.dirname(dir_to_be_zipped) + '.zip', 'w', zipfile.ZIP_DEFLATED)
	for root, dirs, files in os.walk(dir_to_be_zipped):
		for file in files:
			zipf.write(os.path.join(root, file))
	zipf.close();

def upload_to_google_drive(file_to_be_uploaded, filename):

	storage = Storage('credentials')

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
		'description': 'Backup ' + current_date + ' ' + current_time,
		'mimeType': 'application/zip'
	}

	file = drive_service.files().insert(body=body, media_body=media_body).execute()
