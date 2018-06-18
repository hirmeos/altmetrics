from itertools import chain

from django.conf import settings
from django.db.models import Q
from django.utils import timezone

from arrow import utcnow
from celery.utils.log import get_task_logger

from core.celery import app

from .models import Event, Namespace, Scrape, Uri
from .utils import event_generator

logger = get_task_logger(__name__)


@app.task(name='pull-metrics')
def pull_metrics():
    """ Call a scrape for each enabled data source plugin. """

    uri_unprocessed_or_refreshable = Uri.objects.filter(
        Q(last_checked__isnull=True) |
        Q(
            last_checked__lte=utcnow().shift(
                days=-settings.DAYS_BEFORE_REFRESH
            ).datetime
        ),
    )

    if uri_unprocessed_or_refreshable:
        scrape = Scrape.objects.create()

    # TODO: we need a way to check whether the user wants a specific DOI to
    # be in one or more namespaces. For now, we will assume that there is
    # only one namespace and the user wants all his DOIs to be in there.

    for uri in uri_unprocessed_or_refreshable:

        events = event_generator(
            uri=uri,
            namespaces=Namespace.objects.all(),
            scrape=scrape,
        )

        flatten = chain.from_iterable(events)

        try:
            Event.objects.bulk_create(flatten)
        except Exception as e:
            logger.error(e)

    scrape.end_date = timezone.now()
    scrape.save()
