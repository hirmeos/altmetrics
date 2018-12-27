"""
Common settings for the HIRMEOS Metrics project.
"""

from enum import IntEnum
import os

from generic import utils


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


class Config(object):

    SECRET_KEY = os.environ.get('SECRET_KEY', 'secret-key')

    APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))

    # ## CELERY

    RMQ_USER = os.getenv('RMQ_USER')
    RMQ_PASSWORD = os.getenv('RMQ_PASSWORD')
    RMQ_URI = os.getenv('RMQ_URI')

    CELERY_BROKER_URL = 'amqp://{user}:{password}@{uri}'.format(
        user=RMQ_USER,
        password=RMQ_PASSWORD,
        uri=RMQ_URI,
    )

    # ## DATABASES ##
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_HOST = os.getenv('DB_HOST')
    DB_NAME = os.getenv('DB_NAME')
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

    METRICS_VERSION = "0.0.1"

    # # ## PLUGINS ##
    #
    PLUGINS, ORIGINS = utils.load_plugins(
        folder='plugins',
        ignore=[
            'generic',
            '__pycache__',
            "facebook",
            "twitter",
        ]
    )
    TECH_EMAIL = os.getenv('TECH_EMAIL', 'example@example.org')
    # ## BEHAVIOUR #

    DAYS_BEFORE_REFRESH = 7

    # ## Temporary solution to cref cited-by credentials

    CITED_BY_FILE = os.getenv('CITED_BY_FILE', 'xref.csv')


class DevConfig(Config):
    DEBUG = True
    FLASK_ENV = "development"


class LiveConfig(Config):

    DEBUG = False
    FLASK_ENV = "production"
