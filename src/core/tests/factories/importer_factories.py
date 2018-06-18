import factory

from importer import models


class CSVUploadFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.CSVUpload

    file_name = '6f8b4b88bb9b4b7f9325b334ad2e946f-import_example.csv'
    link = ('https://s3-eu-west-1.amazonaws.com/metrics-uploads/'
           '6f8b4b88bb9b4b7f9325b334ad2e946f-import_example.csv')
