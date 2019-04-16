"""
Common settings for the HIRMEOS Altmetrics project.
"""

from enum import IntEnum
from os import getenv, pardir, path
import re

from nameko.standalone.rpc import ClusterRpcProxy

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
    hirmeos_altmetrics = 6


class Config:

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

    AMQ_URL = 'amqp://{user}:{password}@{host}:5672/{vhost}'
    RESULT_BACKEND = None
    CELERY_BROKER_URL = AMQ_URL.format(
        user=RMQ_USER,
        password=RMQ_PASSWORD,
        host=RMQ_HOST,
        vhost=RMQ_VHOST
    )

    # ## Nameko

    NAMEKO_USER = getenv('NAMEKO_USER')
    NAMEKO_PASSWORD = getenv('NAMEKO_PASSWORD')
    NAMEKO_VHOST = getenv('NAMEKO_VHOST')

    NAMEKO_BROKER_URL = AMQ_URL.format(
        user=NAMEKO_USER,
        password=NAMEKO_PASSWORD,
        host=RMQ_HOST,
        vhost=NAMEKO_VHOST
    )

    NAMEKO_CONFIG = {
        'AMQP_URI': NAMEKO_BROKER_URL,
        'WEB_SERVER_ADDRESS': '{host}:15672'.format(host=RMQ_HOST),
        'rpc_exchange': 'nameko-rpc',
        'max_workers': 10,
        'parent_calls_tracked': 10,
    }

    CLUSTER_RPC = ClusterRpcProxy(NAMEKO_CONFIG)

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

    METRICS_VERSION = '0.2.25'

    # ## Twitter ##
    TWITTER_APP_KEY = getenv('TWITTER_APP_KEY')
    TWITTER_APP_KEY_SECRET = getenv('TWITTER_APP_KEY_SECRET')
    TWITTER_ACCESS_TOKEN = getenv('TWITTER_ACCESS_TOKEN')
    TWITTER_ACCESS_TOKEN_SECRET = getenv(
        'TWITTER_ACCESS_TOKEN_SECRET'
    )
    TWITTER_LABEL = getenv('TWITTER_LABEL')

    # # ## PLUGINS ##
    #
    PLUGINS, ORIGINS = utils.load_plugins(
        folder='plugins',
        ignore=[
            'generic',
            '__init__.py',
            '__pycache__',
            'facebook',
            'crossref_cited_by',
        ]
    )

    # ## Mail settings #

    TECH_EMAIL = getenv('TECH_EMAIL', 'tech@ubiquitypress.com')
    TECH_NAME = getenv('TECH_NAME', 'tech')

    MAIL_SERVER = getenv('MAIL_SERVER', 'localhost')
    MAIL_PORT = getenv('MAIL_PORT', '587')
    MAIL_USERNAME = getenv('MAIL_USERNAME')
    MAIL_PASSWORD = getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = getenv('MAIL_DEFAULT_SENDER')

    SECURITY_CONFIRMABLE = getenv('SECURITY_CONFIRMABLE', 'True') is 'True'
    SECURITY_POST_REGISTER_VIEW = '/account/confirmation'

    # ## BEHAVIOUR #

    DAYS_BEFORE_REFRESH = 1

    # ## Temporary solution to cref cited-by credentials

    CITED_BY_FILE = getenv('CITED_BY_FILE', 'xref.csv')

    # ## SENTRY ##

    SENTRY_DSN = getenv('SENTRY_DSN', None)

    # ## REDIS ##

    REDIS_HOST = getenv('REDIS_HOST', 'localhost')
    REDIS_URL = f'redis://{REDIS_HOST}:6379/0'


class DevConfig(Config):

    DEBUG = True
    FLASK_ENV = 'development'
    JWT_KEY = getenv('JWT_KEY', 'dev-key-ok-as-is')


class LiveConfig(Config):

    DEBUG = False
    FLASK_ENV = 'production'
    JWT_KEY = getenv('JWT_KEY', 'LIVE KEY - PLEASE SET THIS!')
