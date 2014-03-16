import ConfigParser
import os
import sys
import time
import calendar
import re
import string
import os_functions

class UserParams:

	def __init__(self, config_file):
		self.config_file = config_file
		self.params = {}

		# Define which parameters to fetch
		# *_params dicts map category to list of params
		# params_list holds dicts to be parsed
		self.general_params = { 'General': ['working_path', 'temp_file_persist_time', 'backup_prefix'] }
		self.mysql_params = { 'Mysql': ['db_backup', 'db_name', 'db_user', 'db_user_password', 'db_prefix']}
		self.email_params = { 'Email': ['to_email', 'from_email']}
		self.dir_params = { 'Directories': ['dir_backup', 'dir_list', 'dir_prefix']}
		self.drive_params = { 'Google Drive': ['client_id', 'client_secret', 'oauth_scope', 'redirect_url']}
		self.params_list = [self.general_params, self.mysql_params, self.email_params, self.dir_params, self.drive_params]

		self.params['current_date_string'] = time.strftime('%m-%d-%Y')
		self.params['current_time_string'] = time.strftime('%H:%M:%S')
		self.params['current_month_string'] = calendar.month_name[int(time.strftime('%m'))]

	# Main fetching method
	def fetch_params(self):
		config = ConfigParser.ConfigParser(allow_no_value=True)
		config.read(self.config_file)
		self.parser_error_catcher(self.fetcher, config)
		self.check_generals()
		self.check_mysql_params()
		self.check_email_params()
		self.check_dir_params()
		self.check_drive_params()

	def fetcher(self, parser):
		for section in self.params_list:
			for option in section.values()[0]:
				self.params[option] = parser.get(section.keys()[0], option).strip(' \t\n\r')

	def parser_error_catcher(self, function_call, function_param = ''):
		try:
			function_call(function_param)
		except ConfigParser.NoSectionError as e:
			os_functions.terminate(e.__str__(), self.params)

###### Section Check Functions ######
	def check_generals(self):
		self.isValidDir(self.params['working_path'])
		self.isPositiveInt(self.params['temp_file_persist_time'])
		self.params['backup_prefix'] = self.makeValidFileName(self.params['backup_prefix'])

	def check_mysql_params(self):
		if not isinstance(self.params['db_backup'], bool):
			self.params['db_backup'] = True if self.params['db_backup'].upper() == 'TRUE' else False
		self.params['db_name'] = self.str_to_list(self.params['db_name'])
		self.params['db_user'] = self.str_to_list(self.params['db_user'])
		self.params['db_user_password'] = self.str_to_list(self.params['db_user_password'])
		self.params['db_prefix'] = self.str_to_list(self.params['db_prefix'])

	def check_email_params(self):
		self.isValidEmail(self.params['to_email'])
		self.isValidEmail(self.params['from_email'])

	def check_dir_params(self):
		if not isinstance(self.params['dir_backup'], bool):
			self.params['dir_backup'] = True if self.params['dir_backup'].upper() == 'TRUE' else False
		self.params['dir_list'] = self.str_to_list(self.params['dir_list'])
		for dir in self.params['dir_list']:
			self.isValidDir(dir)
		self.params['dir_prefix'] = self.str_to_list(self.params['dir_prefix'])

	def check_drive_params(self):
		self.isNotEmpty(self.params['client_id'])
		self.isNotEmpty(self.params['client_secret'])
		self.isNotEmpty(self.params['oauth_scope'])
		self.isNotEmpty(self.params['redirect_url'])

###### Validation Functions ######
	def isNotEmpty(self, param):
		if param is None or not param:
			terminate('Required value is empty', self.params)

	def str_to_list(self, param):
		temp_lst = param.split(',')
		return [db.strip() for db in temp_lst]

	def isValidDir(self, path):
		try:
			if not os.path.isdir(path):
				raise ValueError(path + ' is not a valid directory')
		except ValueError as e:
			os_functions.terminate(e.__str__(), 'Error', self.params)
		return True

	def isPositiveInt(self, number):
		try:
			val = int(number)
			if val <= 0:
				raise Exception
		except ValueError as e:
			terminate(number + ' is not a positive integer', self.params)
		except Exception as e:
			terminate(number + ' is not a positive integer', self.params)
		return True

	def makeValidFileName(self, name):
		valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
		filename = ''.join(c for c in name if c in valid_chars)
		filename = filename.replace(' ','_')
		return filename

	def isValidEmail(self, input):
		if not re.match(r"[^@]+@[^@]+\.[^@]+", input):
			terminate('Invalid email entered')