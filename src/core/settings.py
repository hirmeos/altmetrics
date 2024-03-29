"""
Common settings for the HIRMEOS Altmetrics project.
"""

from os import environ, pardir, path

from .variables import Origins, StaticProviders  # noqa
from generic import utils


class Config:

    SECRET_KEY = environ.get('SECRET_KEY', 'secret-key')

    APP_DIR = path.dirname(path.dirname(path.abspath(__file__)))
    PROJECT_ROOT = path.abspath(path.join(APP_DIR, pardir))

    # ## Security ##

    SECURITY_PASSWORD_SALT = environ.get('SECURITY_PASSWORD_SALT')
    SECURITY_REGISTERABLE = environ.get('SECURITY_REGISTERABLE', True)

    # ## CELERY ##

    RMQ_USER = environ.get('RMQ_USER')
    RMQ_PASSWORD = environ.get('RMQ_PASSWORD')
    RMQ_HOST = environ.get('RMQ_HOST')
    RMQ_VHOST = environ.get('RMQ_VHOST')

    AMQ_URL = 'amqp://{user}:{password}@{host}:5672/{vhost}'
    RESULT_BACKEND = None
    CELERY_BROKER_URL = AMQ_URL.format(
        user=RMQ_USER,
        password=RMQ_PASSWORD,
        host=RMQ_HOST,
        vhost=RMQ_VHOST
    )

    # ## DATABASES ##

    DB_USER = environ.get('DB_USER')
    DB_PASSWORD = environ.get('DB_PASSWORD')
    DB_HOST = environ.get('DB_HOST')
    DB_NAME = environ.get('DB_NAME')
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

    METRICS_VERSION = '0.5.6'

    # ## Twitter ##
    TWITTER_APP_KEY = environ.get('TWITTER_APP_KEY')
    TWITTER_APP_KEY_SECRET = environ.get('TWITTER_APP_KEY_SECRET')
    TWITTER_ACCESS_TOKEN = environ.get('TWITTER_ACCESS_TOKEN')
    TWITTER_ACCESS_TOKEN_SECRET = environ.get(
        'TWITTER_ACCESS_TOKEN_SECRET'
    )
    TWITTER_LABEL = environ.get('TWITTER_LABEL')

    # # ## PLUGINS ##
    #
    PLUGINS, ORIGINS = utils.load_plugins(
        folder='plugins',
        ignore=[
            'generic',
            '__init__.py',
            '__pycache__',
        ]
    )

    # ## Ignore settings for testing: ##

    if environ.get('CONFIG') != 'TestConfig':
        # ## Mail settings #
        TECH_EMAIL = environ['TECH_EMAIL']
        TECH_NAME = environ.get('TECH_NAME', 'tech')

        MAIL_SERVER = environ.get('MAIL_SERVER', 'localhost')
        MAIL_PORT = environ.get('MAIL_PORT', '587')
        MAIL_USERNAME = environ.get('MAIL_USERNAME')
        MAIL_PASSWORD = environ.get('MAIL_PASSWORD')
        MAIL_DEFAULT_SENDER = environ.get('MAIL_DEFAULT_SENDER')

        SECURITY_CONFIRMABLE = environ.get(
            'SECURITY_CONFIRMABLE', 'True'
        ) == 'True'
        SECURITY_POST_REGISTER_VIEW = '/account/confirmation'

        # ## BEHAVIOUR #

        DAYS_BEFORE_REFRESH = int(environ.get('DAYS_BEFORE_REFRESH', 1))
        PULL_SET_SIZE = int(environ.get('PULL_SET_SIZE', 500))

        # ## Temporary solution to cref cited-by credentials

        CITED_BY_FILE = environ.get('CITED_BY_FILE', 'xref.csv')

        # ## SENTRY ##

        SENTRY_DSN = environ.get('SENTRY_DSN', None)

        # ## REDIS ##

        REDIS_HOST = environ.get('REDIS_HOST', 'localhost')
        REDIS_URL = f'redis://{REDIS_HOST}:6379/0'
        REDIS_PREFIX = environ.get('REDIS_PREFIX')

        # ## METRICS_API ##

        METRICS_API_BASE = environ.get(
            'METRICS_API_BASE', 'http://localhost:8000'
        )

        # ## MEASURES VALUES ## - Expand as plugins are added

        MEASURES_DICT = {  # measure for each origin
            Origins.hypothesis: environ['MEASURES_HYPOTHESIS'],
            Origins.twitter: environ['MEASURES_TWITTER'],
            Origins.wikipedia: environ['MEASURES_WIKIPEDIA'],
            Origins.wordpressdotcom: environ['MEASURES_WORDPRESSDOTCOM'],
        }


class DevConfig(Config):

    DEBUG = True
    FLASK_ENV = 'development'
    JWT_KEY = environ.get('JWT_KEY', 'dev-key-ok-as-is')


class LiveConfig(Config):

    DEBUG = False
    FLASK_ENV = 'production'
    JWT_KEY = environ.get('JWT_KEY', 'LIVE KEY - PLEASE SET THIS!')


class TestConfig(Config):

    DEBUG = True
    TESTING = True
    FLASK_ENV = 'testing'
    JWT_KEY = 'test-not-nb'

    TECH_EMAIL = environ.get('TECH_EMAIL', 'tech@alt.m.com')
