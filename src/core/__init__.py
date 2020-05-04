# -*- coding: utf-8 -*-
import os

from celery import Celery
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

from flask_api import FlaskAPI
from flask_mail import Mail
from flask_migrate import Migrate
from flask_redis import FlaskRedis

from .celery import FlaskCelery
from .database import db
from .plugins import AltmetricsPlugins


CONFIG = os.getenv('CONFIG', 'DevConfig')
celery_app = FlaskCelery()
mail = Mail()
plugins = AltmetricsPlugins()
redis_store = FlaskRedis()


def create_app():
    app = FlaskAPI(__name__, template_folder='templates')
    app.config.from_object(f'core.settings.{CONFIG}')

    if app.config.get('SENTRY_DSN'):
        sentry_sdk.init(
            dsn=app.config.get('SENTRY_DSN'),
            release=app.config.get('METRICS_VERSION'),
            environment=os.getenv('SENTRY_ENV', 'production'),
            integrations=[FlaskIntegration()]
        )

    if CONFIG != 'TestConfig':
        celery_app.init_app(app, plugins)

    db.init_app(app)
    plugins.init_app(app)
    Migrate(app, db)

    mail.init_app(app)  # Set up mail.

    from .security import init_security
    init_security(app)

    from api.views import bp as api_blueprint
    from core.views import bp as core_blueprint
    from processor.tasks import pull_metrics, trigger_plugins  # noqa
    from processor.views import bp as processor_blueprint

    app.register_blueprint(api_blueprint)
    app.register_blueprint(core_blueprint)
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
