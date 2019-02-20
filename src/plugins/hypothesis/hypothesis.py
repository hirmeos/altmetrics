import datetime
import json
from logging import getLogger
import requests

from core.settings import Origins, StaticProviders
from generic.mount_point import GenericDataProvider
from processor.models import Event, RawEvent


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

        events = {}

        default_params = {
            'uri': uri.raw,
            'order': 'asc',
        }
        if last_check:
            default_params.update(search_after=last_check.isoformat())
        
        # 1) Process DOI
        self.query_h(uri, origin, scrape, event_dict, events, default_params)

        for url in uri.urls:  # 2) Process urls
            parameters = default_params.copy()
            parameters.update(uri=url.url)
            self.query_h(uri, origin, scrape, event_dict, events, parameters)

            del(parameters['uri'])
            parameters.update(wildcard_uri=f'{url.url}/?loc=*')
            self.query_h(uri, origin, scrape, event_dict, events, parameters)

        self.log_new_events(uri, origin, self.provider, events)
        return event_dict, events

    def query_h(self, uri, origin, scrape, event_dict, events, parameters):
        """ Query the h API, and update the current set of Hypothes.is
        events with the results.

        *h is web app for hypoths.is.
        """
        api_url = 'https://hypothes.is/api/search'
        request_content = json.loads(
            requests.get(api_url, params=parameters).content
        )
        results = request_content.get('rows')

        for result in results:
            subj = result.get('links', {}).get('html')

            if (
                    self.get_event(uri.id, subj, event_dict)
                    or not result.get('text')
            ):
                continue

            created_at = datetime.datetime.fromisoformat(
                result.get('created')
            ).date()

            event = Event(
                uri_id=uri.id,
                subject_id=subj,
                origin=origin.value,
                created_at=created_at
            )
            event_dict.update(subj=event)

            events[event] = [
                RawEvent(
                    event=event,
                    scrape_id=scrape.id,
                    external_id=result.get('id'),
                    origin=origin.value,
                    provider=self.provider.value,
                    created_at=created_at
                )
            ]
