import datetime
import json
from logging import getLogger
import requests

from core.settings import Origins, StaticProviders
from generic.mount_point import GenericDataProvider
from models import Event, Error, RawEvent


logger = getLogger(__name__)


class HypothesisDataProvider(GenericDataProvider):
    """ Implements Crossref Cited-by API integration. """

    provider = StaticProviders.crossref_event_data
    supported_origins = [Origins.hypothesis]

    def process(self, uri, origin, scrape, last_check, event_dict):
        """ Pull annotations from Hypothesis API, and create Events.

        Args:
            uri (Uri): An Uri object.
            origin (Enum): Service which originated the event we are fetching.
            scrape (Scrape): Scrape from ORM, not saved to database (yet).
            last_check (datetime): when this uri was last successfully scraped.
            event_dict: dict of events not yet committed to the db in the form:
                {subj-id: event-object}

        Returns:
            list: Contains results.
        """

        api_url = 'https://hypothes.is/api/search'
        parameters = {
            'uri': uri.raw,
            'order': 'asc',
        }
        if last_check:
            parameters.update(search_after=last_check.isoformat())
        
        request_content = json.loads(
            requests.get(api_url, params=parameters).content
        )
        results = request_content.get('rows')

        events = {}
        for result in results:
            subj = result.get('links', {}).get('html')
            if self.get_event(uri.id, subj, event_dict):
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
            event_dict.update(subj=event)

            events[event] = [
                RawEvent(
                    event=event,
                    scrape_id=scrape.id,
                    external_id=result.get('id'),
                    origin=origin,
                    provider=self.provider,
                    created_at=created_at
                )
            ]

        self.log_new_events(uri, origin, self.provider, events)
        return event_dict, events
