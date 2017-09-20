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

# from elasticsearch import Elasticsearch

# Log transport details (optional):
# logging.basicConfig(level=logging.INFO)

# Parse the auth and host from env:
bonsai = os.environ['BONSAI_URL']
auth = re.search('https\:\/\/(.*)\@', bonsai).group(1).split(':')
host = bonsai.replace('https://%s:%s@' % (auth[0], auth[1]), '')

ELASTICSEARCH_DSL['default']['hosts'] = host
