import ast

from django.test import TestCase

from rest_framework.test import APIClient

import processor.models.scrape
from core.tests.factories import (
    generic_factories,
    importer_factories,
    processor_factories
)
from processor import models as processor_models


class APITestCase(TestCase):
    """ Tests for the API module. """

    def setUp(self):
        """ Instantiate client, users, models and endpoints. """

        self.client = APIClient()
        self.user = generic_factories.UserFactory()
        self.user.set_password('test_pass')
        self.user.save()

        self.non_owner = generic_factories.UserFactory()
        self.non_owner.set_password('non_owner_pass')
        self.non_owner.save()

        self.doi = processor_factories.DoiFactory(doi='10.5334/bbc')
        self.url = processor_factories.UrlFactory(
            doi=self.doi,
            url='https://doi.org/{}'.format(self.doi)
        )
        self.csvupload = importer_factories.CSVUploadFactory(user=self.user)
        self.doiupload = processor_factories.DoiUploadFactory(
            upload=self.csvupload,
            doi=self.doi
        )
        self.event = processor_factories.EventFactory(doi=self.doi)

        self.api_endpoints = [
            'dois', 'doiuploads',
            'events', 'scrapes', 'urls'
        ]

    def login(self):
        """ Login helper function. """

        return self.client.login(
            username=self.user.username,
            password='test_pass'
        )

    def non_owner_login(self):
        """ Login helper function for non-owner user. """

        return self.client.login(
            username=self.non_owner.username,
            password='non_owner_pass'
        )

    def test_login(self):
        """ Test that user can log in with given credentials. """

        self.assertTrue(self.login())

    def test_authorised_user(self):
        """ Test every endpoint gives 200 response to authorised user. """

        self.login()
        for endpoint in self.api_endpoints:
            request = self.client.get('/api/{}/'.format(endpoint), follow=True)
            self.assertEqual(request.status_code, 200)

    def test_unauthorised_user(self):
        """ Test every endpoint gives 403 response to unauthorised user. """

        for endpoint in self.api_endpoints:
            request = self.client.get('/api/{}/'.format(endpoint))
            self.assertEqual(request.status_code, 403)

    def test_dois_display_for_owner(self):
        """ Test that API displays DOI for the DOI's owner.  """

        self.assertIn(self.user, self.doi.owners())
        self.login()

        response = self.client.get('/api/dois/')
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0].get('doi'), '10.5334/bbc')

    def test_dois_do_not_display_for_non_owner(self):
        """ Test that API does not display DOI for non-owner. """

        self.assertNotIn(self.non_owner, self.doi.owners())
        self.non_owner_login()

        response = self.client.get('/api/dois/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_doiuploads_display_for_owner(self):
        """ Test that DoiUpload displays for DoiUpload's owner. """

        self.assertEqual(self.user, self.doiupload.owner())
        self.login()

        response = self.client.get('/api/doiuploads/')
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['doi'].get('doi'), '10.5334/bbc')

    def test_doiuploads_do_not_display_for_non_owner(self):
        """ Test the DoiUpload does not display for non-owner. """

        self.assertNotEqual(self.non_owner, self.doiupload.owner())
        self.non_owner_login()

        response = self.client.get('/api/doiuploads/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_events_display_for_owner(self):
        """ Test that Events display for owner. """

        self.assertIn(self.user, self.event.owners())
        self.login()

        response = self.client.get('/api/events/')
        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            ast.literal_eval(response.data[0]['content']).get('test_data'),
            'Lorem Ipsum'
        )

    def test_events_do_not_display_for_non_owner(self):
        """ Test that Events do not display for non-owner. """

        self.assertNotIn(self.non_owner, self.event.owners())
        self.non_owner_login()

        response = self.client.get('/api/events/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_urls_display_for_owner(self):
        """ Test that URLs display for owner. """

        self.assertIn(self.user, self.url.owners())
        self.login()

        response = self.client.get('/api/urls/')
        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            response.data[0]['url'],
            'https://doi.org/{}'.format(self.doi)
        )
        self.assertEqual(response.data[0]['doi'].get('doi'), '10.5334/bbc')

    def test_scrape_display(self):
        """ Test that Scrapes display for authenticated users. """

        test_scrape = processor_factories.ScrapeFactory()
        number_of_scrapes = len(processor.models.scrape.Scrape.objects.all())
        self.login()

        response = self.client.get('/api/scrapes/')
        self.assertEqual(len(response.data), number_of_scrapes)
