from collections import defaultdict
from datetime import date
from json import JSONDecodeError
from logging import getLogger

from requests.exceptions import ReadTimeout, HTTPError

from core.celery import CeleryRetry
from core.settings import Origins
from generic.mount_point import GenericDataProvider
from processor.logic import check_existing_entries, set_generic_twitter_link
from processor.models import Event, Error, RawEvent, UriPrefix


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
            dumped_data, _ = self.validator.dump(event)
            event_data, errors = self.validator.load(dumped_data)
            if not errors:
                yield event_data
            # else:   # Results in a lot of logs.
            #     logger.error(f'Event Data Validation Errors: {errors}')

    def _pre_build(self, event_data):
        """Divide events by URI_id and Origin.

        Args:
            event_data (Iterable): list of Event dicts coming from the schema.

        Returns:
            dict: events, divided by URI_id and Origin.
        """
        organised_events = defaultdict(dict)

        for event in event_data:
            uri_id = event['uri_id']
            origin = event['origin']
            organised_events[uri_id].setdefault(origin, []).append(event)

        return organised_events

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
            )  # external_id is the UUID of the ED Event (from our Schema).

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

    def process(self, uri_prefix, scrape, last_check, task, cursor=None):
        """ Implement processing of an URI to get events.

        Args:
            uri_prefix (str): UriPrefix to check the Event Data API with.
            scrape (Scrape): Scrape from ORM, not saved to database (yet).
            last_check (datetime): when this uri was last successfully scraped.
            task (object): Celery task running the current plugin.
            cursor (str): from API response to fetch next set of results.

        Returns:
            dict: new Event (key) and RawEvent (values) objects.
        """

        self._add_validator_context(  # Add context to Marshmallow validator
            provider=self.provider.value,
            scrape_id=scrape.id
        )

        parameters = {'rows': '5000', 'obj-id.prefix': uri_prefix}

        if cursor:
            parameters.update(cursor=cursor)

        if last_check:
            parameters.update(
                {'from-collected-date': last_check.date().isoformat()}
            )

        try:
            events, errors, next_cursor = self.client.get_events(**parameters)

        except (JSONDecodeError, ReadTimeout) as e:
            exception = CeleryRetry(e, 'Request timeout/server overloaded')
            raise task.retry(exc=exception, countdown=10, max_retries=120)

        except HTTPError as e:
            exception = CeleryRetry(e, 'Request 400 error')
            raise task.retry(exc=exception, countdown=10, max_retries=120)

        except (IndexError, TypeError) as e:
            exception = CeleryRetry(e, 'Server 500 Error')
            raise task.retry(exc=exception, countdown=10, max_retries=120)

        if errors:
            description = errors['message'][0]['message'][:100]
            prefix_id = UriPrefix.query.filter_by(value=uri_prefix).first().id

            return {
                Error(
                    uri_prefix_id=prefix_id,
                    scrape_id=scrape.id,
                    provider=self.provider.value,
                    description=description,
                    last_successful_scrape_at=last_check or date(1900, 1, 1)
                ): []
            }, None

        valid = self._validate(events)
        event_data = self._pre_build(valid)

        events = {}
        for uri_id, per_origin_data in event_data.items():
            for origin, valid_events in per_origin_data.items():
                events.update(
                    self._build(
                        event_data=valid_events,
                        uri_id=uri_id,
                        origin=origin
                    )
                )

        if events:
            logger.info(
                f'{self.provider.name}: Retrieved {len(events)} new events '
                f'for URI Prefix: {uri_prefix}'
            )

        return events, next_cursor
