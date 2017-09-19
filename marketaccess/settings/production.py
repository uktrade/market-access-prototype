from marketaccess.settings.base import *

import os

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['marketaccess-demo.cluefulmedia.com']

# when we move to another database - still on sqlite for now

DATABASES = {
 'default': {
   'ENGINE': 'django.db.backends.postgresql_psycopg2',
   'NAME': os.environ['MARKETACCESS_DB_NAME'],
   'USER': os.environ['MARKETACCESS_DB_USER'],
   'PASSWORD': os.environ['MARKETACCESS_DB_PASSWORD'],
   'HOST': os.environ['MARKETACCESS_DB_HOST'],
   'PORT': os.environ['MARKETACCESS_DB_PORT']
 }
}

SECRET_KEY = 'ao(i7!witkldhc*%^oex^hir9catusjsgrhbq=20d$8iasdfs&&!s0t^h=($'

STATIC_ROOT = '/var/www/marketaccess-demo.cluefulmedia.com/dit/marketacess/static/'
