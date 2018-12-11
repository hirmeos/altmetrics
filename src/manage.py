from flask_migrate import Migrate

from models import app, db

migrate = Migrate(app, db)
