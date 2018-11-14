from entity_fishing_client.client import ApiClient

from django.conf import settings


class CrossRefEventDataClient(ApiClient):
    """ Dedicated CrossRef Event Data API client. """

    api_base = 'https://api.eventdata.crossref.org/v1/events'

    def __init__(self):
        super().__init__(base_url=self.api_base)

    @staticmethod
    def _build_filters(values):
        """ Helper to create filters to be used when querying the API.

        Args:
            values (dict): List of filter and values to use as query parameters.

        Returns:
            dict: Ready to use value to be added to the parameters.
        """
        values.update({'mailto': settings.TECH_EMAIL})

        return values

    def get_doi(self, doi, origin):
        """ Get results for a specific DOI.

        Args:
            doi (str): A text representing a DOI.
            origin (str): Service which originated the event we are fetching.

        Returns:
            dict: JSON containing CrossRef Event API information about the DOI.
        """
        filters = self._build_filters({'obj-id': doi, 'source': origin})
        response, status = self.get(self.api_base, params=filters)

        result = self.decode(response), None
        if status != 200:  # TODO: Check status and handle error if not 200
            return None, result

        return result, None




    def get_events(self, doi, origin):
        """ Get list of CrossRef Event Data API events.

        Args:
            doi (str): A text representing a DOI.
            origin (str): Origin for the event to be searched (e.g. 'twitter').

        Returns:
            list: An iterable of event dictionaries.
        """
        return self.get_doi(doi, origin).get('message', {}).get('events', [])
