"""
WSGI config for marketaccess project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/

Actually this is now based on
https://stackoverflow.com/questions/26979579/django-mod-wsgi-set-os-environment-variable-from-apaches-setenv
but it didn't work properly so I added an answer...
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "marketaccess.settings.production")

def application(environ, start_response):
    for key in environ:
        if key.startswith('MARKETACCESS_'):
            os.environ[key] = environ[key]
    return get_wsgi_application()(environ, start_response)
