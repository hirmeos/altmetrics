from flask_redis import FlaskRedis


class AutoPrefixFlaskRedis(FlaskRedis):
    """FlaskRedis client which automatically adds prefixes to the get, set and
    delete methods.
    """

    def __init__(self, prefix=None, *args, **kwargs):
        """Add a prefix to be used when caching values."""
        super().__init__(*args, **kwargs)
        self.prefix = prefix

    def init_app(self, app, **kwargs):
        self.prefix = kwargs.pop('prefix', None)
        super().init_app(app, **kwargs)

    def get_key_value(self, key):
        if self.prefix:
            key = f'_{self.prefix}_/{key}'
        return key

    def get(self, name):
        return self._redis_client.get(name=self.get_key_value(name))

    def set(self, name, value):
        return self._redis_client.set(
            name=self.get_key_value(name),
            value=value
        )

    def delete(self, *names):
        """map key prefix to all entries before executing delete command."""
        names = map(self.get_key_value, names)
        return self._redis_client.delete(*names)

    def __getitem__(self, name):
        return super().__getitem__(name=self.get_key_value(name))

    def __setitem__(self, name, value):
        return super().__setitem__(name=self.get_key_value(name), value=value)

    def __delitem__(self, name):
        return super().__delitem__(name=self.get_key_value(name))
