# -*- coding: utf-8 -*-
import os
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

from flask import Flask
from flask_api import FlaskAPI
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from .admin import init_admin


db = SQLAlchemy()

CONFIG = os.getenv('CONFIG', 'DevConfig')


def create_app():
    # app = Flask(__name__)
    app = FlaskAPI(__name__, template_folder='templates')
    app.config.from_object(f'core.settings.{CONFIG}')

    if app.config.get('SENTRY_DNS'):
        sentry_sdk.init(
            dsn=app.config.get('SENTRY_DNS'),
            integrations=[FlaskIntegration()]
        )

    db.init_app(app)
    Migrate(app, db)

    from .security import init_security
    security = init_security(app)

    from api.views import bp as api_blueprint
    from processor.views import bp as processor_blueprint

    app.register_blueprint(api_blueprint)
    app.register_blueprint(processor_blueprint)

    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

    init_admin(app, db)

    return app


if __name__ == "__main__":
    application = create_app()
    application.run()
