from bs4 import BeautifulSoup
import datetime
import requests
import uuid

from django.conf import settings
from django.utils import timezone

from generic.mount_point import GenericDataProvider


class CrossrefCitedByDataProvider(GenericDataProvider):
    """ Implements Crossref Cited-by API integration. """

    def process(self, doi):
        """ Pull citation data from API and create Event models. """

        api_url = (
            'http://doi.crossref.org/servlet/getForwardLinks?'
            'usr={user}&pwd={password}&doi={doi}'
            '&startDate=1900-01-01&endDate={end_date}'
        ).format(
            user=settings.CROSSREF_TEST_USER,
            password=settings.CROSSREF_TEST_PASSWORD,
            doi=doi.doi,
            end_date='{}-12-31'.format(datetime.datetime.now().year)
        )
        api_request = requests.get(api_url)
        xml_data = BeautifulSoup(api_request.text, 'xml')
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
                    'external_id': str(uuid.uuid4()),
                    'source_id': item.find('doi').text,
                    'source': 'crossref_cited_by',
                    'created_at': timezone.now(),
                    'content': content,
                    'doi': doi
                }]

        else:
            return []
