from django.db import models

from django.contrib.auth.models import User


class Event(models.Model):
    """ Hold data related to the events.

    A quick note on terminology:

    provider: the service we are talking to in order to retrieve the event
      (e.g. Crossref Event Data API).

    origin: the service where the event originated (e.g. Twitter).
    """

    value = models.IntegerField(
        default=1,
        help_text='Useful for aggregation.',
    )
    external_id = models.UUIDField(
        unique=True,
        help_text='UUID of the event from the original provider.',
    )
    origin_id = models.CharField(
        max_length=250,
        help_text='ID of the event in the source, where it originated.'
    )
    created_at = models.DateTimeField(
        help_text='Time of creation in the service where it originated.'
    )
    content = models.TextField(
        null=True,
        help_text="Event's content in the service where it originated.",
    )
    uri = models.CharField(
        max_length=255,
    )
    scrape = models.ForeignKey(
        'processor.Scrape',
        on_delete=models.DO_NOTHING,
        help_text='Scrape process which pulled the event.',
    )
    uploader = models.ForeignKey(
        User,
        null=False,
        unique=False,
        on_delete=models.DO_NOTHING,
    )
    country = models.ForeignKey(
        'processor.Country',
        null=True,
        unique=False,
        on_delete=models.DO_NOTHING,
    )
    measure = models.ForeignKey(
        'processor.Measure',
        null=False,
        unique=False,
        on_delete=models.DO_NOTHING,
    )

    # def __str__(self):
    #     return 'Event: {}'.format(self.id, self.measure.source)
