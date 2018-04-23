import factory
import uuid

from django.utils import timezone

from .importer_factories import CSVUploadFactory
from processor import models


class DoiFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Doi


class DoiUploadFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.DoiUpload

    doi = factory.SubFactory(DoiFactory)
    upload = factory.SubFactory(CSVUploadFactory)


class ScrapeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Scrape
    end_date = timezone.now()


class EventFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Event

    scrape = factory.SubFactory(ScrapeFactory)
    external_id = uuid.uuid4()
    created_at = timezone.now()
    content = {'test_data': 'Lorem Ipsum'}


class UrlFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Url
