from core import db
from core.settings import Origins


def get_origin_from_name(name):
    """ Get Origin (enum), based on string name of the origin."""
    for origin in Origins:
        if origin.name == name:
            return origin


def queryset_exists(queryset):
    """ Check if queryset exists in the database. Shorthand function to
    neaten up the code a bit.

    Args:
        queryset (flask_sqlalchemy.BaseQuery): result of running a filter

    Returns:
        bool: True if query exists otherwise False

    """
    return db.session.query(queryset.exists()).scalar()
