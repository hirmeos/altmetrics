""" Python client for making API requests to the Altmetrics service.

This will be used to fetch a JWT token using user login information, as well
as use this token to make further API requests.

This will be developed alongside the Altmetrics API to help use this service.

TODO: This should eventually live outside of the Altmetrics service as a
TODO:   separate installable Python package.
"""

import requests  # I can't seem to get flask to work with regular post data
from requests.auth import HTTPBasicAuth


def utf8(bytes_value):
    return bytes_value.decode('utf-8')


class AltmetricsClient(object):

    API_BASE = 'https://altmetrics.ubiquity.press/api'

    def __init__(self, email, password, api_base=API_BASE):
        """Set the base_url and user credentials for the client.

        Args:
            email (str): email for user login on the altmetrics system
            password (str): password for user login on the altmetrics system
            api_base (str): url for the altmetrics API
        """
        self.base_url = api_base
        self.email = email
        self.password = password
        self.api_base = api_base.rstrip('/')
        self.token = None
        self.header = None

        # ## get token and set header
        self.get_token()
        self.set_header()

        # ## URLs used by this client can be set here
        self.doi_url = f'{self.api_base}/uriset'
        self.event_url = f'{self.api_base}/eventset'

    def get_token(self):
        """Makes a request to the altmetrics API to get a JWT token."""
        if self.token:
            return

        token_url = f'{self.api_base}/get_token'
        response = requests.get(
            token_url,
            auth=HTTPBasicAuth(self.email, self.password)
        )

        if response.status_code == 200:
            self.token = utf8(response.content)
        else:
            raise ValueError(response.content)

    def set_header(self):
            self.header = {'Authorization': f'Bearer {self.token}'}

    def register_dois(self, doi_list):
        """Post dois to the Altmetrics API.

        Args:
            doi_list (list): list of dicts containing dois to be sent

        Returns:
            object: Response returned by API
        """
        response = requests.post(
            self.doi_url,
            json=doi_list,
            headers=self.header
        )

        return response

    def query_dois(self):
        """Check all DOIs associated with user's account. """
        response = requests.get(self.doi_url, headers=self.header)

        return utf8(response.content)
