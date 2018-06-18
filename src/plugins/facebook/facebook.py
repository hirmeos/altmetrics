from generic.mount_point import GenericDataProvider


class FacebookProvider(GenericDataProvider):
    """ Implements a Scrapy-based interface to get FB data. """

    supported_origins = ['facebook']

    def load(self, string):
        pass

    def process(self, doi):
        return []
