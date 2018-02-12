from generic.mount_point import GenericDataProvider

from .client import CrossRefClient


class CrossrefEventDataProvider(GenericDataProvider):
    """ Implements Crossref Event Data API integration. """

    supported_sources = ['twitter', 'wikipedia', 'hypothes.is']

    def process(self, doi):
        """doi is the DOI model"""
        client = CrossRefClient()

        return [
            event
            for event in client.get_events(doi.doi)
            if event.get('source') in self.supported_sources
        ]
