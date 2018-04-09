from django.test import Client, TestCase


class CitedByProcessorTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_site_response(self):
        resp = self.client.get('https://doi.crossref.org/servlet/useragent')
        self.assertEqual(resp.status_code, 200)
