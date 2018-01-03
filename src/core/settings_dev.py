from .settings import *


config = RawConfigParser()
config.read('../local.ini')


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


# ## LOGGING ##

RAVEN_CONFIG = {  # Sentry.
    'dsn': config.get('sentry', 'DSN'),
    'release': SENTRY_RELEASE
}

# ## EXTERNAL SERVICES ##
