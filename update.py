# -*- coding: utf-8 -*-

import zipfile
from distutils.dir_util import copy_tree
import shutil
#import errno
import os
from os import path as os_path
from datetime import datetime

SQL_USER = "root"
SQL_PWD = "root"
SQL_BDD = "django_template"

fromDirectory = "dist"
toDirectory = "mysite"


last_file = ""

# delete temp dir dist/
shutil.rmtree("dist", ignore_errors=True)


# create if not exist a backup folder
if not os.path.exists("backup"):
    os.makedirs("backup")


# Find last update.zip in dir by date
for file in os.listdir("."):
    if file.endswith(".zip"):
        if last_file == "":
            last_file = file
        else:
            if datetime.strptime(file.split('__')[1].split('.')[0], '%d-%m-%Y_%H%M') > datetime.strptime(last_file.split('__')[1].split('.')[0], '%d-%m-%Y_%H%M'):
                last_file = file


if last_file != "":

	# make a SQL backup or read last valid backup is more recent
	backup_file = ""
	for file in os.listdir("backup"):
		if datetime.strptime(file.split('__')[1].split('.')[0], '%d-%m-%Y_%H%M') > datetime.strptime(last_file.split('__')[1].split('.')[0], '%d-%m-%Y_%H%M'):
			# there is a backup file more recent than update.zip => we must revert BDD
			backup_file = file
			break
	if backup_file != "":
		# revert update
		# use backup file
		backup_file = 'backup/' + backup_file
		os.system('mysql -u' + SQL_USER + ' -p' + SQL_PWD + ' ' + SQL_BDD + ' < ' + backup_file)
		# delete it
		os.remove(backup_file)
	else:
		# make new backup
		backup_file = 'backup/dump_TEMPLATE__' + last_file.split('__')[1].split('.')[0] + ".sql"
		os.system('mysqldump -u' + SQL_USER + ' -p' + SQL_PWD + ' ' + SQL_BDD + ' > ' + backup_file)


	# extract zip info
	with zipfile.ZipFile(last_file, "r") as z:
	    z.extractall(".")

	# copy sources
	copy_tree(fromDirectory, toDirectory)

	# delete temp dir dist/
	shutil.rmtree("dist", ignore_errors=True)



#cd /app
os.chdir(toDirectory)



os.system('pip install -r requirements.txt')

# make BDD update
os.system('python manage_prod.py migrate')
os.system('python manage_prod.py collectstatic --noinput')

# relaunch services (make in parent bat file)
#Apache.exe -k install
#os.system('net stop Apache2.4')
#os.system('net start Apache2.4')
#
#os.system('net stop FusionService')
#os.system('net start FusionService')

