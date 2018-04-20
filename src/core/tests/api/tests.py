from django.contrib.auth.models import User
from django.test import TestCase

from rest_framework.test import APIClient


class APITestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username='test_api_user')
        self.user.set_password('test_api_pass')
        self.user.save()
        self.api_endpoints = ['dois', 'doiuploads', 'events', 'scrapes', 'urls']

    def test_unauthorised_user(self):
        """ Test every endpoint gives 403 response to unauthorised user. """

        for endpoint in self.api_endpoints:
            request = self.client.get('/api/{}/'.format(endpoint))
            self.assertEqual(request.status_code, 403)

    def test_authorised_user(self):
        """ Test every endpoint gives 200 response to authorised user. """

        self.client.login(
            username='test_api_user',
            password='test_api_pass'
        )
        for endpoint in self.api_endpoints:
            request = self.client.get('/api/{}'.format(endpoint), follow=True)
            self.assertEqual(request.status_code, 200)
