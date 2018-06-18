from generic.mount_point import GenericDataProvider


class TwitterProvider(GenericDataProvider):

    supported_origins = ['twitter']

    def load(self, string):
        pass

    def process(self, doi):
        return []
