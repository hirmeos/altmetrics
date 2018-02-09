from datetime import datetime

from django.conf import settings
from django.db.models import Q

import arrow

from core.celery import app

from .models import Doi, Event, Scrape


@app.task(name='pull-metrics')
def pull_metrics():
    """ For each enabled data source plugin, call a scrape. """

    dois_unprocessed_or_to_refresh = Doi.objects.filter(
        Q(last_checked__isnull=True),
        Q(last_checked__lte=arrow.utcnow().shift(days=-7).datetime)
    )

    for doi in dois_unprocessed_or_to_refresh:
        for events in (
            settings.AVAILABLE_PLUGINS.get(source).PROVIDER.process(doi)
            for source in settings.AVAILABLE_PLUGINS
        ):
            for event in events:
                Event.objects.get_or_create(
                    external_id=event.get('external_id'),
                    source_id=event.get('source_id'),
                    source=event.get('source'),
                    created_at=event.get('created_at'),
                    content=event.get('content'),
                    doi=doi,
                    scrape=Scrape.objects.create(end_date=datetime.utcnow()),
                )
