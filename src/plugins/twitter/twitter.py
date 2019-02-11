from generic.mount_point import GenericDataProvider
from processor.models import Origins


class TwitterProvider(GenericDataProvider):

    supported_origins = [Origins.twitter]

    def load(self, string):
        pass

    def process(self, doi):
        return []
