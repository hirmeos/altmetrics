import factory

from .importer_factories import CSVUploadFactory
from processor import models


class DoiFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Doi

    doi = '10.5334/bbc'


class DoiUploadFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.DoiUpload

    doi = factory.SubFactory(DoiFactory)
    upload = factory.SubFactory(CSVUploadFactory)
