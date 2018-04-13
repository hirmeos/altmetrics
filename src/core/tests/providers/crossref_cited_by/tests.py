from datetime import date
from os import path

from django.test import TestCase

import requests

from processor import models as processor_models
from providers.crossref_cited_by.crossref_cited_by import CrossrefCitedByDataProvider


class CitedByProcessorTestCase(TestCase):
    def setUp(self):
        self.response_fixture = path.join(
            path.dirname(path.realpath(__file__)),
            'example_response.json'
        )
        self.doi = processor_models.Doi.objects.create(doi='10.5334/bbc')
        self.scrape = processor_models.Scrape.objects.create(
            end_date=date.today()
        )

    def test_site_response(self):
        resp = requests.get('https://doi.crossref.org/')
        self.assertEqual(resp.status_code, 200)

    def test_events_created(self):
        cited_by_events = processor_models.Event.objects.filter(
            source='crossref_cited_by'
        )
        self.assertEqual(len(cited_by_events), 0)

        provider = CrossrefCitedByDataProvider(program='crossref_cited_by')
        provider.process(
            self.doi,
            '1900-01-01',
            '{}-12-31'.format(date.today().year)
        )

        self.assertEqual(len(cited_by_events), 1)
