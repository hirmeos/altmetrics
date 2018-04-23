from django.core.validators import RegexValidator
from django.db import models


class Doi(models.Model):

    doi = models.CharField(
        max_length=50,
        unique=True,
        validators=[
            RegexValidator(
                regex='/^10.\d{4,9}/[-._;()/:A-Z0-9]+$/i',
                message='DOI not valid.',
            ),
        ],
    )
    last_checked = models.DateTimeField(
        null=True,
        default=None,
    )

    def __str__(self):
        return self.doi

    def owners(self):
        return [
            doi_upload.owner() for doi_upload in self.doiupload_set.all()
        ]


class Url(models.Model):

    url = models.URLField()
    doi = models.ForeignKey(
        Doi,
        on_delete=models.PROTECT,
    )

    def __str__(self):
        return self.url

    def owners(self):
        return self.doi.owners()


class DoiUpload(models.Model):

    doi = models.ForeignKey(
        Doi,
        null=False,
        on_delete=models.PROTECT
    )
    upload = models.ForeignKey(
        'importer.CSVUpload',
        null=False,
        on_delete=models.PROTECT
    )

    def __str__(self):
        return 'DoiUpload: {}, {}'.format(self.doi, self.upload)

    def owner(self):
        return self.upload.user


class Scrape(models.Model):

    start_date = models.DateTimeField(
        auto_now_add=True,
    )
    end_date = models.DateTimeField()

    def __str__(self):
        return 'Scrape on: {}'.format(self.start_date)


class Event(models.Model):

    external_id = models.UUIDField(
        unique=True,
        help_text='UUID of the event from the original provider.',
    )
    source_id = models.CharField(
        max_length=250,
        help_text='ID of the event in the source, where it originated.'
    )
    source = models.CharField(
        max_length=250,
        help_text='Short text indicating the social media source of the event.'
    )
    created_at = models.DateTimeField(
        help_text='Time of creation in the social media where it originated.'
    )
    content = models.TextField(
        help_text="Event's content in the social media where it originated."
    )
    scrape = models.ForeignKey(
        Scrape,
        on_delete=models.DO_NOTHING,
        help_text='Scrape process which pulled the event.',
    )
    doi = models.ForeignKey(
        Doi,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return 'Event: {}'.format(self.doi, self.source)

    def owners(self):
        return self.doi.owners()
