from datetime import datetime

from django.conf import settings
from django.db.models import Q
from django.contrib.auth.models import User

import arrow

from core.celery import app
from celery.utils.log import get_task_logger

from .models import Doi, DoiUpload, Event, Scrape

logger = get_task_logger(__name__)

def users_from_uploads(doi):
    """
      Generates a list of users that uploaded a csv that created the doi

      Parameters:
        doi (Doi): the doi used to generate a list of users from

      Returns:
        A list of users that uploaded a csv with the doi in it.
    """

    uploads = [doiup.upload for doiup in DoiUpload.objects.filter(doi=doi)]
    users = None
    for upload in uploads:
        if users:
            users |= User.objects.filter(csvupload=upload)
        else:
            users = User.objects.filter(csvupload=upload)

    return users


def doi_event_generator(doi):
    """Generator of events for each of the dois being processed

       Calls on every available plugin, and returns events generated for that
       doi by that plugin process method. Plugins can optionally check if they
       are authorised to generate events for the doi, and won't process the doi
       if they aren't, going to the next plugin

       Parameters:
           doi (Doi): the doi which events are fetched for

       Returns:
           yields a list of events for each plugin, which if turned into a list
           will be a list of lists of events.
    """

    for source in settings.AVAILABLE_PLUGINS:
        if hasattr(settings.AVAILABLE_PLUGINS.get(source).PROVIDER, 'is_authorised'):

            users = users_from_uploads(doi)
            if settings.AVAILABLE_PLUGINS.get(source).PROVIDER.is_authorised(users):
                yield settings.AVAILABLE_PLUGINS.get(source).PROVIDER.process(doi)

        else:
            yield settings.AVAILABLE_PLUGINS.get(source).PROVIDER.process(doi)


@app.task(name='pull-metrics')
def pull_metrics():
    """ For each enabled data source plugin, call a scrape. """

    dois_unprocessed_or_to_refresh = Doi.objects.filter(
        Q(last_checked__isnull=True) |
        Q(last_checked__lte=arrow.utcnow().shift(days=-7).datetime)
    )

    for doi in dois_unprocessed_or_to_refresh:

        for events in doi_event_generator(doi):
            for event in events:
                try:
                    Event.objects.get_or_create(
                        external_id=event.get('external_id'),
                        source_id=event.get('source_id'),
                        source=event.get('source'),
                        created_at=event.get('created_at'),
                        content=event.get('content'),
                        doi=doi,
                        scrape=Scrape.objects.create(end_date=datetime.utcnow()),
                    )
                except Exception as e:
                    logger.error(e)
                    print(e)
