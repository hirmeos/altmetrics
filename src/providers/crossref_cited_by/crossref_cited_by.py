from bs4 import BeautifulSoup
import datetime
import requests
import uuid

from django.conf import settings

from generic.mount_point import GenericDataProvider
from processor.models import Event


class CrossrefCitedByDataProvider(GenericDataProvider):
    """ Implements Crossref Cited-by API integration. """

    def process(self, doi, start_date, end_date):
        """ Pull citation data from API and create Event models. """

        api_url = (
            'http://doi.crossref.org/servlet/getForwardLinks?'
            'usr={user}&pwd={password}&doi={doi}'
            '&startDate={start_date}&endDate={end_date}'
        ).format(
            user=settings.CROSSREF_TEST_USER,
            password=settings.CROSSREF_TEST_PASSWORD,
            doi=doi,
            start_date=start_date,
            end_date=end_date
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
                event_dict = {
                    'external_id': str(uuid.uuid4()),
                    'source_id': item.find('doi').text,
                    'source': 'crossref_cited_by',
                    'created_at': datetime.datetime.now(),
                    'content': content,
                    'doi': doi
                }
                new_event = Event(**event_dict)


        else:
            return 'No citations available'
