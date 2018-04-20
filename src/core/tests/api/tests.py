from django.contrib.auth.models import User
from django.test import TestCase

from rest_framework.test import APIClient

from core.tests.factories import (
    generic_factories,
    importer_factories,
    processor_factories
)


class APITestCase(TestCase):
    """ Tests for the API module. """

    def setUp(self):
        """ Instantiate client, user and endpoints. """

        self.client = APIClient()
        self.user = generic_factories.UserFactory()
        self.user.set_password('test_pass')
        self.user.save()

        self.non_owner = generic_factories.UserFactory()
        self.non_owner.set_password('non_owner_pass')
        self.non_owner.save()

        self.doi = processor_factories.DoiFactory()
        self.csvupload = importer_factories.CSVUploadFactory(user=self.user)
        self.doiupload = processor_factories.DoiUploadFactory(
            upload=self.csvupload,
            doi=self.doi
        )

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
