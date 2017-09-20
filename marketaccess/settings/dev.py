# marketaccess/settings/dev.py

from marketaccess.settings.base import *

DEBUG = True

INSTALLED_APPS += (
    'debug_toolbar',
)

MIDDLEWARE += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'marketaccess.http_auth_middleware.HttpAuthMiddleware',
)

INTERNAL_IPS = ['127.0.0.1', 'localhost']
