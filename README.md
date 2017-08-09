# Description

A bash script to dump certain MySQL databases, zip up certain directories, and upload a zipped package to Google Drive.

# Usage 

1. Install gdrive (https://github.com/prasmussen/gdrive). Run `gdrive about` to authenticate.

2. Create a dedicated MySQL user (`backup_user`) with only read and lock permissions for all databases.

3. Create a file `~/.my.cnf` with contents:

	[mysqldump]
	user=<special backup user>
	password=<special backup user's password>

4. Create a file `backup-script/config` with contents:

	declare -a BACKUP_DBs=("db1" "db2")
	declare -a BACKUP_FOLDERS=("/var/www/web1" "/var/www/web2")

5. Add `backup-script/backup_script` to non-root crontab.
