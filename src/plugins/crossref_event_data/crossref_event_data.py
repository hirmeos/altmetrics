from datetime import date
from logging import getLogger

from core.settings import StaticProviders, Origins
from generic.mount_point import GenericDataProvider
from models import Event, Error, RawEvent
from processor.schemas import EventSchema

from .client import CrossRefEventDataClient

logger = getLogger(__name__)


class CrossrefEventDataProvider(GenericDataProvider):
    """ Implements Crossref Event Data API integration. """

    client = CrossRefEventDataClient()
    validator = EventSchema()
    provider = StaticProviders.crossref_event_data
    supported_origins = [
        Origins.twitter,
        Origins.wikipedia,
        Origins.hypothesis,
        Origins.wordpressdotcom,
    ]

    def _add_validator_context(self, **kwargs):
        self.validator.context = kwargs

    def _validate(self, events):
        """ Make sure event passes validation.

        Args:
            events (list): Event objects coming from the client.

        Returns:
            list: Contains valid objects.
        """
        return (self.validator.dump(event) for event in events)

    def _build(self, event_data, uri_id, origin, event_dict):
        """ Build a target Event object using the defined schema.

        Args:
            event_data (iter): list of Event dicts as coming from the client.
            uri_id (int): id or uri being queried
            origin (Enum): Service which originated the event we are fetching.
            event_dict: dict of events not yet committed to the db

        Returns:
            iter: iter of HIRMEOS metrics' ORM Events.
        """

        data = (data for data, errors in event_data if not errors)
        raw_events_dict = {}
        for entry in data:
            raw_events_dict.setdefault(entry['subject_id'], []).append(entry)

        events = {}
        for subj, event_list in raw_events_dict.items():
            event = self.get_event(
                uri_id=uri_id,
                subject_id=subj,
                event_dict=event_dict
            )

            if not event:
                min_date = min((
                    entry['created_at'] for entry in event_list
                ))
                event = Event(
                    uri_id=uri_id,
                    subject_id=subj,
                    origin=origin,
                    created_at=min_date
                )
                event_dict.update(subj=event)

            events[event] = [
                RawEvent(
                    event=event,
                    scrape_id=entry['scrape_id'],
                    external_id=entry['external_id'],
                    origin=entry['origin'],
                    provider=entry['provider'],
                    created_at=entry['created_at']
                ) for entry in event_list
            ]

        return event_dict, events

    def process(self, uri, origin, scrape, last_check, event_dict):
        """ Implement processing of an URI to get events.

        Args:
            uri (Uri): An Uri object.
            origin (Enum): Service which originated the event we are fetching.
            scrape (Scrape): Scrape from ORM, not saved to database (yet).
            last_check (datetime): when this uri was last successfully scraped.
            event_dict: dict of events not yet committed to the db in the form:
                {subj-id: event-object}

        Returns:
            generator: Contains events found for the given URI, as dictionaries.
        """

        self._add_validator_context(
            uri_id=uri.id,
            origin=origin,
            provider=self.provider,
            scrape_id=scrape.id
        )

        parameters = {'obj-id': uri.raw, 'source': origin.name}
        if last_check:
            parameters.update(
                {'from-collected-date': last_check.date().isoformat()}
            )
        events, errors = self.client.get_events(**parameters)

        if errors:
            return {
                Error(
                    uri_id=uri.id,
                    scrape_id=scrape.id,
                    origin=origin,
                    provider=self.provider,
                    description=errors['message'][0]['message'][:100],
                    last_successful_scrape_at=last_check or date(1900, 1, 1)
                ): []
            }

        valid = self._validate(events)
        event_dict, events = self._build(
            event_data=valid,
            uri_id=uri.id,
            origin=origin,
            event_dict=event_dict
        )

        self.log_new_events(uri, origin, self.provider, events)
        return event_dict, events
