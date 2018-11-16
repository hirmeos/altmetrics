from generic.mount_point import GenericDataProvider

from models import Event, Error

from .client import CrossRefEventDataClient
from processor.schemas import EventSchema


from core.settings import StaticProviders, Origins


class CrossrefEventDataProvider(GenericDataProvider):
    """ Implements Crossref Event Data API integration. """

    client = CrossRefEventDataClient()
    validator = EventSchema()
    provider = StaticProviders.crossref_event_data
    supported_origins = [
        Origins.twitter,
        Origins.wikipedia,
        Origins.hypothesis,
        Origins.wordpress,
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

    def _build(self, event_data):
        """ Build a target Event object using the defined schema.

        Args:
            event_data (iter): list of Event dicts as coming from the client.

        Returns:
            iter: iter of HIRMEOS metrics' ORM Events.
        """
        return (Event(**data) for data, errors in event_data if not errors)

    def process(self, uri, origin, scrape, last_check):
        """ Implement processing of an URI to get events.

        Args:
            uri (Uri): An Uri object.
            origin (Enum): Service which originated the event we are fetching.
            scrape (Scrape): Scrape from ORM, not saved to database (yet).
            last_check (datetime): when this uri was last successfully scraped.

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
        if uri.last_checked:
            parameters.update()

        events, errors = self.client.get_events(**parameters)

        if errors:
            return [
                Error(
                    uri_id=uri.id,
                    scrape_id=scrape.id,
                    origin=origin,
                    provider=self.provider,
                    description=errors,
                    last_successful_scrape_at=last_check
                )
            ]

        valid = self._validate(events)
        events = self._build(valid)

        return events
