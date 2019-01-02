# -*- coding: utf-8 -*-
import os

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

from .admin import init_admin

db = SQLAlchemy()

CONFIG = os.getenv('CONFIG', 'DevConfig')


def create_app():
    app = Flask(__name__)
    app.config.from_object(f'core.settings.{CONFIG}')

    if app.config.get('SENTRY_DNS'):
        sentry_sdk.init(
            dsn=app.config.get('SENTRY_DNS'),
            integrations=[FlaskIntegration()]
        )

    db.init_app(app)
    Migrate(app, db)

    from api.views import bp as api_blueprint

    app.register_blueprint(api_blueprint)

    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

    init_admin(app, db)

    return app


if __name__ == "__main__":
    application = create_app()
    application.run()

# from __future__ import absolute_import, unicode_literals
#
# # This will make sure the app is always imported when
# # Django starts so that shared_task will use this app.
# from .celery import celery_app
#
# __all__ = ['celery_app']
