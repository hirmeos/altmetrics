from flask_security.forms import (
    ConfirmRegisterForm,
    RegisterForm,
    PasswordField,
    Required,
    StringField,
)
from flask_security import Security, SQLAlchemyUserDatastore

from core import db
from user.models import User, Role


class ExtendedRegisterForm(RegisterForm):
    username = StringField('Username', [Required()])


class ExtendedConfirmRegisterForm(ConfirmRegisterForm):
    username = StringField('Username', [Required()])
    password_confirm = PasswordField()


def init_security(app):
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    return Security(
        app,
        user_datastore,
        register_form=ExtendedRegisterForm,
        confirm_register_form=ExtendedConfirmRegisterForm
    )
