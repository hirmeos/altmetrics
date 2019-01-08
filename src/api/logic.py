from core.settings import Origins


def get_origin_from_name(name):
    """ Get Origin (enum), based on string name of the origin."""
    for origin in Origins:
        if origin.name == name:
            return origin

