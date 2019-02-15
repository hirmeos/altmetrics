import datetime
from itertools import chain
import logging
import requests

from bs4 import BeautifulSoup

from core.logic import get_credentials
from core.settings import Origins, StaticProviders
from generic.mount_point import GenericDataProvider
from processor.models import Event, RawEvent


logger = logging.getLogger(__name__)


class CrossrefCitedByDataProvider(GenericDataProvider):
    """ Implements Crossref Cited-by API integration. """

    provider = StaticProviders.crossref_cited_by
    supported_origins = [Origins.citation]

    def process(self, uri, origin, scrape, last_check, test_data=None):
        """ Pull citation data from API and create Events.

        Args:
            uri (Uri): A Uri object from the ORM.
            test_data: TODO.

        Returns:
            list: Contains results.
        """

        # For now just run for UP DOIs
        try:
            user, password = get_credentials(uri.raw)
        except ValueError:
            logger.warning(
                f'skipping doi "{uri.raw}" - no credentials available.'
            )
            return

        api_url = (
            'https://doi.crossref.org/servlet/getForwardLinks?'
            'usr={user}&pwd={password}&doi={doi}'
            '&startDate=1900-01-01&endDate={end_date}'
        ).format(
            user=user,
            password=password,
            doi=uri.raw,
            end_date=datetime.datetime.today().strftime('%Y-%m-%d')
        )  # may be worth last scrape for this uri to assign a start_date.

        request_content = requests.get(api_url).text

        xml_data = BeautifulSoup(request_content, 'xml')
        xml_journal_citations = xml_data.find_all('journal_cite')
        xml_book_citations = xml_data.find_all('book_cite')

        citations = {}
        for item in chain.from_iterable([
                xml_journal_citations,
                xml_book_citations
        ]):
            subj = item.find('doi').text
            if Event.query.filter_by(uri_id=uri.id, subject_id=subj).first():
                continue

            year = int(item.find('year').text)
            event = Event(
                uri_id=uri.id,
                subject_id=subj,
                origin=origin.value,
                created_at=datetime.date(year, 1, 1)
            )

            citations[event] = [
                RawEvent(
                    event=event,
                    scrape_id=scrape.id,
                    external_id=None,
                    origin=origin.value,
                    provider=self.provider.value,
                    created_at=datetime.date(year, 1, 1)
                )
            ]

        return citations
