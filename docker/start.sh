#!/bin/bash

set -m
set -e

/usr/bin/python /var/www/django-template/update.py

# Read option for create super user
echo "from django.contrib.auth.models import User; User.objects.create_superuser('${ADMIN_USER}', 'admin@example.com', '${ADMIN_PWD}')" | /usr/bin/python /var/www/django-template/mysite/manage_prod.py shell

/bin/chown -R www-data:www-data /var/www/django-template/

/usr/sbin/apache2ctl -DFOREGROUND