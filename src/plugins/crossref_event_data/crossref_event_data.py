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
        return [event for event in events if self.validator.load(event)]

    def _build(self, event_data, uri, origin, scrape, measure):
        """ Build a target Event object using the defined schema.

        Args:
            event_data (dict): Event as coming from the client.
            origin (str): Service which originated the event we are fetching.

        Returns:
            object: An HIRMEOS metrics' ORM Event.
        """
        self.target_schema.context['origin'] = origin
        event = self.target_schema.dump(event_data).data

        event.scrape = scrape
        event.measure = measure
        event.uploader = uri.owner

        return event

    def process(self, uri, origin, scrape, measure):
        """ Implement processing of an URI to get events.

        Args:
            uri (Uri): An Uri object.
            origin (str): Service which originated the event we are fetching.
            scrape (object): Scrape from ORM, not saved to database (yet).
            measure (object): Measure from ORM.

        Returns:
            list: Contains events found for the given URI, as dictionaries.
        """

        events = self.client.get_events(doi=uri.raw, origin=origin)
        valid = self._validate(events)
        events = [self._build(e, uri, origin, scrape, measure) for e in valid]

        return events
