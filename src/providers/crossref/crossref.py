from generic.mount_point import GenericDataProvider

from .client import CrossRefClient


class CrossrefEventDataProvider(GenericDataProvider):
    """ Implements Crossref Event Data API integration. """

    supported_sources = ['twitter', 'wikipedia', 'hypothes.is']

    def process(self, doi):
        client = CrossRefClient()
        return client.get_doi(doi)
