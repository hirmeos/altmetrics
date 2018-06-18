from . import utils


class GenericDataProvider(object, metaclass=utils.MountPoint):
    """ Plugins can inherit this mount point to add a data provider. """

    def __init__(self, program):
        # Nothing is implemented here.
        pass

    def __str__(self):
        return self.__class__.__name__
