from .settings_common import *

DEBUG = False

SECRET_KEY = config.get('security', 'SECRET_KEY')


# ## CELERY

RMQ_USER = config.get('rmq', 'RMQ_USER')
RMQ_PASSWORD = config.get('rmq', 'RMQ_PASSWORD')
RMQ_URI = config.get('rmq', 'RMQ_URI')

CELERY_BROKER_URL = 'amqp://{user}:{password}@{uri}'.format(
    user=RMQ_USER,
    password=RMQ_PASSWORD,
    uri=RMQ_URI,
)

ALLOWED_HOSTS += [
    'localhost',
    '127.0.0.1',
    'metrics.ubiquity.press'
]


# ## EXTERNAL SERVICES ##

AWS_ACCESS_KEY_ID = config.get('s3', 'AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config.get('s3', 'AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = config.get('s3', 'AWS_STORAGE_BUCKET_NAME')
S3DIRECT_REGION = config.get('s3', 'S3DIRECT_REGION')

S3_URL_TEMPLATE = 'https://s3-{region}.amazonaws.com/{bucket_name}/'.format(
    region=S3DIRECT_REGION,
    bucket_name=AWS_STORAGE_BUCKET_NAME,
)

STATIC_ROOT = '/static_files/'
STATICFILES_DIRS = [
    ('static', "/static"),
]
