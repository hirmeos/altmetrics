import datetime
import json
from logging import getLogger
import requests

from generic.mount_point import GenericDataProvider
from processor.models import Event, RawEvent


logger = getLogger(__name__)


class HypothesisDataProvider(GenericDataProvider):
    """ Implements Hypothes.is API integration. """

    def process(self, uri, origin, scrape, last_check, task):
        """ Pull annotations from Hypothesis API, and create Events. Note:
        this uses the wildcard_uri search option, which is subject to change;
        see https://h.readthedocs.io/en/latest/api-reference/#operation/search.

        Args:
            uri (Uri): An Uri object.
            origin (Enum): Service which originated the event we are fetching.
            scrape (Scrape): Scrape from ORM, not saved to database (yet).
            last_check (datetime): when this uri was last successfully scraped.
            task (object): Celery task running the current plugin.

        Returns:
            dict: new Event (key) and RawEvent (values) objects.
        """

        parameters = {
            'uri': [uri.raw],
            'order': 'asc',
        }
        events = {}

        if last_check:
            parameters.update(search_after=last_check.isoformat())

        if uri.urls:
            parameters.update(wildcard_uri=[])
        
        for url in uri.urls:  # 2) Process urls
            parameters['uri'].append(url.url)
            parameters['wildcard_uri'].append(f'{url.url}/?loc=*')

        response = requests.get(self.api_base, params=parameters)

        if not response.content:
            logger.error(
                f'Unexpected: No response from request using request '
                f'parameters: {parameters}. Reason: {response.reason}.'
            )
            results = []
        else:
            response_content = json.loads(response.content)
            results = response_content.get('rows')

        for result in results:
            subj = result.get('links', {}).get('html')

            if self.get_event(uri.id, subj) or not result.get('text'):
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

        self.log_new_events(uri, origin, self.provider, events)
        return events
