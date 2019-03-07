from collections.abc import Iterable
from datetime import datetime
from logging import getLogger
from itertools import chain

from flask import current_app

from generic.mount_point import GenericDataProvider
from processor.logic import get_doi_deposit_date, set_generic_twitter_link
from processor.models import Event, RawEvent


logger = getLogger(__name__)


class TwitterProvider(GenericDataProvider):

    def instantiate_client(self):
        try:
            return self.client_class(
                app_key=current_app.config.get('TWITTER_APP_KEY'),
                app_key_secret=current_app.config.get('TWITTER_APP_KEY_SECRET'),
                access_token=current_app.config.get('TWITTER_ACCESS_TOKEN'),
                access_token_secret=current_app.config.get(
                    'TWITTER_ACCESS_TOKEN_SECRET'
                ),
                label=current_app.config.get('TWITTER_LABEL'),
                api_base=self.api_base
            )
        except RuntimeError:
            logger.error('App not found - skipping client instantiation')
            return None

    def _validate(self, results):
        schema = self.client(many=True)
        iter_results = chain.from_iterable(results)

        return schema.dumps(iter_results)

    @staticmethod
    def _convert_to_python(event_entry):
        """ Parse data from twitter API and convert them to Python types."""
        date_string = event_entry.pop('created_at_str')
        created_at = datetime.strptime(date_string, format='%a %b %d %X %z %Y')

        twitter_id = event_entry.pop('twitter_id')
        subject_id = set_generic_twitter_link(twitter_id)

        return subject_id, created_at

    def _build(self, event_data, uri_id, origin, event_dict):
        """ Build a Event objects using the defined schema.

        Args:
            event_data (Iterable): list of Event dicts coming from the schema.
            uri_id (int): id or uri being queried
            origin (Enum): Service which originated the event we are fetching.
            event_dict: dict of events not yet committed to the db

        Returns:
            tuple: The input event_dict and an Iterable of Event objects
        """

        events = {}
        for event_entry in event_data:
            subj, created_at = self._convert_to_python(event_entry)

            event = self.get_event(
                uri_id=uri_id,
                subject_id=subj,
                event_dict=event_dict
            )

            if not event:
                event = Event(
                    uri_id=uri_id,
                    subject_id=subj,
                    origin=origin.value,
                    created_at=created_at
                )
                event_dict[subj] = event

                events[event] = [
                    RawEvent(
                        event=event,
                        scrape_id=event_entry['scrape_id'],
                        origin=origin.value,
                        provider=self.provider.value,
                        created_at=created_at
                    )
                ]

        return event_dict, events

    def process(self, uri, origin, scrape, last_check, event_dict):
        """ Implement processing of an URI to get Twitter events.

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
            origin=origin.value,
            provider=self.provider.value,
            scrape_id=scrape.id
        )

        start_datetime = last_check or get_doi_deposit_date(
            uri.raw,
            datetime(2006, 3, 22)
        )
        results = self.client.query_twitter_history(
            doi=uri.raw,
            start_datetime=start_datetime
        )

        valid, errors = self._validate(results)
        event_dict, events = self._build(
            event_data=valid,
            uri_id=uri.id,
            origin=origin,
            event_dict=event_dict
        )

        self.log_new_events(uri, origin, self.provider, events)
        return event_dict, events
