from flask import abort, g, request
from flask_login import current_user

from .tokens import validate_token, validate_account


def token_authenticated(f):
    """Checks whether a valid user JWT is sent with the request and, raises a
    401 error otherwise .
    """
    def decorator(*args, **kwargs):
        bearer_token = request.headers.get('Authorization')
        if not bearer_token:
            abort(401, {'message': request.headers})

        token = bearer_token.replace('Bearer ', '')
        is_valid, payload = validate_token(token)

        if not is_valid:
            abort(401, {'message': payload['error']})

        validate_account(payload)

        if not g.user:
            abort(401, {'message': 'Invalid user account.'})

        return f(*args, **kwargs)
    return decorator


def account_approved(f):
    """Checks whether user account has been approved, raises a 401 error
    otherwise .
    """
    def decorator(*args, **kwargs):
        if not current_user:
            abort(401, {'message': 'Invalid user account.'})
        elif not current_user.is_approved:
            abort(401, {'message': 'Account has not yet been approved.'})

        return f(*args, **kwargs)
    return decorator
