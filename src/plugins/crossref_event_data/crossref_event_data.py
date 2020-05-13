from datetime import date
from json import JSONDecodeError
from logging import getLogger
from requests.exceptions import ReadTimeout

from core.settings import Origins
from generic.mount_point import GenericDataProvider
from processor.logic import check_existing_entries, set_generic_twitter_link
from processor.models import Event, Error, RawEvent


logger = getLogger(__name__)


class CrossrefEventDataProvider(GenericDataProvider):
    """ Implements Crossref Event Data API integration. """

    def _validate(self, events):
        """ Make sure event passes validation.

        Args:
            events (list): Event objects coming from the client.

        Returns:
            generator: Yields valid deserialized event objects.
        """

        for event in events:
            event_data, errors = self.validator.dump(event)
            if errors:
                logger.error(f'Crossref Event Data Validation Errors: {errors}')
            else:
                yield event_data

    def _build(self, event_data, uri_id, origin):
        """ Build Event objects using the defined schema.

        Args:
            event_data (Iterable): list of Event dicts coming from the schema.
            uri_id (int): id or uri being queried.
            origin (Enum): Service which originated the event we are fetching.

        Returns:
            dict: new Event objects.
        """

        raw_events_dict = {}
        for entry in event_data:
            raw_events_dict.setdefault(entry['subject_id'], []).append(entry)

        events = {}
        for subj, event_list in raw_events_dict.items():
            if origin == Origins.twitter:
                subj = set_generic_twitter_link(subj)

            event = self.get_event(
                uri_id=uri_id,
                subject_id=subj,
            )

            if not event:
                min_date = min((
                    entry['created_at'] for entry in event_list
                ))
                event = Event(
                    uri_id=uri_id,
                    subject_id=subj,
                    origin=origin.value,
                    created_at=min_date
                )

            existing_raw_ids = check_existing_entries(
                RawEvent.external_id,
                [entry['external_id'] for entry in event_list]
            )
            events[event] = [
                RawEvent(
                    event=event,
                    scrape_id=entry['scrape_id'],
                    external_id=entry['external_id'],
                    origin=origin.value,
                    provider=self.provider.value,
                    created_at=entry['created_at']
                ) for entry in event_list
                if entry['external_id'] not in existing_raw_ids
            ]

            if events[event] and event.is_deleted:
                event.is_deleted = False

        return events

    def process(self, uri, origin, scrape, last_check, task):
        """ Implement processing of an URI to get events.

        Args:
            uri (Uri): An Uri object.
            origin (Enum): Service which originated the event we are fetching.
            scrape (Scrape): Scrape from ORM, not saved to database (yet).
            last_check (datetime): when this uri was last successfully scraped.
            task (object): Celery task running the current plugin.

        Returns:
            dict: new Event (key) and RawEvent (values) objects.
        """

        self._add_validator_context(  # Add context to Marshmallow validator
            uri_id=uri.id,
            origin=origin.value,
            provider=self.provider.value,
            scrape_id=scrape.id
        )

        parameters = {'obj-id': uri.raw, 'source': origin.name}
        if last_check:
            parameters.update(
                {'from-collected-date': last_check.date().isoformat()}
            )

        try:
            events, errors = self.client.get_events(**parameters)
        except (JSONDecodeError, ReadTimeout) as exception:
            raise task.retry(exc=exception, countdown=10)

        if errors:
            return {
                Error(
                    uri_id=uri.id,
                    scrape_id=scrape.id,
                    origin=origin.value,
                    provider=self.provider.value,
                    description=errors['message'][0]['message'][:100],
                    last_successful_scrape_at=last_check or date(1900, 1, 1)
                ): []
            }

        valid = self._validate(events)
        events = self._build(
            event_data=valid,
            uri_id=uri.id,
            origin=origin,
        )

        self.log_new_events(uri, origin, self.provider, events)
        return events
