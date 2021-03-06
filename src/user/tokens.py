""" JSON web token authentication using PyJWT.

Largely based on the HIRMEOS token_api, to ensure consistency between the
Metrics Api and the Altmetrics API, allowing tokens to be shared by both.

This will be adapted as needed.
"""
from datetime import datetime, timedelta

import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from jwt.exceptions import DecodeError

from flask import current_app, g

from .models import User


def issue_token(user, lifespan=None):
    """ Create encoded JWT

    Args:
        user (User): User account requesting token
        lifespan (int): (optional) Seconds token should be valid for

    Returns:
        str: jwt token containing encrypted user data
    """

    authority = 'admin' if user.has_role('admin') else 'user'

    jwt_key = current_app.config.get('JWT_KEY')
    payload = {
        'sub': f'acct:{user.email}',
        'email': user.email,
        'name': user.full_name,
        'authority': authority,
    }

    if lifespan:
        issued_at = datetime.utcnow()
        expires_at = issued_at + timedelta(seconds=lifespan)
        payload.update(iat=issued_at, exp=expires_at)

    return jwt.encode(
        payload,
        jwt_key,
        algorithm='HS256'
    ).decode('utf-8')


def validate_token(token):
    """Checks JWT token to make sure it is valid.

    Args:
        token (str): JWT token

    Returns:
        tuple (bool, dict): whether or not token is valid and either the token
            payload or reason token is invalid
    """
    jwt_key = current_app.config.get('JWT_KEY')

    try:
        payload = jwt.decode(token, jwt_key, algorithms=['HS256'])
        return True, payload
    except (DecodeError, ExpiredSignatureError, InvalidTokenError) as e:
        return False, {'error': e}


def validate_account(token_payload):
    """ Set the user for the request based on the JWT. Returns a boolean
    value indicating whether or not the user has an Altmetrics account.

    Args:
        token_payload (dict): payload returned after JWT has been decoded

    Returns:
        bool: whether or not user has an account
    """
    email = token_payload.get('email')
    g.user = User.query.filter(User.email == email).first()

    return bool(g.user)
