# from flask_security.forms import (
#     RegisterForm,
#     Required,
#     StringField,
# )
from flask_security import Security, SQLAlchemyUserDatastore

from models import User, Role, db


def init_security(app):
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    return Security(app, user_datastore)
