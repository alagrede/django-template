# -*- coding: utf-8 -*-

import shutil
import errno
import os
from os import path as os_path
import datetime


today = datetime.datetime.now()

PATH = os_path.abspath(os_path.split(__file__)[0])

shutil.rmtree("dist", ignore_errors=True)

# compile all scripts
os.system('python -m compileall mysite')

#'*.py', 'settings_prod.pyc', 
# copy .pyc
shutil.copytree('mysite', 'dist', ignore = shutil.ignore_patterns('*.pyc', 'prod_settings.py', 'upload', '.idea', 'db.sqlite3', 'mysite.conf'))
shutil.make_archive('app_TEMPLATE__' + today.strftime('%d-%m-%Y_%H%M'), 'zip', '.', 'dist')
shutil.rmtree("dist", ignore_errors=True)




