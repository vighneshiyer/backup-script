import os_functions
import subprocess

def attempt_dump(db_name, db_user, db_user_password, destination_path, sql_filename, params):
	try:
		db_dump_status = subprocess.check_output('mysqldump -u ' + db_user + ' -p' + db_user_password + ' ' + db_name + ' > ' + destination_path + sql_filename, shell=True, stderr=subprocess.STDOUT)
		db_dump_status = db_dump_status.decode('utf-8')

	except subprocess.CalledProcessError as e: # Bash error
		print('ERROR | Return Code: ' + e.returncode + 'Cmd: ' + e.cmd + 'Output: ' + e.output)
		terminate('Database dump failed.', params)

	if db_dump_status: # Other error
		print('ERROR | ' + db_dump_status)
		terminate('Database dump failed.', params)