from logging import getLogger

import requests
from requests.exceptions import HTTPError

from flask import current_app


logger = getLogger(__name__)


class CrossRefEventDataClient:
    """ Dedicated CrossRef Event Data API client. """

    def __init__(self, api_base):
        self.api_base = api_base

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
            requests.Response: CrossRef Event Data events for the DOI.
        """
        filters = self._build_filters(parameters)
        return requests.get(self.api_base, params=filters, timeout=30)

    def get_events(self, **parameters):
        """ Get list of CrossRef Event Data API events.

        Args:
            doi (str): A text representing a DOI.
            origin (str): Origin for the event to be searched (e.g. 'twitter').

        Returns:
            list: An iterable of event dictionaries.
        """
        response = self.get_doi(**parameters)
        result = response.json()

        if response.status_code != 200:
            try:
                description = result['message'][0]['message']
                if (
                        response.status_code == 400 and
                        description == 'Invalid cursor supplied.'
                ):
                    raise HTTPError('Unexpected 400 Error')

            except (IndexError, TypeError) as e:
                if 'message' in result:  # need to retry
                    raise e

            return None, result, None

        message = result.get('message', {})
        events = message.get('events', [])
        next_cursor = message.get('next-cursor')

        return events, None, next_cursor
