from django.core.validators import RegexValidator
from django.db import models


class Doi(models.Model):

    doi = models.CharField(
        max_length=50,
        unique=True,
        validators=[
            RegexValidator(
                regex='^10.\d{4,9}/[-._;()/:A-Z0-9]+$',
                message='DOI not valid.',
            ),
        ],
    )
    last_upload = models.ForeignKey(
        'importer.CSVUpload',
        null=False,
        unique=False,
        on_delete=models.CASCADE,
    )
    last_checked = models.DateTimeField(
        null=True,
        default=None,
    )


class Url(models.Model):

    url = models.URLField()
    doi = models.ForeignKey(
        Doi,
        on_delete=models.CASCADE,
    )


class Scrape(models.Model):

    start_date = models.DateTimeField(
        auto_now_add=True,
    )
    end_date = models.DateTimeField()


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
