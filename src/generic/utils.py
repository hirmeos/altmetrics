import imp
import os
import sys


class MountPoint(type):

    def __init__(cls, name, bases, attrs):
        if not hasattr(cls, 'plugins'):
            cls.plugins = []
        
        cls.plugins.append(cls)


class ExtensionsAt(object):
    """ Descriptor to get plugins on a given mount point. """

    def __init__(self, mount_point):
        """ Initialize the descriptor with the mount point wanted. """
        self.mount = mount_point

    def __get__(self, instance, owner=None):
        """ Returns all plugins on this mount point. """
        # Plugin are instantiated with the object that is calling them.
        return [p(instance) for p in self.mount.plugins]


def list_plugins(folder):
    """ Utility method to list available plugins. """
    return os.listdir(folder)


def load_plugins(folder, **kwargs):
    """ Utility method to load plugins. """
    ignored_plugins = ()
    names = None

    for key in kwargs:
        if key == 'ignore':
            ignored_plugins = kwargs[key]
        elif key == 'names':
            names = kwargs[key]
        elif key == 'name':
            names = (kwargs[key],)

    if names is None:
        names = list_plugins(folder)

    loaded_plugins = {}

    for addon in names:
        if addon in ignored_plugins:
            print("Plugin {addon}s not loaded because it is disabled".format(
                addon=addon
            ))
            continue
        if addon in loaded_plugins:
            print(
                "Plugin {addon}s not reloaded because it has already been "
                "loaded".format(addon=addon)
            )
            continue
        try:
            file = None  # Defines variable for catch clause.
            file, path, description = imp.find_module(addon, ['providers'])
            module = imp.load_module(addon, file, path, description)
            print(
                "Plugin {} v{} by {} loaded".format(
                    addon,
                    module.__version__,
                    module.__author__
                )
            )
            loaded_plugins[addon] = module
        except:
            if file:
                file.close()
            print(sys.exc_info()[1])

    return loaded_plugins
