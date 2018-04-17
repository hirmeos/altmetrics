from datetime import datetime
from os import path

from django.test import TestCase
from django.utils import timezone

import requests

from providers.crossref_cited_by.crossref_cited_by import CrossrefCitedByDataProvider
from processor import models as processor_models



class CitedByProcessorTestCase(TestCase):
    def setUp(self):
        self.response_fixture = path.join(
            path.dirname(path.realpath(__file__)),
            'example_response.xml'
        )
        self.doi = processor_models.Doi.objects.create(doi='10.5334/bbc')
        self.scrape = processor_models.Scrape.objects.create(
            end_date=timezone.now()
        )

    def test_crossref_site_response(self):
        resp = requests.get('https://doi.crossref.org/')
        self.assertEqual(resp.status_code, 200)

    def test_process_returns_event_dict(self):
        cited_by_events = processor_models.Event.objects.filter(
            source='crossref_cited_by'
        )
        self.assertEqual(len(cited_by_events), 0)

        provider = CrossrefCitedByDataProvider('crossref_cited_by')
        process_result = provider.process(
            self.doi, test_data=self.response_fixture
        )[0]
        self.assertEqual(
            process_result.get('source_id'), '10.1177/1475725717748530'
        )
        self.assertEqual(process_result.get('source'), 'crossref_cited_by')
        self.assertEqual(
            type(process_result.get('created_at')),
            datetime
        )
        self.assertEqual(process_result.get('doi'), self.doi)
        self.assertEqual(
            process_result.get('content').get('journal_title'),
            'Psychology Learning  Teaching'
        )
