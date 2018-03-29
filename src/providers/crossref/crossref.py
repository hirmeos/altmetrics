from bs4 import BeautifulSoup
import requests

from django.conf import settings

from .client import CrossRefClient
from generic.mount_point import GenericDataProvider


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


class CrossrefCitedByDataProvider(GenericDataProvider):

    def __init__(self):
        self.api_base = (
            'http://doi.crossref.org/servlet/getForwardLinks?'
            'usr={user}&pwd={password}&doi={doi}'
            '&startDate={start_date}&endDate={end_date}'
        )

    def process(self, doi, start_date, end_date):
        api_url = self.api_base.format(
            user=settings.CROSSREF_TEST_USER
        )
        api_request = requests.get(api_url)
        soup = BeautifulSoup(api_request.text, 'xml')


    def is_authorised(self, users, **kwargs):
        # Check if user is member of publisher that has permission
        # to access citation data for given DOI.
        pass

