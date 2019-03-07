from datetime import datetime, timedelta
import requests
from requests_oauthlib import OAuth1


class TwitterClient:

    """ Twitter client for searching tweets about DOIs.

    Please note, this uses the Premium Twitter search API. For more details
    visit https://developer.twitter.com/en/docs/tweets/search/api-reference
    /premium-search.html.
    """

    verify_url = 'https://api.twitter.com/1.1/account/verify_credentials.json'
    api_base = 'https://api.twitter.com/1.1/tweets/search'

    def __init__(
            self,
            app_key,
            app_key_secret,
            access_token,
            access_token_secret,
            label,
            api_base=None
    ):
        """ Instantiate the Twitter client.

        Args:
            app_key (str): key for your twitter app.
            app_key_secret (str): key secret for your twitter app.
            access_token (str): access token for your twitter app.
            access_token_secret (str): access token secret for your twitter app.
            label (str): label for your full-archive twitter dev environment.
        """

        self.app_key = app_key
        self.app_key_secret = app_key_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret

        self.api_base = api_base or self.api_base
        self.search_url = f'{self.api_base}/fullarchive/{label}.json'
        self.auth = self.set_authentication()

    def set_authentication(self):
        """ Set authentication credentials used for API calls."""
        return OAuth1(
            self.app_key,
            self.app_key_secret,
            self.access_token,
            self.access_token_secret
        )

    def verify_credentials(self):
        """ Test credentials to see if they are valid.

        Returns:
            Response: API response with your user account details or an error.
        """
        return requests.get(self.verify_url, auth=self.auth)

    @staticmethod
    def twitter_date_format(datetime_obj):
        """ Convert datetime object to a string, in twitter API format."""
        return datetime_obj.strftime('%Y%m%d%H%M')

    @staticmethod
    def calculate_end_date(start_datetime_obj, days=30):
        """ Add a specific number of days to a given a start datetime.

        Args:
            start_datetime_obj (datetime): datetime when query starts.
            days (int): number of days to add.

        Returns:
            datetime: datetime of end_date.
        """
        end_date = start_datetime_obj + timedelta(days=days)
        if end_date > datetime.now():
            end_date = datetime.now()

        return end_date

    def set_parameters(self, doi, start_datetime):
        """ Set parameters for querying a doi using the Twitter API.

        Args:
            doi (str): DOI of book/article to be queried.
            start_datetime: Start date of the query.

        Returns:
            dict: parameters to passed to the Twitter API.
        """
        return {
            'query': doi,
            'fromDate': self.twitter_date_format(start_datetime),
            'toDate': self.twitter_date_format(
                self.calculate_end_date(start_datetime)
            ),
        }

    def query_twitter_api(self, parameters):
        """  Query the Twitter API, searching for tweets that match the
        parameters given.

        Args:
            parameters (dict): Search parameters to use when querying Twitter.

        Returns:
            Response: response from the Twitter API.

        """
        return requests.get(
            self.search_url,
            params=parameters,
            auth=self.auth
        )

    def query_twitter_history(self, doi, start_datetime):
        """ Query the Twitter API over a period of time, in 30 days
        increments, starting from a given date up until the current date,
        searching for tweets that contain a given DOI.

        Args:
            doi (str): DOI to search for.
            start_datetime (datetime): starting day when tweets occur.

        Returns:
            list: List of responses from the Twitter API.

        """
        today = datetime.now()
        results = []
        while start_datetime.date() < today.date():
            parameters = self.set_parameters(doi, start_datetime)
            results.append(
                self.query_twitter_api(parameters)
            )
            start_datetime = self.calculate_end_date(start_datetime)

        return results
