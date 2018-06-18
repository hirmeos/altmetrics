import datetime
import uuid

from django.conf import settings
from django.utils import timezone

from bs4 import BeautifulSoup
import requests

from generic.mount_point import GenericDataProvider


class CrossrefCitedByDataProvider(GenericDataProvider):
    """ Implements Crossref Cited-by API integration. """

    supported_origins = ['citation']

    def process(self, uri, test_data=None):
        """ Pull citation data from API and create Event models.

        Args:
            uri (Uri): A Uri object from the ORM.
            test_data: TODO.

        Returns:
            list: Contains results.
        """

        api_url = (
            'http://doi.crossref.org/servlet/getForwardLinks?'
            'usr={user}&pwd={password}&doi={doi}'
            '&startDate=1900-01-01&endDate={end_date}'
        ).format(
            user=settings.CROSSREF_TEST_USER,
            password=settings.CROSSREF_TEST_PASSWORD,
            doi=uri.raw,
            end_date='{}-12-31'.format(datetime.datetime.now().year)
        )

        if test_data:
            request_content = open(test_data, 'r').read()
        else:
            request_content = requests.get(api_url).text

        xml_data = BeautifulSoup(request_content, 'xml')
        xml_journal_citations = xml_data.find_all('journal_cite')

        if xml_journal_citations:
            for item in xml_journal_citations:
                content = {
                    'journal_title': item.find('journal_title').text,
                    'article_title': item.find('article_title').text
                    if item.find('article_title') else '[Title not found]',
                    'volume': item.find('volume').text
                    if item.find('volume') else None,
                    'issue': item.find('issue').text
                    if item.find('issue') else None,
                    'year': item.find('year').text
                    if item.find('year') else None
                }

                return [{
                    'external_id': str(uuid.uuid4()), # No external ID supplied.
                    'source_id': item.find('doi').text,
                    'source': 'crossref_cited_by',
                    'created_at': timezone.now(),
                    'content': content,
                    'doi': uri
                }]

        return []
