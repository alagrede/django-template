try:
    from settings import *
except ImportError:
    pass


DEBUG = False

#ALLOWED_HOSTS = ['82.234.77.122', '192.168.1.10']
ALLOWED_HOSTS = ['localhost', 'vps115252.ovh.net']

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    #'default': {
    #    'ENGINE': 'django.db.backends.sqlite3',
    #    'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    #},
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django_template',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': 'db_mysite',
        'PORT': '3306',
        'CONN_MAX_AGE': 600,
     }
}

#if DEBUG:
#    # make all loggers use the console.
#    for logger in LOGGING['loggers']:
#        LOGGING['loggers'][logger]['handlers'] = ['console']
