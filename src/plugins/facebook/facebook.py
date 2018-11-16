from generic.mount_point import GenericDataProvider
from models import Origins


class FacebookProvider(GenericDataProvider):
    """ Implements a Scrapy-based interface to get FB data. """

    supported_origins = [Origins.facebook]

    def load(self, string):
        pass

    def process(self, doi):
        return []
