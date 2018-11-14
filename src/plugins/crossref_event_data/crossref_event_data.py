from generic.mount_point import GenericDataProvider

from processor.schemas import EventSchema

from .client import CrossRefEventDataClient
from .schema import CrossRefEventDataEventSchema


class CrossrefEventDataProvider(GenericDataProvider):
    """ Implements Crossref Event Data API integration. """

    client = CrossRefEventDataClient()
    validator = CrossRefEventDataEventSchema()
    target_schema = EventSchema()
    supported_origins = [
        'twitter',
        'wikipedia',
        'hypothesis',
        'wordpressdotcom'
    ]

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
            event_data (dict): Event as coming from the client.
            origin (str): Service which originated the event we are fetching.

        Returns:
            object: An HIRMEOS metrics' ORM Event.
        """
        return (data for data, errors in event_data if not errors)

    def process(self, uri, origin, scrape):
        """ Implement processing of an URI to get events.

        Args:
            uri (Uri): An Uri object.
            origin (str): Service which originated the event we are fetching.
            scrape (object): Scrape from ORM, not saved to database (yet).

        Returns:
            list: Contains events found for the given URI, as dictionaries.
        """

        events = self.client.get_events(doi=uri.raw, origin=origin)
        if events.errors:
            return None, {'Error stuff': 'Error stuff details'}
        valid = self._validate(events)
        events = [self._build(e, uri, origin, scrape) for e in valid]

        return events, None
