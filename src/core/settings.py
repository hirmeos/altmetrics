"""
Django settings for metrics project.
"""

import os
from configparser import RawConfigParser

import raven

from generic import utils


config = RawConfigParser()
config.read('../config.ini')


# ## GENERIC CONFIG ##

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TECH_EMAIL = 'tech@ubiquitypress.com'
ADMINS = (
    ('Tech', 'tech@ubiquitypress.com'),
)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config.get('security', 'SECRET_KEY')

DEBUG = True

ALLOWED_HOSTS = []


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'raven.contrib.django.raven_compat',
    's3direct',
    'core',
    'importer',
    'processor',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': '',
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


# ## STATIC FILES ##

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

# ## VERSION ##

# Updated, committed and tagged using 'bumpversion [major | minor | patch]'
# run on master branch
METRICS_VERSION = '0.1'


# ## DATABASES ##

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config.get('database', 'NAME'),
        'USER': config.get('database', 'USER'),
        'PASSWORD': config.get('database', 'PASSWORD'),
        'HOST': config.get('database', 'HOST'),
        'PORT': config.get('database', 'PORT'),
    }
}


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


# ## INTERNATIONALISATION ##

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# ## STATIC FILES ##

STATIC_URL = '/static/'


# ## CELERY

RMQ_USER = config.get('rmq', 'RMQ_USER')
RMQ_PASSWORD = config.get('rmq', 'RMQ_PASSWORD')
RMQ_URI = config.get('rmq', 'RMQ_URI')

CELERY_BROKER_URL = 'amqp://{user}:{password}@{uri}'.format(
    user=RMQ_USER,
    password=RMQ_PASSWORD,
    uri=RMQ_URI,
)


# ## LOGGING ##

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s '
                      '%(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'sentry': {
            'level': 'ERROR',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
            'tags': {'custom-tag': 'x'},
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'django.security.DisallowedHost': {
            'handlers': ['null'],
            'propagate': False,
        },
    },
}

SENTRY_RELEASE = (
    '{main}-{sha}'.format(
        main=METRICS_VERSION,
        sha=raven.fetch_git_sha(
            os.path.join(
                '/',
                *os.path.dirname(os.path.realpath(__file__)).split('/')[:-2]
            )
        )
    )
)

RAVEN_CONFIG = {  # Sentry.
    'dsn': config.get('sentry', 'DSN'),
    'release': SENTRY_RELEASE
}


# ## PLUGINS ##

AVAILABLE_PLUGINS = utils.load_plugins(folder='providers')


# ## EXTERNAL SERVICES ##

AWS_ACCESS_KEY_ID = config.get('s3', 'AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config.get('s3', 'AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = config.get('s3', 'AWS_STORAGE_BUCKET_NAME')
S3DIRECT_REGION = config.get('s3', 'S3DIRECT_REGION')

S3DIRECT_DESTINATIONS = {
    'default': {
        'key': '/',
    }
}

S3_URL_TEMPLATE = 'https://s3-{region}.amazonaws.com/{bucket_name}'.format(
    region=S3DIRECT_REGION,
    bucket_name=AWS_STORAGE_BUCKET_NAME,
)
