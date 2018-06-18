#!/usr/bin/env python

from configparser import ConfigParser
from os import getenv
from sys import exit

if __name__ == '__main__':
    config = ConfigParser()
    config['database'] = {
        'USER': str(getenv('DB_USER')),
        'PASSWORD': str(getenv('DB_PASSWORD')),
        'HOST': str(getenv('DB_HOST')),
        'PORT': str(getenv('DB_PORT', '5432')),
        'ENGINE': str(getenv('DB_ENGINE', 'postgresql')),
        'NAME': str(getenv('DB_NAME'))
    }

    config['security'] = {
        'SECRET_KEY': str(getenv('SECRET_KEY'))
    }

    config['sentry'] = {
        'DSN': str(getenv('SENTRY_DSN'))
    }

    config['s3'] = {
        'AWS_ACCESS_KEY_ID': str(getenv('AWS_ACCESS_KEY_ID')),
        'AWS_SECRET_ACCESS_KEY': str(getenv('AWS_SECRET_ACCESS_KEY')),
        'AWS_STORAGE_BUCKET_NAME': str(getenv('AWS_STORAGE_BUCKET_NAME')),
        'S3DIRECT_REGION': str(getenv('S3DIRECT_REGION'))
    }

    config['rmq'] = {
        'RMQ_USER': str(getenv('RMQ_USER')),
        'RMQ_PASSWORD': str(getenv('RMQ_PASSWORD')),
        'RMQ_URI': str(getenv('RMQ_URI'))
    }

    config['crossref'] = {
        'CROSSREF_TEST_USER': str(getenv('CROSSREF_TEST_USER')),
        'CROSSREF_TEST_PASS': str(getenv('CROSSREF_TEST_PASS'))
    }

    with open('../config.ini', 'w') as configfile:
        config.write(configfile)

    #exit(0)
