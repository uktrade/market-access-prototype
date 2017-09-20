# marketaccess/settings/dev.py

from marketaccess.settings.base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', False)

ALLOWED_HOSTS = ['market-access-prototype.herokuapp.com']

# Update database configuration with Heroku's $DATABASE_URL config.
import dj_database_url
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

MIDDLEWARE += [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'marketaccess.http_auth_middleware.HttpAuthMiddleware',
]
