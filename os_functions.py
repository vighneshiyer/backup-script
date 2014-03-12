import smtplib
from userparams import UserParams
from email.mime.text import MIMEText

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