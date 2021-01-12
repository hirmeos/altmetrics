from core import db
from core.logic import get_enum_by_name
from core.settings import Origins


def get_origin_from_name(name):
    """ Get Origin (enum), based on string name of the origin."""
    return get_enum_by_name(Origins, name)


def queryset_exists(queryset):
    """ Check if queryset exists in the database. Shorthand function to
    neaten up the code a bit.

    Args:
        queryset (flask_sqlalchemy.BaseQuery): result of running a filter

    Returns:
        bool: True if query exists otherwise False

    """
    return db.session.query(queryset.exists()).scalar()


def get_uri_prefix(uri):
    """Currently gets the prefix of DOIs only.

    Args:
        uri (str): URI to process.

    Returns:
        str: uri prefix if URI is a DOI else None.
    """
    if '/' in uri:
        return uri[:uri.index('/')]
