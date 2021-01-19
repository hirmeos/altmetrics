from generic.mount_point import URITypes


class AltmetricsPlugins:
    """Keep track of plugins used by the altmetrics service."""

    def __init__(self, app=None):
        self.plugins_list = []
        self.plugins_dict = {}
        self.plugin_task_names = []
        self.plugins_by_type = {uri_type: [] for uri_type in URITypes}

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        for plugin in app.config.get('PLUGINS').values():
            self.plugins_list.append(plugin)
            self.plugins_dict[plugin.PROVIDER.provider] = plugin
            self.plugin_task_names.append(
                self.get_plugin_task_name(plugin.PROVIDER.provider.value)
            )
            self.plugins_by_type[plugin.PROVIDER.uri_type].append(
                plugin.PROVIDER.provider
            )

    def get_plugin(self, provider_enum):
        """Fetch plugin, based on its assigned provider enum value.

        Args:
            provider_enum (int): Enum value of provider.

        Returns:
            GenericDataProvider: Plugin associated with the provider.
        """
        return self.plugins_dict[provider_enum]

    def get_plugin_name(self, provider_enum):
        """Fetch plugin name, based on its assigned provider enum value.

        Args:
            provider_enum (int): Enum value of provider.

        Returns:
            str: Name of plugin associated with the provider.
        """
        return self.get_plugin(provider_enum).__name__

    def get_plugin_task_name(self, provider_enum):
        """Fetch the name of the task assigned to run a given plugin.

        Args:
            provider_enum (int): Enum value of provider.

        Returns:
            str: Name of the task assigned to run the plugin.
        """
        return f'process.{self.get_plugin_name(provider_enum)}'
