from flask_security.forms import (
    RegisterForm,
    Required,
    StringField,
)
from flask_security import Security, SQLAlchemyUserDatastore

from models import User, Role, db


class ExtendedRegisterForm(RegisterForm):
    username = StringField('Username', [Required()])


def init_security(app):
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    return Security(app, user_datastore, register_form=ExtendedRegisterForm)
