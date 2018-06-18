import imp
import logging
import os
import sys

logger = logging.getLogger('plugins')


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


def load_origins(plugins):
    """ Create and index of all plugins providing a single source.

    Args:
        plugins (dict): Contains available plugins: name and module.

    Returns:
        dict: Contains available sources: name and relevant module.
    """
    available_origins = {}

    for name, module in plugins.items():
        for origin in module.PROVIDER.supported_origins:
            if not available_origins.get(origin):
                available_origins.update({origin: [module]})
            else:
                available_origins[origin].append(module)

    return available_origins


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

    if not names:
        names = list_plugins(folder)

    loaded_plugins = {}

    for addon in names:

        if addon in ignored_plugins:
            logging.info(
                "Plugin {addon}s not loaded because it is disabled".format(
                    addon=addon
                ))
            continue

        if addon in loaded_plugins:
            logging.info(
                "Plugin {addon}s not reloaded because "
                "it has already been loaded".format(addon=addon)
            )
            continue

        try:
            file = None
            file, path, description = imp.find_module(addon, ['plugins'])
            module = imp.load_module(addon, file, path, description)
            loaded_plugins[addon] = module
            logging.info(
                "Plugin {} v{} by {} loaded".format(
                    addon,
                    module.__version__,
                    module.__author__
                )
            )
        except:
            if file:
                file.close()

            logging.info(sys.exc_info()[1])

    return loaded_plugins, load_origins(loaded_plugins)
