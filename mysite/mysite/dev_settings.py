try:
    from settings import *
except ImportError:
    pass


DEBUG = True

ALLOWED_HOSTS = []


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    #'default': {
    #    'ENGINE': 'django.db.backends.sqlite3',
    #    'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    #},
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        #'ENGINE': 'db_multitenant.db.backends.mysql',
        'NAME': 'django_template',
        #'NAME': 'tenant_devnull',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': '127.0.0.1',
        'PORT': '3306',
     },
    #'client1': {
    #    'ENGINE': 'django.db.backends.mysql',
    #    'NAME': 'tenant_client1',
    #    'USER': 'root',
    #    'PASSWORD': 'root',
    #    'HOST': '127.0.0.1',
    #    'PORT': '3306',
    #    },

}


#if DEBUG:
#    # make all loggers use the console.
#    for logger in LOGGING['loggers']:
#        LOGGING['loggers'][logger]['handlers'] = ['console']

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            },
        },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'DEBUG'),
            },
        },
    }