"""
Django settings for marketaccess project.

Generated by 'django-admin startproject' using Django 1.11.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'tcy4z8^vl8)3!zne519s^!#+69l+_=_p#y84*s@+jl@ewvrylo'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'django.contrib.sites',
    'django_elasticsearch_dsl',
    'directory_header_footer',
    'directory_constants',
    'django.contrib.admin',
    # django library for dealing with hierarchical elements
    'mptt',
    # our apps
    'govuk_template',
    'barriers',
    'backend'
]

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'sso.middleware.SSOUserMiddleware',
]

ROOT_URLCONF = 'marketaccess.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ BASE_DIR + 'templates' ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
                'directory_header_footer.context_processors.sso_processor',
                ('directory_header_footer.context_processors.'
                 'header_footer_context_processor'),
                'django.contrib.auth.context_processors.auth',
            ],
        },
    },
]

WSGI_APPLICATION = 'marketaccess.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_HOST = os.environ.get('STATIC_HOST', '')
STATIC_URL = STATIC_HOST + '/static/'
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

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
            'level': os.getenv('DJANGO_LOG_LEVEL', 'ERROR'),
        },
    },
}

# Elasticsearch config, now using elasticsearch-dsl
# because Haystack doesn't support ES 5.0
ELASTICSEARCH_DSL={
    'default': {
        'hosts': 'localhost:9200'
    },
    # from https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-lang-analyzer.html#english-analyzer
    'analysis': {
      'filter': {
        'english_stop': {
          'type':       "stop",
          'stopwords':  '_english_'
        },
        'english_keywords': {
          'type':       'keyword_marker',
          'keywords':   ['example']
        },
        "english_stemmer": {
          'type':       'stemmer',
          'language':   'english'
        },
        'english_possessive_stemmer': {
          'type':       'stemmer',
          'language':   'possessive_english'
        }
      },
      'analyzer': {
        'english': {
          'tokenizer':  'standard',
          'filter': [
            'english_possessive_stemmer',
            'lowercase',
            'english_stop',
            'english_keywords',
            'english_stemmer'
          ]
        }
      }
    }
}

# ELASTICSEARCH_DEFAULT_ANALYZER = "english_analyzer"

# directory-api
API_CLIENT_CLASSES = {
    'default': 'directory_api_client.client.DirectoryAPIClient',
    'unit-test': 'directory_api_client.dummy_client.DummyDirectoryAPIClient',
}
API_CLIENT_CLASSES = {
    'default': 'directory_api_client.client.DirectoryAPIClient',
    'unit-test': 'directory_api_client.dummy_client.DummyDirectoryAPIClient',
}
API_CLIENT_CLASS_NAME = os.getenv('API_CLIENT_CLASS_NAME', 'default')
API_CLIENT_CLASS = API_CLIENT_CLASSES[API_CLIENT_CLASS_NAME]
API_CLIENT_BASE_URL = os.getenv(    'API_CLIENT_BASE_URL',
    'http://api.trade.great.dev:8000'
)
API_SIGNATURE_SECRET = os.getenv(
    'API_SIGNATURE_SECRET',
    'debug'
)
# for the 'directory-header-footer' app (https://github.com/uktrade/directory-header-footer)
SSO_LOGIN_URL=os.getenv(
    'SSO_LOGIN_URL',
    'http://sso.trade.great.dev:8004/accounts/login/'
)
SSO_SIGNUP_URL=os.getenv(
    'SSO_SIGNUP_URL',
    'http://sso.trade.great.dev:8004/accounts/signup/'
)
SSO_LOGOUT_URL=os.getenv(
    'SSO_LOGOUT_URL',
    'http://sso.trade.great.dev:8004/accounts/logout/?next=http://traderemedies.trade.great.dev:8000/search/govuk/'
)
SSO_PROFILE_URL=os.getenv(
    'SSO_PROFILE_URL',
    'http://profile.trade.great.dev:8006'
)
SSO_PASSWORD_RESET_URL=os.getenv(
    'SSO_PASSWORD_RESET_URL',
    '???'
)
HEADER_FOOTER_CONTACT_US_URL=os.getenv(
    'HEADER_FOOTER_CONTACT_US_URL',
    'https://contact-us.export.great.gov.uk/directory',
)
HEADER_FOOTER_CSS_ACTIVE_CLASSES=os.getenv(
    'HEADER_FOOTER_CSS_ACTIVE_CLASSES',
    'xxx'
)
SSO_SESSION_COOKIE=os.getenv(
    'SSO_SESSION_COOKIE',
    'debug_sso_session_cookie'
)
SSO_SIGNATURE_SECRET=os.getenv(
    'SSO_SIGNATURE_SECRET',
    'proxy_signature_debug'
)
COMPANIES_HOUSE_API_KEY=os.getenv(
    'COMPANIES_HOUSE_API_KEY',
    'debug'
)
COMPANIES_HOUSE_ITEMS_PER_PAGE = 5
COMPANIES_HOUSE_CLIENT_ID=os.getenv(
    'COMPANIES_HOUSE_CLIENT_ID',
    'debug-client-id'
)
COMPANIES_HOUSE_CLIENT_SECRET=os.getenv(
    'COMPANIES_HOUSE_CLIENT_SECRET',
    'debug-client-secret'
)
SSO_API_CLIENT_BASE_URL='http://sso.trade.great.dev:8004/'
