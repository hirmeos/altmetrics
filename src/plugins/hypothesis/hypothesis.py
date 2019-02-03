import datetime
import json
import logging
import requests

from core.settings import Origins, StaticProviders
from generic.mount_point import GenericDataProvider
from models import Event, RawEvent


logger = logging.getLogger(__name__)


class HypothesisDataProvider(GenericDataProvider):
    """ Implements Crossref Cited-by API integration. """

    provider = StaticProviders.crossref_event_data
    supported_origins = [Origins.hypothesis]

    def process(self, uri, origin, scrape, last_check, test_data=None):
        """ Pull citation data from API and create Events.

        Args:
            uri (Uri): A Uri object from the ORM.
            test_data: TODO.

        Returns:
            list: Contains results.
        """

        api_url = 'https://hypothes.is/api/search'
        parameters = {
            'any': uri.raw,
            'order': 'asc',
        }
        if last_check:
            parameters.update(search_after=last_check.isoformat())
        
        request_content = json.loads(
            requests.get(api_url, params=parameters).content
        )
        results = request_content.get('rows')

        annotations = {}
        for result in results:

            subj = result.get('links', {}).get('html')
            if Event.query.filter_by(uri_id=uri.id, subject_id=subj).first():
                continue

            created_at = datetime.datetime.fromisoformat(
                result.get('created')
            ).date()

            event = Event(
                uri_id=uri.id,
                subject_id=subj,
                origin=origin,
                created_at=created_at
            )

            annotations[event] = [
                RawEvent(
                    event=event,
                    scrape_id=scrape.id,
                    external_id=result.get('id'),
                    origin=origin,
                    provider=self.provider,
                    created_at=created_at
                )
            ]

        return annotations
