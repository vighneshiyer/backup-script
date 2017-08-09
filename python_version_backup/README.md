# Description

A Python script I wrote to perform automated regular backups on VPSs. The script can be run as a cron job once it is set up. It is designed to be a set and forget solution for backups to the cloud (Google Drive).

# Installation

1. FTP files to server. You can upload everything including the modules, or you can install them via pip/easy_install

2. Install dependencies. You can install httplib2 and google-api-python-client, or just place the modules in the same folder as the script.

3. Edit config.dat. The options are self-explanatory.

4. Get credentials. 
Go to the [Google quickstart page](https://developers.google.com/api-client-library/python/start/installation) using the Google account you want to backup the files into. Select the Drive API and command line, and click Configure Project.
Download the client secrets file, and upload it to the same directory as the backup script
Download the sample application, and put the client secrets file in its directory
Run the sample application to generate sample.dat (a credentials file)
- Rename sample.dat to credentials.dat and upload it to the server, in the working_path directory.

5. Set up as cron job.

6. Test the script with:
python2.7 backup_script.py