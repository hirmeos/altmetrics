"""
Common settings for the HIRMEOS Metrics project.
"""

from enum import IntEnum
from os import getenv, pardir, path
import re

from generic import utils

re._pattern_type = re.Pattern  # Py3.7 workaround for re module used by celery


# ## Enums used to keep track of origins and providers ##

class Origins(IntEnum):
    twitter = 1
    citation = 2
    wikipedia = 3
    hypothesis = 4
    facebook = 5
    wordpressdotcom = 6


class StaticProviders(IntEnum):
    """Used to keep track of the provider of a given event. Used by Plugins
    to provide a link to the full event record, based on the external event ID.
    """
    crossref_cited_by = 1
    crossref_event_data = 2
    facebook = 3
    twitter = 4
    hypothesis = 5


class Config(object):

    SECRET_KEY = getenv('SECRET_KEY', 'secret-key')

    APP_DIR = path.dirname(path.dirname(path.abspath(__file__)))
    PROJECT_ROOT = path.abspath(path.join(APP_DIR, pardir))

    # ## Security ##

    SECURITY_PASSWORD_SALT = getenv('SECURITY_PASSWORD_SALT')
    SECURITY_REGISTERABLE = getenv('SECURITY_REGISTERABLE', True)

    # ## CELERY ##

    RMQ_USER = getenv('RMQ_USER')
    RMQ_PASSWORD = getenv('RMQ_PASSWORD')
    RMQ_HOST = getenv('RMQ_HOST')
    RMQ_VHOST = getenv('RMQ_VHOST')

    CELERY_BROKER_URL = 'amqp://{user}:{password}@{host}:5672/{vhost}'.format(
        user=RMQ_USER,
        password=RMQ_PASSWORD,
        host=RMQ_HOST,
        vhost=RMQ_VHOST
    )
    RESULT_BACKEND = "amqp"

    # ## DATABASES ##
    DB_USER = getenv('DB_USER')
    DB_PASSWORD = getenv('DB_PASSWORD')
    DB_HOST = getenv('DB_HOST')
    DB_NAME = getenv('DB_NAME')
    PORT = '5432'

    SQLALCHEMY_DATABASE_URI = (
        'postgresql://{user}:{passwd}@{host}:{port}/{db}'.format(
            user=DB_USER,
            passwd=DB_PASSWORD,
            host=DB_HOST,
            port=PORT,
            db=DB_NAME,
        )
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ## LOGGING ##

    # TODO: set up logging

    METRICS_VERSION = "0.0.9"

    # # ## PLUGINS ##
    #
    PLUGINS, ORIGINS = utils.load_plugins(
        folder='plugins',
        ignore=[
            'generic',
            '__pycache__',
            "facebook",
            "twitter",
            "crossref_cited_by",
        ]
    )
    TECH_EMAIL = getenv('TECH_EMAIL', 'example@example.org')
    # ## BEHAVIOUR #

    DAYS_BEFORE_REFRESH = 7

    # ## Temporary solution to cref cited-by credentials

    CITED_BY_FILE = getenv('CITED_BY_FILE', 'xref.csv')

    # ## SENTRY ##

    SENTRY_DSN = getenv('SENTRY_DSN', None)


class DevConfig(Config):
    DEBUG = True
    FLASK_ENV = "development"


class LiveConfig(Config):
    DEBUG = False
    FLASK_ENV = "production"
