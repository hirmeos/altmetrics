from datetime import datetime
from logging import getLogger

from TwitterSearch import TwitterSearchOrder, TwitterSearchException

from flask import current_app

from core import redis_store
from core.celery import CeleryRetry
from generic.mount_point import GenericDataProvider
from processor.logic import set_generic_twitter_link
from processor.models import Event, RawEvent


logger = getLogger(__name__)


class TwitterProvider(GenericDataProvider):

    def instantiate_client(self):
        try:
            return self.client_class(
                consumer_key=current_app.config.get('TWITTER_APP_KEY'),
                consumer_secret=current_app.config.get(
                    'TWITTER_APP_KEY_SECRET'
                ),
                access_token=current_app.config.get('TWITTER_ACCESS_TOKEN'),
                access_token_secret=current_app.config.get(
                    'TWITTER_ACCESS_TOKEN_SECRET'
                ),
            )
        except RuntimeError:
            logger.error('App not found - skipping client instantiation.')
            return None

    def _validate(self, results):
        """ Make sure event passes validation.

        Args:
            results (Iterable): TwitterSearch result objects from the client.

        Returns:
            list: dicts of valid Twitter events.
        """
        valid, errors = self.validator.dump(results)

        if errors:
            logger.error(f'Twitter Validation Errors: {errors}')

        return valid

    @staticmethod
    def _to_python(event_entry):
        """Parse data from twitter API and convert them to Python types."""
        date_string = event_entry.pop('created_at_str')
        created_at = datetime.strptime(date_string, '%a %b %d %X %z %Y')

        twitter_id = event_entry.pop('twitter_id')
        subject_id = set_generic_twitter_link(twitter_id)

        return subject_id, created_at

    def _build(self, event_data, uri_id, origin):
        """Build Event objects using the defined schema.

        Args:
            event_data (list): Event dicts coming from the schema.
            uri_id (int): id or uri being queried.
            origin (Enum): Service which originated the event we are fetching.

        Returns:
            dict: new Event (key) and RawEvent (values) objects.
        """

        events = {}
        for event_entry in event_data:
            subj, created_at = self._to_python(event_entry)

            event = self.get_event(uri_id=uri_id, subject_id=subj)

            if not event:
                event = Event(
                    uri_id=uri_id,
                    subject_id=subj,
                    origin=origin.value,
                    created_at=created_at
                )

                events[event] = [
                    RawEvent(
                        event=event,
                        scrape_id=event_entry['scrape_id'],
                        origin=origin.value,
                        provider=self.provider.value,
                        created_at=created_at
                    )
                ]

        return events

    @staticmethod
    def assess_timeout(task):
        """Retry current task after a timeout if the Redis Twitter-Lock is set.

        Args:
            task (object): Celery task running this plugin.
        """

        twitter_lock = redis_store.get('Twitter-Lock')
        if not twitter_lock:
            return

        delta = datetime.fromtimestamp(int(twitter_lock)) - datetime.now()
        if delta.days:
            return

        timeout = delta.seconds + 1

        exception = CeleryRetry(
            TwitterSearchException(429, 'Twitter rate limit reached.'),
            'Twitter rate limit reached'
        )

        raise task.retry(exc=exception, countdown=timeout)

    def rate_limited_search(self, tw_search_order, task):
        """ Search Twitter, sleeping when rate limitations are reached.

        Args:
            tw_search_order (TwitterSearchOrder): Search parameters for Twitter.
            task (object): Celery task running this plugin.

        Returns:
            Iterable: Tweets matching search parameters.
        """
        try:
            return self.client.search_tweets_iterable(tw_search_order)

        except TwitterSearchException as e:
            if e.code != 429:
                raise e

            reset_value = int(self.client.get_metadata()['x-rate-limit-reset'])
            reset_datetime = datetime.fromtimestamp(reset_value)

            delta = reset_datetime - datetime.now()
            timeout = delta.seconds + 1

            logger.info(
                f'Twitter rate limit reached. Setting Twitter-Lock: '
                f'{timeout} seconds.'
            )
            redis_store.set('Twitter-Lock', reset_value, timeout)

            exception = CeleryRetry(e, 'Twitter rate limit reached')
            raise task.retry(exc=exception, countdown=timeout)

    def process(self, uri, origin, scrape, last_check, task):
        """ Implement processing of a URI to get Twitter events.

        Args:
            uri (Uri): An Uri object.
            origin (Enum): Service which originated the event we are fetching.
            scrape (Scrape): Scrape from ORM, not saved to database (yet).
            last_check (datetime): when this uri was last successfully scraped.
            task (object): Celery task running this plugin.

        Returns:
            dict: new Event objects.
        """

        self.assess_timeout(task)

        if not self.client:
            self.client = self.instantiate_client()

        self._add_validator_context(
            uri_id=uri.id,
            origin=origin.value,
            provider=self.provider.value,
            scrape_id=scrape.id
        )

        tw_search_order = TwitterSearchOrder()

        '''
        What needs to be done here would be along the lines of

        keywords = [f'"url:{url.url}"' for url in uri.urls] + [f'"{uri.raw}"']
        for keyword in keywords:
            # as a new task
            tw_search_order.set_keywords([keyword])
            # then run search and process results as currently done for the
            # 'just doi' search shown below.
        '''

        tw_search_order.set_keywords([f'"{uri.raw}"'])
        tw_search_order.set_include_entities(False)  # `True` for retweet info.

        if last_check:
            tw_search_order.set_since = last_check.date()

        results_generator = self.rate_limited_search(tw_search_order, task)

        event_data = self._validate(results_generator)

        events = self._build(
            event_data=event_data,
            uri_id=uri.id,
            origin=origin,
        )

        self.log_new_events(uri, origin, self.provider, events)
        return events
