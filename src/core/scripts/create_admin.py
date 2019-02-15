"""This logic will eventually be used to auto-create admin users, based on
environmental variables.
"""

import datetime
from getpass import getpass

from flask_security import SQLAlchemyUserDatastore

from core import db
from core.logic import get_or_create
from user.models import User, Role


# These need to be created
admin_role = get_or_create(Role, name='admin')
get_or_create(Role, name='awaiting-confirmation')
get_or_create(Role, name='user')


def get_password():
    for i in range(3):
        password = getpass('Enter password: ')
        confirm = getpass('Confirm password: ')
        if password == confirm:
            return password
        else:
            print('\nPasswords do not match\n')

    raise Exception('Unable to match passwords')


def create_admin():
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)

    parameters = (
        'username',
        'email',
        'first_name',
        'last_name',
        'institution',
    )

    user_details = {}
    for parameter in parameters:
        user_details[parameter] = input(f'{parameter}: ')

    user_details.update(
        password=get_password(),
        active=True,
        approved=True,
        confirmed_at=datetime.datetime.now()
    )

    admin_user = user_datastore.create_user(**user_details)
    admin_user.roles.append(admin_role)

    db.session.commit()

    print('New admin user successfully created.')
