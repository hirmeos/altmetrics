from urllib.parse import urljoin

from nerd_client.client import ApiClient


class CrossRefEventDataClient(ApiClient):
    """ Dedicated CrossRef Event Data API client. """

    api_base = "https://query.eventdata.crossref.org"
    events_service = urljoin(api_base, "events")

    def __init__(self):
        super(CrossRefEventDataClient, self).__init__(base_url=self.api_base)

    @staticmethod
    def _build_filters(values):
        """ Helper to create filters to be used when querying the API.

        Args:
            values (list): List of values to use in the parameters.

        Returns:
            str: Ready to use value to be added to the parameters.
        """
        return {'filter': '{}:{}'.format(*values)}

    def get_doi(self, doi):
        """ Get results for a specific DOI.

        Args:
            doi (str): A text representing a DOI.

        Returns:
            str: JSON containing CrossRef Event API information about the DOI.
        """
        filters = self._build_filters(['obj-id', doi])
        response, _ = self.get(self.events_service, params=filters)

        return self.decode(response)

    def get_events(self, doi):
        """ Get list of CrossRef Event Data API events.

        Args:
            doi (str): A text representing a DOI.

        Returns:
            object: A Python iterable of events.
        """
        return [
            Event.from_message_event(doi, event).to_map() for event
            in self.get_doi(doi).get('message', {}).get('events', [])
        ]


class Event(object):

    external_id = None
    source_id = None
    source = None
    created_at = None
    content = None
    doi = None

    @classmethod
    def from_message_event(cls, doi, event):
        instance = cls()
        instance.external_id = event.get('id')
        instance.source_id = event.get('subj_id')
        instance.source = event.get('source_id')
        instance.created_at = event.get('timestamp')
        instance.content = event.get('subj', {}).get('api-url')
        instance.doi = doi

        return instance

    def to_map(self):
        return {
            'external_id': self.external_id,
            'source_id': self.source_id,
            'source': self.source,
            'created_at': self.created_at,
            'content': self.content,
            'doi': self.doi
        }
