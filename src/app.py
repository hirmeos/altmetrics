# -*- coding: utf-8 -*-
import os

from flask import Flask
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

CONFIG = os.getenv('CONFIG', 'DevConfig')

sentry_sdk.init(
    dsn=os.getenv(
        'SENTRY_DSN',
        'https://al56vly687152-987896oe3re8a7ooy3@sentry.project.com/99'
    ),
    integrations=[FlaskIntegration()]
)

app = Flask(__name__)
app.config.from_object(f'core.settings.{CONFIG}')
