# -*- coding: utf-8 -*-
from configparser import ConfigParser
import os

from celery import Celery
from .celery_config import init_celery
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

from flask_api import FlaskAPI
from flask_mail import Mail
from flask_migrate import Migrate
from flask_redis import FlaskRedis

from .database import db


CONFIG = os.getenv('CONFIG', 'DevConfig')
celery_app = Celery()
mail = Mail()
redis_store = FlaskRedis()


def create_app():
    app = FlaskAPI(__name__, template_folder='templates')
    app.config.from_object(f'core.settings.{CONFIG}')

    if app.config.get('SENTRY_DSN'):
        config_file = ConfigParser()
        config_file.read('sentry_version.ini')
        sentry_release = config_file.get('sentry', 'version', fallback='ERROR')

        sentry_sdk.init(
            dsn=app.config.get('SENTRY_DSN'),
            release=sentry_release,
            environment=os.getenv('SENTRY_ENV', 'production'),
            integrations=[FlaskIntegration()]
        )

    db.init_app(app)
    Migrate(app, db)

    # Set up mail
    mail.init_app(app)

    from .security import init_security
    init_security(app)

    from api.views import bp as api_blueprint
    from processor.views import bp as processor_blueprint

    app.register_blueprint(api_blueprint)
    app.register_blueprint(processor_blueprint)

    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

    from .admin import init_admin
    init_admin(app, db)

    init_celery(app, celery_app)

    redis_store.init_app(app)

    return app


if __name__ == "__main__":
    application = create_app()
    application.run()
