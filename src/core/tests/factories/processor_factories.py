import factory
import uuid

from django.utils import timezone

import processor.models.uri
import processor.models.uriupload
import processor.models.event
import processor.models.scrape
import processor.models.url
from .importer_factories import CSVUploadFactory
from processor import models


class DoiFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = processor.models.uri.Uri


class DoiUploadFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = processor.models.uriupload.UriUpload

    doi = factory.SubFactory(DoiFactory)
    upload = factory.SubFactory(CSVUploadFactory)


class ScrapeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = processor.models.scrape.Scrape
    end_date = timezone.now()


class EventFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = processor.models.event.Event

    scrape = factory.SubFactory(ScrapeFactory)
    external_id = uuid.uuid4()
    created_at = timezone.now()
    content = {'test_data': 'Lorem Ipsum'}


class UrlFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = processor.models.url.Url
