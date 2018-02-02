from core.celery import app

import arrow
from datetime import datetime


from django.conf import settings
from django.db.models import Q

from .models import Doi, Event, Scrape


@app.task(name='pull-metrics')
def pull_metrics():
    """ For each enabled data source plugin, call a scrape. """

    dois_unprocessed_or_to_refresh = Doi.objects.filter(
        Q(last_checked__isnull=True) |
        Q(last_checked__lte=arrow.utcnow().shift(days=-7))
    )

    for doi in dois_unprocessed_or_to_refresh:
        for events in (
                source.process(doi)
                for source in settings.AVAILABLE_PLUGINS
        ):
            for event in events:
                m_event = Event.objects.filter(
                    external_id=event.external_id
                ).first()
                if not m_event:
                    Event.objects.create(
                        external_id=event.get('external_id'),
                        source_id=event.get('source_id'),
                        source=event.get('source'),
                        created_at=event.get('created_at'),
                        content=event.get('content'),
                        doi=doi,
                        scrape=Scrape.objects.create(end_date=datetime.utcnow())
                    )
                else:
                    m_event.source_id=event.get('source_id'),
                    m_event.source=event.get('source'),
                    m_event.created_at=event.get('created_at'),
                    m_event.content=event.get('content'),
                    m_event.doi=doi,
                    m_event.scrape.end_date=datetime.utcnow()
                    m_event.save()

