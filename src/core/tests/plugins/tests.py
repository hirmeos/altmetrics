from datetime import datetime, timedelta
import unittest
from unittest.mock import patch

from plugins.twitter.client import TwitterClient


class TwitterClientTestCase(unittest.TestCase):

    client = TwitterClient(
        app_key='test',
        app_key_secret='test',
        access_token='test',
        access_token_secret='test',
        label='test'
    )

    @patch('requests.get')
    def test_verify_credentials_makes_get_request(self, get_method):
        """ Test that the function makes a get request."""
        self.client.verify_credentials()
        get_method.assert_called()

    def test_twitter_date_format_returns_expected_output(self):
        """ Test that the function converts date to the correct format."""
        twitter_date = self.client.twitter_date_format(
            datetime(2000, 11, 11, 11, 11)
        )
        self.assertEqual(twitter_date, '200011111111')

    def test_get_end_date_returns_correct_date(self):
        """ Test that the function returns the correct date."""
        start_date = datetime(2000, 1, 1, 0, 0)
        expected_end_date = datetime(2000, 1, 31, 0, 0)
        end_date = self.client.calculate_end_date(start_date)
        self.assertEqual(end_date, expected_end_date)

    def test_get_end_date_does_does_not_go_beyond_now(self):
        """ Test that the function does not return an end date that is
        beyond the current datetime."""
        start_date = datetime.now()
        end_date = self.client.calculate_end_date(start_date)
        self.assertLess(end_date, datetime.now())

    def test_set_parameters(self):
        """ Test that the function returns a dictionary with the correct
        keys, and correct value for each key."""
        start_date = datetime(2000, 1, 1, 0, 0)
        doi = '10.1234/abc'
        parameters = self.client.set_parameters(doi, start_date)
        self.assertEqual(
            set(parameters.keys()),
            {'query', 'fromDate', 'toDate'},
            'unexpected or missing parameters'
        )
        self.assertEqual(
            parameters.get('query'),
            doi,
            'incorrect query value set.'
        )
        self.assertEqual(
            parameters.get('fromDate'),
            '200001010000',
            'incorrect value for fromDate.'
        )
        self.assertEqual(
            parameters.get('toDate'),
            '200001310000',
            'incorrect value for toDate.'
        )

    @patch('requests.get')
    def test_twitter_history_returns_correct_number_of_results(
            self,
            mock_requests
    ):
        """ Check that function queries Twitter over the correct number of
        intervals. This tests two different start dates. Up to 30 days ago,
        the function should only return one set of results. Beyond this, the
        function should return more than one result.
        """
        mock_requests.get.return_value = 1
        today = datetime.now()

        start_day_1 = today - timedelta(days=30)
        results = self.client.query_twitter_history('N/A', start_day_1)
        self.assertEqual(
            len(results),
            1,
            'Incorrect number of results returned'
        )

        start_day_2 = today - timedelta(days=31)
        results = self.client.query_twitter_history('N/A', start_day_2)
        self.assertEqual(
            len(results),
            2,
            'Incorrect number of results returned'
        )


