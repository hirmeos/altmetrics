from flask import current_app

from generic.client import ApiClient


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
        values.update(mailto=current_app.config.get("TECH_EMAIL"))

        return values

    def get_doi(self, **parameters):
        """ Get results for a specific DOI.

        Args:
            doi (str): A text representing a DOI.
            origin (str): Service which originated the event we are fetching.

        Returns:
            dict: JSON containing CrossRef Event API information about the DOI.
        """
        filters = self._build_filters(parameters)
        return self.get(self.api_base, params=filters)

    def get_events(self, **parameters):
        """ Get list of CrossRef Event Data API events.

        Args:
            doi (str): A text representing a DOI.
            origin (str): Origin for the event to be searched (e.g. 'twitter').

        Returns:
            list: An iterable of event dictionaries.
        """
        response, status = self.get_doi(**parameters)

        result = self.decode(response)
        if status != 200:  # TODO: Check status and handle error if not 200
            return None, result

        return result.get('message', {}).get('events', []), None
